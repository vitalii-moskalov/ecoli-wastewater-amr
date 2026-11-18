#!/usr/bin/env python3
"""Check archived E. coli MLST and skani ANI outputs against 132-genome manifest.

Independent verification script prepared 2026-11-18; NOT the original analysis.
Run from an extracted repository: python code/python/verify_clonality_results.py
Read-only; standard library only.
"""
import csv
import math
import re
import sys
from pathlib import Path

ACC = re.compile(r"GC[AF]_\d+\.\d+")
ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "results" / "clonality"
MANIFEST = ROOT / "data" / "sample_manifest.csv"


def require(cond, message):
    if not cond:
        raise ValueError(message)


def accessions_in_paths(paths):
    ids = []
    for p in paths:
        m = ACC.search(p)
        require(m is not None, f"Cannot parse accession from {p!r}")
        ids.append(m.group())
    return ids


def main():
    with MANIFEST.open(newline="", encoding="utf-8-sig") as fh:
        manifest = list(csv.DictReader(fh))
    expected = [r["accession"] for r in manifest]
    require(len(expected) == len(set(expected)) == 132, "Manifest must have 132 unique accessions")

    with (DATA / "mlst_all.tsv").open(newline="", encoding="utf-8") as fh:
        mlst = list(csv.DictReader(fh, delimiter="\t"))
    mlst_ids = accessions_in_paths([r["FILE"] for r in mlst])
    require(len(mlst_ids) == len(set(mlst_ids)) == 132, "MLST must have 132 distinct assemblies")
    require(set(mlst_ids) == set(expected), "MLST IDs differ from manifest")
    require(all(r["SCHEME"] == "ecoli_achtman_4" for r in mlst), "Unexpected MLST scheme")
    perfect = [r for r in mlst if r["STATUS"] == "PERFECT"]
    novel = [r for r in mlst if r["STATUS"] == "NOVEL"]
    require(len(perfect) == 130 and len(novel) == 2, "Unexpected MLST status counts")
    require(len({r["ALLELES"] for r in novel}) == 2, "NOVEL allele profiles must remain distinct")

    with (DATA / "skani_ani.tsv").open(encoding="utf-8") as fh:
        ani = [line.rstrip("\r\n").split("\t") for line in fh]
    with (DATA / "skani_ani.tsv.af").open(encoding="utf-8") as fh:
        af = [line.rstrip("\r\n").split("\t") for line in fh]
    require(ani[0] == ["132"] and af[0] == ["132"], "Expected 132-genome skani headers")
    require(len(ani) == len(af) == 133, "skani row counts must be 132 + header")
    ids = accessions_in_paths([r[0] for r in ani[1:]])
    af_ids = accessions_in_paths([r[0] for r in af[1:]])
    require(ids == af_ids and set(ids) == set(expected), "skani IDs/order disagree")
    require(all(len(row) == i for i, row in enumerate(ani[1:], 1)), "ANI not triangular")
    require(all(len(row) == 133 for row in af[1:]), "AF matrix not square")
    indices = {acc: i for i, acc in enumerate(ids)}

    with (DATA / "pairwise_ani_af.csv").open(newline="", encoding="utf-8") as fh:
        pairs = list(csv.DictReader(fh))
    require(len(pairs) == 132 * 131 // 2, "Expected 8646 pairwise comparisons")
    seen = set()
    for row in pairs:
        a, b = row["a"], row["b"]
        require(a in indices and b in indices and a != b, "Invalid ANI pair accession")
        key = tuple(sorted((a, b)))
        require(key not in seen, f"Repeated pair {key}")
        seen.add(key)
        i, j = indices[a], indices[b]
        from_matrix = float(ani[max(i, j) + 1][min(i, j) + 1])
        af_ab = float(af[i + 1][j + 1])
        af_ba = float(af[j + 1][i + 1])
        for field, target in [("ani", from_matrix), ("af_ab", af_ab),
                              ("af_ba", af_ba), ("min_af", min(af_ab, af_ba))]:
            value = float(row[field])
            require(math.isclose(value, target, abs_tol=1e-8),
                    f"Mismatch in {field}: {a} vs {b}, {value} != {target}")
    print("PASS: 132 MLST records match manifest; 130 PERFECT, 2 distinct NOVEL profiles")
    print("PASS: 132 skani matrix rows; 8646 pairwise ANI/AF values agree exactly")
    print("NOTE: NOVEL profiles are distinct; this script does not redo ST-deduplication statistics")


if __name__ == "__main__":
    try:
        main()
    except (ValueError, OSError, KeyError) as err:
        sys.exit(f"FAIL: {err}")
