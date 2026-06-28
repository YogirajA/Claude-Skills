# Disclaimer templates

The honest accounting of where the audit extrapolates beyond Anthropic. Drop these into the `disclaimers` block of the output JSON, swapping the org-specific bits for the actual context.

Four levels:

| Level | When to use |
|---|---|
| `documented` | Anthropic's docs explicitly state the rule that drives the call |
| `inferred` | A defensible reading of the docs but not stated in one verbatim line |
| `org` (or any org slug) | Org context, not Anthropic's |
| `ambiguous` | Genuinely unclear; flag it loudly |

## What NOT to disclaim

Aim for fewer disclaimers, not more. **A disclaimer that restates what the provenance tag already conveys is bloat.** If you find yourself writing "this is org context because the org tag says so," cut it.

Concrete cases to omit:

- **"The N suggested hooks/subagents/settings are org-specific"**: of course they are. Every recommendation in a section labeled with the org slug is org context. Don't repeat it.
- **"The phased migration order is the audit's recommendation"**: anything labeled with the org slug already conveys this. Migration plans are inherently judgment.
- **"The borderline items could go either way"**: the bucket grid already shows borderline status with reasoning. A disclaimer that just lists the borderline file names duplicates content.
- **Dates and version claims sourced from a deck/doc**: only worth a disclaimer if they appear AS NUMBERS in the audit's main pages. If the date isn't visible to a reader of the report, don't pre-empt a hypothetical external quote.

A disclaimer earns its place by telling the reader something they would otherwise miss. Tag-level provenance is already on every item; disclaimers are for the meta-level claims.

## Always-include disclaimers

These belong in every audit, regardless of target folder. Customize the body wording but keep the structure.

```json
[
  {
    "level": "documented",
    "title": "The six-primitive framing itself",
    "body": "Each primitive's definition (Skills, CLAUDE.md, Subagents, Hooks, settings.json, MCP) is taken directly from Anthropic docs. The 'is for / is not for' lines on each bucket card are paraphrases of doc language, with the source linked."
  },
  {
    "level": "documented",
    "title": "The 'MCP for connectivity, skills for expertise' rule",
    "body": "This is the canonical framing in Anthropic's Dec 2025 engineering blog (Equipping agents for the real world with Agent Skills). Anthropic's reference docs do not state it as one sentence, but the architectural design (skills are filesystem-loaded; MCP is a network protocol for remote tools) makes the claim load-bearing."
  },
  {
    "level": "documented",
    "title": "CLAUDE.md is advisory, hooks and settings are enforced",
    "body": "Anthropic's own words from the memory doc: 'Settings rules are enforced by the client regardless of what Claude decides to do. CLAUDE.md instructions shape Claude\\'s behavior but are not a hard enforcement layer.' This grounds the entire 'missing primitives' call."
  },
  {
    "level": "documented",
    "title": "'Reshape in place' status, the diagnostic shape",
    "body": "Some items live in the right primitive but with the wrong scope or content split: an MCP tool that exposes static content categories, or a skill that delegates its body to an MCP fetch. We call these <strong>reshape in place</strong> because the architectural shape is wrong even though the primitive choice is right. This taxonomy is ours; Anthropic does not name it. The fix in each case (shrink the enum, inline the body) is doc-grounded."
  }
]
```

## Common per-audit disclaimers

### Inferred line counts

Whenever the audit recommends a specific line count, flag it as inferred:

```json
{
  "level": "inferred",
  "title": "Targeting ~150 lines per skill body",
  "body": "Anthropic's explicit cap is <strong>500 lines</strong>, not 150. The 150-line target is from the audit's own preferences, citing Anthropic's 'context window is a public good' principle. Reading the line target as Anthropic guidance is wrong; reading it as a stretch goal grounded in Anthropic's direction is fair."
}
```

### Inferred migration counts

```json
{
  "level": "inferred",
  "title": "'~62 of 75 guidelines should be skills'",
  "body": "A judgment call, file-by-file. The category split (procedural vs. mutable) is grounded in the doc framing, but the exact count is ours, and reasonable people could draw the line a few items either way. Borderline cases are flagged in the bucket grid below."
}
```

### Org-specific recommendations

```json
{
  "level": "org",
  "title": "The N suggested hooks",
  "body": "Each is a direct mapping of an existing org rule (currently advisory in skills) to the hook pattern Anthropic publishes. The mapping is sound but the specific scripts are org context."
}
```

```json
{
  "level": "org",
  "title": "The N suggested subagents",
  "body": "These names appear in skill files as references but no <code>.claude/agents/*.md</code> files exist for them in the audited tree. Treat the recommendation as 'the org should formalize what its own skills already reference' rather than a direct Anthropic prescription."
}
```

```json
{
  "level": "org",
  "title": "The Phase 1 / 2 / 3 migration order",
  "body": "Anthropic does not prescribe migration order; they describe primitives. The order is a recommendation derived from the audit's own analysis."
}
```

### Ambiguous items

```json
{
  "level": "ambiguous",
  "title": "Whether some borderline guidelines should migrate",
  "body": "Items with a procedural part AND a live-data part have a defensible call in either bucket. The audit defaulted them to one; the opposite call is also reasonable. Call this judgment-bound."
}
```

```json
{
  "level": "ambiguous",
  "title": "Plugin marketplace ship dates",
  "body": "If the audit asserts specific dates for Anthropic feature releases (skills shipped October 2025, plugin marketplaces December 2025), re-verify against the relevant Anthropic doc before quoting them externally."
}
```

## Writing custom disclaimers

When you spot a claim in the audit that goes beyond what Anthropic says verbatim, write a disclaimer with this shape:

```json
{
  "level": "<documented|inferred|org|ambiguous>",
  "title": "<short headline that names the claim>",
  "body": "<longer explanation. What does Anthropic actually say? Where do we extrapolate? Why is the extrapolation defensible (or not)?>"
}
```

Aim for at least one disclaimer per provenance level. A disclaimer set with only `documented` entries is suspicious: every audit involves judgment.
