# Decision framework, the 7 questions

Walk top to bottom. Take the first **YES**. Each question cites the Anthropic doc that grounds it.

## Q1: Does this need to BLOCK a tool call deterministically?

Examples: "no `rm -rf`", "no `@Transactional` in `application/`", "no PII in analytics edits", "block writes to `./secrets/**`".

- **YES** → **Hook** (PreToolUse / PostToolUse). Anthropic's hooks doc publishes the rm-rf example almost verbatim, plus the lint-on-PostToolUse pattern. CLAUDE.md cannot enforce; hooks can.
- **NO** → continue to Q2.
- Cite: https://code.claude.com/docs/en/hooks.md

## Q2: Is the rule a binary tool-permission allow/deny?

Examples: "always allow `npm test`", "never let `curl` run", "block writes to `./secrets/**`".

- **YES** → **settings.json** (`permissions.allow` / `permissions.deny`). The doc is explicit: settings rules are enforced by the client regardless of what Claude decides to do.
- **NO** → continue to Q3.
- Cite: https://code.claude.com/docs/en/settings.md

## Q3: Is the content a hard floor that must NOT be overridable by individual users?

Compliance, regulatory, security policy.

- **YES** → **managed-policy CLAUDE.md** or managed `settings.json` (deployed via MDM / Group Policy / `/etc/claude-code/`). Anthropic explicitly distinguishes managed-policy CLAUDE.md from project-tier and provides exact paths. Without MDM, project-tier in git is the floor that matters this quarter.
- **NO** → continue to Q4.
- Cite: https://code.claude.com/docs/en/memory.md (Deploy organization-wide CLAUDE.md section)

## Q4: Is this a fact or convention Claude needs in EVERY session, regardless of task?

Build commands, code style, "always do X" rules.

- **YES** → **CLAUDE.md** (project tier, target ≤200 lines). The doc explicitly says CLAUDE.md is for "facts Claude should hold in every session." Path-scoped rules in `.claude/rules/` are the right tool when content grows past 200 lines.
- **NO** → continue to Q5.
- Cite: https://code.claude.com/docs/en/memory.md (When to add to CLAUDE.md section)

## Q5: Is this a multi-step procedure that only applies in certain situations?

A "playbook" you keep pasting in chat. A section of CLAUDE.md that has grown into a procedure.

- **YES** → **Skill** (`.claude/skills/<name>/SKILL.md`). Anthropic's exact words: "Create a skill when you keep pasting the same playbook ... or when a section of CLAUDE.md has grown into a procedure rather than a fact." Body ≤500 lines, references one level deep.
- **NO** → continue to Q6.
- Cite: https://code.claude.com/docs/en/skills.md

## Q6: Does this need its OWN context window, its own tool allowlist, and to be auto-delegated when a task matches its description?

Examples: a security reviewer that cannot write, a research agent that only reads.

- **YES** → **Subagent** (`.claude/agents/<name>.md`). The doc says: "Each subagent runs in its own context window with a custom system prompt, specific tool access, and independent permissions." This is the only primitive that gives hard tool boundaries by role.
- **NO** → continue to Q7.
- Cite: https://code.claude.com/docs/en/sub-agents.md

## Q7: Is this DATA that lives outside the codebase and changes on a business cadence?

Live OpenAPI specs, ticket state, dashboard URLs, team contacts, tenant config, sprint calendar.

- **YES** → **MCP server tool**. The connector is "for connecting to remote MCP servers" with live tool calls. The Anthropic engineering blog (Dec 2025) crystallizes it: connectivity goes here, expertise goes in skills. If you find yourself putting static "how to" content in MCP, the answer is Q5, not this question.
- **NO** → default to **Skill** and re-evaluate. If none of the above fit, the content is most likely procedural (skill) or a fact (CLAUDE.md). MCP and hooks are not catchalls; they earn their place by passing Q1, Q2, or Q7.
- Cite: https://platform.claude.com/docs/en/agents-and-tools/mcp-connector.md

## Notes on ambiguity

- An item that scores YES on Q1 AND would also work as a Q5 skill is best implemented as a **skill plus a hook**: skill for the procedural guidance, hook for the deterministic enforcement. Mark this in the reasoning.
- Borderline items between Q5 (skill) and Q7 (MCP) are common when content is "mostly static, but the dataset behind it changes." Default to skill and have the skill call an MCP tool for the live lookup.
- An item that lives in the right primitive but with the wrong scope (an MCP tool exposing 75 static categories, a skill stub delegating its body to MCP) is **status `stub`**, rendered as "Reshape in place". Q1 through Q7 still produce the same answer; the diagnostic just says the implementation needs work.
