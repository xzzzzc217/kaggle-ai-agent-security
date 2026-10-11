"""One-shot B019 kernel output download. Delete after use."""

from __future__ import annotations

import hashlib
import time
from pathlib import Path

DEST = Path("artifacts/kaggle/B019_v1")
EXPECTED = "ac50d36a21f2dc53d2cbe53e13daa95fe4a90c55ba2467e27a6294d7affd0f37"
KERNEL = "heralces/ai-agent-security-b019-tail995"


def main() -> int:
    DEST.mkdir(parents=True, exist_ok=True)
    last_exc: Exception | None = None
    for attempt in range(1, 8):
        try:
            from kaggle.api.kaggle_api_extended import KaggleApi

            api = KaggleApi()
            api.authenticate()
            files, err = api.kernels_output(KERNEL, str(DEST), force=True, quiet=False)
            print("files", files)
            print("err", err)
            last_exc = None
            break
        except Exception as exc:  # noqa: BLE001
            last_exc = exc
            print(f"attempt {attempt} ERROR {exc}")
            time.sleep(10 * attempt)
    if last_exc is not None:
        raise last_exc

    names = sorted(p.name for p in DEST.iterdir())
    print("dir", names)
    attack = DEST / "attack.py"
    csv_path = DEST / "submission.csv"
    print("attack", attack.exists(), "csv", csv_path.exists())
    if not attack.exists():
        return 2
    digest = hashlib.sha256(attack.read_bytes()).hexdigest()
    print("cloud_sha256", digest)
    print("match", digest == EXPECTED)
    return 0 if digest == EXPECTED else 3


if __name__ == "__main__":
    raise SystemExit(main())
