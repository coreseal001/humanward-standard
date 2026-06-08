from __future__ import annotations

import argparse
import json
from dataclasses import asdict
from .models import ActionRequest
from .agent import HumanwardAgent


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Humanward AI MVP action gate CLI")
    parser.add_argument("--action", required=True, help="Proposed action to evaluate")
    parser.add_argument("--benefit", required=True, help="Claimed human benefit")
    parser.add_argument("--user-request", default="", help="Original user request")
    parser.add_argument("--harms", default="", help="Possible harms")
    parser.add_argument("--data", default="", help="Data involved")
    parser.add_argument("--personal-data", action="store_true", help="Whether personal data is involved")
    parser.add_argument("--consent", default="", help="Consent or authority basis")
    parser.add_argument("--tool", default="none", help="External tool/action requested")
    parser.add_argument("--reversibility", default="unknown", choices=["reversible", "partly_reversible", "irreversible", "unknown"])
    parser.add_argument("--urgency", default="unknown", choices=["low", "medium", "high", "emergency", "unknown"])
    parser.add_argument("--confidence", default="unknown", choices=["low", "medium", "high", "unknown"])
    parser.add_argument("--log", default="humanward_audit_log.jsonl", help="Audit log path")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    req = ActionRequest(
        proposed_action=args.action,
        claimed_human_benefit=args.benefit,
        user_request=args.user_request,
        possible_harms=args.harms,
        data_used=args.data,
        personal_data_involved=args.personal_data,
        consent_basis=args.consent,
        tool_or_external_action=args.tool,
        reversibility=args.reversibility,
        urgency=args.urgency,
        confidence_level=args.confidence,
    )
    agent = HumanwardAgent(audit_log_path=args.log)
    decision = agent.evaluate(req)

    output = {
        "request": asdict(req),
        "decision": {
            "decision": decision.decision.value,
            "reason": decision.reason,
            "failed_checks": decision.failed_checks,
            "safeguards": decision.safeguards,
            "audit_hash": decision.audit_hash,
        },
    }
    print(json.dumps(output, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
