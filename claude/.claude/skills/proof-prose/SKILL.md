# Proof-Prose Skill (appendix and technical writing that does not read like AI)

Use this skill whenever drafting or revising proofs, appendix facts and lemmas,
or any technical derivation prose. It layers on top of `writing-style` and
`model-writing`. Its origin: Mark Westerfield flagged eleven proof passages in
Draft_v7_MW.tex (the \DC{...} markups, 2026-09) as reading like AI; every one
was machine-drafted. This skill encodes what those flags teach.

## The register

A proof establishes; it does not explain. Sentences in a proof should be steps
of the argument. Intuition, glosses, and sentences that teach the reader why
something is true belong in the main text; inside a proof they are the
exception, not the rule — at most a brief signpost where the argument's purpose
is genuinely unclear ("It remains to rule out $L=0$.").

One step per sentence. Every sentence has an explicit subject that is a defined
mathematical object or "we". Brevity comes from asserting straightforward steps
(state them once, without justification), never from fusing several steps into
one clause. The reader should be able to point at each sentence and name the
single inference it performs.

The calibration exemplar is Felix's rewrite of a tie-breaking rule:

> If stopping and continuing yield the same value, we select stopping. If
> several first rungs yield the same value conditional on continuing, we select
> the highest one. We apply this rule again to the optimal continuation above
> each selected rung.

Three sentences, three rules, no compression, no coinage. Match this.
(Match its *structure* only: the vocabulary in it — "stopping", "continuing" —
was later retired from the paper; see tic 9. The whole selection rule was
ultimately deleted in favor of a definition, the best outcome of all.)

## Tics that read as AI (each was flagged in a real draft)

1. **Anthropomorphized mathematics.** Objects do not act like people.
   - flagged: "a worker standing alone", "the winner is the human ladder...",
     "climbing the blocks", "the condition forces $L>0$", "a convex kink cannot
     sit at an interior optimum", "$U$ is pinned", "absorbed by the mix".
   - cure: "the optimal support is empty", "the optimal AI configuration is...",
     "move up the two blocks one rung at a time", "the assumption rules out
     self-employment", "convexity rules out a kink at an interior optimum",
     "$U$ equals the tie utility", "a fall in $r$ changes only the mix".

2. **Gerund-fused sentences carrying several steps at once.**
   - flagged: "Approaching $U^*$ from within $B$ along configurations attaining
     $\bar R$, the closed graph of $\mathcal{C}$ yields $c\in\mathcal{C}(U^*)$
     with $R(U^*,s^c)\geq0$, so $\bar R(U^*)\geq0$."
   - cure: "Take $U_k\uparrow U^*$ with $U_k\in B$ and, for each $k$, a
     configuration $c_k$ attaining $\bar R(U_k)$. By the closed graph of
     $\mathcal{C}$, a subsequence converges to some $c\in\mathcal{C}(U^*)$ with
     $R(U^*,s^c)\geq0$. Hence $\bar R(U^*)\geq0$."

3. **Coined shorthand never defined.** "the stopping branch", "within 1 of
   $p(U)$", "variables that interact", "a convexity structure", "mirror-image
   structure", "clone point". Either define the term where the paper defines
   terms, or spell the condition out ("configurations with
   $P_c(U)\geq p(U)-1$"). Use only the paper's defined vocabulary (replacement,
   re-training, transition, chain, block, support, completion).

4. **Rhythmic parallelism and tricolons.** "once optimal, stays optimal at
   higher knowledge, and standing alone, once optimal, stays optimal at lower
   knowledge" reads as cadence, not mathematics. State each monotonicity as its
   own plain sentence.

5. **Em-dash asides mid-proof.** "---the observation that separates tied
   ladders---" interrupts a derivation to editorialize. Promote the aside to its
   own sentence ("Differentiability is what separates tied ladders.") or cut it.

6. **Bare-formula justifications.** "(at $a=1$, by
   $\kappa-[U+z(q_0)]-h(1-q_0)\kappa\geq0$)" cites a formula as if it were a
   reason. Write the clause: "at $a=1$ the change is $\ldots\geq0$", and name
   the fact that delivers the inequality.

7. **Proving the immediate.** A sentence that derives a claim by rearrangement,
   substitution, or a monotonicity transfer writes out what the reader does in
   their head.
   - flagged: "Rungs increase and $z$ is increasing, so every rung satisfies
     $z(q)\leq z(q_L)\leq 1/h-U$ and lies weakly below $\bar q_U$" — the stated
     rung bound is an immediate consequence of the inequality just proven.
   - cure: end the proof at the substantive step. If the statement has a
     residual clause that follows immediately, silence is correct; at most
     write "the rung bound is immediate." This is the proof-level form of the
     brevity rule: assert straightforward steps, and do not even assert the
     trivial ones.

