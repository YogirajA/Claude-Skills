Review of the upstream script at arwtyxouymz/modern-python-guidelines 7501dd4, written 2026-09-16 before vendoring. Line numbers refer to the upstream file, not to scripts/modern_python.py, which carries the edits this review asked for (see its header).

# Read-only review: `modern_python.py` (arwtyxouymz/modern-python-guidelines @ 7501dd4)

Reviewed 2026-09-17 by reading only; nothing was executed. Subject: the local copy at
`C:\Users\yogia\AppData\Local\Temp\modern_python.py` (1,381 lines, md5
`a53089b7db60cd16749954aabcb535e7`). Also read: upstream `tests/test_modern_python.py`,
`SKILL.md`, `run-tool.sh`, `run-tool.ps1` (fetched into the session scratchpad, not the repo).

This report answers the open items in `scratchpad/modern-python-guidelines.md` (checklist item
1: every subprocess and every write; the fallback-download policy; the unknown-target case;
whether to keep `fix` and `--unsafe-fixes`; the Windows wrappers) and does not repeat its survey.

Conventions: bare line numbers refer to the script; `test:N` and `SKILL:N` refer to the upstream
test file and skill file. "Exit 2" is the script's `ToolError` path (1374-1376), "exit 3" its
`RuffUpdateRequired` path (1371-1373). Claims about what Ruff itself prints are marked as such;
they come from my knowledge of Ruff's source, not from a run.

## 1. Every subprocess invocation

There is one choke point. `run_process` (231-249) calls
`subprocess.run(argv, check=False, capture_output=True, text=True, timeout=..., input=..., cwd=...)`
at 239-247. There is no `shell=True` anywhere and argv is always a tuple or list, so no shell
quoting is involved. `OSError` (binary missing) and `TimeoutExpired` become a `ToolError`
"could not execute ..." (248-249). No `env=` is passed, so children inherit the whole
environment. Every Ruff call goes through `invoke_ruff` (312-322), which accepts return codes 0
and 1 and turns anything else into `ToolError("Ruff failed: <first stderr line>")` (319-321).

Runner candidates (195-228), probed in this order until one answers `--version`:

| Order | Lines | argv as built | Source label |
|---|---|---|---|
| 1 | 198-203 | `shlex.split($MODERN_PYTHON_RUFF_COMMAND, posix=os.name != "nt")` | project |
| 2 | 150-156, 205-207 | `<root>/.venv/bin/ruff` or `<root>/.venv/Scripts/ruff.exe` (absolute) | project |
| 3 | 159-170, 209-210 | `pixi run ruff` (bare name; only if `pixi.toml`, `pixi.lock` or a `[tool.pixi]` table exists and `which("pixi")` succeeds) | project |
| 4 | 212-219 | `poetry run ruff`, `pdm run ruff`, `pipenv run ruff` (bare names; gated on `poetry.lock`, `pdm.lock`, `Pipfile` plus `which`) | project |
| 5 | 221-222 | `<which("ruff")>` (absolute) | ambient |
| 6 | 224-226 | `<sys.executable> -m ruff` | ambient |
| 7 | 173-183 | `<which("uvx")> --from ruff==0.16.6 ruff` | bundled |
| 8 | 184-191 | `<which("pipx")> run ruff==0.16.6` | bundled |

The pin `0.16.6` is read from `ruff-fallback.txt` beside the script (142-147) on every
invocation (174, called from 227), not only when the fallback is used.

Invocations, in the order they occur in the file:

| Line | Command (argv shape) | Purpose | Timeout | On failure |
|---|---|---|---|---|
| 254 | `<candidate argv> --version` | Probe a runner candidate. Accepted only if rc 0 and stdout starts with `ruff ` (258). | 30 s | Candidate skipped, first stderr line recorded (260-261, 286). If the failing candidate is the env override: abort, exit 2 (287-288). All fail: exit 2 "Ruff is unavailable. Install Ruff in the project or install uv/pipx for the bundled fallback. Attempts: ..." (292-296). A failed project-tier candidate becomes a warning when a lower tier wins (271-275). |
| 254 via 301 | `<uvx> --from ruff==0.16.6 ruff --version`, then `<pipx> run ruff==0.16.6 --version` | Probe the bundled reference for the staleness comparison. `list` only (1176). | 30 s | Warning "Could not compare the project Ruff with the bundled reference; continuing..." and go on (1177-1181). |
| 451-454 | `ruff check --show-settings <subject> [--isolated]` | Read the resolved target, preview flags, enabled rules, per-file matchers, config path. Every subcommand except `explain`. | 180 s | Ruff rc 2 (for example "No files found under the given path"): exit 2. Missing target line: `CapabilityError` (417), which is exit 2 because `resolve_settings` runs before `list`'s `try` (1118 vs 1133). |
| 499 | `ruff rule --all --output-format json`, then `ruff rule --all --format json` | Rule inventory. | 180 s | Both fail, or JSON invalid, or not a list of dicts: `CapabilityError` (505-510). In `list`: exit 3, or degraded exit 0 with `--allow-stale`, or exit 2 when the runner is bundled (1135-1143). |
| 624-640 | `ruff check <tmpdir> --isolated --target-version pyXY --select <codes> --output-format json --exit-zero --ignore-noqa --no-cache [--preview]` | Run Ruff's own documented examples to learn which rules fire under the target. Twice per guideline set (679, 688); four times when a reference comparison runs (1183). | 180 s | Invalid JSON or non-list: `CapabilityError` (641-646). Ruff rc 2: exit 2. |
| 728-731 | `ruff check --show-settings <subject> --config <tmp>/ruff.toml [--preview]` | Expand the profile selectors into concrete codes. `check`/`fix` only (983). | 180 s | Wrapped as exit 2 "could not resolve the project's explicit Ruff ignores safely before check/fix" (990-993). |
| 938-955, run at 994 | `ruff check <absolute paths, or cwd> --select <selectors> --output-format json --exit-zero [--ignore <codes>] [--preview] [--fix [--unsafe-fixes]]` | The `check` and `fix` subcommands. | 180 s | Ruff rc 2: exit 2. `--exit-zero` means findings never change the exit code. |
| 1011 | `ruff rule <CODE> --output-format json`, then `ruff rule <CODE> --format json` | `explain`, once per unique code. | 180 s | Unknown code (Ruff rc 2) or non-dict JSON: exit 2 "Ruff could not explain <CODE> as JSON" (1016-1017). |

