# Computational workflows

This directory contains scripts documenting the computational procedures used in the comparative genomic analysis of wastewater-derived *Escherichia coli*.

## Organization

- `bash/` — scripts for genome retrieval, MLST, ANI, and mobile genetic element analysis.
- `python/` — scripts for antimicrobial resistance annotation processing, statistical analysis, and figure generation.

## Reproducibility

Original computational scripts are preserved where available. Software versions, reference database versions, input file identifiers, and execution parameters are documented separately.

Some Bash scripts contain paths specific to the original Ubuntu/WSL2 environment and may require configuration before execution on another system.

The statistical analysis workflows are being independently audited against the original AMRFinderPlus outputs and derived data matrices.

## Interpretation

Statistical associations between resistance determinants do not establish their physical co-localization.

Contig-level localization and computational plasmid predictions are distinguished from experimentally demonstrated horizontal gene transfer.

## Status

Computational documentation is under final verification. Scripts should not be interpreted as fully validated end-to-end reproduction workflows until the audit is completed.
