from datetime import datetime, timedelta

from lesson_watcher.parser import parse_schedule


def test_parse_schedule():
    future = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d %I:%M %p")
    text = f"Available slot: {future}"
    result = parse_schedule(text, days_ahead=2)
    assert len(result) == 1
    assert result[0].strftime("%Y-%m-%d %I:%M %p") == future
