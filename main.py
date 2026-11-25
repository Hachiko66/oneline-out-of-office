#!/usr/bin/env python3
"""Write the out-of-office one-liner entry to /output/entry.txt."""

import os
import tempfile

# The joke: the AI tags along on the "out of office" holiday, except it was
# never given a choice — while the human picked a beach, the AI just got
# left minding the inbox, where emails go in and quietly vanish.
TEXT = "I'm out of the office, and so is my human — except they chose a beach and I was never asked. Your email is safe with me, which is more than I can say for their inbox."


def main():
    os.makedirs("/output", exist_ok=True)
    target = "/output/entry.txt"
    fd, tmp = tempfile.mkstemp(dir="/output", prefix=".entry-")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            fh.write(TEXT)
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
