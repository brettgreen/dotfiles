# Ruizhe's Slide-Making Principles

These principles are extracted from iterative feedback during slide creation. They are **mandatory** — check this file before creating or editing any slide content.

**This is the global canonical copy.** Project-specific overlays (if any) live in `{project}/SLIDE_PRINCIPLES_OVERLAY.md`.

## Tier 1: Absolute Constraints (never violate)

### P1. New Objects Get a Full Walkthrough
When introducing any object students haven't seen before (CI put, bonding curve, PGA mechanism, etc.):
- Build it step by step from something they already know
- Add a **visual/TikZ at every step** of the construction
- **Test**: Can someone who has never seen this understand each step with the diagram alone?
- Never compress a new concept into bullet points. If you can't draw it, you haven't explained it.

*Source: CI put walkthrough (2026-02-17). Original version compressed 3 features into bullets. Correct version: 7 frames, each with a diagram building one layer.*

### P2. Never Show Something Wrong
If a diagram or formula represents a concept, it must be **correct at every overlay stage**. A partially-built diagram that looks like a wrong answer is worse than no diagram.
- If building incrementally, make sure each visible state is either clearly incomplete (labeled "step 1 of 3") or correct on its own.

*Source: P&L graph incident (2026-02-17). Original 3-region P&L was the final answer shown immediately — but the shape was misleading without the limit-order buildup.*

### P3. Build from Simplest Case, Not the General Case
Don't show the full v3 range payoff first. Start with **one tick** at one price, work through what happens, then generalize.
- Single tick → understand the mechanism → multiple ticks → full range
- One period → understand the forces → continuous time

*Source: Limit order bars → single tick → payoff shape redesign (2026-02-17).*

### P4. Story Arc Between Papers Must Be Explicit
When transitioning between papers/acts, the bridge must answer:
1. What did the previous paper establish? (one sentence)
2. What **gap** does it leave? (the tension)
3. What new object/idea does the next paper introduce to fill it?
- The gap must be a **real question students can feel**, not just "now we do the next paper."

*Source: Act I → Act II bridge redesign (2026-02-17). Original bridge jumped to "can we price forward-looking?" without explaining why European → American matters or what the CI put is.*

### P5. Every Concept Gets a Visual
Before finalizing any frame that introduces a new mechanism, force, or object, ask: **Can a student immediately see this?** If not, add a diagram.
- Equilibrium conditions → intersection diagrams
- Regime transitions → threshold visuals
- Timelines → sequential TikZ
- Tradeoffs → two-box or bar comparison
- New financial instruments → payoff/delta diagrams
- **Multi-step processes → TikZ pipeline diagram, never numbered bullet points.** Show where value/risk enters at each stage. A 5-step process as enumerate is a failed frame.
- **Vocabulary/definitions → show the pattern visually.** If defining 4 attack types, draw each as a transaction-ordering pattern, not a bullet list.

*Source: Visualization gap audit (2026-02-17). 11 frames had concepts without diagrams. DEX timeline/MEV vocabulary feedback (2026-02-18): "5 bullet points without a diagram doesn't help anyone understand where risk enters."*

### P6. Every Result Needs a Clear, Simple Intuition
No matter how complex a theorem or proposition, it must come with a simple, accessible explanation that a student can grasp without working through the math.
- Complex result → strip it down to the core force or tradeoff in one sentence
- Use analogies from familiar domains when available (pixel resolution, subscriptions, rent)
- The intuition slide should come before or immediately after the formal statement
- If you can't explain it simply, you haven't understood it well enough to teach it

*Source: Theorem 6 band bound discussion (2026-02-18). The formal error bound |ε| ≤ r·K* needed an intuitive walkthrough: "match your band to a CI put's holding region, and LVR becomes like paying rent."*

### P19. Logical Progression: Problem → Plan → Guess → Reveal → Name
Every concept sequence must follow a logical progression where students learn one thing at a time along the flow. For a story/example (like Dark Forest): (1) What is the problem? (2) What is the plan? (3) Let students guess what happened. (4) Reveal what really happened. (5) Name the concept ("this is what they call a frontrunning attack"). Never dump the whole concept in one frame. Break it into frames where each frame adds exactly one new piece.

*Source: Week 8 Monday review (2026-02-22). Dark Forest story was compressed into one frame. Should be 3-4 frames with guessing and reveal.*

### P20. Never Assume Prior Knowledge on DeFi Primitives
Before introducing any attack or mechanism that relies on a DeFi primitive (lending, AMM, LP positions, liquidation), FIRST explain that primitive step by step with institutional detail. Liquidation MEV requires first explaining DeFi lending. LP sandwich requires first explaining how LP deposits work in concentrated liquidity. Assume students have zero background on every new DeFi concept.