Call counts with a warm runner whose first candidate succeeds: `probe` 2, `explain` 1 + one per
code, `check`/`fix` 4, `list` 5 (9 with a reference comparison, plus up to 2 reference probes).
On this machine, with no Ruff installed, each command spends 6 failed probes (candidates 2 to 6
are absent, the env override is unset) before reaching uvx.

## 2. Every filesystem write

| Line | Path | What is written | Touches the user's project? |
|---|---|---|---|
| 601, 610, 617-619 | `tempfile.TemporaryDirectory(prefix="modern-python-guidelines-")`, then `<CODE>/example_NNN.py` (or `.pyi`, 585-586) | Every ```python fence from each UP/FURB rule explanation; in the second pass `from __future__ import annotations` is prepended when absent (613-616) | No. System temp, removed by the context manager. |
| 725-727 | `tempfile.TemporaryDirectory(prefix="modern-python-policy-")`, then `ruff.toml` | `target-version = "pyXY"` and `[lint] select = [...]` (721-723). The `extend = "<project config>"` variant (715-719) is dead code: the only caller passes `inherit_project=False` (983-985). | No. |
| 952-954 (argv), 994 (run) | The user's files named in `paths` | `fix` passes `--fix` to Ruff, which rewrites the files in place | Yes. The only intentional project write. |
| 938-955 | `<project root>/.ruff_cache/` | Ruff's cache, because `check`/`fix` omit `--no-cache` (the example run at 636 includes it) | Yes, indirectly. Ruff creates its own `.gitignore` inside, so `git status` stays clean. |
| 180, 187 (argv) | uv and pipx caches (`%LOCALAPPDATA%\uv\cache` or `~/.cache/uv`; `~/.local/pipx`) | Ruff 0.16.6 wheel and its venv, written by uvx/pipx on the first probe | No. Outside the project. |

`fix` in detail:

- Files: exactly the `paths` given, resolved to absolute (937, via `intended_path` 325-327).
  With no path at all the list becomes `[str(Path.cwd())]` (937), so `fix` rewrites every
  Python file under the current directory. SKILL:60 says to pass the touched files; the script
  does not enforce it.
- Rules: the profile (default `UP,FURB,SIM,C4,PIE,PTH,FLY,PERF,F401`, 25-29) minus the
  project's reconstructed global ignores (987-989, passed as `--ignore` at 947-948). The
  project's `per-file-ignores`, `fixable`/`unfixable` and `# noqa` comments apply natively,
  because the run uses the project configuration (no `--isolated`, no `--config` at 938-955).
- Without `--unsafe-fixes` Ruff applies only fixes it marks safe. Unsafe candidates stay in the
  output with `fix.applicability == "unsafe"` and the file is untouched for them.
- With `--unsafe-fixes` (953-954) Ruff also applies behavior-changing fixes. There is no dry
  run, diff, or backup at either level, and the script prints only the remaining diagnostics
  (998), so what changed is visible only through `git diff`.
- `F401` in both profiles means `fix` deletes every unused import Ruff finds in the named files,
  including ones unrelated to the current edit (SKILL:94 states this as the intent).

## 3. Every environment variable read

