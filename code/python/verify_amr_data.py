#!/usr/bin/env python3
"""Read-only consistency audit for the 132-genome E. coli wastewater AMR dataset.

Created during the November 2026 reproducibility audit; NOT a historical analysis
script. Requires Python 3.9+ standard library only. Does not rerun AMRFinderPlus,
change input files, test associations, or regenerate manuscript figures.

Usage from any directory:
    python code/python/verify_amr_data.py
    python code/python/verify_amr_data.py --repo /path/to/repository
    python code/python/verify_amr_data.py --checksums /path/to/checksums.csv

This script checks consistency with explicitly conservative filtering rules, including INTERNAL_STOP; it does NOT
establish that the biological selection criteria are optimal or exhaustive.
"""

import argparse
import csv
import hashlib
import re
import sys
from collections import Counter
from decimal import Decimal, InvalidOperation
from pathlib import Path


def require(condition, message):
    if not condition:
        raise ValueError(message)


def read_rows(path, delimiter=","):
    require(path.is_file(), f"Missing required file: {path}")
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle, delimiter=delimiter)
        require(reader.fieldnames is not None, f"Missing header in {path}")
        return list(reader), reader.fieldnames


def as_num(value):
    value = (value or "").strip()
    if not value:
        return ""
    try:
        return str(Decimal(value).normalize())
    except InvalidOperation:
        return value


