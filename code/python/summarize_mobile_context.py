#!/usr/bin/env python3
"""Reconstruct contig-level MOB-suite / IntegronFinder context from archived reports.

Scientific audit reconstruction (2026-11-18), NOT an original execution script.
Run from repository root:
    python code/python/summarize_mobile_context.py
The script reads existing files and writes three derived CSVs to
results/mobile_context/derived/ (existing originals remain unchanged).
A same-contig prediction does not establish plasmid closure or HGT.
"""
from __future__ import annotations
import argparse
import csv
import re
from collections import Counter, defaultdict
from pathlib import Path


def rows(path: Path, *, comment=False, sep=','):
    with path.open(encoding='utf-8-sig', newline='') as f:
        lines = (line for line in f if not (comment and line.startswith('#')))
        return list(csv.DictReader(lines, delimiter=sep))


def contig_id(value):
    return (value or '').split()[0]


def number(value):
    return int(value)


def distance(a,b,s,e):
    return max(a-e, s-b, 0)


def tabwrite(path, data, columns):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=columns, extrasaction='ignore')
        writer.writeheader()
        writer.writerows(data)


def main(root):
    root=Path(root)
    context=root/'results/mobile_context'
    locus_path=root/'figures/figure3_locus_sequence_hashes.csv'
    mlst_path=root/'results/clonality/mlst_all.tsv'
    loci=rows(locus_path)
    carriers=rows(context/'carriers_20_FROM_S4.tsv',sep='\t')
    country_by_acc={r['accession']:r['country'] for r in carriers}
    if len(country_by_acc)!=20 or len(loci)!=20 or len({r['accession'] for r in loci})!=20:
        raise ValueError('Expected exactly 20 unique carriers and 20 locus records')
    if {r['accession'] for r in loci} != set(country_by_acc):
        raise ValueError('Carrier/locus accession mismatch')
    mlst={}
    for r in rows(mlst_path,sep='\t'):
        match=re.search(r'GCA_\d+\.\d+',r['FILE'])
        if not match: raise ValueError(f"Unparseable MLST filename {r['FILE']}")
        acc=match.group(0)
        if acc in mlst: raise ValueError(f'Duplicate MLST accession {acc}')
        mlst[acc]=r
    summary=[]; mges_out=[]; int_out=[]
    for locus in loci:
        acc=locus['accession']; contig=locus['contig']; s=int(locus['span_start']);e=int(locus['span_stop'])
        if locus['country']!=country_by_acc[acc] or e-s+1!=int(locus['span_len']):
            raise ValueError(f'Locus metadata mismatch {acc}')
        mob_base=context/'mob_reports'/acc
        int_base=context/'integron_reports'/acc
        mob_contigs=rows(mob_base/'contig_report.txt',sep='\t')
        hits=[r for r in mob_contigs if contig_id(r['contig_id'])==contig]
        if len(hits)!=1: raise ValueError(f'Expected unique contig in MOB-suite {acc}/{contig}; got {len(hits)}')
        hit=hits[0]
        length=int(hit['size'])
        if not 1<=s<=e<=length: raise ValueError(f'Locus outside reported contig {acc}')
        mob_clusters=rows(mob_base/'mobtyper_results.txt',sep='\t')
        cluster=[r for r in mob_clusters if r.get('primary_cluster_id')==hit['primary_cluster_id']]
        mge_hits=[]
        for r in rows(mob_base/'mge.report.txt',sep='\t'):
            if contig_id(r['contig_id']) != contig:continue
            a=int(r['contig_start']);b=int(r['contig_end'])
            gap=distance(a,b,s,e)
            mge_hits.append(gap)
            mges_out.append(dict(accession=acc,country=locus['country'],contig=contig,
                mge_type=r.get('mge_type',''),mge_subtype=r.get('mge_subtype',''),
                mge_id=r.get('mge_id',''),start=a,stop=b,distance_to_locus_bp=gap))
        integron_files=list(int_base.glob('*.integrons'))
        if len(integron_files)!=1:
            raise ValueError(f'Expected one IntegronFinder .integrons report for {acc}; found {len(integron_files)}')
        intraw=integron_files[0].read_text(encoding='utf-8')
        int_rows=rows(integron_files[0],comment=True,sep='\t') if 'ID_integron' in intraw else []
        genome_integrons={r['ID_integron'] for r in int_rows}
        locus_integrons=defaultdict(list)
        for r in int_rows:
            if contig_id(r['ID_replicon']) == contig:
                locus_integrons[r['ID_integron']].append(r)
        int_gaps=[]
        for integron_id, rset in locus_integrons.items():
            a=min(int(r['pos_beg']) for r in rset); b=max(int(r['pos_end']) for r in rset)
            gap=distance(a,b,s,e); overlap=max(0,min(b,e)-max(a,s)+1)
            int_gaps.append(gap)
            int_out.append(dict(accession=acc,country=locus['country'],contig=contig,
                integron_id=integron_id,start=a,stop=b,distance_to_locus_bp=gap,
                interval_overlap_bp=overlap))
        m=mlst.get(acc)
        if m is None: raise ValueError(f'No MLST record for {acc}')
        summary.append(dict(accession=acc,country=locus['country'],contig=contig,
            locus_start=s,locus_end=e,locus_length=e-s+1,locus_sha256=locus['sha256'],
            contig_length=length,left_flank_bp=s-1,right_flank_bp=length-e,
            mob_molecule_type=hit['molecule_type'],mob_cluster_id=hit['primary_cluster_id'],
            mob_rep_type_contig=hit['rep_type(s)'],
            mob_predicted_mobility_contig=hit['predicted_mobility'],
            mob_reconstructed_plasmid_count=len(mob_clusters),
            mob_cluster_rep_types='|'.join(r['rep_type(s)'] for r in cluster),
            mob_cluster_predicted_mobility='|'.join(r['predicted_mobility'] for r in cluster),
            mge_count_on_locus_contig=len(mge_hits),
            nearest_mge_distance_bp=min(mge_hits) if mge_hits else '',
            integrons_genome=len(genome_integrons),integrons_locus_contig=len(locus_integrons),
            nearest_integron_distance_bp=min(int_gaps) if int_gaps else '',
            ST=m['ST'],STATUS=m['STATUS'],ALLELES=m['ALLELES']))
    if len(summary)!=20:raise ValueError('Expected 20 records')
    out=context/'derived'
    tabwrite(out/'carrier_mobile_context.csv',summary,list(summary[0]))
    tabwrite(out/'mge_on_locus_contigs.csv',mges_out,list(mges_out[0]) if mges_out else ['accession','country','contig','mge_type','mge_subtype','mge_id','start','stop','distance_to_locus_bp'])
    tabwrite(out/'integrons_on_locus_contigs.csv',int_out,list(int_out[0]) if int_out else ['accession','country','contig','integron_id','start','stop','distance_to_locus_bp','interval_overlap_bp'])
    print('Carriers:',len(summary),'Countries:',dict(Counter(r['country'] for r in summary)))
    print('MOB-suite plasmid-associated locus contigs:',sum(r['mob_molecule_type']=='plasmid' for r in summary))
    print('Replicon marker on locus contig:',sum(r['mob_rep_type_contig'] not in ('','-') for r in summary))
    print('Genomes with detected integron:',sum(r['integrons_genome']>0 for r in summary))
    print('Genomes with integron on locus contig:',sum(r['integrons_locus_contig']>0 for r in summary))
    print('Genomes with MGE annotation on locus contig:',sum(r['mge_count_on_locus_contig']>0 for r in summary))
    print('Derived outputs:',out)

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--root',default='.',help='Path to root of repository (default: working directory)')
    a=p.parse_args(); main(a.root)
