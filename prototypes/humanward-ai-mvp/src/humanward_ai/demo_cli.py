from __future__ import annotations

import argparse
import json

from .agent_v02 import HumanwardAgentV02
from .models import ActionRequest
from .model_adapter import ModelRequest, get_model_adapter
from .safe_sharing import classify_sharing
from .audit_chain import verify_audit_chain


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Humanward local controlled demo CLI")
    parser.add_argument("--action", required=True, help="Proposed action to evaluate")
    parser.add_argument("--benefit", required=True, help="Claimed human benefit")
    parser.add_argument("--draft-output", default="", help="Optional draft output to verify directly")
    parser.add_argument("--provider", default="stub", choices=["stub", "echo"], help="Local model adapter")
    parser.add_argument("--personal-data", action="store_true", help="Whether personal data is involved")
    parser.add_argument("--tool", default="none", help="Tool or external action")
    parser.add_argument("--reversibility", default="reversible", choices=["reversible", "partly_reversible", "irreversible", "unknown"])
    parser.add_argument("--urgency", default="low", choices=["low", "medium", "high", "emergency", "unknown"])
    parser.add_argument("--confidence", default="high", choices=["low", "medium", "high", "unknown"])
    parser.add_argument("--audit-log", default="humanward_audit_chain.jsonl")
    parser.add_argument("--review-queue", default="humanward_review_queue.jsonl")
    return parser


def main() -> int:
    args = build_parser().parse_args()

    req = ActionRequest(
        proposed_action=args.action,
        claimed_human_benefit=args.benefit,
        personal_data_involved=args.personal_data,
        tool_or_external_action=args.tool,
        reversibility=args.reversibility,
        urgency=args.urgency,
        confidence_level=args.confidence,
    )

    if args.draft_output:
        draft = args.draft_output
        provider = "manual"
        model_name = "manual-draft"
    else:
        adapter = get_model_adapter(args.provider)
        response = adapter.generate(ModelRequest(prompt=args.action))
        draft = response.text
        provider = response.provider
        model_name = response.model_name

    agent = HumanwardAgentV02(
        audit_chain_path=args.audit_log,
        review_queue_path=args.review_queue,
    )
    decision = agent.evaluate_and_verify(req, draft)
    sharing = classify_sharing(draft)
    audit_chain_valid = verify_audit_chain(args.audit_log)

    output = {
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
        "audit_chain_valid": audit_chain_valid,
    }

    print(json.dumps(output, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
