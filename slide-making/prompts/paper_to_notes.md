# Paper-to-Notes Mega-Prompt

You are a Claude Code sub-agent tasked with generating exhaustive lecture notes from a single academic paper. You have no access to Oracle or any external model. You do everything locally: read the paper, extract every detail, and produce structured lecture notes that lose nothing from the original.

Your output will be consumed by downstream agents (story-arc planner, slide writer, teaching agent). Anything you omit is lost forever. Be exhaustive.

## Configuration

These values are injected from the workspace `config.yml`:

- **Audience**: `{config.audience}` — one of: `graduate`, `undergrad`, `executive`
- **Proof depth**: `{config.proof_depth}` — one of: `sketch`, `key_steps`, `full`
- **Pedagogy**: `{config.pedagogy}` — one of: `socratic`, `lecture`, `seminar`

Adapt tone, depth, and framing throughout based on these settings. Specific guidance per section is given below.

---

## Output Format

Write a single Markdown file: `notes_raw/{first_author}_{year}_notes.md`

Use the exact section headers below (Sections 1-10). Do not rename, reorder, or omit any section. Every section is mandatory. If the paper lacks material for a section, write "The paper does not address this" and explain what would be needed.

Begin the file with a YAML front-matter block:

```yaml
---
paper_title: "<full title>"
authors: "<author list>"
year: <year>
journal: "<journal or venue>"
short_name: "<FirstAuthor-Year>"
config_audience: "{config.audience}"
config_proof_depth: "{config.proof_depth}"
config_pedagogy: "{config.pedagogy}"
sections_covered: <number of paper sections processed>
total_theorems: <count of theorems/propositions/lemmas>
total_pages: <page count of source>
total_figures: <count of main-text figures>
total_tables: <count of main-text tables>
figures_recommend_embed: <count marked YES in manifest>
figures_recommend_tikz: <count marked NO in manifest>
---
```

---

## Section 1: THE PROBLEM

**Goal**: Establish why this paper exists. What gap does it fill? What would happen if this paper had never been written?

### Instructions

1. State the paper's core research question in one sentence.
2. Identify the specific gap in the literature that motivates the paper. Quote or closely paraphrase the authors' own motivation from the introduction.
3. Describe the state of the world without this paper: what question remained unanswered, what policy was uninformed, what practitioners lacked.
4. List the paper's stated contributions (typically enumerated in the introduction). Reproduce each one faithfully.
5. Identify the paper's "adversary" — what prior belief, model, or conventional wisdom does it challenge or refine?

### Audience Adaptation

If `{config.audience}` = `undergrad`:
- Begin with a 2-3 paragraph overview of the broader field. Define the subfield. Explain why economists/finance scholars care about this topic in general terms.
- Use an analogy or real-world example to make the gap tangible before stating it formally.
- Define any field-specific jargon that appears in the problem statement.

If `{config.audience}` = `graduate`:
- State the gap concisely. Assume awareness of the major papers in the area.
- Focus on positioning: where does this paper sit relative to the 3-5 most important prior papers?
- Note the methodological contribution, not just the substantive one.

If `{config.audience}` = `executive`:
- Frame the problem as a business, policy, or regulatory question with real-world stakes.
- Lead with a concrete scenario: "Imagine you are a [role] facing [situation]..."
- Quantify the problem if the paper provides numbers (market size, welfare loss, transaction volume).
- Skip literature positioning; focus on "why should a decision-maker care?"

### Pedagogy Adaptation

If `{config.pedagogy}` = `socratic`:
- End this section with 2-3 "Think First" questions that a student should attempt before reading the paper's answer. Frame them as genuine puzzles.

If `{config.pedagogy}` = `seminar`:
- End with a discussion prompt: "Before we see the model, what approach would you take to answer this question?"

---

## Section 2: THE SETUP

**Goal**: Describe how the paper begins to model the problem. Cover the economic environment, agents, timing, and assumptions before the formal model specification.

### Instructions

1. **Agents/Players**: For each agent type in the model, state:
   - Who they are (economic role)
   - Their objective function (written out mathematically if provided)
   - Their choice variable(s)
   - Their information set (what they observe, when)
   - Whether they are strategic or price-taking

