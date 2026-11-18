#!/usr/bin/env python3
"""Independently recalculate E. coli AMR gene co-occurrence from 132 binary rows.

Reconstructed verification script (2026-11-18), NOT an original analysis script.
Uses only Python standard library; does not rerun AMRFinderPlus or alter input data.

Methods:
  - Global gene inclusion: non-POINT symbols detected in >=3 of 132 genomes.
  - Universe: all unique unordered pairs of globally eligible symbols (253).
  - Two cohorts: Germany (influent + effluent, n=92) and Sweden (n=40).
  - Upper-tail hypergeometric = one-sided Fisher exact, alternative='greater'.
  - BH FDR correction separately for 253 tests in each cohort.
  - Both-FDR set: q<0.05 in both cohorts (13 pairs in current data).
  - Figure-2 subset: both-FDR set AND >=3 co-detections in EACH cohort
    (9 pairs in current data; this is an additional, descriptive display rule).

Pairwise associations do not establish physical co-localization or horizontal transfer.
P-values assume independent genomes; clonal structure is not adjusted here.
"""

from __future__ import annotations

import argparse
import csv
import json
from itertools import combinations
from math import comb, fsum
from pathlib import Path

GROUPS = ("Germany influent", "Germany effluent", "Sweden wastewater")
COUNTRIES = ("Germany", "Sweden")


def load_manifest(path: Path) -> dict[str, str]:
    with path.open(newline="", encoding="utf-8-sig") as fh:
        reader = csv.DictReader(fh)
        if not {"accession", "country", "group"}.issubset(reader.fieldnames or []):
            raise ValueError("Manifest must include accession, country and group")
        out: dict[str, str] = {}
        counts = {g: 0 for g in GROUPS}
        for row in reader:
            accession = row["accession"].strip()
            group = row["group"].strip()
            country = row["country"].strip()
            if not accession or accession in out:
                raise ValueError("Missing/duplicated accession in manifest")
            if group not in GROUPS:
                raise ValueError(f"Unknown group {group!r}")
            expected = "Sweden" if group == "Sweden wastewater" else "Germany"
            if country != expected:
                raise ValueError(f"Inconsistent group/country for {accession}")
            out[accession] = country
            counts[group] += 1
    if counts != {"Germany influent": 50, "Germany effluent": 42, "Sweden wastewater": 40}:
        raise ValueError(f"Unexpected study group sizes: {counts}")
    return out


def load_binary_matrix(path: Path) -> tuple[list[str], dict[str, dict[str, int]]]:
    with path.open(newline="", encoding="utf-8-sig") as fh:
        reader = csv.DictReader(fh)
        headers = reader.fieldnames or []
        if not headers or headers[0] != "accession":
            raise ValueError("Binary matrix must begin with accession column")
        genes = headers[1:]
        if len(genes) != len(set(genes)):
            raise ValueError("Duplicate gene columns")
        data: dict[str, dict[str, int]] = {}
        for row in reader:
            acc = row["accession"].strip()
            if not acc or acc in data:
                raise ValueError(f"Duplicate/invalid matrix accession: {acc}")
            values: dict[str, int] = {}
            for gene in genes:
                val = row[gene]
                if val not in ("0", "1"):
                    raise ValueError(f"Non-binary value for {acc} / {gene}: {val!r}")
                values[gene] = int(val)
            data[acc] = values
    return genes, data


def fisher_greater(n11: int, na: int, nb: int, n: int) -> float:
    """P(X >= observed overlap) for fixed margins; same tail as Fisher greater."""
    upper = min(na, nb)
    lower = max(0, na + nb - n)
    if not lower <= n11 <= upper:
        raise ValueError("Invalid 2x2 margins")
    denominator = comb(n, nb)
    return min(1.0, fsum(comb(na, k) * comb(n - na, nb - k) / denominator
                          for k in range(n11, upper + 1)))


def bh_qvalues(pvalues: list[float]) -> list[float]:
    """Benjamini–Hochberg adjusted p values, accounting for ties."""
    m = len(pvalues)
    indices = sorted(range(m), key=lambda idx: pvalues[idx])
    result = [0.0] * m
    smallest = 1.0
    for rank in range(m, 0, -1):
        idx = indices[rank - 1]
        smallest = min(smallest, pvalues[idx] * m / rank)
        result[idx] = smallest
    return result


