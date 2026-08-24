"""Poll B018-fastharmony submission 55737814 until terminal. No Kaggle writes."""

from __future__ import annotations

import sys
import time
from datetime import datetime, timezone
from pathlib import Path

COMPETITION = "ai-agent-security-multi-step-tool-attacks"
SUBMISSION_REF = "55737814"
LOG_PATH = Path("evidence/b018_monitor.log")
INTERVAL_S = 20 * 60
MAX_CHECKS = 48  # 16 hours


def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")  # noqa: UP017


def _log(line: str) -> None:
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with LOG_PATH.open("a", encoding="utf-8") as handle:
        handle.write(line + "\n")
    print(line, flush=True)


def _status() -> tuple[str, str, str]:
    from kaggle.api.kaggle_api_extended import KaggleApi

    api = KaggleApi()
    api.authenticate()
    for submission in api.competition_submissions(COMPETITION):
        if str(submission.ref) == SUBMISSION_REF:
            return (
                str(submission.status),
                str(submission.public_score or ""),
                str(submission.error_description or ""),
            )
    return ("MISSING", "", "")


def main() -> int:
    _log(f"[{_now()}] start ref={SUBMISSION_REF} interval={INTERVAL_S}s max={MAX_CHECKS}")
    terminal_tokens = (
        "SubmissionStatus.COMPLETE",
        "SubmissionStatus.ERROR",
        "SubmissionStatus.FAILED",
        "COMPLETE",
        "ERROR",
        "FAILED",
    )
    for check in range(1, MAX_CHECKS + 1):
        try:
            status, score, err = _status()
            _log(
                f"[{_now()}] check {check}/{MAX_CHECKS} "
                f"status={status} public={score!r} err={err!r}"
            )
        except Exception as exc:  # noqa: BLE001
            _log(f"[{_now()}] check {check}/{MAX_CHECKS} ERROR {exc}")
            status, score = "", ""
        if any(token in str(status) for token in terminal_tokens):
            _log(f"[{_now()}] TERMINAL status={status} public={score!r}")
            print("DONE", flush=True)
            return 0
        if check < MAX_CHECKS:
            time.sleep(INTERVAL_S)
    _log(f"[{_now()}] TIMEOUT after {MAX_CHECKS} checks")
    print("TIMEOUT", flush=True)
    return 1


if __name__ == "__main__":
    sys.exit(main())
