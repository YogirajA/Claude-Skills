---
name: onboard-light
description: >-
  Onboard Claude onto a repo without touching .claude/: the full onboard-repo flow (recon, mutual
  interrogation, verified feedback loop, CLAUDE.md block, wiki, cold eval) with the harness phase
  (4b) skipped by standing instruction. Use when the user says "onboard light", "onboard without
  the harness", "onboard but no hooks/settings/rules", or wants knowledge-only onboarding on a
  repo where enforcement config is unwanted (a client repo, a restricted repo, or one that is not
  theirs to configure). For the full flow including the .claude/ harness use onboard-repo; to add
  only the harness to an already-onboarded repo, run onboard-repo and re-run phase 4b alone.
---

# onboard-light

A standing pre-answer over onboard-repo, not a second process. The entire method lives in
`~/.claude/skills/onboard-repo/SKILL.md`; this wrapper changes exactly one decision, so the two
can never drift apart.

## What to do

1. **Invoke the `onboard-repo` skill and follow it in full**: same phases, same checkpoint
   protocol, same references.
2. **Treat the Phase 4b checkpoint as already answered: "later".** Do not run the harness
   interview, do not write anything under `.claude/`, and do not ask; the choice was made by
   invoking this skill.
3. **Record the skip** in `knowledgebase/wiki/repo-onboarding.md` as "harness unbuilt, skipped via
   onboard-light", so a future run sees the gap. The existing edge case ("wiki exists, no
   `.claude/HARNESS.md`: recommend Phase 4b alone") then offers the harness whenever the user wants
   it, with Phases 0 to 3 read from the wiki instead of re-derived.
4. Everything else is unchanged: every checkpoint still stops and waits, Phase 3 still executes
   commands only with approval, Phase 5 still runs cold.

At the close, say in one line that the harness can be added any time by running `onboard-repo` and
choosing to re-run phase 4b alone. Do not sell it harder than that.

## Boundary

If, mid-run, the user asks for hooks, settings, rules, or anything under `.claude/`, that is no
longer light: say so, and continue under plain onboard-repo rules (run Phase 4b normally at its
checkpoint) rather than improvising harness writes inside the light flow.
