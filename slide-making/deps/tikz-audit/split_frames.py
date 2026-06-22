#!/usr/bin/env python3
"""Split a beamer tex file at frame boundaries for parallel editing.

Usage: python3 split_frames.py <tex_file> --n-segments 10 [--output-dir /tmp/tikz_segments]

Creates:
  /tmp/tikz_segments/header.tex       — everything before first frame
  /tmp/tikz_segments/seg_00.tex       — frames for batch 0
  /tmp/tikz_segments/seg_01.tex       — frames for batch 1
  ...
  /tmp/tikz_segments/footer.tex       — everything after last frame
  /tmp/tikz_segments/manifest.json    — batch assignments (frame ranges per segment)

Reassemble: cat header.tex seg_00.tex seg_01.tex ... seg_NN.tex footer.tex > output.tex
"""
import re, sys, os, json, argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('tex_file', help='Path to the beamer tex file')
    parser.add_argument('--n-segments', type=int, default=10,
                        help='Number of segment files to create')
    parser.add_argument('--output-dir', default='/tmp/tikz_segments',
                        help='Directory for segment files')
    args = parser.parse_args()

    with open(args.tex_file) as f:
        content = f.read()
    lines = content.split('\n')

    # Find frame boundaries
    frame_starts = []  # (line_index, frame_number)
    frame_ends = []    # (line_index, frame_number)
    frame_num = 0

    for i, line in enumerate(lines):
        if re.match(r'\s*\\begin\{frame\}', line):
            frame_num += 1
            frame_starts.append((i, frame_num))
        if re.match(r'\s*\\end\{frame\}', line):
            frame_ends.append((i, frame_num))

    if not frame_starts:
        print("ERROR: No frames found in file")
        sys.exit(1)

    print(f"Found {len(frame_starts)} frames")

    # Pair up starts and ends
    frames = []
    for start_idx, fn in frame_starts:
        # Find matching end
        matching_end = None
        for end_idx, en in frame_ends:
            if end_idx > start_idx and en == fn:
                matching_end = end_idx
                break
        if matching_end is None:
            # Use the next end after this start
            for end_idx, _ in frame_ends:
                if end_idx > start_idx:
                    matching_end = end_idx
                    break
        if matching_end is not None:
            frames.append((start_idx, matching_end, fn))

    print(f"Paired {len(frames)} frames")

    # Split into segments
    n_seg = min(args.n_segments, len(frames))
    batch_size = len(frames) // n_seg
    remainder = len(frames) % n_seg

    os.makedirs(args.output_dir, exist_ok=True)

    # Header: everything before first frame
    header_end = frames[0][0]
    header = '\n'.join(lines[:header_end])
    with open(os.path.join(args.output_dir, 'header.tex'), 'w') as f:
        f.write(header + '\n')

    # Segments
    manifest = {'source': args.tex_file, 'segments': []}
    idx = 0
    for seg in range(n_seg):
        size = batch_size + (1 if seg < remainder else 0)
        batch_frames = frames[idx:idx + size]
        idx += size

        if not batch_frames:
            continue

        seg_start = batch_frames[0][0]
        seg_end = batch_frames[-1][1]

        # Include any lines between frames (comments, blank lines)
        if seg > 0:
            prev_end = frames[idx - size - 1][1] if idx - size > 0 else header_end
            seg_start_actual = prev_end + 1
        else:
            seg_start_actual = seg_start

        if seg < n_seg - 1 and idx < len(frames):
            seg_end_actual = seg_end
        else:
            seg_end_actual = seg_end

        seg_content = '\n'.join(lines[seg_start_actual:seg_end_actual + 1])
        seg_file = f'seg_{seg:02d}.tex'
        with open(os.path.join(args.output_dir, seg_file), 'w') as f:
            f.write(seg_content + '\n')

        frame_nums = [fn for _, _, fn in batch_frames]
        manifest['segments'].append({
            'file': seg_file,
            'frames': frame_nums,
            'line_start': seg_start_actual + 1,  # 1-indexed
            'line_end': seg_end_actual + 1,
        })
        print(f"Segment {seg:02d}: frames {frame_nums[0]}-{frame_nums[-1]} "
              f"(lines {seg_start_actual+1}-{seg_end_actual+1})")

    # Footer: everything after last frame
    footer_start = frames[-1][1] + 1
    footer = '\n'.join(lines[footer_start:])
    with open(os.path.join(args.output_dir, 'footer.tex'), 'w') as f:
        f.write(footer + '\n')

    # Write manifest
    with open(os.path.join(args.output_dir, 'manifest.json'), 'w') as f:
        json.dump(manifest, f, indent=2)

    print(f"\nOutput: {args.output_dir}/")
    print(f"Reassemble: cd {args.output_dir} && "
          f"cat header.tex {' '.join(f'seg_{i:02d}.tex' for i in range(n_seg))} "
          f"footer.tex > reassembled.tex")


if __name__ == '__main__':
    main()
