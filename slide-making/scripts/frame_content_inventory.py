#!/usr/bin/env python3
"""frame_content_inventory.py — Estimate vertical content height per beamer frame.

Parses .tex files, identifies elements per frame, computes estimated height,
and flags frames that exceed the beamer body budget (~6.0 cm for 16:9).

Usage:
    python3 frame_content_inventory.py act1.tex act2.tex act3.tex [--nav nav_file] [--out /tmp/ptl_diagnosis]
"""

import re
import json
import sys
import os
from pathlib import Path

# Height estimates (cm) for common beamer elements
HEIGHTS = {
    "paperfigure": 5.0,  # figure + caption + keyinsight (conservative)
    "includegraphics": 4.5,  # standalone figure
    "think": 1.5,  # base height for \think{}
    "keyinsight": 1.2,  # base height for \keyinsight{}
    "mechanism": 1.2,
    "warning": 1.2,
    "checkpoint": 1.2,
    "block": 0.8,  # \begin{block}
    "itemize_item": 0.4,  # per \item
    "enumerate_item": 0.4,
    "equation_display": 0.8,  # \[ \] or equation environment
    "equation_align": 1.0,  # align/align* environment
    "text_line": 0.3,  # per ~80 chars of body text
    "vspace_small": 0.2,  # \vspace{3pt} etc
    "tikzpicture": 4.0,  # base estimate for tikzpicture
    "theorem": 1.5,  # proposition/theorem environment
}

BEAMER_BODY_BUDGET = 6.0  # cm, 16:9 after title bar + footer


def estimate_text_height(text: str) -> float:
    """Estimate height of a text block based on character count."""
    chars = len(text.strip())
    lines = max(1, chars / 80)
    return lines * HEIGHTS["text_line"]


def parse_nav_file(nav_path: str) -> dict:
    """Parse .nav file to get frame -> (first_page, last_page) mapping."""
    mapping = {}
    frame_num = 0
    with open(nav_path) as f:
        for line in f:
            m = re.search(r"beamer@framepages\s*\{(\d+)\}\{(\d+)\}", line)
            if m:
                frame_num += 1
                mapping[frame_num] = (int(m.group(1)), int(m.group(2)))
    return mapping


def extract_macro_arg(text: str, start: int) -> str:
    """Extract the content of a braced argument starting at position start."""
    if start >= len(text) or text[start] != "{":
        return ""
    depth = 0
    end = start
    for i in range(start, len(text)):
        if text[i] == "{":
            depth += 1
        elif text[i] == "}":
            depth -= 1
            if depth == 0:
                return text[start + 1 : i]
    return text[start + 1 :]


