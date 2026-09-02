# Templates

Fill these from interview answers. A placeholder you cannot fill from an answer means the item was
not earned; drop it rather than inventing a justification.

---

## `.claude/HARNESS.md` (the manifest)

The point of the whole skill. Without this, an opinionated scaffold becomes the unreviewable cruft
that Cherny, Pocock and the Anthropic docs all warn about. With it, the six-month delete is a
checklist rather than a judgement call.

```markdown
# Harness manifest

What is installed in `.claude/`, why, and when to check whether it still earns its place.
Written by `onboard-repo` Phase 4b on <YYYY-MM-DD>. **Next review: <YYYY-MM-DD, +6 months>.**

## How to review

For each entry below, in order:

1. Read the justification. Is it still true?
2. Remove the item and work normally for a few sessions.
3. Put it back only if you see the same failure it was installed to prevent.

Removal is the default answer. Cherny's rule is that you cannot predict which instruction the
model needs, so you delete and let repeated failure tell you. An entry nobody can justify is
costing context or maintenance for nothing.

## Entries

| Item | Mechanism | Installed | Justification (from the interview) | Remove when |
|---|---|---|---|---|
| `hooks/protect-paths.py` | PreToolUse | <date> | "<verbatim answer>" | Secrets move out of the repo |
| `rules/api.md` | Rule, `paths: src/api/**` | <date> | "<verbatim answer>" | Claude stops making this mistake |

## Not installed, and why

Recording the noes matters as much as the yeses: it stops the next run from re-proposing
something already rejected.

| Considered | Declined because |
|---|---|
| Stop-hook verification gate | Test suite takes 6 minutes, too slow to run every turn |

## Known gaps

Things nothing in this harness covers, so they stay visible instead of being quietly forgotten.

- <gap, e.g. "no screenshot path for UI changes">
```

---

## `.claude/settings.json` snippets

**Always merge into the existing file.** Read it, add your keys, write it back. Never clobber keys
you did not add.

Hooks, referencing scripts by `$CLAUDE_PROJECT_DIR` so they work from any working directory:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Write|Edit|MultiEdit",
        "hooks": [
          { "type": "command", "command": "python \"$CLAUDE_PROJECT_DIR/.claude/hooks/protect-paths.py\"" }
        ]
      },
      {
        "matcher": "Bash",
        "hooks": [
          { "type": "command", "command": "python \"$CLAUDE_PROJECT_DIR/.claude/hooks/block-destructive.py\"" }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Write|Edit|MultiEdit",
        "hooks": [
          { "type": "command", "command": "python \"$CLAUDE_PROJECT_DIR/.claude/hooks/run-after-edit.py\"", "timeout": 90 }
        ]
      }
    ],
    "Stop": [
      {
        "hooks": [
          { "type": "command", "command": "python \"$CLAUDE_PROJECT_DIR/.claude/hooks/verify-on-stop.py\"", "timeout": 180, "statusMessage": "Verifying..." }
        ]
      }
    ]
  }
}
```

Permissions. **Every `allow` entry must name a command that was actually executed in Phase 3.**

```json
{
  "permissions": {
    "allow": [
      "Bash(npm run lint)",
      "Bash(npm test)",
      "Bash(git status)",
      "Bash(git diff:*)"
    ],
    "ask": [
      "Bash(git push:*)"
    ],
    "deny": [
      "Bash(npm publish:*)",
      "Bash(git push --force:*)",
      "Read(./.env)",
      "Read(./secrets/**)"
    ]
  }
}
```

`ask` is for irreversible-but-workflow-normal commands (push-as-deploy, publish on request):
prompted interactively, stopped in unattended runs. Ask rules are prefix matches, so a
command-rewriting hook needs the rewritten form listed too (`Bash(rtk git push:*)` alongside the
plain one, for instance).

Two facts that change what is worth writing here:

- `deny` and `ask` apply immediately, but `allow` **only applies after each teammate trusts the
  folder.** For a shared repo, a deny is reliable in a way an allow is not.
- `permissions.defaultMode` values `auto` and `bypassPermissions` are **ignored** in project and
  local settings. They only work from user or managed settings. Do not write them here.

Set the hook script timeout above the command's real runtime, or the hook is cancelled and its
output discarded, which silently looks like a pass.

---

## `.claude/rules/<topic>.md`

Scope with `paths:` unless the user confirmed it is genuinely global. An unscoped rule loads every
session at the same priority as `.claude/CLAUDE.md`, so it competes with the build commands.

```markdown
---
paths:
  - "src/api/**/*.ts"
---

# API conventions

- <the specific, verifiable correction from the interview>
- <one per line, imperative, concrete enough to check>

<!-- Installed <date> because: "<verbatim interview answer>". See .claude/HARNESS.md -->
```

The HTML comment is stripped before the content enters context, so the provenance costs nothing at
runtime and is still there when someone opens the file.

Write rules the way the docs say to write instructions: "Use 2-space indentation", not "format code
properly". If it cannot be checked, it cannot be followed reliably.

---

## `.claude/skills/<name>/SKILL.md`

Only if section 5 produced a procedure the user actually repeats.

```markdown
---
name: <kebab-case>
description: <when to use this, in the words someone would say to trigger it>
disable-model-invocation: true
---

# <Name>

<The procedure, numbered, as concrete as the user described it.>
```

Set `disable-model-invocation: true` for anything with side effects. It keeps the description out of
context entirely and guarantees only the user fires it.

---

## `.claude/agents/<name>.md`

For read-heavy work that would otherwise flood the main conversation.

```markdown
---
name: <kebab-case>
description: <when to delegate to this>
tools: Read, Grep, Glob, Bash
model: opus
---

<Role, what to look for, and what to report. Tell it to report only what affects
correctness or the stated requirements: a reviewer asked to find gaps will invent
them, which leads to over-engineering.>
```

---

## `.gitignore`

```gitignore
.claude/settings.local.json
.claude/.verify-state
```

Claude Code adds `settings.local.json` to your global git excludes when it creates the file itself,
but not when the file is created by hand. Add it explicitly.
