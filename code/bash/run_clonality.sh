#!/usr/bin/env bash
set -Eeuo pipefail

ROOT="$HOME/ecoli_clonality"
GER="$HOME/ecoli_germany_amr/input/germany_fasta"
SWE="$HOME/ecoli_sweden_amr"

mkdir -p "$ROOT"/{results,logs}
cd "$ROOT"

LIST="$ROOT/genomes_132.txt"
MANIFEST="$ROOT/genome_manifest.tsv"

# Build a fresh, validated input manifest
: > "$LIST"
printf 'accession\tcollection\tfasta\n' > "$MANIFEST"

for fasta in "$GER"/*.fna; do
    [[ -f "$fasta" ]] || continue
    acc=$(basename "$fasta" .fna)
    path=$(realpath "$fasta")
    printf '%s\n' "$path" >> "$LIST"
    printf '%s\tGermany\t%s\n' "$acc" "$path" >> "$MANIFEST"
done

while IFS= read -r fasta || [[ -n "$fasta" ]]; do
    [[ -n "$fasta" ]] || continue

    if [[ "$fasta" = /* ]]; then
        path="$fasta"
    else
        path="$SWE/$fasta"
    fi

    [[ -s "$path" ]] || {
        echo "Missing Swedish FASTA: $path" >&2
        exit 1
    }

    path=$(realpath "$path")
    acc=$(basename "$(dirname "$path")")

    printf '%s\n' "$path" >> "$LIST"
    printf '%s\tSweden\t%s\n' "$acc" "$path" >> "$MANIFEST"
done < "$SWE/genome_files.txt"

n=$(wc -l < "$LIST")
unique=$(cut -f1 "$MANIFEST" | tail -n +2 | sort -u | wc -l)

echo "Genome files: $n"
echo "Unique accessions: $unique"

if [[ "$n" -ne 132 || "$unique" -ne 132 ]]; then
    echo "ERROR: Expected 132 unique genomes."
    exit 1
fi

if ! mlst --list | grep -qw 'ecoli_achtman_4'; then
    echo "ERROR: ecoli_achtman_4 scheme unavailable."
    exit 1
fi

skani --version > logs/skani_version.txt 2>&1
mlst --version > logs/mlst_version.txt 2>&1

echo "=== MLST analysis ==="

mkdir -p results/mlst_individual

while IFS=$'\t' read -r acc collection fasta; do
    [[ "$acc" = accession ]] && continue

    output="results/mlst_individual/${acc}.tsv"
    tmp="${output}.tmp"

    if [[ -s "$output" ]]; then
        echo "SKIP MLST: $acc"
        continue
    fi

    echo "MLST: $acc"

    if mlst --scheme ecoli_achtman_4 --full \
        --nopath "$fasta" \
        > "$tmp" 2> "logs/mlst_${acc}.log"; then

        if [[ $(wc -l < "$tmp") -eq 2 ]]; then
            tail -n 1 "$tmp" > "$output"
        else
            echo "INVALID MLST output: $acc"
        fi
    else
        echo "FAILED MLST: $acc"
    fi

    rm -f "$tmp"
done < "$MANIFEST"

printf 'FILE\tSCHEME\tST\tSTATUS\tSCORE\tALLELES\n' \
    > results/mlst_all.tsv

while IFS=$'\t' read -r acc collection fasta; do
    [[ "$acc" = accession ]] && continue
    file="results/mlst_individual/${acc}.tsv"
    if [[ -s "$file" ]]; then
        cat "$file" >> results/mlst_all.tsv
    fi
done < "$MANIFEST"

echo "MLST records:"
echo $(( $(wc -l < results/mlst_all.tsv) - 1 ))

echo "=== skani ANI analysis ==="

if [[ -s results/skani_ani.tsv ]] && \
   [[ -s results/skani_ani.tsv.af ]]; then
    echo "ANI matrix already available; skipping."
else
    rm -f results/skani_ani.tsv.tmp \
          results/skani_ani.tsv.tmp.af

    if skani triangle \
        -l "$LIST" \
        -t 2 \
        -o results/skani_ani.tsv.tmp \
        > logs/skani_stdout.log \
        2> logs/skani_stderr.log; then

        if [[ -s results/skani_ani.tsv.tmp ]] && \
           [[ -s results/skani_ani.tsv.tmp.af ]]; then
            mv results/skani_ani.tsv.tmp \
               results/skani_ani.tsv
            mv results/skani_ani.tsv.tmp.af \
               results/skani_ani.tsv.af
            echo "ANI matrix completed."
        else
            echo "ERROR: Incomplete skani output."
            exit 1
        fi
    else
        echo "ERROR: skani failed. Check logs."
        exit 1
    fi
fi

echo "=== SUMMARY ==="
echo "Genome count: $(wc -l < "$LIST")"
echo "MLST records: $(( $(wc -l < results/mlst_all.tsv) - 1 ))"
echo "ANI matrix: results/skani_ani.tsv"
echo "Aligned fraction: results/skani_ani.tsv.af"
echo "Analysis finished."
