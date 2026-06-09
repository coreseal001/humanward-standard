from __future__ import annotations
import json
from dataclasses import dataclass, asdict, field
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import List

class ReviewPriority(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"

@dataclass
class ReviewItem:
    reason: str
    priority: ReviewPriority
    proposed_action: str = ""
    output_text: str = ""
    failed_checks: List[str] = field(default_factory=list)
    safeguards: List[str] = field(default_factory=list)

def enqueue_review(item: ReviewItem, queue_path: str = "humanward_review_queue.jsonl") -> dict:
    record = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "system": "humanward-ai-mvp",
        "system_version": "0.2.0",
        "review_item": {**asdict(item), "priority": item.priority.value},
    }
    with Path(queue_path).open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")
    return record
