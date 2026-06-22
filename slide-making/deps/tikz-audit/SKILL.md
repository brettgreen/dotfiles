---
name: tikz-audit
description: >-
  Audit and fix TikZ diagrams in beamer slides using a converging parallel loop.
  Compiles, renders ALL pages, launches parallel background audit agents,
  collects defects via file-based IPC, launches parallel fixers with patch files,
  re-audits the full deck every iteration, and iterates until convergence. Use when diagrams have overlaps,
  spacing issues, clipping, or need comprehensive quality sweeps.
  Triggers: tikz-audit, tikz fix, diagram audit, visual defects, TikZ convergence.
allowed-tools: Read, Edit, Write, Bash, Glob, Grep, Task, TodoWrite
user-invocable: true
---

# TikZ Convergence Loop — Full Audit-Fix Skill

## Architecture

```
COMPILE -> RENDER ALL -> PARALLEL AUDIT -> COLLECT -> PARALLEL FIX -> RE-COMPILE -> RE-RENDER -> RE-AUDIT -> ... -> 0 DEFECTS
```

**Core innovation**: Background agents + file-based IPC. Agents write results to `/tmp` files, never to main context. This enables 20+ parallel agents without context explosion.

## Anti-Pattern: NEVER DO THIS

```
WRONG: 20 foreground agents -> 20 result messages -> 10K+ lines -> context dead
```

## Correct Pattern

```
RIGHT: 20 background agents (run_in_background: true)
       -> each writes to /tmp/tikz_audit_batch_NN.md
       -> poll completion via bash (sleep + check files)
       -> bash script merges all files
       -> Read ONE merged summary into context
```

---

## Step-by-Step Protocol

### Step 0: Checkpoint Commit
Before ANY edits, ensure working tree is clean or commit current state.
```bash
git add -f <tex_file> && git commit -m "TikZ audit checkpoint (pre-edit)"
```
This is the rollback point.

### Step 0.5: Source-Code Pre-Audit (MANDATORY — before rendering)

Run these automated checks on the tex source BEFORE compiling or rendering. They catch ~40% of defects instantly with zero rendering cost.

```bash
# Gate G9: fill=white inside tikzpicture (must be 0)
FILL_WHITE=$(sed -n '/\\begin{tikzpicture}/,/\\end{tikzpicture}/p' <file>.tex | grep -v '^\s*%' | grep -c 'fill=white' || true)

# Gate G10: Every tikzpicture has a CLEARANCE block
TIKZ_COUNT=$(grep -c '\\begin{tikzpicture}' <file>.tex || true)
CLEARANCE_COUNT=$(grep -c '% === CLEARANCE ===' <file>.tex || true)
# CLEARANCE_COUNT should equal TIKZ_COUNT

# Gate G11: No scale < 0.70 with text width > 1.8cm
# Extract scale + text width pairs from tikzpicture blocks and check
```

**If G9 > 0**: Remove all fill=white inside tikzpicture. Replace with coordinate repositioning (PTL-014). This is the #1 fix anti-pattern — agents that don't read the anti-pattern list use fill=white as a "quick fix" and it creates visible white rectangles.

**If G10 mismatch**: Add `% === CLEARANCE ===` blocks to tikzpictures that lack them. Compute physical clearances for all adjacent node pairs.

**If G11 fails**: Either increase scale to >= 0.70 or reduce text width to <= 1.8cm.

**Subagent prompt requirement (PTL-029)**: Every audit/fix subagent prompt MUST include the full anti-pattern list from this file (the "Anti-patterns" section below). Do NOT rely on agents reading this file — inject the list as literal text in the prompt.

### Step 1: Enumerate ALL Frames and TikZ Frames
Parse the tex file for all `\begin{frame}` blocks and all `\begin{tikzpicture}` blocks. Map each to frame number and PDF page range using the `.nav` file.

