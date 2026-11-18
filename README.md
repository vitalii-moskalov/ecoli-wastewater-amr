# Antimicrobial resistance determinants in wastewater-derived *Escherichia coli*

## Overview

This repository contains data, computational workflows, and supporting materials for the study:

**Molecular diversity and co-occurrence of antimicrobial resistance determinants in wastewater-derived Escherichia coli: a comparative genomic analysis**

**Authors:** V. B. Moskalov and Y. D. Batuieva

The study investigates the molecular diversity, functional distribution, co-occurrence, and genomic organization of antimicrobial resistance determinants in *Escherichia coli* isolated from municipal wastewater.

The analysis focuses on resistance-associated genomic variation within urban wastewater systems, recurrent antimicrobial resistance gene combinations, bacterial population structure, and predicted associations with mobile genetic elements.

## Datasets

The study includes 132 publicly available *E. coli* genome assemblies from two independently generated collections:

| Collection | Number of genomes | NCBI BioProject |
|---|---:|---|
| Germany — WWTP influent | 50 | PRJNA380388 |
| Germany — WWTP effluent | 42 | PRJNA380388 |
| Sweden — wastewater | 40 | PRJNA1266621 |
| **Total** | **132** | |

The original studies used different sampling and isolate-selection procedures. Consequently, comparisons between the German and Swedish collections are descriptive and should not be interpreted as representative estimates of geographical differences in antimicrobial resistance prevalence.

## Computational methods

The analytical workflow includes:

1. Genome accession verification and metadata harmonization.
2. Antimicrobial resistance determinant annotation using NCBI AMRFinderPlus.
3. Construction of resistance determinant presence–absence matrices.
4. Functional classification and statistical analysis of resistance profiles.
5. Pairwise gene co-occurrence analysis with false discovery rate correction.
6. Examination of conserved resistance-associated nucleotide sequences.
7. Multilocus sequence typing and average nucleotide identity analysis.
8. Prediction of plasmid-associated genomic context and integron structures.

The study integrates genomic annotations, statistical associations, nucleotide-level organization, and bacterial relatedness. Statistical gene co-occurrence is distinguished from physical gene linkage, and predicted plasmid association is not treated as direct evidence of horizontal gene transfer.

## Software

Major tools used in the study include:

| Tool | Version |
|---|---|
| AMRFinderPlus | 4.2.7 |
| AMRFinderPlus database | 2026-10-29.1 |
| mlst | 2.35.0 |
| skani | 0.4.0 |
| MOB-suite | 3.1.9 |
| IntegronFinder | 2.0.6 |
| Python | See workflow-specific environment information |

## Repository contents

The repository is being organized into directories containing input metadata, annotation outputs, analysis scripts, verified results, figures, supplementary materials, and computational provenance.

Original genome assemblies are available from NCBI and are not intended to be duplicated in this repository.

## Reproducibility status

**Repository under preparation and final scientific audit.**

Computational outputs, analytical scripts, filtering rules, and figure source data are being consolidated and checked against the original results. Additional documentation will be provided as the audit is completed.

## Citation

The associated manuscript is in preparation. Publication details and the recommended citation will be added when available.
