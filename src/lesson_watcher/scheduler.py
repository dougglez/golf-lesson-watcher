from __future__ import annotations

import os
import requests
from bs4 import BeautifulSoup  # type: ignore
from datetime import datetime, timedelta
from typing import List
from urllib.parse import urljoin

from .config import Config
from .parser import parse_schedule
from .agent import ScheduleAgent
from .notifier import notify


class ScheddyClient:
    def __init__(self, config: Config):
        self.config = config
        self.session = requests.Session()

    def login(self) -> None:
        """Login to the scheduling site if credentials are provided."""
        if not self.config.username or not self.config.password:
            return
        resp = self.session.get(self.config.url, timeout=30)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")
        form = soup.find("form")
        if not form:
            return
        action = form.get("action", self.config.url)
        token = form.find("input", {"name": "__RequestVerificationToken"})
        alias = form.find("input", {"name": "Alias"})
        data = {
            "UserName": self.config.username,
            "Password": self.config.password,
        }
        if token and token.get("value"):
            data["__RequestVerificationToken"] = token["value"]
        if alias and alias.get("value"):
            data["Alias"] = alias["value"]
        login_url = urljoin(self.config.url, action)
        resp = self.session.post(login_url, data=data, timeout=30)
        resp.raise_for_status()

    def fetch_schedule(self) -> str:
        """Fetch raw schedule HTML or text for the configured coach."""
        self.login()
        resp = self.session.get(self.config.url, timeout=30)
        resp.raise_for_status()
        if "Login" in resp.text and "Password" in resp.text:
            raise RuntimeError(
                "Login failed: schedule page still shows login screen"
            )
        return resp.text

    def find_openings(self, days_ahead: int = 7) -> List[datetime]:
        html = self.fetch_schedule()
        text = BeautifulSoup(html, "html.parser").get_text(" ")

        if os.getenv("USE_LLM"):
            try:
                agent = ScheduleAgent()
                outputs = agent(text)
                openings = [datetime.fromisoformat(o) for o in outputs]
                return [dt for dt in openings if dt <= datetime.now() + timedelta(days=days_ahead)]
            except Exception:
                pass

        return parse_schedule(text, days_ahead)

    def check_and_notify(self, days_ahead: int = 7) -> List[datetime]:
        openings = self.find_openings(days_ahead)
        if openings:
            formatted = "\n".join(dt.strftime("%Y-%m-%d %I:%M %p") for dt in openings)
            notify(f"Openings found:\n{formatted}")
        return openings
