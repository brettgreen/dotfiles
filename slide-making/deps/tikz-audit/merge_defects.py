#!/usr/bin/env python3
"""Merge all tikz audit batch reports into a single defect list.

Usage: python3 merge_defects.py [--n-batches 20] [--iteration 1]
Output: /tmp/tikz_defects_iteration_N.md
        /tmp/tikz_fix_assignment_NN.md (per-frame fix assignments)
"""
import re, os, json, argparse
from collections import defaultdict

def parse_severity(text):
    """Try multiple severity formats agents might use."""
    for pat in [
        r'\*\*Severity\*\*.*?(HIGH|MEDIUM|LOW)',
        r'\*\*(HIGH|MEDIUM|LOW)\*\*',
        r'\[(HIGH|MEDIUM|LOW)\]',
        r'Severity:\s*(HIGH|MEDIUM|LOW)',
        r'\|\s*(HIGH|MEDIUM|LOW)\s*\|',
        r'—\s*(HIGH|MEDIUM|LOW)',
    ]:
        m = re.search(pat, text, re.IGNORECASE)
        if m:
            return m.group(1).upper()
    return 'UNKNOWN'

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--n-batches', type=int, default=20)
    parser.add_argument('--iteration', type=int, default=1)
    args = parser.parse_args()

    all_defects = []

    for i in range(args.n_batches):
        path = f"/tmp/tikz_audit_batch_{i:02d}.md"
        if not os.path.exists(path):
            print(f"Batch {i:02d}: MISSING")
            continue

        with open(path) as f:
            content = f.read()

        # Split by ## Frame headers
        frame_sections = re.split(r'(?=^## Frame)', content, flags=re.MULTILINE)
        for section in frame_sections:
            if not section.strip() or not section.startswith('## Frame'):
                continue

            frame_match = re.match(r'## Frame (\d+)', section)
            if not frame_match:
                continue
            frame_num = int(frame_match.group(1))

            if 'NO DEFECT' in section.upper():
                continue

            # Extract individual defects
            defect_sections = re.split(r'(?=^### Defect|^\*\*\d)', section, flags=re.MULTILINE)
            for dsec in defect_sections:
                if not (dsec.strip().startswith('### Defect') or
                        re.match(r'^\*\*\d', dsec.strip())):
                    # Also try table rows and other formats
                    if 'HIGH' not in dsec.upper() and 'MEDIUM' not in dsec.upper():
                        continue

                severity = parse_severity(dsec)

                title_match = re.match(r'### Defect \d+[:\s]*(.+)', dsec)
                if title_match:
                    title = title_match.group(1).strip()
                else:
                    # Try other title patterns
                    title_match2 = re.match(r'\*\*(.+?)\*\*', dsec.strip())
                    title = title_match2.group(1).strip() if title_match2 else 'Unknown'

                all_defects.append({
                    'frame': frame_num,
                    'severity': severity,
                    'title': title[:100],
                    'batch': i,
                    'text': dsec.strip()
                })

    # Sort by severity then frame
    sev_order = {'HIGH': 0, 'MEDIUM': 1, 'LOW': 2, 'UNKNOWN': 3}
    all_defects.sort(key=lambda d: (sev_order.get(d['severity'], 3), d['frame']))

    high = sum(1 for d in all_defects if d['severity'] == 'HIGH')
    med = sum(1 for d in all_defects if d['severity'] == 'MEDIUM')
    low = sum(1 for d in all_defects if d['severity'] == 'LOW')
    unk = sum(1 for d in all_defects if d['severity'] == 'UNKNOWN')

    print(f"Total: {len(all_defects)} defects (HIGH={high}, MED={med}, LOW={low}, UNK={unk})")

    # Group by frame
    by_frame = defaultdict(list)
    for d in all_defects:
        by_frame[d['frame']].append(d)

    # Write merged report
    out_path = f"/tmp/tikz_defects_iteration_{args.iteration}.md"
    with open(out_path, 'w') as f:
        f.write(f"# TikZ Defect Report -- Iteration {args.iteration}\n\n")
        f.write(f"Total: {len(all_defects)} defects\n")
        f.write(f"- HIGH: {high}\n- MEDIUM: {med}\n- LOW: {low}\n- UNKNOWN: {unk}\n\n")

        for frame_num in sorted(by_frame.keys()):
            defects = by_frame[frame_num]
            defects.sort(key=lambda d: sev_order.get(d['severity'], 3))
            f.write(f"### Frame {frame_num} ({len(defects)} defects)\n\n")
            for d in defects:
                f.write(f"- [{d['severity']}] {d['title']}\n")
            f.write("\n")

    print(f"Report: {out_path}")

    # Create fix assignments for HIGH+MEDIUM frames
    fix_frames = sorted(set(d['frame'] for d in all_defects if d['severity'] in ('HIGH', 'MEDIUM')))
    print(f"Frames needing fixes: {len(fix_frames)}")

    # Group into batches of ~3 frames
    n_fixers = min(10, max(1, len(fix_frames)))
    batch_size = len(fix_frames) // n_fixers if n_fixers > 0 else 0
    remainder = len(fix_frames) % n_fixers if n_fixers > 0 else 0
    idx = 0

    for b in range(n_fixers):
        size = batch_size + (1 if b < remainder else 0)
        batch_frames = fix_frames[idx:idx + size]
        idx += size

        with open(f'/tmp/tikz_fix_assignment_{b:02d}.md', 'w') as f:
            f.write(f"# Fix Assignment Batch {b:02d}\n\n")
            f.write(f"Frames to fix: {batch_frames}\n\n")
            for fn in batch_frames:
                defects = [d for d in by_frame[fn] if d['severity'] in ('HIGH', 'MEDIUM')]
                f.write(f"## Frame {fn} ({len(defects)} HIGH/MEDIUM defects)\n\n")
                for d in defects:
                    f.write(f"{d['text']}\n\n---\n\n")

        print(f"Fix batch {b:02d}: frames {batch_frames}")

if __name__ == '__main__':
    main()
