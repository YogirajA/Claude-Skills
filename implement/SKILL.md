---
name: implement
description: "Implement a piece of work based on a spec, a set of tickets, or an agent brief on a triaged issue."
disable-model-invocation: true
---

Implement the work described by the user in the spec, tickets, or agent brief.

Use the `superpowers:test-driven-development` skill (plugin) where possible, at pre-agreed seams.

Run typechecking regularly, single test files regularly, and the full test suite once at the end.

Once done, use `/code-review` (the code-review plugin) to review the work.

Commit your work to the current branch.
