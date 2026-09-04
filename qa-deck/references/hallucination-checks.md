# Content / hallucination check protocol

This is the part most deck QA passes skip and most decks fail. The visual pass catches whether the slide LOOKS right; this pass catches whether the slide IS right.

## The claim taxonomy

For each slide, extract every claim that could be true or false. Categorize as:

1. **Numbers**: percentages, counts, durations, multipliers, dollar amounts, ratios. ("80 percent faster", "650+ PRs/month", "30,000 practitioners", "5-minute TTL".)
2. **Named entities**: companies, products, people, places. ("Ramp", "Novo Nordisk", "Claude 4.7", "Anthropic Skilljar".)
3. **Dates and timeframes**: calendar dates, fiscal periods, deadlines, "since X". ("Q4 2025", "Effective 13 April 2026", "by Thursday", "24 working days".)
4. **Technical specs**: version numbers, model names, configuration values, file paths, command names. ("Sonnet 4.6", "WSL2", "claude doctor", "/status", "19 approved MCP servers".)
5. **Direct quotes**: anything in quotation marks or attributed to a person or company.
6. **Statistical claims**: "X times faster", "Y percent of organizations", "the average team", "median time".
7. **Source attributions**: URLs, citation footers, "Source: X". Every URL must resolve; every cited source must exist.
8. **Causal claims**: "because X", "driven by Y", "X led to Y". Easy to drift on.
9. **Comparison claims**: "more than", "less than", "fastest in industry". Comparatives are frequently wrong even when the underlying number is right.
10. **Pricing or commercial claims**: package pricing, license costs, "free", "included". High-risk if outdated.

## Where claims come from (and where they go wrong)

- **Sourced**: pulled from a specific source document. Most reliable when the source is fresh. Verify by grep / read of the source.
- **Public**: pulled from public knowledge. Verify with WebFetch. Cite the URL.
- **Inferred / paraphrased**: the model rewrote a source claim. This is where drift happens most often. ("Sharply higher" became "doubled". "Up to 90 percent" became "90 percent".)
- **Fabricated**: no source. Pure hallucination. The customer name is real but the stat is invented, or the stat is right but attributed to the wrong customer.

## Verification protocol

For each claim:

### Step 1: locate the source

If the user provided source documents, grep the source for the key number, name, or phrase. Use the most distinctive token in the claim (the specific number, the customer name + metric, the exact phrase).

```bash
grep -i "80 percent" sources/*.md sources/*.pptx.md
grep -i "Ramp" sources/*
```

If no source document, search public knowledge. For customer case studies, the authoritative source is `claude.com/customers/<name>` or `anthropic.com/customers/<name>`. For model specs, `docs.claude.com` or `anthropic.com`. For partnership announcements, `newsroom.accenture.com` or `anthropic.com/news`.

Use WebFetch on the specific URL the deck cites. If the deck does not cite a URL, search and pick the most authoritative source.

### Step 2: compare exactly

Numbers must match exactly. "80 percent" is not "80%" (style, fine) but "80 percent" is NOT "approximately 80%" (drift) and is NOT "85 percent" (wrong). Dates must match (year, month, and day if the deck specifies it). Names must spell exactly (case sensitive for product names like CLAUDE.md, MCP, WSL2).

For quotes, the wording must be exact OR the deck must indicate it is a paraphrase (italics, "paraphrased", "in essence").

### Step 3: tag the claim

- **Verified**: claim matches the source exactly. No action needed.
- **Wrong**: claim contradicts the source. Highest severity. Must fix.
- **Unverifiable**: no source could be found. Highest risk. Either find a source, soften the claim, or remove it.
- **Stale**: the claim was true at some point but the source has since updated. Common with model versions, pricing, and partnership stats. Update.
- **Drift**: close to the source but paraphrased imprecisely. Common low-severity issue. Either tighten or mark as paraphrase.

### Step 4: report

Use a single content findings table:

