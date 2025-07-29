import re
from datetime import datetime, timedelta
from typing import List

TIME_RE = re.compile(r"(\d{4}-\d{2}-\d{2})\s+(\d{1,2}:\d{2}\s*[AP]M)")


def parse_schedule(text: str, days_ahead: int = 7) -> List[datetime]:
    """Parse schedule text and return openings within the next `days_ahead` days."""
    now = datetime.now()
    end = now + timedelta(days=days_ahead)
    openings: List[datetime] = []
    for match in TIME_RE.finditer(text):
        date_str, time_str = match.groups()
        try:
            dt = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %I:%M %p")
        except ValueError:
            continue
        if now <= dt <= end:
            openings.append(dt)
    return openings