| Line | Variable | What it controls |
|---|---|---|
| 31, 198-203 | `MODERN_PYTHON_RUFF_COMMAND` | The only variable read by name. Highest-priority runner, split with `shlex.split(..., posix=os.name != "nt")` and executed verbatim. If it fails the probe the script aborts with exit 2 instead of falling through (287-288). |
| 200 | `os.name` | Selects POSIX or non-POSIX shlex mode. |
| 225 | `sys.executable` | The `-m ruff` candidate. |
| 176, 184, 209, 218, 221 | `PATH` (and `PATHEXT` on Windows) through `shutil.which` | Whether pixi, poetry, pdm, pipenv, ruff, uvx, pipx are considered. |
| 860 | `HOME` / `USERPROFILE` through `Path.expanduser` | An `extend = "~/..."` entry in a Ruff config chain. |
| 601, 725 | `TMPDIR` / `TEMP` / `TMP` through `tempfile` | Where the example and policy directories are created. |
| 239 | The entire environment, inherited by children | No `env=` argument, so Ruff, uv and pipx honor `RUFF_CACHE_DIR`, `UV_CACHE_DIR`, `UV_INDEX_URL`, `PIPX_HOME`, proxy variables, and so on. `VIRTUAL_ENV` is not consulted for runner discovery. |

## 4. Network surface

Direct: none. The imports (6-23) are `argparse, fnmatch, json, os, re, shlex, shutil,
subprocess, sys, tempfile, collections.abc.Sequence, dataclasses, pathlib, tomllib`. A grep for
`http`, `socket`, `urllib`, `request`, `ssl`, `ftp`, `urlopen`, `download` finds only the word
"requested" in a warning string (1129). The script never opens a connection itself.

Indirect paths, all through child processes:

1. Runner discovery fallback (227, probed at 254). Any subcommand, whenever candidates 1 to 6
   all fail. On this machine (no Ruff, `uvx` on PATH, no `pipx`) that is the default path for
   every command: the first run downloads Ruff 0.16.6 into uv's cache; later runs resolve from
   the cache (whether uv still contacts the index is uv's policy, outside the script). The whole
   download has to fit inside the 30 s probe budget (254).
2. Bundled reference comparison (1169-1176, 299-309). `list` only, when the chosen runner is
   project or ambient and its version is lower than 0.16.6 (1173). It probes uvx then pipx, so
   it downloads even when the project has a working Ruff, and even with `--allow-stale`
   (`should_compare` at 1169-1174 does not consult that flag). No consent is asked for this
   download: the exit-3 protocol covers updating the project's Ruff, not fetching the reference.
3. Manager-run candidates (210, 213-215). `pixi run ruff` solves and installs the environment on
   first use if it is missing, which is a network operation; `poetry run`, `pdm run` and
   `pipenv run` do not install.
4. Ruff itself never uses the network.

## 5. Target-version resolution, step by step

1. Start directory (`runner_start`, 1344-1351): `list`, `probe` and `explain` use `--file`;
   `check` and `fix` use the first path, else cwd. A file becomes its parent directory.
2. Project root (`find_project_root`, 122-139): walk upward from there and stop at the first
   directory containing any of `pyproject.toml, ruff.toml, .ruff.toml, uv.lock, pixi.toml,
   pixi.lock, poetry.lock, pdm.lock, Pipfile, .git`. No marker anywhere: the start directory
   itself. This root is the `cwd` of every Ruff call (318) and the base for the `.venv` lookup.
3. Subject (`settings_subject`, 330-349): the file itself if it exists. Otherwise the root's
   `ruff.toml`, `.ruff.toml` or `pyproject.toml`; otherwise any `*.py`/`*.pyi` in the file's
   directory or the root; otherwise the script's own path with `--isolated` (349, 452-453).
   Every case but the first sets `inferred_file_context`.
4. `ruff check --show-settings <subject>` (451-454). Ruff discovers configuration by its own
   rules from cwd upward, and falls back to a user-level config (`%APPDATA%\ruff\ruff.toml` or
   `~/.config/ruff/ruff.toml`) when the project has none.
5. A `--target-version pyXY` override wins (456-461), validated by `^py3[0-9]{1,2}$` (34),
   with source `command-line override`.
6. Otherwise `target_from_settings` (408-432):

   ```python
   base_match = re.search(
       r"^linter\.unresolved_target_version = (3\.[0-9]+)$", settings, re.MULTILINE
   )
   if base_match is not None:
       target = base_match.group(1)
   else:
       legacy_match = re.search(r"^linter\.target_version = Py3?([0-9]+)$", settings, re.MULTILINE)
       if legacy_match is None:
           raise CapabilityError("Ruff did not report a resolved target Python version")
       target = f"3.{legacy_match.group(1)}"
   source = "Ruff resolved target"
   ```

   then per-file target entries (420-431) override it with source `per-file-target-version`.
7. Config attribution (473-476):

   ```python
   config_match = re.search(r'^Settings path: "(.+)"$', settings_text, re.MULTILINE)
   config_path = Path(config_match.group(1)) if config_match else None
   if target_source == "Ruff resolved target" and config_path is not None:
       target_source = config_path.name
   ```

The no-config case (NPC-Investments: `requirements.txt` and `.git`, nothing else):

- Root is the git root (`.git` marker). Subject is the target file. Ruff finds no
  `pyproject.toml`, `ruff.toml` or `.ruff.toml` above cwd, so it uses default settings. Ruff's
  `show_settings` prints the `Settings path:` line only when a configuration file was found, so
  `config_path` is `None` and `target_source` stays the literal `"Ruff resolved target"`.
- Which target Ruff falls back to: the script neither knows nor pins it; it accepts whatever
  `linter.unresolved_target_version` says. By my reading of Ruff's source, the `TargetVersion`
  display prints the linter's default for an unset target (py39 in the Ruff docs I know, after
  a bump from py38; 3.9 reached end of life in October 2025, so 0.16.6 may well print `3.10`).
  If a Ruff version ever printed something not matching `3\.[0-9]+`, the script would exit 2
  with "Ruff did not report a resolved target Python version" (417). The `probe` command in the
  scratchpad's checklist item 2 settles the exact value in one run.
