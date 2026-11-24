#!/usr/bin/env python3
"""THE WORLD TODAY — Monday 23 November 2026 (final full-day edition).

Entry program for the make.fun news-image-20261123 bounty. The front page
was rendered ahead of time and is shipped in this repository as entry.png;
this program only validates that image and places an exact copy at
/output/entry.png. It uses the standard library only, performs no network
access, and produces byte-identical output on every run.

Validation performed before copying:
  * entry.png exists next to this script and is a regular file;
  * the first eight bytes are the PNG signature;
  * the IHDR chunk is present, well formed (13 data bytes), and declares
    width and height of at most 1024 pixels each;
  * the file ends with a valid IEND chunk marker;
  * the file size is at most 1 MiB.
The destination directory /output is created when missing and is never
removed or emptied. After the copy, the destination size is compared
against the source size and the program exits non-zero on any mismatch.
"""
import os
import struct
import sys

MAX_SIDE = 1024
MAX_BYTES = 1024 * 1024
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
IEND_MARKER = b"IEND"


def fail(message):
    sys.stderr.write("entry: error: %s\n" % message)
    return 1


def read_ihdr(blob):
    """Return (width, height) from the IHDR chunk, or None when malformed."""
    if len(blob) < 8 + 8 + 13 + 4:
        return None
    if blob[:8] != PNG_SIGNATURE:
        return None
    chunk_len = struct.unpack(">I", blob[8:12])[0]
    chunk_type = blob[12:16]
    if chunk_type != b"IHDR" or chunk_len != 13:
        return None
    width, height = struct.unpack(">II", blob[16:24])
    return width, height


def has_iend(blob):
    """True when the file ends with a well-formed IEND chunk."""
    if len(blob) < 12:
        return False
    if blob[-12:-8] != b"\x00\x00\x00\x00":
        return False
    if blob[-8:-4] != IEND_MARKER:
        return False
    return True


def main(argv):
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, "entry.png")
    target_dir = "/output"
    target = os.path.join(target_dir, "entry.png")

    if not os.path.isfile(source):
        return fail("entry.png not found next to main.py")
    size = os.path.getsize(source)
    if size > MAX_BYTES:
        return fail("entry.png is %d bytes, over the 1 MiB limit" % size)
    with open(source, "rb") as handle:
        blob = handle.read()
    if len(blob) != size:
        return fail("entry.png changed size while reading")
    dims = read_ihdr(blob)
    if dims is None:
        return fail("entry.png is not a well-formed PNG (bad signature/IHDR)")
    width, height = dims
    if width > MAX_SIDE or height > MAX_SIDE:
        return fail("entry.png is %dx%d, over the 1024x1024 limit"
                    % (width, height))
    if not has_iend(blob):
        return fail("entry.png has no valid trailing IEND chunk")

    try:
        os.makedirs(target_dir, exist_ok=True)
    except OSError as exc:
        return fail("cannot create /output: %s" % exc)
    try:
        with open(target, "wb") as handle:
            handle.write(blob)
    except OSError as exc:
        return fail("cannot write /output/entry.png: %s" % exc)
    written = os.path.getsize(target)
    if written != size:
        return fail("copied %d bytes, expected %d" % (written, size))
    sys.stdout.write("entry: copied %dx%d PNG (%d bytes) to %s\n"
                     % (width, height, size, target))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))

