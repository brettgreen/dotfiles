---
name: strategic-revision
description: Process a revise-and-resubmit package (manuscript + referee reports + editor's decision letter) for one of the user's own papers and produce, in sequence, (1) a strategic revision memo that prioritizes every referee point and recommends comply / partial / push back, then (2) a point-by-point response-to-referees letter in the user's voice. Use when the user is responding to referees on their own paper. The user publishes in top finance/economics journals.
---

# Strategic Revision Skill

Help the user respond to referees on **their own** manuscript (a revise-and-resubmit). This is the author side of the table — the goal is to win the revision: address concerns convincingly, push back where the referees are wrong or where compliance would harm the paper, and do it in the user's established voice.

Work through the phases in order. Produce the **strategy memo (Phase 3) first** and get the user's decisions before drafting any letter (Phase 4). The letter encodes the user's strategic choices — do not pre-empt them.

## Phase 1 — Locate the package

1. The user should provide a folder path as the argument (usually a `*Revision`/`*Response` subfolder inside the paper's directory). If no path was given, ask for one.
2. List the files in the folder (and the parent paper folder if needed). Identify:
   - The **manuscript** — both the current/revised version and, if present, the previously submitted version (a diff of the two reveals what's already been changed).
   - The **referee reports** (e.g. `referee_1.pdf`, `report_A.pdf`, `RefereeReport*.pdf`).
   - The **editor's decision letter** — critical: it tells you which concerns the editor weighted most heavily and whether this is a high- or low-probability revision.
   - Any **prior-round materials** if this is a 2nd+ round R&R: the user's previous response letter, prior reports, prior decision letter. The new response must show how earlier concerns were resolved and not reopen settled points.
3. If any file's role is ambiguous, confirm with the user before proceeding.
4. Ask the user which **journal** this is for and **which round** (1st response, 2nd, etc.). Journal drives tone; round drives how much of the "Main Changes" framing references prior correspondence.
4a. Determine the **required response format** from the decision letter — this governs Phase 4's structure, so read the letter's instructions explicitly rather than assuming:
   - **Per-referee** (the default at most journals — JF, JFE, RFS, REStud, Econometrica, etc.): a point-by-point response to every referee report, usually one section per referee plus a section for the editor.
   - **Editor-comment-driven** (e.g., AER: Insights conditional accepts): the letter responds to the *editor's* numbered comments, and point-by-point referee responses are explicitly **not** required — referee points are folded in where they go beyond the editor's asks. AERI also gives a "conditional accept," not an R&R, with a short fixed deadline and no second referee round.
   - If the letter doesn't say, ask the user; default to per-referee.
5. Read **prior response letters by the user** to model voice and structure. There is **no single archive** — they live in each paper's revision folder. Use these known exemplars as style references (read 2–3, preferring the same journal or closest genre — theory vs. empirical):
   - `Dropbox/Research/Daley_Green/Signaling_with_grades/RESTUD_revision/response_letter.tex` (REStud, theory; richest structure)
   - `Dropbox/Research/Published/inforeputation/JFE_version_2/RefereeResponseJFE2014_0305.tex` (JFE, theory)
   - `Dropbox/Research/Published/Streakiness_shared/Management Science revision/response_to_reviewers.tex` (Mgmt Sci, empirical; AE + referee)
   - `Dropbox/Research/Daley_Green/Lemons/Econometrica_Revision{1,2}_submission/response_letter.pdf` (Econometrica, theory)
   - `Dropbox/Research/Daley_Green/Bargaining/AER_Revision/Response_Letter.pdf` (AER, theory)
   - `Dropbox/Research/PayJoy/ReStud Response/Responses_PAYGo.tex` (REStud, empirical)
   - (Base path: `/Users/b.green/Library/CloudStorage/Dropbox/`)
   - If the current paper has a prior-round response in its own folder, prefer that as the primary voice model. If none of the exemplars are readable, ask the user to point at one.
   - Note: salutation, the up-front **Main Changes** block, comment-labeling scheme (M./E./R1.S/R1.), how comments are quoted (italic verbatim vs. paraphrased "for parsimony"), how pushback is phrased, sign-off.

## Phase 2 — Read and extract

1. Read the manuscript (prioritize: abstract, intro, model/hypotheses, methodology, main results, conclusion; skim heavy appendices). If a prior version exists, note what already changed between versions.
2. Read the editor's decision letter in full, then each referee report in full.
3. Produce, in a single message to the user:
   - **Paper summary** (~120 words) — just enough to anchor the discussion.
   - **Editor's letter read** (~80 words) — what the editor is really asking for, which concerns they flagged as decisive, and the implied bar for the revision.
   - **Extracted points** — one block per source (`Editor`, `Referee 1`, `Referee 2`, …). Within each block, enumerate **every discrete point** as a numbered item (E.1, R1.1, …), each stated in one tight sentence. Capture minor/exposition points too, but mark them `[minor]`. This list is the spine of both the memo and the letter, so be exhaustive — a missed point becomes a missed response.
   - **Cross-source conflicts** (~60 words) — where referees contradict each other, or a referee contradicts the editor. These are the highest-stakes strategic decisions.
4. Ask the user to confirm the extraction is complete and accurate before proceeding. Add anything missed.

## Phase 3 — Strategic revision memo (the review gate)

This is the heart of the skill. Produce a **strategy memo** (not a letter — a working document for the user). For **every** extracted point, give one row/entry with:

- **ID** (E.1, R1.3, …) and a one-line restatement of the ask.
- **Recommendation**: **Comply** / **Partial** / **Push back** / **Defer-to-user** (for genuinely judgment-dependent calls).
- **Why** — the reasoning. For *comply*: roughly what the change is and how costly. For *partial*: what to grant and what to hold. For *push back*: the substantive grounds (the referee is mistaken, the request is outside scope, compliance would weaken the paper, or it conflicts with another referee/the editor) **and** a suggested diplomatic framing for the rebuttal.
- **Effort/risk flag** — call out points that are expensive (new analysis, new data, re-derivation) or that, if mishandled, could sink the revision.

Then add three synthesis sections:
- **Conflicts & priorities** — resolve each cross-source conflict with a recommended stance, and rank the 3–6 points that will most determine the revision's success. Tie these to what the editor emphasized.
- **Recommended pushback set** — the consolidated list of points where you advise *not* fully complying, since these carry the most risk and the user will most want to weigh in.
- **Open questions for the user** — anything `Defer-to-user`, plus any point where the right move depends on facts only the user knows (feasibility of an analysis, private editor correspondence, co-author constraints).

Then **stop and get the user's decisions**. Walk through at least the pushback set and open questions — use AskUserQuestion (or plain sequential questions) so the user can confirm comply / partial / push back per contested point and supply justification you can't infer. Record the final disposition for every point before drafting. Do not draft the letter until the user has signed off on the strategy.

## Phase 4 — Draft the response letter

Draft the letter matching the voice of the exemplars and reflecting the user's Phase 3 decisions exactly. **Choose the structure based on the required response format identified in Phase 1a** — do not assume:

**Per-referee format** (most journals — the default). One combined letter:
1. **Salutation** to the editor (match exemplar; e.g. "Dear Professor ___").
2. **Opening paragraph** — thank the editor/referees, state that the paper has improved, and (the user's convention) invite the editor to share the letter with the referees and to flag anything misunderstood.
3. **Main Changes** (M.1, M.2…) — the most prominent revisions first, framed around the editor's high-level goals. This is where the strategic narrative lives: lead with what you did, so individual responses read as supporting detail.
4. **Editor Specific Comments** (E.1…) — quote (or paraphrase "for parsimony") each editor point in italics, then respond, pointing to concrete manuscript locations (section/page/footnote).
5. **Per-referee sections** (Referee 1, …) — same quote-then-respond pattern, in the report's order; split into *Substantial Comments* and *Additional Remarks/Minor* if that referee's volume warrants it (as in the exemplars). **Every** referee point gets its own response.
6. **Sign-off** matching the exemplar.

**Editor-comment-driven format** (e.g. AERI conditional accept — only when Phase 1a establishes the letter responds to the editor's comments and per-referee responses are not required):
1. **Salutation** + opening paragraph (thank the editor; note the paper has improved; offer to discuss anything that seems sub-optimal — matches the conditional-accept's "aligned incentives" tone).
2. **Response to the editor's numbered comments** (1, 2, 3…), quote-then-respond, in the editor's order. **Fold the relevant referee points into the editor comment they map to** (e.g. the LATE comment absorbs the referees' LATE objections), rather than a separate per-referee walk-through.
3. A brief closing section addressing notable referee points that fall outside the editor's numbered asks (the editor's "consider the remaining points" instruction), at least with caveats — not necessarily one-by-one.
4. **Sign-off** matching the exemplar.

In both formats: each response uses the comply / partial / push-back register below.

For each response:
- **Comply** → state what was changed and where, concisely. Don't over-explain a concession.
- **Partial** → grant what you granted graciously, then explain what you held and why.
- **Push back** → use the user's diplomatic-but-firm register: acknowledge the point, then give the substantive reason, often offering a smaller accommodation ("We are hesitant to… as it would…; instead we have…"). Never dismissive.
- Reference real manuscript locations. Where the exact section/page isn't yet known, insert a clearly marked placeholder (e.g. `[Section X]`) rather than inventing one.

Output the draft in a code block (LaTeX if the exemplars/folder are LaTeX, matching their labeling macros where visible; otherwise clean prose) so the user can paste it. Then ask what to revise and iterate.

## Guidance

- Write in the user's voice — read `/Users/b.green/.claude/skills/writing-style/SKILL.md` before drafting; it defines the voice and the tics to avoid. Measured, precise, concrete; concede readily where warranted and push back substantively where not. Avoid author platitudes ("we thank the referee for this insightful comment" on repeat); vary and keep it genuine.
- This is the user's own paper and is **co-authored** — use "we." Refer to referees as Referee 1/R1, the editor as the editor; never speculate about identities even if a report is signed.
- The strategy is the user's to set. Phase 3 recommendations are advice; the user decides. Never quietly comply with a point the user wanted to contest, or vice versa.
- Be exhaustive about points — every referee/editor item gets a response in the letter, including minor ones. A dropped point reads as evasion.
- Never invent manuscript changes, results, or citations. If a response requires a change not yet made, write the response and flag to the user that the corresponding revision still needs doing (this skill drafts the letter; it doesn't edit the paper unless asked).
- If a referee asks for something genuinely infeasible or that would damage the paper, the memo should say so plainly and the letter should decline diplomatically with reasons — don't promise what can't be delivered.
- In editor-comment-driven format, when the editor has overruled a referee's negative recommendation (e.g. a conditional accept over a "reject"), do **not** re-argue with that referee in the letter — it re-litigates a settled point and spotlights the most negative report. Address the underlying substance through the editor's framing instead (e.g. sharpen the contribution where the editor asked, rather than rebutting the referee's "modest contribution" view directly).
- Do not save paper content, referee/editor content, the strategy memo, or the draft letter to auto-memory — this is confidential pre-publication material.
- This is the author-side counterpart to the [[referee-report]] and ae-recommendation skills; tone-match the user's **response letters**, not their referee reports — the genres differ (advocacy vs. evaluation).
