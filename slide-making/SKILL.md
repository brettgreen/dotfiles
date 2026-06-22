---
name: slide-making
description: "Build polished slide decks from any source \u2014 academic papers, lecture\
  \ topics, research presentations, or stand-alone teaching content (e.g., trade-map\
  \ district decks). Two output paths: (1) LaTeX Beamer for projector/PDF audiences,\
  \ (2) Stanford-standard HTML/Reveal.js for browser/online audiences. HTML standard\
  \ mirrors the Stanford Governance Summit deck: Cardinal palette, Playfair + DM Sans\
  \ typography, inline SVG diagrams on every slide, fragment fade-in build-ups, Think-First\
  \ \u2192 Reveal pedagogy, story-arc structure (hook \u2192 question \u2192 mechanism\
  \ \u2192 reveal \u2192 punchline). Self-contained pipeline: PDF/topic intake, note\
  \ extraction, story arc design, combined notes, QA, and slide generation. Optional\
  \ Oracle/Codex add-ons documented separately. Replaces /lecture-prep and /paper-to-lecture.\
  \ Triggers: slide-making, paper-to-lecture, lecture from papers, make slides from\
  \ papers, create lecture, paper to slides, turn papers into lectures, teaching slides,\
  \ presentation deck, governance-summit-style slides, Stanford-style HTML deck, build\
  \ a deck from this topic."
argument-hint: '[--config | --step N | --selftest | --sync-agents | --html-stanford
  | --beamer]'
allowed-tools: Bash, Read, Write, Edit, Glob, Grep, Agent, AskUserQuestion
---

# Slide-Making (formerly Paper-to-Lecture)

Build polished slide decks — from a paper, a lecture topic, or a stand-alone presentation brief.

**Package**: 31 files, ~8,300 lines, 47 lessons. Three output paths:

- **Beamer (LaTeX)** — TikZ diagrams, PDF output, projector-ready, university lecture default
- **HTML — Stanford standard** (Reveal.js) — Cardinal palette, Playfair/DM Sans, inline SVG per slide, fragment build-ups, story-arc structure. Default for online/seminar/non-paper decks.
- **HTML — generic** (Reveal.js) — older lighter-weight path, retained for compatibility

The Stanford HTML standard is the recommended path for any deck where the
audience opens slides in a browser (governance summits, internal seminars,
trade-map district tours, paper-to-presentation packages).

## Quick Start

Just type `/slide-making` (or `/paper-to-lecture` — same skill). Claude handles everything:
1. Checks dependencies (`pdftotext`, `pdflatex`) — installs if missing (asks permission)
2. Asks config questions (source: paper or topic brief; arc style; proof depth; theme; audience; output format; ...)
3. Runs pipeline: PDF/brief intake → notes → story arc → **you review the arc** → combined notes → QA → slides
4. Output: compiled PDF in `final_slides/` (beamer) or single HTML file in `html_slides/` (Reveal.js, Stanford or generic)

### Output presets

| Preset | When to pick | Reference |
|---|---|---|
| **Beamer** (LaTeX) | University lecture, projector, PDF handout | `templates/beamer_preamble.tex`, `prompts/beamer_generation.md` |
| **HTML — Stanford** (default for HTML) | Online seminar, governance summit, internal presentation, trade-map tour decks, paper-to-presentation packages | `templates/stanford_html_template.html`, `references/stanford_visual_grammar.md`, `prompts/stanford_html_generation.md` |
| **HTML — generic** | Lightweight fallback (Reveal.js without Stanford palette) | `prompts/html_generation.md` |

The Stanford-HTML path is the recommended default for any browser-targeted deck — palette, typography, and components are codified in `references/stanford_visual_grammar.md`. Read that file before generating any HTML deck.

## Invocation Modes

- No args: check for `config.yml` → if exists, show dashboard + resume; if not, negotiate
- `--config`: re-enter negotiation (overwrite existing config)
- `--step N`: jump directly to step N (1-6)
- `--selftest`: verify skill integrity and dependencies (no papers needed)
- `--sync-agents`: update embedded agent prompts from standalone skills (if available)

---

## Important: Skill Directory

All bundled resources (prompts, agents, templates, references) live inside this skill's directory.
The skill directory is: `${CLAUDE_SKILL_DIR}`

When the instructions below say "Read: `${CLAUDE_SKILL_DIR}/prompts/X.md`", the actual path is `${CLAUDE_SKILL_DIR}/prompts/X.md`.
When they say "Read: `${CLAUDE_SKILL_DIR}/agents/X.md`", the actual path is `${CLAUDE_SKILL_DIR}/agents/X.md`.
And so on for `templates/`, `references/`, `scripts/`.

**Always resolve bundled file paths relative to `${CLAUDE_SKILL_DIR}`, NOT the user's working directory.**

---

## Pre-Flight: Dependency Bootstrap

Before anything else (negotiation, pipeline, selftest), check dependencies silently and fix them:

```
1. Run: which pdftotext
   - If missing: tell user "pdftotext not found — needed for PDF processing"
     then run the appropriate install command (detect OS first):
       - Debian/Ubuntu: sudo apt-get install -y poppler-utils
       - macOS: brew install poppler
     Ask user permission before sudo commands.

2. Run: which pdflatex
   - If missing: tell user "pdflatex not found — needed for slide compilation"
     then run the appropriate install command:
       - Debian/Ubuntu: sudo apt-get install -y texlive-latex-base texlive-latex-recommended texlive-latex-extra texlive-fonts-recommended
       - macOS: brew install --cask mactex
     Ask user permission before sudo commands.

3. If both present: proceed silently (no output).
```

---

## Self-Test Mode (`--selftest`)

When invoked with `--selftest`, run a full integrity check — no papers needed, no user input needed. This verifies the skill works on this machine.

### Checks to run:

1. **Skill directory**: Confirm `${CLAUDE_SKILL_DIR}` resolves. List all files in it.

2. **Bundled files**: Read each of these and confirm they exist and are non-empty:
   - `${CLAUDE_SKILL_DIR}/prompts/paper_to_notes.md`
   - `${CLAUDE_SKILL_DIR}/prompts/proof_extraction.md`
   - `${CLAUDE_SKILL_DIR}/prompts/combined_notes.md`
   - `${CLAUDE_SKILL_DIR}/prompts/notes_qa.md`
   - `${CLAUDE_SKILL_DIR}/prompts/beamer_generation.md`
   - `${CLAUDE_SKILL_DIR}/prompts/html_generation.md`
   - `${CLAUDE_SKILL_DIR}/agents/story-arc.md`
   - `${CLAUDE_SKILL_DIR}/agents/teaching-review.md`
   - `${CLAUDE_SKILL_DIR}/agents/visualization-audit.md`
   - `${CLAUDE_SKILL_DIR}/references/slide_principles.md`
   - `${CLAUDE_SKILL_DIR}/references/beamer_conventions.md`
   - `${CLAUDE_SKILL_DIR}/references/lessons.md`
   - `${CLAUDE_SKILL_DIR}/templates/config.yml`
   - `${CLAUDE_SKILL_DIR}/templates/beamer_preamble.tex`
   - `${CLAUDE_SKILL_DIR}/templates/folder_structure.md`
   - `${CLAUDE_SKILL_DIR}/scripts/compile_check.sh`

3. **Dependencies**: `which pdftotext` and `which pdflatex`

4. **Preamble compile test**: Create a temp directory, copy the preamble template, substitute default theme values (stanford_red), append `\end{document}`, compile with pdflatex. Confirm exit 0 and PDF exists.

5. **Config template test**: Read `${CLAUDE_SKILL_DIR}/templates/config.yml`, verify it has all 7 preference fields and the progress block.

### Output format:
```
=== paper-to-lecture self-test ===
Skill directory: {path}
Files:         29 total, 16/16 critical present
Dependencies:  pdftotext OK, pdflatex OK
Preamble:      compiles (1 page)
Config:        7/7 fields, progress block OK
PTL lessons:   46

Result: READY — type /paper-to-lecture to start
```

If anything fails, report exactly what failed and suggest the fix. Clean up temp files after.

---

## Phase 0: Negotiation

On first run (no `config.yml` in working directory) or with `--config`, present the user with configuration choices. Ask each question using AskUserQuestion, showing the options clearly. The user can accept defaults by pressing Enter or typing their choice.

### Question 1: Papers and Topic (REQUIRED — no default)
Ask: "Which PDF papers should this lecture cover, and what is the topic/title?"
- The user provides: paths to PDF files (relative or absolute) and a lecture title
- If the user gives a directory, scan it for PDFs
- This question has no default — the user MUST answer

### Question 2: Story Arc Style
Ask: "How should the lecture be structured?"
Present these options (default = cinematic):
1. **cinematic** — Central puzzle drives the lecture. Hook → tension → mechanism → resolution.
2. **chronological** — Paper-by-paper with explicit bridge paragraphs between papers.
3. **thematic** — Group results by concept across papers (3-5 themes).
4. **custom** — Describe your own structure.

### Question 3: Proof Depth
Ask: "How much proof detail?"
Present these options (default = key_steps):
1. **sketch** — State result + one-line intuition. Good for survey/overview lectures.
2. **key_steps** — Break proof into steps, show non-obvious steps in full, compress routine steps.
3. **full** — Every step, every derivation. For advanced seminars.

### Question 4: Theme/Colors
Ask: "What color theme?"
Present these options (default = stanford_red):
1. **stanford_red** — Primary: dark red (140,21,21), Accent: navy (0,51,102)
2. **mit_blue** — Primary: crimson (163,31,52), Accent: navy (0,51,102)
3. **chicago_maroon** — Primary: maroon (128,0,0), Accent: dark blue (21,50,81)
4. **minimal** — Black and gray, no color
5. **custom** — Provide your own RGB values

### Question 5: Visualization Density
Ask: "How many diagrams?"
Present these options (default = standard):
1. **minimal** — Only critical diagrams (equilibria, key processes)
2. **standard** — One visual per major concept
3. **maximum** — Every concept gets TikZ; multi-step processes MUST be pipeline diagrams

### Question 5.5: Figure Handling (conditional — ask only if papers contain empirical figures)

After scanning the PDFs in Step 1, if any paper has >= 3 figures/tables, ask:

