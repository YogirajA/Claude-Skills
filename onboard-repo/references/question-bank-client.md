# Phase 1 question bank: a cold repo

Neither of you may have ground truth. Bias toward questions whose answers are checkable in the code
within a minute, so the user can grade without domain knowledge.

## Orientation

- What does this system do, in one paragraph, and what evidence supports that?
- Who are its callers, and what does it call? Show the seams.
- What is the deployment target, and how do you know?

## Verifiable claims

Each of these must be answered with a file and line the user can open.

- Where does execution begin?
- Where is authentication enforced, and is it enforced in one place or many?
- What is the data model, and where is it defined?
- Where are the external dependencies (network, disk, queue, third-party APIs)?

## Risk surface

- What here has no test coverage but looks important?
- What looks copy-pasted, and does it drift between copies?
- What is the oldest code still on a hot path?

## Honest unknowns

- What are the three things you are least sure about, and what would resolve each?

Ask that last one every time on a cold repo. It seeds Phase 2 directly, and it is the fastest route
to a well-formed unknowns ledger.

## Reminder

Offer these as a menu. The user asks; you answer. Do not run through them yourself.
