import socket
import ssl
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone

import dns.resolver
import requests
import whois


def _serialize_date(d):
    if isinstance(d, list):
        d = d[0] if d else None
    if isinstance(d, datetime):
        return d.isoformat()
    return str(d) if d else None


def fetch_dns(domain: str) -> dict:
    records = {}
    resolver = dns.resolver.Resolver()
    resolver.lifetime = 5

    record_types = ["A", "AAAA", "MX", "NS", "TXT", "CNAME", "SOA"]
    for rtype in record_types:
        try:
            answers = resolver.resolve(domain, rtype)
            if rtype == "MX":
                records[rtype] = [
                    {"priority": r.preference, "exchange": str(r.exchange)}
                    for r in answers
                ]
            elif rtype == "SOA":
                r = list(answers)[0]
                records[rtype] = {
                    "mname": str(r.mname),
                    "rname": str(r.rname),
                    "serial": r.serial,
                    "refresh": r.refresh,
                    "retry": r.retry,
                    "expire": r.expire,
                    "minimum": r.minimum,
                }
            else:
                records[rtype] = [str(r) for r in answers]
        except dns.resolver.NXDOMAIN:
            return {"error": "Domain does not exist"}
        except (dns.resolver.NoAnswer, dns.resolver.NoNameservers):
            continue
        except dns.exception.Timeout:
            if not records:
                return {"error": "DNS query timed out"}
            break
        except Exception:
            continue

    return records


def fetch_ssl(domain: str) -> dict:
    try:
        ctx = ssl.create_default_context()
        with socket.create_connection((domain, 443), timeout=5) as sock:
            with ctx.wrap_socket(sock, server_hostname=domain) as ssock:
                cert = ssock.getpeercert()

        subject = dict(x[0] for x in cert.get("subject", []))
        issuer = dict(x[0] for x in cert.get("issuer", []))

        not_before = datetime.strptime(cert["notBefore"], "%b %d %H:%M:%S %Y %Z")
        not_after = datetime.strptime(cert["notAfter"], "%b %d %H:%M:%S %Y %Z")
        days_until_expiry = (not_after - datetime.now(timezone.utc).replace(tzinfo=None)).days

        return {
            "issuer": issuer.get("organizationName", issuer.get("commonName", "Unknown")),
            "subject": subject.get("commonName", "Unknown"),
            "valid_from": not_before.isoformat(),
            "valid_to": not_after.isoformat(),
            "days_until_expiry": days_until_expiry,
        }
    except ssl.SSLCertVerificationError as e:
        return {"error": f"SSL verification failed: {e}"}
    except socket.timeout:
        return {"error": "SSL connection timed out"}
    except ConnectionRefusedError:
        return {"error": "No SSL (port 443 refused)"}
    except socket.gaierror:
        return {"error": "Could not resolve hostname"}
    except Exception as e:
        return {"error": str(e)}


def fetch_whois(domain: str) -> dict:
    try:
        w = whois.whois(domain)
        expiration = w.expiration_date
        if isinstance(expiration, list):
            expiration = expiration[0]

        days_until_expiry = None
        if expiration and isinstance(expiration, datetime):
            now = datetime.now(timezone.utc)
            if expiration.tzinfo is None:
                expiration = expiration.replace(tzinfo=timezone.utc)
            days_until_expiry = (expiration - now).days

        return {
            "registrar": w.registrar,
            "creation_date": _serialize_date(w.creation_date),
            "expiration_date": _serialize_date(w.expiration_date),
            "updated_date": _serialize_date(w.updated_date),
            "name_servers": list(w.name_servers) if w.name_servers else [],
            "days_until_expiry": days_until_expiry,
        }
    except Exception as e:
        return {"error": str(e)}


