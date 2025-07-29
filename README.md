# Golf Lesson Watcher

This tool checks your coach's lesson schedule for last-minute openings and sends a notification via [ntfy.sh](https://ntfy.sh/).

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Set the following environment variables:
   - `SCHEDDY` – URL of the schedule page.
   - `Coach` – your coach's name.
   - `SCHEDDY_USER` and `SCHEDDY_PASS` – (optional) credentials for the site. If provided, the watcher will log in automatically.
   - `OPENAI_API_KEY` – required if the schedule parsing uses LLMs.
   - `USE_LLM=1` – (optional) enable LLM-based parsing via LangChain.
   - `NTFY_TOPIC` – (optional) ntfy topic name. Defaults to `dougglez_test_alert_12345asdf`.
   - `NTFY_URL` – (optional) override the full ntfy URL.

## Usage

Run a single check:

```bash
python -m lesson_watcher.main check
```

Run continuously every 15 minutes:

```bash
python -m lesson_watcher.main run --interval-minutes 15
```

Notifications are sent to the topic `dougglez_test_alert_12345asdf` on `ntfy.sh`.
If login fails, the command will raise `RuntimeError: Login failed: schedule page still shows login screen`.
