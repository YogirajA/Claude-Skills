# Example: Acme audit summary

The skill produced this audit when run against `C:\code\Acme-Platform\platform-skills 1\` on 2026-04-28. Use it for orientation when classifying a similar enterprise stack (skills + Java MCP server + guideline files).

## Inventory

- 19 Acme skills under `platform-skills/acme/skills/`
- 12 MCP tools exposed by `platform-guidelines-mcp-server` (Java, Quarkus)
- 75 guideline `.md` files served via `mcp__platform-guidelines__get-guideline`
- 93 BCC files served via `mcp__platform-guidelines__get-bounded-context`
- 85 OpenAPI YAML specs served via `mcp__platform-guidelines__get-openapi-spec`
- 0 hooks, 0 subagents, minimal `settings.json`, partial CLAUDE.md per repo

## KPIs from the audit

| Metric | Today | After migration |
|---|---:|---:|
| Misplaced (in wrong primitive) | 61 | 0 |
| Reshape in place | 3 | 0 |
| Missing primitive | 11 | 0 |
| Items moving primitive | - | 61 |
| Items reshaped in place | - | 3 |
| Primitives created | - | 11 |

| Primitive | Today | After | Δ |
|---|---:|---:|---:|
| CLAUDE.md | 1 | 2 | +1 |
| Subagents | 0 | 3 | +3 |
| Skills | 19 | 80 | +61 |
| Hooks | 0 | 5 | +5 |
| settings.json | 0 | 2 | +2 |
| MCP | 87 | 26 | -61 |

## Headline calls

- The MCP `get-guideline` tool is **reshape in place**: the tool stays, but the type enum shrinks from 75 categories to ~13 mutable ones once the static guidelines migrate to skills.
- Two skills are reshape-in-place stubs that delegate their body to MCP: `acme:ddd-patterns` (slide 13's named example) and `acme:bcc-generation`.
- ~62 of the 75 guideline files are pure procedural knowledge ("how to write a hexagonal adapter", "git commit format", "how to name things") that belong in the skill marketplace, not behind an MCP tool call.
- ~13 guideline files are legitimately mutable: team contacts, infrastructure permissions, release calendar, Billing test customers, dashboard URLs, OpenAPI specs, BCCs. Keep these in MCP. Sharpen the server's scope.
- Hooks, subagents, and `settings.json` are absent. Iron laws like "no `@Transactional` in `application/`" are advisory text in skills today; they should be deterministic at the tool boundary.

## Provenance distribution

| Level | Count | Examples |
|---|---:|---|
| `documented` | ~25 | The six primitives' definitions. The "MCP for connectivity, skills for expertise" rule. CLAUDE.md ≤200 lines. Skill body ≤500 lines. |
| `inferred` | ~75 | "62 of 75 guidelines should be skills" (file-by-file judgment). The 148-line `ddd-patterns` target (Acme deck slide 13 number). The category split for individual borderline guidelines. |
| `org` | ~10 | The five suggested hooks. The three suggested subagents. The Phase 1/2/3 migration order. |
| `ambiguous` | ~5 | `jira-project-codes-guidelines.md`, `test-data-management-guidelines.md`, `acme-ai-agents-guidelines.md`, `sonarqube-api-guidelines.md`. Borderline static-vs-mutable. |

## Key lessons for future audits

1. **The "stub" / "reshape in place" diagnostic is rare but high-value.** Most items are simply correct, borderline, or misplaced. The reshape-in-place class catches the architectural mistake of "right primitive, wrong content split", which is otherwise invisible.

2. **The biggest wins come from migrating the bulk class.** In the Acme case, ~62 files moving from MCP to skills accounts for almost the entire migration cost. The other ~30 individual items (skills tweaked, subagents added, hooks created) are noise by comparison.

3. **Provenance honesty is the audit's value.** Without the `documented` / `inferred` / `org` / `ambiguous` flags, every claim looks equally weighty. With them, the reader can immediately tell which numbers to quote externally and which to argue internally.

4. **The decision framework should match Anthropic's framing, not the auditor's preferences.** The seven questions in `reference/decision-framework.md` map onto Anthropic's docs section by section; if Anthropic publishes a new primitive, add a question rather than reinterpreting an existing one.
