#!/usr/bin/env python3
"""Reproduce isolate-level AMR determinant burden comparisons.

Reconstructed and audited 2026-11-18 from corrected presence_all_core.csv.
This script is NOT the original historical bootstrap code; its recorded seed
makes the newly reported interval estimates exactly reproducible under the
specified computational environment.

Run from repository root:
  python code/python/recalculate_burden_statistics.py
Optional:
  python code/python/recalculate_burden_statistics.py --seed 20261118 --resamples 4000

Dependencies: numpy, scipy, statsmodels (already used by manuscript analyses).
Output: results/statistics/burden_group_summary.csv and
        results/statistics/burden_pairwise_bootstrap.csv.
Input files are never modified.
"""
from __future__ import annotations
import argparse
import csv
from pathlib import Path
import numpy as np
from scipy.stats import mannwhitneyu
from statsmodels.stats.multitest import multipletests

GROUPS = ('Germany influent', 'Germany effluent', 'Sweden wastewater')
N = {'Germany influent': 50, 'Germany effluent': 42, 'Sweden wastewater': 40}
PAIRS = ((GROUPS[0],GROUPS[1]), (GROUPS[0],GROUPS[2]), (GROUPS[1],GROUPS[2]))


def read_csv(path):
    with path.open(encoding='utf-8-sig', newline='') as f:
        return list(csv.DictReader(f))


def save_csv(path, records, fields):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w', encoding='utf-8', newline='') as f:
        w=csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(records)


def main():
    pa=argparse.ArgumentParser(description=__doc__)
    pa.add_argument('--repo', type=Path, default=Path(__file__).resolve().parents[2])
    pa.add_argument('--out', type=Path, default=None)
    pa.add_argument('--resamples', type=int, default=4000)
    pa.add_argument('--seed', type=int, default=20261118)
    args=pa.parse_args()
    if args.resamples < 100: raise ValueError('Resamples must be at least 100')
    repo=args.repo.resolve()
    manifest=read_csv(repo/'data/sample_manifest.csv')
    matrix=read_csv(repo/'data/derived/presence_all_core.csv')
    if len(manifest)!=132 or len(matrix)!=132: raise ValueError('Expected 132 assemblies')
    symbols=list(matrix[0].keys())
    if symbols[0]!='accession' or len(symbols)!=61: raise ValueError('Expected accession plus 60 determinants')
    groups={r['accession']:r['group'] for r in manifest}
    if len(groups)!=132: raise ValueError('Duplicate accessions in manifest')
    counts={g:[] for g in GROUPS}
    ids=set()
    for r in matrix:
        a=r['accession']
        if a in ids or a not in groups: raise ValueError('Duplicate or unexpected accession: '+a)
        ids.add(a)
        values=[r[s] for s in symbols[1:]]
        if any(v not in ('0','1') for v in values): raise ValueError('Nonbinary matrix entry: '+a)
        counts[groups[a]].append(sum(map(int,values)))
    if set(groups)!=ids: raise ValueError('Incomplete accession set')
    if {g:len(v) for g,v in counts.items()}!=N: raise ValueError('Unexpected group sizes')
    x={g:np.array(v,dtype=np.int64) for g,v in counts.items()}
    # Fixed design: within-group nonparametric bootstrap, with replacement;
    # independent deterministic seed per pair; difference = second - first;
    # unweighted percentile bounds from sorted 4000 bootstrap differences.
    group_rows=[]
    for g in GROUPS:
        vals=x[g]
        group_rows.append({'group':g,'n':len(vals),'total_symbols':int(vals.sum()),
                           'mean':f'{vals.mean():.8f}', 'median':f'{np.median(vals):.8f}',
                           'n_positive':int((vals>0).sum())})
    ps=[float(mannwhitneyu(x[a],x[b],alternative='two-sided',method='auto').pvalue)
        for a,b in PAIRS]
    qs=multipletests(ps,method='fdr_bh')[1]
    rows=[]
    for i,((a,b),p,q) in enumerate(zip(PAIRS,ps,qs)):
        rng=np.random.default_rng(args.seed + i)
        aa=x[a]; bb=x[b]
        ax=aa[rng.integers(0,len(aa),size=(args.resamples,len(aa)))].mean(axis=1)
        bx=bb[rng.integers(0,len(bb),size=(args.resamples,len(bb)))].mean(axis=1)
        low,high=np.quantile(bx-ax,[0.025,0.975],method='linear')
        rows.append({'group_a':a,'group_b':b,'n_a':len(aa),'n_b':len(bb),
                     'mean_diff_b_minus_a':f'{bb.mean()-aa.mean():.8f}',
                     'ci95_lower':f'{low:.8f}','ci95_upper':f'{high:.8f}',
                     'ci_contains_zero':str(low<=0<=high).lower(),
                     'mw_u_p_two_sided':f'{p:.12g}','mw_bh_q_3':f'{q:.12g}',
                     'bootstrap_n':args.resamples,'seed':args.seed+i})
    out=args.out if args.out else repo/'results/statistics'
    save_csv(out/'burden_group_summary.csv',group_rows,list(group_rows[0]))
    save_csv(out/'burden_pairwise_bootstrap.csv',rows,list(rows[0]))
    print('PASS: 132 assemblies, 60 symbols, group N=50/42/40')
    for r in rows:
        print(f"{r['group_a']} vs {r['group_b']}: difference={float(r['mean_diff_b_minus_a']):.3f}; "
              f"95% percentile bootstrap [{float(r['ci95_lower']):.3f}, {float(r['ci95_upper']):.3f}], "
              f"p={float(r['mw_u_p_two_sided']):.4f}, q={float(r['mw_bh_q_3']):.4f}")
    print('NOTE: reconstruction, not evidence of the original historical bootstrap seed')

if __name__=='__main__': main()