```python
# Outputs:
# /tmp/frame_map_all.txt  — list of (frame#, page_start, page_end, title)
# /tmp/tikz_frame_map.txt — list of (frame#, page_start, page_end)
```

Expected: 40-80 TikZ frames in a typical lecture deck.

### Step 1.5: Source-Code Clearance Pre-Check (PTL-013)

**Before rendering**, grep for all `scale=` and `text width=`/`minimum width=` in tikzpicture environments. Compute physical gaps algebraically. This catches the #1 defect class (PTL-006: scale-vs-physical-width overlap) without needing PNGs.

```bash
# Extract all tikzpicture blocks with scale + text width/minimum width
grep -n 'scale=\|text width=\|minimum width=' <file>.tex
```

**For each tikzpicture with `scale=S`:**
1. Find all node coordinates (x, y) and their `text width=Ncm` or `minimum width=Ncm`
2. For each pair of adjacent nodes at coords (x1, y1) and (x2, y2):
   - `physical_gap = sqrt((x2-x1)^2 + (y2-y1)^2) * scale`
   - `max_box_extent = max(text_width_1, text_width_2)`
   - If `physical_gap < max_box_extent + 0.3cm`: flag as **CRITICAL**
3. Write flagged overlaps to `/tmp/tikz_clearance_precheck.md`

**Rule G7:** No `scale < 0.70` paired with `text width > 1.8cm` anywhere in the file.

**If any CRITICAL flags found**, fix them BEFORE compiling. This saves an entire audit iteration. The fix pattern: increase scale to 0.72-0.85, reduce text width to fit, or widen coordinate gaps.

### Step 2: Compile + Render ALL Pages

**STALE-RENDER GUARD (PTL-012):** If the PDF already exists, check `stat -c %Y <file>.pdf` vs `stat -c %Y <file>.tex`. If `pdf_mtime < tex_mtime`, the PDF is stale — MUST recompile. Never audit stale PNGs. Similarly, if PNGs exist in `/tmp/tikz_render/`, verify they are from the CURRENT compilation by comparing mtimes.

```bash
# Clean compile (2 passes for nav)
pdflatex -interaction=nonstopmode -halt-on-error <file>.tex
pdflatex -interaction=nonstopmode -halt-on-error <file>.tex

# Verify: 0 errors, check page count
pdfinfo <file>.pdf | grep Pages  # Record as BASELINE_PAGES

# Render ALL pages in ONE pdftoppm call (not a loop — loops corrupt the PDF)
cp <file>.pdf /tmp/render_source.pdf
pdftoppm -png -r 150 /tmp/render_source.pdf /tmp/tikz_render/page
```

**CRITICAL**: Always `cp` the PDF first, then render from the copy. Never render from the working PDF while compiling. Loop-based `pdftoppm -f N -l N` calls corrupt the file on macOS.

### Step 3: Parallel Audit — 20+ Background Agents (FULL DECK)

Split ALL frames/pages into 20+ batches. Each audit agent:

1. Reads PNG renders for its assigned pages (3-8 PNGs = small context)
2. Reads corresponding frame source (and TikZ source if present)
3. Checks against the **defect checklist** (see below)
4. Writes defect report to `/tmp/tikz_audit_batch_NN.md`

**Launch pattern:**
```
Task(
  subagent_type="general-purpose",
  run_in_background=true,
  model="sonnet",
  prompt="... write report to /tmp/tikz_audit_batch_NN.md ..."
)
```

**Why 20+ agents**: Each sees a small page slice, high accuracy. All agents finish near the wall time of one small batch.

**Default rule (strict)**: Never scope to only user-mentioned frames unless the user explicitly asks for a scoped/quick run. Standard mode is full-deck audit every time.

### Step 4: Poll Completion + Merge

