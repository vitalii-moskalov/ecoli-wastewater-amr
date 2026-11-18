#!/usr/bin/env python3
"""Verify and recreate manuscript Figure 3 (locus geometry and sequence variants).

Reconstructed for repository documentation on 2026-11-18; NOT original historical code.
Figure-specific data (3 exact AMRFinderPlus coordinates and 20 independently
archived locus-sequence SHA-256 identifiers) are in figures/.

Usage from the repository root:
    python code/python/figure3.py --check-only
    python code/python/figure3.py
Requires matplotlib only for plotting. Does not alter source data.
"""
from __future__ import annotations
import argparse
import csv
from collections import Counter, defaultdict
from pathlib import Path

GENES = ['sul2', "aph(3'')-Ib", 'aph(6)-Id']
REFERENCE = 'GCA_003145035.1'

def csvrows(path):
    with path.open(newline='',encoding='utf-8-sig') as f:
        return list(csv.DictReader(f))

def verify(repo):
    folder=repo/'figures'
    loc=csvrows(folder/'figure3_reference_gene_coordinates.csv')
    hashes=csvrows(folder/'figure3_locus_sequence_hashes.csv')
    assert len(loc)==3 and {r['Element symbol'] for r in loc}==set(GENES)
    assert {r['accession'] for r in loc}=={REFERENCE}
    assert len({r['Contig id'] for r in loc})==1
    assert {r['Strand'] for r in loc}=={'-'}
    lo=min(int(r['Start']) for r in loc)
    hi=max(int(r['Stop']) for r in loc)
    length=hi-lo+1
    assert length==2513, f'Unexpected locus span: {length}'
    # Transform the reference '-' oriented contig coordinates to sul2->aph->aph orientation.
    parts=sorted((hi-int(r['Stop']), hi-int(r['Start'])+1, r['Element symbol']) for r in loc)
    assert [r[2] for r in parts] == GENES
    assert [parts[i+1][0]-parts[i][1] for i in (0,1)]==[63,2]
    assert len(hashes)==20 and len({r['accession'] for r in hashes})==20
    assert Counter(r['country'] for r in hashes)=={'Germany':12,'Sweden':8}
    assert all(r['span_len']=='2513' for r in hashes)
    for r in hashes:
        assert len(r['sha256'])==64 and all(c in '0123456789abcdef' for c in r['sha256'])
    counts=defaultdict(Counter)
    for r in hashes:
        counts[r['sha256']][r['country']]+=1
    assert len(counts)==6, 'Expected six distinct nucleotide sequence variants'
    sorted_hashes=sorted(counts,key=lambda h:(-sum(counts[h].values()),-counts[h]['Germany'],-counts[h]['Sweden'],h))
    values=[(f'V{i}',h,counts[h]['Germany'],counts[h]['Sweden']) for i,h in enumerate(sorted_hashes,1)]
    assert sum(v[2]+v[3] for v in values)==20
    assert sum(v[2]>0 and v[3]>0 for v in values)==3
    assert [(v[2],v[3]) for v in values]==[(6,1),(2,5),(1,2),(1,0),(1,0),(1,0)]
    print('PASS: 2513-bp locus; gene order sul2–aph(3\'\')-Ib–aph(6)-Id; gaps 63 and 2 bp')
    print('PASS: 20 sequences, 6 exact variants, 3 shared (12 German and 8 Swedish carriers)')
    return length,parts,values

def render(length,parts,values,dest):
    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        from matplotlib.patches import FancyArrow
    except ImportError as exc:
        raise SystemExit('Plotting requires matplotlib') from exc
    fig,(a,b)=plt.subplots(2,1,figsize=(9,5.1),gridspec_kw={'height_ratios':[.85,1.55],'hspace':.75})
    shades=['#555555','#888888','#b1b1b1']
    for i,(start,end,label) in enumerate(parts):
        span=end-start
        # Arrow extends across the predicted coding segment; source coordinates are inclusive.
        a.arrow(start,.5,max(0,span-38),0,width=.20,head_width=.30,head_length=46,
                length_includes_head=True,color=shades[i],ec=shades[i],lw=.5)
        a.text((start+end)/2,.5,label,color='white',weight='bold',ha='center',va='center',fontsize=11)
    a.set_xlim(-40,length+40);a.set_ylim(0,1);a.axis('off');a.text(-.055,1.13,'A',transform=a.transAxes,fontsize=14,weight='bold')
    yy=list(range(len(values)))
    g=[v[2] for v in values];s=[v[3] for v in values]
    b.barh(yy,g,color='#5b5b5b',label='Germany')
    b.barh(yy,s,left=g,color='#b5b5b5',label='Sweden')
    b.set_yticks(yy,[v[0] for v in values]);b.invert_yaxis();b.set_xlim(0,12)
    b.set_xlabel('Genomes carrying locus variant (n)')
    b.legend(frameon=False,loc='upper right')
    b.spines[['top','right']].set_visible(False)
    b.text(-.055,1.08,'B',transform=b.transAxes,fontsize=14,weight='bold')
    fig.subplots_adjust(left=.12, right=.96, top=.90, bottom=.10)
    dest.mkdir(parents=True,exist_ok=True)
    for ext in ('png','pdf'):
        target=dest/f'Figure3_locus_architecture.{ext}'
        fig.savefig(target,dpi=300,facecolor='white')
        print('SAVED',target)
    plt.close(fig)

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--repo',type=Path,default=Path(__file__).resolve().parents[2])
    ap.add_argument('--check-only',action='store_true')
    ap.add_argument('--outdir',type=Path,default=None)
    args=ap.parse_args()
    length,parts,variants=verify(args.repo)
    if not args.check_only:
        render(length,parts,variants,args.outdir or args.repo/'figures')

if __name__=='__main__':
    main()
