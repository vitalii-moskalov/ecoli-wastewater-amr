# Statistical analysis results

This directory contains reproducible statistical outputs from the comparative analysis of antimicrobial resistance determinants in 132 wastewater-derived *Escherichia coli* genome assemblies.

## Gene co-occurrence analysis

Pairwise associations were evaluated using the non-POINT gene presence–absence matrix.

Genes detected in at least three genomes across the complete dataset were eligible for analysis.

The analysis included:

- 23 eligible gene symbols.
- 253 unique gene pairs.
- 92 German genomes (influent and effluent combined).
- 40 Swedish genomes.

Positive associations were evaluated using one-sided Fisher's exact tests. Benjamini–Hochberg false discovery rate correction was applied separately to all 253 tests within each collection.

## Output files

- `gene_pairs_all_253.csv` — complete pairwise association results.
- `gene_pairs_both_fdr_13.csv` — 13 pairs with q < 0.05 in both collections.
- `gene_pairs_figure2_9.csv` — nine pairs additionally meeting the criterion of at least three joint detections in each collection.
- `gene_pair_audit_summary.json` — computational settings and verification summary.

## Reproducibility

The results can be independently recalculated using:

`../../code/python/recalculate_gene_cooccurrence.py`

This Python script was reconstructed during the scientific audit on 18 November 2026 and is not the original historical analysis script.

## Interpretation and limitations

Gene co-occurrence represents statistical association and does not establish physical linkage, plasmid localization, or horizontal gene transfer.

The pairwise tests assume independent genomes and do not formally account for bacterial population structure or clonality.

Differences in sampling and isolate-selection procedures preclude population-level interpretation of between-country prevalence differences.

The nine pairs included in Figure 2 represent a predefined display subset of the 13 pairs meeting the statistical significance criterion in both collections. The additional co-detection threshold is a descriptive selection rule, not a separate statistical significance test.

These analyses are exploratory and should be interpreted accordingly.