Ask: "This paper has [N] figures and [M] tables. How should we handle them?"
Present these options (default = embed_when_possible):
1. **embed_when_possible** — Embed complex empirical plots directly from the PDF; redraw simple conceptual diagrams as TikZ. Best for empirical papers with publication-quality figures.
2. **tikz_only** — Redraw everything as TikZ diagrams (current behavior). Best for theory papers.
3. **ask_per_figure** — Show the figure manifest and let you decide per-figure.

If no papers have >= 3 figures, skip this question and default to `tikz_only`.

### Question 6: Audience Level
Ask: "Who is the audience?"
Present these options (default = graduate):
1. **graduate** — Assume math maturity; define only novel objects
2. **undergrad** — Define everything; more examples and intuition frames
3. **executive** — Minimize math; maximize intuition and real-world analogies

### Question 7: Pedagogical Style
Ask: "What teaching style?"
Present these options (default = socratic):
1. **socratic** — Heavy "Think First" prompts, prediction before reveal (12+ interactive prompts)
2. **lecture** — Present results with intuition, efficient coverage (4-6 prompts)
3. **seminar** — Deep technical, frontier questions, critique (2-3 prompts)

### Question 8: Output Format
Ask: "What output format?"
Present these options (default = beamer):
1. **beamer** — LaTeX beamer slides with TikZ diagrams, compiled to PDF. Requires pdflatex.
2. **html** — Single-file Reveal.js slides. Opens in any browser, no LaTeX needed. Best for virtual talks or sharing online.
3. **both** — Generate both formats from the same notes.

### After Negotiation
Also ask for optional course/event info: course name, week/topic label, instructor name, institution, event name, date, duration.

Then write `config.yml` to the workspace using the template from `${CLAUDE_SKILL_DIR}/templates/config.yml`, filling in all user choices. Read the template first, then substitute values.

---

## Pipeline: 6-Step Workflow

### Architecture: Thin Orchestrator

You (the orchestrator) are a **dispatcher**. You:
- Read config and progress
- Launch sub-agents with focused tasks
- Collect results (file paths + summaries only — never full content)
- Update progress tracking
- **Never read full paper text or full slide decks yourself**

This keeps your context clean for 10+ paper lectures.

---

### Step 1: Workspace Setup

1. Create folder structure: `material/`, `notes_raw/`, `lecture_notes/`, `final_slides/`
2. Copy or move PDFs into `material/`
3. Convert all PDFs to text: `pdftotext -layout material/{paper}.pdf notes_raw/{paper}.txt`
4. Update `config.yml` progress: `step1_setup: complete`

---

### Step 2: Paper Processing (PARALLEL — 1 agent per paper)

Read these prompt files first (paths relative to `${CLAUDE_SKILL_DIR}`):
- `${CLAUDE_SKILL_DIR}/prompts/paper_to_notes.md` (the mega-prompt)
- `${CLAUDE_SKILL_DIR}/prompts/proof_extraction.md` (the depth protocol matching `config.proof_depth`)
- `${CLAUDE_SKILL_DIR}/references/lessons.md` (inject any relevant lessons into the agent prompt)

Launch **one Agent per paper** with `run_in_background: true`:

```
Each paper-reader agent receives:
  1. The paper PDF path (agent reads it directly via multimodal)
  2. The full text of ${CLAUDE_SKILL_DIR}/prompts/paper_to_notes.md
  3. The relevant section of ${CLAUDE_SKILL_DIR}/prompts/proof_extraction.md
  4. Config values: proof_depth, audience, pedagogy

Each agent MUST:
  - Write output to notes_raw/{first_author}_{year}_notes.md
  - Return a 5-line summary:
    Line 1: Problem (one sentence)
    Line 2: Model type (game theory / optimization / mechanism design / etc.)
    Line 3: Key results (list theorem/proposition numbers)
    Line 4: Theorem count and proof count
    Line 5: Suggested act assignment (if obvious)

Each agent MUST also (when config.figure_handling != tikz_only):
  - Produce the Figure and Table Manifest (Section 3.7 of paper_to_notes.md)
  - Write manifest to notes_raw/{first_author}_{year}_figures.md
  - Return additional summary line: "Line 6: Figure manifest — N figures (X embed, Y tikz)"
```

**For 3 papers: 3 parallel agents. For 10 papers: 10 parallel agents.**

After all agents complete:
- Collect summaries
- Verify each notes file passes quality gates:
  - Contains notation table (grep for `|` delimited table)
  - Contains theorem ledger
  - Contains numerical example
  - If figure_handling != tikz_only: figure manifest present with embed decisions
- Update progress per paper

---

### Step 3: Story Arc Design (1 agent, sequential)

Read: `${CLAUDE_SKILL_DIR}/agents/story-arc.md`

Launch **one arc-designer agent**:

```
Agent receives:
  1. All paper summaries from Step 2 (NOT full notes — agent reads those itself)
  2. config.story_arc setting
  3. Full text of ${CLAUDE_SKILL_DIR}/agents/story-arc.md

Agent MUST:
  - Read all notes files in notes_raw/
  - Write notes_raw/plan.md
  - Include a CONCEPT INVENTORY section in plan.md: a table of (concept, concept type, expected diagram type) for every new mechanism, equilibrium, tradeoff, timeline, comparison, or process. This inventory drives Wave 1.5 visualization coverage audit.
  - Return: arc outline (~30 lines) with acts, paper assignments, transitions
```

