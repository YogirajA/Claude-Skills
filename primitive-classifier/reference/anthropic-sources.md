# Canonical Anthropic doc sources

These are the sources cross-checked in phase 3. URLs use the Mintlify `.md` endpoint, which is more stable than the rendered HTML (no per-request build IDs or analytics tokens).

When fetching, use `WebFetch` with a prompt asking for verbatim quotes about the primitive. Capture one quote per source for the `sources` block in the output JSON.

## Source list (id, group, title, url)

```yaml
- id: skills-overview
  group: Agent Skills
  title: Agent Skills overview
  url: https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview.md

- id: skills-best
  group: Agent Skills
  title: Skill authoring best practices
  url: https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices.md

- id: skills-cc
  group: Claude Code
  title: Claude Code skills
  url: https://code.claude.com/docs/en/skills.md

- id: memory
  group: Claude Code
  title: CLAUDE.md and memory
  url: https://code.claude.com/docs/en/memory.md

- id: subagents
  group: Claude Code
  title: Subagents
  url: https://code.claude.com/docs/en/sub-agents.md

- id: hooks
  group: Claude Code
  title: Hooks
  url: https://code.claude.com/docs/en/hooks.md

- id: settings
  group: Claude Code
  title: Settings configuration
  url: https://code.claude.com/docs/en/settings.md

- id: mcp-connector
  group: MCP
  title: MCP connector
  url: https://platform.claude.com/docs/en/agents-and-tools/mcp-connector.md

- id: engineering-blog
  group: Anthropic Engineering
  title: Equipping agents for the real world with Agent Skills
  url: https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills
```

## Per-source guidance

### `skills-overview`
Quote the "Skills are reusable, filesystem-based resources" line and the three-level loading model (metadata always-on, body on trigger, references on read). This grounds Q5 in the decision framework.

### `skills-best`
Quote the "<500 lines body" guidance and the "references one level deep" rule. This grounds size critiques and progressive-disclosure recommendations.

### `skills-cc`
Quote the "Create a skill when you keep pasting the same playbook ... or when a section of CLAUDE.md has grown into a procedure rather than a fact" line. This is the canonical "this should be a skill" trigger.

### `memory`
Quote both the "Keep it to facts Claude should hold in every session" line AND the "Settings rules are enforced by the client regardless of what Claude decides to do. CLAUDE.md instructions shape Claude's behavior but are not a hard enforcement layer" line. The first grounds Q4; the second grounds the entire "advisory vs enforcement" framing.

### `subagents`
Quote the "Each subagent runs in its own context window with a custom system prompt, specific tool access, and independent permissions" line. Plus the description-based delegation line.

### `hooks`
Quote the "Hooks are user-defined shell commands, HTTP endpoints, or LLM prompts that execute automatically at specific points in Claude Code's lifecycle" line, plus the "For instructions that never change, prefer CLAUDE.md" comparison.

### `settings`
Quote the table that distinguishes settings (permissions, env vars, tool behavior) from CLAUDE.md (instructions), Skills, and MCP servers.

### `mcp-connector`
Quote the "connect to remote MCP servers directly from the Messages API" line. Note that this doc is API-focused; the architectural framing of "MCP for connectivity, skills for expertise" lives in the engineering blog, not this reference doc.

### `engineering-blog`
The "MCP for connectivity, skills for expertise" framing is most concisely captured here. If Anthropic restructures their docs and this URL changes, search anthropic.com for "skills and mcp" or "agent skills connectivity expertise".

## Caching policy

Re-fetch all nine sources only when:

1. The user explicitly asks for a fresh check (`audit primitives, refresh sources`)
2. A snapshot drift check (e.g. Acme's `scripts/check-platform-docs.js`) reports any tracked URL changed
3. The most recent cached source is older than 30 days

Otherwise reuse cached quotes. The Mintlify endpoints are stable enough that monthly refresh is fine.
