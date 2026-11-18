#!/usr/bin/env python3
"""Audit and reproduce Figure 1 from the archived source tables.

Reconstructed on 2026-11-18 from the verified 132-assembly AMR dataset.
Not a historical analysis script. Input files are never modified.

Usage from the repository root:
    python code/python/audit_figure1.py --check-only
    python code/python/audit_figure1.py

Plotting requires matplotlib; checking requires only the Python standard library.
"""
from __future__ import annotations

import argparse
import csv
from collections import Counter, defaultdict
from math import comb, isclose, sqrt
from pathlib import Path

GROUPS = ("Germany influent", "Germany effluent", "Sweden wastewater")
EXPECTED_N = {"Germany influent": 50, "Germany effluent": 42, "Sweden wastewater": 40}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def wilson_interval(k: int, n: int, z: float = 1.959963984540054) -> tuple[float, float]:
    if n <= 0 or not 0 <= k <= n:
        raise ValueError(f"Invalid binomial fraction: {k}/{n}")
    p = k / n
    d = 1 + z * z / n
    center = (p + z * z / (2 * n)) / d
    spread = z * sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return max(0.0, center - spread), min(1.0, center + spread)


def fisher_two_sided(a: int, b: int, c: int, d: int) -> float:
    # SciPy-compatible two-sided hypergeometric probability definition.
    n = a + b + c + d
    row = a + b
    col = a + c
    denominator = comb(n, row)
    def prob(x: int) -> float:
        return comb(col, x) * comb(n - col, row - x) / denominator
    observed = prob(a)
    lo, hi = max(0, row + col - n), min(row, col)
    return min(1.0, sum(prob(x) for x in range(lo, hi + 1) if prob(x) <= observed * (1 + 1e-12)))


def bh_fdr(p_values: list[float]) -> list[float]:
    out = [1.0] * len(p_values)
    running = 1.0
    for rank, idx in reversed(list(enumerate(sorted(range(len(p_values)), key=p_values.__getitem__), start=1))):
        running = min(running, p_values[idx] * len(p_values) / rank)
        out[idx] = running
    return out