Store the returned arc outline for dispatching Step 3.5.
Update progress: `step3_arc: draft`

---

### Step 3.5: Story Arc Approval (HUMAN GATE — optional, on by default)

**Skip condition:** If `config.yml` contains `arc_review: false`, skip this step entirely and proceed directly to Step 4. The default is `arc_review: true`.

Before proceeding to slide generation, present the story arc to the user for review. This is a **blocking approval gate** — the pipeline does NOT continue until the user approves or requests changes.

**Present to the user:**

1. The arc outline (~30 lines) returned by the story-arc agent
2. The concept inventory table from `plan.md` (concepts × expected diagram types)
3. Key structural decisions:
   - Number of acts and their themes
   - Paper-to-act assignments (which paper content goes where)
   - Transitions between acts (the narrative thread)
   - Puzzle/hook framing (for cinematic arcs)
4. Estimated slide count per act

**Ask the user** (via AskUserQuestion):

```
Story Arc Review — please approve or request changes:

[display arc outline, concept inventory, act structure]

Options:
1. Approve as-is → proceed to Step 4
2. Modify structure → describe changes (reorder acts, merge/split, change emphasis)
3. Change arc style → switch to different arc type (cinematic/chronological/thematic)
4. Adjust scope → add/remove concepts, change proof depth for specific results
5. Skip review for future runs → set arc_review: false in config
```

**If user requests changes:**
- Re-run the story-arc agent with the user's feedback appended to the prompt
- Present the revised arc for another approval round
- Loop until approved (no max iteration limit — this is a human decision)

**After approval (or skip):**
- Write the approved arc to `notes_raw/plan.md` (overwrite draft if changed)
- Update progress: `step3_arc: approved`
- Record approver: append `Approved by: {user} on {date}` to plan.md (or `Auto-approved (arc_review: false)`)

**Why this gate exists:** The story arc determines the entire lecture structure — act boundaries, narrative flow, concept ordering, and visualization targets. Fixing a bad arc after slides are generated wastes all downstream work (Steps 4-6). A 2-minute human review here saves hours of regeneration. Set `arc_review: false` in config to skip if you trust the defaults.

---

### Step 4: Combined Notes (PARALLEL — 1 agent per act)

Read: `${CLAUDE_SKILL_DIR}/prompts/combined_notes.md`

From the arc outline, determine acts and paper assignments.

Launch **one notes-combiner agent per act** with `run_in_background: true`:

```
Each agent receives:
  1. List of paper notes files for its act
  2. notes_raw/plan.md (transitions and arc context)
  3. Full text of ${CLAUDE_SKILL_DIR}/prompts/combined_notes.md
  4. Config values: pedagogy, audience

Each agent MUST:
  - Read the full notes for papers assigned to its act
  - Produce unified lecture notes for that act
  - Write to lecture_notes/act{N}_notes.md
  - Return: file path + content summary (topic, theorem count, Think First count)
```

After all act agents complete:
- Launch one merge agent to combine act files into `lecture_notes/{topic}_lecture_notes.md`
- Ensure cross-act notation consistency
- Update progress: `step4_combined: complete`

---

### Step 5: QA Review (PARALLEL — 1 agent per paper)

Read: `${CLAUDE_SKILL_DIR}/prompts/notes_qa.md`, `${CLAUDE_SKILL_DIR}/agents/teaching-review.md`

Launch **one qa-reviewer agent per paper** with `run_in_background: true`:

```
Each agent receives:
  1. Original paper notes (notes_raw/{paper}_notes.md)
  2. Relevant section of combined lecture notes
  3. Full text of ${CLAUDE_SKILL_DIR}/prompts/notes_qa.md
  4. Full text of ${CLAUDE_SKILL_DIR}/agents/teaching-review.md
  5. Config: pedagogy (for Think First targets)

Each agent MUST:
  - Score on 7 dimensions (1-5 scale)
  - List specific gaps with IDs (GAP-001, GAP-002, ...)
  - Return: scores table + gap list
```

After all QA agents complete:
- If any dimension < 4: launch targeted fix agents (parallel, one per gap)
- After fixes: re-run QA on fixed sections
- Convergence: loop until all dimensions >= 3 (max 3 iterations)
- Write QA log to `notes_raw/qa_log.md`
- Update progress: `step5_qa: complete`

---

### Step 6: Slides (format-dependent)

If `config.output_formats` includes `beamer` (or is not set, defaulting to beamer), run Step 6-Beamer.
If `config.output_formats` includes `html`, run Step 6-HTML.
If both, run them sequentially (beamer first, then HTML from the same notes).

### Step 6-Beamer: Beamer Slides (3-WAVE PARALLEL)

#### Wave 1: Generation (parallel by act)

Read: `${CLAUDE_SKILL_DIR}/prompts/beamer_generation.md`, `${CLAUDE_SKILL_DIR}/references/slide_principles.md`

