---
name: figure-style
description: House style for ALL figures the user asks for (papers, slides, exploration) — Kieran Healy's Data Visualization principles plus final-print-size authoring. Use whenever creating or revising any figure or plot, in any language (MATLAB, R, python), before writing the first line of plotting code.
---

# Figure-Style Skill (Healy best practices, the user's house style)

Follow Kieran Healy, *Data Visualization: A Practical Introduction* (Princeton,
2019). The goal is a figure that reads at a glance in print: direct, labeled,
uncluttered, colorblind-safe, with type at document size.

## Size and type — the non-negotiables

- **Author every figure at its FINAL printed size** in physical units, and
  include it in the document at natural size (`\includegraphics` with **no**
  `width=`). Never author large and scale down — that is how fonts end up
  unreadable. MATLAB: `figure('Units','inches','Position',[1 1 W H])`.
  Defaults: 4.5 × 3.1–3.3 in for a single panel (≈0.7 of a 6.5in text block),
  6.5 in wide for a full-width or two-panel figure.
- **Type scheme (printed points, uniform across a document)**:
  single-panel figures — ticks 9pt, labels/annotations 10pt;
  two-panel figures — one step smaller, ticks 8pt, labels/annotations 9pt
  (panels are half-width, so type steps down with them).
  If a figure must shrink, shrink the canvas, never the font below these.
- After export, verify: the `.eps` `%%BoundingBox` must match the intended
  physical size (1 in = 72 pt). If it does not, the size setting was ignored —
  find out why before shipping.

## Color

- **Okabe–Ito colorblind-safe palette only**: blue `#0072B2`, vermillion
  `#D55E00`, green `#009E73`, plus greys (`[.45 .45 .45]`). Reserve one hue
  per economic object and keep it consistent across figures in a document
  (e.g. the same curve is vermillion in every figure it appears in).
- Shaded regions: the region's hue at low alpha (`FaceAlpha` 0.07–0.12),
  no edge.

## Marks and hierarchy

- **Solid = the operative object** (the envelope, the frontier, the max, the
  equilibrium path). **Dashed/dotted = supporting cast** (losing candidates,
  benchmarks, counterfactuals). One glance should reveal what matters.
- Line widths ~2–2.6 for the operative curve, ~1.1–1.4 for supporting curves.
- Mark special points sparingly: open circles for kinks/rungs, filled markers
  only when they carry meaning. No decorative markers. If an equilibrium or
  threshold needs locating, prefer thin dotted guides to the axes over a fat
  dot.

## Labels

- **Direct labeling over legends**: name each curve on the plot, in the
  curve's own color, next to a stretch where it is unambiguous. Legends only
  when 4+ line styles genuinely collide (e.g. a comparative-statics panel).
- No on-figure titles for paper figures — captions live in LaTeX. (Slides may
  keep titles.)
- Math in labels: use the document's notation exactly (`$\bar\kappa(q^A)$`,
  `$\tilde p(U)$`), LaTeX interpreter.

## Chartjunk

- `Box off`, `TickDir out`, light y-grid only (`GridAlpha` 0.12–0.15), no
  minor grids, no background tinting, no drop shadows.
- Axis limits tight to the data plus label headroom; no dead white space.

## Workflow

1. Compute the data first; cache slow solves (a `_data.mat` or a SOLVE
   section) so styling iterations never re-solve.
2. Author at final size, style per above, export vector (`exportgraphics`
   `ContentType','vector'` for .eps) plus a .png preview.
3. Verify the BoundingBox and view the render before declaring done; show the
   figure inline to the user — they steer off the geometry.
4. Keep one canonical script per figure, named `paper_fig_<name>.m`, living
   in the paper's `figs/` folder, runnable headless top to bottom.

## MATLAB gotchas (learned the hard way)

- Function-file figure scripts cannot be launched with `run()` in `-batch` —
  call them by name, and set `addpath` to solver folders explicitly.
- `Position` in pixels ≠ points; use `'Units','inches'` and physical sizes.
- Octave portability (if needed): RGB triplets not hex names, `print()`
  fallback when `exportgraphics` is absent, `set(ax,...)` not dot-syntax on
  numeric handles.
