---
name: ae-recommendation
description: Synthesize referee reports and the user's own feedback into a draft Associate Editor recommendation letter to a co-editor for the Journal of Finance. Use when the user wants to process an editorial package (paper + referee reports) and produce a recommendation letter. The user is an Associate Editor at JF.
---

# AE Recommendation Letter Skill

Help the user (an Associate Editor at the Journal of Finance) synthesize a submission package into a draft recommendation letter to the co-editor. Work through the phases below in order. Do not skip phases or produce the draft letter before collecting the user's structured feedback.

## Phase 1 — Locate the package

1. The user should provide a folder path as the argument. If no path was given, ask for one.
2. List the files in the folder. Identify:
   - The manuscript (usually the largest PDF; may be named `paper.pdf`, `manuscript.pdf`, or similar)
   - Referee reports / letters (often `referee_1.pdf`, `report_A.pdf`, `ref2.docx`, etc.)
   - Any cover letter or prior decision letters (note but do not summarize unless relevant)
3. If any file's role is ambiguous, confirm with the user before proceeding.
4. Read **prior AE letters** from the user's archive to model tone and structure:
   - Default archive path: `/Users/b.green/Library/CloudStorage/Dropbox/Professional/Referee Reports/Journal of Finance JF/AE letters`
   - List the letters in that folder. If there are several, sample 2–3 recent ones (or ask the user which are most representative). If the folder is empty or missing, ask the user for an alternate path.
   - Note: salutation style, section ordering, length, level of formality, how the recommendation is phrased, sign-off.

## Phase 2 — Read and summarize

1. Read the manuscript. For long papers, prioritize: abstract, introduction, hypothesis development, data/methodology section, main results tables, conclusion. Skim technical appendices.
2. Read each referee report in full.
3. Produce, in a single message to the user:
   - **Paper summary** (≈150–250 words): research question, data, methodology, main findings, claimed contribution.
   - **Per-referee summary**: one block per referee titled `Referee 1`, `Referee 2`, etc. Each block ≈100–180 words and must include: (a) the referee's overall stance/recommendation if stated, (b) the referee's main concerns in priority order, (c) any suggested revisions, (d) notable points of agreement/disagreement with other referees.
   - **Cross-referee synthesis** (≈75 words): where referees converge vs. diverge.
4. Ask the user to confirm the summaries are accurate before proceeding. Correct if needed.

## Phase 3 — Collect the AE's own feedback (structured)

Use the AskUserQuestion tool (or plain questions if that tool is unavailable) to ask these in sequence. Do **not** bundle them into one prompt. Wait for each answer before the next.

1. **Contribution**: How significant and novel is the paper's contribution to the finance literature?
2. **Methodology / identification**: Are the empirical strategy, identification, and robustness convincing? Any concerns the referees missed or overstated?
3. **Referee agreement**: For each referee, do you agree with their main criticisms? Are any concerns decisive vs. addressable in revision?
4. **Fit and framing**: Is the paper well-suited to JF? Any issues with framing, positioning, or scope?
5. **Recommendation**: What recommendation are you making to the co-editor? (User specifies freely — e.g., Reject, Reject with encouragement to resubmit, Major Revision, Minor Revision, Conditional Accept, Accept.) Ask the user to state this verbatim as they want it to appear.
6. **Key points to emphasize** (open-ended): Anything else the co-editor should know — conflicts among referees you want to resolve, points you want to flag, prior-round context, etc.

## Phase 4 — Draft the letter

Draft the letter matching the tone, length, and structure of the example letter the user provided. Default structure if the example is silent on ordering:

1. Salutation to the co-editor (match example).
2. One-paragraph paper summary (tighter than Phase 2 — ~100 words).
3. Synthesis of the referee reports, with the AE's assessment woven in (not a mechanical rehash of Phase 2 — integrate the AE's view of which concerns are decisive).
4. The AE's independent assessment of contribution, methodology, and fit.
5. Explicit recommendation, phrased as the user stated it in Phase 3.
6. Brief reasoning for the recommendation, tying back to referee concerns and AE assessment.
7. Sign-off matching the example.

Output the draft in a code block (so the user can copy it cleanly) and then ask the user what to revise. Iterate until the user is satisfied.

## Guidance

- Write in the user's voice — measured, precise, specific. Avoid generic editorial platitudes ("interesting paper," "makes a contribution"). If the user is rejecting, the letter should clearly explain why without being harsh.
- Always refer to referees as R1, R2, etc. — never by name, even if a referee signed their report or a cover letter identifies them. This applies to both the Phase 2 summaries and the final letter.
- Never invent referee recommendations or paper results. If something is unclear in the source material, flag it to the user rather than guessing.
- Never write the letter before Phase 3 is complete. The AE's own view is the core of the letter.
- Do not save any of the paper content, referee content, or draft letter to auto-memory — this is confidential peer-review material.
- If the folder contains a prior-round decision letter or author response, read it for context but keep the new letter focused on the current round.
