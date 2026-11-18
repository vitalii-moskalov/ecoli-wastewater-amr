# Mobile genetic element and integron context

This directory contains computational genomic-context results for 20 *Escherichia coli* assemblies carrying the investigated sul2–aph(3'')-Ib–aph(6)-Id locus.

The analyzed subset comprises 12 German and 8 Swedish assemblies.

## Software

- MOB-suite 3.1.9
- IntegronFinder 2.0.6

The original Bash execution script is available at `../../code/bash/run_mobile_context.sh`.

## Contents

- `mob_reports/` — original MOB-suite text reports for 20 assemblies, including contig classification, plasmid typing, and mobile genetic element predictions.
- `integron_reports/` — original IntegronFinder reports for the same 20 assemblies.
- `carriers_20_FROM_S4.tsv` — reconstructed accession list derived from Supplementary Table S4.
- `report_sha256.csv` — file integrity and provenance records for 140 original text reports.

The original analysis archive contains 20 successful completion markers for each program.

## Interpretation

MOB-suite plasmid assignments and mobility classifications are computational predictions, not experimental confirmation of plasmid structure or horizontal transfer.

Integrons detected within an assembly are not necessarily located on the contig carrying the investigated resistance locus.

Statistical ARG co-occurrence, physical gene co-localization, and horizontal gene transfer are distinct levels of evidence.

## Reproducibility

The text reports are preserved without modifying their original content. Large intermediate FASTA reconstructions are retained separately in the original analysis archive and are not duplicated in this directory.

The carrier accession list was reconstructed from archived results and should not be represented as the original historical input file.

Final interpretation of the genetic context remains subject to integration with the locus coordinates, MLST/ANI results, and manuscript.
