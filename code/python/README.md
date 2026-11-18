# Python analysis and validation

Python scripts used to independently check or reproduce selected analytical steps. Unless stated otherwise, these programs were developed or reconstructed for the November 2026 audit; they **must not** be presented as the original historical implementations.

| File | Purpose |
| --- | --- |
| `verify_amr_data.py` | Check original TSV integrity, filtering and binary presence matrices (407 retained records, 60 symbols) |
| `recalculate_gene_cooccurrence.py` | Recalculate 253 one-sided Fisher tests per collection and BH-adjusted p-values; generate association tables |
| `figure1.py` | Audit and render eight functional/contextual category prevalences and Wilson intervals |
| `figure2.py` | Audit and render nine selected ARG co-occurrence pairs |
| `figure3.py` | Audit and render the conserved resistance-locus architecture |
| `verify_clonality_results.py` | Validate 132 MLST results and 8,646 unique ANI/AF pairs |
| `verify_mobile_context_reports.py` | Verify file counts, sizes and SHA-256 for 140 context reports |
| `summarize_mobile_context.py` | Construct derived per-carrier summaries from archived MOB-suite/IntegronFinder, locus and MLST inputs |

Run from a local repository root, for example:

```bash
python code/python/verify_amr_data.py
python code/python/verify_clonality_results.py
python code/python/verify_mobile_context_reports.py
python code/python/figure1.py --check-only
python code/python/figure2.py --check-only
python code/python/figure3.py --check-only
```

The plotting scripts use Matplotlib to produce figures. **The non-plotting validation scripts largely use the Python standard library.** Regeneration scripts can write or overwrite files in `results/`; use a clean working copy or specify a separate output directory where supported. Execution parameters and required input paths are described in each script.

Scientific limits: curated AMR-category assignments are partly provisional; statistical co-occurrence does not demonstrate physical linkage or horizontal gene transfer.
