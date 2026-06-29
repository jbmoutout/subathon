#!/usr/bin/env python3
"""
Tiny zero-dependency dev server for the zawathon dashboard.

Serves the static HTML *and* proxies /api/data to the upstream so the
browser sees a single origin -> no CORS, no "(blocked:origin)".

Usage:
    python3 serve.py            # http://localhost:8000/
    python3 serve.py 9000       # custom port
"""
import sys
import urllib.request
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

UPSTREAM = "https://zawathon.ascentcloud.art"
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8000


class Handler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith("/api/"):
            return self.proxy()
        return super().do_GET()

    def proxy(self):
        try:
            req = urllib.request.Request(
                UPSTREAM + self.path,
                headers={"User-Agent": "zawathon-dashboard/1.0"},
            )
            with urllib.request.urlopen(req, timeout=15) as up:
                body = up.read()
                self.send_response(up.status)
                self.send_header(
                    "Content-Type",
                    up.headers.get("Content-Type", "application/json"),
                )
                self.send_header("Content-Length", str(len(body)))
                self.send_header("Cache-Control", "no-store")
                self.end_headers()
                self.wfile.write(body)
        except Exception as e:
            self.send_error(502, f"upstream error: {e}")

    def log_message(self, fmt, *args):  # quieter logs
        sys.stderr.write("%s - %s\n" % (self.address_string(), fmt % args))


if __name__ == "__main__":
    print(f"→ http://localhost:{PORT}/")
    print(f"  proxying /api/* → {UPSTREAM}")
    ThreadingHTTPServer(("127.0.0.1", PORT), Handler).serve_forever()
