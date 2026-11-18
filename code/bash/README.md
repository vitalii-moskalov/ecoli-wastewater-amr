# Bash workflows (Ubuntu/WSL2)

The following scripts document historical computations unless explicitly marked as reconstructed.

| Script | Origin and purpose |
| --- | --- |
| `download_germany_resume.sh` | Original; retrieval of 92 selected German genome assemblies, with retries, logging and FASTA validation |
| `run_clonality.sh` | Original; MLST (mlst 2.35.0, Achtman) and ANI (skani 0.4.0) for 132 assemblies |
| `run_mobile_context.sh` | Original; MOB-suite 3.1.9 and IntegronFinder 2.0.6 processing of 20 locus-carrying assemblies |
| `retrieve_sweden_genomes_reconstructed.sh` | **Reconstructed on 18 November 2026** from Swedish selection metadata and command history; **not** the historical execution script |

German and Swedish AMRFinderPlus commands are supported by the original Ubuntu history and 132 stored output TSVs, but a single original annotation launcher for the complete study has not been recovered.

Do not execute historical scripts without first reviewing absolute paths, input lists, Conda environments, output destinations and destructive cleanup operations. Historical scripts are provenance materials, not a tested cross-platform installation workflow. The reconstructed Swedish retriever was syntax/dry-run checked; the complete download was not repeated.