1. Generate preamble from `${CLAUDE_SKILL_DIR}/templates/beamer_preamble.tex`:
   - Replace `%%PRIMARY_RGB%%` with theme colors from config
   - Replace `%%COURSE_NAME%%`, `%%WEEK_LABEL%%`, etc.
   - Write to `final_slides/preamble.tex`

2. Launch **one slide-writer agent per act** with `run_in_background: true`:

```
Each agent receives:
  1. Combined notes for its act (lecture_notes/act{N}_notes.md)
  2. Full text of ${CLAUDE_SKILL_DIR}/prompts/beamer_generation.md
  3. Full text of ${CLAUDE_SKILL_DIR}/references/slide_principles.md
  4. The generated preamble (for custom commands reference)
  5. Config: audience, proof_depth, pedagogy, viz_density

Each agent MUST:
  - Generate compilable LaTeX frames for its act
  - Write to final_slides/act{N}.tex
  - Return: file path + frame count + TikZ diagram count
```

3. Merge all act files into `final_slides/{topic}_slides.tex`:
   - Include preamble
   - `\input{act1.tex}`, `\input{act2.tex}`, etc.
   - `\end{document}`

4. Compile: `pdflatex -interaction=nonstopmode -halt-on-error {topic}_slides.tex` (2 passes)
5. Fix any LaTeX errors and recompile

#### Wave 1.25: Frame Content Inventory (MANDATORY — do NOT skip)

After compilation succeeds but BEFORE visualization audit, run the frame content inventory to catch vertical overflow. Beamer silently clips overflowing content without warnings (PTL-026), so this is the only reliable detection method at generation time.

**Protocol**: Run `frame_content_inventory.py` and `paperfigure_budget_check.py` on all act .tex files:

```bash
python3 frame_content_inventory.py act*.tex --nav *.nav
python3 paperfigure_budget_check.py act*.tex
```

**Gates**:
- 0 HIGH-risk frames (>5.8cm estimated height)
- 0 paperfigure budget violations (keyinsight >160 chars, \think{} + \paperfigure, etc.)

**Fix recipes**:
- `\paperfigure` + `\think{}` on same frame: move `\think{}` to preceding frame
- Keyinsight > 160 chars: shorten to core message (1-2 sentences)
- Multiple heavy elements: split frame
- Paper prose verbatim: redesign as bullets + keyinsight

**Gate**: Wave 1.25 must pass (0 HIGH, 0 violations) before proceeding to Wave 1.5.

#### Wave 1.5: Visualization Coverage Audit (MANDATORY — do NOT skip)

After compilation succeeds but BEFORE TikZ quality audit, run a visualization gap analysis. This catches missing diagrams early — adding diagrams after TikZ quality fixes wastes iterations.

**Protocol**: Read `${CLAUDE_SKILL_DIR}/agents/visualization-audit.md` and launch the visualization audit agent:

```
Agent receives:
  1. The compiled .tex file
  2. Full text of ${CLAUDE_SKILL_DIR}/agents/visualization-audit.md
  3. Config: viz_density setting
  4. Rendered PNGs of all pages (from Wave 1 compilation)

Agent produces:
  - Concept inventory: list of (frame, concept type, has visual Y/N, expected diagram type)
  - Visual debt list: frames that need diagrams added
  - Bullet-list processes that should be TikZ pipelines
  - Embedded figure count: frames using \includegraphics from source PDFs

**Embedded figures count as valid visuals.** A frame with an embedded paper figure
satisfies the viz coverage requirement for that concept. Do not flag embedded
empirical figures as visual debt.
```

**Action**: For each visual debt item, add the appropriate TikZ diagram type. Use the concept-to-diagram mapping table from `${CLAUDE_SKILL_DIR}/deps/tikz-audit/SKILL.md` (section "Visualization Gaps"). Recompile after adding all diagrams. Only then proceed to Wave 2.

**Gate**: Visual coverage ratio must meet density threshold:
- `minimal`: >= 50% of concept frames have visuals
- `standard`: >= 75% of concept frames have visuals
- `maximum`: 100% of concept frames have visuals

#### Wave 1.75: Embedded Figure Audit (MANDATORY when figure_handling != tikz_only)

After Wave 1.5 confirms visual coverage but BEFORE Wave 2 TikZ audit, audit all embedded figures. Skip this wave entirely if `figure_handling` = `tikz_only` or no `\includegraphics[...page=]` found in the .tex file.

**Protocol**: Read `${CLAUDE_SKILL_DIR}/agents/visualization-audit.md` section "Embedded Figure Quality Rules" and execute the audit loop:

**Step 1: Render and inspect.** Compile the deck. For every frame containing `\includegraphics`:
  - Render that page to PNG (`pdftoppm -f N -l N -r 200`)
  - Launch 1 background audit agent per embedded-figure frame

**Step 2: Per-frame embedded figure audit.** Each agent checks all 10 EF rules:

