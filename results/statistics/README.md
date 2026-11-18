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

Validation/plotting: `../../code/python/figure1.py`. The category dictionary is **provisional**, and these are not experimentally verified resistance mechanisms.

## Limitations

Genome independence is assumed by the pairwise tests; the primary tests do not control phylogenetic population structure. Differences in study design preclude nationally representative comparison. Statistical co-occurrence is not physical gene linkage, plasmid assignment, or proof of horizontal transfer.
