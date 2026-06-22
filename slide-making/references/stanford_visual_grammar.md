# Stanford Visual Grammar — HTML Slide Standard

**Mandatory reading before building any HTML/Reveal.js deck.**

Source: Stanford FDCI / Governance Summit "Price of Participation" deck (2026-05). The standard codified here is what raised the trade-map decks from "laundry-list bullets" to publishable presentation quality.

This file is the canonical visual + structural grammar. The skeleton template lives at `templates/stanford_html_template.html`. The generation instructions live at `prompts/stanford_html_generation.md`.

---

## 1. Palette

```css
--white:    #ffffff;
--off:      #f8f7f5;   /* page background tint, schema cards */
--light:    #f0eeeb;
--border:   #e2dfd9;
--muted:    #9b9690;
--text:     #1a1916;

--cardinal:        #8C1515;   /* Stanford red — primary accent */
--cardinal-soft:   #f7eeee;   /* highlighted card background */
--cardinal-line:   #d8b9b9;   /* separator strokes */
--cardinal-muted:  #a43a32;

--accent:    #007C92;          /* teal — secondary, "direct/positive" */

/* group colors — pick a small palette per deck */
--c-mm:      #4caf6e;          /* green — market makers, success */
--c-retail:  #9b6fd4;          /* purple — retail, customer side */
--c-algo:    #e07ab0;          /* pink — algorithms */
--c-bond:    #007C92;          /* teal — alt domain */
--c-liq:     #e62600;          /* orange-red — liquidation, stress */
```

**Rules.**
- White background. Always. Cardinal as accent only — never as a fill that dominates the slide.
- Each deck picks ONE protagonist color (e.g. `--c-d1: #1f6feb` for a lit-equity district deck) and uses it consistently for that domain's title accents and progress bar.
- Group colors are persistent across the deck. If MM is green on slide 5, it's green on slide 25.

---

## 2. Typography

```css
--serif: 'Playfair Display', Georgia, serif;   /* h1, h2, h3, big stats, hero quotes */
--sans:  'DM Sans', -apple-system, system-ui, sans-serif;   /* body, labels, tables, callouts */

font-weight 300 (light) for body
font-weight 500 for emphasis
font-weight 600 for serif headings
```

Load from Google Fonts:
```html
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,600;1,400&family=DM+Sans:opsz,wght@9..40,300;9..40,400;9..40,500&display=swap" rel="stylesheet">
```

---

## 3. The slide skeleton

Every content slide is the same structure:

```html
<section data-id="<slug>">
  <h2>Title — the punchline as a sentence</h2>
  <h3>Optional italic subtitle that frames the question</h3>

  <div class="fig-area"> ...inline SVG diagram... </div>

  <div class="callout"> or <div class="math-box"> or <div class="callout-think">
    ...synthesis sentence or formula or pause prompt
  </div>
</section>
```

Do **not** ship a slide that is bullet text only. Every content slide must carry one of: SVG diagram, schema-card grid, table with `anim-cols`, math-box, big-stat panel, or hero quote.

---

## 4. Component library

### `.label-sm` — section/region label with red dot
Small uppercase letter-spaced label, prefixed by a 6×6 cardinal dot.

### `<h2>` — title with cardinal underline
A 42×2 cardinal rule sits beneath every h2 via `::after`.

### `<h3>` — italic muted subtitle with cardinal-line left border
Frames the question the slide answers.

### `.callout` — teal info box
Use for synthesis sentences, "the lesson is …", calm conclusions.

### `.callout-warn` — orange warning box
Use for risk callouts, regulatory boundaries, stress scenarios.

### `.callout-think` — purple dashed box, "Think first — pause 30 seconds"
**Critical pedagogical primitive.** Drop in before any reveal so the audience commits before seeing the answer. Always include `<div class="think-label">` prefix.

### `.math-box` — formula on off-white with cardinal left border
Each math-box has a `.mlabel` uppercase tag (e.g. "OPTIMAL SIZE", "ARITHMETIC") and one or two formulas + a one-line interpretation.

### `.bigtext` — hero quote slide
Centered Playfair, ~1.7em, italic cardinal accents on emphasized words. Use sparingly — once at climax of a section, once at end-of-deck punchline.

### `.bigstat` — large number with uppercase letter-spaced label below
For "the numbers" panels: 4 stats in a row, each Playfair 2.6em number + DM Sans tiny label.

### `.schema-card` — off-white panel with cardinal-line top border
For dataset reveals, dimension cards, frame inventories.