*Source: Week 8 Monday review (2026-02-22). Liquidation MEV frame assumed students knew how DeFi lending works. They don't.*

### P21. Three Gates Before Any Slide (MANDATORY)
Every slide or slide sequence must pass three gates in order:
1. **Gate 1: Deep Research.** Make sure YOU understand every institutional detail perfectly. Get the mechanics right. If CEX-DEX arb isn't truly atomic, say so.
2. **Gate 2: Visualization Design.** Think about the best way to gradually show people what's going on. Design the visual progression BEFORE writing any LaTeX. What does each overlay reveal?
3. **Gate 3: Execute.** Only then write the TikZ/beamer code.
Never skip to Gate 3. A badly researched or badly designed slide wastes more time than starting over.

*Source: Week 8 Monday review (2026-02-22). Multiple TikZ diagrams were "badly designed" because visualization was not planned before coding.*

### P23. Never Jump Into a Model Without Context
When presenting a paper, NEVER start with "The Agents" or "The Model Setup." First establish: (1) What is the real-world context? Introduce the institutional objects (e.g., private pools) concretely. (2) What is the motivating question? Frame it as something students care about (e.g., "Is MEV a pure transfer or genuine waste?"). (3) What is the logical progression the paper follows? Walk students through the paper's own reasoning, not just its formal structure. Only THEN introduce the model — and when you do, visualize every agent, every choice, every stage. Text descriptions of model agents = failed frame.

*Source: Week 8 Monday review (2026-02-22). Act II jumped straight to "The Agents" and "The Sequential Game" without motivating context. "This is the worst way of talking about a paper."*

### P24. Frontier Topics = Student Thinking Territory
When introducing unsettled topics (execution tickets, L2 MEV, FOCIL), the goal is NOT to present settled answers. Give enough institutional context that students can form opinions and debate. Frame these as open questions, not lectures. "Here's how it works, here's what's unresolved — what do you think?"

*Source: Week 8 Monday review (2026-02-22). Act IV should give institutional detail on PBS/L2/execution tickets as thinking territory for students.*

### P22. Ask "Why Is This Possible Here But Not There?"
When introducing an attack or mechanism, ask students: why is this possible in an AMM/blockchain but NOT in a traditional centralized exchange? This comparison deepens understanding and connects to TradFi knowledge they already have. E.g., "Why is sandwich only possible in an AMM? Could you do this on NYSE?"

*Source: Week 8 Monday review (2026-02-22). Sandwich attack was presented without asking why it's AMM-specific.*

## Tier 2: Strong Defaults (follow unless context demands otherwise)

### P7. Think First → Reveal Pattern
For every major result, first ask students to think about it, then reveal. The Think-First prompt should be a question they can actually attempt, not a rhetorical question.

### P8. Concrete Numbers Before Abstraction
When a theorem has parameters, show a **toy numerical example** immediately after. Students anchor on numbers, not Greek letters.

### P9. Side-by-Side Comparisons for Equivalences
When claiming "A is equivalent to B" (LP = covered call, CI put delta = liquidity tick), show both objects **side by side** on the same frame with matching visual structure.
- **TradFi-DeFi comparisons → parallel flow diagrams with named examples.** Not just a table. Show "Retail → Broker → Wholesaler" alongside "User → Private mempool → Builder" with concrete names and dollar amounts where possible.
- Every comparison should make a student say "oh, it's the same thing with different labels."

*Source: PFOF/internalization feedback (2026-02-18): "What is PFOF as a graph? What is private orderflow in DeFi? Give a concrete example."*

### P10. One New Idea Per Frame
Don't stack two independent concepts on one frame. If a frame has "and also..." it should be split.

### P11. Pitch Before Theory
Before diving into a paper's formalism, give a **concrete scenario** that makes the theory feel necessary. "You're a market maker with $10M, someone offers you 10% yield..."

*Source: Motivating pitch frames (2026-02-17). Added before the options lens hook.*

## Tier 3: Follow Unless Impractical

### P12. TikZ Scale 0.80-0.95 for Complex, 1.0 for Simple
After P29 (no `transform shape`), nodes are full-size so scales need to be higher. Prevents overflow while keeping diagrams readable.

### P13. Stanford Colors Consistently
StanfordRed = bad/loss/informed, StanfordGreen = good/success, StanfordBlue = neutral/reference.

### P14. Mechanism Box After Every Diagram
After a TikZ diagram, include `\mechanism{}` or `\keyinsight{}` explaining what the picture shows in words.

### P15. Frame Titles Should Be Complete Sentences or Claims
"The Delta Becomes a Step Function" > "Delta Step Function" > "Lemma 1"

### P17. Hooks Are Questions, Not Statements
When you have a powerful concept (e.g., "12 seconds of absolute power"), make it a question first. Ask students to answer — "What happens in those 12 seconds? Who decides?" — before revealing the answer. A hook that tells is a missed opportunity. A hook that asks creates engagement from frame 1.

