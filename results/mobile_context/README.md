# Mobile-element and integron context results

The targeted genomic-context analysis covers **20** *Escherichia coli* assemblies (12 Germany, 8 Sweden) carrying the investigated `sul2`–`aph(3'')-Ib`–`aph(6)-Id` locus.

Original workflow: `../../code/bash/run_mobile_context.sh` (MOB-suite 3.1.9 and IntegronFinder 2.0.6).

## Data

- `mob_reports/`: 20 accession directories × 4 original text files = **80** reports.
- `integron_reports/`: 20 accession directories × 3 original reports = **60** reports.
- `carriers_20_FROM_S4.tsv`: **reconstructed** carrier input list from the archived S4, not the historical original launcher input.
- `report_sha256.csv`: integrity manifest for the 140 archived reports.
- `derived/`: integrated assembly-level and locus-contig analyses **reconstructed** from original reports, not primary MOB-suite or IntegronFinder files.

Use `../../code/python/verify_mobile_context_reports.py` to check local report integrity. `../../code/python/summarize_mobile_context.py` regenerates derived summaries and **can overwrite them**.

## Evidence limits

MOB-suite classifications indicate predicted plasmid association. Among 20 carriers, 11 have a replicon marker on the locus-bearing contig. Integron structures occur somewhere in 13 assemblies, but only one locus-bearing contig has a predicted integron interval; its overlap with the investigated locus is limited to **26 bp**. Five MGE annotations occur on locus-bearing contigs in two assemblies. None of these analyses experimentally establishes an entire integron-borne locus or horizontal transfer.