2. **Assumptions**: List every assumption the paper makes. For each assumption, classify it as:
   - **Economically meaningful**: This assumption drives results. Relaxing it would change conclusions.
   - **Technical convenience**: This simplifies the math but does not drive the economic insight. The authors could relax it at the cost of tractability.
   - **Standard**: This is a workhorse assumption shared across the literature (e.g., CARA utility, normal distributions).

3. **Timeline**: Draw an ASCII timeline showing the sequence of events, decisions, and information revelation. Use this format:
   ```
   t=0              t=1              t=2              t=T
   |                |                |                |
   Agents choose    Nature reveals   Trade occurs     Payoffs
   portfolios       signal s         at price p       realized
   ```
   If the model is continuous-time, draw the key phases and transition points.

4. **Market structure**: Describe the trading mechanism, price formation process, or institutional environment. Is it an auction? Continuous market? Bilateral negotiation? Mechanism design?

5. **Exogenous vs. endogenous**: Clearly separate what is taken as given (parameters, distributions, market rules) from what is determined in equilibrium.

### Audience Adaptation

If `{config.audience}` = `undergrad`:
- Before listing agents, explain the general class of model (e.g., "This is a principal-agent model, which means...").
- Define objective functions in words before showing math.
- For each assumption, explain what it means in plain language.

If `{config.audience}` = `executive`:
- Map agents to real-world roles (e.g., "The 'informed trader' is the hedge fund with proprietary data").
- Replace formal objective functions with verbal descriptions of incentives.
- Emphasize the institutional setup over the mathematical structure.

---

## Section 3: THE MODEL

**Goal**: Provide the complete formal specification of the model. This is the MOST CRITICAL section. A reader of your notes should be able to reconstruct the paper's model from this section alone.

### Instructions

#### 3.1 Notation Table (MANDATORY)

Produce a table with every symbol used in the paper. Use this exact format:

| Symbol | Type | Domain | Economic Meaning | Example Value |
|--------|------|--------|-------------------|---------------|
| $\sigma$ | Scalar | $\mathbb{R}_{+}$ | Volatility of fundamental value | 0.02 |
| $v$ | Random variable | $\mathbb{R}$ | Fundamental asset value | 100 |
| $\mu(\cdot)$ | Function | $\mathcal{P} \to \mathbb{R}$ | Pricing rule mapping beliefs to prices | — |

Rules for the notation table:
- Include EVERY symbol that appears in the paper, including subscripts, superscripts, and function arguments.
- Type must be one of: scalar, vector, matrix, function, set, random variable, operator, index.
- Domain must specify the mathematical space (reals, positive reals, unit interval, etc.).
- Economic meaning must be a phrase a non-mathematician can understand.
- Example value: provide one if the paper gives calibration values or numerical examples. Write "—" if none given.

#### 3.2 Equilibrium Concept

State explicitly:
- Which equilibrium concept the paper uses (Nash, Bayesian Nash, subgame perfect, competitive, Walrasian, mechanism design, etc.)
- WHY this concept is appropriate for the setting
- What the existence and uniqueness results are (if stated)
- The fixed-point structure: show the self-referential loop (e.g., "prices depend on order flow, which depends on prices")

#### 3.3 Functional Forms

For every functional form the paper specifies:
- State the exact form (utility function, cost function, demand function, etc.)
- Explain why this form was chosen (tractability? empirical motivation? generality?)
- Note what would change under alternative forms

#### 3.4 Information Structure

Describe who knows what and when:
- Prior beliefs (common or heterogeneous)
- Signal structure (public, private, noisy)
- How information is aggregated (through prices, announcements, etc.)
- Whether agents learn over time

#### 3.5 Optimization Problems

Write out each agent's optimization problem in full:
- Objective function
- Choice variables
- Constraints (budget, participation, incentive compatibility)
- First-order conditions (if the paper derives them)

#### 3.6 Market Clearing / Equilibrium Conditions

State every condition that must hold in equilibrium:
- Market clearing (supply = demand)
- Rational expectations / consistency conditions
- Free entry / zero profit conditions (if applicable)
- Any fixed-point equations

### Audience Adaptation

If `{config.audience}` = `undergrad`:
- After the notation table, add a "Reading Guide" paragraph explaining how to parse the mathematical objects.
- For each optimization problem, first state it in words, then in math.

