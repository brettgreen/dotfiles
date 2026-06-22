# Stanford HTML Slide Generation

Use this prompt when the deck is destined for browser viewing (online seminar, governance summit, internal presentation, trade-map district tour). Mandatory for any HTML output by default — generic HTML is only the fallback when Stanford palette is inappropriate.

## Required pre-reads

Before writing a single slide:

1. `references/stanford_visual_grammar.md` — palette, typography, components, story-arc rules
2. `references/slide_principles.md` — global P1–P30 (no bullet-only slides, every concept gets a visual, etc.)
3. `templates/stanford_html_template.html` — copy this as the starting skeleton

If any of these has not been read in this session, read it before generating.

## Inputs

1. Either: combined lecture notes (paper-derived) OR a topic brief (e.g., "build a deck for trade-map District 5 Treasury Mountains, 5 cities").
2. `config.yml` — audience, depth, theme accent color (the deck's protagonist color), date.
3. Any reference figures or screenshots in `material/`.

## Output

ONE self-contained `.html` file. No build step required. Reveal.js loaded from local `node_modules/` if available, else from CDN.

## Structural contract (non-negotiable)

The deck's `<section>` order MUST follow:

1. **Title** — `<section class="slide-title">`. Author block + cardinal rule + date. One signal, no mechanism diagram (P30).
2. **Hook** — a single question + 4–6 SVG nodes appearing one at a time via `class="fragment fade-in" data-fragment-index="N"`. End with a question or tension sentence.
3. **News hook OR big number** — large Playfair number (e.g. `$39.6B`) + comparison bar chart. Establishes "this matters."
4. **Academic / structural question** — 4-card grid using `.schema-card`, one card highlighted with `--cardinal-soft` background + `--cardinal` top border. This is the question the rest of the deck answers.
5. **Setup / dataset / map zoom** — schema-card grid OR an `.anim-cols` table OR a continent-map fragment.
6. **Mechanism walkthroughs** — one new object per slide (P1, P3). Each has an inline SVG that builds via fragments. Use `.callout-think` *before* any reveal so the audience commits.
7. **Numbers slide** — 4 `.bigstat` panels in a row (large Playfair number + uppercase letter-spaced label).
8. **Connections** — show how this content joins the larger map (trade routes, related papers, downstream lectures).
9. **Punchline** — `<section class="slide-center">` with `.bigtext` two-line quote. Italic cardinal accents on emphasized words.
10. **End card** — "where to next" + 2-3 follow-on links.

If the deck is for a multi-part series (e.g., trade-map districts), include a **city-banner** strip at the top of each city's first slide:
```html
<div class="city-banner">
  <span class="city-id">5.3</span>
  <span class="city-name">Treasury basis trader</span>
  <span class="city-pos">City 3 of 5 · D5</span>
</div>
```

## Component usage

| Component | When to use | Don't use it for |
|---|---|---|
| `.callout` | Synthesis sentence, "the lesson is …", calm conclusion | A regulatory boundary (use `.callout-warn`) |
| `.callout-warn` | FINRA / SEC / CFTC boundary, stress scenario, kill switch | A neutral conclusion |
| `.callout-think` | Pause prompt before any non-trivial reveal | After the answer (defeats the purpose) |
| `.math-box` | Formula + one-line interpretation | More than 2 lines of math (move to display block) |
| `.bigtext` | Climax of a section, end of deck | Bullet points (it's hero quote only) |
| `.bigstat` | "The numbers" — 4 panels in a row | Single stat (use inline) |
| `.schema-card` | Dimension cards, dataset reveals | Extended prose |
| `.label-sm` | Section labels (above big stats / above formulas) | Slide titles (use `<h2>`) |

## SVG rules

- Build SVGs in `viewBox="0 0 1100 380"` (or 380 wider/taller as needed) for consistency.
- Always `<defs>` an arrowhead marker once per slide if any arrows are drawn.
- Wrap each animated step in `<g class="fragment fade-in" data-fragment-index="N">`.
- Use Playfair Display for big numbers/labels INSIDE SVG (`font-family="Playfair Display"`), DM Sans for everything else.
- Use CSS variables: `fill="var(--cardinal)"`, `stroke="var(--c-d1)"`, etc.
- Diagrams should be **first-principle** for the domain — order book, payoff diagram, queue, decomposition bar, factor map. Avoid generic stock-image clip-art.

## Color rules

- Pick ONE protagonist accent color per deck (e.g., `--c-d1: #1f6feb` for lit equity). Use it for h1 span color, progress bar, region badges.
- Cardinal red (`--cardinal`) is the accent for h2 underline, math-box left border, callout-think top border, big-stat numbers — kept consistent across decks.
- Group colors persist across slides — if MM is `--c-mm: #4caf6e` on slide 5, it stays green on slide 25.

## Validation gates

Before declaring the deck complete:

1. **Bullet-only count**: 0. Every content slide has SVG / table / schema / hero quote.
2. **Stanford asset count**: every slide has at least one of `.label-sm`, `<h2>` cardinal underline, `.callout` family, `.math-box`, `.bigstat`, `.schema-card`, `.bigtext`, or inline SVG.
3. **Story-arc presence**: title → hook → news hook → question → setup → mechanism → numbers → connections → punchline → end. If any section is missing, reject the deck.
4. **Think-First reveals**: at least 2 `.callout-think` boxes paired with reveal slides.
5. **Numbers slide**: at least one `.bigstat` panel with 4 numbers.
6. **Diagram density**: ≥80% of content slides have an inline `<svg>`.
7. **Reveal.js init**: `Reveal.initialize()` called with `slideNumber: 'c/t'`, `progress: true`, `transition: 'slide'`.

## Generation procedure

1. Copy `templates/stanford_html_template.html` to the output path.
2. Replace the title block with the deck's title, author, date.
3. Replace the deck's protagonist accent variable (`--c-d1`) with the appropriate color (Cardinal for academic, deck-specific for tour decks).
4. For each section in the structural contract above, write the slide(s) using the component palette. Each section may take 1–4 slides (e.g., "mechanism walkthrough" is typically 5–10 slides).
5. Build SVGs by hand. For each diagram, sketch on paper first, then translate to SVG with consistent margins.
6. Add `.callout-think` before each reveal pair.
7. Ship one numbers slide (4 `.bigstat` panels).
8. Ship a connections slide showing where the deck fits in the larger map / curriculum.
9. Ship a `.bigtext` punchline + an end card.
10. Run validation gates. If any fails, iterate.

## Reference

The canonical worked example is `templates/stanford_html_template.html` (originally trade-map District 1, ~17 slides for 5 cities at this exact standard). Lift its component patterns wholesale — palette, typography, callouts, SVG style, story arc.

The deepest reference is the original Stanford FDCI / Governance Summit "Price of Participation" deck. Read it when in doubt about a layout decision.