```bash
# Poll loop (run every 30-60s)
for i in $(seq -w 0 19); do
  if [ -f "/tmp/tikz_audit_batch_${i}.md" ]; then
    echo "Batch $i: DONE"
  else
    echo "Batch $i: pending"
  fi
done

# When all 20 done, merge with Python script
python3 merge_defects.py  # -> /tmp/tikz_defects_iteration_N.md
```

**Severity parsing**: Agents use varied formats (`**Severity**: HIGH`, `[HIGH]`, table rows). The merge script must try multiple regex patterns:
```python
for pat in [r'\*\*Severity\*\*.*?(HIGH|MEDIUM|LOW)',
            r'\[HIGH\]|\[MEDIUM\]|\[LOW\]',
            r'Severity:\s*(HIGH|MEDIUM|LOW)']:
    ...
```

### Step 5: Parallel Fix — 20 Background Agents

Group defects by frame. Each fixer agent gets 1-2 frames (non-overlapping). Tighter scope reduces new-collision risk. Each fixer:

1. Reads the FULL tex file + its defect report + PNG evidence
2. Applies **structural fixes** (not coordinate nudges):
   - Text clipping -> increase box width (rectangle coords or minimum width)
   - Box too small -> increase minimum width/minimum height
   - Font overflow -> reduce font to `\scriptsize` or add `text width=Ncm`
   - Label overlap -> reposition with `pos=` on path
   - Footer collision -> reduce scale or move content up
3. Writes a JSON patch file to `/tmp/tikz_fix_patches_NN.json`:

```json
[
  {
    "frame": 5,
    "defect": "Text clips right edge",
    "old_string": "exact string from file",
    "new_string": "replacement string"
  }
]
```

**CRITICAL**: Fixers write patches to FILES, not direct edits. A single sequential merge step applies all patches afterward. This prevents edit conflicts.

### Step 6: Apply Patches Sequentially

```python
# Validate: each old_string must appear exactly once
# Apply bottom-up (reverse position order) to preserve offsets
positions.sort(key=lambda x: x[0], reverse=True)
for pos, patch in positions:
    content = content[:pos] + patch['new_string'] + content[pos + len(patch['old_string']):]
```

### Step 7: Re-compile + Re-render + Re-audit

```
Compile: must be 0 errors
Page count: must be ±2 of BASELINE_PAGES
Re-render all pages (same method as Step 2)
Launch re-audit agents on the FULL deck (not only fixed frames)
```

**Re-run Step 1.5 source-code clearance check** after recompile. Any new G7 violations introduced by the fix wave = REGRESSION — revert that patch and re-fix before proceeding.

### Step 8: Convergence Check

| Gate | Condition | Action if FAIL |
|------|-----------|----------------|
| G1 | 0 compile errors | Fix compile errors before visual check |
| G2 | Page count ±2 of baseline | Investigate what changed |
| G3 | 0 HIGH defects remaining (full deck) | Must fix all HIGH before next iteration |
| G4 | 0 MEDIUM defects remaining (full deck) | Fix or document (max 2 iterations on MEDIUM) |
| G5 | Defect count decreasing | If increasing, revert to checkpoint |
| G6 | Max iterations ≤10 | If defect count not decreasing for 2 consecutive iterations, escalate. Otherwise continue looping. |
| G7 | Source-code clearance: no `scale < 0.70` with `text width > 1.8cm` | Fix scale/width before visual audit |
| G8 | Stale-render check: PDF mtime > tex mtime | Recompile before auditing |
| G9 | Full-deck spot-check completed each iteration | If not, run another full pass |
| G10 | Per-frame spot-check: after each fix wave, re-render only patched frames and run 1 quick-audit agent per patched frame. Any new collision in a patched frame = REGRESSION (revert + re-fix). Do NOT proceed to full re-audit until G10 passes. | ~30s per fix wave | If REGRESSION: revert patch, add neighbor-check context, re-fix |