def analyze_frame(frame_text: str, frame_num: int, source_file: str) -> dict:
    """Analyze a single frame's content and estimate vertical height."""
    elements = []
    total_height = 0.0

    # paperfigure (includes figure + caption + keyinsight)
    for m in re.finditer(r"\\paperfigure\{", frame_text):
        # Find the 4th argument (keyinsight text)
        pos = m.start()
        # Skip through 3 args to get to the 4th
        arg_starts = []
        p = m.end() - 1
        for _ in range(4):
            while p < len(frame_text) and frame_text[p] != "{":
                p += 1
            arg_content = extract_macro_arg(frame_text, p)
            arg_starts.append(arg_content)
            # Move past this arg
            depth = 0
            for i in range(p, len(frame_text)):
                if frame_text[i] == "{":
                    depth += 1
                elif frame_text[i] == "}":
                    depth -= 1
                    if depth == 0:
                        p = i + 1
                        break

        caption_text = arg_starts[2] if len(arg_starts) > 2 else ""
        keyinsight_text = arg_starts[3] if len(arg_starts) > 3 else ""
        ki_height = estimate_text_height(keyinsight_text) if keyinsight_text else 0
        h = HEIGHTS["paperfigure"] + ki_height
        elements.append(
            {
                "type": "paperfigure",
                "height": h,
                "keyinsight_chars": len(keyinsight_text),
            }
        )
        total_height += h

    # Standalone includegraphics (not inside paperfigure)
    for m in re.finditer(r"\\includegraphics\[", frame_text):
        # Check it's not inside a paperfigure
        preceding = frame_text[: m.start()]
        if "\\paperfigure" not in preceding[-200:]:
            elements.append(
                {"type": "includegraphics", "height": HEIGHTS["includegraphics"]}
            )
            total_height += HEIGHTS["includegraphics"]

    # Pedagogical boxes
    for macro in ["think", "keyinsight", "mechanism", "warning", "checkpoint"]:
        # Skip keyinsights that are part of paperfigure (already counted)
        pattern = rf"\\{macro}\{{"
        for m in re.finditer(pattern, frame_text):
            # Check not inside paperfigure
            preceding = frame_text[: m.start()]
            if macro == "keyinsight" and "\\paperfigure" in preceding[-300:]:
                continue
            arg = extract_macro_arg(frame_text, m.end() - 1)
            h = HEIGHTS[macro] + estimate_text_height(arg)
            elements.append({"type": macro, "height": h, "chars": len(arg)})
            total_height += h

    # tikzpicture environments
    tikz_count = len(re.findall(r"\\begin\{tikzpicture\}", frame_text))
    for _ in range(tikz_count):
        elements.append({"type": "tikzpicture", "height": HEIGHTS["tikzpicture"]})
        total_height += HEIGHTS["tikzpicture"]

    # itemize/enumerate items
    items = len(re.findall(r"\\item\b", frame_text))
    if items > 0:
        h = items * HEIGHTS["itemize_item"]
        elements.append({"type": "items", "count": items, "height": h})
        total_height += h

    # Display equations
    display_eqs = len(re.findall(r"\\\[", frame_text)) + len(
        re.findall(r"\\begin\{equation", frame_text)
    )
    for _ in range(display_eqs):
        elements.append(
            {"type": "equation_display", "height": HEIGHTS["equation_display"]}
        )
        total_height += HEIGHTS["equation_display"]

    # align environments
    align_envs = len(re.findall(r"\\begin\{align", frame_text))
    for _ in range(align_envs):
        elements.append({"type": "equation_align", "height": HEIGHTS["equation_align"]})
        total_height += HEIGHTS["equation_align"]

    # block environments (not already captured by pedagogical boxes)
    blocks = len(re.findall(r"\\begin\{block\}", frame_text))
    for _ in range(blocks):
        elements.append({"type": "block", "height": HEIGHTS["block"]})
        total_height += HEIGHTS["block"]

    # theorem/proposition environments
    for env in ["theorem", "proposition", "lemma", "corollary"]:
        count = len(re.findall(rf"\\begin\{{{env}\}}", frame_text))
        for _ in range(count):
            elements.append({"type": env, "height": HEIGHTS["theorem"]})
            total_height += HEIGHTS["theorem"]

    # Classify risk
    if total_height > 5.8:
        risk = "HIGH"
    elif total_height > 5.0:
        risk = "MEDIUM"
    else:
        risk = "LOW"

    # Extract frame title
    title_m = re.search(r"\\begin\{frame\}(?:\[.*?\])?\{(.*?)\}", frame_text)
    if not title_m:
        title_m = re.search(r"\\frametitle\{(.*?)\}", frame_text)
    title = title_m.group(1) if title_m else "(untitled)"

    return {
        "frame": frame_num,
        "title": title,
        "source_file": source_file,
        "elements": elements,
        "estimated_height_cm": round(total_height, 2),
        "budget_cm": BEAMER_BODY_BUDGET,
        "overflow_cm": round(max(0, total_height - BEAMER_BODY_BUDGET), 2),
        "risk": risk,
        "has_paperfigure": any(e["type"] == "paperfigure" for e in elements),
        "has_tikz": any(e["type"] == "tikzpicture" for e in elements),
        "has_think": any(e["type"] == "think" for e in elements),
    }


