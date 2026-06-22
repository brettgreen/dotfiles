# Paper-to-Lecture Lessons

Accumulated lessons from production use. Each lesson follows the format:
`### PTL-NNN: Title` + Situation + Principle + Date

These lessons are injected into sub-agent prompts at relevant steps.

---

<!-- Lessons will be appended below this line -->

### PTL-001: Agent-to-agent, not human-to-human
Situation: Built install.sh (bash script) for skill distribution. User pointed out recipients should not run shell commands — their Claude Code should handle everything.
Principle: When packaging tools for distribution between Claude Code users, all setup instructions should be in markdown that Claude reads and executes, not bash scripts that humans run. Minimize human steps to: unzip + type the slash command. Everything else is agent work.
Date: 2026-03-10

### PTL-002: Self-test before first use
Situation: Cold-start test revealed the install script had a path normalization bug. Without a self-test mode, users would only discover issues mid-pipeline.
Principle: Every portable skill should have a --selftest that verifies file integrity, dependencies, and template compilation without requiring any input data. Run this on installation, not on first real use.
Date: 2026-03-10

### PTL-003: ${CLAUDE_SKILL_DIR} for all bundled paths
Situation: All bundled file references used bare relative paths (e.g., `prompts/paper_to_notes.md`). On another machine, Claude resolved these relative to the user's working directory, not the skill directory.
Principle: Every reference to a file inside the skill package must use `${CLAUDE_SKILL_DIR}/` prefix. Claude Code provides the skill's base directory in the system context as "Base directory for this skill: ...".
Date: 2026-03-10

### PTL-004: Bundle quality-critical dependencies, don't reference them
Situation: Shipped skill without the tikz-audit convergence loop. Friend's Claude skipped it because it wasn't in the package. Inline description in SKILL.md was too vague — Claude generated a lightweight 3-agent audit instead of the full 20-agent convergence loop.
Principle: If a dependency is critical for output quality, bundle it inside the skill (deps/) AND make the SKILL.md reference it with explicit file paths and non-negotiable language ("MANDATORY — do NOT skip"). Never assume the recipient has sibling skills installed.
Date: 2026-03-11

### PTL-005: Cold-start test every distributable
Situation: CLAUDE.md compile test had wrong placeholder names (%%SECONDARY_RGB%% instead of %%GREEN_RGB%%, missing %%TOPIC%%, double \begin{document}). Would have failed silently on every recipient's machine.
Principle: Before shipping any skill package, run a full cold-start simulation: unzip to temp dir, follow CLAUDE.md instructions literally, verify every path resolves, every compile test passes. Placeholders are the #1 source of cold-start failures.
Date: 2026-03-11

### PTL-006: Scale vs physical-cm interaction in TikZ
Situation: Week 10 PD spectrum diagram used `text width=2.8cm` on nodes at scaled coordinates (scale=0.58). Nodes physically 2.8cm wide but spaced only 2.15cm apart in physical space. Result: boxes overlapped and clipped each other's text for 3 fix iterations.
Principle: Never mix `text width=Ncm` (physical) with `scale=S` (coordinate-only). Either (a) remove scale entirely and position everything in physical cm, or (b) compute physical spacing as `coordinate_gap * scale` and ensure `text width < physical_spacing * 0.9`. The safe default: drop scale, use direct cm coordinates.
Date: 2026-03-11

### PTL-007: Visualization gaps are the #1 slide quality issue
Situation: Week 10 initial slides had 9 TikZ diagrams. Audit found 12 concept-introducing frames with no visual. Adding 12 diagrams was the single biggest quality improvement — bigger impact than fixing all the existing TikZ defects combined.
Principle: Run visualization coverage audit BEFORE TikZ quality audit (Wave 1.5 in pipeline). Adding diagrams to bare concepts changes the slide count and layout, so doing it after TikZ fixes wastes iterations. The concept inventory from the story arc (Step 3) drives this audit.
Date: 2026-03-11

### PTL-008: Reserved TikZ names cause silent failures
Situation: Named a style `step` which conflicts with TikZ built-in `step` key. LaTeX compiled without error but the style was silently ignored. Similarly, `\ding{55}` fails without `pifont` package — prefer `$\times$`.
Principle: Before naming any TikZ style, check against TikZ reserved names (step, draw, fill, node, path, etc.). Use descriptive compound names: `stepbox`, `stepnode`, `flowstep`. For symbols, prefer math mode over packages that may not be loaded.
Date: 2026-03-11

### PTL-009: Projection-readable color saturation
Situation: Weekend Funding Timeline band labels used StanfordRed!40 for +/-3% annotations. Unreadable on projector. Changed to StanfordRed!70. Similarly, labels using light tints of any color (below 50% saturation) disappear at projection distance.
Principle: Any colored label or annotation in TikZ must use >= 70% saturation (e.g., StanfordRed!70, not StanfordRed!40). Black text is always safe. Test by viewing at 50% zoom — if hard to read on screen at 50%, it's invisible on a projector.
Date: 2026-03-11

### PTL-010: Physical clearance formula for scaled TikZ
Situation: AMM Evolution transition labels at y=1.6 appeared safe (1.6 units above box centers). But at scale=0.58 with minimum height=1.8cm, the physical clearance was only 0.028cm — labels sat directly on box edges. Fixed by computing: physical_position = coordinate * scale, then checking against physical_node_height / 2.
Principle: When auditing or fixing label positions in scaled TikZ, always compute physical distances: physical_y = coordinate_y * scale. Compare against physical node extents (minimum height/2, text width/2 — these are NOT scaled). Target >= 0.3cm physical clearance. The formula: clearance = (label_coord - box_edge_coord) * scale - (node_physical_height / 2). If < 0.2cm, it's a defect.
Date: 2026-03-11

