#!/usr/bin/env bash
set -Eeuo pipefail
ROOT="$HOME/ecoli_mobile_context"
GER="$HOME/ecoli_germany_amr/input/germany_fasta"
SWE="$HOME/ecoli_sweden_amr"
mkdir -p "$ROOT"/{results,logs,tmp}
cd "$ROOT"
for program in mob_recon python3; do
  command -v "$program" >/dev/null || { echo "Missing: $program"; exit 1; }
done
[[ -s "$ROOT/carriers_20.tsv" ]] || { echo "Missing carriers_20.tsv in $ROOT"; exit 1; }
{
  date -Is
  mob_recon --help | head -n 3 || true
  conda run -n ecoli_integron --no-capture-output integron_finder --version || true
} > logs/software_versions.txt 2>&1
while IFS=$'\t' read -r acc country; do
  [[ "$acc" == accession || -z "$acc" ]] && continue
  if [[ "$country" == Germany ]]; then
    fasta="$GER/$acc.fna"
  elif [[ "$country" == Sweden ]]; then
    fasta=$(find "$SWE/input/sweden_all/ncbi_dataset/data/$acc" -maxdepth 1 -name '*.fna' -print -quit)
  else
    echo "Invalid country $country"; exit 1
  fi
  [[ -s "$fasta" ]] || { echo "MISSING FASTA: $acc"; exit 1; }
  echo "PROCESSING $acc"
  # MOB-suite: run each assembly separately; atomic success marker.
  if [[ ! -f "$ROOT/results/$acc/mob.ok" ]]; then
    mkdir -p "$ROOT/results/$acc"
    if mob_recon --infile "$fasta" --outdir "$ROOT/results/$acc/mob" --num_threads 2 \
         > "$ROOT/logs/${acc}_mob.log" 2>&1; then
      touch "$ROOT/results/$acc/mob.ok"
    else
      echo "MOB-RECON FAILED $acc (see logs)"
    fi
  fi
  # IntegronFinder: output directory per accession, so restarts skip finished samples.
  if [[ ! -f "$ROOT/results/$acc/integron.ok" ]]; then
    mkdir -p "$ROOT/results/$acc/integron"
    if conda run -n ecoli_integron --no-capture-output integron_finder "$fasta" --cpu 2 --outdir "$ROOT/results/$acc/integron" \
         > "$ROOT/logs/${acc}_integron.log" 2>&1; then
      touch "$ROOT/results/$acc/integron.ok"
    else
      echo "INTEGRONFINDER FAILED $acc (see logs)"
    fi
  fi
done < "$ROOT/carriers_20.tsv"
echo 'DONE. MOB successes:'
find results -name mob.ok | wc -l
echo 'Integron successes:'
find results -name integron.ok | wc -l