**G10 spot-check protocol** (run after EVERY fix wave, before full re-audit):
```bash
# Re-render only patched frames
for frame in ${PATCHED_FRAMES}; do
  pdftoppm -png -r 150 -f ${page_start[$frame]} -l ${page_end[$frame]} \
    /tmp/render_source.pdf /tmp/tikz_render/spotcheck_frame${frame}
done
# Launch 1 quick-audit agent per patched frame (background)
# Each writes to /tmp/tikz_spotcheck_frame${frame}.md
# Poll until all complete, then check for REGRESSION markers
```

**If converged (0 HIGH + 0 MEDIUM)**: commit and done.
**If not converged**: loop back to Step 5 with remaining defects.

### Step 9: Rule Extraction + Commit

After convergence:
1. Extract defect patterns and fix patterns that worked
2. Append to `memory/tikz_convergence_rules.md`
3. Commit with descriptive message

---

## Defect Checklist (for audit agents)

Each rendered page is checked for (all pages, all overlays):

### Visual Defects (existing diagrams)
1. **Text clipping** — text touches or extends past box edges (left/right/top/bottom)
2. **Frame boundary overflow** — content extends beyond slide area
3. **Label collision** — labels overlap with other labels, arrows, or boxes
4. **Footer/header collision** — element within 10pt of footer bar or title bar
5. **Overlay overlap** — elements that shouldn't overlap on specific overlay stages
6. **Font too small (P29)** — any text smaller than body text (`\small` / ~10pt on 11pt beamer). Grep for `transform shape`, `\tiny`, `\scriptsize`, `font=\footnotesize` in TikZ environments — all must be zero.
7. **Boxes too small** — content doesn't fit the container
8. **Arrows through text (PTL-014)** — lines or arrows crossing through text nodes. Check ALL labels placed on or near arrow paths: if the label lacks `fill=white`, the arrow line will cut through the text. Labels with `right`/`left` anchoring near diagonal arrows are the most common offenders. Labels with `above`/`below` on straight horizontal/vertical arrows are usually safe. Standalone `\node` labels at the same y-coordinate as nearby arrow endpoints also fail.
9. **Missing/cut-off text** — nodes with truncated content
10. **Color contrast** — text unreadable against background color. For colored labels (not black), saturation must be >= 70% (e.g., `StanfordRed!70` not `StanfordRed!40`). Light tints (< 50%) are unreadable on projectors.
11. **Label-to-element overlap (PTL-016)** — label text extent overlaps with nearby boxes, legends, or other labels (not just arrows). Compute physical text width at given font+scale and check clearance against ALL neighboring elements. Must be >= 0.3cm.
12. **Inter-gap label overflow (PTL-017)** — label placed between two boxes (above connecting arrow) is wider than the physical gap. Verify `label_text_width < gap_width - 0.4cm` at the diagram's scale.
13. **Invisible chart elements (PTL-018)** — bars, lines, or data points with physical height < 0.25cm. Check all quantitative chart elements (bar charts, dot plots) for elements scaled below the visibility threshold. Flag as HIGH.
14. **Frame boundary overflow (PTL-019)** — `\node` text placed at coordinates that map outside the beamer slide area. In 16:9 beamer, safe range is approximately x: [-6.5, 6.5]cm, y: [0.2, 7.8]cm. Grep source for any `\node` with coordinate |x| > 6.5 or y < 0.2 or y > 7.8. Also check visually: content touching or past right/left/top slide edges. Flag as **HIGH**. Fix: reposition to inside boundary + add `text width` constraint. Common cause: side-annotation nodes placed next to tabular environments.
15. **Diagonal rotated label collision (PTL-R1)** — `\node[rotate=N]` where N ∉ {0, 90, 180, 270}. Rotated text occupies a larger bounding box:
    - `width_bb = |cos(N°)| × text_width + |sin(N°)| × text_height`
    - `height_bb = |sin(N°)| × text_width + |cos(N°)| × text_height`
    Check clearance of this rotated footprint against ALL neighboring elements (axis lines, other labels, box edges). Must be >= 0.3cm physical. Flag as **MEDIUM**. Fix: reposition the rotated node to a less crowded location, or reduce text length.