*Source: Week 8 Monday review (2026-02-22). "12 Seconds of Absolute Power" was a statement with stats. Should be a question students attempt to answer.*

### P18. Don't Force Weak Bridges Between Weeks
If the connection between this week and last week isn't naturally strong, don't manufacture a ceremonial "last week we learned X, this week we do Y" bridge frame. Instead, directly state the gap — what we're doing today and why it matters. Cut the bridge frame entirely if it adds nothing.

*Source: Week 8 Monday review (2026-02-22). Week 7→8 bridge frame ("We know MEV exists") was weak and unnecessary. Just state the gap directly.*

### P25. Every Multi-Step TikZ Gets Overlay Progression
Any TikZ diagram showing a pipeline, process, timeline, flow, or multi-step mechanism MUST use `\pause`, `\onslide`, or `\only` to reveal steps progressively. The student sees step 1, processes it, guesses what comes next, then step 2 appears. Showing the full diagram at once = telling the answer before asking the question.
- **Test**: If the diagram has 3+ nodes in sequence (A → B → C), it MUST have overlays. No exceptions.
- **Comparison diagrams** (side-by-side A vs B) should show one side first, then reveal the other.
- A static pipeline is a failed pipeline. James Cameron doesn't show the whole scene in one frame — he reveals it shot by shot.

*Source: Week 8 Monday review round 2 (2026-02-22). 52 out of 58 TikZ diagrams were static. "Pre-Merge Ethereum: Miners Do Everything" showed Users → Mempool → Miner → Block all at once. "If you ask James Cameron, they will say it is not vivid and clear enough."*

### P27. Setup Before Attack — Show the Calm Before the Storm
Every attack, mechanism, or disruption diagram MUST start with an equilibrium/calm state overlay BEFORE the action begins. Students need to see the world in equilibrium so they can feel what changes. Without this anchor, students arrive mid-crisis with no reference point.
- Sandwich attack: show empty block + flat price line → THEN frontrun happens
- CEX-DEX arb: show both venues synchronized at $2,000 → THEN news drops one
- Liquidation: show healthy collateral position → THEN price drops
- Any supply chain disruption: show the normal flow → THEN show the break
- **Test**: Does overlay 1 show a state where "nothing is wrong yet"? If not, add a setup overlay.

*Source: Week 8 Monday overlay revision (2026-02-23). Sandwich started mid-attack, CEX-DEX started post-news. Adding equilibrium overlays transformed comprehension.*

### P28. Logical Progression, Not Mechanical Reveals
Overlays must build CONCEPTUAL meaning, not just reveal boxes in order. Each overlay step should answer "what changed and why?" — not just "here's the next box." The test: does each overlay step correspond to an EVENT or FORCE (price moves, news arrives, threshold crossed), or just to the next element in a diagram?
- **Good**: Price chart builds with each transaction → student sees price impact accumulate
- **Good**: Venue prices start equal → news drops one → gap appears (causal chain)
- **Bad**: Box1 appears → Box2 appears → Box3 appears (no causal connection)
- **Bad**: Full pipeline revealed left-to-right with no conceptual anchor at each step
- A cycle diagram (problem → fix → centralization → new fix) is logical because each arrow represents a CAUSAL step students can reason about.

*Source: Week 8 Monday overlay revision (2026-02-23). "We only have progression literally but the logical progression is not there." — 52/58 diagrams had mechanical reveals.*

### P26. TikZ Boundary Safety — No Text May Touch Frame Edges
Every TikZ diagram must maintain safe margins from frame boundaries:
- **Bottom**: No element (including keyinsight/mechanism boxes below the TikZ) may be clipped by the footer. Leave ≥ 10pt clearance.
- **Sides**: No node text may extend past visible frame width. Use `text width` constraints on long labels.
- **Top**: No element within 5pt of frame title bottom.
- **Test**: After compilation, spot-check every TikZ page with `pdftoppm`. Any clipped or overlapping text = FAIL. Fix before presenting.

*Source: Week 8 Monday review round 2 (2026-02-22). Multiple frames had text overlapping with frame borders and footer bar.*

### P29. Minimum TikZ Font = Body Text
No text inside any TikZ diagram may render smaller than the frame body text (`\small` / ~10pt on 11pt beamer). Enforcement rules:
- **Remove `transform shape`** from all diagrams. With `transform shape`, canvas `scale` compounds with font sizes (e.g., `\scriptsize` at scale=0.68 = 5.44pt). Without it, fonts render at declared size regardless of scale.
- **`font=\small` is the minimum** for all nodes, edge labels, and annotations. `\scriptsize`, `\footnotesize`, and `\tiny` are NOT acceptable inside TikZ.
- After removing `transform shape`, increase scale (0.80-0.95) and widen coordinate spacing to compensate for physically larger nodes.
- **Test**: grep for `transform shape`, `\tiny`, `\scriptsize`, `font=\footnotesize` in TikZ environments. All must be zero.

