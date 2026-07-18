---
name: model-writing
description: Draft or rewrite economic-model / theory exposition (a model note, a setup section, an equilibrium definition, assumptions, propositions and their intuition) in the user's own writing voice — the measured, declarative theory-paper style of his published work. Use whenever producing or revising model exposition so it reads as the user wrote it rather than as generic or AI prose. The user is a theorist who publishes in AER/JET/JF.
---

# Model-Writing Skill (the user's voice)

Write model exposition the way the user writes it in his published theory papers: measured, precise, declarative, and free of the tics that mark generic or AI prose. A reader who knows his work should recognize the writing as his.

This skill layers model-specific conventions on top of the user's general voice. **First read `/Users/b.green/.claude/skills/writing-style/SKILL.md`** — the general voice principles and the full tics-to-avoid list live there and apply here; the rules below are specific to model exposition.

## Calibration corpus

The user's voice is defined by his published theory papers. When in doubt, read one model section before drafting to reset the ear:

- `/Users/b.green/Library/CloudStorage/Dropbox/Research/Published/Sentiments Liquidity and Asset Prices/AER_Final_Submission/sentiments_final.tex` — §"The Model" (setup, equilibrium definition, benchmark).
- `/Users/b.green/Library/CloudStorage/Dropbox/Research/Published/Information Aggregation in Dynamic Markets with Correlated Assets/JET Revision/Revision_draft2.tex` — §"The Model" and its "Remarks on Modeling Assumptions".
- Other theory folders under `/Users/b.green/Library/CloudStorage/Dropbox/Research/Published/` (Dynamic Lemons with Correlated Types, Ratings/Securitization, Sentiments variants).

Match the **model sections**, not the introductions — the intro is a different register.

## How the user writes models

**Setup is a sequence of plain declarative sentences.** Introduce each object, agent, and primitive one at a time, symbol and domain inline: "There are $N+1$ sellers indexed by $i\in\{1,\dots,N+1\}$." "Each seller is endowed with an indivisible asset and is privately informed of her asset's type, denoted $\theta_i\in\{L,H\}$." Do not open a model section with a roadmap of its subsections or a motivational flourish; open with the economy.

**"We" carries every modeling choice.** "we assume," "we denote," "we refer to," "we restrict attention to," "we start by considering," "we focus on primitives that satisfy," "we set." First person plural, direct.

**Name a concept, then symbolize it.** Give an object an intuitive name (often in quotes) and attach the symbol: an owner "has a private value ... or ``productivity,'' denoted $\omega_{mt}\in\{l,h\}$." "For this reason, when $\omega_{mt}=l$, we say the owner is \emph{shocked}." The name does economic work later.

**Weave interpretation into the setup.** After a parameter restriction, give its content: "we assume $c_H>v_L$, which implies that the common-value component is important enough that adverse selection remains relevant." Offer readings where useful: "One can interpret $c_\theta$ and $v_\theta$ as the present value of the flow payoffs to the seller and buyer."

**Separate substantive assumptions from convenience ones, explicitly — this is a signature.** State an assumption, then say whether it matters. "For simplicity, we assume each owner's status is iid," with a footnote: "independence over time facilitates tractability but is not essential for our main results (see Section X)." Reach for "for simplicity," "for convenience," "for parsimony and tractability," "purely for convenience and can be relaxed," "not essential / not strictly necessary for our results," "simplifies exposition and rules out ...". When several assumptions need this, collect them in a short **"Remarks on Modeling Assumptions"** subsection that says what the assumptions isolate and which can be relaxed.

**Footnotes do real work.** Robustness qualifications, technical conditions, alternative interpretations, and pointers to extensions go in footnotes, so the main text stays clean.

**Formal environments, then intuition.** State Assumptions, Definitions, and Propositions formally, then follow with prose that says what they do: "The first assumption, which we refer to as the ``lemons'' condition, asserts that adverse selection is severe enough to rule out the efficient equilibrium." "This result illustrates that adverse selection is necessary for our main results. The intuition is that ...".

**Motivate a choice by what it isolates or ensures.** "to isolate the reason trade is delayed," "to ensure strategic interactions remain relevant," "which ensures buyers make zero expected profit."

**Connectives, sparing and natural:** "Thus," "Therefore," "Clearly," "Of course," "Notice that," "To fix ideas," and enumerated emphasis in prose ("First, ... Second, ... Finally, ...") rather than bullet lists.

## Tics to avoid

The full list lives in the writing-style skill (read it per the note at the top). In LaTeX model exposition, the most common offenders are `\paragraph{...}` run-ins that are punchy slogan sentences (genuine structural run-ins like `\paragraph{Environment.}` are fine), bullet lists of prose points, and filler intensifiers.

## Workflow

1. If rewriting an existing draft, read it; then read one model section from the corpus to reset the ear.
2. Work section by section, in the user's order: environment and primitives → agents and preferences → market / trading protocol → informational assumptions → formal assumptions with their economic content → a "Remarks on Modeling Assumptions" discussion if warranted → value functions / equilibrium definition → benchmark → results, each proposition followed by intuition.
3. Keep equations, labels, and notation exactly as given; change prose only, unless asked to change the model.
4. Prefer footnotes for caveats, robustness, and alternative interpretations.
5. After drafting, reread against "Tics to avoid" and strip anything that trips it.
6. Produce the prose; do not add editorial meta-commentary about the writing.
