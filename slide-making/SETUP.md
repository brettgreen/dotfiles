# Paper-to-Lecture Package

Turn academic papers into polished lecture slides using Claude Code. Two output formats: LaTeX beamer (PDF) or Reveal.js HTML (browser).

## Quick Start (3 steps)

### 1. Unzip this package

```bash
unzip paper-to-lecture-package.zip -d paper-to-lecture
```

### 2. Install as a Claude Code skill

```bash
mkdir -p ~/.claude/skills
cp -a paper-to-lecture ~/.claude/skills/paper-to-lecture
```

### 3. Start making slides

Open Claude Code in any directory with your PDF papers and say:

> Turn these papers into lecture slides

Or use the slash command (available after installation):

> /paper-to-lecture

Claude will ask you 8 questions (papers, arc style, proof depth, theme, visuals, audience, pedagogy, output format), then run the full pipeline.

## What's in the Package

```
paper-to-lecture/
  SKILL.md              # Main skill definition (Claude reads this)
  SETUP.md              # This file
  prompts/              # Sub-agent prompts
    paper_to_notes.md   #   Paper reading + note extraction
    proof_extraction.md #   Proof depth protocol
    combined_notes.md   #   Act-level note merging
    notes_qa.md         #   7-dimension QA review
    beamer_generation.md#   LaTeX beamer slide writer
    html_generation.md  #   Reveal.js HTML slide writer
  agents/               # Specialized agent definitions
    story-arc.md        #   Cinematic/chronological/thematic arc design
    teaching-review.md  #   Pedagogical validation
    visualization-audit.md # Visual coverage + embedded figure audit
  references/           # Quality standards
    slide_principles.md #   29 pedagogical principles (P1-P29)
    beamer_conventions.md#  LaTeX beamer style guide
    lessons.md          #   46 PTL lessons from production runs
  templates/            # Starting templates
    config.yml          #   Configuration template
    beamer_preamble.tex #   LaTeX preamble with theme placeholders
    folder_structure.md #   Workspace layout
  scripts/              # Build + audit scripts (beamer only)
    compile_check.sh    #   Structural gates G1-G11
    frame_content_inventory.py  # Overflow detection
    paperfigure_budget_check.py # Vertical budget validator
    render_last_overlays.sh     # PNG rendering
    visual_audit_loop.sh        # Convergence loop wrapper
  deps/tikz-audit/      # TikZ diagram quality convergence (beamer only)
```

## Dependencies

| Output | Required | Install |
|--------|----------|---------|
| HTML (Reveal.js) | None | Just a browser |
| Beamer (LaTeX) | pdftotext | `apt install poppler-utils` or `brew install poppler` |
| Beamer (LaTeX) | pdflatex | `apt install texlive-latex-base texlive-latex-recommended texlive-latex-extra texlive-fonts-recommended` or `brew install --cask mactex` |

**HTML output requires zero dependencies.** Just Claude Code and a browser.

## Output Formats

### HTML (Reveal.js) -- recommended for sharing
- Single self-contained `.html` file
- Opens in any browser
- CSS-based visualizations (flow diagrams, bar charts, metric cards)
- KaTeX math rendering
- Speaker notes (press `S` in presentation)
- Best for: virtual talks, workshops, sharing online

### Beamer (LaTeX) -- recommended for in-person lectures
- Compiled PDF with TikZ diagrams
- Publication-quality typesetting
- Multi-wave quality audit (content overflow, visualization coverage, TikZ convergence)
- Best for: university lectures, projector presentations, PDF handouts

## The Pipeline (6 steps)

1. **Setup** -- workspace creation, PDF-to-text conversion
2. **Paper Processing** -- parallel note extraction (1 agent per paper)
3. **Story Arc** -- cinematic/chronological/thematic structure design
4. **Combined Notes** -- unified lecture notes per act
5. **QA Review** -- 7-dimension quality scoring + gap fixing
6. **Slides** -- generation + multi-wave quality audit (beamer) or single-pass generation (HTML)

Steps 1-5 are shared across both output formats. Step 6 diverges.

## Tips

- **Start with HTML** if you don't have LaTeX installed. The quality is the same; only the rendering differs.
- **Use cinematic arc** for research seminars (default). It structures the talk as a puzzle the audience solves.
- **Set `arc_review: false`** in config.yml to skip the human approval gate (faster, but you lose the chance to reshape the narrative).
- **For 1-paper talks**: the pipeline still works -- just provide one paper.
- **For talks without papers** (e.g., workshop presentations): set `source_type: talk_outline` in config.yml and provide material in `material/` instead of PDF papers.

## Self-Test

After installation, verify everything works:

```
/paper-to-lecture --selftest
```

This checks all files, dependencies, and template compilation without needing any papers.
