# Statistical results

## ARG co-occurrence

The 132-genome non-POINT matrix includes 42 retained determinant symbols, of which **23** were observed in at least three assemblies overall. This yields **253 unique pairs**. One-sided Fisher exact tests for positive associations were performed separately for Germany (92 assemblies, influent and effluent combined) and Sweden (40 assemblies). Benjamini–Hochberg FDR adjustment was performed separately across the 253 tests within each collection.

- `gene_pairs_all_253.csv`: full tested set.
- `gene_pairs_both_fdr_13.csv`: 13 pairs meeting FDR < 0.05 in **both** collections.
- `gene_pairs_figure2_9.csv`: display subset requiring at least three co-detections in **each** collection (a descriptive presentation rule, not a significance test).
- `gene_pair_audit_summary.json`: audit settings and summary.

Recalculation: `../../code/python/recalculate_gene_cooccurrence.py`. This reconstructed script is **not** the original historical analysis script.

## Figure 1 functional and contextual categories

- `mechanism_prevalence_by_group.csv`: eight predicted categories × three collection groups (24 rows); percentages are per assembly with at least one assigned feature, including 95% Wilson confidence intervals.
- `germany_mechanism_fisher_bh.csv`: eight German influent-versus-effluent Fisher tests with BH correction; none is significant at FDR < 0.05.

Validation/plotting: `../../code/python/figure1.py`. The dictionary has been curated with 19 explicitly conditional assignments; the categories are genotype-based and not experimentally verified phenotypic mechanisms.

## Per-genome AMR determinant burden and bootstrap

- `burden_group_summary.csv`: corrected counts, means, medians and numbers of genomes with at least one retained core determinant (50 German influent, 42 German effluent and 40 Swedish wastewater genomes).
- `burden_pairwise_bootstrap.csv`: three pairwise mean differences, 95% percentile bootstrap intervals, two-sided Mann–Whitney U p-values and BH-adjusted q-values.

Recalculation: `../../code/python/recalculate_burden_statistics.py`. It uses the **corrected 132 × 60** core AMR presence matrix, **4,000 bootstrap resamples with replacement within groups**, and independent NumPy random generators seeded with **20261118, 20261119 and 20261120** for the three pairwise comparisons. The statistic is *mean of the second group minus mean of the first group*. Percentile limits are 2.5% and 97.5% quantiles of 4,000 resampled mean differences. The tests use SciPy `mannwhitneyu` (two-sided, `method=auto`); BH correction is applied to the three p-values using statsmodels. Python package versions should be recorded before a software release is frozen.

The code was **reconstructed during the 18 November 2026 audit**; it is not the original historical bootstrap implementation. Its outputs supersede the earlier `statistics_burden.csv` estimates based on the pre-correction matrix. All three corrected bootstrap intervals include zero and all three q-values are ≥ 0.05. Running without `--out` writes files into `results/statistics/`; use a separate output directory when validating a clean copy.

## Limitations

Genome independence is assumed by the pairwise tests; the primary tests do not control phylogenetic population structure. Differences in study design preclude nationally representative comparison. Statistical co-occurrence is not physical gene linkage, plasmid assignment, or proof of horizontal transfer.
