#!/usr/bin/env python3
"""Verify the accio router against reality.

A router is the one kind of skill where being out of date is worse than not
existing: its whole job is telling you what to invoke next, so a stale entry
sends you somewhere confidently wrong. This is what stops that happening
silently. It is what the retired `toolbox` skill lacked, which is how it came
to be missing 11 of the 24 skills it was the only index for.

Two checks, both of which must pass:

  1. FORWARD   every `/skill` named in SKILL.md resolves to a real skill,
               a known shell builtin, or a declared plugin route.
  2. REVERSE   every user-only skill (disable-model-invocation: true) is
               named somewhere in SKILL.md. Those have no description in the
               model's context, so if the router omits one it is unreachable
               by anything except someone remembering the name.

Usage:
    python accio/scripts/check-routes.py            # check the repo
    python accio/scripts/check-routes.py <dir>      # check an installed copy

Exit 0 clean, 1 on any finding. Safe to wire into a Stop hook or CI.
"""
from __future__ import annotations

import io
import os
import re
import sys

# Reachable, but not skill directories. Keep these lists short and explicit:
# a silent allow-list is how a router rots.
BUILTINS = {"clear", "compact", "goal"}
PLUGIN_ROUTES = {"code-review", "remember"}

ROUTE = re.compile(r"`/([a-z0-9][a-z0-9-]*)`")
FRONTMATTER = re.compile(r"^---\r?\n(.*?)\r?\n---", re.S)


def user_only(skill_dir: str) -> bool:
    path = os.path.join(skill_dir, "SKILL.md")
    try:
        text = io.open(path, encoding="utf-8", errors="replace").read()
    except OSError:
        return False
    m = FRONTMATTER.match(text)
    return bool(m) and "disable-model-invocation: true" in m.group(1)


def main(root: str) -> int:
    skill_md = os.path.join(root, "accio", "SKILL.md")
    if not os.path.isfile(skill_md):
        print("accio/SKILL.md not found under %s" % root)
        return 1

    text = io.open(skill_md, encoding="utf-8", errors="replace").read()
    named = set(ROUTE.findall(text))
    on_disk = {
        d for d in os.listdir(root)
        if os.path.isfile(os.path.join(root, d, "SKILL.md"))
    }

    findings = []

    # 1. forward: nothing named that does not exist
    dead = sorted(named - on_disk - BUILTINS - PLUGIN_ROUTES)
    for d in dead:
        findings.append("DEAD ROUTE   /%s is named in the router but no such skill exists" % d)

    # 2. reverse: no user-only skill left out
    uo = {d for d in on_disk if user_only(os.path.join(root, d))}
    missing = sorted(uo - named - {"accio"})
    for m in missing:
        findings.append("UNREACHABLE  /%s is user-only and absent from the router" % m)

    covered = len(named & on_disk)
    print("routes named: %d  (%d resolve to skills, %d builtin, %d plugin)"
          % (len(named), covered, len(named & BUILTINS), len(named & PLUGIN_ROUTES)))
    print("user-only skills: %d, all named: %s" % (len(uo), "yes" if not missing else "NO"))

    if not findings:
        print("\nOK: router is consistent with the collection.")
        return 0

    print("\n%d finding%s:" % (len(findings), "" if len(findings) == 1 else "s"))
    for f in findings:
        print("  " + f)
    print("\nFix SKILL.md, not this script. A router that names a skill which does not")
    print("exist, or omits one only the user can reach, is worse than no router.")
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else os.getcwd()))
