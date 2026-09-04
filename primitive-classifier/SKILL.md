---
name: primitive-classifier
description: Audit a folder for Claude Code primitives (skills, MCP servers, subagents, hooks, settings.json, CLAUDE.md) and classify each item into the primitive that actually fits, cross-checked against Anthropic docs. Produces a self-contained interactive HTML report with KPI hero, today vs target layout tabs, an explicit migration list, the 7-question decision framework, and provenance badges flagging documented vs inferred vs org-specific claims. Use when the user says "audit primitives", "classify skills and MCP", "primitive audit", "where does this content belong", "is this stuff in the right place", "review my Claude setup", or after generating any deck or doc that asserts which primitive a piece of context belongs in.
---

# Primitive classifier, audit a folder against the six Anthropic primitives

Produces an interactive HTML report classifying every skill, MCP tool, hook, subagent, settings entry and CLAUDE.md file in a target folder against the six Anthropic primitives, with provenance and migration recommendations.

## When to use

Run this whenever the user wants to know:

- Are my skills, MCP servers, hooks, etc. in the right primitives?
- What's misplaced today, what should move where, and how many things are we talking about?
- Is the architecture being asserted in this deck / doc / repo grounded in Anthropic docs or are we extrapolating?

The output is one HTML file that lays out today vs target, lists the explicit migrations, runs the decision framework, cites Anthropic's canonical docs, and flags every claim's provenance.

Triggers: "audit primitives", "classify skills", "primitive audit", "where does this belong", "review my Claude setup", "check our Claude Code architecture".

## What this skill produces

A single self-contained HTML file (typically 100kb+, no external assets) with six tabs:

| Tab | Content |
|---|---|
| **Overview** | KPI hero (today vs after migration), before/after movement table, headline verdicts, phase plan |
| **Today's layout** | Six buckets populated by current location |
| **Target layout** | Six buckets populated by recommended location |
| **Migrations** | Flat list of items that need action, with from → to and reasoning |
| **Decision framework** | The 7 questions, each citing the Anthropic doc that grounds it |
| **Sources & disclaimers** | Verbatim Anthropic doc quotes + extrapolation flags |

## Workflow

Five phases. Do them in order.

### Phase 1, discovery

Inventory the target folder. Read `reference/discovery-targets.md` for the exact patterns to scan.

Standard inventory:

```bash
# Skills
find "$TARGET" -name "SKILL.md" -o -name "skill.md"

# MCP servers (look for src/main/java for Java MCP, or .mcp.json, or mcp-server/)
find "$TARGET" -name ".mcp.json" -o -name "mcp.json"
find "$TARGET" -path "*mcp-server*" -name "*.java" | head -5

# Subagents
find "$TARGET" -path "*.claude/agents/*.md"

# CLAUDE.md hierarchy
find "$TARGET" -maxdepth 3 -name "CLAUDE.md" -o -name "CLAUDE.local.md"

# Settings
find "$TARGET" -path "*.claude/settings*.json"

# Hook scripts
find "$TARGET" -path "*.claude/hooks/*"

# Guideline files served by an MCP server (common Acme pattern)
find "$TARGET" -path "*resources/guidelines*.md"
```

For each found item, capture:

- `name` (file path or canonical id like `mcp:get-guideline`)
- `kind` (skill / mcp-tool / subagent / hook / setting / claude-md / guideline)
- `currentLocation` (one-line factual description, e.g. "MCP guideline served via get-guideline")
- relevant body text (first 50 lines is usually enough to judge content vs procedural)

### Phase 2, classification

For each inventoried item, walk the **decision framework** (`reference/decision-framework.md`). The framework is seven yes/no questions. First YES wins. The output is one of the six primitive buckets: `claudemd`, `subagents`, `skills`, `hooks`, `settings`, `mcp`.

Then assign one of these statuses by comparing **current** vs **recommended**:

| Status | Meaning |
|---|---|
| `correct` | Current bucket = recommended bucket, content is shaped right |
| `borderline` | Current = recommended, but the content shape could be sharper |
| `misplaced` | Current ≠ recommended; the item lives in the wrong primitive and should move |
| `stub` (rendered as "Reshape in place") | Current = recommended, but the scope or content split is wrong (e.g., a skill that delegates its body to MCP, or an MCP tool that exposes static content) |
| `missing` | The item should exist in the recommended bucket but does not exist anywhere |

The label "Reshape in place" is the user-facing rendering of the internal `stub` status. Internal class names, JSON keys, and CSS use `stub`; visible labels say "Reshape in place".

### Phase 3, cross-check against Anthropic

Fetch each canonical doc from `reference/anthropic-sources.md`. Use WebFetch or curl. For each doc:

1. Capture a verbatim quote that grounds the primitive's purpose
2. Note the URL
3. Mark which classifications in your inventory the doc supports

The Mintlify `.md` endpoint (e.g. `.../skills/overview.md`) is the stable variant. Avoid the rendered HTML.

### Phase 4, provenance

For every item, classify the **strength of evidence** behind its placement:

