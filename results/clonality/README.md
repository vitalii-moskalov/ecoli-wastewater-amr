# MLST and ANI results

This directory contains multilocus sequence typing (MLST) and average nucleotide identity (ANI) results for 132 wastewater-derived *Escherichia coli* genome assemblies.

## Contents

- `mlst_all.tsv` — original MLST results for 132 assemblies.
- `skani_ani.tsv` — original triangular ANI matrix.
- `skani_ani.tsv.af` — aligned-fraction matrix.
- `pairwise_ani_af.csv` — derived table of 8,646 pairwise comparisons.

## Software

- mlst 2.35.0, Achtman scheme (`ecoli_achtman_4`)
- skani 0.4.0

## Validation

All 132 assemblies match the genome accession manifest. Two assemblies have distinct NOVEL MLST allele profiles and must not be treated as a single sequence type.

Pairwise ANI and aligned-fraction values were verified against the original skani matrices.

The original execution workflow is documented in `../../code/bash/run_clonality.sh`. An independent validation script is provided in `../../code/python/verify_clonality_results.py`.

MLST and ANI describe bacterial genetic relatedness; they do not independently establish horizontal transfer of antimicrobial resistance genes.
