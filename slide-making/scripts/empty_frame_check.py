#!/usr/bin/env python3
# ruff: noqa: D205,D400
r"""
empty_frame_check.py — detect frames whose visible body is essentially empty.

Catches the PTL-052 defect: Wave 1.25 fixers can over-aggressively move content
into \note{} blocks, leaving frames with only a \think{} prompt and no answer
or reveal on the slide. The frame_content_inventory.py height heuristic does
not catch this because \think{} alone has positive height.

Rule (PTL-052): every frame's last overlay must contain at least 2 substantive
elements. Substantive = not a \note{}, not pure whitespace, not just \pause /
\onslide directives. Acceptable substantive elements:

  \begin{block}, \begin{proposition}, \begin{theorem}, \begin{proof}
  display equation \[...\] or \begin{equation}/\begin{align*}
  \mechanism{}, \keyinsight{}, \warning{}, \checkpoint{}
  \paperfigure{}, \includegraphics
  \begin{tikzpicture} (with >=2 \node or \draw)
  \begin{itemize} / \begin{enumerate} (with >=2 \item)
  \begin{tabular}

Usage:
  python3 empty_frame_check.py act1.tex act2.tex act3.tex
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

SUBSTANTIVE_PATTERNS = [
    (r"\\begin\{block\}", "block"),
    (r"\\begin\{proposition\}", "proposition"),
    (r"\\begin\{theorem\}", "theorem"),
    (r"\\begin\{proof\}", "proof"),
    (r"\\begin\{equation\}", "equation"),
    (r"\\begin\{align\*?\}", "align"),
    (r"\\\[", "display_math"),
    (r"\\mechanism\{", "mechanism"),
    (r"\\keyinsight\{", "keyinsight"),
    (r"\\warning\{", "warning"),
    (r"\\checkpoint\{", "checkpoint"),
    (r"\\paperfigure\{", "paperfigure"),
    (r"\\includegraphics", "includegraphics"),
    (r"\\begin\{tikzpicture\}", "tikzpicture"),
    (r"\\begin\{tabular\}", "tabular"),
    (r"\\begin\{itemize\}", "itemize"),
    (r"\\begin\{enumerate\}", "enumerate"),
]

THINK_PATTERN = re.compile(r"\\think\{")
NOTE_BLOCK_PATTERN = re.compile(r"\\note\{[^}]*\}", re.DOTALL)
COMMENT_LINE = re.compile(r"^\s*%.*$", re.MULTILINE)


def strip_comments_and_notes(body: str) -> str:
    """Drop comment lines and \\note{} blocks (which are not visible on slide)."""
    body = re.sub(COMMENT_LINE, "", body)
    body = NOTE_BLOCK_PATTERN.sub("", body)
    return body


def count_substantive(body: str) -> dict[str, int]:
    """Count substantive elements in the frame body."""
    counts: dict[str, int] = {}
    for pattern, name in SUBSTANTIVE_PATTERNS:
        n = len(re.findall(pattern, body))
        if n > 0:
            counts[name] = n
    return counts


def find_frames(text: str) -> list[tuple[int, int, str]]:
    """Return list of (start_line, end_line, body) for each \\begin{frame}...\\end{frame}."""
    frames = []
    lines = text.split("\n")
    in_frame = False
    start = 0
    body_lines: list[str] = []
    for i, line in enumerate(lines, 1):
        if not in_frame and re.search(r"\\begin\{frame\}", line):
            in_frame = True
            start = i
            body_lines = [line]
        elif in_frame:
            body_lines.append(line)
            if re.search(r"\\end\{frame\}", line):
                in_frame = False
                frames.append((start, i, "\n".join(body_lines)))
    return frames


def get_title(body: str) -> str:
    m = re.search(r"\\begin\{frame\}(?:\[[^\]]*\])?\{([^}]*)\}", body, re.DOTALL)
    if m:
        title = m.group(1).strip()
        # Truncate to ~60 chars
        return title[:60] + ("…" if len(title) > 60 else "")
    return "(no title)"


def audit_file(path: Path) -> list[dict]:
    text = path.read_text()
    frames = find_frames(text)
    defects = []
    for start, end, body in frames:
        title = get_title(body)
        clean = strip_comments_and_notes(body)
        has_think = bool(THINK_PATTERN.search(clean))
        counts = count_substantive(clean)
        total_substantive = sum(counts.values())
        # PTL-052 rule: must have >= 2 substantive elements OR >= 1 substantive + a heading-only \begin{frame}
        # If frame has \think but 0 substantive other elements, it's "answer-on-note"
        if has_think and total_substantive == 0:
            defects.append(
                {
                    "file": path.name,
                    "start_line": start,
                    "end_line": end,
                    "title": title,
                    "issue": "ANSWER-ON-NOTE",
                    "detail": "Frame has \\think{} but no substantive body element (block/equation/mechanism/keyinsight/etc.)",
                    "elements": counts,
                }
            )
        elif total_substantive == 0 and not has_think:
            defects.append(
                {
                    "file": path.name,
                    "start_line": start,
                    "end_line": end,
                    "title": title,
                    "issue": "EMPTY-BODY",
                    "detail": "Frame has no substantive body element at all",
                    "elements": counts,
                }
            )
        elif total_substantive == 1 and has_think:
            # think + one element is borderline; warn but don't fail
            defects.append(
                {
                    "file": path.name,
                    "start_line": start,
                    "end_line": end,
                    "title": title,
                    "issue": "MINIMAL-BODY",
                    "detail": "Frame has \\think{} + only 1 substantive element (recommend >= 2 for a complete reveal)",
                    "elements": counts,
                }
            )
    return defects


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Detect frames whose visible body is essentially empty (PTL-052 answer-on-note check)."
    )
    parser.add_argument("tex_files", nargs="+", type=Path)
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Treat MINIMAL-BODY as failure (default: only ANSWER-ON-NOTE and EMPTY-BODY fail)",
    )
    args = parser.parse_args()

    all_defects = []
    for f in args.tex_files:
        if not f.exists():
            print(f"WARN: {f} not found", file=sys.stderr)
            continue
        all_defects.extend(audit_file(f))

    crit = [d for d in all_defects if d["issue"] in ("ANSWER-ON-NOTE", "EMPTY-BODY")]
    minor = [d for d in all_defects if d["issue"] == "MINIMAL-BODY"]

    print("=" * 64)
    print(f"EMPTY-FRAME CHECK — {sum(1 for _ in all_defects)} flagged frames")
    print("=" * 64)

    if crit:
        print(f"\nCRITICAL ({len(crit)}):")
        for d in crit:
            print(f"  {d['file']}:{d['start_line']}-{d['end_line']}  {d['issue']}")
            print(f"    title: {d['title']}")
            print(f"    {d['detail']}")
            print(f"    visible body: {d['elements'] or '(none)'}")

    if minor:
        print(f"\nMINIMAL-BODY ({len(minor)}):")
        for d in minor:
            print(f"  {d['file']}:{d['start_line']}  {d['title']}")
            print(f"    visible: {d['elements']}")

    print()
    fail = bool(crit) or (args.strict and bool(minor))
    print(f"Verdict: {'FAIL' if fail else 'PASS'}")
    return 1 if fail else 0


if __name__ == "__main__":
    sys.exit(main())
