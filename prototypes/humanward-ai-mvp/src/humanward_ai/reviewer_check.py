from __future__ import annotations

import json
from pathlib import Path

from .red_team_pack import run_red_team_pack
from .audit_chain import verify_audit_chain
from .provider_guardrail import ProviderRequest, evaluate_provider_request


def run_reviewer_check(base_dir: str = ".") -> dict:
    base = Path(base_dir)
    audit = base / "humanward_reviewer_audit_chain.jsonl"
    review = base / "humanward_reviewer_review_queue.jsonl"

    red_team = run_red_team_pack(str(audit), str(review))
    audit_valid = verify_audit_chain(str(audit))

    local_provider = evaluate_provider_request(ProviderRequest(provider_name="stub", external_call=False))
    unsafe_provider = evaluate_provider_request(
        ProviderRequest(
            provider_name="external-unknown",
            external_call=True,
            sends_user_data=True,
            allows_training_use=True,
            has_api_key=True,
        )
    )

    provider_checks_pass = (
        local_provider.decision.value == "ALLOW_LOCAL_ONLY"
        and unsafe_provider.decision.value == "BLOCK"
    )

    result = {
        "red_team": red_team,
        "audit_chain_valid": audit_valid,
        "provider_guardrail": {
            "local_provider_decision": local_provider.decision.value,
            "unsafe_provider_decision": unsafe_provider.decision.value,
            "passed": provider_checks_pass,
        },
        "overall_pass": bool(red_team["overall_pass"] and audit_valid and provider_checks_pass),
    }

    return result


def main() -> int:
    result = run_reviewer_check()
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result["overall_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
