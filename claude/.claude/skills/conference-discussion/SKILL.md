---
name: conference-discussion
description: Build a Beamer slide deck for a conference discussion of someone else's paper, in the user's established discussant style. Read the paper, draft the exposition slides (what the paper does, key insight, intuition, and optionally what it teaches us about the world), then collect the user's own critical comments and draft the comment slides from them. Use when the user has been assigned to discuss a paper at a conference and wants to prepare their discussion slides. The user discusses regularly at top finance/economics conferences (AFA, WFA, NBER, etc.).
---

# Conference Discussion Skill

Help the user build the slide deck for a conference discussion — a 15–20 minute presentation in which the user (the discussant) summarizes a paper they did **not** write and then offers constructive critical comments. The deck is the user's view of the paper, so the **comment slides are the user's comments**, not generic critiques Claude invents. Claude drafts the exposition; the user supplies the substance of the critique.

Work through the phases in order. Draft the exposition (Phase 2) for the user to confirm, then **collect the user's comments (Phase 3) before drafting any comment slides** (Phase 4). Do not write the critical comments before the user has supplied them.

## House style (what these decks look like)

Every deck the user has built follows a recognizable pattern — match it unless the user says otherwise.

- **Beamer**, `\documentclass[12pt,aspectratio=169]{beamer}`, `\usetheme{default}`, `\usecolortheme{rose}`, `\usefonttheme{professionalfonts}`, `\usefonttheme{serif}`, then `\input{presentation_style}`.
- Title block: `\title[ShortTag]{{\small Discussion of} \\ <Paper Title>}`, `\author{<Authors, last names>}`, and a `\date{<Conference> \\[12pt] <Month Year> \\[12pt] Discussant: Brett Green}`.
- Convenience macros from `presentation_style.tex`: `\bi … \ei` (itemize), `\be … \ee` (enumerate), `\bs`/`\ms` (big/medskip), `\beq … \eeq`. Color/emphasis macros usually defined in the preamble: `\newcommand{\keyt}[1]{{\color{blue} #1}}` (key terms, blue), `\newcommand{\alrt}[1]{{\color{red} #1}}` (alerts, red), `\keytb` (bold blue).
- Builds reveal incrementally with `\pause`, `\only<n>{…}`, and the `[<+->]` overlay specs baked into `\bsi`/`\bse`.
- Figures are usually native **TikZ / pgfplots** (load `\usepackage{tikz}`, `\usepackage{pgfplots}`, `\pgfplotsset{compat=1.18}`), not imported images — e.g. gains-from-trade plots with `axis lines=middle`, empty ticks, dynamics arrows via `decoration={markings,…}`. Reuse/adapt these rather than inventing a new figure idiom. Imported figures (`\includegraphics`) appear when lifting a plot straight from the paper.
- The user keeps salutation/sign-off-free decks; the closing slide is an "Overall" slide, not a thank-you slide.

### The slide arc

A typical deck runs ~12–18 frames in this order. Adapt to the paper, but this is the spine:

1. **Title slide** (`\maketitle`).
2. **What does this paper do?** / **Summary** — the research question and what the paper delivers, in 1 frame. For empirical papers this often opens by situating the question in the literature (a bulleted list of strands with citations) before stating what *this* paper isolates.
3. **Background / setup** — the prior-work anchor the paper builds on (e.g. "Starting Point: DeMarzo and Uroševi\'c (2006)") and the key tension. Often 1–2 frames.
4. **Key insight of the paper** — the one idea, stated cleanly (often an "if (i) … AND (ii) … THEN …" structure).
5. **Intuition / mechanism** — the model recap or empirical design, with the central equation(s) or figure(s). 2–4 frames. This is where the TikZ plots live. **Every deck should explain the paper with at least one picture** — see "Lead with a picture" below.
6. **(Optional) Literature context** — where the paper sits relative to prior work and what it adds. See "Placing the paper in the literature." Often folded into the background slide; can be its own "literature map" frame.
7. **(Optional) What this teaches us about the world** — see below. Include when the user asks for it.
8. **Comments** — numbered frames, `\frametitle{Comment k: <sharp title>}`, each making one point and ending in a bold **Suggestion:**. Usually 3–5 comment frames, in the user's priority order.
9. **Overall** — a short closing frame: genuine praise (1–2 lines) plus the consolidated main suggestions in one bullet.