| Slide | Claim | Status | Source | Note |
|-------|-------|--------|--------|------|
| 3 | "30,000 practitioners trained" | Verified | newsroom.accenture.com/anthropic-partnership | Exact match |
| 5 | "Anthropic Skilljar Claude 101" | Verified | anthropic.skilljar.com/claude-101 | URL resolves |
| 7 | "5-minute TTL" | Wrong | docs.claude.com/en/docs/build-with-claude/prompt-caching | Doc says 5 min default, but configurable up to 1 hour |
| 9 | "650+ PRs / month" (Spotify) | Verified | claude.com/customers/spotify | Exact match |
| 14 | "Q4 2025 launch" | Stale | press release dated 2026-01 | Launched earlier than Q4 |

Lead with **Wrong** items. Those block ship.

## High-risk claim categories

These are the categories that fail most often in real decks. Audit them with extra care:

### Customer case study statistics

Customer stats are the single most-fabricated category. The model often gets the customer name right and the metric category right but invents the specific number, or swaps numbers between customers (Ramp's stat attributed to Rakuten).

Always verify against the customer's official case study page. For Anthropic customers, that's `claude.com/customers/<name>` or `anthropic.com/customers/<name>`. The exact URL is usually in the deck footer; if not, search.

### Model names and versions

The model family is fast-moving. A deck referencing "Claude 4.6" may have been correct three weeks ago and wrong today. Verify model version, family name, and capability claims against `docs.claude.com` or the latest Anthropic announcement.

Common errors:
- Right model family, wrong version (Sonnet 4.5 vs Sonnet 4.6)
- Right version, wrong capability (Haiku does not do X, Sonnet does)
- Mixing up Haiku / Sonnet / Opus assignments in a "model routing" section

### Dates and timeframes

"Effective 13 April 2026", verify against the source document's actual effective date. "Singapore session Friday 20 March", verify against the event invite or planning doc, including the year.

Relative dates ("by Thursday", "next quarter") become wrong as time passes. Flag them and convert to absolute dates where possible.

### Technical specs and command names

PowerPoint slides routinely contain wrong command syntax, wrong filenames, wrong flag names. Examples to look for:
- `CLAUDE.md` not `Claude.md` (case sensitive)
- `claude doctor` not `claude --doctor`
- `/status` is a slash command, runs inside a session, not a CLI flag
- MCP server names exactly as approved in V21 managed settings

### URLs and source citations

Every URL on a slide must resolve. WebFetch each one, or at minimum check the domain is real and the path looks plausible. Common failures:
- Made-up `claude.com/research/agentic-rollouts` style URLs that don't exist
- Real domain, wrong path
- Real URL but the underlying page has moved or been deleted

### Quotes attributed to people

Direct quotes are nearly always either real-and-cited or fabricated. There is rarely an in-between. If the deck has a quote, either find it in a published source (interview, press release, customer case study, internal transcript) or flag it as Unverifiable.

## Working WITHOUT source documents

If the user did not provide source documents:

1. Ask once. ("Do you have the source decks or notes this was built from? I can verify claims more confidently with them.")
2. If still none, do a best-effort pass using public sources:
   - WebFetch the URLs the deck cites
   - Search for the most distinctive claims
   - Flag anything that looks made-up but cannot be verified one way or the other
3. Be explicit in the report: "Verified using public sources only. <N> claims could not be sourced and are tagged Unverifiable. Treat the Unverifiable list as the highest-priority audit before ship."

## Working WITH source documents

If the user provided source documents:

1. Index them once. Read each one to get a feel for what's there.
2. For each claim, grep the source. If multiple sources, grep all of them.
3. If a claim does not appear in any source, that is itself a finding: either the claim was inferred (drift risk) or fabricated.

The "claim does not appear in any source" finding is the most valuable single check this skill can run. Insist on it.

## What is NOT a hallucination

- **Reasonable paraphrase** of a source statement, with no number or named entity drift, is not a hallucination. ("Demonstrated significant gains" rephrasing "Showed substantial improvement" is fine.)
- **Stylistic rewrites** ("80%" → "80 percent") are not hallucinations as long as the value is preserved.
- **Generic industry truisms** that don't claim a specific source ("Software teams adopting AI ship more code") are not hallucinations even though they aren't directly sourceable.
- **Forward-looking statements** clearly marked as such ("We expect", "We plan to") are not hallucinations even if they aren't yet verifiable.

Focus the audit on specific, verifiable, falsifiable claims. Don't waste cycles flagging that "the agentic era is here" cannot be sourced.
