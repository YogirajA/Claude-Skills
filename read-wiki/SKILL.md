---
name: read-wiki
description: >-
  Query the knowledge base before doing work. Use when the user asks "what do we know about X",
  "get context before I update this", "have we seen this pattern", "what connects A and B", or any
  question that accumulated project or cross-project knowledge could answer. Also invoke proactively
  when starting a non-trivial code task in a project that has a wiki: read the relevant pages first
  before touching files. Strictly read-only: never writes to any wiki file. Triggers on /read-wiki
  or phrases like "check the wiki", "get context", "what's in the wiki about", "have we documented".
---

# read-wiki: Query the Knowledge Base

Pure read. No writes. Never create, edit, or append to any wiki file during this skill.

## Step 1: Find all known wikis

Read `~/.claude/CLAUDE.md` and look for the `## Wikis` section.
It lists every wiki with a path to its `index.md` and a one-line description of what's in it.
(A global SessionStart hook may already have injected the project and GK index maps into context at session
start; if they are present, use them rather than re-reading.)

Also check if the current working directory has a `./knowledgebase/index.md`: a project wiki
wired by write-wiki. If it exists and is not already in the registry, use it anyway.

## Step 2: Determine which wikis to read

**Project wiki first.** Match the current working directory against registry entries.
If a project wiki exists for this folder, read it first.

**GK wiki as fallback.** If:
- The question is cross-cutting (architecture patterns, methodology, prior engagement experience), OR
- The project wiki doesn't have a relevant answer,

...also read the General Knowledge `index.md` whose path is given by the Wikis registry in `~/.claude/CLAUDE.md`.

Both wikis can contribute to one answer. Synthesize across them, project content takes priority.

## Step 3: Read and synthesize

1. Read `index.md` of the relevant wiki(s). Do not read every page: scan the index to find candidates.
2. Open only the pages that are relevant to the question. Follow `[[wikilinks]]` if they lead somewhere useful.
3. Synthesize a direct answer with citations: reference the wiki page (and through it, the raw source).

Format: answer first, citations at the end as a compact list. Keep it tight.

## Step 4: Stop

Do not offer to update anything. Do not append to log.md. Do not create new pages.
If the answer would be worth saving, say: "Want me to save this to the wiki? Run /write-wiki."
