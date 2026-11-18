# Manuscript figures

These images correspond to the **current working manuscript** and remain subject to final scientific and editorial review. Both PNG and PDF formats are supplied; PDF format alone does not guarantee that every graphical element is vector-encoded.

| Figure | Files | Analytical origin |
| --- | --- | --- |
| 1 — Predicted functional/contextual categories | `Figure1_functional_context_categories.{png,pdf}` | 8 non-exclusive categories × Germany influent, Germany effluent and Swedish wastewater; Wilson 95% intervals |
| 2 — Replicated ARG associations | `Figure2_replicated_associations.{png,pdf}` | 9 display pairs from 13 FDR-significant in both collections, among 253 tested pairs |
| 3 — Three-gene locus architecture | `Figure3_locus_architecture.{png,pdf}` | Conserved `sul2`–`aph(3'')-Ib`–`aph(6)-Id` locus (2,513 bp) in 20 assemblies, six recorded sequence variants |

Source tables for Figure 3: `figure3_locus_sequence_hashes.csv` and `figure3_reference_gene_coordinates.csv`. Figure 1 relies on `../data/derived/mechanism_dictionary_60_symbols.csv`, the corrected presence matrix and `../results/statistics/` tables. Figure 2 relies on the complete 253-test results and the nine-pair display table.

Run checks from the repository root:

```bash
python code/python/figure1.py --check-only
python code/python/figure2.py --check-only
python code/python/figure3.py --check-only
```

Remove `--check-only` to render figures (Matplotlib required). The scripts independently reproduce scientific content, but **pixel-identical styling with every archived manuscript image is not guaranteed**. Numerical disagreement after regeneration requires investigation, not acceptance as normal variation.

Figure 1 categories are curated genotype-based predictions, including 19 conditional annotation assignments, and are not direct resistance phenotype tests. Figure 2 co-occurrence is not physical linkage; Figure 3 architecture and plasmid predictions do not prove horizontal transfer.
