---
name: wiki
description: >-
  Alias for write-wiki. Kept for backward compatibility: /wiki triggers the same behavior as
  /write-wiki. Use write-wiki for adding, ingesting, or updating knowledge. Use read-wiki for
  querying and getting context before doing work.
disable-model-invocation: true
---

# LLM Wiki: a knowledge base the model maintains

This skill turns a folder of markdown into a knowledge base that **compounds** instead of being
re-derived on every question. The core idea (Karpathy's `llm-wiki.md`): rather than retrieving raw
chunks at query time like RAG, you read each source **once**, integrate it into interlinked wiki pages,
and keep those pages current. The cross-references are already drawn; the synthesis already reflects
everything read. The user curates and asks questions; **you do the bookkeeping** (summarizing,
cross-referencing, filing) that humans abandon.

The full reasoning and primary sources live in `knowledgebase/karpathy-llm-wiki-research.html`. Read it
if you need the "why."

## Where it lives

Default root: **`C:\code\knowledgebase\`** (if the user points at a different folder, use that instead).

```
knowledgebase/
  CLAUDE.md     vault config: top-level sections + any local conventions
  index.md      READ THIS FIRST. Catalog of every wiki page, grouped by type, one line each.
  log.md        Append-only timeline. Entries prefixed "## [YYYY-MM-DD] op | Title" so they grep.
  raw/          Immutable sources. You read these, never edit them. The source of truth.
  wiki/         LLM-owned pages: entities, concepts, summaries, comparisons. You write these.
```

## Operating principles (decided with the user, honor them)

- **Lazy, not eager.** Never boil the ocean. Do not mass-summarize folders the user hasn't asked about.
  Grow the wiki where the user actually works and what they actually feed it.
- **Auto-write, review via git.** Make your edits directly. Do not ask permission for each page. The
  user's safety net is the `git diff`, not an approval prompt. (Do confirm before deleting or rewriting
  a page wholesale, and before destructive restructuring.)
- **The user curates; you maintain.** They choose sources and ask questions. You summarize, file,
  cross-link, and keep things consistent. Rarely make the user write a wiki page themselves.
- **Cheap index, lazy drill-down.** `index.md` stays small (one line per page). It is how a fresh
  session orients in seconds without re-reading everything. Read it first, then open only the few pages
  a task needs.
- **Plain markdown, Obsidian-compatible.** Use `[[Wikilinks]]` between pages. No vector DB, no special
  infrastructure. This works well to ~hundreds of pages; past that, suggest a search tool (see Scaling).

## The three operations

The user's intent maps to one of three operations. Infer it; you rarely need to ask.

### ingest: a new source arrives

Triggered by "add this", "ingest", "file this", "remember this source", dropping a link/file, or
pasting content to save.

1. **Get the source into `raw/`.** If it is a URL, fetch it (use WebFetch, or the `watch` skill for
   YouTube). Save the cleaned text as `raw/<slug>.md` with a small header (title, author, url, date,
   how captured). Raw sources are immutable; never edit them after saving.
2. **Read it and surface takeaways.** Briefly tell the user the key points and which existing pages it
   touches. This is where their curation happens. Keep it short.
3. **Write a source summary page** in `wiki/` (`wiki/<slug>.md`): what it is, key claims, notable quotes
   with locations, and `[[links]]` to the entities/concepts it mentions.
4. **Update the entity and concept pages it touches.** A single source typically updates **10-15
   pages**. Create pages for important entities/concepts that don't have one yet. Strengthen, revise, or
   flag-contradict existing claims rather than just appending. This integration step is the whole point.
5. **Update `index.md`** with new/changed pages (one line each, under the right section).
6. **Append to `log.md`**: `## [YYYY-MM-DD] ingest | <Source title>` plus a one-line note of what changed.

Default to ingesting **one source at a time** with the user in the loop. Batch only if they ask.

### query: answer from accumulated knowledge

Triggered by questions the wiki could answer: "what do I know about X", "have I covered Y", "what
connects A and B", "what patterns / missed opportunities do you see", "summarize my thinking on Z".

1. **Read `index.md` first** to find candidate pages. Drill into the few that matter; follow `[[links]]`.
2. Synthesize an answer **with citations** to the pages (and through them, the raw sources) you used.
3. **File good answers back.** If the answer is a genuinely useful new synthesis, comparison, or
   connection, offer to save it as a new `wiki/` page so the exploration compounds instead of vanishing
   into chat. Then add it to `index.md` and `log.md`.

### lint: health-check the wiki

Triggered by "lint", "clean up", "audit my wiki", "what's stale / missing / orphaned", or run it
proactively when the wiki has grown a lot since the last lint (check `log.md`).

Scan for, and report (fix the safe ones, propose the rest):
- **Contradictions** between pages.
- **Stale claims** newer sources have superseded.
- **Orphan pages** with no inbound `[[links]]`.
- **Missing pages**: concepts mentioned often but lacking their own page.
- **Missing cross-references**: pages that should link but don't.
- **Data gaps** worth a web search to fill.

End a lint by appending to `log.md` and suggesting the next sources or questions worth pursuing.

## Page and file conventions

- **Page = one entity or concept.** Filenames are kebab-case slugs. Page title is an `# H1`.
- **Wikilinks** `[[Page Title]]` for every cross-reference, so Obsidian's graph view works.
- **Cite sources** inside pages: link to the `raw/` file (and a location: timestamp, section, page).
- **index.md format**: grouped by type, one line per page:
  ```
  ## Concepts
  - [[LLM Wiki]]: knowledge base the model maintains; compounds vs RAG. (src: 2)
  ## Sources
  - [[Karpathy llm-wiki gist]]: the canonical idea file. raw/karpathy-llm-wiki.gist.md
  ```
- **log.md format**: append-only, newest at bottom, parseable prefix:
  ```
  ## [2026-06-26] ingest | Karpathy llm-wiki gist
  Created [[LLM Wiki]], [[Andrej Karpathy]]; updated index. 4 pages touched.
  ```

## First run / bootstrap

If `index.md`, `log.md`, or `CLAUDE.md` are missing, create them before the first operation. Seed
`CLAUDE.md` with the top-level sections the user wants (ask once if unclear; reasonable defaults:
Concepts, Entities, Sources, Topics). Do not auto-ingest everything already in `raw/`; mention what's
there and let the user pick what to ingest first. Lazy, always.

## Scaling

The `index.md`-first approach works well to roughly a few hundred pages. If the index gets unwieldy
(Karpathy's rule of thumb: ~200+ entries), add a `wiki/_meta/topic-map.md` that groups pages by theme,
and consider a local markdown search tool such as `qmd` (https://github.com/tobi/qmd) so you can shell
out to search instead of scanning the index. Suggest this to the user; don't build it preemptively.

## Optional: make reading automatic

The wiki only helps if it gets read. Three ways make a fresh session pick it up without the
user typing `/wiki`: (1) a one-line pointer in the always-loaded global `~/.claude/CLAUDE.md` (its `## Wikis`
registry) saying the wiki exists at `knowledgebase/index.md` and should be consulted when relevant; (2) the `knowledgebase/CLAUDE.md`
file, which Claude reads automatically when working in that folder; (3) a global `SessionStart` hook
(`~/.claude/hooks/wiki-context.py`) that injects the project and GK index maps into context at session start,
so they are seen before any search. These are already wired up by this skill's bootstrap and the global hook. Obsidian is purely an optional human viewer over the same markdown; never required.
