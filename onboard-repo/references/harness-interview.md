# The interview

Six sections, in this order. Each is one `AskUserQuestion` call. The order matters: autonomy sets
how strict everything downstream should be, and verification is the highest-value answer in the set.

**Lead every section with a recommendation** computed from Phases 0 to 3, marked `(Recommended)`. The user
should be able to accept in one word. **Skip any section Phases 0 to 3 already settled** and say you skipped
it. A section you skip because the repo answered it is the interview working correctly.

Record every answer verbatim. Answers become the justification lines in `HARNESS.md`, so a section
that produces no usable answer produces no installed item.

---

## Section 1: Autonomy

> How far do you walk away while Claude works in this repo?

| Option | Means | Sets the posture to |
|---|---|---|
| **Watched** | You read most diffs before they land | Minimal. Guardrails only where the blast radius is real |
| **Semi-autonomous** | Auto mode, you check in at milestones | Standard. Guardrails plus a verification gate |
| **Unattended** | Long runs, `/goal`, cron, you read the result | Strict. Everything gated, because nobody is watching |

Recommend from evidence: a repo with a green test suite and clean git history supports
**semi-autonomous**. A repo with no runnable tests cannot support **unattended**, whatever the user
prefers, and you should say so rather than install a gate that cannot gate anything.

**Sets:** how aggressively sections 2 and 3 propose. Under **watched**, propose only the deny rules.
Under **unattended**, the Stop-hook verification gate is close to mandatory and you should say why.

---

## Section 2: Verification

Cherny's claim is that verification, not prompting, is what lets a run go long. This section is the
reason the skill exists; do not rush it.

> When Claude says it is done here, what command proves it?

Lead with the command Phase 3 actually ran, with its real runtime. Offer:

| Option | Installs | When |
|---|---|---|
| **Stop-hook gate** | `verify-on-stop.py` running the verified command | Semi-autonomous or unattended, command under ~2 min |
| **Reminder rule** | Path-scoped rule naming the command | Watched, or the command is slow |
| **Nothing yet** | Records the gap in `HARNESS.md` as the top finding | No command runs |

Two things to state plainly rather than bury:

- Claude Code **overrides a Stop hook after 8 consecutive blocks**. It is a strong gate, not an
  infinite one, so a genuinely stuck run still terminates.
- A slow command in a Stop hook taxes **every turn**, not just the last one. Over about two minutes,
  prefer the rule and let the user run the command themselves.

If nothing runs, say so directly: a repo with no feedback loop is exactly where Claude produces
confident garbage. That sentence belongs in the report.

---

## Section 3: Danger zones

> What in this repo must never be touched, whatever Claude decides?

Multi-select. Pre-tick anything recon (Phase 0) found evidence for (a `.env`, a `migrations/` directory, a
protected branch, a deploy script).

| Zone | Installs | Notes |
|---|---|---|
| Secrets (`.env`, `*.pem`, keyfiles) | `protect-paths.py` | Near-universal. Still requires a yes |
| Migrations, schema files | `protect-paths.py` glob | Append-only is usually the real rule |
| Generated code, lockfiles, vendored deps | `protect-paths.py` glob | Cheap and stops a whole class of churn |
| Destructive git and shell | `block-destructive.py` | Force-push, hard reset, `rm -rf`, history rewrite |
| Deploy, publish, release | `permissions.deny` | Structural. No script needed |
| Workflow-normal but irreversible (push = deploy, publish the user requests) | `permissions.ask` | Deny breaks the workflow, allow lets unattended runs fire it silently |
| Immutable source dirs | `protect-paths.py` | The `raw/` pattern from the knowledgebase repo |

**Ask what deploy actually is on this repo before filling this table.** Where deploying is a git
push (Railway-style push-to-deploy), plain `git push` is an irreversible action wearing a safe
command's name: offer it under `permissions.ask`, and under **Unattended** autonomy say plainly that
leaving it ungated means an unattended run can ship. List the rewritten form too if a
command-rewriting hook is in play, since ask rules are prefix matches.

**Prefer `permissions.deny` over a hook** when a plain pattern match is enough. It costs nothing and
there is no script to maintain. Reach for a hook when the decision needs logic, such as "block edits
to existing files here but allow new ones".

---

## Section 4: Repeated corrections

