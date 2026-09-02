# Phase 5 eval rubric

## Subagent contract

One `general-purpose` subagent, spawned via the Agent tool with `run_in_background: false`, carrying
no conversation history. It receives all 10 to 12 questions in a single prompt and returns all
answers in one structured reply, so the eval costs one agent call rather than one per question.

**Stated limitation, and say it out loud in the results.** A subagent's file tools cannot be
hard-blocked, so this is not a sandbox. Two mitigations, and they are mitigations, not isolation:

1. **Inline the artifacts** (the CLAUDE.md block and every wiki page) into the prompt, so it has no
   reason to go looking.
2. **Require a citation** naming the wiki page for every answer. Uncited answers are flagged, not
   scored.

## Prompt template

    You are answering questions about a codebase you have never seen.
    Below are the ONLY materials you may use. Do not read any files.

    <artifacts>
    {inlined CLAUDE.md block and all wiki pages}
    </artifacts>

    Answer each question below. For every answer, cite the page it came from as
    [page: <name>]. If the materials do not contain the answer, reply exactly:
    UNANSWERABLE: <what is missing>

    Guessing is worse than UNANSWERABLE. An honest gap is a useful result.

    <questions>
    {the 10 to 12 questions, numbered}
    </questions>

## Scoring

| Outcome | Meaning | Graded by |
|---|---|---|
| **pass** | Correct and cited | User |
| **gap** | Replied UNANSWERABLE. The wiki is incomplete. The honest failure | Mechanical |
| **wrong** | Confident and incorrect. The wiki actively misleads. Worst outcome | User |
| **uncited** | Answered with no citation. Suspect, likely read source | Mechanical |

Present results as a table and ask the user to grade only the answered rows. `gap` and `uncited` are
determined mechanically and need no human judgment.

## Routing

- **gap**: add the missing content to the relevant page, then re-run that question only.
- **wrong**: a bug in the wiki. Jumps the queue. Fix before anything else.
- **gap plus wrong exceeds 30%**: recommend `deeper` on Phases 0 and 2 rather than patching page by
  page. At that rate the problem is coverage, not wording.

## Bar

- A repo the user knows well: **pass at or above 80%**, and **`wrong` = 0**.
- A cold repo: gaps are expected and acceptable, but **`wrong` = 0** still.

A `gap` means the wiki is quiet. A `wrong` means it lies, and a lying wiki is worse than no wiki.
