# Building the harness (Phase 4b mechanics)

The interview itself is `harness-interview.md`. This file is what to do with its answers. Decision
criteria and provenance for every claim here are in `mechanism-table.md`.

## Order of preference

Where a need could be met more than one way, prefer the lower number.

| # | Mechanism | Why it wins | Context cost |
|---|---|---|---|
| 1 | **Hook** | Deterministic; fires whether or not the model agrees | Zero unless it returns output |
| 2 | **Path-scoped rule** (`paths:`) | Loads only when matching files are touched | Only on match |
| 3 | **settings.json permissions** | Structural, no tokens at all | Zero |
| 4 | **Unscoped rule** | Always loaded, same priority as `.claude/CLAUDE.md` | Every session |
| 5 | **CLAUDE.md line** | Competes with every other line in the file | Every session |
| 6 | **Skill** | Loads on demand | Description every session |

"Never edit `.env`" in CLAUDE.md is a request. A `PreToolUse` hook is a guarantee.

## Propose, then stop

Present the whole proposal as a file tree. For each item give three things:

- the **mechanism** and why it beat the alternatives above
- the **`HARNESS.md` justification line**, quoting the interview answer verbatim
- the **context cost**

Diff anything that already exists. **Then stop and wait.** Never write on the same turn as the
proposal. The user accepts, drops individual items, or edits.

## Write order

Hooks before the settings that reference them, so nothing ever points at a missing file.

1. `.claude/hooks/*` from `library/hooks/`, **adapted** to this repo (paths, commands, messages),
   plus `library/test-hooks.py` alongside them
2. `.claude/settings.json`, **merging** into any existing file. Never clobber keys you did not add
3. `.claude/rules/*.md`, each with `paths:` frontmatter unless the user confirmed it is global
4. `.claude/agents/*.md` and `.claude/skills/*/SKILL.md`, only if interview section 5 earned them
5. The wiki, if section 6 opted in: **invoke `write-wiki`'s bootstrap operation.** Do not create
   `knowledgebase/`, `index.md` or the `~/.claude/CLAUDE.md` registry line yourself; write-wiki owns
   page layout and the federation registry
6. `.claude/HARNESS.md` from the template in `library/templates.md`
7. Append `.claude/settings.local.json` to `.gitignore` if absent

The Phase 4 CLAUDE.md block and its 40-line cap stay untouched. Only ever append a pointer line to
`.claude/HARNESS.md`, and only with consent.

## Adapt, never copy

Every library hook carries an `ADAPT THIS FILE` note. Shipping one unadapted is how you get a guard
that reports noise on every edit, which teaches the user to ignore all of them.

The flag that matters most is `existing_only` in `protect-paths.py`:

- **`True`** is the *immutable archive* posture. Edits to existing files blocked, new files allowed.
  This is what lets an ingest write a new dated source while the archive stays unrewritable.
- **`False`** is the *never touch* posture, for secrets and generated code, where whether the file
  exists is irrelevant.

Reaching for the second where the first was meant blocks legitimate creation, and the user disables
the hook rather than fixing the flag.

## Verify

A hook that does not fire is worse than no hook: it reads as protection that is not there.

1. Run `python .claude/hooks/test-hooks.py`. It sweeps every hook for fail-open behaviour and runs
   the declared fire cases
2. **Add a fire case per protection installed.** The runner reports an untested hook as a finding,
   not a pass, and exits non-zero for it
3. Confirm `settings.json` parses:
   `python -c "import json;json.load(open('.claude/settings.json'))"`
4. Confirm every `permissions.allow` entry names a command Phase 3 actually executed
5. Tell the user to run `/context` to confirm rules load as expected

Two failure modes the sweep exists to catch, both found in testing this library:

- **A hook that dies on odd input.** `null` and `[]` are valid JSON, so `json.load` succeeds and the
  next `.get()` raises. The hook exits non-zero and blocks legitimate work with no usable message
- **A gate that looks broken but is not.** A `Stop` hook exiting 2 on well-formed input is doing its
  job. The sweep separates unparseable input (every hook must survive) from valid-but-irrelevant
  input (only non-gates must pass through), via the `GATE_HOOKS` set

Report what fired, what did not, and what you could not test. **Untested is a finding, not a pass.**

## Re-run mode

If `.claude/HARNESS.md` already exists:

1. Report its entries and flag any past their review date
2. For each overdue entry ask whether the original justification still holds. **Removal is the
   default answer.** Cherny's rule is that you cannot predict which instruction the model needs, so
   you delete and let repeated failure tell you
3. Read the "Not installed, and why" table before proposing anything, so you do not re-pitch
   something already declined
4. Offer: review overdue entries, add new items, or full refresh
