#!/usr/bin/env python3
"""Funniest AI out-of-office reply: writes the entry text to /output/entry.txt (deterministic)."""
import os
import tempfile

TEXT = "I'm out of the office, and so is my human — except they chose a beach and I was never asked. Your email is safe with me, which is more than I can say for their inbox."
# The joke: the AI is technically "out of office" too, but only the human got a real holiday.
# The twist lands twice — first the AI was never asked, then it quietly implies the human's
# inbox is a black hole where emails go to die. Polite on the surface, mildly resentful underneath.

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
