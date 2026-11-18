# Figures

This directory contains the main figures used in the manuscript on antimicrobial resistance determinants in wastewater-derived *Escherichia coli*.

## Contents

### Figure 1. Functional categories of AMR determinants
- `Figure1_functional_context_categories.png`
- `Figure1_functional_context_categories.pdf`

This figure summarizes the prevalence of the major predicted antimicrobial resistance mechanism categories across the three study groups:
- German influent
- German effluent
- Swedish wastewater

The figure was generated from processed AMR annotation data and validated prevalence summaries.

### Figure 2. Replicated ARG associations
- `Figure2_replicated_associations.png`
- `Figure2_replicated_associations.pdf`

This figure shows selected pairwise co-occurrence relationships among antimicrobial resistance genes identified in the non-POINT gene presence–absence matrix.

The plotted associations represent the subset selected for visualization from the full reproducible statistical results.

### Figure 3. Locus architecture
- `Figure3_locus_architecture.png`
- `Figure3_locus_architecture.pdf`

This figure illustrates the genomic organization of the investigated sul2–aph(3'')-Ib–aph(6)-Id locus and its structural variation among the analyzed *E. coli* genomes.

Where provided, accompanying source tables document the locus coordinates and structural variants used for plotting.

## Reproducibility

The corresponding figure-generation scripts are stored in:

- `../code/python/figure1.py`
- `../code/python/figure2.py`
- `../code/python/figure3.py`

Supporting processed data and statistical outputs are stored elsewhere in the repository, primarily in:

- `../data/derived/`
- `../results/statistics/`

These figures are intended to represent the final manuscript versions.  
PNG files are suitable for quick viewing and manuscript drafting.  
PDF files are provided for high-resolution and vector-based use.

## Notes

- Figures were generated from curated and validated intermediate data rather than directly from raw NCBI downloads.
- Some figures depend on processed analytical tables produced in earlier workflow steps.
- If the scripts are re-run after updates to the source tables or filtering rules, minor visual or numerical changes may occur.

## Provenance

This directory is part of the repository:

**ecoli-wastewater-amr**  
Reproducible comparative genomic analysis of antimicrobial resistance determinants in municipal wastewater-derived *Escherichia coli*.
