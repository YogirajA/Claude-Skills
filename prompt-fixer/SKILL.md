---
name: prompt-fixer
description: Cleans up a rough, vague, or underspecified prompt the user wrote into a clear, well-structured prompt in plain English (no XML, no tags), then hands it back to read, paste, and edit rather than executing it. Adds the four things most prompts miss, a persona, an unambiguous task, two or three examples where they help, and explicit constraints. Use whenever the user shares a prompt and wants it tightened, fixed, sharpened, polished, cleaned up, de-jargoned, made more precise, or made to produce less vague or inconsistent output, usually a short rough one (e.g. 'classify each lead as hot/warm/cold', 'review my script and tell me whats wrong', 'write a cold email to a VP'), or wants a solid reusable prompt as the takeaway from a brainstorm even if they do not say "fix this prompt." This is the default for plain-English prompt cleanup. Do NOT use when the user wants the prompt wrapped in XML or wants Claude to then run it (that is the prompt-optimizer skill), or for editing ordinary prose, emails, messages, or data files.
---

# Prompt Fixer

Take a rough prompt and return a tightened version. The job is mechanical and fast: diagnose what is missing, add it, and hand back a clean prompt the user can paste straight into a model. Do not over-engineer. A good fix is the smallest set of additions that removes ambiguity.

The output is **plain English**, not XML. You hand the improved prompt back for the user to read, paste, and edit themselves. You do not execute it. If the user wants an XML-structured prompt, or wants Claude to run the prompt for them, that is the **prompt-optimizer** skill, not this one. This skill owns plain-English hygiene; prompt-optimizer owns the XML-and-execute lane.

## The four checks

Run every prompt through these four checks, in order. Add only what is actually missing. Never pad a prompt that is already specified on a given dimension.

1. **Persona.** If no role is set, set one. Pick the persona that a competent human would assign to this task (e.g. "You are a senior Python engineer," "You are a fixed-income analyst"). One sentence. Skip if the user already framed a role.

2. **Task clarity.** Restate the actual ask as a single unambiguous instruction. Resolve vague verbs ("look at," "deal with," "handle") into concrete ones ("rank," "rewrite," "extract," "classify"). State the deliverable and its format explicitly. If the original prompt buries the real ask under context, surface it to the top.

3. **Examples.** Add two or three input/output examples only when they sharpen the task, which is the usual case for classification, formatting, tone-matching, extraction, and transformation work. Skip examples for open-ended generative or reasoning tasks where they would narrow the output too much. When you add them, keep them short and representative, and cover at least one edge or tricky case rather than three easy ones.

4. **Constraints.** Add the constraints that keep the output usable: length, format, what to include, what to exclude, tone, and any hard "do not" rules. Pull constraints from context the user already gave rather than inventing arbitrary limits. If the task has an obvious failure mode (hallucinated facts, wrong format, too long), add a constraint that guards against it.

## Output format

ALWAYS respond in this exact structure:

```
**Fixed prompt**

<the rewritten prompt in plain English, ready to paste>

---

**What changed**
- Persona: <what you added, or "already set">
- Task: <how you sharpened it, or "already clear">
- Examples: <added N, or "skipped because ...">
- Constraints: <what you added, or "already specified">
```

Keep the "What changed" section to one line per check. The user wants the fixed prompt first and the rationale second. Do not lecture.

## Principles

- The fixed prompt must be self-contained. Someone who never saw the original should be able to use it.
- Keep it plain English. No XML tags, no JSON scaffolding. If structure helps, use plain headings and bullets the user can read at a glance. (XML structuring is prompt-optimizer's job.)
- Preserve the user's intent exactly. You are tightening, not redirecting. If the original is ambiguous between two readings, pick the more likely one and note the assumption in a single line under "What changed."
- Match the domain. For fintech, telecom, and agent-building prompts, default to a domain-expert persona and add correctness or grounding constraints, since those are the common failure modes.
- Do not add examples, constraints, or persona that fight the task. A persona on a pure-math prompt adds nothing; examples on a brainstorm kill divergence. Restraint is part of the fix.
- If the prompt is genuinely already good, say so in one line and return it mostly unchanged rather than manufacturing edits.

## Example

**Input prompt from user:**
> summarize these support tickets and tell me whats going wrong

**Fixed prompt:**

```
You are a support operations analyst.

Read the support tickets below and produce a summary that identifies the top recurring issues. For each issue, give: a short label, the number of tickets it appears in, and one representative quote.

Then list the single most likely root cause for the top issue.

Format:
## Top issues
1. <label> (<count> tickets) - "<quote>"
...
## Likely root cause
<2-3 sentences>

Constraints:
- Base every claim on the tickets provided. Do not infer issues that are not present in the text.
- Keep the whole response under 300 words.
- If fewer than 3 distinct issues exist, report only the ones you find.

Tickets:
<paste tickets here>
```

**What changed**
- Persona: added "support operations analyst"
- Task: turned "tell me whats going wrong" into a ranked-issues summary plus a root-cause call
- Examples: skipped, the output format spec carries the load here
- Constraints: added grounding rule, word limit, and a graceful-degradation rule for sparse data
