---
name: toolbox
description: "Index of the hand-typed skills: what each is for and when to reach for it."
disable-model-invocation: true
---

# Toolbox

Yogi typed `/toolbox` because he cannot remember which hand-typed skill fits.
Read the list, name the one or two that actually fit, and tell him what to type.

You cannot run them. Every skill below is user-invoked, so it has no description
and nothing reaches it but Yogi typing its name. Naming the right one is the
whole deliverable.

## Teach and present

- `/conference-talk-deck`: a new talk. Interviews him, then generates a
  self-contained offline HTML deck with author mode.
- `/field-guide-builder`: one deep teaching page on a technical topic, cited to
  primary sources, with worked examples and do/avoid practice.
- `/sdd-workshop-walkthrough`: an animated click-through workshop page in the
  Athena house style (specworkshop.html, repo.html).
- `/qa-deck`: a .pptx about to go out. Renders every slide, hunts visual defects
  and fabricated facts.

## Plan before building

- `/spec-interview`: he knows the rough shape and wants it pinned down fast. One
  question at a time, ends in a spec he approves.
- `/wayfinder`: bigger than one session can hold. Decision tickets on the issue
  tracker, resolved one at a time until the route is clear.

## Cut what is not needed

- `/ponytail-review`: the current diff. What to delete.
- `/ponytail-audit`: the whole repo. Ranked, biggest cut first.
- `/smells`: Fowler's twelve, on the diff. Design and structure, not correctness.

## Knowledge and career

- `/wiki`: add, ingest, update, or lint a knowledge base. Alias for write-wiki,
  which also fires on its own.
- `/personal-skill`: a company plus a job posting, out to a 2-page .docx.

## Meta

- `/writing-great-skills`: before pruning or splitting a skill. The invocation
  cost model, the information hierarchy, and the failure taxonomy.

## When nothing fits

Say so plainly. The rest of the setup is model-invoked and fires without being
asked, so anything covered there is already handled. Forcing a match from this
list wastes a run and buries the better answer.

## Keeping it true

When a skill flips to user-invoked, add it here. This list is its only index: a
user-invoked skill missing from it is invisible, reachable only by someone who
happens to remember the name.
