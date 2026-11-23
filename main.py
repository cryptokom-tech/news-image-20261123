"""news-image-20261123 — round 2 entry.

The front page image ("THE WORLD TODAY", Monday 23 November 2026, 36
stories) is rendered offline during development and bundled in this
repository as entry.png. This program only validates that bundled image
and copies it, byte for byte, to /output/entry.png.

Standard library only: no third-party packages, no fonts, no network
access, so it runs in any minimal Python 3.13 image. Two runs produce
byte-identical output because a copy never changes a byte.
"""

import os
import struct
import sys

# The bundled front-page image lives next to this script in the repo.
SOURCE_NAME = "entry.png"

# The grader mounts the output directory here; never remove it, only
# write the single output file into it.
OUTPUT_DIR = "/output"
OUTPUT_NAME = "entry.png"

# Competition limits for the output image.
MAX_BYTES = 1024 * 1024
MAX_WIDTH = 1024
MAX_HEIGHT = 1024

# PNG file signature (8 bytes) and the IHDR chunk layout.
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


def source_path():
    """Absolute path of the bundled image next to this script."""
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(here, SOURCE_NAME)


def read_png_size(data):
    """Return (width, height) from the IHDR chunk of PNG bytes."""
    if len(data) < 33 or data[:8] != PNG_SIGNATURE:
        raise ValueError("not a PNG file (bad signature)")
    # After the 8-byte signature: 4-byte length, 4-byte "IHDR",
    # then width (4 bytes) and height (4 bytes), big-endian.
    if data[12:16] != b"IHDR":
        raise ValueError("not a PNG file (first chunk is not IHDR)")
    width, height = struct.unpack(">II", data[16:24])
    return width, height


def main():
    src = source_path()
    if not os.path.isfile(src):
        print("error: bundled image %s not found" % src, file=sys.stderr)
        return 1

    with open(src, "rb") as handle:
        data = handle.read()

    if len(data) > MAX_BYTES:
        print("error: bundled image is %d bytes, over the %d-byte limit"
              % (len(data), MAX_BYTES), file=sys.stderr)
        return 1

    try:
        width, height = read_png_size(data)
    except ValueError as exc:
        print("error: bundled image is not a valid PNG: %s" % exc,
              file=sys.stderr)
        return 1

    if width > MAX_WIDTH or height > MAX_HEIGHT:
        print("error: bundled image is %dx%d, over the %dx%d limit"
              % (width, height, MAX_WIDTH, MAX_HEIGHT), file=sys.stderr)
        return 1

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    dest = os.path.join(OUTPUT_DIR, OUTPUT_NAME)
    with open(dest, "wb") as handle:
        handle.write(data)

    # Confirm the copy landed byte for byte.
    if os.path.getsize(dest) != len(data):
        print("error: copied image size mismatch", file=sys.stderr)
        return 1

    print("wrote %s (%d, %d) %d bytes" % (dest, width, height, len(data)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
