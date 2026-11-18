# Analysis results

This directory separates **statistical summaries**, **bacterial genetic relatedness**, and **genomic-context predictions** for 132 public wastewater-derived *Escherichia coli* assemblies.

| Directory | Data and provenance |
| --- | --- |
| [`statistics/`](statistics/) | 253 ARG pairwise comparisons, 13 replicated FDR-significant pairs, the nine displayed Figure 2 pairs, and eight mechanism-category comparisons |
| [`clonality/`](clonality/) | Original MLST and `skani` ANI/AF outputs, plus a derived table of 8,646 unique pairs |
| [`mobile_context/`](mobile_context/) | MOB-suite and IntegronFinder reports for 20 carriers of the investigated three-gene locus, checksum manifest, and post hoc summaries |

## Verification

```bash
# Run from the repository root:
python code/python/verify_clonality_results.py
python code/python/verify_mobile_context_reports.py
python code/python/figure1.py --check-only
python code/python/figure2.py --check-only
```

Other analysis scripts, including `recalculate_gene_cooccurrence.py` and `summarize_mobile_context.py`, can write derived outputs; consult their options before running them on the checked-in files.

## Interpretation

- These are **genome-based predictions and statistical summaries**, not experimentally determined antibiotic susceptibility profiles.
- The 132 assemblies derive from studies with different sampling designs; percentages must not be presented as nationally representative comparisons.
- Gene co-occurrence, contig-local colocalization, computational plasmid classification and horizontal transfer represent **different evidence levels**.
- Integrons detected elsewhere in an assembly must not be assigned to a resistance-locus contig without sequence/coordinate evidence.

The original archives and derived tabulations were checked locally during the November 2026 audit. Where documented, checks on the local files should be independently repeated after cloning the public GitHub repository; no uninterrupted end-to-end raw-assembly pipeline has been certified.