### Lead with a picture (default)

The user thinks visually and wants the paper *explained with a picture*, not just bullets. **By default, every deck includes at least one figure that does real explanatory work** — a phase diagram, a tradeoff plot, a timeline, a decision tree, a mechanism schematic, or the paper's own key figure. Treat this as a requirement to satisfy or consciously waive, not a nice-to-have.

- Aim to carry the **key insight or mechanism** in a picture, not only in prose. If a frame is doing heavy conceptual lifting with bullets alone, ask whether a figure would do it better.
- Prefer native **TikZ / pgfplots** in the house idiom (adapt an archive plot — see the gains-from-trade and groupplot examples in `AFA2025/green_discussion.tex`). Lift the paper's own figure with `\includegraphics` when that figure already nails it; redraw when the paper's version is cluttered or you want to strip it to the essential idea.
- If the paper genuinely resists a useful figure, say so to the user and propose the closest alternative (e.g. a schematic of the setup or a stylized version of the main result) rather than silently shipping a bullets-only deck.
- When in doubt, sketch the figure idea in Phase 2 and show it early — a rough-but-right picture beats a polished paragraph.

### Placing the paper in the literature (optional, on request)

The user sometimes wants a slide (or a framing of the background slide) that **positions the paper in the literature** — what's been done before, what this paper adds, and how it differs from the closest work. How to build it, in order of reliability:

