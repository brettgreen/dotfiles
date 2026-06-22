#!/usr/bin/env bash
# compile_check.sh — Compile beamer slides and validate against quality gates
# Usage: ./compile_check.sh <tex_file> [--strict]
#
# Gates checked:
#   G1: PDF compiles (pdflatex exits 0)
#   G2: Page count > 0
#   G3: P29 compliance (no transform shape, no \tiny/\scriptsize/\footnotesize in TikZ)
#   G4: Overfull box count
#   G5: Content coverage (optional: pass author names as extra args)
#   G6: Think First count (pedagogy metrics)
#   G7: Embedded figure quality (clip + keyinsight)
#   G8: Frame content inventory (no HIGH risk overflow frames)
#   G9: fill=white ban inside tikzpicture (PTL-014/031)
#   G10: CLEARANCE blocks per tikzpicture (PTL-006/013)
#   G11: No dangerously low scale values (PTL-006)
#
# Exit codes: 0 = all gates pass, 1 = compilation failed, 2 = gate violation

set -euo pipefail

TEX_FILE="${1:?Usage: compile_check.sh <tex_file> [--strict]}"
STRICT=false
AUTHOR_NAMES=()

shift
for arg in "$@"; do
    if [ "$arg" = "--strict" ]; then
        STRICT=true
    else
        AUTHOR_NAMES+=("$arg")
    fi
done

BASE="${TEX_FILE%.tex}"
DIR="$(dirname "$TEX_FILE")"
GATE_PASS=0
GATE_FAIL=0

