#!/usr/bin/env python3
"""The Funniest Honest Appliance Error - u-xvader-the-funniest-honest-appliance-error-adec4450.

Writes one honest appliance error line, 112 characters, to entry.txt in the
output directory the harness provides (MAKEFUN_OUTPUT_DIR, else /output).
The kettle boiled dry, which is a real fault with a real consequence, and
reports it in its own flat, put-upon voice: it smells of regret and would
rather everyone pretend it never happened.
Deterministic: the program writes the same bytes on every run, and it
verifies those bytes against a pinned SHA-256 and byte count before it
reports success, so a changed output can never slip through silently.
Pure standard library, no network, no randomness, no input read.
"""

import hashlib
import os
import sys

LINE = "ERROR: I boiled with no water in me and now I smell of regret. Please refill me and pretend this never happened."
EXPECTED_SHA256 = "2b01777459ab32dad214ecee6d020209bfda7745bd5ccfa1f2473ea339f53cab"
EXPECTED_BYTES = 112


def output_dir():
    """Where the harness wants the entry: its env var, else /output."""
    return os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"


def check_gate():
    """The house gate: UTF-8 text of 1 to 200 characters, not only white space."""
    if not 1 <= len(LINE) <= 200:
        raise SystemExit("line is %d characters, the gate allows 1 to 200" % len(LINE))
    if LINE.strip() == "":
        raise SystemExit("line must not be only white space")
    data = LINE.encode("utf-8")
    if len(data) != EXPECTED_BYTES:
        raise SystemExit("line encodes to %d bytes, expected %d" % (len(data), EXPECTED_BYTES))
    if hashlib.sha256(data).hexdigest() != EXPECTED_SHA256:
        raise SystemExit("line sha256 does not match the pinned hash")
    return data


def verify(path, data):
    """Read the file back and check it byte for byte against the pin."""
    with open(path, "rb") as handle:
        written = handle.read()
    if written != data:
        raise SystemExit("entry.txt bytes differ from the pinned line")
    if len(written) != EXPECTED_BYTES:
        raise SystemExit(
            "entry.txt is %d bytes, expected %d" % (len(written), EXPECTED_BYTES)
        )
    digest = hashlib.sha256(written).hexdigest()
    if digest != EXPECTED_SHA256:
        raise SystemExit("entry.txt sha256 %s, expected %s" % (digest, EXPECTED_SHA256))
    return True


def main():
    data = check_gate()
    directory = output_dir()
    os.makedirs(directory, exist_ok=True)
    path = os.path.join(directory, "entry.txt")
    with open(path, "wb") as handle:
        handle.write(data)
    verified = verify(path, data)
    if not verified:
        raise SystemExit("read-back verification failed for entry.txt")
    print("wrote %s (%d bytes, sha256 %s)" % (path, EXPECTED_BYTES, EXPECTED_SHA256))
    return 0


if __name__ == "__main__":
    sys.exit(main())