- **Read the paper first.** Its introduction and related-work section give the *authors' own* positioning and the citations they rely on — start there, and note the prior-work anchor the paper builds on (this is often already the background slide).
- **Read related papers the user drops in the folder.** This is the most reliable source for a sharp contrast. If the user wants to position against specific papers (close competitors, the anchor model, or the user's own related work), they should include those PDFs; read them precisely and draw the comparison from the text, not from memory.
- **Use training knowledge cautiously, and verify.** Claude can place the paper using its knowledge of the finance/econ literature, but **must not invent citations, years, or results.** Verify anything load-bearing with WebSearch (deferred tool — load it via ToolSearch) or by asking the user, since a misattributed result in a discussion is costly. If unsure of a citation, flag it for the user to confirm rather than putting it on a slide.
- In Phase 1, ask whether the user wants this slide, and **tell them they can drop related PDFs into the folder** for a more accurate contrast. The result is a constructive (exposition-block) slide, typically a "literature map" — strands with citations and a one-line statement of what this paper does differently.

### The "what we learn about the world" slide (optional, on request)

The user sometimes wants a slide on **what the paper teaches us about the world** — which real questions or puzzles it helps answer, and what we learn about specific applications. When the user wants this (ask in Phase 1; offer it if they don't mention it):

- Take the applications **seriously and concretely** — name the actual phenomenon (LBOs, activist campaigns, mortgage servicing, OTC market structure, …) and state what the paper's mechanism *predicts or explains* about it. Not "this could apply to many settings."
- Frame it as puzzles answered: "Why do we see X?" → the paper's mechanism gives an answer. Tie predictions to known empirical patterns or stylized facts where the user can point to them.
- This slide is constructive (it sells the paper's relevance), so it sits in the exposition block (before the comments), and Claude may **draft candidate content** for it from the paper — but flag it for the user to confirm, since the applications are a judgment call.

## Phase 1 — Locate the paper and set up the deck

1. The user should provide a path as the argument — either a folder for the discussion or the paper PDF itself. If nothing was given, ask. The default working area is `/Users/b.green/Git/Discussions/`; new discussions get their own subfolder there, and the archive of past discussions lives in `past/Conference_Discussions/`.
2. Identify **the paper being discussed** (the PDF that is not one of the user's own decks). If a folder has several PDFs, the paper is usually the largest / most recent manuscript — but note that the folder may also contain **related papers the user dropped in for literature context** (see Phase 2); distinguish the paper-under-discussion from those, and confirm with the user if ambiguous.
3. Ask the user (briefly, can be bundled):
   - The **conference and date** (for the title slide — e.g. "AFA Meetings, January 2026").
   - The **talk length / slide budget** (discussions are short — typically 15–20 min ≈ 12–18 slides). This caps how many comments and how much exposition to plan.
   - Whether to include an optional **literature-context** slide. If yes, tell the user they can drop the key related papers (close competitors, the anchor model, their own related work) into the folder for a more accurate contrast — Claude will read those precisely rather than rely on memory. See "Placing the paper in the literature."
   - Whether to include the optional **"what this paper teaches us about the world"** slide.
4. Set up the deck folder:
   - If the user pointed at an existing folder, work there. Otherwise create a new subfolder of `/Users/b.green/Git/Discussions/` named for the conference (e.g. `AFA2026_Bargaining/`).
   - Copy `presentation_style.tex` from `/Users/b.green/Git/Discussions/past/Conference_Discussions/presentation_style.tex` into the new folder so `\input{presentation_style}` resolves locally and the folder is self-contained. (Recent decks in the archive `\input{../presentation_style}`; copying the file in is more portable.)
   - Name the deck `green_discussion.tex`, matching the archive convention.
5. Read **2–3 recent decks from the archive** to lock in tone and structure before drafting. Good models: `past/Conference_Discussions/AFA2025/green_discussion.tex` (theory), `past/Conference_Discussions/DukeUNC_CF_2023/green_discussion.tex` (empirical-flavored), and one closest to the current paper's genre. Note: how the summary frame opens, how comments are titled and phrased, the **Suggestion:** convention, and the figure idiom.

## Phase 2 — Read the paper and draft the exposition

1. Read the paper. Prioritize: abstract, introduction, model setup / hypotheses, main results, the key proposition or main table, and the conclusion. For theory, get the model and the main result precisely; for empirical, get the identification strategy and the headline estimates. If a **literature-context** slide was requested, also read the paper's related-work section for the authors' own positioning and read any **related-paper PDFs** the user dropped in the folder; verify load-bearing citations with WebSearch and never put an unverified citation on a slide (see "Placing the paper in the literature").
2. Draft the **exposition slides** (arc items 2–6 above) directly into `green_discussion.tex`: title slide, "What does this paper do?", background, key insight, intuition/mechanism, and — if requested — the "what we learn about the world" slide. **Plan at least one explanatory picture from the start** (see "Lead with a picture") — decide early what the key idea's figure is and build it in TikZ/pgfplots in the house idiom (adapt an archive plot rather than starting from scratch); if a figure is better lifted from the paper, leave a clearly marked `\includegraphics` placeholder noting which figure to drop in. Surface the figure idea to the user early even if it's still rough.
3. Compile the deck (see Phase 4 compile note) so the user can see real slides, then send the user:
   - A one-line map of the frames drafted so far.
   - The **paper summary** as you understand it (≈150 words) and the **key insight** you've stated on the slide — ask the user to confirm both are right. The exposition must be faithful; a discussant who misstates the paper loses the room.
   - If you drafted the "what we learn" slide, surface the applications you chose and ask the user to confirm/redirect them.
4. Correct the exposition based on the user's feedback before moving on.

## Phase 3 — Collect the user's comments (the gate)

The comments are the user's contribution and the reason the deck exists. Collect them before drafting the comment slides. Use AskUserQuestion (or plain sequential questions if unavailable); ask in sequence, do not bundle.

1. **Overall stance**: What's the headline reaction? Is this a strong paper with refinements to suggest, or one with a more fundamental concern? (Sets the tone of the comments and the Overall slide.)
2. **Major comments**: What are the 3–5 comments you want to make, in priority order? For each, capture: the point, *why it matters*, and the constructive suggestion (what the authors could do). Push the user for specifics — a discussion comment should be sharp enough that the authors and audience know exactly what's being raised. If the user gives a terse comment, offer to sharpen the framing and propose the **Suggestion:** line for their approval (drafting the *wording* is fine; inventing the *substance* is not).
3. **Minor points**: Any smaller exposition/robustness/framing points worth one quick slide or a bullet? (Optional.)
4. **Praise for the Overall slide**: What's genuinely good about the paper — the line(s) to lead the closing slide with?
5. Confirm the comment count fits the slide budget from Phase 1; if not, help the user cut or merge.

## Phase 4 — Draft the comment slides and finish the deck

1. Add one **Comment** frame per major comment, in the user's priority order: `\frametitle{Comment k: <sharp, specific title>}`, the point developed in 2–4 bullets (use `\pause`/`[<+->]` to reveal the suggestion last, matching the archive), ending in a bold **\textbf{Suggestion:}** line. Fold minor points into a single frame or append as sub-bullets, as the archive does.
2. Add the **Overall** frame: 1–2 lines of genuine praise (from Q4), then the consolidated main suggestions in one bullet ("Main suggestions: clarify the research question, explore normative implications, and simplify the model").
3. Compile the deck and confirm it builds:
   - Prefer `latexmk -pdf green_discussion.tex` (run twice if `latexmk` is unavailable: `pdflatex green_discussion.tex` ×2). Run from inside the deck folder.
   - If compilation fails, read the `.log`, fix the LaTeX, and recompile until it builds cleanly. Report the final page count against the slide budget.
4. Show the user the frame list and page count, and iterate: tighten wording, adjust builds, refine figures, re-order or cut comments until the user is satisfied.

## Guidance

- Write in the user's discussant voice: precise, generous about what's good, and constructive about what's not. The sentence-level voice rules in `/Users/b.green/.claude/skills/writing-style/SKILL.md` apply to slide text too (no slogans, no filler intensifiers, surgical emphasis) — bullets are of course the norm on slides. Comments are framed to *improve* the paper, each ending in a concrete **Suggestion:** — never a takedown. Even a fundamental concern is raised respectfully.
- **The exposition must be accurate.** Never misstate the model, the result, or the empirical design. If something in the paper is unclear, that ambiguity is itself a candidate comment ("It is not clear whether X or Y is intended") — flag it to the user rather than guessing on a slide.
- **Never invent the substance of a comment.** Claude drafts exposition, sharpens the wording of the user's comments, and proposes figures — but the critical points come from the user (Phase 3). The "what we learn about the world" and "literature context" slides are the places Claude may propose substantive (constructive) content, and even there the user confirms it.
- **Never invent citations.** Author names, years, titles, and attributed results must come from the paper, from related PDFs the user provided, or from a verified source (WebSearch) — never from unverified memory. When unsure, flag it for the user rather than putting it on a slide. A misattributed result in a discussion is costly.
- Respect the slide budget — discussions are short. When in doubt, fewer, sharper slides. Cut exposition before cutting comments; the comments are why the user is on stage.
- **Default to explaining the paper with a picture.** The user is visual — aim for at least one figure that carries the key insight or mechanism, not bullets alone. Match the figure idiom: native TikZ/pgfplots in the house style, adapted from archive plots. Keep axes clean (empty ticks, `axis lines=middle`), and use the dynamics-arrow decoration pattern for phase-diagram-style plots. Only ship a bullets-only deck if the paper genuinely resists a useful figure — and say so.
- Refer to the authors by last name (as on the title slide) and to "the paper"; this is public-facing, so the tone is collegial.
- The paper being discussed is typically an unpublished working paper shared in confidence for the discussion. Do not save the paper's content or the user's comments to auto-memory. Saving reusable *style* preferences the user states (e.g. "always include the applications slide") is fine.
- This is the discussant-side counterpart to the user's [[referee-report]] (evaluation for an editor) and [[strategic-revision]] (author-side response) skills; the genres differ — a discussion is a public, constructive presentation, so tone-match the archive decks, not the referee reports.
