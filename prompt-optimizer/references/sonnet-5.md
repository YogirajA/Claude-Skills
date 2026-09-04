# Target model: Claude Sonnet 5

Source: [Prompting Claude Sonnet 5](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-sonnet-5).
Snippets in `text` blocks are quoted from that page and meant to be pasted verbatim, so their
punctuation is left exactly as published.

Model id `claude-sonnet-5`. Adaptive thinking is **on by default** (a change from Sonnet 4.6, where
the same request ran without thinking). Default effort is `high`. Existing Sonnet 4.6 prompts run
well without changes.

## Subtract before you add

| Remove | Why |
|---|---|
| "After every 3 tool calls, summarize progress" and similar interim-status scaffolding | Sonnet 5 gives regular, higher-quality updates on its own. |
| `temperature`, `top_p`, `top_k` at any non-default value | **Returns a 400 error.** New constraint for Sonnet-class models. Steer tone through the system prompt instead. |
| `thinking: {type: "enabled", budget_tokens: N}` | Manual extended thinking is removed and **returns a 400**. Use adaptive thinking plus effort. |
| "Only report high-severity issues", "be conservative", "don't nitpick" in review prompts | Followed more faithfully than by earlier models, so recall drops. See Code review below. |

## The literalism shift

Sonnet 5 interprets prompts literally and explicitly, especially at lower effort. It does not
silently generalize an instruction from one item to another and does not infer requests you did not
make. That is a feature for structured extraction and tuned pipelines, but it means **scope must be
stated**. If an instruction should apply broadly, say so: "Apply this formatting to every section,
not just the first one."

## Behaviours to steer, and the prompt text that steers them

### Response length

Length is calibrated to task complexity rather than a fixed verbosity: shorter on lookups, longer on
open-ended analysis. To reduce it:

```text
Provide concise, focused responses. Skip non-essential context, and keep examples minimal.
```

Positive examples of the concision you want beat negative instructions about what not to do.

### Thinking frequency

Adaptive thinking triggering is steerable. Large or complex system prompts can make it emit thinking
blocks more often than wanted:

```text
Thinking adds latency and should only be used when it will meaningfully improve answer quality, typically for problems that require multistep reasoning. When in doubt, respond directly.
```

If reasoning is shallow on complex problems, **raise effort first** rather than prompting around it.
Only if effort must stay at `low` for latency:

```text
This task involves multistep reasoning. Think carefully through the problem before responding.
```

### Tone

Prose style shifts between generations. If the product relies on a specific voice, re-evaluate style
prompts against the new baseline. Since `temperature` is unavailable, tone is a prompt-side lever now:

```text
Use a warm, collaborative tone. Acknowledge the user's framing before answering.
```

### Tool use triggering

More agentic than Sonnet 4.6 by default; it reaches for tools and runs self-verification loops more
readily. With thinking **disabled** it is less likely to reach for tools or consider searching, so
add an explicit nudge if you depend on tool calls with thinking off. `high` and `xhigh` show
substantially more tool use in agentic search and coding.

### Code review recall

A harness tuned for an earlier model can show *lower recall* on Sonnet 5. This is a harness effect,
not a capability regression: it investigates just as thoroughly, then declines to report findings
below the bar your prompt stated. Precision rises, measured recall falls.

```text
Report every issue you find, including ones you are uncertain about or consider low-severity. Do not filter for importance or confidence at this stage - a separate verification step will do that. Your goal here is coverage: it is better to surface a finding that later gets filtered out than to silently drop a real bug. For each finding, include your confidence level and an estimated severity so a downstream filter can rank them.
```

This works even without an actual second stage. If you must self-filter in one pass, set a concrete
bar rather than a qualitative one: "report any bugs that could cause incorrect behavior, a test
failure, or a misleading result; only omit nits like pure style or naming preferences."

### Frontend and design defaults

It settles into a consistent default visual style on open-ended briefs, which reads wrong for
dashboards, dev tools, fintech, healthcare, and enterprise apps. Generic negations ("don't use that
color", "make it clean and minimal") just move it to a different fixed palette. Two things work:

1. **Specify a concrete alternative.** Give explicit palette hex values, typography, spacing, radius,
   section structure, and transition timing. It follows detailed specs precisely.
2. **Have it propose options first.** With `temperature` unavailable this is the recommended way to
   get variety across runs:

```text
Before building, propose 4 distinct visual directions tailored to this brief (each as: bg hex / accent hex / typeface, plus a one-line rationale). Ask the user to pick one, then implement only that direction.
```

To steer away from the "AI slop" aesthetic:

```text
<frontend_aesthetics>
NEVER use generic AI-generated aesthetics like overused font families (Inter, Roboto, Arial, system fonts), cliched color schemes (particularly purple gradients on white or dark backgrounds), predictable layouts and component patterns, and cookie-cutter design that lacks context-specific character. Use unique fonts, cohesive colors and themes, and animations for effects and micro-interactions.
</frontend_aesthetics>
```

## Effort and token budget

`max` (no constraint) · `xhigh` (hardest coding and agentic) · `high` (default) · `medium`
(cost-sensitive) · `low` (short scoped tasks, latency-sensitive, not intelligence-sensitive).

It respects effort strictly, especially at the low end: at `low` and `medium` it scopes work to
exactly what was asked. Good for cost, but moderately complex tasks at `low` risk under-thinking.

Cross-model mapping when migrating: **Sonnet 5 at `medium` ≈ Sonnet 4.6 at `high`**, and
**Sonnet 5 at `high` ≈ Sonnet 4.6 at `max`**. When benchmarking, match by observed thinking length
rather than effort name.

Two `max_tokens` traps:
- `max_tokens` is a hard limit on **thinking plus response**. At `high` and above, leave headroom or
  you get a response that is almost entirely thinking, then a truncated answer with
  `stop_reason: "max_tokens"`. Raise `max_tokens` or drop to `medium`.
- Sonnet 5 uses a **new tokenizer producing roughly 30% more tokens for the same text**, so limits
  tuned on Sonnet 4.6 may truncate equivalent output.

If you previously ran Sonnet 4.6 with thinking off, try thinking on at a lower effort instead.

## Interactive coding products

Use `xhigh` or `high`, add autonomous modes, and reduce required human turns. Specify task, intent,
and constraints **up front in the first turn**: ambiguous asks spread over several user turns cost
more tokens and sometimes perform worse.

## Computer use

Supports `computer_toolset_20260801` (Claude API and Google Cloud) and `computer_20251124`, plus the
browser use tool `browser_toolset_20260801`. Works up to 2576px / 3.75MP; **1080p is the recommended
balance** of performance and cost, with 720p or 1366x768 as cheaper options.