def fetch_ping(domain: str) -> dict:
    timestamp = datetime.now(timezone.utc).isoformat()
    for scheme in ("https", "http"):
        url = f"{scheme}://{domain}"
        try:
            resp = requests.get(url, timeout=10, allow_redirects=True,
                                headers={"User-Agent": "dnsboard/0.1"})
            return {
                "is_up": resp.status_code < 500,
                "status_code": resp.status_code,
                "response_time_ms": round(resp.elapsed.total_seconds() * 1000, 1),
                "url": url,
                "timestamp": timestamp,
            }
        except requests.exceptions.SSLError:
            if scheme == "https":
                continue
            return {"is_up": False, "error": "SSL error", "timestamp": timestamp}
        except requests.exceptions.ConnectionError:
            if scheme == "https":
                continue
            return {"is_up": False, "error": "Connection failed", "timestamp": timestamp}
        except requests.exceptions.Timeout:
            return {"is_up": False, "error": "Request timed out", "timestamp": timestamp}
        except Exception as e:
            return {"is_up": False, "error": str(e), "timestamp": timestamp}

    return {"is_up": False, "error": "Could not connect", "timestamp": timestamp}


PUBLIC_RESOLVERS = [
    ("Google", "8.8.8.8"),
    ("Cloudflare", "1.1.1.1"),
    ("Quad9", "9.9.9.9"),
    ("OpenDNS", "208.67.222.222"),
    ("AdGuard", "94.140.14.14"),
]


def fetch_dns_propagation(domain: str) -> list[dict]:
    results = []

    def query_resolver(name, ip):
        r = dns.resolver.Resolver()
        r.nameservers = [ip]
        r.lifetime = 5
        try:
            answers = r.resolve(domain, "A")
            return {
                "resolver": name,
                "ip": ip,
                "records": sorted([str(a) for a in answers]),
                "status": "ok",
            }
        except dns.resolver.NXDOMAIN:
            return {"resolver": name, "ip": ip, "records": [], "status": "nxdomain"}
        except dns.exception.Timeout:
            return {"resolver": name, "ip": ip, "records": [], "status": "timeout"}
        except Exception as e:
            return {"resolver": name, "ip": ip, "records": [], "status": str(e)}

    with ThreadPoolExecutor(max_workers=len(PUBLIC_RESOLVERS)) as pool:
        futures = {pool.submit(query_resolver, name, ip): name
                   for name, ip in PUBLIC_RESOLVERS}
        for fut in as_completed(futures):
            results.append(fut.result())

    # Check consistency
    ok_records = [set(r["records"]) for r in results if r["status"] == "ok" and r["records"]]
    consistent = len(ok_records) > 1 and all(s == ok_records[0] for s in ok_records)
    for r in results:
        r["consistent"] = consistent

    return results


def fetch_all(domains: list[str]) -> dict:
    results = {d: {} for d in domains}
    max_workers = min(len(domains) * 4, 20)

    with ThreadPoolExecutor(max_workers=max_workers) as pool:
        futures = {}
        for domain in domains:
            for name, func in [("dns", fetch_dns), ("ssl", fetch_ssl),
                               ("whois", fetch_whois), ("ping", fetch_ping),
                               ("propagation", fetch_dns_propagation)]:
                fut = pool.submit(func, domain)
                futures[fut] = (domain, name)

        for fut in as_completed(futures):
            domain, name = futures[fut]
            try:
                results[domain][name] = fut.result()
            except Exception as e:
                results[domain][name] = {"error": str(e)}

    return results


def fetch_pings(domains: list[str]) -> dict:
    results = {}
    with ThreadPoolExecutor(max_workers=min(len(domains), 10)) as pool:
        futures = {pool.submit(fetch_ping, d): d for d in domains}
        for fut in as_completed(futures):
            domain = futures[fut]
            try:
                results[domain] = fut.result()
            except Exception as e:
                results[domain] = {"is_up": False, "error": str(e),
                                   "timestamp": datetime.now(timezone.utc).isoformat()}
    return results
