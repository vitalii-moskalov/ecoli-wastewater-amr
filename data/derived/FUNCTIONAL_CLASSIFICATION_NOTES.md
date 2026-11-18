# Functional classification audit notes

**Status:** Annotation-based functional/contextual dictionary curated and approved for repository release (18 November 2026). Nineteen entries retain context-dependent (`conditional`) interpretation.

## Input and verification

- The classification dictionary contains **60 distinct symbols** retained after exclusion of the `estX/sat2` `INTERNAL_STOP` record.
- Its symbols exactly match the 60 columns in `data/derived/presence_all_core.csv` (excluding accession).
- There are **42 non-POINT** and **18 POINT** symbols.
- The symbol-level `n_genomes` values were compared against the corrected binary matrix: **60/60 match**.
- The eight-category proportions in the existing `mechanism_prevalence_by_group.csv` were recalculated from the corrected matrix using all 132 genome accessions: **24/24 counts match**.
- **41 entries** have dictionary `confidence=high`, while **19** have `confidence=conditional`. These labels are editorial confidence in *mechanistic assignment*, **not** estimates of phenotypic resistance probability or independent experimental validation.

## Interpretation cautions

1. The eight groups comprise **mechanisms and association/context categories**, rather than eight experimentally demonstrated modes of drug resistance. In particular, `Accessory / contextual`, `Regulatory / expression-associated`, and `Indirect / transport / metabolic variant` are not direct biochemical resistance mechanisms in every carrier.
2. `cyaA_S352T` is annotated with original AMRFinderPlus `drug_class=FOSMIDOMYCIN`. Published analyses discuss this substitution in the context of **fosfomycin**; these drug names are not interchangeable, and a causal resistance phenotype is not established for every isolate carrying the variant. The source class was preserved verbatim.
3. `ptsI_V25I` and `uhpT_E350Q` are reported as fosfomycin-associated variants but should not be interpreted as evidence of fosfomycin resistance without susceptibility testing and appropriate allelic context.
4. `mrx(A)` is an accessory gene that can potentiate `mph(A)`-associated macrolide resistance, but it should not be counted as an independently established antibiotic-inactivating enzyme.
5. The raw AMRFinderPlus TSV files use `Type = AMR` for retained resistance findings, including entries where `Subtype = POINT`. Therefore `Scope = core` and `Type = AMR` are **not inconsistent** with the inclusion of POINT annotations. For the gene-only association matrix, exclude `Subtype = POINT` explicitly; describe the separate filtering of disrupted hits, including `INTERNAL_STOP`. This corrects an earlier note that incorrectly treated POINT as a `Type` value.
6. This dictionary does not demonstrate antimicrobial resistance phenotypes, physical co-localization of genes or horizontal transfer.

## Status and planned use

This curated dictionary may be released with the repository as an annotation-based classification resource. Do not describe functional assignments as experimentally established resistance phenotypes. Figure 1 uses the same eight-category count definitions; its numerical consistency has been verified, but the figure caption and manuscript distinguish predicted biochemical mechanisms from indirect/contextual associations.

## Relevant references for the interpretation cautions

- NCBI AMRFinderPlus documentation: https://www.ncbi.nlm.nih.gov/pathogens/antimicrobial-resistance/AMRFinder/
- Study on fosfomycin and nitrofurantoin resistance in *E. coli*: https://pmc.ncbi.nlm.nih.gov/articles/PMC7558542/
- NCBI AMRFinderPlus interpretation methods: https://www.ncbi.nlm.nih.gov/pathogens/docs/data_processing/
- Original mph(A)/mrx(A) functional background: https://pmc.ncbi.nlm.nih.gov/articles/PMC94651/
- 2026 experimental study on mrx cooperative resistance: https://pubmed.ncbi.nlm.nih.gov/42288131/

These links are background support for the cautions, not an assertion that all 60 symbols have been individually experimentally validated.
