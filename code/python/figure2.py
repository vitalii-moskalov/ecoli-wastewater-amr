#!/usr/bin/env python3
"""Reproduce manuscript Figure 2 from independently verified co-occurrence tables.

Reconstructed for repository documentation on 2026-11-18; NOT original historical code.
Run from any working directory:
    python code/python/figure2.py --check-only
    python code/python/figure2.py
Requires matplotlib only when plotting. Existing data are never modified.
"""
from __future__ import annotations
import argparse
import csv
from math import log2
from pathlib import Path

# Presentation order used in the archived manuscript Figure 2.
ORDER = [
    ("aph(3'')-Ib", 'aph(6)-Id'),
    ("aph(3'')-Ib", 'sul2'),
    ('aph(6)-Id', 'sul2'),
    ('blaTEM-1', 'sul2'),
    ('mph(A)', 'mrx(A)'),
    ('aph(6)-Id', 'blaTEM-1'),
    ('dfrA17', 'mph(A)'),
    ('dfrA17', 'mrx(A)'),
    ('mph(A)', 'sul1'),
]

def read_csv(path: Path):
    with path.open(newline='', encoding='utf-8-sig') as handle:
        return list(csv.DictReader(handle))

def key(row):
    return frozenset((row['gene_a'], row['gene_b']))

def verify(repo: Path):
    stats = repo / 'results' / 'statistics'
    full = read_csv(stats / 'gene_pairs_all_253.csv')
    plotted = read_csv(stats / 'gene_pairs_figure2_9.csv')
    assert len(full) == 253, 'Expected 253 association tests'
    assert len(plotted) == 9 and len({key(r) for r in plotted}) == 9
    assert len({key(r) for r in full}) == 253
    fullmap = {key(r): r for r in full}
    shared = [r for r in full if float(r['Germany_q']) < .05 and float(r['Sweden_q']) < .05]
    eligible = [r for r in shared if int(r['Germany_n11']) >= 3 and int(r['Sweden_n11']) >= 3]
    assert len(shared) == 13 and len(eligible) == 9, 'Unexpected selection counts'
    assert {key(r) for r in eligible} == {key(r) for r in plotted}, 'Subset differs from all-test table'
    for r in plotted:
        original = fullmap[key(r)]
        for field in ('Germany_q', 'Sweden_q', 'Germany_lift', 'Sweden_lift', 'Germany_n11', 'Sweden_n11'):
            assert abs(float(original[field]) - float(r[field])) < 1e-12, f'Disagreement: {key(r)} {field}'
        for country in ('Germany','Sweden'):
            assert float(r[f'{country}_lift']) > 0
    assert {frozenset(pair) for pair in ORDER} == {key(r) for r in plotted}
    rows = {key(r):r for r in plotted}
    print('PASS: 253 total tests; 13 BH-significant in both collections; 9 with >=3 co-detections each')
    print('PASS: pairwise q, lift and joint counts match complete source table')
    return [rows[frozenset(pair)] for pair in ORDER]

def render(rows, dest: Path):
    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
    except ImportError as exc:
        raise SystemExit('Plotting requires matplotlib') from exc
    matrix = [[log2(float(r[f'{country}_lift'])) for country in ('Germany','Sweden')] for r in rows]
    fig, ax = plt.subplots(figsize=(8.9, 5.1))
    im = ax.imshow(matrix, cmap='Greys', vmin=0, vmax=4.25, aspect='auto')
    ax.set_xticks([0,1],['Germany (n=92)','Sweden (n=40)'])
    ax.set_yticks(range(len(rows)), [r['gene_a']+' + '+r['gene_b'] for r in rows])
    ax.tick_params(length=0)
    for i, row in enumerate(rows):
        for j,country in enumerate(('Germany','Sweden')):
            if float(row[f'{country}_q']) < .05:
                ax.text(j,i,'*',ha='center',va='center',weight='bold',fontsize=15,
                        color='white' if matrix[i][j] > 2.4 else 'black')
    fig.colorbar(im,ax=ax,fraction=.045,pad=.025,label=r'$\log_2$(lift)')
    fig.tight_layout()
    dest.mkdir(parents=True,exist_ok=True)
    for ext in ('png','pdf'):
        target=dest/f'Figure2_replicated_associations.{ext}'
        fig.savefig(target,dpi=300,facecolor='white')
        print('SAVED',target)
    plt.close(fig)

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--repo',type=Path,default=Path(__file__).resolve().parents[2])
    ap.add_argument('--check-only',action='store_true')
    ap.add_argument('--outdir',type=Path,default=None)
    a=ap.parse_args()
    rows=verify(a.repo)
    if not a.check_only:
        render(rows,a.outdir or a.repo/'figures')

if __name__=='__main__':
    main()
