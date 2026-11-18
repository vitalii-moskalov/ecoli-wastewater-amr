#!/usr/bin/env bash
set -uo pipefail

ROOT="$HOME/ecoli_germany_amr"
LIST="$ROOT/input/germany_92_accessions.txt"
OUT="$ROOT/input/germany_fasta"
LOG="$ROOT/logs/download_germany.log"
FAILED="$ROOT/logs/failed_downloads.txt"
TMP="$ROOT/input/download_tmp"

mkdir -p "$OUT" "$ROOT/logs" "$TMP"

if [[ ! -f "$LIST" ]]; then
    echo "ERROR: Accession list not found"
    exit 1
fi

if ! command -v datasets >/dev/null 2>&1; then
    echo "ERROR: NCBI datasets is not installed"
    exit 1
fi

if ! command -v unzip >/dev/null 2>&1; then
    echo "ERROR: unzip is not installed"
    exit 1
fi

log() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') $*" \
        | tee -a "$LOG"
}

# Basic FASTA integrity check
valid_fasta() {
    local file="$1"

    [[ -s "$file" ]] || return 1

    awk '
        BEGIN {headers=0; seq=0; bad=0}
        /^>/ {
            if (length($0) < 2) bad=1
            headers++
            next
        }
        /^[[:space:]]*$/ {next}
        {
            if (headers == 0 || $0 ~ /[^A-Za-z]/) bad=1
            seq++
        }
        END {
            if (headers > 0 && seq > 0 && bad == 0)
                exit 0
            exit 1
        }
    ' "$file"
}

# Stop safely with Ctrl+C
trap 'log "INTERRUPTED by user"; exit 130' INT
trap 'log "TERMINATED"; exit 143' TERM

log "=== START / RESUME ==="

TOTAL=0
SKIPPED=0
DOWNLOADED=0
FAILED_COUNT=0

: > "$FAILED"

while IFS= read -r ACC || [[ -n "$ACC" ]]; do

    ACC="${ACC//$'\r'/}"
    [[ -z "$ACC" ]] && continue

    ((TOTAL+=1))

    FINAL="$OUT/${ACC}.fna"
    WORK="$TMP/$ACC"
    ZIP="$WORK/download.zip"
    TEMP_FASTA="$WORK/${ACC}.fna"

    # Existing valid genomes are never re-downloaded
    if valid_fasta "$FINAL"; then
        ((SKIPPED+=1))
        log "[$TOTAL] SKIP $ACC - valid FASTA exists"
        continue
    fi

    # Remove invalid final file, if present
    if [[ -e "$FINAL" ]]; then
        log "[$TOTAL] INVALID existing FASTA: $ACC"
        rm -f "$FINAL"
    fi

    SUCCESS=0

    for ATTEMPT in 1 2 3; do

        log "[$TOTAL] DOWNLOAD $ACC attempt $ATTEMPT/3"

        rm -rf "$WORK"
        mkdir -p "$WORK"

        if ! datasets download genome accession "$ACC" \
            --include genome \
            --filename "$ZIP" \
            --no-progressbar \
            >> "$LOG" 2>&1; then

            log "Download error: $ACC"
            sleep 5
            continue
        fi

        # Validate archive CRC and ZIP structure
        if ! unzip -tqq "$ZIP" >/dev/null 2>&1; then
            log "Invalid ZIP: $ACC"
            sleep 5
            continue
        fi

        # Locate genomic FASTA inside the NCBI package
        FASTA_ENTRY=$(
            unzip -Z1 "$ZIP" 2>/dev/null \
            | grep -E '\.fna$' \
            | head -n 1
        )

        if [[ -z "$FASTA_ENTRY" ]]; then
            log "No FASTA in ZIP: $ACC"
            sleep 5
            continue
        fi

        # Extract into temporary file
        if ! unzip -p "$ZIP" "$FASTA_ENTRY" \
            > "$TEMP_FASTA"; then
            log "Extraction error: $ACC"
            sleep 5
            continue
        fi

        if ! valid_fasta "$TEMP_FASTA"; then
            log "Invalid FASTA: $ACC"
            sleep 5
            continue
        fi

        # Atomic commit of successfully checked genome
        mv "$TEMP_FASTA" "$FINAL"

        ((DOWNLOADED+=1))
        SUCCESS=1

        log "[$TOTAL] OK $ACC"

        rm -rf "$WORK"
        break

    done

    if [[ "$SUCCESS" -eq 0 ]]; then
        ((FAILED_COUNT+=1))
        echo "$ACC" >> "$FAILED"
        log "[$TOTAL] FAILED $ACC after 3 attempts"
    fi

done < "$LIST"

log "=== FINISHED ==="
log "Processed accessions: $TOTAL"
log "Previously valid: $SKIPPED"
log "Newly downloaded: $DOWNLOADED"
log "Failed: $FAILED_COUNT"

echo
echo "Valid genome FASTA files:"
find "$OUT" -maxdepth 1 -type f -name "*.fna" | wc -l

echo "Failed accessions:"
cat "$FAILED"
