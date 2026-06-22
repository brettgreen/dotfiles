#!/usr/bin/env python3
"""Apply TikZ fix patches from JSON files to a tex file.

Usage: python3 apply_patches.py <tex_file> [--n-batches 10] [--dry-run]
Input:  /tmp/tikz_fix_patches_NN.json (one per fixer batch)
Output: Modified tex file (in place) + /tmp/tikz_patch_report.md

Patch JSON format:
[
  {
    "frame": 5,
    "defect": "Text clips right edge",
    "old_string": "exact string from file",
    "new_string": "replacement string"
  }
]
"""
import json, os, sys, argparse
from datetime import datetime


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('tex_file', help='Path to the tex file to patch')
    parser.add_argument('--n-batches', type=int, default=10)
    parser.add_argument('--dry-run', action='store_true',
                        help='Validate patches without applying')
    args = parser.parse_args()

    with open(args.tex_file) as f:
        content = f.read()

    all_patches = []
    load_errors = []

    for i in range(args.n_batches):
        path = f"/tmp/tikz_fix_patches_{i:02d}.json"
        if not os.path.exists(path):
            continue

        try:
            with open(path) as f:
                raw = f.read().strip()
            # Handle agents wrapping JSON in markdown code blocks
            if raw.startswith('```'):
                lines = raw.split('\n')
                lines = [l for l in lines if not l.startswith('```')]
                raw = '\n'.join(lines)
            patches = json.loads(raw)
            if not isinstance(patches, list):
                patches = [patches]
            for p in patches:
                p['batch'] = i
            all_patches.extend(patches)
        except (json.JSONDecodeError, KeyError) as e:
            load_errors.append(f"Batch {i:02d}: {e}")

    print(f"Loaded {len(all_patches)} patches from {args.n_batches} batches")
    if load_errors:
        print(f"Load errors: {len(load_errors)}")
        for err in load_errors:
            print(f"  - {err}")

    # Validate: each old_string must appear exactly once
    valid = []
    invalid = []
    for p in all_patches:
        old = p.get('old_string', '')
        if not old:
            invalid.append((p, 'empty old_string'))
            continue

        count = content.count(old)
        if count == 0:
            invalid.append((p, 'old_string not found'))
        elif count > 1:
            invalid.append((p, f'old_string found {count} times (ambiguous)'))
        else:
            pos = content.find(old)
            valid.append((pos, p))

    print(f"Valid: {len(valid)}, Invalid: {len(invalid)}")

    # Check for overlapping patches
    valid.sort(key=lambda x: x[0])
    non_overlapping = []
    for i, (pos, patch) in enumerate(valid):
        end = pos + len(patch['old_string'])
        overlaps = False
        for j, (pos2, patch2) in enumerate(non_overlapping):
            end2 = pos2 + len(patch2['old_string'])
            if pos < end2 and end > pos2:
                overlaps = True
                invalid.append((patch, f'overlaps with frame {patch2.get("frame", "?")} patch'))
                break
        if not overlaps:
            non_overlapping.append((pos, patch))

    valid = non_overlapping
    print(f"After overlap check: {len(valid)} valid, {len(invalid)} invalid")

    if args.dry_run:
        print("\n--- DRY RUN (no changes applied) ---")
    else:
        # Apply bottom-up (reverse position order) to preserve offsets
        valid.sort(key=lambda x: x[0], reverse=True)
        for pos, patch in valid:
            old = patch['old_string']
            new = patch['new_string']
            content = content[:pos] + new + content[pos + len(old):]

        with open(args.tex_file, 'w') as f:
            f.write(content)
        print(f"\nApplied {len(valid)} patches to {args.tex_file}")

    # Write report
    report_path = '/tmp/tikz_patch_report.md'
    with open(report_path, 'w') as f:
        f.write(f"# TikZ Patch Report\n\n")
        f.write(f"Generated: {datetime.now().isoformat()}\n")
        f.write(f"File: {args.tex_file}\n")
        f.write(f"Mode: {'DRY RUN' if args.dry_run else 'APPLIED'}\n\n")
        f.write(f"## Summary\n\n")
        f.write(f"- Patches loaded: {len(all_patches)}\n")
        f.write(f"- Valid & applied: {len(valid)}\n")
        f.write(f"- Invalid/skipped: {len(invalid)}\n")
        f.write(f"- Load errors: {len(load_errors)}\n\n")

        if valid:
            f.write(f"## Applied Patches ({len(valid)})\n\n")
            for _, p in sorted(valid, key=lambda x: x[1].get('frame', 0)):
                f.write(f"- Frame {p.get('frame', '?')}: {p.get('defect', 'unknown')[:80]}\n")
            f.write("\n")

        if invalid:
            f.write(f"## Invalid Patches ({len(invalid)})\n\n")
            for p, reason in invalid:
                f.write(f"- Frame {p.get('frame', '?')}: {reason} — {p.get('defect', '')[:60]}\n")
            f.write("\n")

    print(f"Report: {report_path}")
    return len(invalid)


if __name__ == '__main__':
    sys.exit(main())
