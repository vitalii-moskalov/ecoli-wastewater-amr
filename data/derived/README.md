# Derived data

This directory contains processed antimicrobial resistance annotation tables and analytical matrices generated from the original AMRFinderPlus results for 132 wastewater-derived *Escherichia coli* genome assemblies.

## Principal datasets

- `core_amr_hits.csv` — 407 retained core AMR annotation records.
- `excluded_uncertain_hits.csv` — 18 excluded annotation records, including the `INTERNAL_STOP` finding.
- `presence_all_core.csv` — binary presence–absence matrix containing 60 distinct retained AMR determinant symbols.
- `presence_gene_only.csv` — binary presence–absence matrix containing 42 non-POINT determinant symbols.

Each distinct determinant symbol is counted once per genome in the binary matrices.

## Filtering and validation

The original AMRFinderPlus TSV files are preserved without modification in `../annotations/`.

The analytical filtering excludes uncertain or potentially disrupted annotations according to the documented filtering criteria.

The `estX/sat2` annotation with an `INTERNAL_STOP` match was excluded during the final scientific audit on 18 November 2026 to maintain consistency with the stated conservative filtering approach.

The corrected matrices were independently checked against the original annotation outputs.

The validation procedure is documented in `../../code/python/verify_amr_data.py`.

## Functional classification

Functional mechanism assignments remain subject to final scientific review.

Predicted antimicrobial resistance mechanisms should not be interpreted as experimentally confirmed resistance phenotypes.

Non-POINT annotations do not necessarily represent horizontally acquired resistance genes.

## Statistical interpretation

Statistical co-occurrence of resistance determinants does not establish physical genetic linkage, plasmid localization, or horizontal gene transfer.

The correction of the `INTERNAL_STOP` annotation did not change the set of 23 genes eligible for the reported pairwise co-occurrence analysis or its 253 statistical comparisons.

## Reproducibility status

The annotation filtering and presence–absence matrices have undergone independent computational verification.

Final functional classification and manuscript consistency checks are ongoing.
