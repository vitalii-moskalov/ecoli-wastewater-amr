# Python analysis workflows

This directory is intended to document the Python-based computational analyses performed for the wastewater-derived *Escherichia coli* study.

## Analytical components

The analysis includes:

1. Processing and conservative filtering of AMRFinderPlus annotations.
2. Construction of core AMR and non-POINT gene presence–absence matrices.
3. Descriptive statistics and functional classification of resistance determinants.
4. Statistical analysis of resistance-gene co-occurrence with multiple-testing correction.
5. Analysis of conserved resistance-associated nucleotide sequences and their genomic context.
6. Integration of MLST and ANI results.
7. Generation of manuscript tables and figures.

## Script provenance

Historical analysis scripts and independently developed verification scripts will be identified separately.

Some existing Python scripts depend on absolute file paths and intermediate datasets from the original analytical environment.

Scripts will be added following verification of their inputs, outputs, computational assumptions, and consistency with the manuscript.

## Scientific validation

Statistical associations are distinguished from physical gene co-localization and inferred genetic mobility.

Genome relatedness and differences in sampling strategies are considered when interpreting associations and between-collection comparisons.

## Current status

The Python workflows are undergoing final scientific and reproducibility auditing.

The presence of an archived script does not imply that it has been validated as part of a portable end-to-end pipeline.