16. **Proof/logic diagram height overflow (PTL-020)** — When a frame contains a TikZ diagram with 4+ connected boxes arranged vertically (proof circuits, equivalence chains), compute:
    `total_height = (max_y - min_y) × scale + max_node_physical_height`
    Beamer body available height ≈ 6.0cm (after title bar + footer). If `total_height > 5.5cm`: flag as **HIGH** (content will clip into footer or mechanism box will be cut off). Fix: (a) increase horizontal spread — arrange as 2-3 boxes per row instead of a single column, (b) use `\scriptsize` for box content text only (not labels), or (c) split the proof into two frames.

17. **Vertical content overflow (PTL-026)** — frame content exceeds beamer body height (~6.0cm for 16:9 after title + footer). Beamer silently clips without emitting overfull vbox warnings. Detect by computing estimated vertical height: `\paperfigure` ~5.0cm, `\tikzpicture` ~4.0cm, `\think{}/\keyinsight{}` ~1.5cm + 0.3cm/line, items ~0.4cm each, display equation ~0.8cm. If total > 5.8cm: flag as **HIGH**. Common offender: `\paperfigure` + `\think{}` on same frame, or multi-panel figure + long keyinsight. Fix: split frame, shorten keyinsight to <=160 chars, or move `\think{}` to preceding frame. Run `frame_content_inventory.py` for automated detection.

18. **fill=white artifacts (PTL-014/031)** — any `fill=white` inside a tikzpicture environment (excluding comments and mseLegend style definitions). Creates visible white rectangles that mask content instead of properly spacing it. Flag as **CRITICAL**. Fix: remove `fill=white` and reposition the element using coordinate gaps. The `compile_check.sh` G9 gate catches this automatically, but visual audit should also flag it since agents that bypass the gate will produce this defect. Most common pattern: `mseEdgeLabel` overridden with `fill=white` to "fix" arrow-through-label overlaps.

### Visualization Gaps (missing diagrams)
11. **Concept without visual** — frame introduces a new mechanism, equilibrium, tradeoff, timeline, or comparison but has NO TikZ diagram. The pedagogical principle: "Can a student immediately *see* this mechanism?" If not, it needs a diagram. Flag as MEDIUM (concept-only frames) or HIGH (multi-step process described in bullets with no pipeline diagram).
12. **Bullet-list process** — a numbered or bulleted list describing a sequential process (3+ steps) that should be a TikZ pipeline/timeline instead. Flag as MEDIUM.
13. **Missing mechanism/keyinsight box** — a TikZ diagram exists but is NOT followed by a `\mechanism{}` or `\keyinsight{}` box explaining what the diagram shows. Flag as LOW.

**Concept-to-diagram mapping** (what diagram style each concept type needs):
| Concept Type | Expected Diagram |
|---|---|
| Equilibrium / indifference | Two curves intersecting or threshold diagram |
| Regime transition | Threshold with behavior flip on each side |
| Timeline / sequence | Horizontal TikZ timeline with labeled events |
| Game theory | 2x2 payoff matrix or extensive-form game tree |
| Tradeoff / opposing forces | Two-box comparison with threshold |
| Flow / pipeline / process | Pipeline diagram with stages and arrows |
| Functional form / curve | Plot (bonding curve, utility, cost) |
| Comparison (A vs B) | Side-by-side parallel diagrams |
| Architecture / system | Box-and-arrow system diagram |
| Data / empirical result | Bar chart, scatter plot, or stylized chart |

---

## Fix Pattern Library (proven patterns from production)

