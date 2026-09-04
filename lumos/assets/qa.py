#!/usr/bin/env python3
"""
QA checker for a single-file field guide.

Usage:  python qa.py path/to/guide.html

Checks (each prints PASS/FAIL):
  - no em dashes (U+2014) anywhere
  - every [N] citation (href="#ref-N") resolves to an id="ref-N"
  - no reference is defined but never cited (catches orphans)
  - every internal href="#anchor" resolves to a matching id
  - reports doc-page / concept-card counts as a sanity check

Exit code is non-zero if any hard check fails, so it is CI-friendly.
"""
import re
import sys


def main(path: str) -> int:
    html = open(path, encoding="utf-8").read()
    ok = True

    # 1. Em dashes
    em = html.count("—")
    print(f"[{'PASS' if em == 0 else 'FAIL'}] em dashes (U+2014): {em}")
    ok &= em == 0

    # 2/3. Citation integrity
    ref_ids = set(re.findall(r'id="ref-(\d+)"', html))
    ref_links = set(re.findall(r'href="#ref-(\d+)"', html))
    cited_undefined = sorted(int(x) for x in ref_links - ref_ids)
    print(f"[{'PASS' if not cited_undefined else 'FAIL'}] citations resolve: "
          f"{'none missing' if not cited_undefined else cited_undefined}")
    ok &= not cited_undefined
    orphans = sorted(int(x) for x in ref_ids - ref_links)
    # orphan references are a soft warning, not a hard fail
    print(f"[{'PASS' if not orphans else 'WARN'}] no orphan references: "
          f"{'none' if not orphans else orphans}")

    # 4. Internal anchors
    all_ids = set(re.findall(r'id="([^"]+)"', html))
    href_anchors = set(re.findall(r'href="#([^"]+)"', html))
    broken = sorted(a for a in href_anchors if a and a not in all_ids)
    print(f"[{'PASS' if not broken else 'FAIL'}] internal anchors resolve: "
          f"{'none broken' if not broken else broken}")
    ok &= not broken

    # 5. Sanity counts
    pages = html.count('class="doc-page')
    concepts = len(re.findall(r'<div class="concept[ "]', html))
    print(f"[INFO] doc-pages: {pages}  concept-cards: {concepts}  "
          f"references: {len(ref_ids)}")

    print("\nRESULT:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(2)
    sys.exit(main(sys.argv[1]))
