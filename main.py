#!/usr/bin/env python3
"""Deliver the picture for the news-image-20261120 bounty.

``entry.png`` sits in this repository next to this file: a single
image summing up the world's news of Friday 20 November 2026,
painted by the companion generator ``draw.py`` (the README lists
the stories shown).  The judging sandbox installs nothing, so this
program sticks to the standard library: it copies the committed
picture to the output location exactly as stored, which also makes
the result deterministic - repeated runs emit identical bytes.
"""

import hashlib
import os
import shutil
import sys

PICTURE = "entry.png"
PNG_SIGNATURE = b"\x89\x50\x4e\x47\x0d\x0a\x1a\x0a"


def output_path():
    folder = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    return os.path.join(folder, PICTURE)


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, PICTURE)
    with open(source, "rb") as handle:
        blob = handle.read()
    if not blob.startswith(PNG_SIGNATURE):
        raise SystemExit("entry.png is not a PNG file")
    target = output_path()
    os.makedirs(os.path.dirname(target) or ".", exist_ok=True)
    with open(target, "wb") as handle:
        handle.write(blob)
    digest = hashlib.sha256(blob).hexdigest()
    print(f"wrote {target} ({len(blob)} bytes, sha256 {digest})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