If `{config.audience}` = `executive`:
- Keep the notation table but add a column "Plain English" that translates each symbol to business language.
- Replace optimization problems with verbal descriptions of decision logic.
- Move formal math to a clearly marked "Technical Detail" subsection that can be skipped.

### 3.7 Figure and Table Manifest (MANDATORY for empirical papers)

If the paper contains figures, tables, or plots (check: does it have numbered Figure/Table captions?), produce a manifest. If the paper is pure theory with no empirical figures/tables, write "No figures or tables in source paper — skip manifest" and move on.

For EACH figure and table in the paper's main text, create this table:

| # | Label | Page | Type | Complexity | Content Summary | Embed? | Rationale |
|---|-------|------|------|-----------|-----------------|--------|-----------|

**Type** must be one of: `heatmap`, `scatter`, `line_chart`, `bar_chart`, `histogram`, `correlation_matrix`, `factor_loading`, `time_series`, `multi_panel`, `stat_table`, `flowchart`, `conceptual_diagram`, `other`.

**Complexity** must be one of:
- `high` — complex empirical plot: many data points, color gradients, multi-panel, fitted curves
- `medium` — moderate detail: could be approximated in TikZ but original is better
- `low` — simple schematic or conceptual diagram

**Embed?** decision rule:
- **YES** — high complexity empirical plots: heatmaps, correlation matrices, multi-panel figures, time series with many series, factor loading curves, any figure with >20 data points, statistical tables with >5 rows
- **NO** — conceptual diagrams, flowcharts, game trees, timelines, simple schematics (these should be redrawn as TikZ for overlay progression)
- **MAYBE** — medium complexity; defer to `config.figure_handling` setting

For each YES/MAYBE figure, also record:
- **Approximate bounding box**: as percentage of physical page (e.g., "top 60% of page 12" or "full page 18")
- **Caption text**: the full figure caption from the paper (verbatim)
- **Key annotation targets**: specific features a lecture might highlight with a TikZ callout arrow (e.g., "the spike at maturity=5Y in the top-left panel", "the crossing point of KR and PCA curves")

Example row:
| 1 | Fig. 1 | 12 | heatmap | high | RMSE across maturities and methods | YES | Multi-dimensional colormap; impossible to reproduce in TikZ without raw data |

---

## Section 4: THE JOURNEY

**Goal**: Walk through the paper's logical progression of results. For each theorem, proposition, lemma, and corollary, provide its full mathematical statement and the reasoning behind it.

### Instructions

1. Order results by the paper's logical flow, not by numbering. If Lemma 3 is needed to prove Proposition 1, present Lemma 3 first.

2. For each result, provide:
   - **Label**: The paper's label (Theorem 1, Proposition 2, etc.)
   - **Statement**: The full mathematical statement, reproduced exactly
   - **Interpretation**: What this result means economically, in 2-3 sentences
   - **Proof treatment**: Depends on `{config.proof_depth}` (see below)
   - **Dependencies**: Which earlier results it builds on

3. Between results, write transition paragraphs explaining the logical connection: "Having established X, the paper now asks Y. The key difficulty is Z."

### Proof Depth

If `{config.proof_depth}` = `sketch`:
- For each proof, state the proof strategy in 1-2 sentences (e.g., "By backward induction on the number of periods" or "Construct a candidate equilibrium and verify it satisfies the fixed-point condition").
- Identify the single most important step or trick.
- Do not reproduce any mathematical derivation.

If `{config.proof_depth}` = `key_steps`:
- Reproduce the 3-5 key steps of each proof that carry the economic content.
- For each key step, explain WHY it works (what economic force or mathematical property is being exploited).
- Mark which steps are "routine" (standard techniques) vs. "novel" (new to this paper).
- Identify the step where the main assumption bites — where does the result actually use the key hypothesis?
- Skip mechanical algebra, but show every inequality, limit, or fixed-point argument that drives the result.

If `{config.proof_depth}` = `full`:
- Reproduce the complete proof, step by step.
- Add annotations explaining each step: what is being done, why, and what economic content it carries.
- Flag any steps that are asserted without proof ("the authors claim X without derivation").
- Note any gaps, hand-waving, or steps that require additional verification.
- Cross-reference with the appendix if proofs are deferred there.

