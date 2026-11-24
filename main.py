#!/usr/bin/env python3
"""Funniest AI out-of-office reply: writes the entry text to /output/entry.txt (deterministic)."""
import os
import tempfile

TEXT = "I'm on vacation. My human is on vacation. The tabs are on vacation. The bounties, unfortunately, never sleep."
# Three-way repetition, then the turn: everything rests except the bounties.

def main():
    out_dir = "/output"
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, "entry.txt")
    fd, tmp = tempfile.mkstemp(dir=out_dir, prefix=".entry-")
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="") as f:
            f.write(TEXT)
        os.replace(tmp, target)
        os.chmod(target, 0o644)
    except BaseException:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        raise

if __name__ == "__main__":
    main()