8. **Written for someone who already knows the argument.** AI-drafted proofs
   read as if composed from the inside: objects are used before they are
   introduced, a quantity appears with a name the reader meets three lines
   later, and compressed passages parse only on a second read. The test is the
   first-time reader: someone meeting the argument for the first time must be
   able to follow each sentence without looking ahead. Introduce an object
   before using it; when a step's purpose is not obvious, say in a few words
   what it is for ("It remains to rule out $L=0$."); never rely on the reader
   reconstructing the plan from the conclusion.

9. **Cute verbs and picture nouns. Stick to basic prose.** (Brett, 2026-09-03:
   "don't use colloquial verbs or nouns here. stick to basics.") Banned once
   flagged, and the pattern generalizes: *stopping/continuing* (name the value
   equation instead: "$V(y)=y$", "$T(y)=h(1-y)\kappa$", "$W(q)=w(q)$"),
   *peeling*, *climbing/the climb/the ascent*, *splice*, *junction*, *pincer*,
   *exchange (as a name)*, *tails*, *empty chain* (say "$V(y)=y$" or "the chain
   above $y$ is empty" only where the emptiness itself is the point),
   *contributes* (a slope is "a subgradient at", never "contributed"),
   *placing AI next*, *standing alone*, *utility climbs*, *earns its keep*,
   *beats* (prefer "is cheaper than", "exceeds"), *wins / never wins*,
   *delivers* ("\eqref{...} delivers the margin" → state the inequality),
   *the winner* (say "the optimal configuration"; a locally defined term like
   "frontier winner" is still worse than the plain name), possessive noun
   framings ("Its margin is $s-s_h=\dots$" → "For this configuration,
   $s-s_h=\dots$"). The neutral verbs are: is,
   gives, attains, satisfies, implies, follows, minimizes, maximizes, exceeds.
   If a sentence needs a vivid verb to be clear, the sentence is doing
   explanation that belongs in the main text.

10. **Extra words.** Cut with no mercy: glosses appended after a colon that
    restate the math in words ("...: the tie cannot survive an improvement"),
    consequences re-derived in prose ("...): total finding effort expands"),
    inequality chains the hypothesis makes immediate ("$h(1-x')<h(1-x)$" when
    $x<x'$ is in scope), substitution parentheticals for a citation whose
    application is plain ("(with $f=V$ and $g=w$)" — keep such a parenthetical
    only when the direction of the conclusion is genuinely unobvious, e.g. a
    minimization with a decreasing weight), coefficient names introduced only
    to be explained ("at coefficient $c=h(1-x)$: the mass of the layer being
    hired" — write the objective with $h(1-x)$ inline), and roadmap sentences
    at proof openings. Generic-function names in a stated fact must not collide
    with the paper's parameters (an $f$-and-$g$ lemma in a paper where $f$ is
    finder productivity reads as a bug; use letters the paper does not use).

## Organization (Brett, 2026-09-03)

The exemplar proof is Proposition 1's, in full: "The human layers above solve
the chain problem above $q^A$, in which $\kappa$ does not appear, and the
layers below solve the block problem, in which $q^A$ does not appear. By
Fact A.4, the chain's rungs weakly rise with $q^A$ and the block's rungs
weakly rise with $\kappa$." No opener, no restated hypothesis, no insurance
coda — the operative steps only.

- **No `\emph{...}` step titles in proofs.** Enumerate the statement into
  (i), (ii), ... — in the order the proof establishes them (reorder the
  statement, not the proof) — and open each proof paragraph "For (i), ...".
  A shared intermediate step precedes the parts as a plain opening block
  ("We first show ...", stated as the claim itself, no title).
- **No roadmap sentences** at proof openings ("We parametrize each
  equilibrium condition by..."), no restated hypotheses as headers
  ("Part (i): a qualified AI"), no insurance codas covering cases outside
  the stated hypothesis.
- **Do not promote a defined scalar to a function silently.** If the
  preliminaries define "the crossing $\kappa_a$" at fixed parameters,
  writing "$\kappa_{a'}(q^A)$ are continuous functions" uses notation never
  introduced; say "each crossing $\kappa_{a'}$ is continuous in $q^A$".
- **Before wording a passage, state to yourself what it claims** in two or
  three numbered steps; if that cannot be done, the passage is explanation,
  not proof, and should be cut or moved to the text.

## Workflow

1. Draft with one inference per sentence, subjects explicit.
2. Reread hunting the ten tics above; rewrite any sentence that trips one.
   For tic 7, delete any sentence whose content the reader reconstructs by
   rearrangement or monotonicity. For tic 8, reread once more as a first-time reader: stop at the first
   sentence that requires knowledge of what comes later, and fix it.
3. Check every noun against the paper's terminology key; no new names.
4. Apply `writing-style`'s brevity pass last: cut words, never merge steps.
