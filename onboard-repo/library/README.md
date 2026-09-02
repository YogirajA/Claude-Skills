# The library

An opinionated menu, not a set of defaults. Nothing here is installed without an explicit yes in the
interview, and nothing is installed without a justification line in `.claude/HARNESS.md`.

Every file is a starting point to **adapt**, not to copy verbatim. Each carries an `ADAPT THIS FILE`
note saying what to change. Shipping an unadapted hook is how you get a guard that reports noise on
every edit, which teaches the user to ignore it.

## Contents

| File | Mechanism | Earned by | Cost |
|---|---|---|---|
| `hooks/protect-paths.py` | `PreToolUse`, blocks | Section 3, danger zones | Zero unless it fires |
| `hooks/block-destructive.py` | `PreToolUse`, blocks | Section 3, danger zones | Zero unless it fires |
| `hooks/verify-on-stop.py` | `Stop`, blocks | Section 2, verification | One command run per changed turn |
| `hooks/run-after-edit.py` | `PostToolUse`, reports | Section 2, verification | One command run per edit |
| `test-hooks.py` | Test runner | Always, at Phase 4b verify | None |
| `templates.md` | `HARNESS.md`, settings, rules, skills, agents | Varies by section | Varies |

Install `test-hooks.py` alongside the hooks it checks. A guard nobody has fired is a guard nobody
knows is broken.

## The two postures worth understanding

`protect-paths.py` has an `existing_only` flag per pattern, and the choice matters more than it
looks:

- **`existing_only=True`** is the *immutable archive* posture. Edits to files that already exist are
  blocked, new files are allowed. This is what lets an ingest write a new dated source while the
  archive stays unrewritable. The knowledgebase repo's `raw/` uses exactly this.
- **`existing_only=False`** is the *never touch* posture, for secrets and generated code, where the
  file existing or not is irrelevant.

Reaching for the second where the first was meant is the common mistake: it blocks legitimate
creation and the user disables the hook rather than fixing the flag.

## Where the opinions come from

The point of view baked into these files, and where each claim is checkable:

| Opinion | Source |
|---|---|
| Hooks beat prompting for anything that must hold every time | `code.claude.com/docs/en/features-overview` |
| Verification, not prompting, is what lets a run go long | Boris Cherny, YC talk; `docs/en/best-practices` |
| Delete config every six months, re-add only on repeated failure | Boris Cherny, YC talk |
| Delete everything, watch the bare agent, add back what you miss | Matt Pocock, David Ondrej interview |
| Every skill leaks its description into every session | Matt Pocock; Daisy Hollman, NDC |
| Scope rules with `paths:` or they compete with the build commands | `docs/en/memory`; Anthropic blog, *Steering Claude Code* |
| Cut any line the model already honours without it | `docs/en/best-practices` |
| A reviewer told to find gaps will invent them | `docs/en/best-practices` |

The first four all argue **against** pre-populating config. That is not a contradiction with this
library existing; it is the reason the interview and the manifest are mandatory. Those sources are
describing config that arrives unasked and cannot be audited later. Answer both and the objection is
answered with it.

## Adding to the library

A candidate earns a place only if it is **repo-independent in mechanism and repo-specific in
configuration**, the way `protect-paths.py` is. Anything whose content is a guess about what a repo
needs belongs in the interview as a question, not here as a file.
