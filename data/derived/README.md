# Derived data

This directory contains processed antimicrobial resistance annotation tables and analytical matrices generated from the original AMRFinderPlus results for 132 wastewater-derived *Escherichia coli* genomes.

## Principal datasets

- `core_amr_hits.csv` — filtered core AMR annotations.
- `presence_all_core.csv` — binary matrix including retained core AMR gene and point-mutation determinants.
- `presence_gene_only.csv` — binary matrix restricted to non-POINT annotations.
- `mechanism_dictionary_61_symbols.csv` — curated functional classification of resistance determinants.

Each distinct determinant symbol is counted once per genome in the binary matrices.

## Interpretation

Non-POINT annotations must not automatically be interpreted as horizontally acquired resistance genes.

Functional classifications represent predicted molecular mechanisms rather than experimentally confirmed resistance phenotypes.

Statistical associations between resistance genes do not establish physical genetic linkage or horizontal gene transfer.

## Validation status

The analytical matrices have been compared against the original AMRFinderPlus outputs. Functional mechanism assignments and final manuscript consistency remain subject to scientific audit.
