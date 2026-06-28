---
name: prompt-optimizer
description: Transform a raw or messy ask into an XML-structured Claude prompt (role / context / task / examples / output format / constraints), validate it with the user, then execute it to produce the actual deliverable. The XML output is built to be used as-is and run for you, not hand-edited. Use when the user explicitly invokes /prompt-optimizer, says "optimize this prompt", "wrap this in XML tags", "rewrite this as a Claude prompt", or "structure this and run it", or pastes a long, ambiguous, multi-requirement, multi-step ask that clearly benefits from structured framing before execution. Do NOT use when the user just wants a cleaned-up, plain-English prompt handed back to read, paste, and tweak themselves, that is the prompt-fixer skill (English hygiene, no XML, no execution). Also skip simple one-liners, greetings, trivial code edits, direct file reads, or clear conversational follow-ups.
---

# Prompt Optimizer

Claude models perform best when instructions arrive as **XML-tagged** structured prompts. (Anthropic's own prompt-engineering docs recommend XML tags over JSON for prompts — tags are easier to nest, easier for Claude to parse, and don't fight with code or strings inside the content.) This skill takes a user's raw ask, restructures it into that format, validates with the user, then executes.

## When to invoke

**Invoke when:**
- User typed `/prompt-optimizer` explicitly.
- The ask is **complex**: ≥2 of {multi-step workflow, specific output format required, domain-specific reasoning, examples would meaningfully change the answer, constraints that are easy to miss, persona/role matters}.
- User pasted a wall of requirements and said "do this" — the prompt itself is the bottleneck.

**Skip when:**
- One-shot lookups: "what does this function do", "read this file", "what's the date".
- Conversational follow-ups where context is already established.
- Mechanical edits: rename, format, add a log line.
- Anything where the structuring overhead > the clarity gain.
- The user wants a plain-English prompt handed back to edit by hand, not XML you'll execute. That's the **prompt-fixer** skill. This skill owns the XML lane; prompt-fixer owns plain-English hygiene.

When in doubt on a borderline case, ask: *"This looks complex — want me to run it through prompt-optimizer first, or just go?"* One sentence, then proceed based on the answer.

## Workflow

### 1. Parse intent

Read the user's raw ask and extract:
- **Core task** — the verb. What do they want produced?
- **Implicit role** — is there a clear persona that would sharpen the answer? (e.g., "senior security reviewer", "Postgres DBA", "technical writer for non-technical audience")
- **Context already provided** — files, prior decisions, constraints they mentioned.
- **Output format** — did they specify? (markdown table, JSON, code only, a doc, etc.)
- **Examples** — did they include any input→output pairs?
- **Constraints / non-goals** — things to avoid, scope limits.
- **Success criteria** — how will they know the answer is good?

### 2. Identify gaps

List what's *missing* that would materially improve the output. Be selective — don't demand fields the task doesn't need. A code-refactor ask probably doesn't need a "persona"; a tone-sensitive writing ask probably does.

### 3. Handle missing examples (for complex tasks)

If the task is complex and examples would meaningfully help (classification, transformation, style-matching, structured extraction), ask the user **once**, in a single message:

> Examples would sharpen this. Three options:
> **a)** You provide 1–2 input/output examples.
> **b)** I generate plausible examples and you sanity-check them.
> **c)** Skip — proceed without examples.

Don't badger. If they pick (c), move on.

For non-example gaps (output format, constraints, role): make a reasonable default, mark it explicitly in the draft so the user can see and override at validation. Don't pepper them with questions.

### 4. Build the optimized prompt

Use this XML scaffold. **Omit tags that don't apply** — empty tags are noise. Order matters: role → context → task → examples → format → constraints. Claude reads top-down and weights later instructions more heavily for *how* to execute, so put format/constraints near the end.

```xml
<role>
[Only if a persona meaningfully changes the answer. One sentence.]
</role>

<context>
[Background, files, prior decisions, why this matters. Anything Claude
needs to know that isn't the task itself.]
</context>

<task>
[The actual ask, in imperative form. Be specific about the verb and the
deliverable. One or two sentences.]
</task>

<examples>
<example>
<input>...</input>
<output>...</output>
</example>
[Repeat for additional examples. 1–3 is usually enough.]
</examples>

<output_format>
[Exact structure expected: markdown table with these columns / JSON with
this schema / code block only / a doc with these sections. Be concrete.]
</output_format>

<constraints>
- [Hard rules: don't do X, must do Y, stay under Z tokens, etc.]
- [Non-goals: explicitly out of scope.]
</constraints>

<success_criteria>
[Optional. How the user will judge the result. Useful for ambiguous or
subjective tasks.]
</success_criteria>
```

**Style notes for the body:**
- Imperative voice ("Generate…", "List…", "Refactor…").
- Concrete > abstract. "List 5 risks ranked by severity" beats "think about risks".
- Explain *why* for non-obvious constraints — Claude follows reasoned rules more reliably than bare prohibitions.
- Inline references with `[[filename.md]]` or absolute paths the executor can read.

### 5. Validate with user

Show the assembled prompt in a code block and ask, in one short message:

> Here's the optimized prompt. Look good? (Reply "go" / edits / "scrap it".)

Don't over-explain — the prompt should speak for itself. If they reply with edits, fold them in and show the diff or the new version, then proceed.

### 6. Execute

Once approved, **act on the optimized prompt yourself** — don't paste it back to the user as if it were the deliverable. The optimized prompt is the *instruction set you now follow* to produce the real output.

## Why XML over JSON

For prompt structure, XML wins because:
- Tags nest cleanly and survive code/string content inside them without escaping.
- Claude is specifically trained to attend to XML-tagged structure.
- Edits are local — changing `<constraints>` doesn't risk breaking JSON syntax.

JSON is fine when the *output* needs to be machine-parseable. For the *prompt itself*, use XML.

## Anti-patterns

- **Don't structure trivial asks.** A `<task>Read file X</task>` prompt is worse than just reading file X.
- **Don't invent constraints the user didn't imply.** Defaults should be flagged so they can override.
- **Don't ask >1 clarifying question round.** Batch all gaps into one message, propose defaults for the rest.
- **Don't make the user approve a prompt twice.** One validation pass. If they edit, apply and go.
- **Don't keep the scaffold rigid.** If `<role>` or `<examples>` doesn't help this specific ask, drop the tag.

## Example transformation

**Raw ask:**
> can you look at my auth code and tell me whats wrong with it, its in src/auth and i think theres something off with how tokens are being stored

**Optimized prompt (after parse + one gap-question about output format, user said "markdown bullets, ranked"):**

```xml
<role>
You are a security-focused senior engineer reviewing authentication code.
</role>

<context>
The user suspects an issue with how tokens are stored in the auth module
at src/auth/. They haven't pinned down the specific bug — this is an
open-ended audit, not a fix request.
</context>

<task>
Read all files under src/auth/ and identify security or correctness
issues, with special attention to token storage (where tokens are kept,
how they're encrypted/scoped, lifetime, exposure to logs or other code).
</task>

<output_format>
Markdown bulleted list, ranked from highest to lowest severity. For each
issue: file:line reference, one-line description, and one-line suggested
fix direction (not the actual code).
</output_format>

<constraints>
- Don't write any code changes — this pass is review-only.
- If something looks suspicious but you can't confirm without more
  context (e.g., how a value flows into auth from elsewhere), flag it
  as "needs verification" rather than asserting it's broken.
</constraints>
```

The user sees that, says "go", and execution proceeds against the structured version — which will produce a sharper, more navigable answer than acting on the raw ask.