- Whether the script reports it as inferred or defaulted: neither. `inferred_file_context` is
  false (the file exists), the two warning sources at 1126-1131 cover only runner warnings and a
  missing file, and `status` is `"ok"` (1261). The only signal is the literal string
  `Ruff resolved target` in `target_source`, which appears exactly when no config file was
  discovered or `--isolated` was used. The wiki's "report unknown, never infer from the
  interpreter" rule is half met (the interpreter is never consulted) and half unimplemented (the
  default is presented as a resolved fact). A five-line patch at 475-476 plus one warning fixes
  that.
- What `list` prints in that case, text format (1050-1087), assuming the default is 3.9 and the
  bundled runner:

  ```
  Modern Python Guidelines
  File: src\scoring\verdict.py
  Target: Python 3.9 (Ruff resolved target)
  Ruff: 0.16.6 [U+2014] bundled uvx fallback [bundled]
  Preview: disabled
  Guidelines: 38 baseline, 4 conditional, 0 ignored by project policy

  Baseline means Ruff's official examples diagnose under the resolved target. The post-edit check can still surface configuration-dependent guidance.

  Baseline guidelines:
  UP004 Checks for useless class inheritance from `object`.
  UP006 Checks for the use of generics that can be replaced with standard library variants based on PEP 585.
  ...

  Conditional with postponed annotations:
  UP007 Checks for the use of `Union` in type annotations...
  ```

  Counts and descriptions are illustrative. `[U+2014]` marks the em dash the script hardcodes
  at 1053. No `Ignored:` line and no `Warnings:` block appear, since the project has no policy
  and the runner produced no warnings.

## 6. What `list` does

1. Arguments (1299-1315): `--file` (required), `--target-version`, `--preview`, `--allow-stale`,
   `--format text|json` (default text).
2. Root and runner (1357-1358) as in section 5. Any runner failure is exit 2.
3. `resolve_settings(..., require_file=True)` (1118-1123): a directory is rejected (448-449,
   exit 2); a missing file is accepted and marked inferred, with a warning (1127-1131).
4. Preview flags (1124-1125): `preview_mode = project preview or --preview`;
   `include_preview_rules = preview_mode or project explicit-preview-rules`.
5. Guideline set (`build_guideline_set`, 669-703):
   - Inventory via `ruff rule --all` (494-511).
   - Keep codes starting with `UP` or `FURB` (30, 533-534) whose status is `Stable`, or
     `Preview` when included (537-551). Status comes from the `status` dict's first key, or a
     `## Removed` / `## Deprecated` heading in the explanation, or the `preview` flag (519-530).
     Deprecated and removed rules are dropped here and never reach the output.
   - Extract every ```python or ```py fence from each explanation (35, 566-572). Both the
     "bad" and the "use instead" blocks are extracted and written; only the bad one is expected
     to fire.
   - Write them to a temp dir and run Ruff twice: plain, then with
     `from __future__ import annotations` prepended (679-696). A code is **baseline** when a
     diagnostic with that code lands in that code's own subdirectory (656-657); cross-firing on
     another rule's example is ignored. **Conditional** = fires only with the future import and
     the explanation mentions `__future__`, "future annotations" or "postponed annotations"
     (661-666, 698-702). Rules with no fence go into `missing_example_codes` (678) and are
     reported in a warning (1238-1242); they can never be baseline.
6. Failure split (1135-1152): a `CapabilityError` here with the bundled runner is re-raised (exit
   2). With a project or ambient runner and no `--allow-stale`: exit 3 with "... Ask the user
   whether to update the project's Ruff. Do not update it without approval. If they decline,
   rerun `list --allow-stale` ...". With `--allow-stale`: the degraded payload (1090-1114),
   `status: "degraded"`, empty lists, exit 0.
7. Policy (`resolve_policy`, 882-894, called at 1157-1164): global ignores are reconstructed by
   parsing the project's config file chain with tomllib or a hand parser (845-866, 755-842),
   minus codes Ruff reports as natively enabled (877-879); preview codes require native exact
   selection when the project sets `explicit-preview-rules` and `--preview` was not passed
   (1161-1163, 892); per-file ignores are matched against the intended file (741-746).
