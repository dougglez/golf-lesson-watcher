import os
from dataclasses import dataclass


def _strip_quotes(value: str | None) -> str | None:
    if not value:
        return value
    return (
        value.strip()
        .strip('"')
        .strip("'")
        .strip("“")
        .strip("”")
        .strip()
    )


@dataclass
class Config:
    url: str
    coach: str
    username: str | None = None
    password: str | None = None


def load_config() -> Config:
    url = _strip_quotes(os.getenv("SCHEDDY"))
    coach = _strip_quotes(os.getenv("Coach")) or _strip_quotes(os.getenv("COACH"))
    username = _strip_quotes(os.getenv("SCHEDDY_USER")) or _strip_quotes(os.getenv("USERNAME"))
    password = _strip_quotes(os.getenv("SCHEDDY_PASS")) or _strip_quotes(os.getenv("PASSWORD"))

    if not url or not coach:
        raise ValueError("SCHEDDY and Coach environment variables must be set")

    return Config(url=url, coach=coach, username=username, password=password)