### PTL-011: Fix-creates-new-collision — always check neighbors
Situation: "FROZEN at Friday close" label at (7, -1.5) collided with the index line. Moved to (7, -0.7) — immediately collided with the "Sun" time marker at x=7. Had to move again to (5.5, -0.8) which is between Sat (x=4) and Sun (x=7), avoiding all markers.
Principle: Every label repositioning fix must check ALL elements within the destination radius. Specifically: (1) other labels at similar y within 2cm x-range, (2) axis/timeline markers, (3) data points or curve annotations. The fix radius check is: scan all \node commands within ±1.5 scaled units of the new position. If anything is within 0.3cm physical, pick a different position.
Date: 2026-03-11

### PTL-012: Stale-render audit failure — always recompile before visual audit
Situation: tikz-audit ran on PNGs from a previous compilation. The tex file had been edited to add 11 TikZ diagrams, but the PNGs still showed the old text-only frames. The audit converged to 0 defects while all 11 new diagrams had overlapping issues.
Principle: Before any visual audit, verify that the PDF was compiled from the CURRENT tex source. Check: PDF mtime > tex mtime. If not, recompile. Never trust existing PNGs without verifying freshness.
Date: 2026-03-11

### PTL-013: Source-code clearance check — catch overlaps before rendering
Situation: All 11 overlapping diagrams could have been detected from source code alone by computing physical_gap = coord_gap * scale and comparing to text_width / minimum_width. No PNG needed.
Principle: Add a source-code pre-check step to tikz-audit that computes physical clearances algebraically. Flag physical_gap < box_width + 0.3cm as CRITICAL before even rendering. This catches the #1 defect class (PTL-006) at creation time, not audit time.
Date: 2026-03-11

### PTL-014: Arrow-through-label — reposition labels away from arrow paths (never fill=white)
Situation: After fixing scale-vs-physical-width overlaps on 11 slides, labels like "reprice" (slide 12), "deploy" (slide 34), "Widen spread or deny" (slide 37), and "Quoted: 0.3 bps" (slide 61) had arrow lines cutting through the text. Initial fix used fill=white to mask the arrow — user corrected this: fill=white is a hack, not a fix. The right approach is to reposition the label so it doesn't intersect the arrow at all.
Principle: When a label overlaps an arrow path, REPOSITION it — don't mask with fill=white. For edge labels on arrows: use separate `\node` at explicit (x,y) coordinates above the arrow path, NOT `midway, above=Npt` (any pt value risks grazing). For standalone labels near arrow endpoints: ensure >= 0.5cm physical gap from arrow tip to text edge. The audit must flag arrow-through-label as a visual defect (requires rendered PNGs, not source-code-only). Labels with `right`/`left` anchoring near diagonal arrows are the #1 offender. Also check that labels at box boundaries have >= 0.3cm physical clearance from box edges.
Date: 2026-03-11

### PTL-015: Minimum physical clearance for label offsets — never trust small pt values
Situation: Fixed arrow-through-label defects on slides 34, 36, 61 using `above=5pt`. The audit marked them fixed ("label is above arrow"). But 5pt = 1.75mm, while `\tiny` text height = 6pt (2.1mm) and arrowhead extent = 3pt (1mm). Net clearance: 5 - 3(text half) - 3(arrowhead) = -1pt. The "fix" still overlapped. Required a second round: separate \node at explicit coords (slide 34), moving text 1+ coordinate units from arrow endpoints (slide 36), relocating annotations to uncrowded regions (slide 61).
Principle: Never use small pt offsets (`above=5pt`, `right=3pt`) for labels near arrows. The minimum clearance formula is: `offset >= text_height/2 + arrowhead_extent + 3pt margin`. For `\tiny` (6pt): offset >= 3+3+3 = 9pt minimum. For `\scriptsize` (8pt): 11pt. For `\small` (10pt): 13pt. **Preferred approach**: always use separate `\node` at explicit (x,y) coordinates computed to clear the arrow path by >= 0.3cm physical. For arrow endpoints near text nodes: `physical_gap = |endpoint_coord - text_coord| * scale - text_physical_height/2`. Must be >= 0.3cm. For annotation regions: flag any area with 3+ text nodes within 1cm physical radius as CROWDED — spread them to separate regions.
Date: 2026-03-11

### PTL-016: Label text extent must clear ALL neighboring elements, not just arrows
Situation: On page 6 (observation patterns), "N₀ units" label at x=5.2 overlapped with legend box starting at x=6.0. On page 12 (pipeline), arrow labels at y=0.6 sat inside box vertical extent (box top at ~y=0.8). PTL-014/015 only addressed arrow-to-label clearance, not label-to-box or label-to-legend clearance.
Principle: Before placing any label \node, compute its physical text extent (width x height at the given font size and scale). Then check clearance against ALL elements within that extent — boxes, other labels, legend items, arrows, braces. The clearance check is: `gap = |element_edge_coord - label_edge_coord| * scale`. Must be >= 0.3cm for every neighboring element. This generalizes PTL-015 from "labels near arrows" to "labels near anything."
Date: 2026-03-12

### PTL-017: Inter-element labels must fit within the physical gap
Situation: On page 12, "debiased moments" text (~3 tikz units wide) was centered in the 1.6-unit gap between Step 2 and Step 3 boxes. The text extended past both box edges. The generation agent placed the label "above the arrow" without checking whether the text would physically fit.
Principle: When placing a label between two elements (above an arrow connecting boxes), verify: `label_physical_width <= gap_physical_width - 0.4cm margin`. If the label doesn't fit, either (a) widen the gap by increasing inter-element spacing, (b) shorten the label text, (c) place the label further above/below to clear both elements, or (d) use a line break. For pipeline diagrams specifically: inter-box gap must be >= `max(label_text_width) + 0.5cm` at the given scale.
Date: 2026-03-12

