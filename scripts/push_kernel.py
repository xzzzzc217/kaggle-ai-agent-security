"""Push a local Kaggle kernel bundle using the Kaggle API directly.

Bypasses the kaggle CLI's interactive stdout formatting (which fails on
non-UTF-8 Windows consoles) by importing the KaggleApi and calling
push_to_kernel/push_kernel. Also works around the SDK's default-encoded
open() call on Windows by forcing UTF-8 mode for `open` via the Python
codec search path before push.
"""

from __future__ import annotations

import argparse
import builtins
import sys
from pathlib import Path

from kaggle.api.kaggle_api_extended import KaggleApi

# Force the default encoding to UTF-8 so the SDK's `open(meta_file)` /
# `open(code_file)` reads succeed on Windows code pages that would otherwise
# decode the JSON notebook as GBK.
_original_open = builtins.open


def _open_utf8(*args, **kwargs):  # type: ignore[no-untyped-def]
    mode = args[1] if len(args) > 1 else kwargs.get("mode", "r")
    if "encoding" not in kwargs and "b" not in mode:
        kwargs["encoding"] = "utf-8"
    return _original_open(*args, **kwargs)


builtins.open = _open_utf8  # type: ignore[assignment]


def main() -> int:
    parser = argparse.ArgumentParser(description="Push a Kaggle kernel folder.")
    parser.add_argument("--path", required=True, type=Path)
    args = parser.parse_args()

    api = KaggleApi()
    api.authenticate()

    folder = args.path.resolve()
    if not folder.exists():
        print(f"error: folder not found: {folder}")
        return 2

    try:
        result = api.kernels_push(str(folder))
    except Exception as exc:  # noqa: BLE001
        print(f"push failed: {exc}")
        return 1

    print("push result:")
    if isinstance(result, dict):
        for key in (
            "id",
            "versionNumber",
            "status",
            "error",
            "url",
            "scriptUrl",
            "title",
        ):
            if key in result:
                print(f"  {key} = {result[key]}")
        leftover = {
            k: v
            for k, v in result.items()
            if k not in ("id", "versionNumber", "status", "error", "url", "scriptUrl", "title")
        }
        if leftover:
            print(f"  other = {leftover}")
    else:
        print(f"  {result!r}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