def hash_file(path):
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def assert_matrix(file, accession_set, positives):
    rows, columns = read_rows(file)
    require(columns[0] == "accession", f"Wrong first column in {file}")
    require(len(columns[1:]) == len(set(columns[1:])), f"Duplicate symbols in {file}")
    require(len(rows) == len(accession_set), f"Wrong number of isolates in {file}")
    got = Counter()
    seen = set()
    for row in rows:
        acc = row["accession"]
        require(acc not in seen, f"Duplicate accession {acc} in {file}")
        seen.add(acc)
        for symbol in columns[1:]:
            value = row[symbol]
            require(value in {"0", "1"}, f"Nonbinary value for {acc}, {symbol}: {value}")
            if value == "1":
                got[(acc, symbol)] += 1
    require(seen == accession_set, f"Accession mismatch in {file}")
    require(got == positives, f"Positive accession-symbol pairs disagree in {file}")
    require(set(columns[1:]) == {symbol for _, symbol in positives},
            f"Symbol columns mismatch in {file}")
    return len(columns) - 1, sum(got.values())


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[2],
                        help="Repository root (default: two directories above script)")
    parser.add_argument("--checksums", type=Path, default=None,
                        help="Alternate location for checksum CSV")
    args = parser.parse_args()
    root = args.repo.resolve()
    data = root / "data"
    annotation_dir = data / "annotations"
    derived = data / "derived"
    checksum_path = args.checksums or annotation_dir / "ecoli_amrfinder_132_file_checksums.csv"

    manifest, _ = read_rows(data / "sample_manifest.csv")
    require(len(manifest) == 132, f"Manifest contains {len(manifest)} instead of 132 records")
    meta = {r["accession"]: r for r in manifest}
    require(len(meta) == 132, "Duplicate accessions in sample_manifest.csv")
    groups = Counter(r["group"] for r in manifest)
    require(groups == {"Germany influent": 50, "Germany effluent": 42,
                       "Sweden wastewater": 40}, f"Unexpected group counts: {groups}")

    checksum_rows, _ = read_rows(checksum_path)
    require(len(checksum_rows) == 132, "Checksum manifest must contain 132 entries")
    file_records = Counter()
    excluded = Counter()
    expected_all = Counter()
    expected_genes = Counter()
    seen = set()
    source_hit_count = 0
    for entry in checksum_rows:
        country, name = entry["country"], entry["filename"]
        require(country in {"Germany", "Sweden"}, f"Unexpected collection: {country}")
        acc = name.removesuffix("_amrfinder.tsv") if hasattr(name, 'removesuffix') else name[:-len('_amrfinder.tsv')]
        require(name.endswith("_amrfinder.tsv"), f"Unexpected file name: {name}")
        require(acc not in seen, f"Duplicate input accession: {acc}")
        seen.add(acc)
        require(acc in meta and meta[acc]["country"] == country,
                f"Accession-country mismatch: {acc}")
        file = annotation_dir / country / name
        require(file.is_file(), f"Missing original annotation: {file}")
        require(file.stat().st_size == int(entry["bytes"]), f"File size mismatch: {name}")
        require(hash_file(file) == entry["sha256"].lower(), f"SHA-256 mismatch: {name}")
        original, fields = read_rows(file, delimiter="\t")
        for col in ["Scope", "Type", "Subtype", "Element symbol", "Method", "Class",
                    "% Coverage of reference", "% Identity to reference"]:
            require(col in fields, f"Missing column '{col}' in {name}")
        for row in original:
            if row["Scope"].lower() != "core" or row["Type"].upper() != "AMR":
                continue
            symbol = row["Element symbol"]
            bad = ("DISRUPT" in row["Subtype"].upper()
                   or "INTERNAL_STOP" in row["Method"].upper()
                   or "PARTIAL" in row["Method"].upper()
                   or bool(re.search(r"fsTer|Ter[0-9]*$", symbol, flags=re.I)))
            if bad:
                excluded[(acc, symbol)] += 1
                continue
            source_hit_count += 1
            file_records[(acc, country, meta[acc]["group"], symbol,
                          row["Subtype"], row["Class"], row["Method"],
                          as_num(row["% Coverage of reference"]),
                          as_num(row["% Identity to reference"]), row["Scope"])] += 1
            expected_all[(acc, symbol)] = 1
            if not row["Subtype"].upper().startswith("POINT"):
                expected_genes[(acc, symbol)] = 1

    require(seen == set(meta), "Original annotations and manifest contain different accessions")
    require(sum(acc.startswith("GCA_") for acc in seen) == 132,
            "Expected GenBank GCA assembly accessions")
    hits, _ = read_rows(derived / "core_amr_hits.csv")
    actual_records = Counter((r["accession"], r["country"], r["group"], r["symbol"],
                              r["subtype"], r["cls"], r["method"],
                              as_num(r["coverage"]), as_num(r["identity"]), r["scope"])
                             for r in hits)
    require(file_records == actual_records,
            "Filtered core_amr_hits.csv does not match original annotated hits")
    rejected, _ = read_rows(derived / "excluded_uncertain_hits.csv")
    require(excluded == Counter((r["accession"], r["symbol"]) for r in rejected),
            "Exclusion records do not match filtered original annotations")

    all_symbols, all_positive = assert_matrix(
        derived / "presence_all_core.csv", set(meta), expected_all)
    gene_symbols, gene_positive = assert_matrix(
        derived / "presence_gene_only.csv", set(meta), expected_genes)
    require((len(hits), len(rejected), all_symbols, gene_symbols,
             all_positive, gene_positive) == (407, 18, 60, 42, 391, 287),
            "Unexpected summary totals: inspect possible dataset version drift")
    positive_genomes = len(set(acc for acc, _ in expected_all))
    require(positive_genomes == 82, f"Unexpected AMR-positive isolate count: {positive_genomes}")

    print("PASS: 132 matching assembly accessions (92 Germany, 40 Sweden)")
    print("PASS: all 132 original TSV sizes and SHA-256 checksums")
    print(f"PASS: {source_hit_count} retained core AMR hits; {sum(excluded.values())} excluded")
    print(f"PASS: {all_symbols} determinant symbols / {all_positive} positive matrix cells")
    print(f"PASS: {gene_symbols} non-POINT symbols / {gene_positive} positive matrix cells")
    print(f"PASS: {positive_genomes} genomes with >=1 retained core AMR finding")
    print("NOTE: Data consistency only; this is not a biological validation of mechanisms")
    print("      or a phylogenetically adjusted statistical analysis.")


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, KeyError, csv.Error) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        sys.exit(1)
