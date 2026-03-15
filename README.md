# dnsboard

Real-time DNS, SSL, and uptime dashboard for your domains.

Run `dnsboard example.com` and a browser opens with a live monitoring dashboard.

## Installation

```bash
git clone <repo-url> && cd dnsboard
pip install .
```

## Usage

```bash
# Monitor specific domains
dnsboard example.com mysite.org

# Run without arguments to use a saved preset
dnsboard

# Options
dnsboard --port 9090 example.com       # Custom port
dnsboard --no-browser example.com      # Don't auto-open browser
dnsboard --list-presets                 # List saved presets
dnsboard --delete-preset my-apps       # Delete a preset
```

On first run with domains, you'll be prompted to save them as a preset for quick access later.

## What it monitors

- **DNS Records** — A, AAAA, MX, NS, TXT, CNAME, SOA
- **SSL Certificates** — issuer, expiry date, days remaining (alerts at <30 days)
- **WHOIS** — registrar, creation/expiry dates (alerts at <60 days)
- **Uptime** — live HTTP ping every 30 seconds with response time

## License

MIT