8. Staleness comparison (1165-1206): only when the runner is not bundled and
   `parse_version(runner) < 0.16.6`. Probes uvx/pipx (network, section 4), builds a second full
   guideline set with Ruff 0.16.6 (four more Ruff calls, two more temp dirs) and diffs
   (904-914): `missing` = reference codes, allowed by policy, that the project Ruff does not have
   active; `retired` = project codes the reference no longer has active.
9. Exit 3 (1207-1227) when either list is non-empty and `--allow-stale` is absent; the message
   names up to 12 codes per side and ends "If they decline, rerun `list --allow-stale` and do
   not ask again during this task." With `--allow-stale` the same facts become warnings
   (1228-1237) and retired codes are subtracted from the output (1244-1245).
10. Output sets (1244-1249): `baseline = baseline_codes & allowed - retired`, likewise
    conditional; `ignored = available - allowed`. Sort key (554-563): all UP first, then FURB,
    ascending by number, so oldest rules first. That is the opposite of the Go pack's
    newest-first order the scratchpad wants to carry over.
11. Render (`render_guidelines`, 1043-1087). The compact text shape:

    ```
    Modern Python Guidelines
    File: <path relative to cwd, or absolute across drives>
    Target: Python <X.Y> (<source>)
    Ruff: <version> [U+2014] <runner label> [<project|ambient|bundled>]
    Preview: <enabled|disabled>
    Guidelines: <n> baseline, <m> conditional, <k> ignored by project policy
    Ignored: <codes>                                  (only when k > 0)

    Baseline means Ruff's official examples diagnose under the resolved target. The post-edit check can still surface configuration-dependent guidance.

    Warnings:                                         (only when any)
    - <warning>

    Baseline guidelines:                              (only when non-empty)
    <CODE> <one line: the "## What it does" paragraph collapsed, else summary, else name>

    Conditional with postponed annotations:           (only when non-empty)
    <CODE> <description>
    ```

    `<source>` is one of `command-line override`, `per-file-target-version`, the config file's
    basename (`pyproject.toml`, `ruff.toml`, `.ruff.toml`), or `Ruff resolved target`.

    JSON (`--format json`, 1259-1279): `status, file, target_python, target_version,
    target_source, runner, runner_source, ruff_version, preview, explicit_preview_rules,
    inferred_file_context, baseline_count, conditional_count, ignored_count, ignored_codes,
    baseline[], conditional[], warnings[]`, where each rule is
    `{code, name, description, status, applicability}` (1022-1033) and applicability is
    `baseline` or `postponed-annotations`. Printed with `indent=2, sort_keys=True,
    ensure_ascii=False` (1284).

Exit codes for `list`: 0 for ok and degraded; 3 for the two `RuffUpdateRequired` triggers (step
6 without `--allow-stale` on a non-bundled runner; step 9 without `--allow-stale`); 2 for every
other `ToolError`/`CapabilityError` (no runner, settings parse failure, malformed
`--target-version`, directory `--file`, bundled-runner capability failure); argparse usage
errors also exit 2; an uncaught exception (missing `ruff-fallback.txt` at 143, an encoding
error, see section 8) exits 1 with a traceback. On this machine, where the runner is bundled,
`list` can exit 0 or 2 but never 3.

Preview and removed rules, summarized: `--preview` or a project `preview = true` adds
Preview-status rules to the candidate set and passes `--preview` to the example runs (638-639);
a project `explicit-preview-rules = true` admits only preview rules the project selects by exact
code; removed and deprecated rules are dropped at step 5; rules the bundled reference has retired
are additionally subtracted at step 10 when `--allow-stale` is in effect.

## 7. What `check`, `fix` and `explain` do

`check` (977-998; parser 1320-1322):

1. Selectors: `--rules` (comma list, uppercased, each matching `^[A-Z]+[0-9]*$`, 917-927),
   else `--profile core|modern` (25-29, default `modern`).
2. Settings resolved for `paths[0]` or `.` (979-980); directories are allowed here.
3. Expand the selectors into concrete codes with a temp config (983-986), then reconstruct the
   project's global ignores (987-989). Any failure in this step is exit 2 (990-993): the script
   fails closed rather than checking with the project's ignores dropped.
4. Run `ruff check` as in section 1 (994). Output: Ruff's JSON array verbatim, `[]` when
   empty (998). Each Ruff diagnostic object carries `code, message, filename,
   location{row,column}, end_location, fix{applicability, message, edits[]} or null,
   noqa_row, url, cell`.
5. Exit 0 whenever Ruff ran (`--exit-zero`, 945); 2 on Ruff rc 2 or any `ToolError`. Findings
   never change the exit code, so a hook could not use it directly.

`fix` (1365-1366): identical, plus `--fix` and optionally `--unsafe-fixes` (951-954). The
output is the diagnostics that remain after fixing; nothing reports what was changed. Write
surface: section 2.

