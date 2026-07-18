---
name: referee-report
description: Draft a referee report on an academic finance manuscript, synthesizing the user's structured assessment of the paper into a report that matches the tone and structure of their prior reports. Use when the user wants to process a refereeing assignment (paper + editor's invitation) and produce a draft referee report. The user referees regularly for top finance journals.
---

# Referee Report Skill

Help the user draft a referee report on a manuscript they've been asked to review. Work through the phases below in order. Do not skip phases or produce the draft report before collecting the user's structured assessment — the report is the user's view of the paper, not a generic summary.

## Phase 1 — Locate the package

1. The user should provide a folder path as the argument. If no path was given, ask for one.
2. List the files in the folder. Identify:
   - The manuscript (usually the largest PDF; may be named `paper.pdf`, `manuscript.pdf`, or similar)
   - The editor's invitation / cover letter, if present (e.g. `invitation.pdf`, `editor_letter.pdf`)
   - Any online appendix, supplementary materials, or prior-round materials (author response, prior referee reports if this is an R&R)
3. Ask the user which **journal** the report is for (this drives both tone-matching and archive lookup). Common targets: Journal of Finance (JF), Review of Financial Studies (RFS), Journal of Financial Economics (JFE).
4. Ask the user whether this is a **first-round** report or an **R&R** (revise-and-resubmit). If R&R, ask for the path to the prior-round report the user wrote — the new report should reference how the authors addressed prior concerns.
5. If any file's role is ambiguous, confirm with the user before proceeding.
6. Read **prior referee reports by the user** to model tone and structure:
   - Default archive path: `/Users/b.green/Library/CloudStorage/Dropbox/Professional/Referee Reports`
   - Look for a journal-specific subfolder matching the target journal. If not found, list what's there and ask the user where to look.
   - Sample 2–3 recent reports (or ask the user which are most representative). Note: salutation style, section ordering (e.g. summary → major comments → minor comments, or comments-to-editor vs. comments-to-authors), length, level of formality, how the recommendation is communicated, sign-off.
   - If the archive is empty or missing, ask the user for an alternate path or for a single example report to model.

## Phase 2 — Read and summarize

1. Read the manuscript. For long papers, prioritize: abstract, introduction, hypothesis development, data/methodology section, main results tables, robustness section, conclusion. Skim technical appendices unless the paper is primarily theoretical.
2. If this is an R&R: read the author response and the user's prior report carefully — the report will need to assess whether prior concerns were adequately addressed.
3. Produce, in a single message to the user:
   - **Paper summary** (≈200–300 words): research question, data, methodology, main findings, claimed contribution, where it sits in the literature.
   - **Initial observations** (bulleted, ≈5–10 bullets): things that stood out on reading — strengths, potential concerns, identification issues, framing issues, robustness questions. Frame as observations to discuss with the user, not conclusions.
   - If R&R: **Response assessment** (≈100 words): which prior concerns the authors addressed convincingly, which remain open.
4. Ask the user to confirm the summary is accurate and to react to the initial observations before proceeding. Correct if needed.

## Phase 3 — Collect the user's structured assessment

Use the AskUserQuestion tool (or plain questions if unavailable) to ask these in sequence. Do **not** bundle them into one prompt. Wait for each answer before the next.

1. **Contribution**: How significant and novel is the paper's contribution? Is it the kind of contribution the target journal publishes?
2. **Identification / methodology**: Is the empirical strategy convincing? What are the most important threats to identification or interpretation? (For theory papers: are the model setup, assumptions, and proofs sound? Are the results genuinely surprising or mechanical?)
3. **Robustness and data**: Concerns about sample construction, variable measurement, robustness, or external validity?
4. **Framing and positioning**: Is the paper well-positioned in the literature? Any over-claiming or under-claiming? Missing relevant prior work?
5. **Major comments**: What are the 3–6 major comments you want to raise? State them in the order of importance. For each, indicate whether it's addressable in revision or a deeper concern.
6. **Minor comments**: Any minor issues — exposition, table formatting, missing references, typos worth flagging? (Open-ended; user can list freely or say none.)
7. **Recommendation**: What recommendation are you making? (Reject, Reject with encouragement to resubmit, Major Revision, Minor Revision, Accept.) Ask the user to state this verbatim.
8. **Comments to editor (confidential)**: Anything to convey to the editor that should not go to the authors? (Conflicts, candor about the recommendation, suggestions about co-referees or process, etc.) Open-ended; user can say none.

## Phase 4 — Draft the report

Draft the report matching the tone, length, and structure of the example reports. Default structure if the examples are silent on ordering:

1. **Confidential comments to the editor** (separate block at the top, clearly labeled — only if the user provided content for question 8, or if the journal's format expects it; otherwise omit).
2. **Comments to the authors**:
   - Brief paper summary (~100–150 words) — shows the authors the referee understood the paper. Tighter than Phase 2.
   - Overall assessment paragraph — high-level reaction, conveying the recommendation's direction without stating it explicitly (the recommendation goes to the editor, not the authors).
   - Major comments — numbered, in the order the user prioritized them in Phase 3. Each should be substantive: state the concern, why it matters, and (where appropriate) what would address it. Avoid vague gestures like "this could be better motivated."
   - Minor comments — numbered or bulleted, brief.
   - For R&R: integrate assessment of how prior concerns were addressed into the relevant major comments rather than as a separate section, unless the user's prior reports do otherwise.
3. Sign-off matching the example reports (often no signature — referee reports are typically anonymous).

Output the draft in a code block (so the user can copy it cleanly) and then ask the user what to revise. Iterate until the user is satisfied.

## Guidance

- Write in the user's voice — read `/Users/b.green/.claude/skills/writing-style/SKILL.md` before drafting; it defines the voice and the tics to avoid. Measured, precise, specific. Avoid generic referee platitudes ("interesting paper," "the authors should clarify"). Each major comment should be sharp enough that the authors know exactly what's being asked.
- Never address the authors by name or speculate about their identity. Refer to the paper or "the authors" in the third person.
- The recommendation (accept/reject/revise) goes only in the comments to the editor, not in the comments to the authors. The authors learn the recommendation from the editor's decision letter.
- Be candid but professional. If the paper has a fatal flaw, the report should make it clear without being dismissive. If the paper is strong, the report should still raise the genuine concerns worth addressing.
- Never invent results or claims that aren't in the paper. If something is unclear, that is itself a comment worth raising (e.g. "It is not clear from the text whether X or Y is intended").
- Never write the report before Phase 3 is complete. The user's assessment is the substance of the report; Phase 2 is just shared understanding of the paper.
- Do not save any of the paper content, the user's assessment, or the draft report to auto-memory — this is confidential peer-review material.
- If the assignment is for a journal where the user has written reports archived under a different name (e.g. AE letters vs. referee reports), tone-match the referee reports, not the AE letters — the genres differ.