def parse_frames(tex_path: str, start_frame: int = 1) -> list:
    """Parse a .tex file and return per-frame analysis."""
    with open(tex_path) as f:
        content = f.read()

    frames = []
    # Split on \begin{frame} boundaries
    parts = re.split(r"(\\begin\{frame\})", content)

    frame_num = start_frame
    i = 1  # Skip the first part (before any frame)
    while i < len(parts):
        if parts[i] == "\\begin{frame}":
            # Collect until \end{frame}
            frame_text = parts[i]
            j = i + 1
            while j < len(parts):
                frame_text += parts[j]
                if "\\end{frame}" in parts[j]:
                    break
                j += 1
            frames.append(
                analyze_frame(frame_text, frame_num, os.path.basename(tex_path))
            )
            frame_num += 1
            i = j + 1
        else:
            # Check for frames with options: \begin{frame}[plain] or \begin{frame}{Title}
            # These would have been split already, but handle \begin{frame}[ or \begin{frame}{ variants
            frame_matches = list(re.finditer(r"\\begin\{frame\}", parts[i]))
            if frame_matches:
                for fm in frame_matches:
                    end_match = re.search(r"\\end\{frame\}", parts[i][fm.start() :])
                    if end_match:
                        frame_text = parts[i][fm.start() : fm.start() + end_match.end()]
                        frames.append(
                            analyze_frame(
                                frame_text, frame_num, os.path.basename(tex_path)
                            )
                        )
                        frame_num += 1
            i += 1

    return frames, frame_num


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Frame content inventory for beamer slides"
    )
    parser.add_argument("tex_files", nargs="+", help=".tex files to analyze")
    parser.add_argument("--nav", help=".nav file for page mapping")
    parser.add_argument("--out", default="/tmp/ptl_diagnosis", help="Output directory")
    args = parser.parse_args()

    os.makedirs(args.out, exist_ok=True)

    # Parse nav file if provided
    page_map = {}
    if args.nav and os.path.exists(args.nav):
        page_map = parse_nav_file(args.nav)

    # Parse all tex files
    all_frames = []
    next_frame = 1
    for tex_file in args.tex_files:
        frames, next_frame = parse_frames(tex_file, next_frame)
        all_frames.extend(frames)

    # Add page mapping
    for f in all_frames:
        if f["frame"] in page_map:
            first, last = page_map[f["frame"]]
            f["pdf_pages"] = [first, last]
            f["last_overlay_page"] = last
        else:
            f["pdf_pages"] = None
            f["last_overlay_page"] = None

    # Write JSON
    json_path = os.path.join(args.out, "content_inventory.json")
    with open(json_path, "w") as f:
        json.dump(all_frames, f, indent=2)

    # Print summary
    high = [f for f in all_frames if f["risk"] == "HIGH"]
    medium = [f for f in all_frames if f["risk"] == "MEDIUM"]
    low = [f for f in all_frames if f["risk"] == "LOW"]

    print(f"\n{'='*60}")
    print(f"FRAME CONTENT INVENTORY — {len(all_frames)} frames analyzed")
    print(f"{'='*60}")
    print(f"  HIGH risk (>5.8cm):   {len(high)} frames")
    print(f"  MEDIUM risk (>5.0cm): {len(medium)} frames")
    print(f"  LOW risk (<5.0cm):    {len(low)} frames")
    print(f"{'='*60}")

    if high:
        print(f"\nHIGH RISK FRAMES:")
        for f in high:
            print(
                f"  Frame {f['frame']:2d} | {f['estimated_height_cm']:5.1f}cm (overflow: {f['overflow_cm']:.1f}cm) | {f['source_file']} | {f['title'][:50]}"
            )
            for e in f["elements"]:
                print(f"           {e['type']:20s}  {e['height']:.1f}cm")

    if medium:
        print(f"\nMEDIUM RISK FRAMES:")
        for f in medium:
            print(
                f"  Frame {f['frame']:2d} | {f['estimated_height_cm']:5.1f}cm | {f['source_file']} | {f['title'][:50]}"
            )

    print(f"\nJSON written to: {json_path}")
    return len(high)


if __name__ == "__main__":
    sys.exit(main())
