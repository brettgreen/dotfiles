#!/usr/bin/env python3
"""Enumerate all TikZ frames in a beamer tex file and map to PDF pages via .nav file.

Usage: python3 enumerate_tikz_frames.py <tex_file>
Output: /tmp/tikz_frame_map.txt (frame#,page_start,page_end per line)
        /tmp/tikz_pages_to_render.txt (one page number per line)
"""
import re, sys, os

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 enumerate_tikz_frames.py <tex_file>")
        sys.exit(1)

    tex_file = sys.argv[1]
    nav_file = tex_file.replace('.tex', '.nav')

    with open(tex_file) as f:
        lines = f.readlines()

    # Find frames containing tikzpicture
    frame_num = 0
    tikz_frames = []
    in_frame = False
    frame_start_line = 0
    frame_title = ''
    has_tikz = False

    for i, line in enumerate(lines, 1):
        if '\\begin{frame}' in line:
            frame_num += 1
            in_frame = True
            frame_start_line = i
            has_tikz = False
            m = re.search(r'\\frametitle\{(.+?)\}', line)
            frame_title = m.group(1) if m else ''
        if '\\frametitle{' in line and in_frame:
            m = re.search(r'\\frametitle\{(.+?)\}', line)
            if m:
                frame_title = m.group(1)
        if '\\begin{tikzpicture}' in line and in_frame:
            has_tikz = True
        if '\\end{frame}' in line and in_frame:
            if has_tikz:
                tikz_frames.append((frame_num, frame_title, frame_start_line))
            in_frame = False

    # Parse nav file for frame-to-page mapping
    if not os.path.exists(nav_file):
        print(f"WARNING: {nav_file} not found. Run pdflatex first.")
        sys.exit(1)

    with open(nav_file) as f:
        nav = f.read()

    frame_pages = re.findall(r'\\beamer@framepages\s*\{(\d+)\}\{(\d+)\}', nav)
    frame_map = {}
    for idx, (start, end) in enumerate(frame_pages, 1):
        frame_map[idx] = (int(start), int(end))

    # Build output
    tikz_frame_nums = [fn for fn, _, _ in tikz_frames]
    all_pages = set()
    tikz_page_map = []

    for fn in tikz_frame_nums:
        if fn in frame_map:
            start, end = frame_map[fn]
            for p in range(start, end + 1):
                all_pages.add(p)
            tikz_page_map.append((fn, start, end))

    # Write mapping file
    with open('/tmp/tikz_frame_map.txt', 'w') as f:
        for fn, start, end in tikz_page_map:
            f.write(f'{fn},{start},{end}\n')

    # Write page list
    pages_sorted = sorted(all_pages)
    with open('/tmp/tikz_pages_to_render.txt', 'w') as f:
        for p in pages_sorted:
            f.write(f'{p}\n')

    print(f"TikZ frames: {len(tikz_page_map)}")
    print(f"Pages to render: {len(pages_sorted)}")
    if pages_sorted:
        print(f"Page range: {min(pages_sorted)}-{max(pages_sorted)}")

if __name__ == '__main__':
    main()
