# Supplementary Tables S1–S5 — audited study datasets

The tabulated data have been numerically audited as of 18 November 2026. S5 has undergone annotation-based curation, with 19 context-dependent assignments retained; it does not establish phenotypic antimicrobial resistance. The main manuscript remains under editorial revision.

| File | Description |
| --- | --- |
| `Supplementary_S1_manifest.csv` | Genome manifest for 132 assemblies, with complete MLST profiles and two distinct NOVEL allele vectors |
| `Supplementary_S2_mechanisms.csv` | 8 predicted functional/contextual categories × 3 collections (24 rows) |
| `Supplementary_S3_all_pair_tests.csv` | Full set of 253 ARG association tests; 13 meet both-collection FDR threshold and 9 meet the figure display criterion |
| `Supplementary_S4_locus_carriers.csv` | 20 locus carriers, coordinates and related contextual results |
| `Supplementary_S5_function_dictionary.csv` | 60 curated determinant annotations; conditional biological assignments clearly identified |
| `audit_summary.json` | Audit machine-readable summary |
| `AUDIT_AND_PROVENANCE.md` | Source hierarchy, changes and remaining limitations |

The original `estX/sat2` `INTERNAL_STOP` record was removed from derived core tables, not from the raw AMRFinderPlus file. S1 was populated with MLST results for **all 132** assemblies. S4 numerical formatting was normalized without changing underlying values.

Read `AUDIT_AND_PROVENANCE.md` before interpreting these tables. Database predictions do not establish phenotypic resistance, clonal transmission, plasmid closure or horizontal gene transfer. National prevalence claims are not justified by these two independently sampled collections.
