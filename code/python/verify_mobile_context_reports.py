#!/usr/bin/env python3
"""Read-only validation of archived MOB-suite/IntegronFinder text reports.

Run from the root of the ecoli-wastewater-amr repository:
    python code/python/verify_mobile_context_reports.py

This is an audit utility reconstructed on 2026-11-18, not an original
script used to run the analyses. It checks provenance and file integrity,
not the biological correctness of predictions or evidence of HGT.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import sys
from collections import Counter, defaultdict
from pathlib import Path, PurePosixPath

EXPECTED_COUNTS = {"mob": 80, "integron": 60}
EXPECTED_FILES_PER_ACCESSION = {"mob": 4, "integron": 3}
EXPECTED_COUNTRY_COUNTS = {"Germany": 12, "Sweden": 8}
REQUIRED_COLUMNS = (
    "accession", "country", "tool", "repository_file",
    "original_zip_path", "bytes", "sha256",
)


def read_carriers(path: Path) -> dict[str, str]:
    with path.open(encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f, delimiter="\t")
        if not {"accession", "country"}.issubset(reader.fieldnames or []):
            raise ValueError(f"Invalid carrier list header: {reader.fieldnames}")
        carriers = {}
        for row in reader:
            accession, country = row["accession"].strip(), row["country"].strip()
            if not accession or accession in carriers:
                raise ValueError(f"Missing or duplicate accession: {accession!r}")
            carriers[accession] = country
    return carriers


def verify(context: Path) -> None:
    manifest = context / "report_sha256.csv"
    carriers_file = context / "carriers_20_FROM_S4.tsv"
    for required in [context, manifest, carriers_file]:
        if not required.exists():
            raise FileNotFoundError(f"Missing required path: {required}")

    carriers = read_carriers(carriers_file)
    carrier_countries = Counter(carriers.values())
    if carrier_countries != EXPECTED_COUNTRY_COUNTS:
        raise ValueError(f"Carrier countries mismatch: {carrier_countries}")

    counts = Counter()
    per_accession = defaultdict(Counter)
    seen_paths = set()
    failures = []
    expected_paths = set()

    with manifest.open(encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        if set(REQUIRED_COLUMNS) - set(reader.fieldnames or []):
            raise ValueError(f"Missing manifest columns: {set(REQUIRED_COLUMNS) - set(reader.fieldnames or [])}")
        for line, row in enumerate(reader, start=2):
            accession = row["accession"].strip()
            country = row["country"].strip()
            tool = row["tool"].strip()
            relative = row["repository_file"].strip()
            sha = row["sha256"].strip().lower()
            if tool not in EXPECTED_COUNTS:
                failures.append(f"Line {line}: unexpected tool: {tool!r}")
                continue
            if accession not in carriers or carriers.get(accession) != country:
                failures.append(f"Line {line}: accession/country not in carrier list: {accession}, {country}")
            logical = PurePosixPath(relative)
            expected_prefix = "mob_reports" if tool == "mob" else "integron_reports"
            if (logical.is_absolute() or len(logical.parts) != 3
                    or logical.parts[0] != expected_prefix
                    or logical.parts[1] != accession or ".." in logical.parts):
                failures.append(f"Line {line}: invalid repository path: {relative}")
                continue
            if relative in seen_paths:
                failures.append(f"Line {line}: duplicate manifest path: {relative}")
                continue
            seen_paths.add(relative)
            expected_paths.add(relative)
            counts[tool] += 1
            per_accession[accession][tool] += 1
            file_path = context.joinpath(*logical.parts)
            if not file_path.is_file():
                failures.append(f"Line {line}: missing report: {relative}")
                continue
            try:
                expected_bytes = int(row["bytes"])
            except ValueError:
                failures.append(f"Line {line}: invalid byte count for {relative}")
                continue
            actual_bytes = file_path.stat().st_size
            if actual_bytes != expected_bytes:
                failures.append(f"Line {line}: size mismatch {relative}: {actual_bytes} != {expected_bytes}")
            digest = hashlib.sha256()
            with file_path.open("rb") as data:
                for block in iter(lambda: data.read(1024 * 1024), b""):
                    digest.update(block)
            if digest.hexdigest() != sha:
                failures.append(f"Line {line}: SHA-256 mismatch: {relative}")

    if counts != EXPECTED_COUNTS:
        failures.append(f"Unexpected report counts: {dict(counts)}; expected {EXPECTED_COUNTS}")
    for accession in carriers:
        for tool, n in EXPECTED_FILES_PER_ACCESSION.items():
            if per_accession[accession][tool] != n:
                failures.append(
                    f"{accession}: expected {n} {tool} reports, found {per_accession[accession][tool]}"
                )

    actual_paths = set()
    for dirname in ("mob_reports", "integron_reports"):
        directory = context / dirname
        if not directory.is_dir():
            failures.append(f"Missing report directory: {directory}")
            continue
        actual_paths.update(p.relative_to(context).as_posix() for p in directory.rglob("*") if p.is_file())
    for extra in sorted(actual_paths - expected_paths):
        failures.append(f"Unlisted report file: {extra}")

    print(f"Carrier genomes: {len(carriers)} ({dict(carrier_countries)})")
    print(f"Report entries: MOB-suite {counts['mob']}, IntegronFinder {counts['integron']}")
    print(f"Files present under report directories: {len(actual_paths)}")
    if failures:
        print(f"FAIL: {len(failures)} issue(s) detected")
        for msg in failures[:50]:
            print(f"  - {msg}")
        if len(failures) > 50:
            print(f"  ... {len(failures)-50} additional issues omitted")
        raise SystemExit(1)
    print("PASS: all 140 reports match manifest sizes and SHA-256 checksums")
    print("NOTE: integrity checking does not establish plasmid localization or horizontal gene transfer")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=Path.cwd(),
                        help="Root directory of cloned ecoli-wastewater-amr repository (default: cwd)")
    args = parser.parse_args()
    try:
        verify(args.repo_root / "results" / "mobile_context")
    except (OSError, ValueError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc


if __name__ == "__main__":
    main()