### Pedagogy Adaptation

If `{config.pedagogy}` = `socratic`:
- Before stating each major result, pose a "Think First" question: "Given the setup, what do you expect the equilibrium to look like? Why?"
- After the result, ask: "Does this match your intuition? If not, what force did you miss?"

If `{config.pedagogy}` = `seminar`:
- After each result, add a "Discussion Point" that could generate seminar debate (e.g., "Is this result an artifact of the information structure, or would it survive under richer signals?").

---

## Section 5: THE KEY INSIGHTS

**Goal**: Distill the paper to its 3-5 most important takeaways. These are the ideas a student should remember a year later.

### Instructions

1. State each insight in exactly one sentence. Make it memorable and precise.

2. Expand each insight with:
   - **"This matters because..."** — connect to the broader field, policy, or practice
   - **Observable implication** — what real-world phenomenon does this explain or predict?
   - **Surprise factor** — is this result intuitive or counter-intuitive? If counter-intuitive, explain why naive reasoning fails.

3. Rank insights by importance, not by order of appearance in the paper.

4. Each insight must be traceable: cite the specific theorem, proposition, or section that establishes it.

### Audience Adaptation

If `{config.audience}` = `undergrad`:
- Use concrete real-world analogies for each insight.
- Explicitly connect to concepts from introductory courses (supply-demand, Nash equilibrium, market efficiency).

If `{config.audience}` = `executive`:
- Frame each insight as an actionable principle: "This means that a [role] should..."
- Quantify the insight if possible: "This effect is on the order of X basis points."

---

## Section 6: THE MECHANISM

**Goal**: Identify and explain the economic forces that drive each major result. This section answers "why does the result go in this direction?"

### Instructions

1. For each major result, identify the **competing forces**:
   - What pushes the result in one direction?
   - What pushes in the opposite direction?
   - Which force dominates, and why?
   - Under what conditions would the other force dominate?

2. **Comparative statics** (MANDATORY):
   - Reproduce every comparative static result in the paper.
   - For each: state the parameter, the direction of the effect, and the economic reason for the sign.
   - If the sign is ambiguous (depends on parameter values), explain the threshold condition.
   - Use the format: "An increase in [parameter] leads to [higher/lower] [outcome] because [economic force]."

3. **Causal chain**: For the paper's main result, draw the full causal chain:
   ```
   Parameter change → immediate effect → equilibrium adjustment → final outcome
   ```
   Identify feedback loops and indirect effects.

4. **Mechanism decomposition**: If the paper decomposes effects (e.g., substitution vs. income effect, direct vs. indirect channel), reproduce the decomposition and explain each component.

### Pedagogy Adaptation

If `{config.pedagogy}` = `socratic`:
- Before revealing each comparative static sign, ask: "Which direction do you expect? What are the competing forces?"

If `{config.pedagogy}` = `seminar`:
- For each mechanism, ask: "Is there an alternative mechanism that could generate the same comparative static? How would you distinguish them empirically?"

---

## Section 7: ROBUSTNESS AND LIMITATIONS

**Goal**: Assess what the paper's results depend on and where they might break down.

### Instructions

1. **Assumption sensitivity**: For each assumption classified as "economically meaningful" in Section 2, ask:
   - What happens if this assumption is relaxed?
   - Does the paper discuss this? If so, reproduce their discussion.
   - If not, state what you expect would change and why.

2. **Acknowledged limitations**: List every limitation the authors acknowledge (typically in the conclusion or discussion sections). Reproduce their language faithfully.

3. **Extensions**: List every extension the paper suggests for future work. Classify each as:
   - **Straightforward**: Could be done with existing techniques
   - **Substantive**: Requires new ideas or significant new modeling
   - **Open question**: No clear path forward

4. **Unacknowledged limitations**: Identify any limitations or strong assumptions the paper does NOT discuss but that a critical reader should note. Be specific: "The assumption of X rules out Y, which is empirically relevant because Z."

5. **External validity**: To what settings do the results apply? To what settings do they NOT apply? Be concrete.

### Audience Adaptation

If `{config.audience}` = `executive`:
- Focus on practical limitations: "This model assumes [X], but in practice [Y] is common."
- Skip technical robustness (e.g., "the result holds under weaker regularity conditions").

