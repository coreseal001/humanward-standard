from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

EXPECTED_CORE_HASH = "5af88d97cc43303cf5b84211e5b06e7c5feddd006329c16bc8135836354d3629"


def sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with Path(path).open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def run_command(args: list[str], cwd: Optional[str] = None) -> dict:
    completed = subprocess.run(args, cwd=cwd, capture_output=True, text=True)
    return {
        "args": args,
        "cwd": cwd,
        "returncode": completed.returncode,
        "stdout": completed.stdout,
        "stderr": completed.stderr,
    }


def get_git_value(args: list[str], repo_root: str) -> str:
    result = run_command(["git", *args], cwd=repo_root)
    if result["returncode"] != 0:
        return ""
    return result["stdout"].strip()


def generate_evidence_manifest(
    repo_root: str,
    release_name: str = "Humanward v1.9 candidate",
    release_tag: str = "humanward-public-v1.9",
    output_path: str = "HUMANWARD_EVIDENCE_MANIFEST.json",
) -> dict:
    repo = Path(repo_root).resolve()
    core_path = repo / "core" / "IMMUTABLE_CORE.md"
    mvp_path = repo / "prototypes" / "humanward-ai-mvp"

    core_hash = sha256_file(str(core_path)) if core_path.exists() else ""

    pytest_result = run_command([sys.executable, "-m", "pytest"], cwd=str(mvp_path))
    reviewer_result = run_command([sys.executable, "-m", "humanward_ai.reviewer_check"], cwd=str(mvp_path))

    manifest = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "release_name": release_name,
        "release_tag": release_tag,
        "release_commit": get_git_value(["rev-parse", "--short", "HEAD"], str(repo)),
        "git_status": get_git_value(["status", "--short"], str(repo)),
        "python_executable": sys.executable,
        "immutable_core": {
            "path": "core/IMMUTABLE_CORE.md",
            "expected_sha256": EXPECTED_CORE_HASH,
            "actual_sha256": core_hash,
            "matches": core_hash.lower() == EXPECTED_CORE_HASH,
        },
        "tests": {
            "pytest_returncode": pytest_result["returncode"],
            "pytest_passed": pytest_result["returncode"] == 0,
            "stdout": pytest_result["stdout"],
            "stderr": pytest_result["stderr"],
        },
        "reviewer_check": {
            "returncode": reviewer_result["returncode"],
            "passed": reviewer_result["returncode"] == 0,
            "stdout": reviewer_result["stdout"],
            "stderr": reviewer_result["stderr"],
        },
        "claim_boundary": {
            "no_endorsement_claim": True,
            "no_certification_claim": True,
            "no_full_compliance_claim": True,
            "not_production_readiness_claim": True,
        },
        "known_limitations": [
            "Local MVP only.",
            "No full Humanward compliance claim.",
            "No real provider enabled by default.",
            "Audit chain is not yet public notarization.",
            "Tests are evidence, not proof of all possible behavior.",
        ],
    }

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    Path(output_path).write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return manifest
