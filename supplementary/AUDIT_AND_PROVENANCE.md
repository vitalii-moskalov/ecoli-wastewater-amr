# Supplementary Tables S1–S5 — audit and provenance (18 November 2026)

**Status:** the numerical data in S1–S5 have been audited; S5 has undergone an annotation-based biological review, retaining 19 context-dependent (`conditional`) assignments. The manuscript text, Table 1, Results, figure legends and abstracts remain subject to editorial reconciliation. These tables do not represent phenotypic resistance validation.

## Source hierarchy

- Primary data: 132 accession-specific AMRFinderPlus 4.2.7 TSV files (database 2026-10-29.1).
- Updated core annotation filtering: exclude `estX/sat2` hit with `INTERNAL_STOP` in `GCA_003153995.1` (407 retained, 18 excluded, 60 symbols).
- MLST / ANI: archived `mlst_all.tsv` (132 isolates; two different NOVEL allelic profiles), `skani_ani.tsv` and `.af` (8,646 pairs).
- Genetic context: 20 MOB-suite and IntegronFinder report sets, and recomputed contig-level derived summary; 140/140 source report files locally verified by SHA-256.
- Statistical associations: 253 eligible gene-pair tests, BH correction performed within each collection.

## Tables and differences relative to archived Stage 3

| Table | Rows | Decision |
|---|---:|---|
| S1 Genome manifest | 132 | **Updated:** ST and STATUS completed for all 132 assemblies from original MLST results; new `MLST_alleles` column distinguishes two NOVEL profiles. Other metadata unchanged. |
| S2 Predicted functional/contextual categories | 24 | **Retained:** counts and 95% Wilson intervals independently reproduced from corrected 60-symbol presence matrix and curated dictionary. Assignments are genotype-based and 19 are context-dependent. |
| S3 All tested co-occurrence pairs | 253 | **Retained:** p/q match independently recalculated association results; 13 pairs significant in both collections, 9 additionally pass the display rule of >=3 co-detections per collection. |
| S4 Triple-locus carriers | 20 | **Numerically retained:** all common values match recomputed original MOB/IntegronFinder context; three distance values normalized from `8595.0`/`109.0`/`0.0` to integers. |
| S5 Functional dictionary | 60 | **Curated, annotation-based:** removed disrupted `estX/sat2` annotation, corrected drug-class notes/qualification text, frequency values checked against corrected binary matrix. 41 high-assignment and 19 conditional entries; none is direct evidence of resistance phenotype. |

## Critical qualifications

1. Gene co-occurrence does **not** establish physical linkage, plasmid carriage, or horizontal transfer.
2. MOB-suite plasmid assignments are predictions from assemblies; do not state experimental plasmid closure or transmission. Among 20 carriers, 11 have a local replicon marker; 13 have genome-wide integron detections, 1 shows an integron on the locus contig, and 2 have MGE annotations on the locus contig. One integron interval overlaps the resistance locus by 26 bp; this does not make the entire locus integron-borne.
3. Sweden and Germany samples derive from different studies and sampling designs; cross-collection comparisons are not representative geographical prevalence estimates.
4. `cyaA_S352T` is classified by AMRFinderPlus as `FOSMIDOMYCIN`, not simply `FOSFOMYCIN`; the functional dictionary preserves this source category with a caveat.
5. **The repository burden statistics were recalculated after INTERNAL_STOP exclusion; the manuscript Table 1 and Results must be updated to match.** German effluent now has 42 (not 43) unique core determinant symbols and an average of 107/42 = 2.5476 (report 2.55, not 2.57) retained determinants per genome. The other two collection means remain 2.42 and 4.075 (report 4.08). CORRECTION: the retained POINT findings have `Type = AMR` and `Subtype = POINT`; there is no contradiction in the original `Scope = core, Type = AMR` selection rule. Methods should nevertheless distinguish POINT from non-POINT for gene co-occurrence and document exclusion of disrupted findings. Figure 1 category prevalences are numerically unchanged; the category labels are curated annotations, not measured resistance phenotypes.
6. S1 uses `ST = -` and `STATUS = NOVEL` for the two distinct novel profiles. Their allele strings in `MLST_alleles` differentiate them; never collapse them into one clone.

## Repository placement

S5 is released as `supplementary/Supplementary_S5_function_dictionary.csv`, identical in tabular values to `data/derived/mechanism_dictionary_60_symbols.csv`. The former provisional-name files should be deleted from the current branch to avoid two competing versions. Original AMRFinderPlus source files remain unchanged.

## Burden-analysis update (18 November 2026)

The corrected 132-genome core AMR matrix was used to reconstruct per-genome burden statistics. `results/statistics/burden_group_summary.csv` and `burden_pairwise_bootstrap.csv` are accompanied by `code/python/recalculate_burden_statistics.py` (4,000 within-group resamples, percentile intervals, recorded deterministic NumPy seeds; Mann–Whitney U and BH across three comparisons). The historical `statistics_burden.csv` used pre-correction values and should not be cited as the final result. Corrected German effluent mean is 107/42 = 2.5476; the three exploratory tests remain nonsignificant after BH correction. The reconstructed code is not the original historical bootstrap script.
