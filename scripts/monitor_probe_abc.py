"""Poll the ABC gpt-oss probe kernel, then download probe_abc.json."""

from __future__ import annotations

import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

KERNEL = "heralces/ai-agent-security-probe-abc-gptoss"
LOG_PATH = Path("evidence/probe_abc_monitor.log")
OUT_DIR = Path("artifacts/kaggle/probe_abc_v1")
INTERVAL_S = 60
MAX_CHECKS = 40


def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")  # noqa: UP017


def _log(line: str) -> None:
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with LOG_PATH.open("a", encoding="utf-8") as handle:
        handle.write(line + "\n")
    print(line, flush=True)


def main() -> int:
    from kaggle.api.kaggle_api_extended import KaggleApi

    api = KaggleApi()
    api.authenticate()
    _log(f"[{_now()}] start kernel={KERNEL}")
    for check in range(1, MAX_CHECKS + 1):
        try:
            status = api.kernels_status(KERNEL)
            payload = status if isinstance(status, dict) else {"raw": repr(status)}
            text = json.dumps(payload, default=str)
            _log(f"[{_now()}] check {check}/{MAX_CHECKS} {text[:500]}")
        except Exception as exc:  # noqa: BLE001
            _log(f"[{_now()}] check {check}/{MAX_CHECKS} ERROR {exc}")
            text = ""
        if "COMPLETE" in text and "FAILURE" not in text and "ERROR" not in text:
            OUT_DIR.mkdir(parents=True, exist_ok=True)
            try:
                api.kernels_output(KERNEL, str(OUT_DIR), force=True)
                _log(f"[{_now()}] downloaded output to {OUT_DIR}")
            except Exception as exc:  # noqa: BLE001
                _log(f"[{_now()}] download ERROR {exc}")
            print("DONE", flush=True)
            return 0
        if any(token in text for token in ("ERROR", "FAILURE", "CANCELLED")):
            print("FAILED", flush=True)
            return 1
        if check < MAX_CHECKS:
            time.sleep(INTERVAL_S)
    _log(f"[{_now()}] TIMEOUT")
    print("TIMEOUT", flush=True)
    return 1


if __name__ == "__main__":
    sys.exit(main())
