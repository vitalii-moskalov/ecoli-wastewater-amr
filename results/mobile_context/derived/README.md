# Derived mobile-context summaries

This directory contains derived, assembly-level summaries reconstructed during the scientific audit of the wastewater-derived *Escherichia coli* study (18 November 2026). These tables were generated from archived MOB-suite 3.1.9, IntegronFinder 2.0.6 and MLST outputs and the coordinate information underlying Figure 3. They are **not original tool outputs**.

## Files

- `carrier_mobile_context.csv` — integrated locus-contig, MOB-suite, integron, mobile-element and MLST information for 20 assemblies (12 German; 8 Swedish).
- `mge_on_locus_contigs.csv` — five predicted MGE annotations on locus-bearing contigs from two assemblies; distances to the study locus are reported in base pairs.
- `integrons_on_locus_contigs.csv` — one integron-associated interval identified on a locus-bearing contig. The reported interval overlaps the locus interval by 26 bp; this does **not** establish that the complete three-gene locus is part of the integron.

## Reproduction

Run from the root of a local copy of the repository:

```bash
python code/python/summarize_mobile_context.py
```

Inputs are `figures/figure3_locus_sequence_hashes.csv`, `results/clonality/mlst_all.tsv`, `results/mobile_context/carriers_20_FROM_S4.tsv` and the reports under `results/mobile_context/mob_reports/` and `results/mobile_context/integron_reports/`.

The script **overwrites the three derived CSV outputs** when rerun, but leaves original tool reports unchanged. It was developed during the November 2026 audit and must not be represented as an original historical analysis script.

## Evidence limits

MOB-suite assignments are computational predictions, not proof of closed plasmids. Co-occurrence of genes, contig-level colocalization and evidence of horizontal transfer are distinct. The predicted integron interval is reconstructed from reported features and is not equivalent to experimental confirmation of its complete genomic structure. Genomic assemblies may be fragmented.
