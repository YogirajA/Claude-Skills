---
name: smells
description: Review code for the twelve Fowler code smells (Mysterious Name, Duplicated Code, Feature Envy, Data Clumps, Primitive Obsession, Repeated Switches, Shotgun Surgery, Divergent Change, Speculative Generality, Message Chains, Middle Man, Refused Bequest) and name each one Fowler-style with a concrete fix. Defaults to reviewing the current git diff; accepts an optional file or path argument to review specific files instead. Use whenever the user asks to "check for code smells", "smell check", "any smells here", "review for refactoring", "what should I refactor", "is this well structured", or runs /smells, and as a refactoring lens after /code-review. This is about design and structure quality (naming, duplication, coupling, over-abstraction), NOT correctness bugs; use /code-review for bugs.
---

# Smells

Review changed code for Martin Fowler's code smells (from _Refactoring_, ch. 3) and report each one by name with a concrete fix. The point is not to find bugs. It is to catch structural and design problems that make code harder to change: bad names, duplication, misplaced logic, over-abstraction, leaky coupling.

## Why name the smell

These smells are deep in the model's priors because _Refactoring_ is old and heavily cited. Naming the smell out loud ("this is Feature Envy") is what makes the finding land: it pulls in the well-known fix, it gives the user a shared vocabulary to agree or push back with, and it keeps the review honest by forcing each finding to fit a recognized pattern rather than being a vague "this feels off". So always report a finding as its named smell, not as a freeform observation.

## Scope: what to review

Figure out the scope from the argument, then get the code to review.

1. **No argument (default): the current git diff.** Run `git diff HEAD` to get all uncommitted work (staged and unstaged) against the last commit. This is the "check what I am about to commit" case.
   - If that diff is empty, the working tree is clean. Offer the obvious next options rather than guessing: review the last commit (`git diff HEAD~1 HEAD`), or ask for a file/path or a git ref.
   - If `git` fails because this is not a repository, say so plainly and ask for a file or path to review instead. Do not fabricate a scope.
2. **A path argument (a file or directory that exists): review that code as it stands now.** When the user names a file or folder, they usually mean "look at this code", not "look at its recent diff". Read the current content of the file(s) and review the whole thing. For a directory, review the source files under it (skip vendored, generated, and dependency dirs).
3. **A git ref argument (resolves via `git rev-parse` but is not a path, e.g. `main`, `develop`, `HEAD~3`, a SHA): diff against it.** Run `git diff <ref>...HEAD` (three-dot, so the comparison is against the merge base) and review that.

Only read what the scope calls for. Do not go wandering the rest of the codebase; a smell has to be visible in the code under review to be reported.

## The twelve smells

Each entry is _what it is_ then _how to fix_. Match each against the code in scope.

- **Mysterious Name**: a function, variable, or type whose name does not reveal what it does or holds. Fix: rename it; if no honest name comes to mind, the design underneath is probably murky and worth a second look.
- **Duplicated Code**: the same logic shape appears in more than one place in the scope. Fix: extract the shared shape and call it from both sites.
- **Feature Envy**: a method that reaches into another object's data more than its own. Fix: move the method onto the data it envies.
- **Data Clumps**: the same few fields or parameters keep travelling together (a type wanting to be born). Fix: bundle them into one type and pass that.
- **Primitive Obsession**: a primitive or string standing in for a domain concept that deserves its own type. Fix: give the concept its own small type.
- **Repeated Switches**: the same `switch` or `if`-cascade on the same type recurs across the scope. Fix: replace with polymorphism, or one map that both sites share.
- **Shotgun Surgery**: one logical change forces scattered edits across many files. Fix: gather what changes together into one module.
- **Divergent Change**: one file or module gets edited for several unrelated reasons. Fix: split it so each module changes for one reason.
- **Speculative Generality**: abstraction, parameters, or hooks added for needs the code does not actually have yet. Fix: delete it; inline back until a real need shows up.
- **Message Chains**: long `a.b().c().d()` navigation the caller should not depend on. Fix: hide the walk behind one method on the first object.
- **Middle Man**: a class or function that mostly just delegates onward. Fix: cut it and call the real target directly.
- **Refused Bequest**: a subclass or implementer that ignores or overrides most of what it inherits. Fix: drop the inheritance and use composition.

## Two rules that keep this honest

1. **The repo overrides.** If the repo documents a standard (a `CODING_STANDARDS.md`, `CONTRIBUTING.md`, conventions obvious from the surrounding code) that endorses something a smell would flag, suppress the smell. The team's documented choice wins over the generic heuristic.
2. **Every smell is a judgement call.** Report each as a labelled heuristic ("possible Feature Envy"), never as a hard violation. And skip anything tooling already enforces: naming lint, formatting, unused-variable warnings, and so on are the linter's job, not yours.

Do not invent smells to fill a quota. If the code in scope is clean, the right answer is "no smells worth flagging", and saying that plainly is more useful than a stretch.

**When the scope is prose, not code.** If the target is documentation, a markdown file, config, or otherwise not real program code (no functions, types, objects, or control flow), most of these smells are structural code patterns with nothing to bite on. Say that in one line, note the few that could plausibly apply (usually only Duplicated Code and Mysterious Name), and move on. Do not force the object-oriented smells (Feature Envy, Data Clumps, Refused Bequest, and the like) onto text that has no objects.

## How to report

Group findings by file so they are easy to act on, in scope order. For each finding give: the smell name, the location (`file:line` or the hunk), one line on what is smelly there, and the fix. Keep it scannable, this is a checklist to act on, not an essay.

Use this shape:

```
## Smells: <scope, e.g. "git diff HEAD" or "src/auth/session.ts">

### <file path>
- **<Smell name>** (`file:line`): <what is smelly here>. Fix: <how>.
- **<Smell name>** (`file:line`): <what is smelly here>. Fix: <how>.

### <next file path>
- ...

**Summary:** <N> findings across <M> files. Worst: <the one most worth fixing, and why>. All are judgement calls, you decide which are worth acting on.
```

If nothing is worth flagging, skip the per-file breakdown and just say the scope is clean, with a one-line note on what you looked at.

Report only. Do not edit the code unless the user asks you to apply a fix.
