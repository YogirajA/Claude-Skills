---
name: write-wiki
description: >-
  Add to, update, or health-check a knowledge base wiki. Use when the user wants to ingest a new
  source (article, PDF, URL, meeting notes, runbook, design doc), update existing pages, lint the
  wiki for stale or orphaned content, or save a synthesis back to the wiki. Also the entry point
  for creating a new wiki: if no wiki exists for the current project, write-wiki asks whether to
  create a General Knowledge wiki (C:\code\knowledgebase) or a project-specific one (inside the
  current folder). Triggers on /write-wiki, /wiki, "add this to the wiki", "ingest this", "save
  this to the wiki", "update the wiki", "lint the wiki", "file this", "remember this source".
---

# write-wiki: Add to and Maintain the Knowledge Base

## Step 0: Orient

Read `~/.claude/CLAUDE.md` and find the `## Wikis` section.
This tells you every known wiki and its path.

Also check for `./knowledgebase/index.md` in the current working directory.

## Step 1: Does a wiki exist for this context?

**If yes:** proceed to Step 2 with the matching wiki path.

**If no wiki exists for the current project:**
Ask the user once:

> No wiki found for this project. Create one?
> [1] General Knowledge: adds to `C:\code\knowledgebase` (reusable patterns across engagements)
> [2] Project-specific: creates `./knowledgebase/` inside this project folder

Then bootstrap based on their choice (see Bootstrap section below) and proceed.

## Step 2: Determine the operation

Infer from context; don't ask unless truly unclear.

| Intent | Operation |
|---|---|
| User drops a URL, file, or paste of content | **ingest** |
| User says "update", "add a page", "save this" | **ingest** or **update** |
| User says "lint", "clean up", "audit" | **lint** |
| User says "save this answer" after a read-wiki session | **ingest** (save synthesis as a new wiki page) |

## Operation: ingest

A new source arrives (URL, file, paste, meeting notes, runbook, design doc).

1. **Save to raw/.** Fetch the URL with WebFetch if needed. Save as `raw/<slug>.md` with a header block:
   ```
   title: <title>
   source: <url or "direct input">
   date: <YYYY-MM-DD>
   captured: <how>
   ```
   Raw files are immutable. Never edit after saving.

2. **Surface takeaways.** Read the source. Tell the user the key points and which existing wiki pages it touches. Keep this brief; it is their curation moment.

3. **Write a source summary page** at `wiki/<slug>.md`: what it is, key claims, notable quotes with locations, `[[links]]` to entities and concepts it mentions.

4. **Update touched pages.** A single source typically touches 10-15 pages. For each relevant entity or concept page: strengthen, revise, or flag contradictions. Create new pages for important entities that don't have one yet. This integration step is the whole point. Do not skip it.

5. **Update index.md.** Add new pages (one line each, under the right section). Update changed entries.

6. **Append to log.md:**
   ```
   ## [YYYY-MM-DD] ingest | <Source title>
   <one-line note of what changed, pages touched>
   ```

## Operation: update

User wants to add a page, revise an existing one, or record operational knowledge (runbooks, decisions, configurations).

1. Write or update the relevant `wiki/` page directly.
2. Update `index.md` if a new page was created.
3. Append to `log.md`.

## Operation: lint

Health-check the wiki. Scan for and fix/report:
- **Contradictions** between pages
- **Stale claims** newer sources have superseded
- **Orphan pages** with no inbound `[[links]]`
- **Missing pages** for concepts mentioned often but lacking their own page
- **Missing cross-references** between pages that should link
- **Data gaps** worth a web search to fill

Fix safe issues directly. Propose wholesale rewrites before acting. Append lint summary to `log.md`.

## Bootstrap: creating a new wiki

### Option 1: General Knowledge (`C:\code\knowledgebase`)

The GK wiki already exists. Add to the `## Wikis` section in `~/.claude/CLAUDE.md` if not present:
```
- General Knowledge: `C:\code\knowledgebase\index.md` - reusable patterns across engagements
```
Then proceed with the ingest/update operation.

### Option 2: Project-specific (`./knowledgebase/`)

1. Create the folder structure:
   ```
   ./knowledgebase/
     CLAUDE.md      <- vault config (sections, conventions)
     index.md       <- empty catalog with section headers
     log.md         <- bootstrap entry
     raw/
     wiki/
   ```

2. Seed `knowledgebase/CLAUDE.md` with project name, owner, focus, and section headers.
   Default sections: Concepts, Entities, Topics, Sources, Implementation.

3. Update the **project root** `CLAUDE.md` (create it if missing) with:
   ```
   At session start, read ./knowledgebase/index.md for this project's accumulated knowledge.
   ```

4. Add an entry to the `## Wikis` section in `~/.claude/CLAUDE.md`:
   ```
   - <Project Name>: `<absolute path>\knowledgebase\index.md` - <one-line description>
   ```

5. Append to `knowledgebase/log.md`:
   ```
   ## [YYYY-MM-DD] bootstrap | Wiki created
   Project-specific wiki initialized. 0 pages.
   ```

The global `SessionStart` hook auto-injects this project's `index.md` from now on: it self-activates on any
folder that has `./knowledgebase/index.md`, so no per-project hook wiring is needed.

Then proceed with the operation that triggered the bootstrap.

## Principles (from Karpathy's design, honor them)

- **Lazy, not eager.** Don't mass-summarize. Grow where the user actually works.
- **User curates, you maintain.** They choose sources and ask questions. You do the bookkeeping.
- **Cheap index, lazy drill-down.** index.md stays small (one line per page).
- **Plain markdown, Obsidian-compatible.** `[[Wikilinks]]` everywhere. No vector DB.
- **Auto-write.** Make edits directly. User's safety net is git diff. Confirm before deleting a page wholesale.
