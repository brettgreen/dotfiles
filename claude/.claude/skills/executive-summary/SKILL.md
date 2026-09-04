---
name: executive-summary
description: Write an executive summary of a research paper in the user's voice — plain-prose, notation-free, ~1,000 words, built from the paper's own best sentences. Use whenever the user asks for an executive summary, a non-technical summary, or a "what the paper says" document for co-authors, seminar audiences, deans, funders, or policymakers.
---

# Executive-Summary Skill

An executive summary restates the paper for a smart reader outside the field:
no notation, no citations, no theorem numbers, every result in words. It is a
freestanding document, not an abstract and not the introduction — longer than
the first, more compressed and more willing to be pointed than the second.

Read `/Users/b.green/.claude/skills/writing-style/SKILL.md` first; it governs
every sentence here. **The exemplars are the user's own two drafts in
`/Users/b.green/Dropbox/Research/AI with Problems/AI-notes.txt`** — read one
in full before drafting to reset the ear. They set the standard; derivative
updates (e.g. `exec_summary_v7.txt`) are not the calibration target. The
user singled out V1's opening paragraph ("We study AI in a knowledge economy
where firms must compete for problems as well as organize workers to solve
them. … the bottleneck moves.") as the model opener: substance first, not an
aphorism, closing line unelaborated.

## Register (how this genre differs from paper prose)

One notch punchier than the paper. Short causal chains — subject, verb,
consequence, next sentence — and a paragraph may close on a pointed line the
paper itself would not carry ("Knowledge looks up the hierarchy; cost looks
down." "Tax the human cope, not the machine."). At most one such line per
paragraph, earned by the argument before it, and the policy paragraph may
flag its own bluntness ("clear but deliberately provocative"). What stays
forbidden: hedged add-on clauses, filler intensifiers, and any sentence that
merely restates its neighbor.

## Structure (the paragraph skeleton)

1. **Hook + departure.** One sentence stating the paper's central tension in
   plain words ("AI may make the capacity to perform work abundant while
   making worthwhile work scarce."). Then what the paper studies and the one
   critical respect in which it differs from existing work.
2. **Motivation.** The puzzle, phenomenon, or mechanism that gives the
   question force — concrete and recognizable (named occupations, observed
   patterns), ending by naming the central mechanism.
3. **The model in one paragraph.** What is jointly determined, the two or
   three modeling choices that matter, the key primitive(s) in words. No
   symbols: "its capability determines what it can solve; its compute cost
   determines how cheaply it can be deployed."
4. **Results in enumerated prose.** "We obtain three sets of results.
   First, … Second, … Third, …" — one paragraph (or two) per set, never
   bullets. Each result stated flat, then its logic in a sentence or two.
5. **Policy / implications**, if the paper has them. A deliberately pointed
   formulation is allowed here — once ("tax the human cope, not the
   machine") — and may be flagged as such ("clear but deliberately
   provocative").
6. **Close on measurement or practice.** What the results change about what
   researchers, firms, or policymakers should measure or do. No summary
   restating the summary.

## Rules of substance

- **Only proven results, at their proven strength.** A weak inequality stays
  weak ("improvements can only help", not "welfare rises"); hypotheses that
  qualify a result stay attached in words ("when adopting firms use fewer
  humans per problem"). Check each claim against the current draft's
  propositions before writing it.
- **Vocabulary follows the paper's terminology key** (for the AI paper,
  the style key in `v7_changes.md`). The summary must not coin terms the
  paper does not use.
- **Harvest the paper's own best sentences.** The summary is assembled from
  the draft's strongest formulations, lightly compressed — not paraphrased
  from memory. Where the introduction already says it well, take it.
- **No notation, no citations, no author names, no section references.**
  Coined terms in quotes at first use, then bare.
- **The exemplar's prose outranks the paper's internal terminology key.** A
  notation-free document keeps the user's plain words ("its knowledge
  determines what it can solve") even where the paper has since adopted a
  different term of art; do not mechanically propagate vocabulary sweeps
  into the summary at the cost of a sentence that worked.
- **Added paragraphs must survive next to his.** When updating an existing
  summary, any new paragraph is drafted, then read against the paragraphs
  before and after it; if it is looser, longer-winded, or ends weakly by
  comparison, tighten it or cut it. A correct paragraph in a flatter
  register is still a failure in this genre.

## Length and upkeep

- Target 900–1,100 words; every paragraph earns its place.
- The summary is a living document: when the draft moves, edit only the
  paragraphs covering what moved and leave the rest verbatim — do not
  redraft wholesale. Date the file header and note which draft it summarizes.

## Workflow

1. Read the current draft's introduction and results sections (or the change
   ledger, if one exists) to fix what is actually proven and how it is named.
2. Read the calibration sample to reset the ear.
3. Draft to the skeleton above; enumerate in prose; results before
   motivation gets no say here — the skeleton's order stands.
4. Verify every result sentence against its proposition (strength,
   hypotheses, terminology).
5. Reread against the writing-style tics list; brevity pass; save as a dated
   `.txt`/`.md` alongside the draft.