| Defect | Fix | Success Rate |
|--------|-----|-------------|
| Text clips box edge | Widen box (change rectangle coords) | 90% |
| Text overflow | Add `text width=Ncm` constraint | 85% |
| Long single-line text | Wrap to 2 lines with `\\` + `align=center` | 90% |
| Rotated label overflow | Reduce `\small` -> `\scriptsize` | 80% |
| Label collision | Stagger vertically (different y-coords) | 75% |
| Z-order issue | Reorder TikZ draw commands (later = on top) | 85% |
| Footer collision | Reduce scale by 0.03-0.05 | 70% |
| Left-anchored diagram | Add `\useasboundingbox` for consistent centering | 80% |
| `transform shape` shrinks fonts | Remove `every node/.style={transform shape}`, increase scale to 0.80-0.95 | 95% |
| `\onslide` breaks TikZ node | Replace with `\only<N-M>{...}` inside TikZ nodes | 100% |
| `\onslide` breaks tabular row | Replace with `\uncover<N->{}` wrapping each cell individually | 100% |
| Nodes overlap after removing transform shape | Increase coordinate spacing + reduce `minimum width` (nodes now physical size) | 85% |
| Bar chart labels overlap subtitle | Separate title/subtitle from data labels by >= 0.7 scaled y-units | 95% |
| `text width` boxes overlap neighbors (scaled diagram) | Remove `scale`, use direct cm coordinates (scale=1) so text width matches physical spacing | 95% |
| Edge label overlaps nearby node | Move label from `midway` to `pos=0.3` or `pos=0.7`, or place as separate node at explicit coords | 90% |
| Arrow midway label between tight boxes | Place label as separate `\node` at explicit (x,y) above the arrow path, not as edge label | 90% |
| Cascade/chain labels overlap boxes | Use separate label nodes at explicit y-offsets above arrow paths (e.g., y+0.5) | 85% |
| Color too light for projection | Increase saturation from !40 to !70 or higher | 95% |
| Arrow line through label text | REPOSITION as separate `\node` at explicit (x,y) coords that clear the arrow path by >= 0.3cm physical. NEVER use `above=Npt` edge labels (any pt value risks grazing at scaled diagrams) or `fill=white` (PTL-014/015). For arrow endpoints near text: ensure `\|endpoint - text\| * scale - text_height/2 >= 0.3cm`. | 90% |
| Annotation region crowding | 3+ text nodes within 1cm physical radius = CROWDED. Spread annotations to separate regions (e.g., move "Quoted" from right margin to mid-chart). | 85% |
| Left-anchored label clips slide margin | Switch from `[left]` at x=0 to `[right]` at negative x (e.g., x=-3.2) | 90% |
| Repositioned label creates new collision | After moving, check ALL elements within `1cm / scale` coordinate radius of new position | 85% |