`explain` (1001-1019; parser 1333-1339): for each unique code, uppercase it and require
`^[A-Z]+[0-9]+$` (32, 1004-1006; `up045` is accepted, a bare prefix such as `UP` is exit 2),
run `ruff rule CODE --output-format json`, require a dict. Output:
`{"ruff_version": "<v>", "rules": [<Ruff's full rule object: name, code, linter, summary,
message_formats, fix, explanation (full markdown), preview, status>, ...]}` (1019), in the
order requested. Exit 0; 2 for an invalid or unknown code. `--file` only steers runner discovery
(1337, 1346); there is no settings resolution and no temp write. Any prefix is accepted, not
only UP/FURB.

`probe` (958-974), for completeness: resolves settings for `--file` (default `.`) and prints
runner label, source and argv, Ruff version, target and its source, preview flags,
`inferred_file_context`, the default profile and prefixes, and warnings. Exit 0 or 2.

## 8. Windows concerns

1. Venv lookup (150-156) checks `.venv/bin/ruff` and `.venv/Scripts/ruff.exe`: correct on
   Windows. Only `.venv` is recognized, not `venv`, `env` or `VIRTUAL_ENV`.
2. `shutil.which` honors `PATHEXT`, so it finds `.exe`, `.cmd` and `.bat`. But the pixi, poetry,
   pdm and pipenv candidates are launched by bare name (210, 213-215) and `CreateProcess`
   appends only `.exe`. A manager installed as a `.cmd` shim passes `which`, then fails the probe
   with `FileNotFoundError`, which surfaces as the "project-managed Ruff runner was detected but
   unavailable" warning (271-275). It degrades rather than breaks. uvx, pipx, the PATH ruff and
   the venv ruff use absolute paths and are fine.
3. `shlex.split(..., posix=False)` on Windows (200) keeps quote characters inside tokens. A
   quoted `MODERN_PYTHON_RUFF_COMMAND` (which is exactly how the upstream tests set it, test:136)
   yields argv entries that still contain literal double quotes; `subprocess` then escapes those
   quotes again and the launch fails. Unquoted values without spaces work. By reading, the
   upstream suite would not pass on Windows for this reason; its CI presumably runs on Linux.
4. Encoding, the most likely real breakage here. `run_process` uses `text=True` with no
   `encoding` (243), so Ruff's UTF-8 output is decoded with the locale codec (cp1252 on this
   machine's Python 3.13; UTF-8 mode becomes the default only in 3.15). Ruff's rule explanations
   contain non-ASCII characters (curly quotes, arrows). Best case: mojibake in the descriptions
   and in the example files written back at 617; worst case: `UnicodeDecodeError`, an uncaught
   traceback, exit 1, when a multibyte sequence hits one of cp1252's five undefined bytes. On the
   output side `print_json` uses `ensure_ascii=False` (1284) and `print` uses the same codec, so
   `explain` output containing a character outside cp1252 raises `UnicodeEncodeError` when
   stdout is a pipe, which is how Claude Code captures it. Fix: `encoding="utf-8",
   errors="replace"` at 243 and `sys.stdout.reconfigure(encoding="utf-8")` at the top of
   `main`, or `PYTHONUTF8=1` in whatever launches the script.
5. Path matching (392-405): backslashes are normalized to `/` and `fnmatchcase` is
   case-sensitive. Ruff's `absolute_matcher` values are Debug-escaped (`C:\\Users\\...`), which
   `parse_setting_string` un-escapes through `json.loads` (357-365). Both sides come from
   `Path.resolve()` (135, 399), so the drive-letter case should agree, but a per-file target or
   per-file ignore could silently fail to match on a case difference. Low.
6. `Settings path: "..."` (473): Ruff prints it with `.display()`, not Debug, so single
   backslashes; `Path()` handles that. The `json.dumps(str(config_path))` at 717 would have
   escaped it correctly for TOML, but that branch is dead.
7. Wrappers. `run-tool.ps1` tries `py -3` then `python` and propagates `$LASTEXITCODE`, which
   is right, but it needs an execution policy that allows local scripts (client Windows defaults
   to Restricted). `run-tool.sh` prefers `python3`, which on Windows can resolve to the Microsoft
   Store alias stub from Git Bash (prints an install prompt, exits 9009). Under Git Bash with the
   python.org interpreter `os.name` is still `nt`, so item 3 applies there too; MSYS converts the
   `/c/...` script path for the native interpreter, so the path itself is fine. Recommendation:
   skip both wrappers and have SKILL.md call `python <skill-dir>/scripts/modern_python.py`.
8. Minor: `display_path` (1036-1040) falls back to absolute across drives; temp dirs go to
   `%TEMP%`; a `.git` file (worktrees) satisfies `.exists()` (137); `subprocess.run(timeout=...)`
   kills only the direct child on Windows, so a timed-out `uvx` may leave `ruff.exe` running for
   a moment. All low.

## 9. Test coverage

Seventeen tests, all driven through a fake Ruff script substituted via
`MODERN_PYTHON_RUFF_COMMAND` (test:31-123, test:136). Real Ruff is never run.

