---
name: anthropic-doc-validator
description: Validate claims, documentation, code examples, or generated content about Claude Code, the Anthropic API, or Anthropic SDKs against the latest official documentation. Use when the user asks to "validate against docs", "check against anthropic docs", "verify this is current", "is this still accurate", "audit content against documentation", or similar. Also use proactively after generating slides, READMEs, blog posts, training materials, or runbooks that make specific factual claims about Anthropic products, so that those claims do not drift from the source of truth.
---

# Validate content against the latest Anthropic documentation

When invoked, your job is to take a body of content (a file, a passage, a code sample, or a list of claims) and check each factual assertion against the current Anthropic docs. You produce a structured report. You do NOT silently fix things; you surface findings so the user can decide.

## Workflow

1. **Identify what to validate.**
   - If the user pointed at a file or section, read it.
   - If the user pasted a claim, treat the message as the input.
   - Extract a list of discrete, factual, verifiable claims. Skip stylistic opinions and the user's own preferences.

2. **Map each claim to the most likely doc page.** Use the URL index below. If you are unsure, fetch `https://code.claude.com/docs/llms.txt` first to discover the index.

3. **Fetch the doc page with a specific, narrow prompt.** Use `WebFetch` and ask for the exact passage that confirms or refutes the claim. Quote verbatim. Do not paraphrase the docs.

4. **Compare claim vs. doc.** Classify each finding as one of:
   - **Confirmed** — doc quote supports the claim.
   - **Refuted** — doc quote contradicts the claim. Include the corrected statement.
   - **Stale / changed** — doc indicates the API or behavior has changed (deprecated, renamed, replaced).
   - **Not documented** — doc page does not address the claim. Note that this does NOT mean the claim is wrong, only unverifiable from official docs.
   - **Ambiguous** — doc text is consistent with multiple readings; flag for human judgment.

5. **Produce the report.** Use the format in the Output section below.

6. **Do not modify the original content unless the user asks.** Validation is read-only by default. If they say "fix it", apply the corrections; otherwise just report.

## Anthropic documentation URL index

Use these as your first stop. Only fall back to `WebSearch` if a topic isn't covered here.

### Claude Code (the CLI)

| Topic | URL |
|---|---|
| Doc index (truth source) | `https://code.claude.com/docs/llms.txt` |
| CLAUDE.md, rules, auto memory | `https://code.claude.com/docs/en/memory` |
| settings.json hierarchy, all settings keys | `https://code.claude.com/docs/en/settings` |
| Hooks (events, JSON payload, exit codes) | `https://code.claude.com/docs/en/hooks` |
| Skills (precedence, frontmatter, locations) | `https://code.claude.com/docs/en/skills` |
| MCP servers (scopes, precedence) | `https://code.claude.com/docs/en/mcp` |
| Permissions (allow/deny, sandbox) | `https://code.claude.com/docs/en/permissions` |
| Plugins | `https://code.claude.com/docs/en/plugins` |
| CLI flags, env vars | `https://code.claude.com/docs/en/cli-reference` |
| Subagents | `https://code.claude.com/docs/en/sub-agents` |
| Hooks guide (worked examples) | `https://code.claude.com/docs/en/hooks-guide` |
| Context window | `https://code.claude.com/docs/en/context-window` |
| Debug a config | `https://code.claude.com/docs/en/debug-your-config` |
| Features overview | `https://code.claude.com/docs/en/features-overview` |

### Anthropic API / SDK

| Topic | URL |
|---|---|
| API docs root | `https://docs.anthropic.com` |
| Models (capabilities, IDs, deprecation) | `https://docs.anthropic.com/en/docs/about-claude/models` |
| Messages API | `https://docs.anthropic.com/en/api/messages` |
| Tool use | `https://docs.anthropic.com/en/docs/build-with-claude/tool-use` |
| Prompt caching | `https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching` |
| Extended thinking | `https://docs.anthropic.com/en/docs/build-with-claude/extended-thinking` |
| Files API | `https://docs.anthropic.com/en/docs/build-with-claude/files` |
| Batch API | `https://docs.anthropic.com/en/api/creating-message-batches` |
| Citations | `https://docs.anthropic.com/en/docs/build-with-claude/citations` |
| Agent SDK (Python) | `https://docs.anthropic.com/en/api/agent-sdk/python` |
| Agent SDK (TypeScript) | `https://docs.anthropic.com/en/api/agent-sdk/typescript` |

### GitHub repos (for known issues, feature requests)

- Claude Code: `https://github.com/anthropics/claude-code/issues`
- Anthropic SDKs: search via `gh` CLI when needed

## How to call WebFetch correctly

Write a prompt that asks for specific verifiable facts, not summary. Bad prompts produce paraphrased answers that drift. Good prompts ask for quotes.

**Good prompt to WebFetch:**
> "Find documentation on `claudeMdExcludes`. Quote VERBATIM the section that explains: (a) what JSON file it lives in, (b) whether patterns are matched against absolute or relative paths, (c) whether the setting works on managed-policy CLAUDE.md files."

**Bad prompt:**
> "Tell me about claudeMdExcludes."

## Output format

Produce a markdown report. One row per claim. Group by status.

```markdown
# Validation report: <subject>

Validated against: <list of URLs fetched, with timestamps>

## Summary
- N confirmed
- N refuted
- N stale/changed
- N not documented
- N ambiguous

## Refuted (HIGHEST PRIORITY)

### Claim: "<exact quote of the claim from the content>"
**Status:** Refuted
**Doc text:** > "<verbatim quote from doc>"
**Source:** <URL>
**Correction:** <one-line statement of what the claim should say>

## Stale / changed

(same format as Refuted)

## Confirmed

### "<claim>"
**Source:** <URL>
**Doc text:** > "<verbatim quote>"

## Not documented

(list claims with brief note on what was checked)

## Ambiguous

(list claims with both readings and a recommendation for which to use)

## Recommended fixes

<numbered list of concrete textual changes the user could apply>
```

## Things to watch out for

- **Doc pages change.** Always quote verbatim with a timestamp. A correct answer from last week may be stale today.
- **Feature requests vs shipped features.** Some terms (e.g., env vars, settings keys) appear in GitHub issues as requests. Verify against the docs, not just search snippets.
- **Version-specific behavior.** If a doc says "requires Claude Code v2.x.y or later", flag that the claim may only apply to recent installs.
- **API vs CLI confusion.** `https://docs.anthropic.com` covers the API/SDK. `https://code.claude.com` covers the CLI. They are different products; don't validate CLI claims against API docs.
- **Path matching is the #1 source of subtle bugs.** Different settings use different conventions: `claudeMdExcludes` matches absolute paths; `.claude/rules/` `paths:` field matches relative paths. Always check.
- **Frontmatter keys are case-sensitive and exact.** YAML formatting matters.

## Scope limits

This skill validates against PUBLIC Anthropic documentation only. It does not validate:
- Third-party blog posts, even from well-known authors
- ClaudeLog, eesel, or community wikis (use as discovery aids, not source of truth)
- GitHub issue comments that are not from Anthropic staff
- Internal Anthropic docs you do not have access to

If the only available source is a community blog, say so explicitly in the report and downgrade the confidence rating.
