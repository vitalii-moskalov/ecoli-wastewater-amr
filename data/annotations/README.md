# Original AMRFinderPlus annotations

This directory contains the original per-assembly AMRFinderPlus TSV outputs used in the comparative analysis of 132 wastewater-derived *Escherichia coli* genomes.

## Directory structure

- `Germany/` — 92 annotation files corresponding to PRJNA380388.
- `Sweden/` — 40 annotation files corresponding to PRJNA1266621.

Each TSV file corresponds to one genome assembly identified by its NCBI accession number.

## Annotation software

- AMRFinderPlus version: 4.2.7
- Database version: 2026-10-29.1
- Organism parameter: `Escherichia`
- Extended annotations: `--plus`

The same software and database versions were used for both collections.

## Data processing

These files contain the annotation outputs before the analytical filtering applied in this study.

Filtered core AMR records, excluded annotations, and binary presence–absence matrices are provided separately in `../derived/`.

Original annotations and derived matrices should not be treated as interchangeable.

## Reproducibility

Genome accession numbers and collection assignments are provided in `../sample_manifest.csv`.

The original genome assemblies remain available through their corresponding NCBI BioProjects.

File integrity can be checked against the SHA-256 checksum manifest supplied with the repository.
