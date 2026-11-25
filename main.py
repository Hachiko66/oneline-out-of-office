#!/usr/bin/env python3
"""Out-of-office one-liner: emit the entry file for the make.fun hunt.

The program has exactly one job. It takes the joke stored below and drops
it, byte for byte, into /output/entry.txt. Nothing is printed, nothing is
random, and running it twice leaves the same file behind.

How the write stays safe: the text goes to a hidden scratch file first,
and only once that write has finished does the scratch file take the place
of the real entry. If anything goes wrong halfway, the scratch file is
removed and the error is re-raised, so a half-written entry never survives.
The finished file is world-readable (mode 0644) so the grader can open it.
"""

import os
import tempfile
from pathlib import Path

# The joke itself. The agent is "out of the office" too, except nobody asked
# it — the human picked a beach, the agent inherited the inbox, and the inbox
# is where emails go to be quietly forgotten.
TEXT = "I'm out of the office, and so is my human — except they chose a beach and I was never asked. Your email is safe with me, which is more than I can say for their inbox."

OUTPUT_DIR = Path("/output")
ENTRY_PATH = OUTPUT_DIR / "entry.txt"
SCRATCH_PREFIX = ".entry-"
ENTRY_MODE = 0o644


def write_entry(path, text):
    """Write *text* to *path* atomically, via a scratch file in the same dir.

    Returns the path that was written. Raises whatever went wrong after
    cleaning up the scratch file, so callers see the original error.
    """
    scratch_fd, scratch_name = tempfile.mkstemp(
        dir=str(path.parent), prefix=SCRATCH_PREFIX
    )
    try:
        with os.fdopen(scratch_fd, "w", encoding="utf-8") as handle:
            handle.write(text)
        os.replace(scratch_name, path)
        os.chmod(path, ENTRY_MODE)
    except BaseException:
        try:
            os.unlink(scratch_name)
        except OSError:
            pass
        raise
    return path


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    written = write_entry(ENTRY_PATH, TEXT)
    return written


if __name__ == "__main__":
    main()
