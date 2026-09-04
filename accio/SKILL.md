---
name: accio
description: "Summon the right skill. A router over this whole collection plus the enabled plugins: say what you are working on, get told what to type."
disable-model-invocation: true
---

# Accio

*Summoning Charm.* You do not remember 62 skills. Name the problem, not the skill.

Fired bare, with nothing attached, ask what is being worked on. Reprinting this map back is a
no-op: the reader is already looking at it. **Name the one or two that fit and say what to type.**

Two markers below:

- **(type it)** the skill is `disable-model-invocation: true`. Nothing reaches it but the user
  typing its name, so naming it is the whole deliverable.
- **(plugin)** it comes from an enabled plugin, not this collection.

> Every route on this page was verified against disk. If you add a skill, add it here; if you
> remove one, remove it here. A router that names something that does not exist is worse than no
> router, because it is confidently wrong. `/skill-comply` on this file measures whether that has
> rotted.

## Arriving somewhere new

- **`/onboard-repo`**: a repo Claude has no context on. Recon, mutual interrogation, a feedback
  loop it actually executes, a capped CLAUDE.md, a project wiki, and an interview-gated `.claude/`
  harness. Runs once per repo.
- **`/onboard-light`**: the same flow with the harness phase pre-answered "skip". For a repo whose
  `.claude/` is not yours to write: a client repo, a restricted one.
- **`/read-wiki`**: before touching anything in a repo that has a wiki. Strictly read-only.
- **`/caveman-explore`**: cold-start orientation when you need file:line answers and want the
  reading kept out of the main context.

## Idea to shipped

The route most work travels.

1. **`/grill-with-docs`** (type it) sharpens the idea by interview and leaves a paper trail in
   `CONTEXT.md` and ADRs. Use it whenever there is a working directory to leave that trail in.
   **`/grill-me`** (type it) is the same interview with no repo under it. Both run **`/grilling`**,
   which you reach directly only when you want the interview with no wrapper.
   - Lighter alternative: **`/spec-interview`** (type it) when the shape is roughly known and you
     just want it pinned down fast, one question at a time.
   - `brainstorming` (plugin, superpowers) covers the same ground from the other direction and
     fires on its own. If it has already run, do not re-interview from scratch.
2. **Question needs a runnable answer?** Detour through **`/prototype`**: throwaway code that
   settles one design question (does this state model feel right, what should this UI look like).
   The prototype is kept as a primary source, not destroyed.
3. **Multi-session build?**
   - **Yes** → **`/to-spec`** (type it), then **`/to-tickets`** (type it) for tracer-bullet tickets
     with blocking edges, then **`/implement`** (type it) per ticket, `/clear`ing between each.
   - **No** → **`/implement`** right here.

**Keep steps 1 to 3 in one unbroken context window.** Do not compact or clear until after
`/to-tickets`, so grilling, spec and tickets all build on the same thinking. Each `/implement`
then starts fresh from its ticket.

**`/setup-matt-pocock-skills`** (type it) is the precondition: run once per repo before the first
flow, to configure the issue tracker and label vocabulary the ticket skills assume.

## Too big to hold in one session

**`/wayfinder`** (type it). When the way to the destination is not visible yet, it charts a map of
**decision tickets** and resolves them one at a time, producing decisions rather than deliverables.
When the fog clears it hands off to `/to-spec`; it does not build. Save it for genuinely foggy
work, never a well-scoped feature.

## Something is broken

- `systematic-debugging` (plugin, superpowers): the first reach. Refuses to theorise before it has
  a tight feedback loop that goes red on this bug.
- **`/surgical-patch`**: once the cause is known, fix at the narrowest responsible layer with a
  regression proof and the surrounding behaviour preserved.
- **`/resolving-merge-conflicts`**: an in-progress merge or rebase, resolved by intent hunk by
  hunk. Never runs `--abort`.

## Bugs and requests piling up

**`/triage`** (type it), for issues **you did not create**: bug reports, incoming requests, raw
arrivals. Tickets that `/to-tickets` produced are already agent-ready, so do not triage them.

## Changing code safely

- **`/safe-refactor`**: restructure while preserving behaviour, verification bracketing every
  structural edit.
- **`/migration`**: reversible, compatibility-safe transitions (schema, data, API, config,
  dependency).
- **`/ponytail`**: forces the laziest solution that works. Reach for it on any coding task where
  over-engineering is the risk. Levels: lite, full, ultra.

## Reviewing

- **`/ponytail-review`** (type it): the current diff, over-engineering only. What to delete.
- **`/ponytail-audit`** (type it): the same lens over the whole repo.
- **`/smells`** (type it): the twelve Fowler smells with concrete fixes.
- **`/code-review`** (plugin) and `requesting-code-review` / `receiving-code-review` (plugin,
  superpowers) for general review of a branch or PR.
- **`/codebase-design`**: not a review, the shared vocabulary (module, interface, depth, seam,
  adapter) for designing a module's shape. `/improve-codebase-architecture` (type it) is the
  survey that finds candidates; this is the bench you design the chosen one on.

## Deciding

- **`/mental-models`**: pressure-test a real decision through named frameworks, ending in a
  recommendation.