# Resolve \input{} references: create a combined content file for searching
COMBINED_TEX=$(mktemp /tmp/compile_check_combined.XXXXXX)
trap 'rm -f "$COMBINED_TEX"' EXIT
# Inline \input{} one level deep (covers act1.tex, act2.tex, etc.)
awk -v dir="$DIR" '
/^\\input\{/ {
    fname = $0
    gsub(/.*\\input\{/, "", fname)
    gsub(/\}.*/, "", fname)
    # Try path relative to dir
    full = dir "/" fname
    while ((getline line < full) > 0) print line
    close(full)
    next
}
{ print }
' "$TEX_FILE" > "$COMBINED_TEX" 2>/dev/null || cp "$TEX_FILE" "$COMBINED_TEX"
# Use COMBINED_TEX for all content searches; TEX_FILE for compilation

gate_result() {
    local gate="$1" status="$2" detail="$3"
    if [ "$status" = "PASS" ]; then
        echo "  [PASS] $gate: $detail"
        GATE_PASS=$((GATE_PASS + 1))
    else
        echo "  [FAIL] $gate: $detail"
        GATE_FAIL=$((GATE_FAIL + 1))
    fi
}

echo "=== paper-to-lecture compile check ==="
echo "File: $TEX_FILE"
echo ""

# --- G1: Compilation ---
echo "Compiling (pass 1/2)..."
if ! pdflatex -interaction=nonstopmode -halt-on-error -output-directory="$DIR" "$TEX_FILE" > /dev/null 2>&1; then
    echo "  [FAIL] G1: First pass compilation failed"
    echo ""
    echo "Last 20 lines of log:"
    tail -20 "${BASE}.log" 2>/dev/null || echo "  (no log file found)"
    exit 1
fi

echo "Compiling (pass 2/2)..."
if ! pdflatex -interaction=nonstopmode -halt-on-error -output-directory="$DIR" "$TEX_FILE" > /dev/null 2>&1; then
    gate_result "G1-compile" "FAIL" "Second pass compilation failed"
else
    gate_result "G1-compile" "PASS" "Compiled successfully"
fi

# --- G2: Page count ---
if [ -f "${BASE}.pdf" ]; then
    if command -v pdfinfo > /dev/null 2>&1; then
        PAGES=$(pdfinfo "${BASE}.pdf" 2>/dev/null | grep -i "Pages" | awk '{print $2}')
    else
        PAGES=$(strings "${BASE}.pdf" | grep -c "/Type /Page" || echo "?")
    fi
    if [ "$PAGES" -gt 0 ] 2>/dev/null; then
        gate_result "G2-pages" "PASS" "${PAGES} pages"
    else
        gate_result "G2-pages" "FAIL" "0 pages or unable to count"
    fi
else
    gate_result "G2-pages" "FAIL" "No PDF generated"
fi

# --- G3: P29 compliance (TikZ quality) ---
TRANSFORM_COUNT=$(grep -c 'transform shape' "$COMBINED_TEX" 2>/dev/null || true)
TRANSFORM_COUNT=${TRANSFORM_COUNT:-0}
# Count \tiny only inside tikzpicture environments
TINY_IN_TIKZ=$(sed -n '/\\begin{tikzpicture}/,/\\end{tikzpicture}/p' "$COMBINED_TEX" 2>/dev/null | grep -c '\\tiny' || true)
TINY_IN_TIKZ=${TINY_IN_TIKZ:-0}
SCRIPTSIZE_IN_TIKZ=$(sed -n '/\\begin{tikzpicture}/,/\\end{tikzpicture}/p' "$COMBINED_TEX" 2>/dev/null | grep -c '\\scriptsize' || true)
SCRIPTSIZE_IN_TIKZ=${SCRIPTSIZE_IN_TIKZ:-0}
FOOTNOTESIZE_IN_TIKZ=$(sed -n '/\\begin{tikzpicture}/,/\\end{tikzpicture}/p' "$COMBINED_TEX" 2>/dev/null | grep -c '\\footnotesize' || true)
FOOTNOTESIZE_IN_TIKZ=${FOOTNOTESIZE_IN_TIKZ:-0}

P29_VIOLATIONS=$((TRANSFORM_COUNT + TINY_IN_TIKZ + SCRIPTSIZE_IN_TIKZ + FOOTNOTESIZE_IN_TIKZ))
if [ "$P29_VIOLATIONS" -eq 0 ]; then
    gate_result "G3-P29" "PASS" "0 violations"
else
    gate_result "G3-P29" "FAIL" "${P29_VIOLATIONS} violations (transform_shape=${TRANSFORM_COUNT}, tiny=${TINY_IN_TIKZ}, scriptsize=${SCRIPTSIZE_IN_TIKZ}, footnotesize=${FOOTNOTESIZE_IN_TIKZ})"
fi

# --- G4: Overfull boxes ---
OVERFULL=$(grep -c 'Overfull' "${BASE}.log" 2>/dev/null || true)
OVERFULL=${OVERFULL:-0}
if [ "$OVERFULL" -eq 0 ]; then
    gate_result "G4-overflow" "PASS" "0 overfull warnings"
elif [ "$OVERFULL" -lt 5 ]; then
    gate_result "G4-overflow" "PASS" "${OVERFULL} overfull warnings (within tolerance)"
else
    if [ "$STRICT" = true ]; then
        gate_result "G4-overflow" "FAIL" "${OVERFULL} overfull warnings"
    else
        gate_result "G4-overflow" "PASS" "${OVERFULL} overfull warnings (not strict mode)"
    fi
fi

# --- G5: Content coverage (optional) ---
if [ ${#AUTHOR_NAMES[@]} -gt 0 ]; then
    MISSING=()
    for name in "${AUTHOR_NAMES[@]}"; do
        if ! grep -qi "$name" "$COMBINED_TEX" 2>/dev/null; then
            MISSING+=("$name")
        fi
    done
    if [ ${#MISSING[@]} -eq 0 ]; then
        gate_result "G5-coverage" "PASS" "All ${#AUTHOR_NAMES[@]} authors found"
    else
        gate_result "G5-coverage" "FAIL" "Missing: ${MISSING[*]}"
    fi
fi

# --- G6: Think First count (pedagogy) ---
THINK_COUNT=$(grep -c '\\think{' "$COMBINED_TEX" 2>/dev/null || true)
THINK_COUNT=${THINK_COUNT:-0}
echo ""
echo "Pedagogy metrics:"
echo "  \\think{} count: ${THINK_COUNT}"
echo "  \\keyinsight{} count: $(grep -c '\\keyinsight{' "$COMBINED_TEX" 2>/dev/null || true)"
echo "  \\mechanism{} count: $(grep -c '\\mechanism{' "$COMBINED_TEX" 2>/dev/null || true)"
echo "  TikZ diagrams: $(grep -c '\\begin{tikzpicture}' "$COMBINED_TEX" 2>/dev/null || true)"
echo "  Embedded figures: $(grep -c '\\includegraphics\[.*page=\|\\paperfigure{' "$COMBINED_TEX" 2>/dev/null || true)"

# --- G7: Embedded figure quality ---
# Match both raw \includegraphics[...page=] and the \paperfigure{} convenience macro
EMBED_COUNT=$(grep -c '\\includegraphics\[.*page=\|\\paperfigure{' "$COMBINED_TEX" 2>/dev/null || true)
EMBED_COUNT=${EMBED_COUNT:-0}
if [ "$EMBED_COUNT" -gt 0 ]; then
    # Check clip on raw \includegraphics only (\paperfigure passes options through, so check those too)
    EMBED_NO_CLIP=$(grep '\\includegraphics\[.*page=' "$COMBINED_TEX" 2>/dev/null | grep -v 'clip' | wc -l || true)
    EMBED_NO_CLIP=${EMBED_NO_CLIP:-0}
    if [ "$EMBED_NO_CLIP" -gt 0 ]; then
        gate_result "G7-embed" "FAIL" "${EMBED_NO_CLIP} embedded figures missing 'clip'"
    else
        gate_result "G7-embed" "PASS" "All ${EMBED_COUNT} embedded figures have clip"
    fi
    # Check that every embedded figure frame has a keyinsight or mechanism
    # \paperfigure always includes keyinsight (4th arg), so only check raw \includegraphics
    EMBED_FRAMES=$(grep -n '\\includegraphics\[.*page=' "$COMBINED_TEX" 2>/dev/null | cut -d: -f1)
    EMBED_NO_INSIGHT=0
    for line_num in $EMBED_FRAMES; do
        # Check next 20 lines after includegraphics for keyinsight or mechanism
        CONTEXT=$(sed -n "${line_num},$((line_num + 20))p" "$COMBINED_TEX" 2>/dev/null)
        if ! echo "$CONTEXT" | grep -q '\\keyinsight\|\\mechanism\|\\paperfigure'; then
            EMBED_NO_INSIGHT=$((EMBED_NO_INSIGHT + 1))
        fi
    done
    if [ "$EMBED_NO_INSIGHT" -gt 0 ]; then
        gate_result "G7-insight" "FAIL" "${EMBED_NO_INSIGHT} embedded figures missing \\keyinsight{} or \\mechanism{}"
    else
        gate_result "G7-insight" "PASS" "All ${EMBED_COUNT} embedded figures have interpretation"
    fi
fi

# === G8: Frame Content Inventory ===
echo ""
echo "=== G8: Frame Content Inventory ==="
# Locate frame_content_inventory.py: check current dir, then scripts dir alongside this script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FCI_SCRIPT=""
if [ -f "./frame_content_inventory.py" ]; then
    FCI_SCRIPT="./frame_content_inventory.py"
elif [ -f "${DIR}/frame_content_inventory.py" ]; then
    FCI_SCRIPT="${DIR}/frame_content_inventory.py"
elif [ -f "${SCRIPT_DIR}/frame_content_inventory.py" ]; then
    FCI_SCRIPT="${SCRIPT_DIR}/frame_content_inventory.py"
fi

if [ -n "$FCI_SCRIPT" ]; then
    FCI_OUTPUT=$(python3 "$FCI_SCRIPT" "$COMBINED_TEX" --out /tmp/compile_check_fci 2>&1) || true
    HIGH_COUNT=$(echo "$FCI_OUTPUT" | grep -oP 'HIGH risk.*?:\s*\K\d+' || echo "0")
    HIGH_COUNT=${HIGH_COUNT:-0}
    echo "$FCI_OUTPUT"
    if [ "$HIGH_COUNT" -gt 0 ]; then
        gate_result "G8-inventory" "FAIL" "${HIGH_COUNT} HIGH risk frames (overflow >5.8cm)"
    else
        gate_result "G8-inventory" "PASS" "0 HIGH risk frames"
    fi
else
    echo "  [SKIP] G8: frame_content_inventory.py not found"
fi

# === G9: fill=white inside tikzpicture (PTL-014/031) ===
echo ""
echo "=== G9: fill=white ban ==="
# Extract tikzpicture blocks, exclude comments, count fill=white
FILL_WHITE_IN_TIKZ=$(sed -n '/\\begin{tikzpicture}/,/\\end{tikzpicture}/p' "$COMBINED_TEX" 2>/dev/null | grep -v '^\s*%' | grep -c 'fill=white' || true)
FILL_WHITE_IN_TIKZ=${FILL_WHITE_IN_TIKZ:-0}
# Exclude mseLegend style definition (legitimate use in preamble)
FILL_WHITE_LEGEND=$(sed -n '/\\begin{tikzpicture}/,/\\end{tikzpicture}/p' "$COMBINED_TEX" 2>/dev/null | grep -v '^\s*%' | grep 'mseLegend' | grep -c 'fill=white' || true)
FILL_WHITE_LEGEND=${FILL_WHITE_LEGEND:-0}
FILL_WHITE_ACTUAL=$((FILL_WHITE_IN_TIKZ - FILL_WHITE_LEGEND))
if [ "$FILL_WHITE_ACTUAL" -le 0 ]; then
    gate_result "G9-fill-white" "PASS" "0 fill=white in tikzpicture (PTL-014)"
else
    gate_result "G9-fill-white" "FAIL" "${FILL_WHITE_ACTUAL} fill=white in tikzpicture (PTL-014: banned — reposition elements instead)"
fi

# === G10: CLEARANCE blocks per tikzpicture ===
echo ""
echo "=== G10: CLEARANCE blocks ==="
TIKZ_COUNT=$(grep -c '\\begin{tikzpicture}' "$COMBINED_TEX" 2>/dev/null || true)
TIKZ_COUNT=${TIKZ_COUNT:-0}
CLEARANCE_COUNT=$(grep -c '% === CLEARANCE ===' "$COMBINED_TEX" 2>/dev/null || true)
CLEARANCE_COUNT=${CLEARANCE_COUNT:-0}
CLEARANCE_MISSING=$((TIKZ_COUNT - CLEARANCE_COUNT))
if [ "$CLEARANCE_MISSING" -le 0 ]; then
    gate_result "G10-clearance" "PASS" "${CLEARANCE_COUNT}/${TIKZ_COUNT} tikzpictures have CLEARANCE blocks"
else
    if [ "$STRICT" = true ]; then
        gate_result "G10-clearance" "FAIL" "${CLEARANCE_MISSING} tikzpictures missing CLEARANCE blocks (${CLEARANCE_COUNT}/${TIKZ_COUNT})"
    else
        echo "  [WARN] G10: ${CLEARANCE_MISSING} tikzpictures missing CLEARANCE blocks (${CLEARANCE_COUNT}/${TIKZ_COUNT})"
    fi
fi

# === G11: No scale < 0.70 with text width > 1.8cm ===
echo ""
echo "=== G11: scale/text-width safety ==="
# Extract tikzpicture blocks and check for dangerous scale+text-width combos
G11_VIOLATIONS=0
TIKZ_BLOCKS=$(sed -n '/\\begin{tikzpicture}/,/\\end{tikzpicture}/p' "$COMBINED_TEX" 2>/dev/null || true)
if [ -n "$TIKZ_BLOCKS" ]; then
    # Check for scale < 0.70 in any tikzpicture that also has text width > 1.8cm
    # Simple heuristic: grep for scale=0.6 or scale=0.5 patterns
    for bad_scale in "scale=0.5" "scale=0.6" "scale=0.4" "scale=0.3"; do
        COUNT=$(echo "$TIKZ_BLOCKS" | grep -c "$bad_scale" || true)
        G11_VIOLATIONS=$((G11_VIOLATIONS + COUNT))
    done
fi
if [ "$G11_VIOLATIONS" -eq 0 ]; then
    gate_result "G11-scale-safety" "PASS" "No dangerously low scale values (<0.70)"
else
    gate_result "G11-scale-safety" "FAIL" "${G11_VIOLATIONS} tikzpictures with scale < 0.70 (risk of text-width overlap — PTL-006)"
fi

# --- Summary ---
echo ""
echo "=== Results: ${GATE_PASS} passed, ${GATE_FAIL} failed ==="

if [ "$GATE_FAIL" -gt 0 ]; then
    exit 2
fi
exit 0
