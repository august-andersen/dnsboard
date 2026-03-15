import threading
import webbrowser

from flask import Flask, jsonify, Response

from dnsboard.dashboard import get_dashboard_html
from dnsboard.fetcher import fetch_all, fetch_pings


def create_app(domains: list[str], initial_data: dict | None = None) -> Flask:
    app = Flask(__name__)
    app.config["domains"] = domains

    cache = {"data": initial_data or {}}
    lock = threading.Lock()

    @app.route("/")
    def index():
        return Response(get_dashboard_html(), content_type="text/html")

    @app.route("/api/data")
    def api_data():
        with lock:
            data = dict(cache["data"])

        # Re-fetch pings live
        pings = fetch_pings(domains)
        for domain in domains:
            if domain in data and domain in pings:
                data[domain]["ping"] = pings[domain]

        data["_meta"] = {"domains": domains}
        return jsonify(data)

    @app.route("/api/refresh", methods=["POST"])
    def api_refresh():
        new_data = fetch_all(domains)
        with lock:
            cache["data"] = new_data
        new_data["_meta"] = {"domains": domains}
        return jsonify(new_data)

    return app


def run_server(domains: list[str], port: int = 8080, no_browser: bool = False,
               initial_data: dict | None = None) -> None:
    app = create_app(domains, initial_data)

    if not no_browser:
        threading.Timer(1.5, webbrowser.open, args=[f"http://localhost:{port}"]).start()

    import logging
    log = logging.getLogger("werkzeug")
    log.setLevel(logging.WARNING)

    try:
        app.run(host="127.0.0.1", port=port, debug=False)
    except OSError as e:
        if "Address already in use" in str(e):
            print(f"Error: Port {port} is already in use. Try --port <number>.")
        else:
            raise
