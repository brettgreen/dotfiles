# Workspace Folder Structure

When `/paper-to-lecture` creates a workspace, it follows this layout:

```
{workspace}/
├── config.yml              # User preferences + progress tracking
├── material/               # Source PDFs (input)
│   ├── paper1.pdf
│   └── paper2.pdf
├── notes_raw/              # Per-paper notes + story arc plan
│   ├── paper1_notes.md     # Detailed notes from paper-reader agent
│   ├── paper2_notes.md
│   ├── plan.md             # Story arc design
│   └── qa_log.md           # QA review results
├── lecture_notes/           # Combined lecture notes
│   ├── act1_notes.md       # Per-act notes (if multi-act)
│   ├── act2_notes.md
│   └── {topic}_lecture_notes.md  # Final combined notes
├── final_slides/            # Beamer output
│   ├── preamble.tex        # Generated from theme config
│   ├── act1.tex            # Per-act slide content
│   ├── act2.tex
│   ├── {topic}_slides.tex  # Final merged deck
│   └── {topic}_slides.pdf  # Compiled output
├── .best_known/             # Snapshots of gate-passing artifacts
│   ├── notes/
│   └── slides/
└── .proof_tokens/           # Machine-checkable verification tokens
    └── verify_*.txt
```

## Naming Conventions

- Paper notes: `notes_raw/{first_author}_{year}_notes.md`
- Combined notes: `lecture_notes/{topic}_lecture_notes.md`
- Slides: `final_slides/{topic}_slides.tex`
- Act files: `act{N}.tex` or `act{N}_notes.md` (N = 1, 2, 3, ...)
