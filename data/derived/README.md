# Curated and derived AMR data

The original per-assembly AMRFinderPlus files are in [`../annotations/`](../annotations/). This directory contains products of the conservative 2026-11-18 audit:

| File | Description |
| --- | --- |
| `core_amr_hits.csv` | **407** retained AMRFinderPlus records |
| `excluded_uncertain_hits.csv` | **18** excluded records, including one `INTERNAL_STOP` finding |
| `presence_all_core.csv` | Binary per-genome matrix, **60** retained determinant symbols |
| `presence_gene_only.csv` | Binary per-genome matrix, **42** non-POINT symbols |
| `mechanism_dictionary_60_symbols.csv` | Curated annotation-based assignment of retained symbols to functional/contextual categories (41 high, 19 conditional) |
| `FUNCTIONAL_CLASSIFICATION_NOTES.md` | Caveats and ambiguous functional assignments |

One determinant symbol is counted at most once per assembly in the presence matrices. The `INTERNAL_STOP` hit for `estX/sat2` was removed as part of the final conservative filtering audit; original TSVs were not changed.

The 60-symbol dictionary includes **19 conditional** assignments. Figure 1 category frequencies are reproducible under this dictionary, but **not** phenotypic resistance measurements. Non-POINT hits should not automatically be called horizontally acquired ARGs.

Use `../../code/python/verify_amr_data.py` to validate the tables against original reports and checksums. Statistical co-occurrence does not establish same-contig linkage, plasmid carriage, or transfer.
