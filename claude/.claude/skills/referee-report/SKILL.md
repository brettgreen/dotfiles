---
name: referee-report
description: Draft a referee report and editor letter for an academic paper. Use when the user asks to write, draft, or help with a referee report, review, or editor letter.
allowed-tools: Read Bash(pdflatex *) Bash(bibtex *) Bash(latexmk *) Bash(open *)
---

# Referee Report Skill

Draft a referee report and editor letter in the user's voice and style. The user will provide the paper (PDF or description). Output LaTeX files for both the report and editor letter.

## Voice and Tone

- **Direct, intellectually honest, and respectful but unhedged.** Do not soften punches with excessive hedging.
- **First person freely:** "I think," "I am skeptical," "It seems to me that," "I would like to be convinced that," "I did not understand."
- **Genuine but brief praise** when warranted: "This is an elegant and well-written paper on an important topic." Do not over-praise.
- **Frank critiques:** State concerns plainly. "My main issue with the paper is that..." "I do not believe that..."
- **Constructive framing:** Even negative reports should include concrete suggestions. Propose specific paths forward: "In an ideal revision, the author would: (i)... (ii)... (iii)..."
- **Rhetorical questions** to push the author's thinking: "Is that correct?" "Are you arguing to the contrary?"
- **Parenthetical asides** to qualify or pre-empt: "(though I do not believe that it is)"
- **Honest about uncertainty:** "I must admit that I did not follow..." "My impression is that..."

## Report Structure

Use this structure with `\section*{}` headers (always unnumbered):

1. **Summary** — A concise, technically precise paragraph (5-15 lines). Describe the economic setting/framework, the key friction or mechanism, and the main formal results. Use the paper's own notation and reference specific propositions. Neutral and descriptive — do not editorialize here.

2. **Overall Assessment** — 1-2 paragraphs giving the referee's frank overall take. Signal the recommendation direction. This is where opinions belong.

3. **Major Comments** — Numbered list of substantive concerns, ordered by importance. Each comment should:
   - Identify the issue clearly
   - Explain *why it matters* for the paper's contribution
   - State what would satisfy the concern (a concrete ask)
   - Flag whether it is a "must fix" or "would strengthen"

4. **Minor Comments** — Separate section for smaller points: notation issues, typos, missing references, expositional suggestions. Use itemize or enumerate.

## Editor Letter Structure (Referee)

Separate file. Structure:
1. Open with the recommendation directly in the first sentence: "My recommendation is that the paper be rejected / receive a revise and resubmit / be accepted."
2. 1-3 paragraphs of substantive justification summarizing the key concern(s). Do not duplicate the full report — keep it high-level.
3. Close with: "My report contains a number of suggestions for the authors that I hope will be useful in revising the paper. Please let me know if I can be of further assistance in the editorial process."
4. Sign off: "Sincerely," followed by signature block.

## AE Recommendation Letter Structure

When the user is acting as Associate Editor (not referee), draft an AE recommendation letter instead. Structure:

1. **Open with the recommendation** directly in the first sentence.
2. **Brief summary of the paper** — 2-4 sentences on the question, approach, and main results. Concise and neutral.
3. **Main issues with the paper** — Organize by issue, not by referee. Write in active voice stating the AE's own view on each concern. Reference referees by number (e.g., "R1," "both referees") where it adds weight, but never by name -- the AE letter should not reveal referee identities. The goal is a coherent assessment in the AE's voice, not a book report on the referee reports.
5. **Closing** — A sentence or two wrapping up. For rejections, be direct but not harsh. For R&Rs, highlight the most critical issues for revision.
6. **Sign off.**

## Best Practice Reminders

Apply these when drafting:
- **Separate major from minor explicitly** — always use distinct sections, never mix them in one list.
- **State the "so what"** — for each major comment, explain how it affects the paper's contribution. "If this assumption is relaxed, I suspect the main result no longer holds because..."
- **End every major comment with a concrete ask** — what specifically should the author do?
- **Flag "must fix" vs. "would strengthen"** — helps the editor set revision expectations.
- **Keep the letter lean** — recommendation + one-paragraph justification. Let the report do the heavy lifting.
- **A useful test for theory papers:** "Consider whether a similar result would obtain in a simpler model."

## LaTeX Formatting

Use the user's existing templates and conventions:

**Report:**
```latex
\documentclass[12pt]{article}
\input{../report_style.tex}

\begin{document}
\begin{spacing}{1.25}
\begin{center}
{\Large Paper Title}

\medskip
{\large \textit{Journal Name} referee report}
\medskip

\today
\end{center}

\section*{Summary}
...

\section*{Overall Assessment}
...

\section*{Major Comments}
\be
\item ...
\item ...
\ee

\section*{Minor Comments}
\bi
\item ...
\ei

\end{spacing}
\end{document}
```

**Editor letter:**
```latex
\documentclass[12pt]{letter}
\usepackage{setspace}
\usepackage{amsmath}
\usepackage{amssymb}
\usepackage[colorlinks, citecolor=blue]{hyperref}
\usepackage{url}
\usepackage[margin=1in]{geometry}
\begin{document}

\setcounter{page}{1}

\vspace{10pt}
\hfill\today

\vspace{.25in}
\noindent Dear Professor [Editor Name],

\vspace{.25in}
\begin{spacing}{1.125}

My recommendation is that the paper be [rejected / revised and resubmitted / accepted].

[1-3 paragraphs of justification]

My report contains a number of suggestions for the authors that I hope will be useful in revising the paper. Please let me know if I can be of further assistance in the editorial process.

\vspace{1cm}
\noindent Sincerely,

\bigskip
\includegraphics[width=0.75in,angle=90]{../../sig2.pdf} \\[6pt]
{\textsc{Brett Green} \\ \textsc{Associate Professor of Finance} \\ \textsc{Olin Business School} \\ \textsc{Washington University in St. Louis}}

\end{spacing}
\end{document}
```

**Macros available from `report_style.tex`:**
- `\bi` / `\ei` — `\begin{itemize}` / `\end{itemize}`
- `\be` / `\ee` — `\begin{enumerate}` / `\end{enumerate}`

## Editor Letter Format Options

The editor letter can be produced in either LaTeX (PDF) or plain text, depending on the user's preference. Ask the user which format they prefer during the workflow.

- **LaTeX (PDF):** Use when the recommendation involves mathematical notation, references to equations, or the user wants a formal signed PDF. Use the LaTeX template above.
- **Plain text:** Use when the letter is straightforward prose with no math. Output a `.txt` file with the same structure (recommendation, justification, closing, signature block) but no LaTeX markup.

## Workflow

1. Read the paper carefully (the user will provide it).
2. Ask the user for: journal name, editor name, any initial reactions or concerns they want emphasized, and whether the editor letter should be in LaTeX (PDF) or plain text.
3. Draft the report LaTeX file.
4. Draft the editor letter in the chosen format (LaTeX or plain text).
5. Compile the report (and editor letter if LaTeX) with `pdflatex` and open for review.
6. Iterate based on feedback.

For **R2+ revision reports**, keep it short — focus only on whether previous concerns were adequately addressed and any new issues that arose.
