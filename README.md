# Antimicrobial resistance determinants in wastewater-derived *Escherichia coli*

Supporting datasets, computational scripts, validation routines and figures for the study:

**Molecular diversity and co-occurrence of antimicrobial resistance determinants in wastewater-derived Escherichia coli: a comparative genomic analysis**

Authors: V. B. Moskalov and Y. D. Batuieva.

## Scope and design

The analysis includes **132 publicly available genome assemblies**: 50 from German municipal wastewater influent and 42 from effluent (BioProject **PRJNA380388**) and 40 selected Swedish wastewater assemblies (BioProject **PRJNA1266621**). The collections originate from different studies and sampling/selection procedures; between-collection comparisons are descriptive, **not** estimates of national AMR prevalence.

The analyses cover AMRFinderPlus annotations, curated presence–absence matrices, ARG co-occurrence, MLST/ANI, and a targeted genomic-context investigation of a conserved `sul2`–`aph(3'')-Ib`–`aph(6)-Id` locus in 20 assemblies.

## Repository contents

| Directory | Contents |
| --- | --- |
| [`data/`](data/) | Genome manifest, original AMRFinderPlus outputs and curated matrices |
| [`code/`](code/) | Historical Bash workflows, reconstructed retrieval script, Python analyses and validation |
| [`results/`](results/) | Statistics, MLST/ANI, and original/derived mobile-context reports |
| [`figures/`](figures/) | Three manuscript figures, numeric plotting sources and formats |
| [`supplementary/`](supplementary/) | Audited Supplementary Tables S1–S5 and provenance notes; manuscript text remains under editorial revision |

## Principal software and reference data

- AMRFinderPlus **4.2.7**, database **2026-10-29.1**, `--organism Escherichia --plus`.
- `mlst` **2.35.0** (Achtman scheme); `skani` **0.4.0**.
- MOB-suite **3.1.9** and IntegronFinder **2.0.6** (original computational outputs for 20 assemblies).
- Original genome assemblies are referenced by NCBI accession; the FASTA collections are **not redistributed** here.

## Key analytical distinctions

- The corrected conservative annotation dataset retains **407 AMRFinderPlus records**, **60 unique determinant symbols**, and documents **18 excluded records**, including an `INTERNAL_STOP` hit.
- The gene-only analysis considered **253 pairs** among 23 eligible gene symbols. **13** pairs pass FDR < 0.05 in both collections; **nine** are displayed in Figure 2 after an additional minimum of three co-detections in each collection.
- Statistical co-occurrence is not evidence of physical linkage. Same-contig localization is distinct from plasmid prediction, and neither alone demonstrates horizontal gene transfer.
- The annotation-based category dictionary has been curated and reviewed (41 `high`, 19 `conditional` assignments); these categories are not experimentally measured resistance phenotypes.

## Basic reproducibility checks

Clone or download the repository and run the following commands **from its root** using Python 3. Audit dependencies are listed in [`requirements-audit.txt`](requirements-audit.txt) (tested with Python 3.13.5; these are post hoc audit versions, not the original Ubuntu/WSL2 software environment):

```bash
python code/python/verify_amr_data.py
python code/python/recalculate_gene_cooccurrence.py --help
python code/python/recalculate_burden_statistics.py --help
python code/python/verify_clonality_results.py
python code/python/verify_mobile_context_reports.py
python code/python/figure1.py --check-only
python code/python/figure2.py --check-only
python code/python/figure3.py --check-only
```

Some figure-generation commands additionally require Matplotlib. **Caution:** certain data-generation scripts write into `results/` when run without an alternate output directory. Use a disposable clone or configure an output directory before regenerating tables. The repository is a documented collection of archived procedures and independently verified components, **not** a validated one-command end-to-end pipeline from raw NCBI assemblies.

## Scientific and publication status

The S1–S5 tables and S5 category dictionary have been numerically audited and scientifically curated, with 19 context-dependent (`conditional`) entries retained. Corrected bootstrap burden results and their reconstructed reproduction script are available in `results/statistics/` and `code/python/`, respectively. The manuscript remains under editorial revision; its Table 1, Results and Abstract must be brought into agreement with the corrected `INTERNAL_STOP` filtering before submission. Read [`supplementary/AUDIT_AND_PROVENANCE.md`](supplementary/AUDIT_AND_PROVENANCE.md) for known limitations.

## Licensing and attribution

Software authored for this repository is offered under the [MIT License](LICENSE). Original author-created tables, figure artwork and repository documentation are offered under [CC BY 4.0](LICENSE-DATA.md) **to the extent the contributors hold the rights**. NCBI source data, accession-associated metadata and unmodified third-party tool outputs are excluded from any blanket relicensing; their original terms and citations remain applicable. See [LICENSING.md](LICENSING.md).

Please cite the associated manuscript when bibliographic details are available, and identify the repository URL and commit or release used for analyses.
