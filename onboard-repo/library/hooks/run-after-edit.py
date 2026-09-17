#!/usr/bin/env python
"""PostToolUse: run the formatter or linter on the file Claude just edited.

Feeding lint output straight back as context is the cheap half of the verification
loop: Claude sees its own mistake immediately, in the same turn, instead of at the end
of a long run. Formatting on save also stops a whole class of diff noise.

PostToolUse cannot block, and on that event a non-zero exit is ignored. So this hook
reports rather than enforces: it returns findings as additionalContext via JSON on
stdout, which is the reliable way to put text in front of Claude here. If something
must be blocked instead, that is a PreToolUse hook or a Stop gate.

Only files matching EXTENSIONS are touched, so editing a markdown file does not invoke
a TypeScript linter.

ADAPT THIS FILE: set COMMANDS to what this repo actually has. An entry whose tool is
not installed is worse than no entry, because it reports noise on every edit.
"""
import json
import os
import subprocess
import sys

# --- adapt per repo -------------------------------------------------------
# Each entry: file extensions, the command ({file} is substituted), and whether
# a non-zero exit is worth reporting back to Claude. Optional keys:
#   "findings_exit": report only this exit code (the tool's "findings remain" code);
#                    any other non-zero exit is a tool problem and stays silent, so a
#                    missing binary cannot spam every edit.
#   "timeout":       seconds for this command, when TIMEOUT_SECONDS is too short.
COMMANDS = [
    {
        "extensions": (".ts", ".tsx", ".js", ".jsx"),
        "command": "npx prettier --write {file}",
        "report_failure": False,     # formatters just fix things; silence is correct
    },
    {
        "extensions": (".ts", ".tsx"),
        "command": "npx eslint {file}",
        "report_failure": True,      # lint findings are the point
    },
    # Python via the modern-python skill: exit 1 when findings remain (one line each with
    # --concise), 2 on a tool error, which findings_exit keeps silent. Take --profile from
    # the project's .claude/modern-python.md; add --target-version pyXY only when that file
    # says target-source: chosen. Expand the home directory here, in Python: shell=True is
    # cmd.exe on Windows, where a literal ~ never expands. Point at the skill's real folder
    # if it is not under ~/.claude/skills. Earned by harness interview section 7 at "enforced".
    # {
    #     "extensions": (".py",),
    #     "command": 'python "' + os.path.expanduser(
    #         "~/.claude/skills/modern-python/scripts/modern_python.py"
    #     ) + '" check --concise --profile modern {file}',
    #     "report_failure": True,
    #     "findings_exit": 1,
    #     "timeout": 180,   # the first run may fetch Ruff through uvx
    # },
]
TIMEOUT_SECONDS = 60
MAX_OUTPUT_CHARS = 2000
# -------------------------------------------------------------------------


def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        return 0
    if not isinstance(data, dict):
        return 0  # valid JSON of the wrong shape (null, a list) must not block either

    if data.get("tool_name") not in ("Write", "Edit", "MultiEdit"):
        return 0

    path = (data.get("tool_input") or {}).get("file_path") or ""
    if not path or not os.path.exists(path):
        return 0

    findings = []
    for entry in COMMANDS:
        if not path.endswith(entry["extensions"]):
            continue
        cmd = entry["command"].format(file='"{}"'.format(path))
        try:
            proc = subprocess.run(
                cmd, shell=True, capture_output=True, text=True,
                timeout=entry.get("timeout", TIMEOUT_SECONDS),
            )
        except Exception:
            continue  # tool missing or hung: stay silent rather than cry wolf

        findings_exit = entry.get("findings_exit")
        if findings_exit is not None:
            reportable = proc.returncode == findings_exit
        else:
            reportable = proc.returncode != 0
        if reportable and entry.get("report_failure"):
            out = ((proc.stdout or "") + (proc.stderr or "")).strip()
            if out:
                findings.append("$ {}\n{}".format(cmd, out))

    if not findings:
        return 0

    text = "\n\n".join(findings)
    if len(text) > MAX_OUTPUT_CHARS:
        text = text[:MAX_OUTPUT_CHARS] + "\n... (truncated)"

    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PostToolUse",
            "additionalContext": (
                "Lint findings for the file you just edited. Fix them now, "
                "while the change is in front of you:\n\n" + text
            ),
        }
    }))
    return 0


if __name__ == "__main__":
    sys.exit(main())
