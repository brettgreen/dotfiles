#!/usr/bin/env python3
"""paperfigure_budget_check.py — Check paperfigure frames for content overflow.

Finds all \\paperfigure calls, measures keyinsight text length,
and flags frames that combine paperfigure with other heavy elements.

Usage:
    python3 paperfigure_budget_check.py act1.tex act2.tex act3.tex
"""

import re
import sys
import os

MAX_KEYINSIGHT_CHARS = 160  # ~2 lines at 80 chars/line


def extract_braced_arg(text: str, pos: int) -> tuple:
    """Extract content of braced argument starting at pos. Returns (content, end_pos)."""
    if pos >= len(text) or text[pos] != "{":
        return "", pos
    depth = 0
    for i in range(pos, len(text)):
        if text[i] == "{":
            depth += 1
        elif text[i] == "}":
            depth -= 1
            if depth == 0:
                return text[pos + 1 : i], i + 1
    return text[pos + 1 :], len(text)


def find_enclosing_frame(text: str, pos: int) -> tuple:
    """Find the frame number and boundaries enclosing position pos."""
    # Find all frame starts before pos
    frame_starts = [
        (m.start(), m.end())
        for m in re.finditer(r"\\begin\{frame\}", text)
        if m.start() <= pos
    ]
    if not frame_starts:
        return None, "", ""
    # The last frame start before pos is the enclosing frame
    fstart, fstart_end = frame_starts[-1]
    # Find end of this frame
    fend_m = re.search(r"\\end\{frame\}", text[fstart:])
    if fend_m:
        frame_text = text[fstart : fstart + fend_m.end()]
    else:
        frame_text = text[fstart:]
    # Extract title
    title_m = re.search(r"\\begin\{frame\}(?:\[.*?\])?\{(.*?)\}", frame_text)
    title = title_m.group(1) if title_m else "(untitled)"
    return len(frame_starts), title, frame_text


def analyze_file(tex_path: str, frame_offset: int = 0):
    """Analyze a single .tex file for paperfigure budget violations."""
    with open(tex_path) as f:
        content = f.read()

    filename = os.path.basename(tex_path)
    violations = []

    # Count frames for numbering
    frame_positions = [m.start() for m in re.finditer(r"\\begin\{frame\}", content)]

    for m in re.finditer(r"\\paperfigure\{", content):
        pos = m.end() - 1  # position of opening {

        # Extract all 4 arguments
        args = []
        p = pos
        for _ in range(4):
            while p < len(content) and content[p] != "{":
                p += 1
            arg, p = extract_braced_arg(content, p)
            args.append(arg)

        options = args[0] if len(args) > 0 else ""
        pdf_path = args[1] if len(args) > 1 else ""
        caption = args[2] if len(args) > 2 else ""
        keyinsight_text = args[3] if len(args) > 3 else ""

        # Find enclosing frame
        frame_idx = sum(1 for fp in frame_positions if fp <= m.start())
        frame_num = frame_idx + frame_offset

        # Get frame text
        if frame_idx > 0 and frame_idx <= len(frame_positions):
            fstart = frame_positions[frame_idx - 1]
            fend_m = re.search(r"\\end\{frame\}", content[fstart:])
            frame_text = (
                content[fstart : fstart + fend_m.end()] if fend_m else content[fstart:]
            )
        else:
            frame_text = ""

        # Check for violations
        issues = []

        # V1: Keyinsight too long
        ki_chars = len(keyinsight_text.strip())
        if ki_chars > MAX_KEYINSIGHT_CHARS:
            issues.append(
                f"keyinsight too long: {ki_chars} chars (max {MAX_KEYINSIGHT_CHARS})"
            )

        # V2: Frame also has \think{}
        if "\\think{" in frame_text:
            issues.append("frame combines \\paperfigure with \\think{}")

        # V3: Frame also has \mechanism{}
        if "\\mechanism{" in frame_text:
            issues.append("frame combines \\paperfigure with \\mechanism{}")

        # V4: Frame also has itemize
        item_count = len(re.findall(r"\\item\b", frame_text))
        if item_count > 2:
            issues.append(f"frame has {item_count} \\items alongside \\paperfigure")

        # V5: Frame also has display equations
        eq_count = len(re.findall(r"\\\[", frame_text)) + len(
            re.findall(r"\\begin\{equation", frame_text)
        )
        if eq_count > 0:
            issues.append(
                f"frame has {eq_count} display equation(s) alongside \\paperfigure"
            )

        # V6: Frame also has another paperfigure
        pf_count = len(re.findall(r"\\paperfigure\{", frame_text))
        if pf_count > 1:
            issues.append(f"frame has {pf_count} \\paperfigure calls (should be max 1)")

        # V7: Caption too long
        if len(caption.strip()) > 120:
            issues.append(f"caption too long: {len(caption.strip())} chars")

        # V8: Figure width > 0.85
        width_m = re.search(r"width\s*=\s*([\d.]+)\\textwidth", options)
        if width_m and float(width_m.group(1)) > 0.88:
            issues.append(
                f"figure width {width_m.group(1)}\\textwidth may cause horizontal overflow"
            )

        # Extract frame title
        title_m = re.search(r"\\begin\{frame\}(?:\[.*?\])?\{(.*?)\}", frame_text)
        title = title_m.group(1) if title_m else "(untitled)"

        if issues:
            violations.append(
                {
                    "frame": frame_num,
                    "file": filename,
                    "title": title,
                    "keyinsight_chars": ki_chars,
                    "issues": issues,
                }
            )

    return violations, len(frame_positions)


def main():
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} act1.tex act2.tex act3.tex", file=sys.stderr)
        sys.exit(1)

    all_violations = []
    frame_offset = 0
    for tex_file in sys.argv[1:]:
        violations, frame_count = analyze_file(tex_file, frame_offset)
        all_violations.extend(violations)
        frame_offset += frame_count

    print(f"\n{'='*60}")
    print(f"PAPERFIGURE BUDGET CHECK — {frame_offset} frames scanned")
    print(f"{'='*60}")

    if not all_violations:
        print("  No violations found.")
    else:
        print(f"  {len(all_violations)} frames with violations:\n")
        for v in all_violations:
            print(f"  Frame {v['frame']:2d} | {v['file']} | {v['title'][:45]}")
            for issue in v["issues"]:
                print(f"    - {issue}")
            print()

    return len(all_violations)


if __name__ == "__main__":
    sys.exit(min(main(), 255))
