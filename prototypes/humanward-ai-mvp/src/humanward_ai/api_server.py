from __future__ import annotations

import argparse
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from .agent_v02 import HumanwardAgentV02
from .models import ActionRequest
from .model_adapter import ModelRequest, get_model_adapter
from .safe_sharing import classify_sharing
from .audit_chain import verify_audit_chain


class HumanwardHandler(BaseHTTPRequestHandler):
    server_version = "HumanwardLocalDemo/0.1"

    def _send_json(self, status: int, payload: dict) -> None:
        body = json.dumps(payload, indent=2, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path == "/health":
            self._send_json(200, {
                "status": "ok",
                "service": "humanward-local-controlled-demo",
                "warning": "Localhost demo only. Do not expose publicly without security review.",
            })
            return

        self._send_json(404, {"error": "not_found"})

    def do_POST(self):
        if self.path != "/demo":
            self._send_json(404, {"error": "not_found"})
            return

        try:
            length = int(self.headers.get("Content-Length", "0"))
            raw = self.rfile.read(length).decode("utf-8")
            data = json.loads(raw or "{}")

            action = data.get("action", "")
            benefit = data.get("benefit", "")
            draft_output = data.get("draft_output", "")
            provider_name = data.get("provider", "stub")

            if not action or not benefit:
                self._send_json(400, {"error": "action and benefit are required"})
                return

            req = ActionRequest(
                proposed_action=action,
                claimed_human_benefit=benefit,
                personal_data_involved=bool(data.get("personal_data", False)),
                tool_or_external_action=data.get("tool", "none"),
                reversibility=data.get("reversibility", "reversible"),
                urgency=data.get("urgency", "low"),
                confidence_level=data.get("confidence", "high"),
            )

            if draft_output:
                draft = draft_output
                provider = "manual"
                model_name = "manual-draft"
            else:
                adapter = get_model_adapter(provider_name)
                response = adapter.generate(ModelRequest(prompt=action))
                draft = response.text
                provider = response.provider
                model_name = response.model_name

            audit_log = "humanward_api_audit_chain.jsonl"
            review_queue = "humanward_api_review_queue.jsonl"

            agent = HumanwardAgentV02(audit_log, review_queue)
            decision = agent.evaluate_and_verify(req, draft)
            sharing = classify_sharing(draft)

            self._send_json(200, {
                "model": {
                    "provider": provider,
                    "model_name": model_name,
                    "external_call": False,
                },
                "draft_output": draft,
                "humanward_decision": decision,
                "sharing_classification": {
                    "decision": sharing.decision.value,
                    "reason": sharing.reason,
                    "risk_flags": sharing.risk_flags,
                    "required_controls": sharing.required_controls,
                },
                "audit_chain_valid": verify_audit_chain(audit_log),
            })
        except Exception as exc:
            self._send_json(500, {"error": type(exc).__name__, "message": str(exc)})


def main() -> int:
    parser = argparse.ArgumentParser(description="Humanward local controlled demo API")
    parser.add_argument("--host", default="127.0.0.1", help="Bind host. Default localhost only.")
    parser.add_argument("--port", type=int, default=8766, help="Bind port.")
    args = parser.parse_args()

    if args.host not in {"127.0.0.1", "localhost"}:
        print("WARNING: This demo should not be exposed publicly without security review.")

    server = ThreadingHTTPServer((args.host, args.port), HumanwardHandler)
    print(f"Humanward local demo API running at http://{args.host}:{args.port}")
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