This is Anthropic's own trigger ("Claude gets a convention wrong twice") asked directly.

> What do you find yourself correcting Claude on, more than once, in this repo specifically?

Open-ended, then classify each answer yourself:

| Shape of answer | Goes to |
|---|---|
| Applies only to certain files | Path-scoped rule with `paths:` |
| Applies everywhere, and is a fact | CLAUDE.md line (hand to onboard-repo, do not write it here) |
| Applies everywhere, and must hold every time | Hook |
| Is a multi-step procedure | Section 5, not here |
| The model already gets it right | **Nothing.** Say so and move on |

That last row is the one that matters. Cherny: "You don't want to guess what's the instruction that
the model needs, because you might not predict it correctly." If the user names something Claude
already does correctly, do not install a rule for it. Tell them it is already handled.

Every rule you write here must have `paths:` unless the user confirms it is genuinely global.

---

## Section 5: Repeated procedures

The skill trigger: "you paste the same playbook a third time."

> Is there a multi-step procedure you type or paste repeatedly for this repo?

| Answer | Installs |
|---|---|
| A procedure with side effects (deploy, release, migrate) | Project skill with `disable-model-invocation: true` |
| A procedure without side effects (review checklist, PR body) | Project skill |
| A read-heavy investigation that floods context | Subagent in `.claude/agents/` |
| Nothing comes to mind | **Nothing.** This is the expected answer on a first pass |

"Nothing comes to mind" is the common and correct answer. A procedure the user has not yet repeated
is a guess, and a skill that is never invoked still leaks its description into every session.

Set `disable-model-invocation: true` on anything with side effects. It removes the description from
context entirely and guarantees only the user can fire it.

---

## Section 6: Knowledge base

The wiki is the pull layer: knowledge Claude fetches when it needs it, rather than context it
carries every session. A repo with real accumulated knowledge and no wiki pays for that knowledge in
CLAUDE.md lines instead, which is the expensive place to keep it.

> Should this repo get its own knowledge base, or read from the General Knowledge one?

Check the recon first. `knowledgebase/index.md` already present means the wiki exists; skip the
bootstrap and offer only the wiring rows below.

| Option | Installs | When |
|---|---|---|
| **Bootstrap a project wiki** | `knowledgebase/` with `index.md`, `log.md`, `wiki/`, `raw/` | Repo has domain knowledge that is not derivable from the code |
| **Register only** | Registry line pointing at an existing wiki | The wiki exists but is not in the registry |
| **General Knowledge only** | Nothing | Small repo, or the knowledge is cross-cutting rather than project-specific |

**Do not create the wiki structure yourself.** Bootstrapping, page layout, `index.md` shape and the
global registry line all belong to `write-wiki`. Invoke it with its bootstrap operation and let it
own those files. This skill's job is the wiring around it.

The wiring, each its own yes:

| Item | Mechanism | Effect |
|---|---|---|
| Registry line in `~/.claude/CLAUDE.md` under `## Wikis` | write-wiki | The always-loaded index learns this wiki exists |
| `raw/` guard: `protect-paths.py` with `existing_only=True` | `PreToolUse` hook | `raw/` sources become genuinely immutable, not just conventionally |
| Index injection at session start | `SessionStart` hook | The wiki index loads without the user asking |
| `read-wiki` pointer | CLAUDE.md line, via onboard-repo | Tells Claude to check the wiki before exploring blind |

Two checks before installing any of these:

- **A user-level `SessionStart` hook may already inject wiki indexes.** If `~/.claude/settings.json`
  has one, do not install a project copy. Report it as covered.
- **The `raw/` guard must block edits to existing files while still allowing new ones to be
  created** (`existing_only=True` in `protect-paths.py`). That distinction is what lets ingest write a new dated source while keeping the
  archive immutable. Copy the posture from the knowledgebase repo's own hook rather than writing a
  blunter one.

If the repo has no accumulated knowledge yet, say so and recommend **General Knowledge only**. An
empty wiki is a maintenance burden that returns nothing, and the registry line makes it look
populated when it is not.

---

## Closing the interview

Before proposing, read back the mapping: each answer, the item it justifies, and the mechanism
chosen. Anything you cannot trace to an answer does not get proposed. If a section produced no
answer, say which one and what that means for the scaffold.
