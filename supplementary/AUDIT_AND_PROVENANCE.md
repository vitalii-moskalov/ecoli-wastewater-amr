# Supplementary Tables S1–S5 — audited working draft (18 November 2026)

**Status:** computationally cross-checked draft, NOT manuscript-approved supplementary material. The S5 functional mapping remains provisional and requires final biological review. Do not label the entire set "final" until manuscript Table 1, Methods, Results, Figure legends, and Supplementary Table captions have been reconciled.

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
| S2 Predicted functional/contextual categories | 24 | **Retained:** counts and 95% Wilson intervals independently reproduced from corrected 60-symbol presence matrix and provisional dictionary. Biologic classification remains provisional. |
| S3 All tested co-occurrence pairs | 253 | **Retained:** p/q match independently recalculated association results; 13 pairs significant in both collections, 9 additionally pass the display rule of >=3 co-detections per collection. |
| S4 Triple-locus carriers | 20 | **Numerically retained:** all common values match recomputed original MOB/IntegronFinder context; three distance values normalized from `8595.0`/`109.0`/`0.0` to integers. |
| S5 Functional dictionary | 60 | **Updated, provisional:** removed disrupted `estX/sat2` annotation, corrected drug-class notes/qualification text, frequency values checked against corrected binary matrix. 41 high-assignment and 19 conditional entries; none is direct evidence of resistance phenotype. |

## Critical qualifications

1. Gene co-occurrence does **not** establish physical linkage, plasmid carriage, or horizontal transfer.
2. MOB-suite plasmid assignments are predictions from assemblies; do not state experimental plasmid closure or transmission. Among 20 carriers, 11 have a local replicon marker; 13 have genome-wide integron detections, 1 shows an integron on the locus contig, and 2 have MGE annotations on the locus contig. One integron interval overlaps the resistance locus by 26 bp; this does not make the entire locus integron-borne.
3. Sweden and Germany samples derive from different studies and sampling designs; cross-collection comparisons are not representative geographical prevalence estimates.
4. `cyaA_S352T` is classified by AMRFinderPlus as `FOSMIDOMYCIN`, not simply `FOSFOMYCIN`; the functional dictionary preserves this source category with a caveat.
5. **Manuscript Table 1 and any n_core summaries/bootstraps need explicit rechecking after INTERNAL_STOP exclusion.** German effluent now has 42 (not 43) unique core determinant symbols and an average of 107/42 = 2.5476 (report 2.55, not 2.57) retained determinants per genome. The other two collection means remain 2.42 and 4.075 (report 4.08). The manuscript statement that only `Type = AMR` findings were retained is inconsistent with inclusion of 18 `POINT` symbols; clarify the actual filtering rules. Figure 1 category prevalences are numerically unchanged, but biological interpretation has not been finalized.
6. S1 uses `ST = -` and `STATUS = NOVEL` for the two distinct novel profiles. Their allele strings in `MLST_alleles` differentiate them; never collapse them into one clone.

## Repository placement

Upload CSVs to `supplementary/`, keeping these names. Consider renaming the provisional S5 to the journal-required title only after the final biology review. This supplementary audit does not alter primary source data.
