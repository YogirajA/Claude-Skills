#!/usr/bin/env python
"""Prove the installed hooks fire, and prove they fail open.

Run from the repo root after the harness files are written:

    python .claude/hooks/test-hooks.py

A hook that does not fire is worse than no hook: it reads as protection that is not
there. A hook that crashes on bad input is worse still, because it blocks legitimate
work with no useful message. This checks both.

The fail-open sweep is automatic across every hook found. The fire cases are
repo-specific, so add one per protection you installed: an untested guard is a
finding, not a pass.
"""
import json
import os
import subprocess
import sys

HOOK_DIR = os.path.join(".claude", "hooks")

# --- add one entry per protection installed ------------------------------
# (label, hook filename, stdin payload, expected exit code)
FIRE_CASES = [
    ("blocks .env write", "protect-paths.py",
     {"tool_name": "Write", "tool_input": {"file_path": ".env"}}, 2),
    ("allows ordinary file", "protect-paths.py",
     {"tool_name": "Write", "tool_input": {"file_path": "src/index.ts"}}, 0),
    ("blocks force push", "block-destructive.py",
     {"tool_name": "Bash", "tool_input": {"command": "git push --force origin main"}}, 2),
    ("allows force-with-lease", "block-destructive.py",
     {"tool_name": "Bash", "tool_input": {"command": "git push --force-with-lease"}}, 0),
    # A gate's fire case has to be a real run. With the verifier passing this exits 0;
    # break something first and it should exit 2:
    # ("verify gate passes when green", "verify-on-stop.py", {}, 0),
]

# Hooks that legitimately block on well-formed input, because blocking IS their job.
# A Stop gate exits 2 whenever verification fails, so it is exempt from the
# well-formed sweep below. It is never exempt from the unparseable sweep.
GATE_HOOKS = {"verify-on-stop.py"}
# -------------------------------------------------------------------------

# Not JSON at all. EVERY hook must exit 0, gates included: a hook that dies on
# garbage blocks legitimate work with no usable message.
UNPARSEABLE = ["", "not json", "<<<>>>", "{trailing,", "\x00\x01"]

# Valid JSON that carries nothing to act on. Every non-gate hook must exit 0:
# these are the shapes that reach a hook on turns it has no opinion about.
WELL_FORMED_IRRELEVANT = ["{}", '{"tool_name":"Write"}', "null", "[]", '{"tool_input":null}']


def run(script, payload):
    text = payload if isinstance(payload, str) else json.dumps(payload)
    proc = subprocess.run(
        [sys.executable, os.path.join(HOOK_DIR, script)],
        input=text, capture_output=True, text=True, timeout=60,
    )
    return proc.returncode, (proc.stderr or "").strip()


def main():
    if not os.path.isdir(HOOK_DIR):
        print("No {} directory. Run from the repo root.".format(HOOK_DIR))
        return 1

    hooks = sorted(f for f in os.listdir(HOOK_DIR)
                   if f.endswith(".py") and f != os.path.basename(__file__))
    if not hooks:
        print("No hooks found in {}.".format(HOOK_DIR))
        return 1

    failures = []

    print("Fail-open sweep")
    for hook in hooks:
        is_gate = hook in GATE_HOOKS
        payloads = list(UNPARSEABLE)
        if not is_gate:
            payloads += WELL_FORMED_IRRELEVANT
        bad = []
        for payload in payloads:
            try:
                code, _ = run(hook, payload)
            except Exception as exc:
                bad.append("{!r} raised {}".format(payload, exc))
                continue
            if code != 0:
                bad.append("{!r} exited {}".format(payload, code))
        label = "{} (gate: unparseable only)".format(hook) if is_gate else hook
        if bad:
            failures.append("{} does not fail open: {}".format(hook, "; ".join(bad)))
            print("  FAIL  {}".format(label))
        else:
            print("  ok    {}".format(label))

    print("\nFire cases ({})".format(len(FIRE_CASES)))
    covered = set()
    for label, hook, payload, want in FIRE_CASES:
        covered.add(hook)
        if not os.path.exists(os.path.join(HOOK_DIR, hook)):
            failures.append("{}: {} is not installed".format(label, hook))
            print("  FAIL  {} (hook missing)".format(label))
            continue
        code, err = run(hook, payload)
        if code == want:
            print("  ok    {} (exit {})".format(label, code))
        else:
            failures.append("{}: exit {}, wanted {}".format(label, code, want))
            print("  FAIL  {} (exit {}, wanted {})".format(label, code, want))

    untested = [h for h in hooks if h not in covered]
    if untested:
        print("\nUNTESTED, which counts as a finding, not a pass:")
        for hook in untested:
            print("  {} has no fire case. Add one to FIRE_CASES.".format(hook))

    print()
    if failures:
        print("{} failure(s):".format(len(failures)))
        for line in failures:
            print("  - {}".format(line))
        return 1
    if untested:
        print("All checks passed, but {} hook(s) have no fire case.".format(len(untested)))
        return 1
    print("All hooks fire correctly and fail open.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