### Stat panel — `<div class="bigstat">`
```html
<div class="bigstat">
  <div class="num">$92M</div>
  <div class="label">trade size</div>
</div>
```

### Table with column animation — `.anim-cols`
For "traditional dataset → linked record" reveals. Columns start at opacity 0, then `.col-visible` fades them in.

### Chip — `.chip-mm`, `.chip-retail`, `.chip-algo`
Small rounded labels to mark group identity inline.

---

## 5. Story-arc structure (mandatory)

Every deck — paper-derived or topic-derived — must follow:

1. **Title slide** — author block + cardinal rule + date-line. One signal, not a mechanism diagram. (P30 lesson: don't crowd the title.)
2. **Hook** — 1 question on screen + 4-6 SVG nodes appearing one at a time via `fragment fade-in` (e.g., "What happens in the next 250 ms?"). Closes with a question or a tension.
3. **News hook OR big number** — one $XXX number + comparison bar chart. Establishes "this matters."
4. **Academic/structural question** — 4-card schema grid, one card highlighted in cardinal red. Names the question the rest of the deck will answer.
5. **Setup / data / map zoom** — schema-card grids, dataset tables, or map fragments. Show what we have to work with.
6. **Mechanism walkthrough** — one new object per slide, built from something familiar (P1 / P3 lessons), each step with an SVG.
7. **Think-First → Reveal pairs** — every meaningful claim is a Think-First box (audience predicts) followed by a reveal slide with the answer + diagram.
8. **The numbers** — 4 big-stat panels showing the punchline quantitatively.
9. **Trade-routes / connections** — show how this content connects to other decks/cities/concepts. Avoid leaving the deck self-contained.
10. **Punchline slide** — `.bigtext` hero quote summarizing the deck in 2 lines max.
11. **End card** — "where to next" + 2-3 suggested follow-on decks.

---

## 6. SVG-per-slide guidance

- One SVG per content slide. Build SVGs in `viewBox="0 0 1100 380"` (or similar 16:9 fragment) for consistent scale.
- Reuse the marker definition for arrowheads:
  ```html
  <defs>
    <marker id="arr" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto">
      <path d="M0,0 L10,5 L0,10 z" fill="var(--muted)"/>
    </marker>
  </defs>
  ```
- Wrap each step of a build-up in `<g class="fragment fade-in" data-fragment-index="N">` so reveal.js animates it.
- Use Playfair for big numbers/labels inside SVG, DM Sans for everything else. Set `font-family="Playfair Display"` or `font-family="DM Sans"` directly on `<text>` elements.
- Use `fill="var(--cardinal)"` etc. — the CSS variables resolve inside SVG inline styles in modern browsers.
- Diagrams should be **first-principle** — order book, price path, queue, decomposition bar. Avoid generic stock-image clip-art.

---

## 7. Reveal.js initialization

```html
<script src="node_modules/reveal.js/dist/reveal.js"></script>
<script>
Reveal.initialize({
  hash: true,
  slideNumber: 'c/t',
  controls: true,
  progress: true,
  transition: 'slide',
  width: 1280,
  height: 800,
  margin: 0.04
});
</script>
```

The progress-bar color must be the deck's protagonist color, set via `.reveal .progress { color: var(--c-d1); }` or whatever the protagonist accent is.

---

## 8. Do / Don't

**Do**
- Lead with the punchline as the slide title ("Inventory drift dominates spread economics", not "About inventory").
- Show a number and let the audience react before the bullet that explains it.
- Use Think-First before any non-trivial reveal.
- Keep one protagonist color per deck; map group colors consistently.
- Build SVGs by hand. They are the deck's vocabulary, not decoration.

**Don't**
- Don't use bullet-only slides. Every slide carries an SVG, table, schema, or hero quote.
- Don't reuse the title slide's mechanism diagram on later slides.
- Don't mix Stanford-cardinal accents with other strong reds in the same deck — readers think they're related.
- Don't use `font-weight: 700` on body text. 300 + selective 500 is the rhythm.
- Don't omit `.callout-warn` for regulatory boundaries (FINRA 5270/5310/5320, CFTC) — these need visual contrast.
- Don't ship a deck without a numbers slide. "Why does this matter?" → big-stat panel.

---

## 9. Reference deck

Use a completed local HTML deck as the worked reference implementation: a concise
deck with story arc, SVG per slide, Think-First reveals, and a clear punchline.

For the Stanford-style HTML path, use the bundled visual grammar in this file and
the template at `${CLAUDE_SKILL_DIR}/templates/stanford_html_template.html` as the
canonical reference.
