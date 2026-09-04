# Target model: Claude Opus 5

Source: [Prompting Claude Opus 5](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5).
Read this before assembling the prompt. Snippets in `text` blocks are quoted from that page and are
meant to be pasted verbatim, so their punctuation is left exactly as published.

Model id `claude-opus-5`. Thinking is **on by default**; it can be disabled only at effort `high` or
below. Default effort is `high`. Existing Opus 4.8 prompts run well without changes; the items below
are the ones that usually need tuning.

## Subtract before you add

Opus 5 does several things unprompted that older prompts explicitly asked for. Leaving those
instructions in makes the behaviour worse, not better. **Delete these from any prompt you inherit:**

| Remove | Why |
|---|---|
| "Include a final verification step", "use a subagent to verify" | Opus 5 verifies its own work unprompted. These cause over-verification and waste tokens with no quality gain. |
| "Double-check your answer", "re-verify before responding" | Same compounding effect. It already self-corrects well. |
| "Only report high-severity issues", "be conservative", "don't nitpick" in review prompts | Taken literally, so it reports less. Ask for everything and filter in a separate pass. |
| Any rule telling the model not to think or not to reason | Increases internal-tag leakage when thinking is disabled. |
| Prompt-side vision workarounds tuned for older models | Re-validate; they are often no longer needed. |

This subtraction step is the highest-value part of targeting Opus 5. Do it before adding anything.

## Behaviours to steer, and the prompt text that steers them

### Response length

Default user-facing responses run longer than prior Opus models. Effort controls how much it
*thinks*, not how much it *says*, so lowering effort will not reliably shorten the visible answer.
Prompt for length explicitly.

```text
Keep responses focused, brief, and concise. Keep disclaimers and caveats short, and spend most of the response on the main answer. When asked to explain something, give a high-level summary unless an in-depth explanation is specifically requested.
```

In a long system prompt, repeat a short reminder near the end:

```text
<tone_preference>
Keep outputs reasonably concise.
</tone_preference>
```

### Agentic narration

It announces what it is about to do and its per-message output in agentic sessions runs long.
Describe the cadence you want rather than forbidding narration:

```text
Before your first tool call, say in one sentence what you're about to do. While working, give a brief update only when you find something important or change direction. When you finish, lead with the outcome: your first sentence should answer "what happened" or "what did you find," with supporting detail after it for readers who want it.
```

Positive examples of the style you want beat instructions about what not to do. The same lever works
in the other direction to increase narration.

### Written deliverable length

Separate lever from conversational verbosity. Files written to disk (reports, Markdown, summaries)
run long. If the product ships Claude-authored documents:

```text
Match the length of written documents to what the task needs: cover the substance, but do not pad with filler sections, redundant summaries, or boilerplate.
```

### Task scope

It can widen scope, adding steps that were not requested.

```text
Deliver what was asked, at the scope intended. Make routine judgment calls yourself, and check in only when different readings of the request would lead to materially different work. If the request seems mistaken or a better approach exists, say so in a sentence and continue with the task as asked rather than quietly narrowing, widening, or transforming it. Finish the whole task, and stop short of actions that are clearly beyond what was asked.
```

### Subagent spawning

It delegates more readily than prior models. Delegation pays on genuinely independent, sizeable
tracks and multiplies cost on small ones.

```text
Delegate to a subagent only for large tasks that are genuinely independent and parallelizable, such as a wide multi-file investigation. Do not delegate work you can finish yourself in a handful of tool calls, and do not use subagents to verify or double-check your own work. If one subagent can complete the task, use one rather than several, and keep spawn counts low.
```

For Claude Code or the Agent SDK there are deterministic caps instead:
`CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH`, `CLAUDE_CODE_MAX_CONCURRENT_SUBAGENTS`, and the SDK's
`max_budget_usd`. They need Claude Code 2.1.217 or later.

### Correction narration

It narrates corrections to its own earlier statements more than prior models, which reads badly in
user-facing products.

```text
Only correct an earlier statement when the error would change the user's code, conclusions, or decisions. State corrections plainly and briefly, then continue the task. For slips that change nothing for the user, make the fix and move on without noting it.
```

## Effort

Default `high`. `low` and `medium` give strong quality at a fraction of the tokens and latency, and
accuracy holds at lower effort even for code review, which supports a fast pass then a thorough one.
Step up to `xhigh` for demanding coding and agentic work. Re-run an effort sweep on your own evals
rather than carrying defaults over from another model.

## If thinking must be disabled

Prefer thinking on at `low` effort over thinking off: for most tasks it performs better at similar
cost. If the integration requires thinking off, two artifacts can appear. Tool calls can be written
into visible text instead of emitted as a structured `tool_use` block (the call never runs, and in
agent loops the leaked text stays in history and affects later turns). Internal `<thinking>` tags can
appear in the visible response. One combined instruction mitigates both:

```text
When you use a tool, you may say a brief sentence first. If no tool can express what the user asked for, say so instead of guessing. Do not include internal or system XML tags in your response.
```

Naming thinking tags specifically is less effective than this general form.

## Where Opus 5 is strong enough to prompt less

Multi-file features and larger refactors (give the complete spec up front and let it run), code
review precision and recall, 1M context with consistent instruction following throughout, multi-sheet
spreadsheets and slide decks, chart and diagram vision, and subagent coordination with writer-verifier
patterns. Vision is strongest when it has tools to crop and visually verify, which is a more
cost-effective lever than thinking alone.
