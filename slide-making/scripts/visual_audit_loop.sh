#!/usr/bin/env bash
# visual_audit_loop.sh — Visual audit convergence loop for beamer slides
#
# Compiles the deck, renders all pages as PNGs, runs structural gates
# (compile_check.sh), and prepares a manifest for visual inspection.
# Designed to be called iteratively until convergence (0 defects).
#
# Usage: ./visual_audit_loop.sh <tex_file> [--iteration N] [--output-dir DIR]
#
# The loop is:
#   1. Compile (2-pass pdflatex)
#   2. Render all pages as PNGs (pdftoppm)
#   3. Run compile_check.sh structural gates
#   4. Output manifest: page list + structural gate results
#   5. User/agent inspects PNGs, identifies visual defects
#   6. Fix defects in source
#   7. Repeat from step 1
#
# Exit codes:
#   0 = structural gates pass, PNGs ready for inspection
#   1 = compilation failed
#   2 = structural gate violation (fix before visual audit)
#   3 = missing dependency (pdftoppm, pdflatex)

set -euo pipefail

TEX_FILE="${1:?Usage: visual_audit_loop.sh <tex_file> [--iteration N] [--output-dir DIR]}"
ITERATION=1
OUTPUT_DIR=""

shift
while [ $# -gt 0 ]; do
    case "$1" in
        --iteration) ITERATION="$2"; shift 2 ;;
        --output-dir) OUTPUT_DIR="$2"; shift 2 ;;
        *) shift ;;
    esac
done

BASE="${TEX_FILE%.tex}"
DIR="$(dirname "$TEX_FILE")"
PDF="${BASE}.pdf"

# Default output dir
if [ -z "$OUTPUT_DIR" ]; then
    OUTPUT_DIR="${DIR}/audit_pngs/iter_${ITERATION}"
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "============================================"
echo "  Visual Audit Loop — Iteration ${ITERATION}"
echo "============================================"
echo "File: $TEX_FILE"
echo "Output: $OUTPUT_DIR"
echo ""

# --- Check dependencies ---
for cmd in pdflatex pdftoppm; do
    if ! command -v "$cmd" > /dev/null 2>&1; then
        echo "ERROR: $cmd not found. Install texlive and poppler-utils."
        exit 3
    fi
done

# --- Step 1: Compile ---
echo "=== Step 1: Compile (2-pass) ==="
echo "Pass 1..."
if ! pdflatex -interaction=nonstopmode -halt-on-error -output-directory="$DIR" "$TEX_FILE" > /dev/null 2>&1; then
    echo "  FAIL: First pass compilation failed"
    echo "  Last 20 lines of log:"
    tail -20 "${BASE}.log" 2>/dev/null || echo "  (no log file)"
    exit 1
fi
echo "Pass 2..."
if ! pdflatex -interaction=nonstopmode -halt-on-error -output-directory="$DIR" "$TEX_FILE" > /dev/null 2>&1; then
    echo "  FAIL: Second pass compilation failed"
    exit 1
fi
echo "  OK: Compiled successfully"

# --- Step 2: Count pages ---
if command -v pdfinfo > /dev/null 2>&1; then
    PAGES=$(pdfinfo "$PDF" 2>/dev/null | grep -i "Pages" | awk '{print $2}')
else
    PAGES=$(strings "$PDF" | grep -c "/Type /Page" || echo "?")
fi
echo "  Pages: $PAGES"

# --- Step 3: Render all pages as PNGs ---
echo ""
echo "=== Step 2: Render all $PAGES pages as PNGs ==="
rm -rf "$OUTPUT_DIR"
mkdir -p "$OUTPUT_DIR"
pdftoppm -png -r 200 "$PDF" "${OUTPUT_DIR}/page"
RENDERED=$(ls "$OUTPUT_DIR"/page-*.png 2>/dev/null | wc -l)
echo "  Rendered: $RENDERED PNGs"

# --- Step 4: Run structural gates ---
echo ""
echo "=== Step 3: Structural gates (compile_check.sh) ==="
COMPILE_CHECK=""
if [ -f "${SCRIPT_DIR}/compile_check.sh" ]; then
    COMPILE_CHECK="${SCRIPT_DIR}/compile_check.sh"
elif [ -f "${DIR}/compile_check.sh" ]; then
    COMPILE_CHECK="${DIR}/compile_check.sh"
fi

GATE_STATUS=0
if [ -n "$COMPILE_CHECK" ]; then
    bash "$COMPILE_CHECK" "$TEX_FILE" --strict || GATE_STATUS=$?
    if [ "$GATE_STATUS" -eq 2 ]; then
        echo ""
        echo "WARNING: Structural gates FAILED. Fix structural issues before visual audit."
    fi
else
    echo "  [SKIP] compile_check.sh not found"
fi

# --- Step 5: Write manifest ---
echo ""
echo "=== Step 4: Audit manifest ==="
MANIFEST="${OUTPUT_DIR}/manifest.txt"
{
    echo "Visual Audit Manifest — Iteration ${ITERATION}"
    echo "Generated: $(date -Iseconds)"
    echo "Source: $TEX_FILE"
    echo "Pages: $PAGES"
    echo "Structural gates: $([ $GATE_STATUS -eq 0 ] && echo 'PASS' || echo 'FAIL')"
    echo ""
    echo "Pages to inspect (all ${RENDERED}):"
    ls -1 "$OUTPUT_DIR"/page-*.png | while read f; do
        echo "  $(basename "$f")"
    done
    echo ""
    echo "Inspection checklist per page:"
    echo "  [ ] No overlapping elements"
    echo "  [ ] No content clipped at bottom"
    echo "  [ ] No paper prose / figure captions on slide"
    echo "  [ ] All text readable at projection size"
    echo "  [ ] Figures properly trimmed (no adjacent panels visible)"
    echo "  [ ] Key Insight box fully visible"
    echo "  [ ] No fill=white artifacts"
    echo "  [ ] Spacing between elements is clean"
} > "$MANIFEST"

echo "  Manifest: $MANIFEST"
echo ""
echo "============================================"
echo "  Iteration ${ITERATION} complete"
echo "  PNGs: ${OUTPUT_DIR}/"
echo "  Structural: $([ $GATE_STATUS -eq 0 ] && echo 'PASS' || echo 'FAIL (exit 2)')"
echo ""
echo "  Next: Inspect PNGs visually. If defects found,"
echo "  fix source and re-run with --iteration $((ITERATION + 1))"
echo "============================================"

if [ "$GATE_STATUS" -eq 2 ]; then
    exit 2
fi
exit 0