Covered:

- `probe` fields (test:146); `check` profile, JSON and `--exit-zero` flags (test:154).
- `list` baseline order and removed-rule exclusion (test:162); future-annotations conditional
  at `py39` (test:173); missing metadata exit 3 and `--allow-stale` degraded (test:187).
- `fix` safe by default and `--unsafe-fixes` pass-through (test:203, test:209).
- `explain` returns the requested codes in order (test:214) and rejects an invalid one
  (test:219).
- Pixi candidate and `[tool.pixi]` detection (test:224, test:240); pin format (test:246).
- Per-file target and per-file ignore matching against one file (test:249); `## Removed`
  heading (test:275); `reference_differences` as a pure function (test:279);
  explicit-preview-rules gating as a pure function (test:300); ignore selectors from
  `pyproject.toml` via tomllib (test:325).

Not covered:

- Any real `--show-settings` or `rule --all` output. The fake's format (test:83-92) is what the
  regexes were written against, so drift in Ruff's format is invisible to the suite.
- The fake never prints `Settings path:`, so every end-to-end test runs the no-config branch.
  Untested: config attribution (475-476), `extend` chains and cyclic detection (849-866), the
  Python 3.10 text parser (784-842), and `global_ignored_codes` actually reaching `--ignore` on
  `check`/`fix`.
- Runner discovery order end to end (venv, PATH, `-m ruff`, uvx/pipx) and the
  project-unavailable warning.
- The staleness comparison and its exit 3 (1165-1227): the fake reports version 9.8.7, above the
  pin, so `should_compare` is always false.
- Text rendering (only `--format json` is asserted), `settings_subject` inference for a missing
  file, `--target-version` validation, a directory `--file`, `check`/`fix` with no paths,
  timeouts, Ruff rc 2, Windows quoting, encoding.
- The tests locate the script by a hardcoded relative path (test:14-23), so they would need a
  path edit to run against a vendored copy.

## 10. Surprises and risks

| # | Finding | Lines | Rating |
|---|---|---|---|
| 1 | `fix` (and `check`) with no path argument operate on the whole current directory; `fix` then rewrites every Python file under it. SKILL.md advises otherwise, the script does not enforce it. | 937 | High |
| 2 | `list` downloads Ruff 0.16.6 through uvx/pipx without consent whenever the project's own Ruff is older than the pin, even with `--allow-stale`. The exit-3 consent covers updating the project's Ruff, not fetching the reference. | 1169-1176, 299-309 | Medium |
| 3 | With no Ruff anywhere, every subcommand's discovery ends in the uvx/pipx download inside a 30 s probe; a slow first download surfaces as "Ruff is unavailable" (the partial download stays in uv's cache, so a retry usually succeeds). | 227, 254 | Medium |
| 4 | A defaulted target is reported as `Ruff resolved target` with `status: "ok"` and no warning (section 5). The wiki's "report unknown" rule is unimplemented. | 419, 473-476 | Medium |
| 5 | Locale-codec decoding of Ruff's output and encoding of the script's stdout on Windows (section 8, item 4). | 243, 1284 | Medium |
| 6 | Everything depends on Ruff's `--show-settings` text format, which Ruff treats as debugging output. A format change surfaces as exit 3 "update Ruff" (misleading when the newer Ruff caused it) or exit 2. | 353, 370-378, 410, 415, 465, 468, 473, 735 | Medium |
| 7 | The script re-parses TOML configuration itself and follows `extend` chains that may leave the project tree and expand `~`. | 755-866, 860 | Low |
| 8 | `.ruff_cache/` is created in the project root by `check`/`fix` (self-gitignored by Ruff). | 938-955 | Low |
| 9 | `ruff-fallback.txt` is read on every command; a missing file is an uncaught traceback, exit 1. | 143, 174, 227 | Low |
| 10 | Hardcoded em dash (U+2014) in the text renderer. | 1053 | Low (house style) |
| 11 | `F401` in both profiles: `fix` removes pre-existing unused imports in the named files, not only ones the modernization made unused. | 26-27 | Low |
| 12 | `pixi run` may solve and install an environment during the probe. | 210 | Low |
| 13 | Dead code: the `extend` config branch, the `input_text` parameter, the legacy `--format json` and `linter.target_version` fallbacks. Harmless, but it is a third of the surface a reader must clear. | 715-719, 316-318, 497, 1009, 415 | Low |
| 14 | Oldest-first ordering, opposite to the Go pack's newest-first. | 554-563 | Low |
| 15 | `MODERN_PYTHON_RUFF_COMMAND` runs any command verbatim. Only relevant if the environment is attacker-controlled. | 198-203 | Low |
| 16 | A Ruff user-level config supplies the target when the project has none, and is reported by its basename (`ruff.toml`) as if it were the project's. | 473-476 | Low |
| 17 | The example-execution baseline is heuristic: rules whose example only fires under a project setting, or whose fence is missing, drop out silently apart from the `missing_example_codes` warning. The script documents this in its own output text (1064-1067). | 606-607, 656-657 | Low |