### PTL-018: Minimum visual size for quantitative chart elements
Situation: On page 27 (bar chart), beta=-0.006 mapped to a bar of 0.06 tikz units — invisible at scale=0.82 (physical height: 0.05cm). Students could not see whether the bar was above or below zero. The chart also had bars with height 0.23 units (barely visible) while other bars were 1.28 units tall — a 20:1 ratio.
Principle: Every bar, line segment, or data point in a TikZ chart must have a minimum physical height/length of 0.25cm (visible on a projected slide). Scale coefficients so that `min_bar_height * scale >= 0.25cm`. For bar charts: if the data range ratio (max/min non-zero bar) exceeds 10:1, consider using a broken axis, log scale, or separate panels. Stars/annotations must have >= 0.3cm clearance from bar endpoints.
Date: 2026-03-12

### PTL-019: Table floating-label boundary overflow
Situation: Frame 2 of the risk_aversion demo_run_2 lecture — "constant!" and "risky" annotation nodes were placed to the right of a tabular environment using floating LaTeX text. These nodes ended up outside the slide's right boundary. The tikz-audit did not flag them because the coordinate positions appeared locally valid (they were placed as text, not as TikZ nodes with checkable coordinates).
Principle: Any node used as a side-annotation to a table, or as a floating label near non-TikZ content, must be placed inside an enclosing `tikzpicture` as an explicit `\node` at (x,y) coordinates verified inside the slide safe zone: x ∈ [-6.5, 6.5]cm, y ∈ [0.2, 7.8]cm. Never rely on LaTeX text positioning (e.g., `\hspace`, `\makebox`, column padding) for diagram annotations — always use TikZ nodes with explicit coords. At audit time: grep all `\node` commands in TikZ environments and verify coordinates are inside the safe zone.
Date: 2026-03-11