**Anti-patterns (these DON'T converge):**
- Blind coordinate nudges (+0.3, -0.2) without understanding layout
- `shrink=N` on beamer frames (unreliable)
- Adjusting scale without checking all overlay stages
- Using `\onslide` inside TikZ `\node` commands (causes "Giving up on this path" error)
- Using `\onslide` to wrap entire tabular rows with `&` and `\\` (causes `\noalign` error)
- JSON patch files with `old_string` matching — match rate ~0% on large files. Use direct Edit tool or file segmentation instead.
- Naming a TikZ style `step` — conflicts with TikZ built-in `step` key. Use `stepbox`, `stepnode`, etc.
- `\ding{55}` without `\usepackage{pifont}` — prefer `$\times$` for cross marks
- Mixing `text width=Ncm` (physical) with `scale=S` (coordinate) — at scale 0.6, two nodes 3 units apart are only 1.8cm apart physically, but 2cm text-width boxes are each 2cm wide. They WILL overlap. Either: (a) drop scale and position in cm directly, or (b) set `text width` small enough for the scaled spacing (`text width <= spacing * scale * 0.9`)
- Labels placed `[midway, above]` on arrows between boxes with < 2 units vertical gap — the label lands inside the destination box. Place as separate node at explicit coordinates instead.
- Repositioning a label without checking neighbors — the new position may collide with time markers, axis labels, or other annotations. Always verify the destination is clear before committing a fix.
- Using `above=5pt` or any small pt offset for edge labels on arrows — 5pt = 1.75mm, less than text height (6-10pt) + arrowhead (3pt). The arrow line WILL graze the text. Always use separate `\node` at explicit coordinates instead (PTL-015).
- Trusting that an arrow endpoint "near" a text node is "close enough" — compute `physical_gap = |endpoint_coord - text_coord| * scale - text_height/2`. If < 0.3cm, the arrowhead overlaps the text.
- Using color saturation below 50% for any label or annotation — will be invisible on projectors even if readable on screen

---

## Physical Clearance Calculation

When checking label-to-box clearance in scaled diagrams, audit agents MUST compute physical distances, not just coordinate distances. TikZ `scale` only affects coordinates, NOT `minimum height`, `minimum width`, or `text width`.

**Formula:**
```
physical_clearance = (label_coordinate - box_edge_coordinate) × scale
box_edge_physical = box_center_coordinate × scale ± (minimum_height / 2)
```

**Example (AMM Evolution, Week 10):**
- Box at y=0 with `minimum height=1.8cm`, scale=0.58
- Box top = 0 × 0.58 + 0.9cm = 0.9cm physical
- Label at y=1.6 → physical y = 1.6 × 0.58 = 0.928cm
- Clearance = 0.928 - 0.9 = 0.028cm ← OVERLAPPING
- Fix: raise to y=2.5 → physical y = 1.45cm → clearance = 0.55cm ← OK

**Rule of thumb**: If `physical_clearance < 0.2cm`, it's a defect. Labels need >= 0.3cm physical clearance from box edges.

---

## Font-Normalization Sub-Protocol (P29 Enforcement)

When TikZ text is too small (common: `transform shape` + scale compounds font sizes), run this dedicated sub-protocol instead of the general audit-fix loop.

### Diagnosis

```bash
# Count diagrams with transform shape
grep -c 'transform shape' <file>.tex

# Find smallest effective font
# With transform shape at scale S: \tiny(6pt)*S, \scriptsize(8pt)*S, \footnotesize(9pt)*S, \small(10pt)*S
# Example: \scriptsize at scale=0.68 = 5.44pt (vs 10pt target)
```

### The Fix: Remove `transform shape` + Enforce `\small` Minimum

**Why**: With `transform shape`, even `\small` at scale=0.68 = 6.8pt (below 10pt). The ONLY way to guarantee 10pt minimum is to decouple fonts from canvas scale.

**Per diagram:**
1. Remove `every node/.style={transform shape}` (or equivalent)
2. Replace ALL `font=\tiny`, `font=\scriptsize`, `font=\footnotesize` with `font=\small`
3. Increase `scale` from 0.65-0.70 → 0.80-0.95 (nodes are now full-size, need more coordinate space)
4. Reduce `minimum width`, `text width` values (nodes were oversized for scaled rendering)
5. Adjust coordinates where nodes would overlap at new sizes
6. Verify no frame boundary overflow

### File Segmentation for Parallel Editing

**Problem**: Multiple agents editing one tex file causes Edit tool conflicts. JSON patch files have ~0% match rate on 3000+ line files.

**Solution**: Split the file at frame boundaries into N segment files. Each agent edits its own segment. Reassemble by concatenation.

```bash
# Split: python script that finds \begin{frame} boundaries
# Assign segments to agents (non-overlapping)
# Each agent edits its segment file directly
# Reassemble: cat header.tex seg_01.tex seg_02.tex ... footer.tex > output.tex
```

**Mandatory default**: use `split_frames.py` for all multi-frame fix batches (when 2+ frames need fixes). This prevents Edit tool conflicts and enables true parallelism. Sequential single-agent editing only for single-frame fixes.

### Convergence Gates (font-specific)

| Gate | Condition |
|---|---|
| G1 | 0 compile errors |
| G2 | Page count ±5 of baseline |
| G3 | `grep -c 'transform shape'` = 0 in TikZ environments |
| G4 | `grep -c 'font=\\tiny\|font=\\scriptsize\|font=\\footnotesize'` = 0 in TikZ environments |
| G5 | 0 HIGH visual defects (overflow, collision from larger nodes) |

### Production Data (Week 8 Wednesday, 2026-02-25)

| Metric | Value |
|---|---|
| Diagrams with `transform shape` | 37 of 45 |
| Worst effective font | 3.7pt (`\tiny` at scale=0.62) |
| Fixer agents (parallel, file segmentation) | 10 |
| Audit agents (background, 20 batches) | 20 |
| Iterations to converge | 2 |
| Final page count | 207 (baseline 205, +2) |
| Compile errors | 0 |

### Production Data (Week 10, 2026-03-11)

| Metric | Value |
|---|---|
| Initial TikZ diagrams | 9 |
| Visualization gaps found | 12 (concept frames with no visual) |
| Diagrams added | 12 (funding gravity, cascade, bar chart, weekend diverge, collocation, Glosten-Milgrom, quote flickering, slippage exploit, PD spectrum, scheduler wars, routers flow, scatter plot) |
| Visual defects fixed | 6 (bar chart overlap, PD spectrum clipping, edge label overlap, cascade label overlap, AMM evolution clipping, slippage overflow) |
| Key anti-pattern discovered | `text width` in cm + `scale` on coordinates causes box overlap when physical width > scaled spacing |
| Key anti-pattern discovered | `step` is a reserved TikZ key — style naming conflict |
| Audit agents (background, 5 batches) | 5 |
| Iterations to converge | 3 |
| Final page count | 71 (baseline 68, +3 from new diagrams) |
| Compile errors/warnings | 0 |

---

## Performance Profile

### General Audit-Fix (from production, 2026-02-23)

| Phase | Agents | Wall Time | Context Lines |
|-------|--------|-----------|---------------|
| Audit (20 agents, ~3 frames each) | 20 | ~3 min | ~20 lines |
| Merge + validate | 0 | ~10 sec | ~5 lines |
| Fix (10 agents, 1-3 frames each) | 10 | ~2 min | ~10 lines |
| Apply patches | 0 | ~5 sec | ~5 lines |
| Re-compile + render | 0 | ~2 min | ~5 lines |
| Re-audit (4 agents, 3 frames each) | 4 | ~3 min | ~5 lines |
| **Total per iteration** | **34** | **~10 min** | **~50 lines** |

### Font Normalization (from production, 2026-02-25)

| Phase | Agents | Wall Time | Context Lines |
|-------|--------|-----------|---------------|
| Font fix (10 agents, file segmentation) | 10 | ~5 min | ~10 lines |
| Re-compile + render | 0 | ~2 min | ~5 lines |
| Font audit (20 agents) | 20 | ~3 min | ~20 lines |
| Defect fix (10 agents, direct edit) | 10 | ~4 min | ~10 lines |
| Re-compile + verify | 0 | ~2 min | ~5 lines |
| Manual fix (5 worst frames) | 0 (main agent) | ~10 min | ~50 lines |
| **Total (2 iterations)** | **70** | **~25 min** | **~100 lines** |

Compare: 20 foreground agents would consume ~10,000+ context lines and crash.

---

## Invocation

When user says `/tikz-audit` or mentions TikZ defects:

1. Ask for the tex file path (or detect from context)
2. Run the full convergence loop (Steps 0-9)
3. If font-size violations detected (P29), run the Font-Normalization Sub-Protocol
4. Iterate until G3+G4 pass or G6 triggers (max 10 iterations — escalate only if defect count stops decreasing for 2 consecutive iterations)
5. Present final defect summary to user
6. Commit with descriptive message