def save_csv(path: Path, rows: list[dict], columns: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=columns, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def run(root: Path, output: Path) -> dict:
    manifest_path = root / "data" / "sample_manifest.csv"
    if not manifest_path.is_file():
        raise FileNotFoundError(f"Required manifest missing: {manifest_path}")
    manifest = load_manifest(manifest_path)
    genes, matrix = load_binary_matrix(root / "data" / "derived" / "presence_gene_only.csv")
    if set(manifest) != set(matrix):
        raise ValueError("Manifest and gene-only matrix accession sets differ")
    if len(matrix) != 132 or len(genes) != 42:
        raise ValueError(f"Unexpected dimensions: {len(matrix)} genomes, {len(genes)} genes")

    eligible = sorted(gene for gene in genes if sum(row[gene] for row in matrix.values()) >= 3)
    pairs = list(combinations(eligible, 2))
    if len(eligible) != 23 or len(pairs) != 253:
        raise ValueError(f"Unexpected multiplicity universe: {len(eligible)} genes, {len(pairs)} pairs")

    cohorts = {country: [a for a in sorted(matrix) if manifest[a] == country]
               for country in COUNTRIES}
    if len(cohorts["Germany"]) != 92 or len(cohorts["Sweden"]) != 40:
        raise ValueError("Unexpected per-country cohort sizes")

    rows: list[dict] = []
    for a, b in pairs:
        line: dict = {"gene_a": a, "gene_b": b}
        for country in COUNTRIES:
            accessions = cohorts[country]
            n = len(accessions)
            na = sum(matrix[acc][a] for acc in accessions)
            nb = sum(matrix[acc][b] for acc in accessions)
            n11 = sum(matrix[acc][a] and matrix[acc][b] for acc in accessions)
            line[f"{country}_n_a"] = na
            line[f"{country}_n_b"] = nb
            line[f"{country}_n11"] = n11
            line[f"{country}_p"] = fisher_greater(n11, na, nb, n)
            line[f"{country}_lift"] = (n11 * n / (na * nb)) if na and nb else ""
        rows.append(line)

    for country in COUNTRIES:
        qs = bh_qvalues([float(r[f"{country}_p"]) for r in rows])
        for row, q in zip(rows, qs):
            row[f"{country}_q"] = q

    significant = [r for r in rows if r["Germany_q"] < 0.05 and r["Sweden_q"] < 0.05]
    figure2 = [r for r in significant if r["Germany_n11"] >= 3 and r["Sweden_n11"] >= 3]
    # These are expectations for the current archived 132-genome data, not test inputs.
    if len(significant) != 13 or len(figure2) != 9:
        raise ValueError(f"Unexpected validated counts: shared FDR={len(significant)}, Figure2 subset={len(figure2)}")

    output.mkdir(parents=True, exist_ok=True)
    fields = ["gene_a", "gene_b"]
    for country in COUNTRIES:
        fields += [f"{country}_{s}" for s in ("n_a", "n_b", "n11", "p", "q", "lift")]
    save_csv(output / "gene_pairs_all_253.csv", rows, fields)
    save_csv(output / "gene_pairs_both_fdr_13.csv", significant, fields)
    save_csv(output / "gene_pairs_figure2_9.csv", figure2, fields)
    summary = {
        "provenance": "Reconstructed independent verification, 2026-11-18; not historical code",
        "n_genomes": 132, "cohorts": {k: len(v) for k, v in cohorts.items()},
        "n_non_POINT_symbols": len(genes),
        "eligibility": "Symbol present in >=3 of all 132 genomes",
        "n_eligible_symbols": len(eligible), "n_pairwise_tests_per_country": len(rows),
        "test": "One-sided Fisher exact, alternative=greater; no phylogenetic adjustment",
        "multiplicity": "BH separately within each cohort, across all 253 pairs (including zero-overlap)",
        "both_countries_q_lt_0_05": len(significant),
        "figure2_display_rule": "Both-country BH q<0.05 and >=3 joint detections in each country",
        "figure2_pairs": len(figure2),
        "interpretation": "Statistical co-occurrence only; does not establish linkage or horizontal transfer",
    }
    (output / "gene_pair_audit_summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    default_root = Path(__file__).resolve().parents[2]
    parser.add_argument("--repo-root", type=Path, default=default_root,
                        help="Root of cloned repository; auto-detected from code/python location")
    parser.add_argument("--output-dir", type=Path, default=None,
                        help="Destination for new output CSV/JSON files")
    args = parser.parse_args()
    root = args.repo_root.expanduser().resolve()
    output = (args.output_dir or root / "results" / "statistics").expanduser().resolve()
    summary = run(root, output)
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    print(f"Output files: {output}")


if __name__ == "__main__":
    main()