### PTL-020: Proof-circuit diagram height budgeting
Situation: Frame 12 of the risk_aversion demo_run_2 lecture — a 5-box proof circuit (boxes arranged in a vertical chain with arrows) plus an "Easy direction" footer block exhausted the frame body height. The last overlay's content clipped into the beamer footer bar. Three tikz-audit iterations failed to converge because each iteration applied coordinate nudges without checking the total layout height constraint. The root cause was structural (diagram too tall for one frame), not a coordinate error.
Principle: Before generating any frame with 4+ connected proof/logic boxes, compute total_height = (max_y - min_y) × scale. Must be < 5.5cm to leave room for mechanism/keyinsight box + beamer footer (beamer body ≈ 6.0cm total). If total_height ≥ 5.5cm: (a) arrange in 2 rows (3 boxes top + 2 bottom) instead of a vertical chain — this halves the height while preserving all connections, or (b) split the proof into two frames. Document the height calculation in the `% === CLEARANCE ===` block. When the audit finds "proof diagram height overflow" (Defect #16), the fix is STRUCTURAL (layout change), NOT coordinate nudging.
Date: 2026-03-11

### PTL-021: Embed empirical figures, redraw conceptual ones
Situation: 92-page empirical finance paper (Filipovic, Pelger, Ye 2023) has 19 main-text figures (heatmaps, factor loadings, correlation matrices, time series) and 3 tables. All are publication-quality. Redrawing any heatmap or factor loading curve in TikZ would be error-prone and lose data fidelity. But conceptual diagrams (flowcharts, timelines) should still be TikZ for overlay progression.
Principle: For empirical papers, embed complex data visualizations directly using `\includegraphics[page=N, trim=L B R T, clip]{material/paper.pdf}`. Reserve TikZ for conceptual diagrams that benefit from progressive reveal. Decision rule: if the figure has >20 data points or uses color gradients/continuous scales, embed it. If it is a flowchart, timeline, or simple comparison, redraw as TikZ. Always add `\keyinsight{}` after embedded figures — a figure without explanation is a failed frame.
Date: 2026-03-12

### PTL-022: compile_check.sh must resolve \input{} and detect convenience macros
Situation: compile_check.sh searched only the master .tex file (5 lines of \input commands). G5 (coverage), G6 (pedagogy metrics), G7 (embed quality) all showed 0 because all content lives in act*.tex files. Additionally, `grep -c` exits with status 1 when count is 0 but still outputs "0" — the `|| echo "0"` fallback appended a second "0", causing `syntax error in expression` in bash arithmetic. Finally, G7 only matched `\includegraphics[...page=]` but 16 of 22 embeds used the `\paperfigure{}` convenience macro.
Principle: (1) Any content-searching validation script must inline `\input{}` references before searching — use awk to create a combined temp file. (2) Replace `grep -c ... || echo "0"` with `grep -c ... || true` plus `${VAR:-0}` default — this handles both zero-match and file-not-found cases without corrupting the value. (3) When adding convenience macros (like `\paperfigure`), update ALL downstream validators to match both the raw command and the macro. The gate that doesn't know about the macro is a silent false-negative.
Date: 2026-03-12

### PTL-023: Scale moves node centers but does NOT resize nodes — the #1 TikZ overlap cause
Situation: Week 11 pipeline-summary slide had 4 boxes at x=0, 3.5, 7.2, 11 with minimum width=2.8cm at scale=0.65. Centers were at physical x=0, 2.275, 4.68, 7.15. But node widths remained 2.8cm (physical), so box 1 right edge (1.4cm) extended past box 2 left edge (0.875cm) by 0.525cm. Five fix iterations tried adjusting positions and minimum widths before identifying the root cause: TikZ `scale` only transforms coordinates, not node dimensions. Same pattern on the open-questions slide (5 doors clipping at scale=0.58).
Principle: The TikZ `scale` key moves node CENTERS but does NOT resize minimum width, minimum height, text width, or font sizes. When computing clearance: `physical_gap = |center2 - center1| * scale - (width1 + width2) / 2`. If < 0, nodes overlap regardless of coordinate spacing. The safest fix: **remove scale entirely and use direct cm coordinates** — then what you specify IS what you get. If scale is needed (for fitting), add `transform shape` to also scale node dimensions: `[scale=0.7, transform shape]`. But prefer no-scale for complex diagrams with many labeled nodes.
Date: 2026-03-12

### PTL-024: Full-deck audit requires computing last-overlay pages
Situation: page_map.py parsed \newlabel from .aux to get frame-to-page mapping, but these give the FIRST overlay page (where \label appears). Verification agents checked wrong pages (e.g., page 50 showed empty "Think First" box instead of full diagram on page 53). Had to compute last overlay = next_frame_first_page - 1.
Principle: For beamer decks with overlays, always verify the LAST overlay page of each frame (where all elements are visible). Compute from the sorted first-page list: last_page(frame_i) = first_page(frame_{i+1}) - 1. Only check pages that contain TikZ diagrams or embedded figures — skip text-only frames. This halves the verification cost.
Date: 2026-03-12

### PTL-025: Paperfigure vertical budget
Situation: A frame with \paperfigure{} has ~1cm left after the figure + caption + keyinsight. figure_height(~4cm) + caption(~0.5cm) + keyinsight_base(~1.2cm) + keyinsight_text_lines * 0.3cm must be < 5.8cm.
Principle: Max 2 lines (~160 chars) in keyinsight arg for paperfigure frames. If interpretation needs more, split to a dedicated insight frame. Never combine \paperfigure with \think{} on the same frame.
Date: 2026-03-13

### PTL-026: Content overflow != overfull box warning
Situation: Beamer silently clips content that exceeds the frame body height (~6.0cm for 16:9). It does NOT emit overfull vbox warnings for this.
Principle: The ONLY reliable detection methods are: (1) PNG rendering + visual inspection, (2) source-code content inventory (compute estimated height per frame). compile_check.sh overfull-box gate (G4) misses this entire defect class. Use frame_content_inventory.py or render_last_overlays.sh.
Date: 2026-03-13

### PTL-027: Paper text != pedagogical slide
Situation: Any frame where >60% of content is quoted/paraphrased paper prose (identifiable by dense paragraphs, passive voice, figure captions pasted as body text, citation-heavy prose) is a "paper intercept" and must be redesigned. This was the #1 defect class in demo_run_3 (7 frames).
Principle: Transform paper intercepts into: 3-4 bullet points + keyinsight box, or embedded figure with 1-line caption. Paper captions belong in lecture notes, not on projected slides.
Date: 2026-03-13

### PTL-028: Frame content inventory gate (Wave 1.25)
Situation: Content overflow detected only at visual audit (Wave 2) after TikZ fixes had already been applied. Fixing overflow changes page count and invalidates prior TikZ coordinate work.
Principle: Run frame_content_inventory.py BEFORE the TikZ audit (Wave 2). It catches content overflow at generation time without rendering. Any frame with estimated height > 5.8cm is HIGH risk. Fix structural issues (split frame, shorten text) before visual audit.
Date: 2026-03-13

### PTL-029: Subagent audit prompts must include the full anti-pattern list
Situation: Demo_run_3 initial audit launched 13 agents that "fixed" slides by using fill=white (explicitly forbidden in PTL-014) and cherry-picked frames instead of checking all. Root cause: agent prompts said "fix TikZ issues" without injecting the anti-pattern list from tikz-audit/SKILL.md. Agents invented their own fix strategies.
Principle: Every subagent prompt for TikZ audit or fix work MUST include: (1) the full anti-pattern list from SKILL.md, (2) the fill=white ban with explanation, (3) the physical clearance formula, (4) explicit instruction to check ALL frames not just a subset. A subagent without the anti-pattern list will reinvent the same bad patterns. Inject these as literal text in the prompt, not as file references the agent may skip reading.
Date: 2026-03-13

### PTL-030: Source-code pre-audit catches 70% of TikZ defects without rendering
Situation: Demo_run_3 full-deck visual audit found 8 TikZ overlap defects. All 8 could have been detected from source code alone by computing physical_gap = coord_gap * scale and comparing to text_width. The fill=white instances (7) were trivially greppable. Total: 15/39 defects (38%) detectable by grep + arithmetic.
Principle: Before any visual rendering, run a source-code pre-audit: (1) grep fill=white inside tikzpicture — must be 0, (2) for each tikzpicture with scale, extract node coordinates and widths, compute physical clearance, flag violations, (3) check for \tiny/\scriptsize/\footnotesize inside tikzpicture. This catches the cheapest defects instantly. compile_check.sh gates G9-G11 automate this.
Date: 2026-03-13

### PTL-031: fill=white grep gate prevents the #1 fix anti-pattern
Situation: 7 fill=white instances found across demo_run_3 act files despite PTL-014 banning it. The ban was in SKILL.md and preamble.tex comments, but not enforced by any automated gate. Agents that didn't read the full SKILL.md used fill=white as a "quick fix" for arrow-through-label overlaps.
Principle: Add a compile_check.sh gate (G9) that greps for fill=white inside tikzpicture environments. Must be 0 to pass. This is the cheapest possible gate (one grep) that prevents the most common anti-pattern. The gate must exclude comments (lines starting with %) and the mseLegend style definition in preamble.tex (which legitimately uses fill=white for legend boxes).
Date: 2026-03-13

### PTL-032: Embedded PDF figure trim requires visual iteration — never guess
Situation: Demo_run_3 pages 102-103 (recession/boom panels), page 108 (complexity premium), and page 110 (IT-VOL) all needed 3-4 trim iterations. Each PDF page has different layout (caption position, panel spacing, text below figures). Initial trim values (8-14cm) always included paper prose or adjacent panels. Only render-verify-adjust cycles converged.
Principle: For \paperfigure and raw \includegraphics[page=N, trim=...], NEVER guess trim values from source code. The mandatory workflow is: (1) start conservative (trim 2.5cm on all sides), (2) render + visually check, (3) increase trim on overflowing sides by 2-3cm per iteration, (4) repeat until only the target panel is visible with no paper text. Budget 2-4 iterations per figure. Paper figure captions and section text are INSIDE the PDF and will appear unless aggressively trimmed from the bottom.
Date: 2026-03-13

### PTL-033: Multi-panel PDF pages must be split into separate frames
Situation: Page 37 of the source PDF had Panel A (Recession) and Panel B (Boom) stacked vertically. Original single frame at width=0.88 showed both panels but clipped Panel B. Splitting into two frames with targeted trim (bottom=17cm for Panel A, top=15.5cm for Panel B) cleanly separated the panels.
Principle: When a PDF page contains 2+ stacked panels, ALWAYS split into separate beamer frames. Each frame uses a different trim to isolate its panel. Trim values: (a) top panel: large bottom trim to cut everything below, (b) bottom panel: large top trim to cut everything above + moderate bottom trim to cut paper caption text. Never try to show multi-panel figures on a single beamer frame — the combined height always exceeds the ~5.8cm frame body budget.
Date: 2026-03-13

### PTL-034: Rotated y-axis labels prevent title collisions in bar charts
Situation: Page 98 (three factors eigenvalue comparison) had "% var" label at top of y-axis (node[above]) colliding with panel title subtitle "(mechanical overlap)" at y=3.6. The [above] anchor pushed the label into the title's vertical space.
Principle: In TikZ bar charts with panel titles above, use `rotate=90, anchor=south` for y-axis labels and place them to the LEFT of the axis (e.g., at x_axis - 0.3). This is standard chart convention and completely avoids vertical collision with panel titles. Never use `node[above]` at the top of a y-axis arrow when there's a panel title above — the two will always compete for the same vertical space.
Date: 2026-03-13

### PTL-035: Visual audit convergence loop must be in the distributable package
Situation: Demo_run_3 defects were only caught by manual render-inspect-fix cycles. The zip package had compile_check.sh (structural gates) but no visual audit automation. Users without the loop would ship slides with invisible overflow, paper text intercepts, and trim-related clipping.
Principle: The distributable package must include a visual_audit_loop.sh script that: (1) compiles, (2) renders all pages as PNGs, (3) runs compile_check.sh structural gates, (4) provides a manifest for visual inspection. The loop script is the OUTER convergence wrapper — compile_check.sh is the inner structural check. Without the visual loop, structural gates give false confidence (they miss all visual-only defects: trim errors, figure overflow, paper text intercepts).
Date: 2026-03-13

### PTL-036: Figure caption text requires 2-3cm extra bottom trim beyond subplot labels
Situation: Pages 30 and 31 of the source PDF had figure caption paragraphs starting ~0.5cm below the subplot (a)-(f) labels. Bottom trim that preserved labels always leaked 2-4 lines of caption text. Required 5 iterations (bottom=3 -> 9 -> 10 -> 13 -> 15cm) to find the right cutoff.
Principle: When trimming bottom of a PDF page with subplot labels + figure caption: the caption starts IMMEDIATELY below the last label row (~0.5cm gap). Budget trim = label_position + 1cm to cleanly cut between labels and caption. If you can see ANY caption text, increase bottom trim by 1cm per iteration. Render the raw paper page at 200dpi first to measure positions before guessing trim values.
Date: 2026-03-13

### PTL-037: Negative visible height silently kills the figure — no LaTeX error
Situation: Frame 29 (Table 1) had trim=2cm 18cm 2cm 10cm. Total trim = 18+10 = 28cm > page height 27.94cm. Visible height = -0.06cm. The figure silently disappeared — no LaTeX error, no warning. The slide showed source citation and bullets but an empty figure area.
Principle: Before applying trim values, verify: bottom_trim + top_trim < page_height (27.94cm for US Letter, 29.7cm for A4). If the sum exceeds page height, the figure vanishes. Add a validation step: extract all trim values, compute visible height, flag any < 1cm as CRITICAL.
Date: 2026-03-13

### PTL-038: Never combine paperfigure + checkpoint on same frame
Situation: Frame 61 (pricing errors bottom panels) had \paperfigure + \checkpoint. The figure (~3cm) + source (~0.5cm) + keyinsight (~1.2cm) + checkpoint (~1.2cm) = ~5.9cm, exceeding the 5.8cm frame body. The checkpoint box was clipped.
Principle: \paperfigure already fills ~4.5cm (figure + source + keyinsight). Adding \checkpoint (~1.2cm) pushes past the 5.8cm limit. Rule: never combine \paperfigure with \checkpoint on the same frame. Move the checkpoint to the next frame or to a dedicated transition frame.
Date: 2026-03-13

### PTL-039: Render paper pages at 200dpi before calibrating trim values
Situation: Trim calibration for 10+ frames required 5-8 iterations each because position estimates were consistently wrong by 1-2cm. Rendering the raw paper pages first (pdftoppm -png -r 200) and visually measuring panel positions would have saved 3-4 iterations per frame.
Principle: Before writing ANY trim values for \paperfigure or \includegraphics, render the target paper page: `pdftoppm -png -r 200 -f N -l N paper.pdf /tmp/page_N`. Visually identify the target panel boundaries in cm (pixel_position / 78.7 = cm from top). Set initial trim with 1cm margin. This reduces trim iterations from 5-8 to 1-2.
Date: 2026-03-13

### PTL-040: Negative vspace before block environments causes title bar overlap
Situation: Frames 10, 12, 53, 54 all had `\vspace{-Npt}` before `\begin{block}{}` which pulled the block's colored background into the red title bar. The overlap was subtle in source but obvious in rendered PNGs — the block header merged visually with the frame title.
Principle: Never use negative `\vspace` before `\begin{block}{}` in beamer. The block background extends upward and will overlap the frame title bar. Use `\vspace{2pt}` (positive) as the safe minimum. Detection: grep for `\\vspace\{-.*\}` immediately before `\\begin\{block\}` in generated .tex files. This is a generation-time rule (R-rule), not just an audit-time check.
Date: 2026-03-13

### PTL-041: Visual convergence loop is the only reliable quality gate
Situation: Source-level checks (compile_check.sh, frame_content_inventory.py) catch structural issues but miss visual defects: paper prose bleeding through figures, keyinsight boxes clipped by footer, block/title overlaps, figures too small. Only rendering every frame as a PNG and visually inspecting catches these.
Principle: After generation and compilation, run a visual convergence loop: compile -> render all frames as PNGs (render_last_overlays.sh) -> parallel visual audit (4 agents, 16 frames each) -> fix defects -> repeat until 0 defects. This loop should be a standard step in the pipeline, not optional. Budget 2-4 iterations for a typical 60-frame deck.
Date: 2026-03-13

### PTL-042: Punchline-first framing for research presentations
Situation: HL retail presentation had research questions ("Market Dynamics", "Retail Performance") without answers. Audience had to wait 15 slides to learn the findings. GPT-5.4 Pro recommended stating main results within the first 5 slides.
Principle: Research presentations (as opposed to lectures) should use punchline-first framing: state the main result on the same slide as the research questions. The audience is evaluating, not discovering. Front-load the answer, then spend the rest proving it. This is the opposite of the cinematic discovery arc used in lectures.
Date: 2026-03-15

### PTL-043: Research question register — welfare and mechanism language
Situation: HL retail presentation used industry labels ("Market Dynamics", "Retail Performance", "Adverse Selection") that sounded like an industry report. GPT-5.4 Pro reframed as "Welfare Incidence", "Retail Welfare", "Mechanism of Wealth Transfer".
Principle: For academic seminar presentations, reframe every research question using welfare, identification, or mechanism language. Each question should map to a specific econometric/theoretical result. Avoid "adverse selection" unless defending the GM mapping — use "mechanism of wealth transfer" for broader evidence about predictable demand generating post-trade drift.
Date: 2026-03-15

### PTL-044: Hook question pattern for title slides
Situation: HL retail title slide had the paper title but no hook. GPT-5.4 Pro recommended making the question ("What is the price of participation?") the dominant element, with the paper title as subtitle.
Principle: The title slide of a research presentation should pose a question the audience knows matters but cannot immediately answer. The question dominates; the formal paper title is secondary. First spoken sentence should expand the hook: "If hedge funds profit, market makers profit, and some retail traders win — who is financing those gains?"
Date: 2026-03-15

### PTL-045: Literature slide as gap argument, not survey
Situation: HL retail slide 2 ("Traditional Literature & The Data Gap") listed 4 generic bullets about microstructure research. GPT-5.4 Pro rewrote as a narrative argument: equilibrium logic → empirical bottleneck → unusual setting.
Principle: The literature slide in a research presentation is an argument, not a survey. Structure: (1) Theory says someone pays, (2) but data cannot tell us who, (3) our setting uniquely solves this. Use question/proposition titles ("Theory tells us someone pays. Existing data cannot tell us who.") instead of generic labels ("Traditional Literature & The Data Gap"). Keep citations in a small footer, not as bullet points.
Date: 2026-03-15

### PTL-046: Present the venue as a laboratory, not a product
Situation: GPT-5.4 Pro flagged that presenting HyperLiquid as a "revolutionary platform" would make the talk sound like a pitch. It should arrive as the answer to a research problem.
Principle: When the research uses a specific venue/platform/dataset, present it as a measurement laboratory or natural experiment, not as a product endorsement. The venue should arrive as the answer to a research problem. Avoid logos, screenshots, or "crypto-native" visual language in the opening slides.
Date: 2026-03-15

### PTL-047: Block-equation overlap — never use vspace{-6pt} or more before display math in blocks
Situation: In a beamer `\begin{block}` containing a `$$...$$` display equation, `\vspace{-6pt}` before the equation pulled the integral formula into the block title bar, creating a visible overlap. The same pattern appeared in 3 slides (act1 frame 10, act3 IT-VOL, act3 T-COM).
Principle: Inside `\begin{block}`, use at most `\vspace{-2pt}` before display math and `\vspace{-4pt}` after. Never use `\vspace{-6pt}` or more aggressive negative spacing before `$$` — beamer block titles have fixed height and the equation will collide. When a block+equation+TikZ+keyinsight stack fills a frame, reduce TikZ scale (to 0.72-0.75) rather than compressing block spacing. Always visually verify the final overlay of any frame with this stack pattern.
Date: 2026-03-16

### PTL-048: Formal definitions and derivations are mandatory in slides
Situation: Generated 122-page beamer deck for MCP literature review. Slides described CR as "if tx is available and slot produces output, tx is included" — a one-line informal paraphrase. Did not show the formal Definition 9 (the hiding game, the valency concept, the mathematical statement). Did not show how resilience 1/5 is derived from the constraint system. User correctly identified this as unacceptable — "it is impossible for me to read, understand the formal meaning, nor do I know how the number is calculated and how it is proved."
Principle: For every paper's core contribution, slides MUST include: (1) Full formal definitions with mathematical statements (Definition N: ..., the complete statement in a block environment). (2) Worked derivation of key parameters (show the constraint system, solve step by step, show why the number is tight). (3) Proof architecture diagram (which lemmas feed which theorems, dependency chain). (4) For multi-property papers, a formal comparison table showing each scenario with payoff functions, not just prose summaries. High-level summaries without formal content are never acceptable — they convey no understanding. This is a HARD GATE in the beamer_generation prompt: every paper section must contain at least one formal definition frame and one derivation/proof-sketch frame.
Date: 2026-03-31

### PTL-049: Definitions-first presentation order
Situation: Presented Garimidi's MCP paper by jumping to the "all-or-nothing insight" without first showing what CR and Hiding formally mean. The insight is meaningless without the definition.
Principle: When presenting any paper, always present formal definitions BEFORE results. The order is: (1) formal definitions (the language), (2) motivating examples/scenarios showing why the definitions matter, (3) protocol/mechanism that achieves the definitions, (4) proof that it works. Never reverse this order. Definitions give readers the context to evaluate everything that follows.
Date: 2026-03-31

### PTL-050: First-principles walkthrough is mandatory for every paper
Situation: Presented Garimidi's MCP paper with formal definitions and high-level summaries. User could not understand how HECC works, what shreds are, why hiding is achieved, or how the constraint system produces 1/5. Asked "assume we don't know anything — build from first principles." The first-principles walkthrough (BFT basics → Reed-Solomon → HECC hiding trick → shreds → VC → full protocol → counting argument for CR → counting argument for hiding → constraint derivation) was far more effective than the formal-definition-first approach alone.
Principle: For every paper with a non-trivial mechanism, slides MUST include a first-principles walkthrough that builds the mechanism step by step from concepts the audience already knows. The walkthrough must: (1) Start from the baseline/status quo ("here's how BFT works today"), (2) Identify the exact problem with the baseline, (3) Introduce each new concept ONE AT A TIME with a concrete example or analogy, (4) Show how the concepts compose into the full mechanism, (5) Walk through the key proof arguments as counting/logical exercises, not just theorem statements, (6) Derive key numbers step by step (constraint systems, thresholds). This is SEPARATE from and IN ADDITION TO formal definition frames (PTL-048). Formal definitions are the mathematical contract; first-principles walkthroughs are the intuition builder. Both are required.
Date: 2026-03-31

### PTL-051: Wave 2 audit must use multimodal visual inspection, not heuristics alone
Situation: demo_run_7 Wave 2 TikZ convergence loop ran orchestrator-driven (no Task subagent tool available). It checked source-code heuristics (clearance blocks, fill=white, font sizes) and visited a sample of pages but missed real visual defects: page 7 had only a Think First box (no body content reveal), page 36 had axis labels colliding with panel-title parentheticals, page 56 had the keyinsight box overlapping the red footer bar and the figure's color bar legend was clipped. All five audit waves declared PASS while these defects remained.
Principle: Heuristic gates (CLEARANCE blocks, grep for fill=white, font-size scans) are NECESSARY but NOT SUFFICIENT. Every Wave 2 must include a visual pass: render every page as a PNG and view at least the pages containing TikZ + the pages with embeds. The orchestrator (or a sub-agent with Read access) must literally Read the PNGs and report defects. If Task tool is not available, the orchestrator falls back to viewing PNGs in 8-10 page batches itself. NEVER declare Wave 2 PASS with only heuristic checks. Add a Wave 2.5 "visual smoke pass" gate to SKILL.md that requires rendered-page inspection.
Date: 2026-04-29

### PTL-052: Wave 1.25 overflow fixer must enforce a "minimum body content" floor
Situation: demo_run_7 Wave 1.25 second-pass fixer was tasked with reducing 26 HIGH-overflow frames in act1.tex from 6.6-8.7cm down to ≤ 5.8cm. Fix recipes included "move leading body paragraphs to \note{}", "trim mechanism/keyinsight to one sentence", "move keyinsight to \note{} on \think{}-bearing frames". The fixer over-applied: page 7 (Frame 6 of act1, "Why exactly six rotational DOFs") ended up with ONLY the Think First box on slide and nothing else — no answer, no diagram, no mechanism. The think prompt asks the question and the slide reveals nothing on the way to the next frame. Pure dead air.
Principle: Every frame body MUST have at least one substantive content element BESIDES the Think First box. Acceptable substantive elements: \begin{block}, display equation, \mechanism{}, \keyinsight{}, \paperfigure{}, \begin{tikzpicture} with ≥ 2 nodes, itemize with ≥ 2 items. A frame with only \think{} + \pause + (nothing visible at last overlay) is a CRITICAL defect. Wave 1.25 fixers must validate: after the fix, the LAST overlay of each frame contains ≥ 2 elements (think + body), not just 1. Add this gate to frame_content_inventory.py: detect "answer-on-note" pattern where think-prompt body got moved to \note{} leaving the slide empty.
Date: 2026-04-29

### PTL-053: Paperfigure footer-clearance check beyond keyinsight char count
Situation: demo_run_7 page 56 (Fig 4 sky map embed via \paperfigure) had the keyinsight box overlapping the red footer bar at the bottom of the slide. PTL-025's "≤ 160 chars in keyinsight" budget was respected (the keyinsight was 158 chars, 2 lines), but the figure itself was tall (a Hammer-Aitoff projection at width=0.78\linewidth = ~5.0cm vertical) and the cumulative stack figure(5.0) + caption(0.5) + keyinsight base(1.2) + 2-line text(0.6) = 7.3cm — well over the 5.8cm body budget. The earlier height heuristic in frame_content_inventory.py uses ~5.0cm for paperfigure but actual height varies dramatically with figure aspect ratio.
Principle: \paperfigure budget must be aspect-aware. Compute actual figure_height from the source paper PDF's page region (after applying the trim values) and the chosen width. Formula: figure_height = (page_height - top_trim - bottom_trim) * (chosen_width / page_width_after_trim). Then enforce: figure_height + caption(0.5cm) + keyinsight(1.2 + 0.3 * lines)cm + 0.5cm footer-clearance < 5.8cm. If too tall: split into a dedicated insight frame following the figure (PTL-038 generalized) OR reduce width. Add aspect-aware computation to paperfigure_budget_check.py.
Date: 2026-04-29

### PTL-054: Embedded figure axis-legend / color-bar visibility check
Situation: Wave 1.75 caught fully-invisible figures (where trim cropped the figure entirely showing paper body text) but missed partially-cropped figures: page 56's color bar legend on the right side was visibly clipped (gradient bar present but tick labels chopped), and page 60's right edge had the right-side legend partially cut. The figures themselves rendered correctly; the legend/colorbar was a casualty of trim values that targeted only the main figure region.
Principle: Wave 1.75 audit must explicitly check for axis-legend/colorbar/legend-key visibility separately from "figure visible". Audit rule EF-11 (NEW): for every embedded figure, identify whether the source paper page has a side legend or color bar; if so, verify after trim that ≥ 90% of the legend's tick labels are visible in the rendered output. If not, widen the corresponding side trim by 1-2cm. Visual-only check; no source-code shortcut. Add to visualization-audit.md EF rules table.
Date: 2026-04-29

### PTL-055: TikZ axis labels must never use [above] anchor near a panel title
Situation: demo_run_7 page 36 ("What goes wrong if you test μ_α* and μ_δ separately") had a side-by-side TikZ comparison: left panel "Separate test (axis-aligned box)" + right panel "Joint χ²μ ellipse (ρ=−0.7)". Each panel had y-axis label "$\mu_\delta/\sigma$" placed via `node[above]` at the top of the y-axis arrow, while the panel title was a regular `\node` above the axis. Result: the axis label and panel title's parenthetical text rendered at the same vertical y-coordinate, overlapping. Visible as garbled text "test_(\mu_\delta/\sigma..." and "ellipse_(\rho..." in the rendered output.
Principle: In any TikZ panel with a panel title above and a y-axis, the y-axis label MUST be rotated 90° and placed to the LEFT of the y-axis (e.g., `\node[rotate=90, anchor=south, left=2pt of axis_top]`). NEVER use `node[above]` at the y-axis top when a panel title exists above — the two will compete for the same vertical band. This generalizes PTL-034 (rotated y-axis labels in bar charts) to ALL panel-title TikZ. Add to visualization-audit.md TikZ rules: "Rule 12 (NEW): Y-axis labels in panel-titled diagrams must use rotate=90 + left placement."
Date: 2026-04-29

### PTL-056: Final visual smoke test (Wave 2.5) before declaring deck shippable
Situation: After 5 audit waves declared PASS in demo_run_7, the user opened the PDF and immediately saw multiple defects on the first few pages they checked. Each individual wave (1.25, 1.5, 1.75, 2) had a narrow scope and used heuristics + sampled visual checks. No wave was responsible for "is the deck visually coherent overall?" — that question fell through the cracks.
Principle: Add a Wave 2.5 "Final Visual Smoke Test" gate BEFORE declaring step6_slides complete. The smoke test: render the deck at 150 dpi; the orchestrator (or a dedicated background agent with Read access) views (a) the title slide, (b) the first frame of each act, (c) the closing/decision frame of each act, (d) every frame containing \paperfigure, (e) every frame at "MEDIUM" risk by frame_content_inventory.py. Minimum coverage: ~30 representative pages. Any visible defect (label overlap, footer overlap, empty body, cropped legend) blocks PASS. This gate is cheap (one render + ~30 PNG views) and catches the failure mode where multiple narrow audits each PASS but the deck has visible problems. Add to SKILL.md as Wave 2.5.
Date: 2026-04-29

### PTL-057: Audit orchestrator architecture — graceful fallback when Task tool unavailable
Situation: demo_run_7 Wave 2 orchestrator agent reported "Task subagent tool was not available in this session, so audit and fix waves ran orchestrator-driven (sequential) rather than as the parallel background-agent pattern the SKILL.md prescribes". It still produced output but missed defects parallel multi-PNG inspection would have caught. The orchestrator-driven path is fragile: a single agent inspecting 37 tikzpictures sequentially gets context-fatigue and skims later frames.
Principle: Every audit-wave SKILL spec must define BOTH a parallel-architecture path (preferred) AND an explicit sequential-fallback path (when Agent/Task tool is unavailable). The fallback path MUST include: (a) explicit batching (e.g., view 8-10 PNGs per Read call cycle, then write defects to a file before context fills), (b) a "checkpoint" requirement (every N pages, write progress to disk so a watchdog kill leaves recoverable progress), (c) explicit "re-render after each fix wave to re-bound visual context" requirement. Add to deps/tikz-audit/SKILL.md and visualization-audit.md.
Date: 2026-04-29

### SM-058: Skill renamed to slide-making + Stanford HTML standard codified
Situation: User pushback on trade-map v1 decks: "the slides have way worse standard compared to what we create for hyperliquid". v1 used Marp markdown with bullet-list-heavy slides. User pointed at the Stanford FDCI / Governance Summit "Price of Participation" deck as the bar — reveal.js, Stanford Cardinal palette, Playfair Display + DM Sans typography, inline SVG diagrams on every slide, `fragment fade-in` build-ups, Think-First → Reveal pedagogy, story-arc structure (hook → news hook → question → mechanism → numbers → connections → punchline). Built trade-map District 1 deck (`trade-map/v2/D1.html`) at this exact standard as proof-of-concept (~17 slides, 5 cities, SVG per slide). User then said: "put that style into our paper to lecture package... condense into one skill, call it slide making."
Principle: The skill formerly known as `paper-to-lecture` is now `slide-making`. It owns three output presets: Beamer (LaTeX, university lectures), HTML-Stanford (default for browser-targeted decks), HTML-generic (legacy fallback). The Stanford HTML standard is codified in three files that future sessions inherit:
- `references/stanford_visual_grammar.md` — palette (#8C1515 Cardinal + Playfair + DM Sans + group colors), component library (`callout-think`, `math-box`, `bigtext`, `bigstat`, `schema-card`, `label-sm`), story-arc structure, do/don't list.
- `prompts/stanford_html_generation.md` — generation procedure, structural contract (10 mandatory section types), component usage matrix, validation gates (0 bullet-only slides; ≥80% slides with inline SVG; ≥2 Think-First reveals; 1 numbers slide; full story-arc).
- `templates/stanford_html_template.html` — copy-paste skeleton (the trade-map D1 deck, 887 lines).
Trigger expansion: skill triggers now include "presentation deck", "governance-summit-style slides", "Stanford-style HTML deck", "build a deck from this topic" — covering both paper-derived and topic-brief-derived decks (e.g., trade-map districts with no upstream paper). The Stanford preset is the recommended default for any HTML output; generic preset retained for non-academic-brand cases.
Date: 2026-05-04
