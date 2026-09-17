# cavecrew

Decision guide. When to delegate to caveman subagents instead of doing the work inline.

## What it does

Tells main thread when to spawn a caveman-style subagent. Compact return
contracts can reduce repeated prose when results return to main context, but
effect depends on task, agent, and delegation count. This skill publishes no
universal reduction rate.

Three subagents:

| Subagent | Job | Use when |
|----------|-----|----------|
| `cavecrew-investigator` | Locate code (read-only) | "Where is X defined / what calls Y / list uses of Z" |
| `cavecrew-builder` | Surgical edit, 1-2 files | Scope is obvious, ≤2 files. Refuses 3+ file scope. |
| `cavecrew-reviewer` | Diff/file review | One-line findings with severity emoji |

Use vanilla `Explore` or `feature-dev:code-reviewer` when you want prose, architecture commentary, or rationale. Use main thread directly for one-line answers and 3+ file refactors.

This skill is a decision guide, not a slash command. It activates when the conversation mentions delegation.

## How to invoke

Triggers on phrases like "delegate to subagent", "use cavecrew", "spawn investigator", "save context", "compressed agent output".

## Example chaining

Locate → fix → verify (most common):

1. `cavecrew-investigator` returns site list (`path:line`, symbol, note)
2. Main thread picks 1-2 sites, hands paths to `cavecrew-builder`
3. `cavecrew-reviewer` audits the resulting diff

Parallel scout: spawn 2-3 `cavecrew-investigator` calls in one message with different angles (defs, callers, tests). Aggregate in main.

## Model overrides

By default, `cavecrew-reviewer` and `cavecrew-investigator` pin `model: haiku` in their frontmatter; `cavecrew-builder` has no `model:` line (uses the session default). To change a preset's model, edit the `model:` line in `~/.claude/agents/cavecrew-*.md`.

## See also

- [`SKILL.md`](./SKILL.md): full decision matrix and output contracts
- [`agents/cavecrew-investigator.md`](agents/cavecrew-investigator.md)
- [`agents/cavecrew-builder.md`](agents/cavecrew-builder.md)
- [`agents/cavecrew-reviewer.md`](agents/cavecrew-reviewer.md)
- [Caveman README](../README.md): repo overview