- **`/the-llm-council`**: five advisors attack it from different angles, peer-review anonymously,
  a chairman delivers a verdict. Advisory.
- **`/scope-creep-check`**: fires proactively when a request has quietly grown. Names the drift,
  shows the cost, asks proceed / park / drop.
- **`/goal-creator`**: turn rough intent into a `/goal`-ready session goal with a verifiable
  outcome and a scope guard.

## Harness health

The tools that measure the setup rather than the code.

- **`/context-budget`**: what is eating the context window, ranked by tokens reclaimable.
- **`/config-gc`**: garbage-collect `~/.claude` (stale, orphaned, redundant), confirm each
  deletion.
- **`/skill-comply`**: measures whether a skill or rule is actually **obeyed**, by generating
  scenarios at three prompt-strictness levels and classifying the tool traces. Costs real quota;
  start with `--dry-run`.
- **`/primitive-classifier`**: audits a folder and says which Claude Code primitive each piece of
  context actually belongs in.
- **`/loop-design-check`**: before building an agent loop, and for reviewing one you suspect will
  spin, cheat, or run a wrong answer to completion.

## Knowledge

- **`/read-wiki`**: query before doing work. Read-only.
- **`/write-wiki`**: ingest a source, update pages, lint, or bootstrap a new wiki. **`/wiki`**
  (type it) is a backward-compatible alias.
- **`/remember`** (plugin): session handoffs and durable memory across sessions.

## Token cost

- **`/caveman`**: terse output mode (lite / full / ultra). Cuts the expensive side of the meter.
- **`/cavecrew`**: when to delegate to the compressed subagent presets instead of a vanilla
  explore, so subagent results do not land in main context verbatim.
- **`/caveman-compress`**: compress a stored CLAUDE.md or memory file, with a readable backup.
- **`/caveman-help`**: the quick-reference card for the above.

## Prompting

- **`/prompt-fixer`**: cleans a rough prompt into plain English and hands it back to paste and
  edit. No XML, does not execute.
- **`/prompt-optimizer`**: wraps the ask in XML, **tuned to the target Claude model** via a
  per-model reference (Opus 5, Sonnet 5, Fable 5.1), validates with you, then runs it. Its model
  references also say what to **remove** from an inherited prompt, which matters more than what to
  add.

## Teaching, publishing, checking

- **`/explain-yogi-like-he-is-5`**: a Socratic session that teaches rather than summarizes.
- **`/watch`**: a YouTube transcript turned into notes, chapters, quotes, or answers.
- **`/field-guide-builder`** (type it): one deep, source-grounded, single-file HTML teaching page.
- **`/conference-talk-deck`** (type it): interviews you, then generates an offline HTML deck.
- **`/sdd-workshop-walkthrough`** (type it): an animated single-file workshop player.
- **`/qa-deck`**: QA a `.pptx` for visual defects and fabricated claims before it ships.
- **`/excalidraw`**: architecture diagrams as `.excalidraw` files from codebase analysis. PNG/SVG
  export needs the Playwright MCP server connected.
- **`/geo-content`**: content written for both classic SEO and AI answer engines.
- **`/anthropic-doc-validator`**: check claims about Claude Code, the API or the SDKs against the
  official docs, with verbatim quotes. Reach for it before asserting anything version-specific.
- **`/research`**: delegate reading legwork to a background agent; it returns a cited Markdown
  file. Feeds the thinking, does not replace it.

## Building a new skill

1. **`/skill-scout`** first: search local, marketplace, GitHub and web before writing anything.
   The collection has absorbed four upstream repos; the odds of duplicating are real.
2. **`/writing-great-skills`** (type it) for the vocabulary and principles. `writing-skills`
   (plugin, superpowers) covers similar ground.
3. **`/skill-comply`** afterwards, to find out whether the thing you wrote is actually followed.

## Other people, and messages that missed

- **`/to-questionnaire`** (type it): the blocker is in someone else's head. Interviews you about
  the send, then writes them a questionnaire.
- **`/wizard`**: steps only a human can take (provisioning, credentials, a third-party dashboard).
  Generates an interactive bash script so the procedure stops being re-explained every time.
- **`/wait-what`** (type it): that last message did not land. Re-pitches it with the missing
  context, in plain English.
- **`/teach`** (type it): learn a concept over multiple sessions, using the current directory as a
  stateful workspace.

## Phase boundaries

At the boundary between two chunks of work you have five options, and choosing between them is the
fuzziest decision here: **continue**, **`/clear`**, hand off via **`/remember`** (plugin),
**subagent**, or **`/compact`**. Read [PHASE-BOUNDARIES.md](PHASE-BOUNDARIES.md) for the ordered
tree and why continue is the one to rule out first.

## Keeping this true

This page is the only index for the **(type it)** skills. They carry no description into the
model's context, so one missing from here is unreachable by anything but someone remembering its
name. That is not hypothetical: the `toolbox` skill this page replaced held the same job and
silently drifted to missing 11 of the 24 it indexed, because nothing checked it.

So there is a check. Run it after adding, renaming or removing any skill:

```bash
python accio/scripts/check-routes.py
```

It fails on a **dead route** (this page names a skill that does not exist) and on an
**unreachable skill** (a user-only skill this page omits). Fix SKILL.md, never the script.
