#!/usr/bin/env bash
# render_last_overlays.sh — Render only the last overlay page of each beamer frame as PNG.
# Parses the .nav file for frame boundaries, then calls pdftoppm for each last page.
# Usage: ./render_last_overlays.sh <nav_file> <pdf_file> <output_dir>
set -euo pipefail

NAV="${1:?Usage: $0 <nav_file> <pdf_file> <output_dir>}"
PDF="${2:?}"
OUTDIR="${3:?}"

mkdir -p "$OUTDIR"

# Extract last-overlay page for each frame from .nav file.
# Lines look like: \headcommand {\beamer@framepages {5}{8}}
# The second number is the last overlay page.
FRAME_NUM=0
grep 'beamer@framepages' "$NAV" | while IFS= read -r line; do
    FRAME_NUM=$((FRAME_NUM + 1))
    LAST_PAGE=$(echo "$line" | grep -oP '\{(\d+)\}\s*\}' | tail -1 | tr -dc '0-9')
    if [ -z "$LAST_PAGE" ]; then
        echo "WARN: Could not parse last page for frame $FRAME_NUM from: $line" >&2
        continue
    fi
    OUTFILE=$(printf "%s/frame_%02d_page_%03d" "$OUTDIR" "$FRAME_NUM" "$LAST_PAGE")
    pdftoppm -png -r 150 -f "$LAST_PAGE" -l "$LAST_PAGE" "$PDF" "$OUTFILE"
    # pdftoppm appends -N.png; rename to clean name
    ACTUAL=$(ls "${OUTFILE}"*.png 2>/dev/null | head -1)
    if [ -n "$ACTUAL" ]; then
        CLEAN=$(printf "%s/frame_%02d_page_%03d.png" "$OUTDIR" "$FRAME_NUM" "$LAST_PAGE")
        [ "$ACTUAL" != "$CLEAN" ] && mv "$ACTUAL" "$CLEAN"
    fi
done

TOTAL=$(ls "$OUTDIR"/frame_*.png 2>/dev/null | wc -l)
echo "Rendered $TOTAL last-overlay PNGs to $OUTDIR"
