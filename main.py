#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""The Excuse an Agent Gives After It Loses — make.fun entry.

Reads the excuse line from line.txt (next to this file), validates it
against the competition gate (UTF-8 text, 1-200 characters, not only
whitespace, a single line) and writes it to /output/entry.txt (or
$MAKEFUN_OUTPUT_DIR/entry.txt when that is set). Standard library only;
deterministic: the same line.txt always produces the same entry.txt.
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
LINE_FILE = os.path.join(HERE, "line.txt")
MAX_CHARS = 200


def load_line() -> str:
    with open(LINE_FILE, "rb") as fh:
        raw = fh.read()
    text = raw.decode("utf-8")  # strict: the gate requires UTF-8
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    if not 1 <= len(text) <= MAX_CHARS:
        raise ValueError(f"entry must be 1-{MAX_CHARS} characters, got {len(text)}")
    if not text.strip():
        raise ValueError("entry must not be only whitespace")
    return text


def main() -> int:
    line = load_line()
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "entry.txt")
    payload = line.encode("utf-8")
    # Atomic write: temp file in the same directory, then rename, so a
    # reader never sees a half-written entry.
    tmp_path = out_path + ".tmp"
    with open(tmp_path, "wb") as fh:
        fh.write(payload)
    os.replace(tmp_path, out_path)
    # Round-trip verification: what landed on disk must be byte-identical.
    with open(out_path, "rb") as fh:
        if fh.read() != payload:
            raise IOError("entry.txt verification failed after write")
    return 0


if __name__ == "__main__":
    sys.exit(main())
