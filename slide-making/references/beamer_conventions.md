# Beamer Slide Conventions

Technical conventions for LaTeX beamer slides. Applies to all teaching projects.

## Frame Content Budget
- **Max estimated height: 5.8cm** for 16:9 beamer after title bar + footer. Beamer silently clips overflow — no warning emitted (PTL-026).
- **Max per frame with `\pause`:** 1 block + 1 custom box + a few lines. Beamer reserves space for ALL overlay content.
- **Never stack** two custom boxes on one frame. Split instead.
- **Equations in `\underbrace`/`\overbrace`** are vertically expensive. Prefer inline or plain `\[ \]`.
- **`\paperfigure` frames:** No `\think{}` on same frame (CO-1). Keyinsight (arg #4) <= 160 chars (CO-2). No verbatim paper captions > 3 lines (CO-3).
- **Paper intercept ban:** Never paste paper prose verbatim. Transform to bullets + keyinsight (R20, PTL-027).
- **Detection:** Run `frame_content_inventory.py` and `paperfigure_budget_check.py` in Wave 1.25.

## Embedded Paper Figures
- **Multi-panel pages: split into separate frames** (PTL-033). Each frame gets its own trim targeting one panel.
- **Trim values require visual iteration** (PTL-032). Never guess — render and verify. Budget 2-4 iterations per figure.
- **Bottom trim must exclude paper caption text** (PTL-036). Figure captions start ~0.5cm below subplot labels. Budget trim = label_position + 1cm. If ANY caption text visible, add 1cm per iteration.
- **Render paper page first** (PTL-039): `pdftoppm -png -r 200 -f N -l N paper.pdf /tmp/page_N`. Measure panel positions before writing trim values. Saves 3-4 iterations.
- **Validate trim arithmetic** (PTL-037): `bottom_trim + top_trim < page_height` (27.94cm US Letter). If sum exceeds page height, the figure silently vanishes — no LaTeX error.
- **Width budget:** `\paperfigure` at `0.72\textwidth` is the safe default. `0.82\textwidth` is max for single-panel figures. For dense content frames, reduce to `0.60-0.65\textwidth`.
- **Never combine `\paperfigure` + `\checkpoint`** on the same frame (PTL-038). Total exceeds 5.8cm. Move checkpoint to next frame.
- **Detection:** `paperfigure_budget_check.py` catches height overflow; `visual_audit_loop.sh` catches trim errors.

## TikZ Diagrams
- **Preferred: no `scale`, use direct cm coordinates** (PTL-023). This avoids the #1 overlap cause entirely.
- Fallback scale: `0.80-0.95` for complex diagrams, `1.0` for simple timelines (post-P29)
- **Font minimum: `\small` (~10pt).** No `\tiny`, `\scriptsize`, or `\footnotesize` inside TikZ. See P29.
- **No `transform shape`.** Remove `every node/.style={transform shape}` — it compounds scale with font sizes.
- Labels: `\small`, place as separate `\node` at explicit (x,y) coordinates. Never `fill=white` (PTL-014), never `above=Npt` edge labels (PTL-015), never `node[midway,above]` on stacked elements
- **`fill=white` is absolutely banned** inside tikzpicture. Creates visible white rectangles. Reposition elements with coordinate gaps instead. `compile_check.sh` G9 enforces this.
- **Y-axis labels in bar charts:** Use `rotate=90, anchor=south` placed to the LEFT of the axis, never `node[above]` at the axis tip (PTL-034). This prevents collision with panel titles.
- Spacing: 0.6+ units between parallel arrows, 0.8+ units to braces
- Always add `% === CLEARANCE ===` comment block before every tikzpicture:
  ```
  % === CLEARANCE ===
  % scale: S
  % adjacent pairs: (A, B) coord_gap=X, physical_gap=X*S, text_width=Ncm -> PASS/FAIL
  ```
  Physical clearance formula: `physical_gap = coord_gap * scale`. Must be >= `(width_A + width_B)/2 + 0.3cm`. TikZ `scale` moves centers but does NOT resize `text width` / `minimum width`.
- Run `/tikz-audit` skill for comprehensive audit-fix cycles

## Custom Boxes
- `\think{}` — student reflection prompt (ask before revealing)
- `\keyinsight{}` — the takeaway after a reveal
- `\mechanism{}` — "reading the picture" after a TikZ diagram
- `\warning{}` — common misconception or trap
- `\checkpoint{}` — end-of-act summary question
- Use `\par\vspace{3pt}` instead of `\begin{center}...\end{center}` (saves ~10pt)

## Global Spacing (inherit from Week 5 preamble)
- `\addtobeamertemplate{frametitle}{}{\vspace{-6pt}}`
- Block begin/end: `\vspace{-4pt}`
- Itemize spacing: 2pt
- Equation display skip: 6pt
- **Never negative `\vspace` before `\begin{block}`** (PTL-040). Negative vspace pulls the block's colored background into the red title bar. Use `\vspace{2pt}` as the safe minimum. Detection: `grep -n 'vspace{-' *.tex | grep -A1 'begin{block}'`.

## TikZ Overlay Gate (MANDATORY — P25)
Every TikZ diagram must be classified before submission:
- **Pipeline/Process** (A → B → C): MUST have `\pause` or `\onslide` between nodes. Each node revealed one at a time.
- **Comparison** (A vs B): Show one side first, `\pause`, then reveal the other.
- **Single-concept** (one diagram, no flow): May be static IF it contains < 3 connected nodes.
- **Build diagrams** (stacked bar, threshold): Use `\onslide<N>` to add layers progressively.

**Automated check**: After writing any TikZ, run this mental test: "Does this diagram reveal information in the order a student would discover it?" If the answer is no, add overlays.

**Pattern for pipeline overlays:**
```latex
\begin{tikzpicture}[scale=0.70]
  % Step 1: always visible
  \draw[very thick,rounded corners=3pt] (0,1) rectangle (2,3);
  \node at (1,2) {Users};
  % Step 2: revealed on click
  \onslide<2->{
    \draw[-{Stealth}] (2,2) -- (3,2);
    \draw[rounded corners=3pt] (3,1) rectangle (5.5,3);
    \node at (4.25,2) {Mempool};
  }
  % Step 3: revealed on next click
  \onslide<3->{
    \draw[-{Stealth}] (5.5,2) -- (6.5,2);
    \draw[rounded corners=3pt] (6.5,1) rectangle (9,3);
    \node at (7.75,2) {Miner};
  }
\end{tikzpicture}
```

## TikZ Boundary Gate (MANDATORY — P26)
After every compilation, check for boundary violations:
1. Run `pdflatex` and check for `Overfull \vbox` warnings — these indicate content exceeding frame bounds
2. Render TikZ-heavy pages with `pdftoppm -r 200` and visually inspect bottom 50px
3. Any text touching or below the red footer bar = FAIL

**Prevention rules:**
- TikZ `y` coordinates: keep content in `[0.3, 4.5]` range (for 16:9 beamer)
- Node text: always use `text width=Xcm` for labels > 5 words
- After TikZ + keyinsight/mechanism: verify with `\vspace{0.1em}` before the box, not `0.3em`

## Color Convention
| Color | Meaning |
|-------|---------|
| StanfordRed | Bad, loss, informed trader, danger |
| StanfordGreen | Good, success, safe |
| StanfordBlue | Neutral, reference, structure |
| StanfordGray | Background, annotations |

## Overlay Commands in Special Contexts (gotchas)
- **Inside TikZ `\node`**: Use `\only<N-M>{...}`, NOT `\onslide`. `\onslide` causes "Giving up on this path" error.
- **Inside tabular rows**: Use `\uncover<N->{}` on EACH CELL individually, with `\\` OUTSIDE the overlay. Never wrap an entire row (with `&` and `\\`) inside `\onslide` or `\only` — causes `\noalign` error.
- **General rule**: `\onslide` = reserves space on all overlays. `\only` = removes content completely. `\uncover` = reserves space but hides content. In TikZ, only `\only` is safe. In tabular, only per-cell `\uncover` is safe.

## Debugging Overflow
- `\small` does NOT affect beamer `block` environments (Madrid theme overrides)
- `shrink=N` is unreliable — use `\small`, `\footnotesize`, or frame splitting
- TeX log line numbers with `\input` are misleading — trace backward for `(./filename.tex`
- Render the overflowing page with `pdftoppm -f N -l N -png` before editing

## Visual Convergence Loop (MANDATORY — PTL-041)
After compilation, run a full visual audit loop until convergence:
1. Compile: `pdflatex` (twice for overlays)
2. Render: `bash render_last_overlays.sh deck.nav deck.pdf output_dir/` — produces one PNG per frame (last overlay)
3. Audit: Launch 4 parallel agents, ~16 frames each. Each agent reads PNGs and reports PASS/FAIL per frame.
4. Fix: Apply fixes for all FAIL frames
5. Repeat from step 1 until 0 FAIL frames

Budget 2-4 iterations for a typical 60-frame deck. This catches defects invisible to source-level analysis: paper prose bleeding through figures, keyinsight boxes clipped by footer, block/title overlaps.
