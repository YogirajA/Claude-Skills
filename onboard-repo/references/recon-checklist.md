# Recon checklist (Phase 0)

Work these in order. Record what you find and, for anything you cannot determine, add a block to the
unknowns ledger. Ask the user nothing during this phase.

## 1. Entry points

How does this start? Look for `main`, `index`, a server bootstrap, a CLI entry, `if __name__`,
`bin` in package.json, `[[bin]]` in Cargo.toml.

## 2. Shape

Languages and their proportions. Frameworks. Package manifests. Workspace or monorepo markers
(`pnpm-workspace.yaml`, `turbo.json`, `lerna.json`, `go.work`, Cargo workspace). If any workspace
marker is present, stop and make the user scope before going further.

## 3. The import spine

Which 5 to 10 files does most of the codebase depend on? Count inbound imports. These become the
entity pages in Phase 4 and the spine questions in Phase 5.

## 4. Candidate commands

Collect but **do not run** them. Running is Phase 3, and it needs approval first. Sources:
package.json `scripts`, `Makefile`, `justfile`, CI workflow files, `README`, `tox.ini`,
`Cargo.toml`, `pyproject.toml`.

## 5. Git history

Skip with a recorded note if there is no repository.

    git log --format='%ae' | sort | uniq -c | sort -rn | head -10
    git log --since='6 months ago' --name-only --format= | sort | uniq -c | sort -rn | head -20

Who wrote it, what is churning, what is frozen, what the largest recent changes were.

## 6. Conventions

How are errors handled? How is config loaded? How are modules named? Where do tests live and what
do they look like? Prefer showing the pattern over describing it.

## 7. Danger zones

Files high in **both** churn and distinct author count. This is where a function grows fifteen
arguments and nobody remembers why. Note them; Phase 2 may ask about them.

## Unknowns ledger format

One block per unknown. Phase 2 consumes these verbatim and may not ask anything that is not here.

    Question:        <what you could not determine>
    Tried:           <specific files, searches, history you checked>
    Blocked because: <why the code cannot answer this>

If you cannot fill "Tried" with something specific, you did not try. Go back and try.

## Scale rule

Above roughly 2,000 source files, cover the import spine only and **declare that you truncated**.
Silent truncation reads as full coverage, which makes the resulting wiki worse than no wiki.
