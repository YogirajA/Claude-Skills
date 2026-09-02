#!/usr/bin/env python
"""PreToolUse guard: block irreversible shell commands.

Reach for this only where a plain pattern in permissions.deny is not enough, which is
mostly where the decision needs a little logic (a force-push is fine to a scratch branch
and not to main). For a flat ban, permissions.deny costs nothing and needs no script.

Every pattern here is about REVERSIBILITY, not danger in the abstract. A command that
git can undo does not belong in this list; a command that destroys history, published
artefacts or production state does.

Exit 2 blocks and returns the stderr text to Claude. Parse problems exit 0.

ADAPT THIS FILE: delete the patterns that do not apply to this repo. A long list nobody
chose is exactly the cruft this whole skill exists to prevent.
"""
import json
import re
import sys

# --- adapt per repo -------------------------------------------------------
# (compiled pattern, what to tell Claude instead)
BLOCKED = [
    (
        # lookahead sits right after `push` so it scans the whole command; placing it
        # after the alternation instead lets `--force-with-lease` match on its `--force`
        r"\bgit\s+push\b(?!.*--force-with-lease).*(--force|-f)\b",
        "Force-push rewrites published history. Use --force-with-lease, or push a new branch.",
    ),
    (
        r"\bgit\s+reset\s+--hard\b",
        "git reset --hard discards uncommitted work irreversibly. Use git stash first.",
    ),
    (
        r"\bgit\s+clean\s+-[a-z]*f",
        "git clean -f deletes untracked files with no recovery. List them first with -n.",
    ),
    (
        r"\brm\s+(-[a-zA-Z]*r[a-zA-Z]*f|-[a-zA-Z]*f[a-zA-Z]*r)\b",
        "Recursive force delete. Remove specific paths, or move them aside instead.",
    ),
    (
        r"\bgit\s+branch\s+-D\b",
        "Capital -D force-deletes an unmerged branch. Use -d, which refuses if work would be lost.",
    ),
    # (r"\bnpm\s+publish\b", "Publishing is irreversible. The user runs this themselves."),
    # (r"\bterraform\s+(apply|destroy)\b", "Infrastructure changes are the user's call."),
    # (r"\bdrop\s+(table|database)\b", "Destructive SQL. The user runs this themselves."),
]
BLOCKED = [(re.compile(p, re.IGNORECASE), msg) for p, msg in BLOCKED]
# -------------------------------------------------------------------------


def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        return 0
    if not isinstance(data, dict):
        return 0  # valid JSON of the wrong shape (null, a list) must not block either

    if data.get("tool_name") not in ("Bash", "PowerShell"):
        return 0

    command = (data.get("tool_input") or {}).get("command") or ""
    if not command:
        return 0

    for pattern, message in BLOCKED:
        if pattern.search(command):
            sys.stderr.write(
                "Denied by block-destructive hook: {}\n"
                "If this is genuinely what the user asked for, say so and let them run it.\n"
                .format(message)
            )
            return 2

    return 0


if __name__ == "__main__":
    sys.exit(main())
