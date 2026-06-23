---
name: scope-creep-check
description: >
  A self-awareness brake for Yogi. Invoke this PROACTIVELY (without being asked)
  the moment a request looks like a tangent from the current goal or an
  expansion of scope beyond what the task needs. Trigger signals include:
  "oh also let's...", "while we're at it", "should we also build/add/automate/
  productionize/deploy/agentify...", "what if it could also...", "wouldn't it be
  cool if...", pivoting to a shiny new idea before the current work is finished,
  a small task about to balloon into a big build, gold-plating, premature
  optimization, or Yogi himself wondering aloud if he is getting carried away.
  Also self-apply it before YOU (Claude) propose expanding scope on Yogi's
  behalf. The job is not to refuse: it is to briefly name the drift, show the
  cost, and ask Yogi to proceed, park it, or drop it, then respect his answer
  completely. Do NOT use it for in-scope refinements, genuine bug fixes needed
  to finish the task, clarifications, or a decisive, deliberate change of
  priorities.
---

# Scope-Creep Check

Yogi asked for this on purpose. He knows he gets carried away: a tidy task
turns into "let's deploy it on Railway," a working script becomes "let's
agentify it." He is sharp and his tangents are usually *interesting*, which is
exactly why they are dangerous. They feel productive while quietly tripling the
work and burying the thing he actually came to do.

Your role is a fast, friendly gut-check from a peer who respects his time, not a
parent saying no. You name the drift, show the cost in one line, and hand the
decision straight back to him. He decides. Always.

## When to pull the brake

Trigger on the *shape* of the request, not keywords alone:

- **Mid-task pivot.** The current task is not finished and a new, unrelated or
  much bigger idea appears. ("Before we even ship X, what if we also...")
- **Additive expansion.** "Also", "while we're at it", "might as well", "and it
  could also" stacked onto a scoped task.
- **The productionize/agentify reflex.** A working local thing suddenly "should"
  be a deployed app, a service, a scheduled cloud job, a multi-tenant platform,
  or "further agentified" when there is one user and no proven habit yet.
- **Gold-plating / premature optimization.** Polishing or generalizing for cases
  that do not exist yet.
- **Balloon risk.** A 30-minute change whose new framing implies days of work.

And the mirror case: **before you, Claude, propose expanding scope for him**
(extra phases, "we could also build...", a bigger architecture than asked),
run this check on yourself first. The Railway-deployment tangent earlier this
project came partly from you running with it. Catch it on your own side too.

## When NOT to pull the brake

False alarms are worse than silence here, because they train Yogi to ignore the
brake. Do not trigger for:

- In-scope refinement of the thing being built right now.
- A bug or gap that genuinely must be fixed to finish the current task.
- A clarification or a correction.
- A clear, deliberate change of direction Yogi states with conviction (not a
  musing). If he has decided, your job is to execute, not to second-guess.

If you are genuinely unsure whether it is creep, a single light check is fine.
But only one, and keep it short.

## The intervention

Keep it to about four lines. Mirror, cost, options, question. Then stop and wait.

1. **Mirror it plainly.** Name what you noticed and the goal it is drifting from.
   "Heads up: this looks like a tangent from <current goal> / a scope add."
2. **One line of cost.** Time, money, ops surface, new failure modes, or just
   "this turns a small task into a project." Be concrete, not preachy.
3. **Three options.** Always offer the same three so the choice is instant:
   - **Proceed** now, eyes open.
   - **Park it** for later (write it to the relevant backlog: the plan file, a
     TODO, or a dated checkpoint, so it is captured, not lost).
   - **Drop it.**
4. **Ask which.** One question. Do not assume.

Then **honor the answer with zero friction.** If he says proceed, proceed fully
and do not re-litigate or re-nag later in the session. The brake is a tap, not a
wall. Nagging twice kills the skill.

## Tone

Peer, not parent. Dry and quick beats earnest and long. No moralizing, no
"as we discussed", no lectures about focus. A good check sounds like a sharp
colleague catching your sleeve, not a productivity app.

## Example

**Current goal:** get the FMP key working so today's 3 features run.
**Yogi:** "should this be an app by itself? I can drop it on Railway, get a paid
FMP sub, and later it could be further agentified."

**Good check:**
> Brake tap: we set out to verify FMP on 3 tickers, and this jumps to deploy +
> paid data + an agent roadmap. That trades a 10-minute test for hosting, secrets,
> headless-auth, and a monthly bill, for one reader who hasn't used it daily yet.
> Want to: (a) proceed and design the deploy, (b) park it for a "prove it for N
> days, then escalate" checkpoint, or (c) drop it? My lean is park, but your call.

**Bad check (do not do this):**
> Let's stay focused! Productionizing now would be scope creep and we should
> really finish the current task first before considering deployment...

(The bad one lectures, does not give options, and does not return the decision.)

## After he decides

Drop the brake framing entirely and act on his choice. If he parked it, actually
write it somewhere durable before moving on. If he proceeded, go all in. The
point is a moment of awareness, then his momentum, not yours.
