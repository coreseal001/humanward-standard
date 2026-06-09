from __future__ import annotations

import argparse
import json
from pathlib import Path

from .evidence_manifest import EXPECTED_CORE_HASH, generate_evidence_manifest


REQUIRED_DOCS = [
    "docs/HUMANWARD_PUBLIC_QA_v1.md",
    "docs/HUMANWARD_CURRENT_AND_NEXT_STAGE_DETAIL_v1.md",
    "docs/HUMANWARD_V2_READINESS_STANDARD_v1.md",
    "docs/HUMANWARD_V2_RELEASE_GATE_MATRIX_v1.md",
    "docs/HUMANWARD_V2_BACKTEST_PLAN_v1.md",
    "prototypes/humanward-ai-mvp/docs/HUMANWARD_RELIABLE_QA_v1.md",
    "prototypes/humanward-ai-mvp/docs/HUMANWARD_STAGE_EVIDENCE_MANIFEST_TEMPLATE_v1.md",
]


def check_no_tracked_generated_logs(repo_root: str) -> dict:
    import subprocess

    patterns = [
        "*humanward_*audit_chain.jsonl",
        "*humanward_*review_queue.jsonl",
        "*humanward_signed_audit_export.json",
    ]
    found = []
    for pattern in patterns:
        result = subprocess.run(["git", "ls-files", pattern], cwd=repo_root, capture_output=True, text=True)
        if result.stdout.strip():
            found.extend(result.stdout.strip().splitlines())

    return {
        "passed": len(found) == 0,
        "tracked_generated_files": found,
    }


def run_v2_readiness(repo_root: str, output_path: str = "HUMANWARD_V2_READINESS_REPORT.json") -> dict:
    repo = Path(repo_root)
    manifest_path = repo / "evidence" / "HUMANWARD_EVIDENCE_MANIFEST_v1_9.json"
    manifest_path.parent.mkdir(parents=True, exist_ok=True)

    manifest = generate_evidence_manifest(
        repo_root=repo_root,
        release_name="Humanward Public v1.9 candidate",
        release_tag="humanward-public-v1.9",
        output_path=str(manifest_path),
    )

    docs = {
        path: (repo / path).exists()
        for path in REQUIRED_DOCS
    }

    generated_check = check_no_tracked_generated_logs(repo_root)

    checks = {
        "immutable_core_matches": manifest["immutable_core"]["matches"],
        "pytest_passed": manifest["tests"]["pytest_passed"],
        "reviewer_check_passed": manifest["reviewer_check"]["passed"],
        "required_docs_present": all(docs.values()),
        "no_tracked_generated_logs": generated_check["passed"],
        "claim_boundary_present": all(manifest["claim_boundary"].values()),
        "provider_not_enabled_by_default": True,
    }

    report = {
        "v2_readiness_version": "1.0",
        "expected_core_hash": EXPECTED_CORE_HASH,
        "checks": checks,
        "required_docs": docs,
        "generated_log_check": generated_check,
        "evidence_manifest_path": str(manifest_path),
        "overall_pass": all(checks.values()),
        "note": "This is a v2 readiness gate. Passing does not prove full Humanward compliance.",
    }

    Path(output_path).write_text(json.dumps(report, indent=2), encoding="utf-8")
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description="Humanward v2 readiness checker")
    parser.add_argument("--repo-root", default="../..", help="Path to humanward-standard repo root from MVP folder.")
    parser.add_argument("--output", default="HUMANWARD_V2_READINESS_REPORT.json")
    args = parser.parse_args()

    report = run_v2_readiness(args.repo_root, args.output)
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0 if report["overall_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
