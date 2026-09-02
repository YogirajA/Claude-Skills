# Which mechanism, and why

Decision criteria for the six places an instruction can live. Sourced from Anthropic's docs, with
the provenance kept so the claims stay checkable when the docs move.

## The one-question test

> **If Claude decided to ignore this, would that be acceptable?**

If no, it is a hook or a permission rule. Everything else is advisory.

Anthropic states this directly: "An instruction like 'never edit `.env`' in CLAUDE.md or a skill is a
request, not a guarantee. A `PreToolUse` hook that blocks the edit is enforcement. If a rule must
hold every time, make it a hook rather than a prompt instruction."
(`code.claude.com/docs/en/features-overview`)

And on memory generally: "Claude treats them as context, not enforced configuration. To block an
action regardless of what Claude decides, use a PreToolUse hook instead."
(`code.claude.com/docs/en/memory`)

## Full comparison

| | Loads | Context cost | Deterministic | Best for |
|---|---|---|---|---|
| **Hook** | On its event | Zero unless it returns output | **Yes** | Guardrails, linting, gates, injected context |
| **permissions deny/ask/allow** | Structural | Zero | **Yes** | Pattern-matchable command and path bans |
| **Path-scoped rule** | When a matching file is read | Only on match | No | Per-language or per-directory conventions |
| **Unscoped rule** | Every session | Every request | No | Cross-cutting conventions, same priority as `.claude/CLAUDE.md` |
| **CLAUDE.md** | Every session | Every request | No | Build commands, layout, always-on facts |
| **Skill** | On invocation or relevance | Description every session, body on use | No | Procedures, reference material |

## Rules of thumb worth keeping

**CLAUDE.md is for facts, skills are for procedures.** "Procedures belong in skills. CLAUDE.md is
for facts Claude should hold all the time: build commands, monorepo layout, team conventions."
(Anthropic blog, *Steering Claude Code*)

**Scope aggressively.** "If a rule only applies to `src/api/**`, scoping it with `paths:` keeps it
out of context during unrelated work."

**`ask` is the posture for irreversible-but-workflow-normal commands.** Where a command is part
of the normal workflow but its consequences leave the repo (push-as-deploy on a Railway-connected
repo, publish, migrate), `deny` breaks the workflow and `allow` lets an unattended run fire it
silently. `permissions.ask` is the middle posture: available interactively, prompted every time,
stopped cold when nobody is watching. Found live on a Railway push-to-deploy repo, where `git push` IS the deploy.
One caveat: permission rules are prefix matches on the command string, unlike hook regexes, so a
command-rewriting hook (an `rtk` proxy, for instance) needs the rewritten form listed too.

**Cut what the model already does.** "For each line, ask: *Would removing this cause Claude to make
mistakes?* If not, cut it. Bloated CLAUDE.md files cause Claude to ignore your actual instructions."
(`code.claude.com/docs/en/best-practices`)

**Size targets.** Docs say under 200 lines per CLAUDE.md. `onboard-repo` imposes a harder cap of 40
for the block it writes, and overflow moves to the wiki rather than being trimmed by judgment. For
reference, Matt Pocock's own repo CLAUDE.md is 25 lines.

**Every skill leaks.** Descriptions load every session whether or not the skill is used. Daisy
Hollman's scaling test is the right one: does this still work in a repo with a thousand of them? Set
`disable-model-invocation: true` to remove a skill's description from context until invoked.

## Where each file goes

| File | Scope | Commit it? |
|---|---|---|
| `.claude/settings.json` | Everyone on the project | Yes |
| `.claude/settings.local.json` | You, this project | **No.** Gitignore it |
| `.claude/rules/*.md` | Everyone on the project | Yes |
| `.claude/hooks/*` | Everyone on the project | Yes |
| `~/.claude/settings.json` | You, every project | N/A |
| `~/.claude/rules/*.md` | You, every project. Loads *before* project rules | N/A |

Precedence, highest first: managed, command line, project local, shared project, user.

Two traps worth knowing before writing a shared `settings.json`:

- `permissions.allow`, `permissions.additionalDirectories` and most `env` values **apply only after
  each teammate trusts the folder.** `deny` and `ask` rules apply immediately. So a deny is reliable
  for a team in a way an allow is not.
- `permissions.defaultMode` values `auto` and `bypassPermissions` **do not take effect** from project
  or local settings. They must be set in user or managed settings.

## Hook events worth knowing

The full list is long; these are the ones this library uses.

| Event | Fires | Can block? |
|---|---|---|
| `PreToolUse` | Before a tool call | **Yes**, exit 2 |
| `PostToolUse` | After a tool call succeeds | No, output ignored |
| `Stop` | When Claude finishes responding | **Yes**, exit 2, overridden after 8 consecutive blocks |
| `SessionStart` | Session begins or resumes | No. Use for injecting context |
| `UserPromptSubmit` | Prompt submitted, before processing | **Yes** |
| `InstructionsLoaded` | A CLAUDE.md or rule file loads | No. Useful for debugging what loaded |

**Exit codes.** 0 is success, and stdout starting with `{` is parsed as JSON. 2 blocks on events that
support blocking, and stderr becomes the message Claude sees. Any other code is a non-blocking error.
On exit 0, stderr goes only to the debug log and Claude never sees it.

**Fail open.** A hook that raises on malformed input blocks legitimate work with no useful message.
Every hook in this library exits 0 on any parse failure. Test that path explicitly.
