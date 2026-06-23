---
name: mental-models
description: Pressure-test a real decision by running it through a curated library of mental models (inversion, second-order thinking, opportunity cost, expected value, base rates / outside view, regret minimization, reversible vs irreversible decisions, margin of safety, incentives, and more), then synthesize a decisive recommendation and the one thing that would change it. Use this whenever the user is weighing a real choice and wants rigorous thinking: "help me decide", "should I do X or Y", "I'm trying to figure out whether to...", "think this through with me", "apply mental models / first principles to this", "what's the smart way to look at this decision", or is stuck between options with real stakes. Complements the-llm-council (which stages a multi-persona debate); this skill instead applies named thinking frameworks. Trigger on genuine decisions even when the user never says "mental models" by name.
---

# Mental models for decisions

Run a real decision through a curated set of mental models - named thinking tools - to see it
from angles you'd otherwise miss, then commit to a recommendation. The value isn't reciting
models; it's that different models *disagree*, and the disagreement shows you where the actual
risk lives.

**How this differs from `the-llm-council`.** The council stages five personas who debate and a
Chairman who rules. This skill instead applies named frameworks (inversion, expected value,
second-order effects, and so on) to the same facts. Use this when you want disciplined solo
reasoning; use the council when you want clashing perspectives. They stack fine - run the
models first, then escalate a big or contested call to the council.

**Be decisive.** Like the council, this ends with one direction the user can act on, plus the
single thing that would change it. Listing considerations and handing the choice back is a
failure - the user already had considerations; they came for a call.

## Step 1 - Frame the decision

Pin down, briefly:

- The **actual decision** (one sentence) and the **real options** - including "do nothing /
  wait," which is always on the table.
- **Constraints**, and what a **good outcome** looks like.
- **Stakes** and **reversibility** - is this a one-way door (hard to undo, high stakes) or a
  two-way door (cheap to reverse)? This sets how much rigor is warranted.
- **Time horizon.**

If the options or success criteria are fuzzy, sharpen them before applying models. Models
applied to a vague question give vague answers.

## Step 2 - Select the 4-6 most relevant models

Relevance beats completeness. Applying all of them is noise; pick the few that bite on *this*
decision and say why you chose them. The library (each shown as the question it forces):

**Framing**
- **Inversion** - what would guarantee failure here? Then avoid that.
- **First principles** - strip to what's actually true; what are we assuming?
- **Circle of competence** - is this inside what we genuinely understand?

**Consequences over time**
- **Second-order thinking** - "and then what?" Two, three steps out.
- **Opportunity cost** - what's the best thing we give up by choosing this?
- **10/10/10** - how will this feel in 10 minutes, 10 months, 10 years?
- **Compounding** - does this small effect snowball if repeated?

**Under uncertainty**
- **Expected value** - payoff x probability across outcomes, not just the hoped-for one.
- **Base rates / outside view** - how do situations like this *usually* go? Start there, not
  from the inside story.
- **Margin of safety** - does it survive being wrong by a comfortable margin?
- **Asymmetry / convexity** - is the downside capped and the upside large (or the reverse)?

**Reversibility & action**
- **One-way vs two-way doors** - reversible decisions deserve speed, irreversible ones deserve
  care.
- **Regret minimization** - at the end, which choice do you least regret not taking?
- **Via negativa** - is the move to *remove* something rather than add?
- **Sunk cost** - ignore what's already spent; decide on what's ahead.

**Bias & incentive checks**
- **Incentives** - "show me the incentive and I'll show you the outcome." Who benefits?
- **Confirmation bias** - what evidence are we discounting because we don't like it?
- **Occam / Hanlon** - prefer the simpler explanation; don't assume malice where ordinary
  causes fit.

## Step 3 - Apply each selected model

For each, produce a *specific insight about this decision*, not a definition. One tight
paragraph or bullet each. The output of a model is a sentence the user couldn't have written
before applying it.

## Step 4 - Read the agreements and conflicts

Where do the models point the same way? Where do they pull apart? The conflict is the signal -
for example, expected value says go while margin of safety says the downside is ruinous. Name
that tension explicitly; it's usually the crux.

## Step 5 - Synthesize a decision

End with:

```
## Recommendation
<one clear direction>

## Why
<the 2-3 models that carried the most weight, and the key tension>

## What would change this
<the single piece of new information or condition that would flip the call>
```

Keep it honest: if the decision is genuinely close, say which way you'd lean and exactly what
tips it, rather than faking certainty.