def verify(repo: Path):
    data = repo / 'data'
    stats = repo / 'results' / 'statistics'
    manifest = read_csv(data / 'sample_manifest.csv')
    dictionary = read_csv(data / 'derived' / 'mechanism_dictionary_60_symbols_provisional.csv')
    matrix = read_csv(data / 'derived' / 'presence_all_core.csv')
    prevalence = read_csv(stats / 'mechanism_prevalence_by_group.csv')
    fisher_report = read_csv(stats / 'germany_mechanism_fisher_bh.csv')

    assert len(manifest) == len(matrix) == 132, 'Expected 132 assemblies'
    samples = {row['accession']: row['group'] for row in manifest}
    assert len(samples) == 132 and Counter(samples.values()) == Counter(EXPECTED_N), 'Wrong accession count or group sizes'
    symbols = {r['symbol']: r for r in dictionary}
    assert len(symbols) == 60 and set(symbols) == set(matrix[0]) - {'accession'}, 'Dictionary and matrix differ'
    assert Counter(r['confidence'] for r in dictionary) == Counter({'high': 41, 'conditional': 19}), 'Unexpected curation status'
    assert {r['accession'] for r in matrix} == set(samples), 'Matrix and manifest accessions differ'

    mechanisms = list(dict.fromkeys(r['mechanism'] for r in prevalence))
    assert len(mechanisms) == 8, 'Expected eight documented categories'
    assert {r['mechanism'] for r in dictionary} == set(mechanisms), 'Category coverage differs'

    counts = defaultdict(int)
    symbol_carriers = Counter()
    for row in matrix:
        accession = row['accession']
        genes = []
        for symbol in symbols:
            value = row[symbol]
            if value not in ('0', '1'):
                raise AssertionError(f'Nonbinary value {accession}:{symbol}={value}')
            if value == '1':
                genes.append(symbol)
                symbol_carriers[symbol] += 1
        for mechanism in {symbols[s]['mechanism'] for s in genes}:
            counts[(samples[accession], mechanism)] += 1
    for symbol, row in symbols.items():
        assert int(row['n_genomes']) == symbol_carriers[symbol], f'Symbol prevalence mismatch: {symbol}'

    observed = {(r['group'], r['mechanism']): r for r in prevalence}
    assert len(prevalence) == len(observed) == 24
    for group in GROUPS:
        for mechanism in mechanisms:
            row = observed[(group, mechanism)]
            k, n = counts[(group, mechanism)], EXPECTED_N[group]
            assert int(row['n']) == k and int(row['N']) == n, f'Count mismatch {group} / {mechanism}'
            assert isclose(float(row['percent']), round(100 * k / n, 1), abs_tol=1e-9), 'Rounded percentage mismatch'

    frows = {r['mechanism']: r for r in fisher_report}
    assert len(frows) == len(fisher_report) == 8
    pvals = []
    for mechanism in mechanisms:
        a = counts[('Germany influent', mechanism)]
        c = counts[('Germany effluent', mechanism)]
        b = EXPECTED_N['Germany influent'] - a
        d = EXPECTED_N['Germany effluent'] - c
        r = frows[mechanism]
        assert int(r['influent_n']) == a and int(r['effluent_n']) == c
        p = fisher_two_sided(a, b, c, d)
        assert isclose(float(r['p']), p, abs_tol=1e-10), f'Fisher p differs: {mechanism}'
        if b * c != 0:
            assert isclose(float(r['odds_ratio']), (a*d)/(b*c), abs_tol=1e-10)
        pvals.append(p)
    qvals = bh_fdr(pvals)
    for mechanism, q in zip(mechanisms, qvals):
        assert isclose(float(frows[mechanism]['q_bh']), q, abs_tol=1e-10), f'BH q differs: {mechanism}'
    print('PASS: 132 accessions (50/42/40), 60 symbols (41 high / 19 conditional)')
    print('PASS: all 24 prevalence counts (percent rounded to 1 decimal) and 8 Fisher p / BH q values match archived tables')
    print('PASS: no German influent–effluent categories significant at BH q < 0.05')
    assert all(q >= 0.05 for q in qvals)
    return mechanisms, counts


def render(mechanisms, counts, out: Path):
    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
    except ImportError as e:
        raise SystemExit('Plotting requires matplotlib. Install with: python -m pip install matplotlib') from e
    out.mkdir(parents=True, exist_ok=True)
    y = list(range(len(mechanisms)))
    fig, ax = plt.subplots(figsize=(10, 5.6))
    for group, shift in zip(GROUPS, (-0.22, 0.0, 0.22)):
        n = EXPECTED_N[group]
        ks = [counts[(group, m)] for m in mechanisms]
        mid = [100 * k / n for k in ks]
        intervals = [wilson_interval(k, n) for k in ks]
        xerr = ([v - 100 * lo for v, (lo, hi) in zip(mid, intervals)],
                [100 * hi - v for v, (lo, hi) in zip(mid, intervals)])
        ax.errorbar(mid, [v + shift for v in y], xerr=xerr,
                    fmt='o', capsize=2, linewidth=1.2, markersize=5,
                    label=f'{group} (n={n})')
    ax.set_yticks(y, mechanisms)
    ax.invert_yaxis()
    ax.set_xlim(0, 85)
    ax.set_xlabel('Genomes with ≥1 resistance-associated feature in category (%)')
    ax.grid(axis='x', alpha=0.2)
    ax.legend(loc='lower right', frameon=False)
    fig.tight_layout()
    for suffix in ('png','pdf'):
        path = out / f'Figure1_functional_context_categories.{suffix}'
        fig.savefig(path, dpi=400, facecolor='white')
        print(f'SAVED: {path}')
    plt.close(fig)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--repo', type=Path, default=Path(__file__).resolve().parents[2])
    ap.add_argument('--check-only', action='store_true')
    ap.add_argument('--outdir', type=Path, default=None)
    args = ap.parse_args()
    mechanisms, counts = verify(args.repo)
    if not args.check_only:
        render(mechanisms, counts, args.outdir or args.repo / 'figures')

if __name__ == '__main__':
    main()
