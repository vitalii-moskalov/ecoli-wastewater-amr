# Study data

Input metadata and original/derived annotation records for 132 public *Escherichia coli* assemblies from municipal wastewater.

| Collection | Assemblies | NCBI BioProject |
| --- | ---: | --- |
| Germany, influent | 50 | PRJNA380388 |
| Germany, effluent | 42 | PRJNA380388 |
| Sweden, selected wastewater | 40 | PRJNA1266621 |

- `sample_manifest.csv`: assembly IDs and collection assignments.
- [`annotations/`](annotations/): the **132 unmodified AMRFinderPlus TSV outputs**, separated by country, plus integrity hashes.
- [`derived/`](derived/): filtered hits, exclusion log, binary matrices and provisional functional classification.
- `selected_genomes.tsv` (where supplied): Swedish selection metadata; selection should not be construed as random geographical sampling.

NCBI genome FASTA files are not replicated in the repository. The two collections used different sampling and isolate-selection protocols; comparisons are observational/descriptive rather than estimates of national resistance prevalence.
