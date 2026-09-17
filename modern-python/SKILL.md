---
name: modern-python
description: Version-gated modern Python guidance backed by Ruff. Use before writing, editing, fixing or refactoring any Python file: list the rules the project's target version allows, apply them, verify. /modern-python setup runs the per-project interview.
license: MIT
metadata:
  version: "7501dd4"
  author: arwtyxouymz
  based_on: JetBrains/go-modern-guidelines (Apache-2.0; the shape, the two-stage retrieval and the call protocol)
  origin: arwtyxouymz/modern-python-guidelines
  imported: "2026-09-17: scripts/modern_python.py and LICENSE copied from https://github.com/arwtyxouymz/modern-python-guidelines at 7501dd4 (MIT), with the edits listed in the script's header: paths required for check and fix, the bundled-reference comparison removed, a defaulted target labelled and warned, UTF-8 forced, no .ruff_cache, the Ruff pin inlined, unsafe fixes removed, pipx dropped, non-zero exit when findings remain. Upstream tests vendored into tests/ and extended. Written here, not upstream: this SKILL.md, the per-project interview in references/interview.md, the answers file, the onboard-repo hook-in, and the four clauses taken from the JetBrains SKILL.md (read the whole list, no truncating pipes, override local convention with three named exits, skipping costs an explain call). Left out: the wrapper scripts, the marketplace manifests, CI, the smoke and distribution scripts. Vendored rather than installed as a plugin, because third-party plugin sources are out of policy here. Needs Python 3.10 or newer on PATH, and Ruff from the project or the pinned fallback through uvx when the interview allowed it."
---

# Modern Python

Ruff is the rule database and the project's target Python version is the gate. The bundled tool
lists only the modernization rules whose own Ruff examples diagnose under that target, so nobody
curates a rule table and the guidance tracks Ruff. It corrects two things at once: training-data
lag (a feature newer than the model) and frequency bias (the older pattern the model reaches for
out of habit).

Tool: `python <skill-dir>/scripts/modern_python.py`, where `<skill-dir>` is this folder.
Subcommands: `list`, `explain`, `check`, `fix`, `probe`.

## Step 0: the project's answers

Read `.claude/modern-python.md` at the repo root. It holds the interview answers: `codebase`,
`convention`, `enforcement`, `target`, `target-source`, `ruff-fallback`, `profile`.

- Present: continue with its values.
- Absent: run the interview in [`references/interview.md`](references/interview.md) once, write
  the file, continue. If the user declines the interview, proceed with `enforcement: advisory`,
  `convention: preserve`, no target override, say so once, and do not ask again this session.
- `/modern-python setup` re-runs the interview and rewrites the file.

## Before editing Python

1. List the guidance that applies to the file you are about to touch:

   ```sh
   python <skill-dir>/scripts/modern_python.py list --file path/to/file.py --target-version <target> --profile <profile>
   ```

   Omit `--target-version` when `target-source: declared`. For a file that does not exist yet,
   pass `--target-version` from the answers file.

2. Exit 3 means the project's Ruff is too old to report rule metadata. Ask whether to update Ruff
   through the project's own manager (uv, Poetry, PDM, pre-commit). On yes, update and rerun. On
   no, rerun with `--allow-stale` and rely on the post-edit check.

3. Read the complete output. Do not pipe it through head, tail, grep, sed, or any other truncating
   or filtering command: a rule dropped there is a rule you will violate. Baseline rules diagnose
   under the target now; conditional ones need `from __future__ import annotations`.

4. For every listed rule that may touch the code you plan to write, read its explanation before
   editing:

   ```sh
   python <skill-dir>/scripts/modern_python.py explain --file path/to/file.py UP045 FURB123
   ```

   Skipping a relevant rule costs the same call: explain it first, then skip with the reason
   stated.

5. Apply the convention the answers file sets:
   - `convention: override`: follow a returned rule even when nearby code or repository
     convention uses the older pattern. Three exits only: it would not run on the target, it
     would change behaviour, or it clearly does not match the edited code.
   - `convention: preserve`: inside existing files, match the surrounding pattern. Use the modern
     idiom in new files and new functions, and everywhere when the task is a modernization pass.

6. Write the code. The target version is the compatibility boundary: no syntax or stdlib API newer
   than it. When the tool reports `Ruff default (no project configuration found)` and the answers
   file carries no target, the target is unknown: avoid version-gated syntax and say so.

## After editing Python

`enforcement: advisory`: done after the edit. Report which rules you applied.

`enforcement: verified` or `enforced`:

1. Check the files you touched (exit 1 means findings remain):

   ```sh
   python <skill-dir>/scripts/modern_python.py check path/to/file.py
   ```

2. `explain` each finding you do not already understand. Fix by hand, or apply Ruff's safe fixes:

   ```sh
   python <skill-dir>/scripts/modern_python.py fix path/to/file.py
   ```

3. `check` again until it exits 0, or name the remaining findings and the documented caveat that
   applies to each.

4. Run the project's own formatter, type checker and tests for the changed code. This check
   supplements them.

`enforced` additionally means a PostToolUse hook runs the same check on every edited `.py` file
and returns findings as context. That hook is installed only by onboard-repo Phase 4b, with its
`HARNESS.md` entry and a tested fire case; this skill never writes `settings.json`. Asked for
enforcement outside onboarding: say to run onboard-repo and re-run Phase 4b alone.

## Profiles

`core` is `UP, FURB, F401`. `modern` (default) adds `SIM, C4, PIE, PTH, FLY, PERF`. Preview
rules stay off unless the project opts in.

## Done when

The listed rules were read in full, every relevant one was applied or explained away, the edit
respects the target, and under verified or enforced the check exits 0 or the remaining findings
are named with their caveat.
