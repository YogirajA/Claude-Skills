---
name: goal-creator
description: Turns a rough intent into a sharp session goal ready to paste into /goal, under the 4000-character limit. Use when the user wants to set, write, or refine a session goal, mentions /goal, or asks to sharpen what an autonomous session should accomplish. Produces one goal text with a verifiable outcome, scope guard, acceptance criteria with proofs, and explicit authorities (deploy, publish, spend, review policy).
---

# Goal Creator

Turn a rough intent into one goal text that an autonomous session can execute without
guessing and without drifting.

The session that runs this goal reads the goal and nothing else about the intent behind
it. Every ambiguity left in the text becomes a decision the session makes alone, hours
later, with no way to ask. That is what the structure below is defending against.

## Output contract

End the response with the goal in a single fenced block, so it is the last thing on
screen and one copy away from `/goal`. Put the character count on the line immediately
above the block. Nothing after the block.

## Hard limits

- Under 4000 characters (the `/goal` cap). Target 1500 to 2500. Count before returning;
  trim detail, never trim authorities or proofs.
- Decide ambiguities and state the assumption inside the goal. Ask only when a genuine
  fork changes the outcome, and then ask once, with AskUserQuestion, rather than
  interviewing.

## Ground it in what is actually there

A goal built from placeholders (`<branch>`, "the relevant tests", "the deploy script")
is a goal the session fills in wrong. Before writing, find the real values: the current
branch, the test command that actually exists, the real paths, the deploy target.
`git branch --show-current`, an `ls`, or the scripts block in `package.json` costs
seconds and beats a plausible guess, because the session will run exactly what is
written.

Where a value cannot be verified, write it into the goal as a named assumption the
session verifies first, not as an assertion. A wrong command that looks confident is
worse than an instruction to go check.

## Goal anatomy

Seven slots, in this order. Each one closes a specific way sessions go wrong.

1. **Outcome**: one sentence, artifact-shaped. What exists when done that does not exist
   now. "Review done" is activity and can be claimed at any moment; "issues ledgered,
   approved fixes merged and deployed, reports republished" cannot.
2. **Why**: one sentence of purpose. This is what settles scope disputes mid-session,
   when the session hits something the criteria did not anticipate.
3. **Scope guard**: one sentence on what this is NOT. The strongest drift brake in the
   goal, because it is the only slot that can stop work rather than direct it.
4. **Acceptance criteria**: 3 to 7 checkable items, each naming its proof: a command, an
   exit code, an artifact path, or a visible fact on a page. A criterion nobody can check
   is a wish, and the session will grade itself generously against it.
5. **Authorities**: who may pull which trigger. Unstated authority is the most expensive
   gap in a goal, because the session either stalls waiting or acts when it should have
   waited. Cover every gate that applies:
   - deploy, publish, anything outward-facing: "wait for my word" or "auto if X"
   - spend (model calls, paid runs): allowed, capped, or ask first
   - destructive ops (deletes, resets, force-pushes): almost always "ask first"
   - blocked protocol: when a permission wall blocks a step, hand the exact command back
     to the user to run and continue elsewhere; never work around a denial
6. **Method constraints**: only the ones that bind. Timebox anything open-ended. Say
   whether subagents and worktrees are authorized for parallel work. Adversarial subagent
   review is optional: include it only when wanted, and then timebox it and cap the fix
   set ("priority actual issues only, no running in circles"). Default otherwise: fix
   directly, self-review the diff.
7. **Parking**: where out-of-scope findings go (a named ledger file), so they are
   captured without being executed. Without a park, everything found gets fixed.

## Sharpness rules

Each of these is a session that went sideways once.

- Absolute over relative: name batch ids, branches, dates, and file paths explicitly.
  "The latest run" resolves differently at hour six than it did at hour one.
- One goal, one outcome. Two outcomes means two sessions, or an ordered "then".
- Every open-ended activity gets a timebox or an iteration cap, or it expands to fill
  the session.
- The review-findings trap: reviews generate work. Pre-commit the triage rule in the
  goal (the severity bar, and who approves the fix list) or the review becomes the
  session and nothing gets fixed.
- If the session may pause (long runs, a VPN drop, waiting on a human), require a
  progress ledger so a resumed session continues instead of restarting.

## Before returning, verify

Fix and re-check rather than returning a near miss:

- [ ] All seven slots present and non-empty
- [ ] Under 4000 characters, count stated above the block
- [ ] Every acceptance criterion names a command, exit code, path, or visible fact
- [ ] Every applicable gate has an explicit authority
- [ ] At least one timebox or iteration cap on open-ended work
- [ ] Scope guard states what is out of bounds
- [ ] No unresolved placeholder text anywhere in the block

## Example

Rough intent: "review the flows and sme reports coming out of kb, fix what's wrong"

Sharpened goal:

```
Outcome: flows and SME report content reviewed, real defects ledgered and triaged,
approved fixes merged to master and deployed, reports regenerated and republished.

Why: the KB exists so SMEs gain confidence in the system for the P23 comparison;
correctness of what they see is the product.

Not in scope: no new KB functionality, no schema changes, no re-ingestion.

Acceptance criteria:
1. Every finding in REVIEW-ISSUES.md with a ruling (fix / defer / reject) and
   evidence. Proof: the file, committed.
2. Only user-approved fixes implemented. Proof: fix list confirmed before first edit.
3. Both interpreter suites green before any deploy. Proof: pytest exit 0 on
   .venv and .venv312.
4. Deployed pages show the fixes. Proof: named artifact on the published page
   (e.g. the 2.4.3 cross-flow box gone from flow-2.4.3-rendered.html).
5. Reports regenerated from the serving batch and published to the review folder.
   Proof: publish script run, files listed.

Authorities: deploy and publish wait for my word. Model spend for re-runs: ask
first. Destructive ops: ask first. If the permission classifier blocks a command,
hand me the exact command to run with ! and continue on other work.

Method: subagents and worktrees authorized for independent fixes; worktrees branch
from master. Adversarial review: 75 minutes max, then triage with me; priority
actual issues only, no running in circles. Everything else: self-review the diff.

Parking: out-of-scope findings go to REVIEW-ISSUES.md as deferred items, not fixed.
```
