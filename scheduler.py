"""
Adaptive Revision Agent — rule-based decision: schedule revision when retention is low.
IF retention < threshold THEN revision required.
"""
from datetime import date, datetime
from typing import Any, Dict, Optional

import math

from memory_model import forgetting_rate, memory_retention

REVISION_THRESHOLD = 0.60  # 60% — below this, revise


def parse_date(s: str) -> date:
    return datetime.strptime(s.strip(), "%Y-%m-%d").date()


def days_between(start: date, end: date) -> float:
    return float((end - start).days)


def needs_revision(
    row: Dict[str, Any],
    today: date,
    threshold: float = REVISION_THRESHOLD,
) -> bool:
    """
    Decide if a concept needs revision today.
    Uses decay since last_reviewed, or forced next_review_due.
    """
    last = parse_date(str(row["last_reviewed"]))
    forced = row.get("next_review_due", "")
    if forced is not None:
        fs = str(forced).strip()
        if fs and fs.lower() not in ("nan", ""):
            due = parse_date(fs)
            if today >= due:
                return True

    d = days_between(last, today)
    diff = str(row.get("difficulty", "Medium"))
    r = memory_retention(d, diff)
    return r < threshold


def estimated_days_until_threshold(difficulty: str, threshold: float = REVISION_THRESHOLD) -> Optional[int]:
    """Rough days until R(t) falls below threshold (for explanation in reports)."""
    k = forgetting_rate(difficulty)
    if k <= 0:
        return None
    # e^(-k t) = threshold  =>  t = -ln(threshold) / k
    t = -math.log(threshold) / k
    return max(0, int(round(t)))
