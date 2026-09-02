#!/usr/bin/env python
"""Stop hook: refuse to end the turn while the verification command fails.

This is the mechanism behind "give the model a way to check its own work". Without it,
"looks done" is the only stop signal available and the user becomes the verification
loop. With it, Claude runs, checks, reads the failure and iterates on its own.

Three things worth knowing before installing this:

  1. Claude Code overrides a Stop hook after 8 consecutive blocks. This is a strong
     gate, not an infinite one, so a genuinely stuck run still terminates.
  2. It runs at the end of EVERY turn, not just the last one. A slow command taxes the
     whole session. Over roughly two minutes, prefer a reminder rule instead.
  3. The skip-if-unchanged guard below keeps the cost off turns that changed nothing
     (answering a question, reading files). Without it a chat turn pays for a test run.

Exit 2 blocks the turn and hands stderr back to Claude. Anything unexpected exits 0:
a broken verifier must not trap the user in a turn that cannot end.

ADAPT THIS FILE: set COMMAND to the command Phase 3 actually executed. Never a command
that has not been run and observed to pass.
"""
import hashlib
import json
import os
import subprocess
import sys

# --- adapt per repo -------------------------------------------------------
COMMAND = "npm test"          # must be a command that has actually been executed
TIMEOUT_SECONDS = 120         # over ~120s, prefer a rule over this hook
MAX_OUTPUT_CHARS = 4000       # truncate so a huge failure log cannot flood context
SKIP_IF_UNCHANGED = True      # skip when no tracked file changed since the last pass
STATE_FILE = ".claude/.verify-state"
# -------------------------------------------------------------------------


def fingerprint():
    """Cheap signal for 'did anything change since last time'."""
    try:
        head = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            capture_output=True, text=True, timeout=10,
        ).stdout.strip()
        status = subprocess.run(
            ["git", "status", "--porcelain"],
            capture_output=True, text=True, timeout=10,
        ).stdout.strip()
        diff = subprocess.run(
            ["git", "diff", "HEAD"],
            capture_output=True, text=True, timeout=20,
        ).stdout
    except Exception:
        return None  # not a git repo, or git unavailable: always run
    return hashlib.sha256((head + status + diff).encode("utf-8", "replace")).hexdigest()


def main():
    try:
        json.load(sys.stdin)
    except Exception:
        return 0

    # Do not re-enter: if this hook already blocked and Claude is stopping again
    # without changing anything, let the turn end rather than spin.
    fp = fingerprint() if SKIP_IF_UNCHANGED else None
    if fp:
        try:
            with open(STATE_FILE) as fh:
                if fh.read().strip() == fp:
                    return 0  # unchanged since the last pass
        except Exception:
            pass

    try:
        proc = subprocess.run(
            COMMAND, shell=True, capture_output=True, text=True, timeout=TIMEOUT_SECONDS,
        )
    except subprocess.TimeoutExpired:
        sys.stderr.write(
            "Verification command timed out after {}s: {}\n"
            "Either it is genuinely hung, or this command is too slow for a Stop hook.\n"
            .format(TIMEOUT_SECONDS, COMMAND)
        )
        return 2
    except Exception:
        return 0  # cannot run the verifier: do not trap the turn

    if proc.returncode == 0:
        if fp:
            try:
                os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
                with open(STATE_FILE, "w") as fh:
                    fh.write(fp)
            except Exception:
                pass
        return 0

    output = ((proc.stdout or "") + (proc.stderr or "")).strip()
    if len(output) > MAX_OUTPUT_CHARS:
        output = output[:MAX_OUTPUT_CHARS] + "\n... (truncated)"
    sys.stderr.write(
        "Verification failed, so the turn is not done. `{}` exited {}.\n\n{}\n\n"
        "Fix the root cause and let this run again. Do not suppress the failure, "
        "do not weaken the test, and do not edit this hook to get past it.\n"
        .format(COMMAND, proc.returncode, output)
    )
    return 2


if __name__ == "__main__":
    sys.exit(main())
