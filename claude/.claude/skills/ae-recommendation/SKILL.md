---
name: ae-recommendation
description: Help an Associate Editor at the Journal of Finance handle an editorial package. Two modes, chosen automatically by whether the folder contains referee reports. First stage (no reports yet) — decide whether to desk-reject the new submission or send it out to referees, and draft the note to the co-editor. Post-referee stage (reports present) — synthesize the reports and the AE's own feedback into a recommendation letter to the co-editor. Use when the user wants to process a JF submission package.
---

# AE Recommendation Letter Skill

Help the user (an Associate Editor at the Journal of Finance) turn a submission package into a draft note to the co-editor. There are **two modes**, and Phase 1 selects between them:

- **First-stage triage** — the folder has a manuscript but **no referee reports**. The paper has just been assigned to the AE and no reports have been solicited yet. The AE's job is to decide whether to **desk-reject** the paper or **send it out to referees**, and to draft the note to the co-editor. Run the **First-Stage** phases below.
- **Post-referee recommendation** — the folder **contains referee reports**. The AE's job is to triage the reports and recommend a course of action. Run the **Post-Referee** phases below.

Work through the phases for the selected mode in order. Do not skip phases or produce the draft before collecting the user's structured feedback.

---

## Phase 1 — Locate the package and select the mode

1. The user should provide a folder path as the argument. If no path was given, ask for one.
2. List the files in the folder. Identify:
   - The manuscript (usually the largest PDF; may be named `paper.pdf`, `manuscript.pdf`, or similar).
   - **Referee reports / letters** (often `referee_1.pdf`, `report_A.pdf`, `ref_report_*.pdf`, `ref2.docx`, etc.). **Whether any exist determines the mode.**
   - Any cover letter, author acknowledgment, or co-editor assignment/notification email (often `*notifycoed*.html`, `mnotfycoed_*.html`, `cover_let_*`). These frequently state the co-editor's own leaning and what they are asking of the AE — read them.