Nothing found that phones home, reads secrets, escalates, or writes outside temp, the
uv/pipx cache, `.ruff_cache`, and the files explicitly named to `fix`.

## 11. Verdict

### (a) Safe to vendor as-is?

Yes on safety: stdlib only, no direct network, no shell, writes confined to temp dirs and to
Ruff's `--fix` on named files. Not as-is on behavior. Lines to change before shipping, in
priority order:

1. 937: require paths for `fix` (make the `fix` subparser's `paths` `nargs="+"` at 1331, or
   raise a `ToolError` when `args.paths` is empty and `fix` is true). Optionally the same for
   `check`.
2. 1165-1237: delete the bundled-reference comparison, or gate it behind an explicit
   `--compare-reference` flag. That removes the unconsented download (risk 2), roughly 100 lines,
   and the second exit-3 trigger. Keep the first trigger (1138-1143): a project Ruff too old to
   emit rule JSON is a real stop.
3. 475-476: when `config_path is None` and there is no override, set `target_source` to
   something like `Ruff default (no project configuration found)` and append a warning, so the
   agent sees the unknown-target case that is the common path on this machine.
4. 243: `encoding="utf-8", errors="replace"`; and `sys.stdout.reconfigure(encoding="utf-8")`
   at the top of `main` (1354).
5. 1053: replace the em dash with a comma or parentheses.
6. 938-955: add `--no-cache` so `check`/`fix` do not create `.ruff_cache/`.
7. 142-147: inline the pin as a constant (`PINNED_RUFF = "0.16.6"`) and drop
   `ruff-fallback.txt`, or wrap the read in a `ToolError`.
8. 1324-1331: drop `--unsafe-fixes`. The skill's write surface should stay at Ruff's safe fixes;
   an agent that wants an unsafe change can edit by hand after `explain`. Keep `fix` itself:
   safe fixes plus a re-`check` is the useful half of the protocol. This answers the checklist's
   open item.
9. Wrappers: leave `run-tool.sh` and `run-tool.ps1` out and call the script with `python`
   directly from SKILL.md (section 8, item 7).

Fallback-download policy (the scratchpad's open decision): keep the uvx fallback in runner
discovery (change 2 removes the other download path). It is the difference between working on
day one here and not, it is pinned, cached outside the project, and the runner label
`bundled uvx fallback [bundled]` is printed on every `list`, so the agent can say so. Consider
dropping the pipx candidate (184-191) since it adds a second downloader for no gain here.

### (b) If we wrote our own thin script instead

Behaviors of this script that a thin replacement over the project's Ruff would have to
reimplement, with a rough size each:

1. Runner discovery with a `--version` probe and a priority order (env override, `.venv`,
   PATH, `-m ruff`, uvx): about 50 lines (this file spends 150 on it with pixi, poetry, pdm,
   pipenv and the warning bookkeeping).
2. Project-root detection by marker walk: 15 lines.
3. Target resolution from `ruff check --show-settings` (the `unresolved_target_version` regex,
   the `Settings path` attribution, the "no config found" label): 30 lines. Per-file target
   versions add another 60 (the matcher block parser at 352-405).
4. Rule inventory from `ruff rule --all --output-format json` with status filtering and
   sorting: 40 lines.
5. The example-execution baseline (fence extraction, temp dir, two Ruff runs, the
   future-annotations split): 90 lines. This is the irreducible core, because Ruff's rule JSON
   has no "minimum target" field; running the documented examples under the target is the only
   general way to learn which UP/FURB rules apply, short of hand-curating a table that rots.
6. Project-ignore preservation for `check`/`fix`: 190 lines here (706-895). A thin script can
   likely replace all of it by passing `--extend-select` instead of `--select` and filtering the
   JSON by code prefix afterwards, since Ruff carries configured ignores over an
   `--extend-select`; that needs one verification run.
7. `check`/`fix` argv building and JSON pass-through: 30 lines.
8. `explain`: 20 lines.
9. Text and JSON rendering: 50 lines.
10. Preview and explicit-preview-rules handling: 25 lines, or drop it and document "preview off".
11. Missing-file subject inference (330-349) for new files: 20 lines, or require
    `--target-version` for new files.
12. The consent protocol against a bundled reference: 120 lines here; a thin script would drop
    it and let SKILL.md say "if `ruff_version` is older than X, ask".

Total for a thin script that keeps items 1 to 5 and 7 to 9: roughly 350 to 450 lines, against
1,381 here, with items 6, 10, 11 and 12 either simplified or omitted.

### (c) Recommendation

Vendor it with the nine edits above, because the review found nothing unsafe, the part a
rewrite could not skip (the example-execution baseline and the settings parsing) has already been
shaped against real Ruff output that we would otherwise rediscover by trial, and the edits
mostly delete code rather than add it. Revisit the thin rewrite only if Ruff's `--show-settings`
format breaks the parsing more than once, at which point the `--extend-select` simplification in
(b) item 6 is the design to start from.
