"""One-shot B019 competition submit. Delete after use."""

from __future__ import annotations

import time


def main() -> int:
    last_exc: Exception | None = None
    for attempt in range(1, 6):
        try:
            from kaggle.api.kaggle_api_extended import KaggleApi

            api = KaggleApi()
            api.authenticate()
            result = api.competition_submit_code(
                file_name="artifacts/kaggle/B019_v1/submission.csv",
                message="B019-tail995 | attack ac50d36a | prereg df44041 | SDK 3.1.2",
                competition="ai-agent-security-multi-step-tool-attacks",
                kernel="heralces/ai-agent-security-b019-tail995",
                kernel_version=1,
            )
            print("result", result)
            last_exc = None
            break
        except Exception as exc:  # noqa: BLE001
            last_exc = exc
            print(f"attempt {attempt} ERROR {exc}")
            time.sleep(10 * attempt)
    if last_exc is not None:
        raise last_exc
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
