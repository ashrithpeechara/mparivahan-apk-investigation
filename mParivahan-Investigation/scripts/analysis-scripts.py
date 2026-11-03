#!/usr/bin/env python3

import argparse
import hashlib
import zipfile
from pathlib import Path


def calculate_sha256(path):
    digest = hashlib.sha256()

    with path.open("rb") as file:
        for chunk in iter(lambda: file.read(1024 * 1024), b""):
            digest.update(chunk)

    return digest.hexdigest()


def analyze_apk(apk_path):
    if not apk_path.is_file():
        print(f"[ERROR] APK not found: {apk_path}")
        return

    print("=" * 65)
    print("APK STATIC TRIAGE")
    print("=" * 65)

    print(f"\nFile: {apk_path}")
    print(f"Size: {apk_path.stat().st_size:,} bytes")
    print(f"SHA256: {calculate_sha256(apk_path)}")

    try:
        with zipfile.ZipFile(apk_path, "r") as archive:

            print("\n[+] ZIP Integrity Check")

            bad_file = archive.testzip()

            if bad_file is None:
                print("[PASS] No CRC errors detected")
            else:
                print(f"[FAIL] Corrupt archive entry: {bad_file}")

            entries = archive.infolist()

            print(f"\n[+] Total Archive Entries: {len(entries)}")

            dex_files = []
            payload_files = []
            manifest_found = False

            for entry in entries:
                name = entry.filename

                if name == "AndroidManifest.xml":
                    manifest_found = True

                if name.endswith(".dex"):
                    dex_files.append(entry)

                if name.startswith("assets/"):
                    payload_files.append(entry)

            print("\n[+] Manifest")
            print(
                "[FOUND] AndroidManifest.xml"
                if manifest_found
                else "[NOT FOUND] AndroidManifest.xml"
            )

            print("\n[+] DEX Files")

            for entry in dex_files:
                print(f"{entry.filename} ({entry.file_size:,} bytes)")

            print("\n[+] Asset Files")

            for entry in payload_files:
                print(f"{entry.filename} ({entry.file_size:,} bytes)")

            print("\n[+] Archive Inventory")

            for entry in entries:
                print(
                    f"{entry.filename} | "
                    f"{entry.file_size:,} bytes"
                )

    except zipfile.BadZipFile:
        print("[ERROR] Invalid ZIP/APK archive")

    except OSError as error:
        print(f"[ERROR] {error}")


def main():
    parser = argparse.ArgumentParser(
        description="Read-only APK static triage utility"
    )

    parser.add_argument("apk", help="Path to APK file")

    args = parser.parse_args()

    analyze_apk(Path(args.apk))


if __name__ == "__main__":
    main()