# MLST and ANI results

This directory documents population relatedness for 132 *Escherichia coli* genome assemblies.

- `mlst_all.tsv`: original `mlst` 2.35.0 typing (Achtman scheme), 132 assemblies.
- `skani_ani.tsv`: original triangular average nucleotide identity matrix from skani 0.4.0.
- `skani_ani.tsv.af`: aligned fraction matrix.
- `pairwise_ani_af.csv`: derived table of **8,646 unique** assembly pairs.

Two genomes have `NOVEL` MLST results with **different seven-allele profiles**. Do not merge them into a single sequence type when assessing clonality.

The historical execution launcher is `../../code/bash/run_clonality.sh`; independent checks are in `../../code/python/verify_clonality_results.py`.

ANI and MLST indicate genetic similarity, not transmission or horizontal acquisition of a specific ARG locus.
