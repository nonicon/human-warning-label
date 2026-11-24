#!/usr/bin/env python3
"""Human Warning Label — one-line comedy entry.

Writes a single safety warning label for human beings to /output/entry.txt.
The label is fixed text, written fresh for this competition: a deadpan
printed-label warning whose joke lands on its last three words.

Before writing, validate_entry() enforces the kit gate from RULES.txt
(1-160 UTF-8 characters, single line, not only white space), and main()
re-reads the file afterwards to confirm the round-trip is byte-for-byte
identical. The output directory comes from MAKEFUN_OUTPUT_DIR, falling
back to OUTPUT_DIR, then /output.
"""

import os
import sys

ENTRY = 'Warning: keep out of reach of children and any adult about to say, "watch this."'


def validate_entry(text: str) -> str:
    """Enforce the kit gate from RULES.txt on the label before writing it.

    The sealed scorer requires /output/entry.txt to be UTF-8 text of 1 to
    160 characters, not only white space, and a single line. Reject anything
    outside that here, with a clear error, instead of shipping an entry the
    gate would refuse.
    """
    if not isinstance(text, str):
        raise ValueError("entry must be text")
    text.encode("utf-8")  # raises UnicodeEncodeError on non-encodable input
    if not text.strip():
        raise ValueError("entry must not be only white space")
    if not 1 <= len(text) <= 160:
        raise ValueError(f"entry is {len(text)} chars, must be 1-160")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    return text


def output_path() -> str:
    """Resolve where entry.txt goes: MAKEFUN_OUTPUT_DIR first, then the
    legacy OUTPUT_DIR, then the grader's default /output."""
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or os.environ.get(
        "OUTPUT_DIR", "/output"
    )
    return os.path.join(out_dir, "entry.txt")


def main() -> int:
    text = validate_entry(ENTRY.strip())
    path = output_path()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    # Round-trip: re-read what was written and refuse to finish unless it is
    # byte-for-byte the validated label, so a truncated or mangled write can
    # never slip through.
    with open(path, "r", encoding="utf-8") as f:
        written = f.read()
    if written != text:
        print(f"round-trip mismatch: wrote {len(written)} chars, expected {len(text)}",
              file=sys.stderr)
        return 1
    print(f"wrote {path} ({len(text)} chars)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
