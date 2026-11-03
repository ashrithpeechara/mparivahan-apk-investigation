#!/usr/bin/env python3

import argparse
import hashlib
import sys
from pathlib import Path


def calculate_sha256(file_path):
    sha256 = hashlib.sha256()

    with file_path.open("rb") as file:
        for chunk in iter(lambda: file.read(1024 * 1024), b""):
            sha256.update(chunk)

    return sha256.hexdigest()


def main():
    parser = argparse.ArgumentParser(
        description="Forensic SHA-256 verification utility"
    )

    parser.add_argument("files", nargs="+", help="Files to hash")
    parser.add_argument(
        "--expected",
        help="Expected SHA-256 hash for a single file"
    )

    args = parser.parse_args()

    if args.expected and len(args.files) != 1:
        parser.error("--expected can only be used with one file")

    for item in args.files:
        path = Path(item)

        if not path.is_file():
            print(f"[ERROR] File not found: {path}")
            continue

        try:
            digest = calculate_sha256(path)

            print(f"\nFile:   {path}")
            print(f"SHA256: {digest}")

            if args.expected:
                if digest.lower() == args.expected.lower():
                    print("[PASS] Hash matches expected value")
                else:
                    print("[FAIL] Hash mismatch")

        except OSError as error:
            print(f"[ERROR] {path}: {error}")


if __name__ == "__main__":
    main()