from __future__ import annotations

import schedule
import time
import typer

from .config import load_config
from .scheduler import ScheddyClient

app = typer.Typer(help="Check your coach's schedule for openings")


@app.command()
def check(days: int = 7) -> None:
    """Run a single check for openings."""
    cfg = load_config()
    client = ScheddyClient(cfg)
    client.check_and_notify(days)


@app.command()
def run(interval_minutes: int = 15, days: int = 7) -> None:
    """Run continuous checks every `interval_minutes`."""
    cfg = load_config()
    client = ScheddyClient(cfg)

    def job() -> None:
        client.check_and_notify(days)

    schedule.every(interval_minutes).minutes.do(job)
    typer.echo(f"Watching for openings every {interval_minutes} minutes...")
    job()
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    app()