| # | Check | Severity | How |
|---|-------|----------|-----|
| EF-1 | Figure is readable at projected size | CRITICAL | Visual: axis labels, legends must be legible at 200dpi |
| EF-2 | `clip` option present | CRITICAL | Grep the `\includegraphics` line |
| EF-3 | No page bleed (paper caption/header/footer visible) | CRITICAL | Visual: only intended figure content visible |
| EF-4 | Width <= 0.92\textwidth | MEDIUM | Grep for `width=` value |
| EF-5 | `\keyinsight{}` or `\mechanism{}` present on frame | CRITICAL | Grep the frame |
| EF-6 | Source attribution present | MEDIUM | Grep for "Source:" or figure reference |
| EF-7 | Correct figure embedded (matches manifest) | CRITICAL | Cross-check `page=` number against figure manifest |
| EF-8 | No content cut off (trim too aggressive) | CRITICAL | Visual: all axes, labels, legends fully visible |
| EF-9 | Frame not overcrowded (figure + text fits) | MEDIUM | Visual: no overflow, footer clearance OK |
| EF-10 | Conceptual diagram not embedded (should be TikZ) | MEDIUM | Cross-check manifest Embed? column |

**Step 3: Fix wave.** For each defect:
  - CRITICAL EF-1 (unreadable): increase width or split multi-panel into separate frames
  - CRITICAL EF-3 (page bleed): adjust trim values to crop tighter
  - CRITICAL EF-5 (no keyinsight): add `\keyinsight{}` with interpretation
  - CRITICAL EF-7 (wrong figure): fix `page=` number per manifest
  - CRITICAL EF-8 (content cut off): widen trim values
  - MEDIUM EF-4 (too wide): reduce width
  - MEDIUM EF-6 (no attribution): add source line
  - MEDIUM EF-10 (should be TikZ): replace `\includegraphics` with TikZ diagram

**Step 4: Re-audit.** After fix wave, re-render fixed frames and re-audit.

**Convergence:** Loop Steps 2-4 until 0 CRITICAL and 0 MEDIUM defects (or max 3 iterations on MEDIUM). Max 5 total iterations — escalate if not converging.

**Output:** Write convergence log to `/tmp/embed_audit_log.md`.

**Gate 6b2:** Wave 1.75 must pass before proceeding to Wave 2.

**Architecture reminder**: Use background agents + file-based IPC (write to `/tmp/embed_audit_frame_NN.md`). Same pattern as tikz-audit.

#### Wave 2: TikZ Convergence Audit (MANDATORY — do NOT skip)

This is the production quality gate. Without it, TikZ diagrams will have overlaps, clipping, tiny fonts, and boundary overflow. The slides are NOT done until this converges.

**Embedded-figure-only frames** (frames with `\includegraphics` but no `\begin{tikzpicture}`) are EXEMPT from TikZ audit — there is no TikZ to audit. However, frames with BOTH embedded figures AND TikZ annotations (e.g., callout arrows overlaid on figures) still get the full TikZ audit on the TikZ portion.

**Protocol**: Read `${CLAUDE_SKILL_DIR}/deps/tikz-audit/SKILL.md` and execute the FULL convergence loop (Steps 0-9) on the compiled deck. The bundled Python helpers are at:
- `${CLAUDE_SKILL_DIR}/deps/tikz-audit/enumerate_tikz_frames.py` — frame-to-page mapping
- `${CLAUDE_SKILL_DIR}/deps/tikz-audit/merge_defects.py` — merge parallel audit reports
- `${CLAUDE_SKILL_DIR}/deps/tikz-audit/apply_patches.py` — sequential patch application
- `${CLAUDE_SKILL_DIR}/deps/tikz-audit/split_frames.py` — file segmentation for parallel editing

**Target file**: `final_slides/{topic}_slides.tex`

**Convergence gates** (from tikz-audit SKILL.md):
- G1: 0 compile errors
- G2: Page count within ±2 of baseline
- G3: 0 HIGH defects (full-deck audit, not just fixed frames)
- G4: 0 MEDIUM defects (or max 2 iterations on MEDIUM)
- G5: Defect count decreasing each iteration (else revert to checkpoint)
- G6: Max 10 iterations (escalate only if defect count stops decreasing for 2 consecutive iterations)
- G7: Full-deck re-audit every iteration (not scoped to changed frames)

**P29 enforcement**: If `grep -c 'transform shape'` > 0 in any TikZ environment, or any font smaller than `\small` detected, run the Font-Normalization Sub-Protocol from the tikz-audit SKILL.md. This alone caused 37/45 diagrams to have illegible text in production.

**Architecture reminder**: Use background agents + file-based IPC (write to `/tmp/tikz_audit_batch_NN.md`). NEVER use foreground agents for audit — 20 foreground agents = 10,000+ context lines = context death.

The slides exit Wave 2 ONLY when G1-G10 all pass. **Slides are NOT shippable until this is confirmed.**

**Mandatory delivery check** (before marking `step6_slides: complete` in config.yml):
1. tikz-audit convergence log confirms G1-G10 all passed (0 HIGH, 0 MEDIUM defects on full deck)
2. User spot-check: present a 4-image sample (first frame of each act + most-complex TikZ frame) for visual sign-off before committing. If user identifies any overlap: re-run tikz-audit targeting that frame only.

#### Wave 2.5: Final Visual Smoke Test (MANDATORY — added 2026-04-29 per PTL-056)

