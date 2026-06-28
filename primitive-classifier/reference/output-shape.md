# Output JSON shape

The build script consumes one JSON file matching this schema. All fields except those marked **(optional)** are required.

```jsonc
{
  // Hero text
  "title": "Acme primitives audit, what belongs where",
  "lede": "One paragraph. The argument in 60 to 100 words.",
  "meta": "Sources, scope, date, click instructions.",

  // 3 to 5 cards on the Overview tab. tone shapes the left border color.
  "verdicts": [
    {
      "tone": "info|warn|miss|good",
      "title": "Static content is delivered through MCP, the tool stays but its scope shrinks",
      "body": "About <strong>62 of 75 guidelines</strong>... HTML allowed."
    }
  ],

  // The six primitives. Standard set; only tweak if Anthropic ships a seventh.
  "buckets": [
    { "id": "claudemd",  "title": "CLAUDE.md",   "isFor": "...", "isNot": "..." },
    { "id": "subagents", "title": "Subagents",   "isFor": "...", "isNot": "..." },
    { "id": "skills",    "title": "Skills",      "isFor": "...", "isNot": "..." },
    { "id": "hooks",     "title": "Hooks",       "isFor": "...", "isNot": "..." },
    { "id": "settings",  "title": "settings.json","isFor": "...", "isNot": "..." },
    { "id": "mcp",       "title": "MCP",         "isFor": "...", "isNot": "..." }
  ],

  // The audit. One entry per item discovered in phase 1 plus one per missing primitive that should exist.
  "items": [
    {
      "name": "acme:ddd-patterns",                  // human-readable id
      "kind": "skill",                                  // skill | mcp-tool | guideline | subagent | hook | setting | claude-md
      "recommendedBucket": "skills",                    // one of the six bucket ids
      "currentLocation": "Skill (66 lines, body delegates to MCP)",  // short human description
      "currentBucket": "skills",                        // (optional) explicit current bucket; default derived from kind
      "status": "stub",                                 // correct | borderline | misplaced | stub | missing
      "reasoning": "Right primitive (skill), wrong shape...",
      "provenance": {
        "level": "documented",                          // documented | inferred | org | ambiguous
        "sources": ["skills-cc", "skills-best"],        // ids referencing entries in the sources block
        "note": "Optional one-liner explaining why this provenance level"
      }
    }
  ],

  // Anthropic doc citations. Used in the Sources tab and via provenance links.
  "sources": [
    {
      "id": "skills-overview",
      "group": "Agent Skills",
      "title": "Agent Skills overview",
      "url": "https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview.md",
      "quote": "Verbatim quote that grounds the primitive's purpose."
    }
  ],

  // The seven decision-framework questions, in order. Used in the Framework tab.
  "decisions": [
    {
      "q": "Does this need to BLOCK a tool call deterministically?",
      "yes": {
        "bucket": "hooks",                              // one of the six bucket ids
        "label": "Hook (PreToolUse / PostToolUse)",
        "detail": "Use a hook. Anthropic publishes the rm-rf example..."
      },
      "no": "Continue to question 2.",                  // string OR object with bucket/label/detail
      "cite": { "source": "hooks" }                     // id from sources block
    }
  ],

  // Extrapolation flags. Used in the Disclaimers tab.
  "disclaimers": [
    {
      "level": "documented|inferred|org|ambiguous",
      "title": "Short headline",
      "body": "Longer explanation. HTML allowed (use <code>, <strong>, etc.)."
    }
  ],

  // (optional) Phase plan shown at the bottom of Overview tab. If omitted, render skips the section.
  "phases": [
    {
      "title": "Phase 1, prove the model on one skill (this quarter)",
      "items": [
        "Migrate <strong>ddd-patterns</strong>...",
        "Add an ArchUnit verification step as a hook..."
      ]
    }
  ]
}
```

## Field rules

### `status` semantics

| Value | Meaning | UI label |
|---|---|---|
| `correct` | current = recommended, content shaped right | "Correct" |
| `borderline` | current = recommended, but could be sharper | "Borderline" |
| `misplaced` | current ≠ recommended; item should move | "Misplaced" |
| `stub` | current = recommended, but scope or content split is wrong | "Reshape in place" |
| `missing` | recommended bucket needs this; item does not exist | "Missing" |

The internal status value stays as `stub`. The build script renders the user-facing label "Reshape in place".

### `currentBucket` derivation (when omitted)

The build script derives:

| `kind` | Default `currentBucket` |
|---|---|
| `guideline` | `mcp` |
| `mcp-tool` | `mcp` |
| `skill` | `skills` |
| `subagent` | `subagents` (or `null` if status = missing) |
| `hook` | `hooks` (or `null` if status = missing) |
| `setting` | `settings` (or `null` if status = missing) |
| `claude-md` | `claudemd` (or `null` if status = missing) |

Set `currentBucket` explicitly only when the default is wrong, e.g. a skill that's currently mis-stored under `mcp-server/` or vice versa.

### `provenance.level` rules

- **documented**: Anthropic's docs explicitly state the rule that drives the placement. Quote it in `provenance.note` and include the URL via `provenance.sources`.
- **inferred**: A defensible reading of the docs but not stated in one verbatim line. Common for items where multiple Anthropic statements combine to support the placement.
- **org** (or any org slug): Org-specific context. Anthropic does not weigh in.
- **ambiguous**: Genuinely unclear. Flag in `disclaimers` so the reader knows.

The label "org" is the historical default; use any org slug (`acme`, `client`, `internal`) and update the CSS class via `--accent-org` in the template if you want a different color. The build script accepts any string for `level` but only the four listed values get distinct CSS styling out of the box.

### `verdicts.tone` styling

| Tone | Left border |
|---|---|
| `info` (default) | red, attention |
| `warn` | yellow, watch out |
| `miss` | purple, missing primitive |
| `good` | green, working as intended |

## Validation

Before passing data to the build script, validate:

- Every `recommendedBucket` matches one of the six bucket ids
- Every `provenance.sources[]` id exists in the `sources` block
- Every `decisions[].cite.source` exists in the `sources` block
- Every `decisions[].yes.bucket` (and `no.bucket` if object) matches a bucket id
- `verdicts` has 3 to 5 entries (4 is the sweet spot)
- `disclaimers` has at least 3 entries (one each for documented / inferred / org at minimum)

Pass through the validator in the build script (`--validate-only`) before generating output.