| Provenance | When to use |
|---|---|
| `documented` | Anthropic explicitly states the rule that drives this placement |
| `inferred` | A defensible reading of the docs, but not stated in one verbatim line |
| `org-specific` | Org context, not Anthropic's call |
| `ambiguous` | Docs do not address; this is a judgment call |

Then write disclaimers (`reference/disclaimer-templates.md`) for the most important extrapolations. The goal: a future reader should never confuse a doc-grounded claim with a judgment call.

### Phase 5, render

Run the bundled build script to produce the HTML:

```bash
node "${CLAUDE_SKILL_DIR}/scripts/build-html.js" --data audit-data.json --out primitives-categorization.html
```

The script takes a JSON file matching `reference/output-shape.md`, substitutes the data into the template, and writes a self-contained HTML.

If you want to inspect or tweak the template directly (rare), it lives at `template/primitives-categorization.template.html`.

## Output JSON shape

The build script consumes a single JSON file. Minimum required keys:

```json
{
  "title": "Acme primitives audit, what belongs where",
  "lede": "One paragraph framing the audit.",
  "meta": "Sources, scope, date.",
  "verdicts": [
    { "tone": "good|warn|miss|info", "title": "...", "body": "html allowed" }
  ],
  "buckets": [
    {
      "id": "claudemd|subagents|skills|hooks|settings|mcp",
      "title": "CLAUDE.md",
      "isFor": "...",
      "isNot": "..."
    }
  ],
  "items": [
    {
      "name": "acme:ddd-patterns",
      "kind": "skill",
      "recommendedBucket": "skills",
      "currentLocation": "Skill (66 lines, body delegates to MCP)",
      "currentBucket": "skills",
      "status": "stub",
      "reasoning": "...",
      "provenance": {
        "level": "documented|inferred|org-specific|ambiguous",
        "sources": ["skills-cc", "skills-best"],
        "note": "..."
      }
    }
  ],
  "sources": [
    { "id": "skills-overview", "group": "Agent Skills", "title": "...", "url": "...", "quote": "..." }
  ],
  "decisions": [
    {
      "q": "Does this need to BLOCK a tool call deterministically?",
      "yes": { "bucket": "hooks", "label": "Hook", "detail": "..." },
      "no": "Continue.",
      "cite": { "source": "hooks" }
    }
  ],
  "disclaimers": [
    { "level": "documented|inferred|org-specific|ambiguous", "title": "...", "body": "html allowed" }
  ]
}
```

For the full schema with optional fields, see `reference/output-shape.md`.

## Iron rules

1. **No em dashes anywhere in the output.** Use a colon, period, comma, "and", or rewrite. The skill applies this to every generated string.
2. **Group items by `recommendedBucket` in the target tab and by `currentBucket` (or kind-derived default) in the today tab.** A misplaced item should appear under its current location in "Today" and its target location in "Target". The migrations tab shows both via from → to.
3. **Internal STATUS value stays `stub`; visible label is "Reshape in place".** The build script handles the rendering. Do not rename the JSON key.
4. **Cite, do not paraphrase silently.** Every "Anthropic says X" claim needs a doc URL in the sources block.
5. **Flag ambiguity loudly.** If you find yourself unsure whether something is documented or inferred, mark it `ambiguous` and write a disclaimer. The skill's value is in the honest map, not the false confidence.

## Quick start

```text
audit primitives in ~/code/example-platform/digital-skills 1/
```

Claude reads this skill, walks the five phases, and writes `primitives-categorization.html` next to the target folder.

## Reference files (one level deep)

- `reference/discovery-targets.md`: glob patterns and file shapes to scan in phase 1
- `reference/decision-framework.md`: the 7 questions verbatim with citation URLs
- `reference/anthropic-sources.md`: canonical doc URLs to fetch in phase 3
- `reference/output-shape.md`: the full JSON schema the build script accepts
- `reference/disclaimer-templates.md`: common extrapolation patterns to flag
- `template/primitives-categorization.template.html`: the HTML scaffold; do not edit unless adding new sections
- `scripts/build-html.js`: substitutes a JSON data file into the template
- `examples/acme-output-summary.md`: what an audit produced on a placeholder stack (for orientation)

## Anti-patterns

- **Don't classify by file location alone.** A `.md` file under `mcp-server/resources/` is delivered as MCP content today, but if its body is a procedural playbook ("how to write a hexagonal adapter") it belongs in skills. Classify by content shape, not directory.
- **Don't use "stub" as a user-visible label.** It is the internal status; the UI says "Reshape in place".
- **Don't bake migration order into the framework.** Phase order is a recommendation, not Anthropic doctrine. Mark migration plans as `org-specific` provenance unless the user explicitly asks for an org-neutral output.
- **Don't bloat the verdicts.** Four cards max on the overview tab; if a fifth point matters, it goes in the migration narrative.
- **Don't fetch Anthropic docs blindly each run.** Cache the source quotes in the JSON. Re-fetch only when the user asks for a fresh check or the deck check script reports drift.
