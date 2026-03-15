import argparse
import re
import sys

from dnsboard.fetcher import fetch_all
from dnsboard.presets import load_presets, save_preset, delete_preset
from dnsboard.server import run_server


def normalize_domain(domain: str) -> str:
    d = domain.strip().lower()
    d = re.sub(r'^https?://', '', d)
    d = d.rstrip('/')
    d = d.split('/')[0]
    return d


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="dnsboard",
        description="Real-time DNS, SSL, and uptime dashboard for your domains",
    )
    parser.add_argument("domains", nargs="*", help="Domain names to monitor")
    parser.add_argument("--port", type=int, default=8080, help="Server port (default: 8080)")
    parser.add_argument("--no-browser", action="store_true", help="Don't auto-open browser")
    parser.add_argument("--list-presets", action="store_true", help="List saved presets")
    parser.add_argument("--delete-preset", metavar="NAME", help="Delete a saved preset")
    return parser


def interactive_preset_selection() -> list[str] | None:
    presets = load_presets()
    if not presets:
        print("No presets found. Usage: dnsboard domain1.com domain2.com")
        return None

    print("\nSaved presets:")
    names = list(presets.keys())
    for i, name in enumerate(names, 1):
        domains = ", ".join(presets[name])
        print(f"  {i}. {name} ({domains})")

    print()
    try:
        choice = input("Select preset (number) or 'q' to quit: ").strip()
    except (EOFError, KeyboardInterrupt):
        print()
        return None

    if choice.lower() == 'q':
        return None

    try:
        idx = int(choice) - 1
        if 0 <= idx < len(names):
            return presets[names[idx]]
    except ValueError:
        pass

    print("Invalid selection.")
    return None


def maybe_save_preset(domains: list[str]) -> None:
    if not sys.stdin.isatty():
        return
    try:
        answer = input("Save as preset? (y/n): ").strip().lower()
    except (EOFError, KeyboardInterrupt):
        print()
        return

    if answer != 'y':
        return

    try:
        name = input("Preset name: ").strip()
    except (EOFError, KeyboardInterrupt):
        print()
        return

    if not name:
        print("No name given, skipping.")
        return

    save_preset(name, domains)
    print(f"Saved preset '{name}'.")


def main():
    parser = build_parser()
    args = parser.parse_args()

    if args.list_presets:
        presets = load_presets()
        if not presets:
            print("No presets saved.")
        else:
            for name, domains in presets.items():
                print(f"  {name}: {', '.join(domains)}")
        sys.exit(0)

    if args.delete_preset:
        if delete_preset(args.delete_preset):
            print(f"Deleted preset '{args.delete_preset}'.")
        else:
            print(f"Preset '{args.delete_preset}' not found.")
        sys.exit(0)

    if args.domains:
        domains = [normalize_domain(d) for d in args.domains]
    else:
        domains = interactive_preset_selection()
        if not domains:
            sys.exit(1)

    print(f"[*] Fetching data for {len(domains)} domain(s): {', '.join(domains)}")
    data = fetch_all(domains)
    print(f"[+] Data fetched. Starting dashboard...")

    if args.domains:
        maybe_save_preset(domains)

    print(f"[+] Dashboard running at http://localhost:{args.port} — press Ctrl+C to stop.")

    try:
        run_server(domains, args.port, args.no_browser, initial_data=data)
    except KeyboardInterrupt:
        print("\n[*] Shutting down.")


if __name__ == "__main__":
    main()
