# The modern-python interview

Five questions, one `AskUserQuestion` each, in this order. Lead each with a recommendation computed
from the recon below, marked `(Recommended)`, so the user can accept in one word. Skip a question
the recon already settles and say you skipped it. Record every answer verbatim: they become the
answers file, and when this runs from onboard-repo Phase 4b, its `HARNESS.md` justification line.

## Recon first

Reads only. Execute nothing from the project.

| Evidence | Where to look | Feeds |
|---|---|---|
| Declared target | `pyproject.toml` (`requires-python`, `[tool.ruff] target-version`), `ruff.toml` or `.ruff.toml` (`target-version`), `.python-version`, `runtime.txt`, a `Dockerfile` `FROM python:3.x`, CI `python-version:` | Q3 |
| Ruff present | `[tool.ruff]` table, `ruff` in `requirements*.txt` or pyproject dependencies, `.pre-commit-config.yaml`, `.venv/Scripts/ruff.exe` or `.venv/bin/ruff` | Q4 |
| Age and size | `git log --reverse --format=%ad --date=short` first line, commit count, number of `.py` files outside `.venv`, `node_modules` and `__pycache__` | Q1 |
| Existing modernization | `[tool.ruff.lint] select` naming `UP` or `FURB`, `pyupgrade` in pre-commit | Q5 |

`probe` reports the resolved runner and target without editing anything:
`python <skill-dir>/scripts/modern_python.py probe --file <a .py file>`. It can fetch Ruff through
uvx when the project has none, so run it only after Q4 is answered.

## Q1: Codebase

> Is this repo greenfield, or existing code?

| Answer | Stores | Recommend when |
|---|---|---|
| **Greenfield** | `codebase: greenfield`, `convention: override` | First commit under three months old, or fewer than 20 `.py` files |
| **Existing** | `codebase: existing`, `convention: preserve` | Everything else |
| **Existing, modernize it** | `codebase: existing`, `convention: override` | The user says so. State plainly that diffs will touch old patterns near every edit |

## Q2: Enforcement

> When Claude edits Python here, how hard is the modern-idiom check applied?

| Answer | Means |
|---|---|
| **Advisory** | List before editing. No post-edit check |
| **Verified** `(Recommended)` | Post-edit `check`, safe `fix`, `check` again |
| **Enforced** | Verified plus a PostToolUse hook that runs the check on every edited `.py` |

Enforced is offered only when this interview runs from onboard-repo Phase 4b, which installs the
hook with its manifest entry and fire case. Standalone, answer that enforced needs Phase 4b, and
store `verified`.

## Q3: Target version

A declared target was found: confirm it in one line, store `target: pyXY` and
`target-source: declared`, and skip the question unless the evidence disagrees with itself.

No declared target:

> Which Python version must this code run on?

Offer 3.10 through 3.14. Recommend the version named by `.python-version`, `runtime.txt`, a
Dockerfile or CI when any of those exist. With no evidence at all, make no recommendation and ask.
Never read the target off the local interpreter. Store `target: pyXY`, `target-source: chosen`.
If `pyproject.toml` exists, offer to add `requires-python = ">=3.X"` as its own yes. Never create a
`pyproject.toml` for this.

## Q4: Ruff source

Ruff present: store `ruff-fallback: not-needed` and skip.

Absent:

> No Ruff in this project. Allow the pinned fallback: Ruff 0.16.6 through uvx, cached outside the
> repo, nothing added to the project?

| Answer | Stores | Notes |
|---|---|---|
| **Allow** `(Recommended when uvx is on PATH)` | `ruff-fallback: allowed` | One cached download on first use |
| **Add Ruff to the project** | `ruff-fallback: not-needed` | Through the project's manager (`uv add --dev ruff`, `poetry add --group dev ruff`, ...), after a separate yes |
| **Neither** | `ruff-fallback: denied` | The skill then runs advisory with no list and says so on each fire |

## Q5: Profile

> How wide should the modernization guidance be?

| Answer | Prefixes | Recommend when |
|---|---|---|
| **modern** `(Recommended)` | `UP, FURB, SIM, C4, PIE, PTH, FLY, PERF, F401` | Default |
| **core** | `UP, FURB, F401` | The project already runs a broad Ruff selection of its own, to avoid double reporting |

## Write the file

`.claude/modern-python.md`, at the repo root:

```markdown
# modern-python

Answers from the modern-python interview, read before every Python edit.
Re-run with /modern-python setup. Written <YYYY-MM-DD>.

codebase: existing
convention: preserve
enforcement: verified
target: py312
target-source: chosen
ruff-fallback: allowed
profile: modern
```

Create `.claude/` when absent. Show the diff before rewriting an existing file. When run from
onboard-repo Phase 4b, hand the verbatim answers back to it for the `HARNESS.md` entry and let it
install the hook; never write `settings.json` from here.