3. **Select the mode:**
   - **No referee reports present → First-Stage Triage.** Go to the First-Stage phases.
   - **Referee reports present → Post-Referee Recommendation.** Go to the Post-Referee phases.
   - If it is genuinely ambiguous whether a file is a referee report (vs. a cover letter or the co-editor's note), confirm with the user before committing to a mode.
4. Read **prior AE letters** from the user's archive to model tone and structure:
   - Default archive path: `/Users/brettgreen/Dropbox/Professional/Referee Reports/Journal of Finance JF/AE letters`
   - List the folder (some entries are loose `.txt`/`.rtf` files, others are per-paper subfolders — the letter is usually a short text/rtf/tex file inside). Sample 2–3 recent ones. For **First-Stage** mode, prefer examples of desk-rejection recommendations if any exist (e.g., a `rejection_rec.txt` or a memo that recommends summary rejection). If the folder is empty or missing, ask the user for an alternate path.
   - Note: salutation style, section ordering, length, level of formality, how the recommendation is phrased, sign-off.

---

# FIRST-STAGE TRIAGE (no referee reports yet)

## The AE's first-stage mandate

When a new submission is assigned, the co-editor asks the AE to confirm the assignment with one of three choices (this is the language of the assignment email):

1. **Editorial advice and suggested referees** — send the paper out for review. The AE recommends three or four referees. A brief statement about the likely significance of the contribution can help (e.g., to motivate the choice of referees), but detailed comments are not expected at this stage.
2. **Associate Editor summarily rejected** (AE desk rejection) — for papers the AE judges to have essentially no chance of publication in the JF. The AE must give the co-editor **reasons that can be drawn upon in the cover letter to the author**.
3. **Decline to handle** — e.g., conflict of interest; suggest another AE if possible.

So the first-stage deliverable is a short note to the co-editor that lands on **desk-reject** or **send-out**, with the reasoning. The co-editor's own assignment note often states a leaning ("I am inclined to DR this...") — engage with it directly: confirm it with independent reasons, or push back if you think there is a contribution worth refereeing.

## First-Stage Phase 2 — Read and summarize

1. Read the manuscript. For theory, prioritize: abstract, introduction, model setup, main propositions and their intuition, extensions, and the discussion/conclusion; skim the proofs but note whether the results are driven by assumptions. For empirical work, prioritize: abstract, introduction, hypothesis development, data/methodology, main tables, conclusion.
2. Produce, in a single message to the user:
   - **Paper summary** (≈150–250 words): research question, setup/data, method, main results, claimed contribution.
   - **AE's tentative read** (≈100–150 words): your honest first impression — is there a genuine idea here, and what are the candidate concerns (e.g., assumptions that look hard-wired to deliver the result, thin contribution, tractability-driven modeling, identification problems, poor fit). Flag whether, on first read, this looks closer to a desk reject or to something worth refereeing. Frame this as a starting point for the user to correct, not a verdict.
3. Ask the user to confirm the summary is accurate before proceeding. Correct if needed.

## First-Stage Phase 3 — Collect the AE's judgment (structured)

Use the AskUserQuestion tool (or plain questions if unavailable) to ask these in sequence. Do **not** bundle them. Wait for each answer. Lead with the tentative read from Phase 2 so the user is reacting to a concrete take, not answering cold.

1. **Contribution**: Is there a real, novel contribution here, or is the core result obvious / already known / mechanical? How does it sit relative to the closest existing work?
2. **Fatal vs. fixable concerns**: What are the main concerns, and are they *fatal* (no realistic revision saves the paper) or *fixable* (a referee round could plausibly address them)? This distinction is the crux of desk-reject vs. send-out. Engage with the co-editor's stated leaning if they gave one.
3. **Modeling / identification**: Do the assumptions look designed to deliver the result? For theory, are the key propositions robust and economically meaningful, or artifacts of the setup? For empirical, is identification credible enough to be worth refereeing?
4. **Fit for JF**: Is this plausibly a JF paper if the concerns were resolved, or is it out of scope / below the bar regardless?
5. **Decision**: Desk-reject or send out? Ask the user to state it plainly.
   - If **send out**: ask for candidate referees (three or four) and any framing/significance points to include. **If the paper is theoretical, offer to run the `ftg-match` skill to suggest referees** from the Finance Theory Group membership — invoke it with the paper's topic/abstract and bring the matched FTG members back as candidate referees for the user to approve or edit. For empirical papers, `ftg-match` is usually not the right tool; collect referee names from the user directly.
   - If **desk-reject**: collect the specific reasons, in priority order, that should go to the co-editor (and, through the cover letter, to the authors).
6. **Anything else** (open-ended): other context the co-editor should know.

## First-Stage Phase 4 — Draft the note to the co-editor

Match the tone, length, and formality of the sampled prior examples. Keep it short.

**If desk-rejecting** (model on a prior summary-rejection memo such as `rejection_rec.txt` if present):
1. Salutation to the co-editor (match example; often just "Dear [First name],").
2. **Recommendation up front**: state plainly that you recommend the paper be summarily rejected, followed by "My reasoning is as follows:".
3. **Numbered reasons** — the decisive concerns, most important first, each with a short heading and a few sentences. These are written so the co-editor can draw on them in the cover letter to the authors, so they must be concrete and defensible, not vague.
4. A brief **summary of the model/paper and its results** (so the co-editor sees you engaged with it), if the example format includes one.
5. Sign-off matching the example (e.g., "Please let me know if I can be of further assistance in the editorial process." + name).

**If sending out for review:**
1. Salutation to the co-editor.
2. One or two sentences on the **likely significance of the contribution** — enough to justify refereeing and to motivate the referee choices. Note honestly if you see it as a close call.
3. **Suggested referees** (three or four), with a phrase on why each is well-suited if useful. For theory papers, draw these from the `ftg-match` results (run in Phase 3) unless the user overrode them.
4. Any brief framing guidance for the referees or the authors.
5. Sign-off matching the example.

Output the draft in a code block (so the user can copy it cleanly) and then ask what to revise. Iterate until the user is satisfied.

---

# POST-REFEREE RECOMMENDATION (referee reports present)

## The AE's post-referee mandate (what the editorial board asks for)

The co-editors have defined the AE's role explicitly. Keep this front of mind throughout — it is the purpose of the whole letter:

> The main role we envision for AEs is to help us (and the authors, in the case of an R&R) sort through the comments and recommendations of the referees. When the referee reports come back, dig into the paper and the reports and give us your take on the referees' comments: **What's important? What's tangential? Did the referees miss something, or do you have other concerns about the quality of the referee reports? Which comments should the authors address in priority, and which can they ignore?** Finally, give a recommendation for the best course of action.

So the letter is **not** a neutral digest of the reports. Its core value is the AE's editorial triage: separating decisive concerns from tangential ones, flagging gaps or weaknesses in the reports themselves, and telling the co-editor (and, on an R&R, the authors) which points must be addressed versus which can be set aside. The recommendation follows from that triage.

## Post-Referee Phase 2 — Read and summarize

1. Read the manuscript. For long papers, prioritize: abstract, introduction, hypothesis development, data/methodology section, main results tables, conclusion. Skim technical appendices.
2. Read each referee report in full.
3. Produce, in a single message to the user:
   - **Paper summary** (≈150–250 words): research question, data, methodology, main findings, claimed contribution.
   - **Per-referee summary**: one block per referee titled `Referee 1`, `Referee 2`, etc. Each block ≈100–180 words and must include: (a) the referee's overall stance/recommendation if stated, (b) the referee's main concerns in priority order, (c) any suggested revisions, (d) notable points of agreement/disagreement with other referees.
   - **Cross-referee synthesis** (≈75 words): where referees converge vs. diverge.
4. Ask the user to confirm the summaries are accurate before proceeding. Correct if needed.

## Post-Referee Phase 3 — Collect the AE's own feedback (structured)

This phase collects the raw material for the triage the board asks for. Use the AskUserQuestion tool (or plain questions if that tool is unavailable) to ask these in sequence. Do **not** bundle them into one prompt. Wait for each answer before the next.

Before asking, it helps to offer the AE a starting point: based on your own read of the paper and reports, propose a tentative triage (which comments look decisive, which look tangential, any gaps you noticed in the reports) and let the user correct or confirm it, rather than asking every question cold.

1. **Contribution**: How significant and novel is the paper's contribution to the finance literature?
2. **Comment triage — what's important vs. tangential**: Across the reports, which referee comments are the important/decisive ones, and which are tangential or minor? This is the heart of the letter — probe until you have a clear ranking, not just a list.
3. **Priority to address vs. can ignore**: Which comments must the authors address (in priority order), and which can they safely set aside or push back on? (On an R&R this guidance is also read by the authors.)
4. **Quality of the reports / gaps**: Did the referees miss anything important? Do you have concerns about the quality, fairness, or correctness of any report? Are any referee criticisms overstated, mistaken, or based on a misreading?
5. **Methodology / identification**: Are the empirical strategy, identification, and robustness (or, for theory, the model and proofs) convincing? Any concerns beyond what the referees raised?
6. **Fit and framing**: Is the paper well-suited to JF? Any issues with framing, positioning, or scope?
7. **Recommendation**: What recommendation are you making to the co-editor? (User specifies freely — e.g., Reject, Reject with encouragement to resubmit, Major Revision, Minor Revision, Conditional Accept, Accept.) Ask the user to state this verbatim as they want it to appear.
8. **Key points to emphasize** (open-ended): Anything else the co-editor should know — conflicts among referees you want to resolve, points you want to flag, prior-round context, etc.

## Post-Referee Phase 4 — Draft the letter

Draft the letter matching the tone, length, and structure of the example letter the user provided. The letter must deliver the board's mandate: an editorial triage of the referee comments, not a neutral digest. Default structure if the example is silent on ordering:

1. Salutation to the co-editor (match example).
2. One-paragraph paper summary (tighter than Phase 2 — ~100 words).
3. **The triage — the core of the letter.** Give the AE's take on the referees' comments: which concerns are important/decisive, which are tangential, and which comments the authors should prioritize versus set aside. Weave in whether the referees missed anything or whether any report is weak, unfair, or mistaken. Do not mechanically rehash Phase 2 — this is the AE's editorial judgment about the reports, and it should read as such.
4. The AE's independent assessment of contribution, methodology, and fit — including any concerns the referees did not raise.
5. Explicit recommendation for the best course of action, phrased as the user stated it in Phase 3.
6. Brief reasoning for the recommendation, tying back to the triage in (3).
7. Sign-off matching the example.

Match the example letters' length and altitude — these are typically short (a few paragraphs), so the triage should be sharp and selective, not an exhaustive point-by-point.

Output the draft in a code block (so the user can copy it cleanly) and then ask the user what to revise. Iterate until the user is satisfied.

---

## Guidance (both modes)

- Write in the user's voice — if `/Users/brettgreen/.claude/skills/writing-style/SKILL.md` exists, read it before drafting (it defines the voice and the tics to avoid); otherwise infer the voice from the sampled prior AE letters. Measured, precise, specific. Avoid generic editorial platitudes ("interesting paper," "makes a contribution"). If the user is rejecting (at either stage), the note should clearly explain why without being harsh.
- Always refer to referees as R1, R2, etc. — never by name, even if a referee signed their report or a cover letter identifies them.
- Never invent referee recommendations or paper results. If something is unclear in the source material, flag it to the user rather than guessing.
- Never write the note/letter before the relevant Phase 3 is complete. The AE's own view is the core of the deliverable.
- Do not save any of the paper content, referee content, or draft note to auto-memory — this is confidential peer-review material.
- If the folder contains a prior-round decision letter or author response, read it for context but keep the new note focused on the current round.
