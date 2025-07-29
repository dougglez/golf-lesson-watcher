"""Simple ntfy.sh notification helper."""

from __future__ import annotations

import os
import requests

DEFAULT_TOPIC = "dougglez_test_alert_12345asdf"

# Allow overriding the topic/URL via environment variables. This makes it easier
# to change where notifications are delivered without modifying the code.
NTFY_TOPIC = os.getenv("NTFY_TOPIC", DEFAULT_TOPIC)
NTFY_URL = os.getenv("NTFY_URL", f"https://ntfy.sh/{NTFY_TOPIC}")


def notify(message: str) -> None:
    """Send a notification using ntfy.sh."""
    try:
        response = requests.post(NTFY_URL, data=message.encode("utf-8"), timeout=10)
        response.raise_for_status()
    except Exception as exc:  # pragma: no cover - network failure
        print(f"Failed to send notification: {exc}")
