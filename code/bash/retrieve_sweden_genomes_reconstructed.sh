#!/usr/bin/env bash
# Reconstructed on 2026-11-18 from original selected_genomes.tsv,
# genome_files.txt, NCBI dataset metadata, and the documented command history.
# NOT an original historical execution script.
set -Eeuo pipefail

usage() {
  cat <<'HELP'
Usage: retrieve_sweden_genomes_reconstructed.sh SELECTED_GENOMES_TSV OUTPUT_DIR [--dry-run]

Requires: NCBI datasets CLI, unzip, awk.
Downloads the 40 specified GCA assembly versions, one at a time, to OUTPUT_DIR.
This reconstruction is for future reproducibility; it was not used to generate
original manuscript annotations. Existing nonempty FASTA files are preserved.
HELP
}
if [[ "${1:-}" == '--help' || $# -lt 2 || $# -gt 3 ]]; then
  usage
  [[ "${1:-}" == '--help' ]] && exit 0 || exit 2
fi
manifest=$1
outdir=$2
dry_run=0
if [[ $# -eq 3 ]]; then
  [[ $3 == '--dry-run' ]] || { usage >&2; exit 2; }
  dry_run=1
fi
[[ -s $manifest ]] || { echo "Missing manifest: $manifest" >&2; exit 1; }

# Validate selection independently of any local FASTA paths in the manifest.
declare -a accessions=()
declare -A seen=()
IFS= read -r header < "$manifest"
[[ $header == $'accession\tbiosample\tstrain\tsource\tcollection_date\tfasta' || \
   $header == $'accession\tbiosample\tstrain\tsource\tcollection_date\tfasta\r' ]] || {
  echo "Unexpected TSV header" >&2; exit 1;
}
while IFS=$'\t' read -r acc biosample strain source date fasta || [[ -n ${acc:-} ]]; do
  acc=${acc%$'\r'}; fasta=${fasta%$'\r'}
  [[ -n $acc ]] || continue
  [[ $acc =~ ^GCA_[0-9]+\.[0-9]+$ ]] || { echo "Invalid assembly accession: $acc" >&2; exit 1; }
  [[ $source == 'wastewater' ]] || { echo "Unexpected isolation source for $acc: $source" >&2; exit 1; }
  [[ $fasta == *"/$acc/"* ]] || { echo "Path/accession mismatch: $acc" >&2; exit 1; }
  [[ -z ${seen[$acc]+x} ]] || { echo "Duplicate accession: $acc" >&2; exit 1; }
  seen[$acc]=1
  accessions+=("$acc")
done < <(tail -n +2 "$manifest")
[[ ${#accessions[@]} -eq 40 ]] || { echo "Expected 40 accessions; got ${#accessions[@]}" >&2; exit 1; }
echo "Validated 40 unique wastewater assembly accessions."

if [[ $dry_run -eq 1 ]]; then
  for acc in "${accessions[@]}"; do
    printf 'DRY RUN: %s -> %s/%s.fna\n' "$acc" "$outdir" "$acc"
  done
  exit 0
fi
for command in datasets unzip awk; do
  command -v "$command" >/dev/null 2>&1 || { echo "Missing program: $command" >&2; exit 1; }
done
mkdir -p "$outdir"
for acc in "${accessions[@]}"; do
  final="$outdir/$acc.fna"
  if [[ -s $final ]]; then
    echo "SKIP (existing nonempty FASTA; verify independently): $acc"
    continue
  fi
  if [[ -e $final ]]; then
    echo "Refusing to overwrite invalid/empty existing file: $final" >&2
    exit 1
  fi
  success=0
  for attempt in 1 2 3; do
    work=$(mktemp -d "$outdir/.${acc}.XXXXXX")
    zip="$work/${acc}.zip"
    if datasets download genome accession "$acc" --include genome --filename "$zip" --no-progressbar \
        && unzip -tqq "$zip"; then
      entry=$(unzip -Z1 "$zip" | awk -v acc="$acc" '
        index($0, "ncbi_dataset/data/" acc "/") && /\.fna$/ {print; exit}
      ')
      if [[ -n $entry ]]; then
        temp="$work/$acc.fna"
        if unzip -p "$zip" "$entry" > "$temp" && \
           awk '/^>/ {h++} !/^>/ && /[ACGTNacgtn]/ {s++} END {exit !(h>0 && s>0)}' "$temp"; then
          mv "$temp" "$final"
          success=1
        fi
      fi
    fi
    rm -rf -- "$work"
    [[ $success -eq 1 ]] && break
    echo "RETRY $acc ($attempt/3)" >&2
  done
  [[ $success -eq 1 ]] || { echo "FAILED $acc" >&2; exit 1; }
  echo "OK $acc"
done