After Wave 2 declares G1-G10 PASS, the orchestrator MUST run a final visual smoke test BEFORE marking `step6_slides: complete`. Heuristic gates pass while real visual defects remain (PTL-051): empty frames where Wave 1.25 over-trimmed (PTL-052), embedded-figure footer overlap (PTL-053), partially clipped color bars (PTL-054), TikZ axis labels colliding with panel titles (PTL-055).

**Protocol**:
1. Render the deck at 150 dpi: `pdftoppm -png -r 150 final_slides/{topic}_slides.pdf render_pngs_hi/p`.
2. The orchestrator (or a dedicated background agent with Read-image access) views, at minimum:
   - The title slide (page 1)
   - The first frame of each act
   - The closing/decision frame of each act
   - **Every** frame containing `\paperfigure{}` or `\includegraphics`
   - Every frame at MEDIUM risk by `frame_content_inventory.py` (>5.0cm est. height)
   - Any frame with `\begin{tikzpicture}` containing >= 3 nodes and panel titles
   - 5 random additional frames for spot-check
3. For each viewed page, classify: **PASS / MEDIUM / HIGH / CRITICAL**. CRITICAL examples: empty body, label overlap, footer overlap, cropped legend.
4. **Gate 6c2**: 0 CRITICAL + 0 HIGH visible defects. If any present, dispatch a focused fix agent (Edit-only, no architecture changes), recompile, re-render, repeat.

**Architecture (PTL-057)**:
- **Preferred path**: spawn parallel background visual-audit agents (~5 batches of ~20 pages each) with Read-image access, write defects to `/tmp/visual_smoke_NN.md`.
- **Sequential fallback** (when Agent tool unavailable): orchestrator views PNGs in batches of 8-10 per Read cycle, writes defects to disk after each batch (checkpoint requirement so a watchdog kill leaves recoverable progress).

**Why this gate exists**: demo_run_7 had 5 audit waves all PASS while real visual defects (empty frame on page 7, axis-label overlap on page 36, footer overlap on page 56) remained shippable. The user opened the PDF and immediately saw them. Heuristic + sampled visual checks are necessary but not sufficient — every page that touches non-trivial layout must be eyeballed before declaring PASS.

#### Final validation:

Run `${CLAUDE_SKILL_DIR}/scripts/compile_check.sh final_slides/{topic}_slides.tex --strict {author_names}`

Update progress: `step6_slides: complete`

---

### Step 6-HTML: Reveal.js Slides

When `config.output_formats` includes `html`, generate browser-based slides instead of (or in addition to) beamer.

**No LaTeX required.** The HTML pathway needs zero dependencies beyond Claude Code and a browser.

**Choose a sub-preset:**

- `config.html_style: stanford` (default — recommended for any browser-targeted deck) — Cardinal palette + Playfair/DM Sans + SVG-per-slide + fragment build-ups + Think-First → Reveal pedagogy + story-arc structure. Read `${CLAUDE_SKILL_DIR}/references/stanford_visual_grammar.md` and `${CLAUDE_SKILL_DIR}/prompts/stanford_html_generation.md`. Skeleton: `${CLAUDE_SKILL_DIR}/templates/stanford_html_template.html`.
- `config.html_style: generic` (legacy) — lighter Reveal.js without Stanford palette. Read `${CLAUDE_SKILL_DIR}/prompts/html_generation.md`. Use only when Cardinal palette is inappropriate (e.g., a non-academic brand requirement).

Read for either: `${CLAUDE_SKILL_DIR}/references/slide_principles.md` (P1–P30 global rules).

#### Generation (Stanford preset)

1. Create `html_slides/` directory.
2. Copy `${CLAUDE_SKILL_DIR}/templates/stanford_html_template.html` to `html_slides/{topic_slug}.html`.
3. If `material/` has images (screenshots, figures), prepare them for embedding.
4. Launch **one slide-writer agent** with the Stanford HTML generation prompt:

```
Agent receives:
  1. Combined lecture notes (lecture_notes/{topic}_lecture_notes.md) OR topic brief
  2. Full text of ${CLAUDE_SKILL_DIR}/prompts/stanford_html_generation.md
  3. Full text of ${CLAUDE_SKILL_DIR}/references/stanford_visual_grammar.md
  4. Full text of ${CLAUDE_SKILL_DIR}/references/slide_principles.md
  5. Skeleton: ${CLAUDE_SKILL_DIR}/templates/stanford_html_template.html
  6. Config values: audience, proof_depth, pedagogy, theme accent color, event info
  7. List of available images in material/

Agent MUST:
  - Follow the structural contract: title → hook → news hook → question → setup → mechanism → numbers → connections → punchline → end
  - Inline SVG on every content slide (no bullet-only slides)
  - Use `.callout-think` before every non-trivial reveal
  - Ship at least one `.bigstat` numbers slide
  - Use Playfair Display for headings/big numbers, DM Sans for body
  - Pass the validation gates listed in stanford_html_generation.md
  - Return: file path + slide count + fragment count + SVG count + bullet-only-slide count (must be 0)
```

#### Generation (generic preset — legacy)

1. Create `html_slides/` directory
2. If `material/` has images (screenshots, figures), prepare them for embedding
3. Launch **one slide-writer agent** with the generic HTML generation prompt:

