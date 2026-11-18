# Bash workflows

This directory contains original and reconstructed Bash scripts documenting computational procedures associated with the comparative genomic analysis of 132 wastewater-derived *Escherichia coli* assemblies.

The original analyses were performed in Ubuntu under Windows Subsystem for Linux (WSL2).

## Original computational scripts

### download_germany_resume.sh

Downloads the 92 selected German genome assemblies from NCBI using a predefined accession list.

The script includes basic FASTA integrity checks, retry logic, execution logging, and support for resuming interrupted downloads.

### run_clonality.sh

Performs multilocus sequence typing (MLST) and average nucleotide identity (ANI) analysis for 132 genome assemblies.

Software:
- mlst 2.35.0 (*E. coli* Achtman scheme)
- skani 0.4.0

The script validates the number of input assemblies, generates MLST results, and produces ANI and aligned-fraction matrices using `skani triangle`.

### run_mobile_context.sh

Performs genomic-context analysis of 20 assemblies carrying the investigated sul2–aph(3'')-Ib–aph(6)-Id gene combination.

Software:
- MOB-suite 3.1.9
- IntegronFinder 2.0.6

The archived script includes the corrected execution of IntegronFinder through its dedicated Conda environment.

Both computational analyses have 20 recorded successful completions. The outputs represent computational predictions rather than experimental confirmation of plasmid structure or horizontal gene transfer.

## Reconstructed genome retrieval workflow

### retrieve_sweden_genomes_reconstructed.sh

This script was reconstructed on 18 November 2026 using the original Swedish genome selection metadata, NCBI accession records, and available Ubuntu command history.

It provides a reproducible procedure for retrieving the 40 selected Swedish genome assemblies from NCBI.

**This is not an original historical execution script and was not used to generate the annotation results reported in the manuscript.**

The reconstructed script has undergone Bash syntax validation and dry-run testing. A complete repeated download has not been performed.

The original Swedish genome selection is documented in `selected_genomes.tsv`.

## AMRFinderPlus annotation

The original AMRFinderPlus annotation commands were recovered from Ubuntu command history.

Software:
- AMRFinderPlus 4.2.7
- Database version 2026-10-29.1
- Organism parameter: `Escherichia`
- Extended annotation option: `--plus`

Original per-assembly annotation outputs are preserved under `../../data/annotations/`.

The original standalone annotation execution scripts have not yet been recovered.

## Reproducibility considerations

Original scripts are preserved as computational provenance materials and may contain paths specific to the original Ubuntu/WSL2 environment.

Before execution, users should review and adapt input paths, software environments, and output directories.

Some scripts may create, overwrite, or remove temporary files or invalid intermediate outputs.

The original genome assemblies are publicly available through NCBI and are not duplicated in this repository.

The repository distinguishes between:
- Original computational scripts and outputs.
- Reconstructed procedures developed for reproducibility.
- Derived analytical datasets and statistical results.

Complete portability and end-to-end reproducibility have not yet been established. Scientific and methodological verification is ongoing.
