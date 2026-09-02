# Phase 1 question bank: a repo the user already knows

The user has ground truth here, so bias toward questions they can grade instantly and where being
wrong is diagnostic. Offer about 10, chosen for what recon actually found. Substitute the bracketed
placeholders with real names from the recon map before offering them.

## Architecture recall

- How does a request get from the entry point to persistence? Name the files in order.
- Which module would I change to alter <the thing recon flagged as the spine>?
- What is the boundary between <module A> and <module B>, and what crosses it?

## History

- Why does <the function recon flagged with the most parameters> have that signature?
- What changed most in the last six months, and what does that suggest is unstable?
- Which files have not been touched in a year? Are they dead, or done?

## Convention inference

- If I add a new <thing this repo has many of>, what files do I touch and in what order?
- How does this codebase handle errors? Show me the pattern, not a description.
- Where does configuration come from, and what wins when two sources disagree?

## Deliberate traps

Include at least two questions where you suspect you may be wrong. A bank that only asks what you
can answer produces a calibration page that says nothing.

- What does <an ambiguously named module> actually do?
- What is <a piece of domain jargon in the code> in business terms?

## Reminder

Offer these as a menu. The user asks; you answer. If you run through them yourself, the phase has
no value, because its purpose is calibrating the user against you.