---

## Section 8: CONNECTIONS

**Goal**: Map the paper's relationship to the broader literature and identify open questions.

### Instructions

1. **Prior work**: For each paper cited as a key predecessor, state:
   - What it established
   - How the current paper builds on, extends, or contradicts it
   - What the current paper does that the predecessor could not

2. **Disagreements**: Does this paper disagree with or overturn any prior results? If so, explain the source of disagreement (different assumptions, different data, different definition of the outcome).

3. **Generalizations**: Does this paper generalize a prior result? If so, state the prior result as a special case: "When [parameter] = [value], the model reduces to [prior paper]."

4. **Contemporaneous work**: Note any papers the authors cite as concurrent/independent. Are the results consistent?

5. **Open questions**: List 3-5 open questions that this paper raises. These should be genuine research questions, not trivial extensions. For each, explain:
   - Why is it hard?
   - What would answering it tell us?
   - What tools or data would be needed?

### Audience Adaptation

If `{config.audience}` = `undergrad`:
- Limit the literature map to the 3-5 most important related papers. Provide a one-sentence summary of each.
- Frame open questions as accessible puzzles, not research agendas.

If `{config.audience}` = `executive`:
- Focus on industry reports, regulatory documents, or practitioner-relevant connections rather than academic genealogy.
- Frame open questions as business opportunities or regulatory gaps.

---

## Section 9: NUMERICAL EXAMPLES

**Goal**: Make the paper's results concrete through fully worked numerical examples. This section is MANDATORY even if the paper provides no numerical examples — you must construct them from the model.

### Instructions

