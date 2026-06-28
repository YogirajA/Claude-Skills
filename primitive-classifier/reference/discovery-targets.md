# Discovery targets, what to scan in phase 1

The skill walks the target folder and inventories every file that maps onto a Claude Code primitive. This file documents the patterns.

## Directory walk

For each target folder, run these in parallel via Glob and Bash:

```bash
TARGET="$1"  # the folder the user wants audited

# Skills (case-insensitive: SKILL.md or skill.md, in any subdirectory)
find "$TARGET" -type f \( -name "SKILL.md" -o -name "skill.md" \)

# Subagents
find "$TARGET" -type f -path "*.claude/agents/*.md"

# CLAUDE.md files (project, local, nested)
find "$TARGET" -type f \( -name "CLAUDE.md" -o -name "CLAUDE.local.md" \)

# Settings
find "$TARGET" -type f \( -name "settings.json" -o -name "settings.local.json" \) -path "*.claude/*"

# Hook scripts
find "$TARGET" -type f -path "*.claude/hooks/*"

# Path-scoped rules
find "$TARGET" -type f -path "*.claude/rules/*.md"

# MCP server source (Java pattern, common in enterprise)
find "$TARGET" -type d -name "mcp-server" -o -type d -name "*-mcp-server"

# MCP server config (declarative)
find "$TARGET" -type f \( -name ".mcp.json" -o -name "mcp.json" \)

# MCP-served guideline files (Acme pattern, generalize as needed)
find "$TARGET" -type f -path "*resources/guidelines/*.md"
find "$TARGET" -type f -path "*resources/ddd/*.md"
find "$TARGET" -type f -path "*resources/openapi/*.yaml"
```

## What to extract per item

| Item kind | Capture | Why |
|---|---|---|
| Skill | `name` (frontmatter), `description`, line count, mentions of MCP fetches in body | Triggers stub detection (skill that delegates body) |
| MCP tool | tool name, description, what it serves | Distinguishes connectivity vs static-content |
| Guideline file (MCP-served) | file name, first heading, body shape (procedural vs reference) | The big migration class for Acme-style stacks |
| Subagent | `name`, `description`, `tools`, `model` | Confirms whether the role is well-bounded |
| CLAUDE.md | line count, subsection list, mentions of "always X" facts vs procedures | Triggers Q4 vs Q5 split |
| Settings | `permissions.allow`, `permissions.deny`, hook config | Reveals what's already deterministic vs advisory |
| Hook script | event type, matcher, command shape | Pre-existing enforcement |

## Stub detection heuristics

A skill is a **stub** (Reshape in place) if any of these are true:

1. Body length < 100 lines AND body contains 3+ references to `mcp__` calls or `get-guideline type=`
2. Body contains text like "see the guideline at..." with no inline iron laws
3. Body is mostly a list of MCP tool calls without procedural content

An MCP tool is **stub-like** if:

1. It exposes a `type` enum with > 20 categorically-different values
2. Its underlying data files are predominantly markdown procedural content (not live JSON, not schemas, not specs)

Both patterns produce status `stub`, rendered as "Reshape in place" in the UI.

## Body shape classification (for guideline files)

When inventorying MCP-served guideline `.md` files, read the first 50 lines and classify:

| Body shape | Suggests |
|---|---|
| Iron-law list ("MUST do X, MUST NOT do Y") with code templates | **Skill** (procedural) |
| Reference table of dates / IDs / URLs / contacts | **MCP** (live data) |
| Tutorial / walkthrough / playbook | **Skill** (procedural) |
| Catalog of mutable items (services, projects, dashboards) | **MCP** (live data) |
| Compliance / regulatory text the org cannot edit | **Managed CLAUDE.md** or **managed settings** |
| Pure naming convention with examples | **CLAUDE.md** (fact) or **Skill** (if it's a "how to name" walkthrough) |

The heuristic is rough; the decision framework in `decision-framework.md` is the authoritative arbiter. Use the body-shape classification to seed the framework, not replace it.

## What to skip

- `node_modules/`, `target/`, `dist/`, `build/`, `.git/`
- Generated files (`*.lock`, `*.min.js`)
- Backup files (`*.bak`, `*.backup`, `*.old`)
- The skill's own template / scripts (so the audit doesn't audit itself recursively)
