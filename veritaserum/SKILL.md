---
name: veritaserum
description: >-
  Use when the user wants to be interviewed into a written spec instead of
  prompting back and forth: when they already know roughly what they want built
  and need it pinned down fast, when they are iterating prompt-by-prompt and
  want to stop, or when they say "interview me", "spec me", "ask me questions
  first", or "help me write the spec". Ends in a spec they approve before any
  building. For a fuzzy idea that still needs 2-3 approaches explored first, use
  superpowers:brainstorming instead. Formerly spec-interview.
disable-model-invocation: true
---

# Veritaserum

*Truth Serum,* the interview that gets the real spec out of you.

## Overview

A spec is you handing your understanding to the agent in a form it can act on.
The agent can compute, but it cannot decide your goal or read your context. So
the fastest route to a good build is not more prompts: it is a short, sharp
interview that pulls the spec out of your head, one question at a time, grades
whether the task is actually thought through, and stops for your approval before
a single line is built.

This is the **fast path**. It assumes you roughly know what you want and just
need it tight.

## When to use, and when not

| Situation | Use |
|---|---|
| You know the rough shape, want a tight spec fast, keep re-prompting instead | **this skill** |
| The idea is fuzzy and needs 2-3 approaches weighed before any design exists | **superpowers:brainstorming** |
| A one-line change with an obvious answer | neither, just do it (see ponytail) |

If mid-interview the answers reveal real design uncertainty (you do not yet know
the approach, or there are competing architectures), **stop and hand off to
superpowers:brainstorming**. Do not turn this into a full design exploration.

## The interview

Ask **one question per message**. Skip any you can already answer from context
or the conversation: never ask what you can infer, it wastes the user's time and
reads as not listening. Prefer concrete, multiple-choice framings where you can.
Aim for the core 5, add up to 3 more when they apply.

**Core five (always):**

1. **Goal, not task.** "What decision or outcome does this drive? If it works
   perfectly, what changes, and how would you know?" Extracts the real goal, the
   one thing the agent can never decide for you.
2. **Done looks like.** "Give me the 2-3 checks you would run to accept this.
   What does good look like, precisely?" Extracts verifiable acceptance criteria,
   set up front, not after.
3. **Out of scope.** "What tempting things are we deliberately NOT doing this
   pass?" Extracts non-goals and keeps the scope one slice wide.
4. **Context and inputs.** "Who or what uses this, on what real data or
   environment? What would I get wrong by assuming?" Extracts the context the
   agent has no signal for.
5. **Hard constraints.** "What is fixed and what must not break: stack,
   dependencies, performance, security, style, deadline?" Extracts the guardrails.

**Add up to three when they apply:**

6. **Prior art.** "Does something like this already exist here to extend or
   match, rather than build fresh?" Reuse before building.
7. **Riskiest unknown.** "What are you least sure about, and where do you want a
   checkpoint before I go further?" Sets the agile review point.
8. **First slice.** "What is the smallest slice that proves the approach?"
   Extracts the MVP cut.

## Before you write: verify the load-bearing calls

Echo back the 3-5 decisions the whole spec rests on and get an explicit yes on
each: "I am about to assume X, Y, Z. Confirm or correct each." This is the step
that catches a confident, wrong spec before it becomes a confident, wrong build.

## Eval: is the task thought through?

Before the spec becomes a plan, grade it. This is the verifier layer: a spec is
thought through only if a builder with zero context could execute it and know
when they are done. Grade the draft with fresh eyes, each row pass or fail.

| # | Check | Fails when |
|---|---|---|
| 1 | Goal is an outcome | it restates the task ("build X") with no decision or change behind it |
| 2 | Acceptance criteria are runnable | they say "looks good" instead of a check you could actually run |
| 3 | Scope has a hard edge | nothing is listed out of scope; the boundary is left implicit |
| 4 | Constraints are exact | "fast", "secure", "modern" instead of verbatim versions, limits, names |
| 5 | A stranger could build it | any load-bearing decision is still deferred or ambiguous |
| 6 | Risk has a checkpoint | the riskiest unknown is unnamed, or has no review point |

Any fail loops back to the interview question that owns it: fix, then re-grade.
Only a clean pass proceeds. Prefer deterministic, checkable criteria over
judgment where you can: an eval you can run beats one you have to feel.

**High-stakes specs (optional second critic):** when a wrong build is expensive,
get a second, independent review, ideally a different model (Codex via the
plugin) or a fresh subagent, prompted to find the holes, unstated assumptions,
unmeasurable criteria, missing edge cases. A critic with a different training set
catches what the author is blind to.

The acceptance criteria locked here become the **build-time eval** later: the
plan and the finished work get checked against the same bar. Set the criteria
once, in the spec, and reuse them.

## Output

1. **Draft** the spec to `docs/superpowers/specs/YYYY-MM-DD-<topic>-spec.md` (the
   same place superpowers writes, so it feeds the same pipeline; a user preference
   for spec location overrides this). Sections: Goal / outcome, Acceptance
   criteria, Scope (in and explicitly out), Context and inputs, Constraints
   (verbatim, exact values), Open risks and checkpoints, First slice.
2. **Eval** the draft against the rubric above. Loop back on any fail.
3. **HARD GATE:** present the spec for approval. Do not write code, scaffold, or
   invoke any build skill until it is written and the user has approved it, no
   matter how simple the task looks.
4. **Hand off:** offer **superpowers:writing-plans** to turn the approved spec
   into an implementation plan.

## Complements, does not replace

- **superpowers:brainstorming**: the heavier sibling for fuzzy ideas. Escalate to
  it if the interview uncovers real design uncertainty; this skill is the fast
  path when the shape is already known. Same spec location, same downstream, so
  the two never fight over the artifact.
- **scope-creep-check**: if an answer balloons the scope, pull that brake rather
  than quietly absorbing the growth into the spec.
- **ponytail**: governs how the build stays minimal once the spec is set. Keep
  the spec YAGNI so the two agree.

## Make it better by using it

These questions are a starting battery, not scripture. The best way to find a
weak question is to run the interview for real, then cut or sharpen whatever
produced a vague answer. Run water through it.