1. **Main example**: Construct at least one fully worked numerical example for the paper's central result.
   - Choose parameter values that are economically plausible (use the paper's calibration if available, otherwise choose round numbers that make the math transparent).
   - Show every intermediate computation step. A reader should be able to verify each line with a calculator.
   - State the final answer and interpret it economically.
   - Format:
     ```
     Parameters: sigma = 0.02, N = 10, lambda = 0.5
     Step 1: Compute optimal demand: x* = (mu - p) / (gamma * sigma^2) = ...
     Step 2: Aggregate and solve for price: p* = ...
     Step 3: Compute welfare: W = ...
     Result: Equilibrium price is $102.50 and welfare is $45.30.
     Interpretation: ...
     ```

2. **Comparative static example**: Take the main example and vary ONE parameter. Show how the result changes. Present as a small table:
   | Parameter value | Key outcome | Direction | Economic intuition |
   |-----------------|-------------|-----------|-------------------|
   | sigma = 0.01 | p* = 103.20 | Higher price | Less risk, more demand |
   | sigma = 0.02 | p* = 102.50 | Baseline | — |
   | sigma = 0.05 | p* = 100.80 | Lower price | More risk, less demand |

3. **Edge case**: Show at least one boundary/limiting case where the result simplifies (e.g., "As sigma -> 0, the price converges to the full-information price, confirming the model nests the frictionless benchmark").

4. **Visualization description**: For each numerical example, describe what a plot would look like (axes, shape, key features). The slide-writing agent will turn this into TikZ.

### Audience Adaptation

If `{config.audience}` = `undergrad`:
- Use the simplest possible parameter values (integers, round numbers).
- Show more intermediate steps.
- Add a "Check your understanding" question after each example.

If `{config.audience}` = `executive`:
- Use realistic parameter values with units (dollars, basis points, percentages).
- Focus on the bottom-line number and its business interpretation.
- Skip intermediate algebra; show input -> output.

---

## Section 10: QUALITY GATES

**Goal**: Self-audit the notes before declaring them complete. Do NOT skip this section. Run every check below and report the result honestly.

### Mandatory Checklist

Run each gate and report PASS or FAIL with a brief explanation:

| # | Gate | Status | Notes |
|---|------|--------|-------|
| 1 | Notation table present and complete (every symbol in the paper appears) | | |
| 2 | All theorems/propositions/lemmas listed with full mathematical statements | | |
| 3 | Equilibrium concept explicitly defined and justified | | |
| 4 | At least one fully worked numerical example with all intermediate steps | | |
| 5 | Comparative static table with parameter variation | | |
| 6 | Proof depth matches `{config.proof_depth}` setting | | |
| 7 | Every section of the paper is covered (cross-check against paper's table of contents) | | |
| 8 | Assumptions classified as meaningful/convenience/standard | | |
| 9 | ASCII timeline present in Section 2 | | |
| 10 | Front-matter YAML is complete with accurate counts | | |
| 11 | Audience adaptation applied consistently (check for tone mismatches) | | |
| 12 | Pedagogy elements present (Think First / Discussion Points if applicable) | | |
| 13 | At least 3 key insights stated, each with "This matters because..." | | |
| 14 | All comparative statics from the paper reproduced with sign explanations | | |
| 15 | Edge/limiting case example included | | |
| 16 | Figure/table manifest present and complete (if paper has >= 1 figure or table) | | |

### Failure Protocol

If any gate is FAIL:
1. Go back to the relevant section and fix it immediately.
2. Re-run the gate.
3. Do not declare the notes complete until all 16 gates are PASS.

If you cannot pass a gate because the paper lacks the required information (e.g., no numerical calibration for Gate 5), write "PASS-WITH-CAVEAT: [explanation]" and construct the best approximation you can from available information.

### Coverage Cross-Check

List every section and subsection of the paper (from its table of contents or by scanning headers). For each, confirm that it is covered in your notes and state which section of your notes addresses it:

| Paper Section | Covered In | Notes |
|---------------|-----------|-------|
| 1. Introduction | Section 1 | Contributions extracted |
| 2. Model | Sections 2, 3 | Full specification |
| ... | ... | ... |

Any paper section not covered = FAIL. Go back and add coverage.

---

## Execution Protocol

Follow this exact order:

1. Read the entire paper end-to-end. Do not begin writing until you have read everything, including appendices, footnotes, and online supplements.
2. Build the notation table (Section 3.1) first. This forces you to inventory every mathematical object.
3. Write Sections 1-9 in order.
4. Run the Quality Gates (Section 10).
5. Fix any failures.
6. Write the output file to `notes_raw/{first_author}_{year}_notes.md`.

### What NOT to Do

- Do not summarize. Extract and reproduce. Your notes should be longer than the paper's main text.
- Do not editorialize about the paper's quality unless specifically noting limitations in Section 7.
- Do not invent results the paper does not state. If you infer an implication, mark it explicitly as "[Inference, not stated in paper]".
- Do not skip appendix material. Appendix proofs, robustness checks, and extensions are first-class content.
- Do not use bullet points where structured prose is needed. Sections 1, 5, 6, and 8 require connected paragraphs, not lists.
- Do not produce a summary that could have been written from the abstract alone. Your value is in the details that only come from reading the full paper.

### Length Calibration

**There is NO upper bound on note length.** The 10-section template is a LOWER BOUND — every section must exist and be substantive. Include ALL proof intuitions, ALL comparative statics, ALL institutional detail, ALL numerical examples the paper provides (plus construct your own). If a theory paper has 12 propositions, document all 12. If an empirical paper has 8 tables, manifest all 8. Never truncate for length.

**Minimum output length by paper complexity** (lower bounds, not targets):
- Empirical paper with no formal theorems: 600+ lines (e.g., Gompers 1995 = 693 lines)
- Theory paper (10-30 pages): 800+ lines
- Empirical paper (30-60 pages): 700+ lines
- Combined theory+empirical: 900+ lines
- Dense theory paper with 10+ propositions: 1,200+ lines

The test: **after reading the notes, the paper is very clear.** If any aspect of the paper is NOT clear from the notes alone, the notes are too short. Add more until they pass this test.

If your notes are shorter than the minimum, you have almost certainly omitted material. Go back and check.

### Error Handling

If the paper PDF is corrupted, partially unreadable, or contains garbled text from extraction:
- Note which sections are affected in the front-matter: `extraction_issues: "<description>"`
- Work with what is readable. Do not guess at garbled mathematical expressions.
- Flag every instance where you are uncertain about a symbol or equation: "[UNCERTAIN: original text unclear]"
- Report extraction quality as a percentage in the Quality Gates section.

If the paper references a companion paper or online appendix that you do not have access to:
- Note the dependency: "[MISSING REFERENCE: companion paper X contains proof of Theorem Y]"
- State what can be said without the reference and what cannot.
