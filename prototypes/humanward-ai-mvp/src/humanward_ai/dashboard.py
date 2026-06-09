from __future__ import annotations

import argparse
import html
import json
from pathlib import Path
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer


def read_jsonl(path: str, limit: int = 50) -> list[dict]:
    p = Path(path)
    if not p.exists():
        return []
    rows = []
    with p.open("r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                try:
                    rows.append(json.loads(line))
                except json.JSONDecodeError:
                    rows.append({"invalid_json": line.strip()})
    return rows[-limit:]


def render_dashboard(audit_path: str, review_path: str) -> str:
    audits = read_jsonl(audit_path)
    reviews = read_jsonl(review_path)

    def pre(obj):
        return "<pre>" + html.escape(json.dumps(obj, indent=2, ensure_ascii=False)) + "</pre>"

    audit_html = "\n".join(pre(a) for a in audits) or "<p>No audit records found.</p>"
    review_html = "\n".join(pre(r) for r in reviews) or "<p>No review records found.</p>"

    return f"""<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <title>Humanward Local Audit Dashboard</title>
  <style>
    body {{ font-family: Arial, sans-serif; margin: 24px; }}
    pre {{ background: #f4f4f4; padding: 12px; overflow-x: auto; }}
    .warning {{ border: 1px solid #999; padding: 12px; }}
  </style>
</head>
<body>
  <h1>Humanward Local Audit Dashboard</h1>
  <div class="warning">
    Local review tool only. Do not expose publicly without authentication, access controls, and security review.
  </div>
  <h2>Audit Chain</h2>
  {audit_html}
  <h2>Review Queue</h2>
  {review_html}
</body>
</html>"""


class DashboardHandler(BaseHTTPRequestHandler):
    audit_path = "humanward_audit_chain.jsonl"
    review_path = "humanward_review_queue.jsonl"

    def do_GET(self):
        if self.path not in {"/", "/dashboard"}:
            self.send_response(404)
            self.end_headers()
            return

        body = render_dashboard(self.audit_path, self.review_path).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def main() -> int:
    parser = argparse.ArgumentParser(description="Humanward local audit/review dashboard")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8767)
    parser.add_argument("--audit-log", default="humanward_audit_chain.jsonl")
    parser.add_argument("--review-queue", default="humanward_review_queue.jsonl")
    args = parser.parse_args()

    DashboardHandler.audit_path = args.audit_log
    DashboardHandler.review_path = args.review_queue

    if args.host not in {"127.0.0.1", "localhost"}:
        print("WARNING: Dashboard should not be exposed publicly without security review.")

    server = ThreadingHTTPServer((args.host, args.port), DashboardHandler)
    print(f"Humanward dashboard running at http://{args.host}:{args.port}")
    print("Press Ctrl+C to stop.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping.")
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
