#!/usr/bin/env python
"""PreToolUse guard: block writes to protected paths.

Prompting can only request that Claude leave a path alone. This enforces it at the
tool level, so the rule holds whether or not the model agrees with it.

Each PROTECTED entry is a glob plus a posture:

  existing_only=True   block edits to files that already exist, allow new ones.
                       This is the "immutable archive" posture: ingest can add a new
                       dated source, but nothing can rewrite history.
  existing_only=False  block the path outright, whether or not the file exists.
                       This is the "never touch" posture, for secrets and generated code.

Exit 2 blocks the call and returns the stderr text to Claude. Any parse problem exits 0
so the hook can never wedge normal work.

ADAPT THIS FILE: edit PROTECTED for the repo. Delete entries that do not apply.
Every entry left here must correspond to a yes in the interview and a HARNESS.md line.
"""
import fnmatch
import json
import os
import sys

# --- adapt per repo -------------------------------------------------------
PROTECTED = [
    {
        "glob": "**/.env*",
        "existing_only": False,
        "reason": "Secrets. Read them through the shell if you need a value, never edit the file.",
    },
    {
        "glob": "**/*.pem",
        "existing_only": False,
        "reason": "Private keys are never edited by an agent.",
    },
    # {
    #     "glob": "raw/**",
    #     "existing_only": True,
    #     "reason": "raw/ holds immutable source documents. Add a new dated file instead.",
    # },
    # {
    #     "glob": "**/migrations/**",
    #     "existing_only": True,
    #     "reason": "Migrations are append-only. Add a new migration, never edit an applied one.",
    # },
]
WATCHED_TOOLS = {"Write", "Edit", "MultiEdit", "NotebookEdit"}
# -------------------------------------------------------------------------


def matches(path, pattern):
    """Match a glob against both the full and repo-relative path.

    fnmatch has no ** semantics, so a leading **/ is also tried as a bare suffix
    match. That keeps '**/.env*' working for both '.env' and 'config/.env.local'.
    """
    candidates = [path]
    cwd = os.getcwd().replace("\\", "/").rstrip("/")
    if path.startswith(cwd + "/"):
        candidates.append(path[len(cwd) + 1:])

    patterns = [pattern]
    if pattern.startswith("**/"):
        patterns.append(pattern[3:])
    if pattern.endswith("/**"):
        patterns.append(pattern[:-3] + "/*")

    for cand in candidates:
        for pat in patterns:
            if fnmatch.fnmatch(cand, pat):
                return True
            # '**' should also cross directory boundaries mid-pattern
            if "**/" in pat and fnmatch.fnmatch(cand, pat.replace("**/", "*/")):
                return True
    return False


def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        return 0  # unparseable input must never block real work
    if not isinstance(data, dict):
        return 0  # valid JSON of the wrong shape (null, a list) must not block either

    if data.get("tool_name") not in WATCHED_TOOLS:
        return 0

    raw_path = (data.get("tool_input") or {}).get("file_path") or ""
    if not raw_path:
        return 0
    path = raw_path.replace("\\", "/")

    for entry in PROTECTED:
        if not matches(path, entry["glob"]):
            continue
        if entry.get("existing_only") and not os.path.exists(raw_path):
            continue  # creating a new file here is allowed
        sys.stderr.write(
            "Denied by protect-paths hook ({}): {}\n".format(entry["glob"], entry["reason"])
        )
        return 2

    return 0


if __name__ == "__main__":
    sys.exit(main())
