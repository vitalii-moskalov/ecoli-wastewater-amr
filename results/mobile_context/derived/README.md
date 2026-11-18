# Derived mobile-context summaries

These are **post hoc integrated tables** produced during the 18 November 2026 audit. They are not original tool outputs.

- `carrier_mobile_context.csv` — assembly-level integration for 20 carriers.
- `mge_on_locus_contigs.csv` — five MGE feature predictions on the locus-containing contigs of two assemblies.
- `integrons_on_locus_contigs.csv` — a single predicted integron interval on a locus contig, overlapping the investigated locus by 26 bp; **not** evidence that the entire three-gene locus is integron-borne.

Source files: `../mob_reports/`, `../integron_reports/`, `../carriers_20_FROM_S4.tsv`, `../../clonality/mlst_all.tsv`, and `../../../figures/figure3_locus_sequence_hashes.csv`.

To regenerate from the repository root (may overwrite the three files):

```bash
python code/python/summarize_mobile_context.py
```

MOB-suite predictions, genomic colocalization and direct horizontal transfer evidence are distinct; assemblies may be incomplete.