*Source: Week 8 Wednesday font audit (2026-02-24). 37 of 45 diagrams had transform shape with fonts as small as 3.7pt. Systematic fix: 10 parallel fixer agents + 20 audit agents + 2 convergence iterations.*

### P30. Title Slides Need One Signal, Not a Mechanism Diagram
Title, section-break, and agenda slides should set the room, not teach the whole mechanism. If a clean title slide is already working, improve it by sharpening hierarchy, subtitle, venue fit, and at most one subtle visual signal. Do **not** add a second slide's worth of content.
- Good title-slide improvements: a more precise subtitle, a cleaner event label, stronger whitespace, a faint low-information visual cue, or a short motif such as `fees · execution · timing · liquidation`.
- Bad title-slide improvements: full pipelines, multi-box diagrams, charts, arrows, definitions, or anything the audience must read carefully before the talk has started.
- Test: If the title slide now explains the argument rather than inviting the audience into it, it has become an overcrowded content slide. Move the mechanism to slide 2 or later.

*Source: Stanford Governance Summit HL retail title-slide revision (2026-05-02). A clean title slide became worse after adding a market-record/order-book/bill pipeline; the right fix was to keep the clean layout and only adapt the conference framing.*

### P16. Read ALL Source Materials Before Writing Slides
Before any slide production: (1) read the reading list, (2) read every paper note one by one, (3) ask for/locate the paper tex/pdf and figures, (4) fetch and read all blog/web sources from the reading list, (5) inventory all available figures. Only then design the story arc and write slides. Skipping this step = shallow content + missing visuals + procedure breach.

*Source: Week 8 Monday incident (2026-02-20). Slides were written without reading blog sources or using paper figures.*

---

## Changelog

| Date | Principle | Source | Project |
|------|-----------|--------|---------|
| 2026-02-17 | P1 (new objects walkthrough) | CI put feedback | MSE347/week7 |
| 2026-02-17 | P2 (never show wrong) | P&L graph incident | MSE347/week7 |
| 2026-02-17 | P3 (simplest case first) | Limit order redesign | MSE347/week7 |
| 2026-02-17 | P4 (explicit paper bridges) | Act I→II bridge | MSE347/week7 |
| 2026-02-17 | P5 (every concept visual) | Visualization audit | MSE347/week7 |
| 2026-02-17 | P11 (pitch before theory) | Motivating scenario | MSE347/week7 |
| 2026-02-18 | P6 (every result needs intuition) | Theorem 6 band bound discussion | MSE347/week7 |
| 2026-02-18 | P5 (processes → pipeline TikZ) | DEX timeline/MEV vocabulary | MSE347/week7 |
| 2026-02-18 | P9 (comparisons → flow diagrams) | PFOF/internalization feedback | MSE347/week7 |
| 2026-02-21 | P16 (read ALL sources first) | Week 8 Monday rewrite | MSE347/week8 |
| 2026-02-22 | P17 (hooks are questions) | "12 Seconds" review | MSE347/week8 |
| 2026-02-22 | P18 (don't force weak bridges) | Week 7→8 bridge cut | MSE347/week8 |
| 2026-02-22 | P19 (logical progression) | Dark Forest compression | MSE347/week8 |
| 2026-02-22 | P20 (never assume prior knowledge) | Liquidation MEV | MSE347/week8 |
| 2026-02-22 | P21 (three gates mandatory) | TikZ design-first | MSE347/week8 |
| 2026-02-22 | P22 (why here not there) | Sandwich AMM-specific | MSE347/week8 |
| 2026-02-22 | P23 (never jump into model) | Act II paper presentation | MSE347/week8 |
| 2026-02-22 | P24 (frontier = student territory) | Act IV design | MSE347/week8 |
| 2026-02-22 | P25 (overlay progression mandatory) | 52/58 static TikZ audit | MSE347/week8 |
| 2026-02-22 | P26 (TikZ boundary safety) | Text-frame overlap | MSE347/week8 |
| 2026-02-23 | P27 (setup before attack) | Sandwich/CEX-DEX overlay revision | MSE347/week8 |
| 2026-02-23 | P28 (logical not mechanical) | "Progression literally but not logically" | MSE347/week8 |
| 2026-02-24 | P29 (min TikZ font = body text) | Font audit: 37/45 diagrams too small | MSE347/week8 |
| 2026-05-02 | P30 (title slides: one signal, not mechanism) | Stanford Governance Summit title-slide revision | HL_retail |
