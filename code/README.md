# Computational workflows

Scripts documenting the computational analyses of 132 wastewater-derived *Escherichia coli* assemblies.

- [`bash/`](bash/) contains original Ubuntu/WSL2 scripts, and a **reconstructed** Swedish genome retrieval workflow.
- [`python/`](python/) contains post hoc validation scripts, statistical analysis and plotting routines.

**Provenance matters:** original execution scripts and subsequently reconstructed audit scripts are not interchangeable. Some historical scripts refer to WSL2-specific paths or environments and must be reviewed before use. Running scripts may overwrite outputs or remove invalid temporary files. No single fully portable, end-to-end rebuild from initial NCBI downloads has been validated.

The original genome assemblies remain with NCBI. Statistical ARG co-occurrence, contig-level linkage, plasmid inference and horizontal transfer are separate levels of evidence.