```
Agent receives:
  1. Combined lecture notes (lecture_notes/{topic}_lecture_notes.md)
  2. Full text of ${CLAUDE_SKILL_DIR}/prompts/html_generation.md
  3. Full text of ${CLAUDE_SKILL_DIR}/references/slide_principles.md
  4. Config values: audience, proof_depth, pedagogy, theme, event info
  5. List of available images in material/

Agent MUST:
  - Generate a single self-contained HTML file
  - Write to html_slides/{topic_slug}.html
  - Return: file path + slide count + fragment count + file size
```

#### Quality Gates (HTML)

| Gate | Check |
|------|-------|
| Valid HTML | No unclosed tags |
| Think First count | Matches pedagogy target |
| Fragment count | 3-5 per content slide |
| Speaker notes | Every slide has `<aside class="notes">` |
| Visuals | Every concept slide has a visual component |
| File size | Single file < 2MB (excluding embedded images) |

No TikZ audit waves needed — CSS visualizations do not have the overlap/clipping issues that TikZ has.

Update progress: `step6_html: complete`

---

## Convergence Gates

| Step | Gate | Check |
|------|------|-------|
| 2 | Notes completeness | notation table + theorem ledger + numerical example per paper |
| 3 | Arc validity | plan.md has ordering + acts + transitions + puzzle |
| 3.5 | **Human approval** | User approved arc structure (skip if `arc_review: false` in config) |
| 4 | Coverage | every paper's theorems appear in combined notes |
| 5 | QA scores | all 10 dimensions >= 3; D8/D9 (formal defs + first-principles) >= 3 is HARD GATE |
| 6a | Compilation | pdflatex exits 0, PDF exists |
| 6b1 | Content inventory | 0 HIGH-risk frames, 0 paperfigure budget violations (Wave 1.25) |
| 6b | Viz coverage | Visual coverage ratio meets density threshold (Wave 1.5); concept inventory from plan.md fully covered |
| 6b2 | Embed audit | Wave 1.75 converged: 0 CRITICAL, 0 MEDIUM embed defects across all embedded figure frames |
| 6c | TikZ G1-G10 | Full tikz-audit convergence loop passes (0 HIGH, 0 MEDIUM, page count stable, G10 per-frame spot-check passes every iteration) |
| 6c2 | **Visual smoke test** | **Wave 2.5: 0 CRITICAL + 0 HIGH visible defects on rendered PNG inspection of every paperfigure frame, every act-boundary frame, every MEDIUM-height frame, every multi-panel-title TikZ frame (PTL-051/056)** |
| 6d | P29 | 0 transform shape + 0 tiny/scriptsize/footnotesize in TikZ (font-normalization sub-protocol if needed) |
| 6e | Coverage | all papers mentioned in slides |
| 6f | Pedagogy | Think First count >= target |
| 6g | **Min body content** | **Wave 1.25: every frame's last overlay has ≥ 2 substantive elements (not just \think{}) — PTL-052** |

After each gate passes, snapshot the artifact to `.best_known/`.
If a fix wave regresses: revert to best_known, stop, report.

---

## Progress Dashboard

On resume, read `config.yml` progress block and display:

```
=== paper-to-lecture progress ===
Topic: {topic}
Papers: {N} total

Step 1   (Setup):       DONE
Step 2   (Papers):      2/3 complete (Embrechts DONE, Guo DONE, He IN PROGRESS)
Step 3   (Arc):         not started
Step 3.5 (Arc Review):  not started  [HUMAN GATE]
Step 4   (Combined):    not started
Step 5   (QA):          not started
Step 6   (Slides):      not started

Next: Complete Step 2 (He-Liu-Wang), then Step 3.
Resume from which step? [2/3/...]
```

---

## Memory and Meta-Learning

### Per-Run Capture
At session end, review:
- QA dimensions that scored < 3 → prompt improvement signal
- TikZ audit iterations needed → generation prompt signal
- Compilation failures → LaTeX convention signal

### Lesson Storage
Append confirmed lessons to `${CLAUDE_SKILL_DIR}/references/lessons.md` with format:
```
### PTL-NNN: Title
Situation: what happened
Principle: what to do differently
Date: YYYY-MM-DD
```

### Lesson Injection
On next run, read `${CLAUDE_SKILL_DIR}/references/lessons.md` and inject relevant lessons into sub-agent prompts.

### Global Promotion
If a lesson is generalizable, use `/log-learning` to promote to:
- `~/.shared/knowledge/packs/teaching/lessons/` (teaching-specific)
- `~/.claude/school/lessons/` (universal)

---

## Agent Sync

If standalone skills (`/story-agent`, `/teaching-agent`, `/visualization-agent`) are updated:
- Check modification dates vs embedded copies in `agents/`
- If standalone is newer: warn and offer to re-embed
- `--sync-agents` flag: regenerate embedded agents from standalone skills

---

## Optional Enhancements (Oracle/Codex)

If Oracle CLI is available (`which oracle`), the pipeline can optionally use GPT-5.4 Pro for:
- Step 2: paper-to-notes generation (higher quality for proof extraction)
- Step 4B: QA review (second opinion on completeness)

This is NOT the default path. The core pipeline works entirely within Claude Code.

To enable: add `oracle_enabled: true` to `config.yml`.
