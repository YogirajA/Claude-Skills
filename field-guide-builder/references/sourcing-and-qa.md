# Sourcing and QA

The thing that makes these guides trustworthy is that **every concrete claim is true and traceable**. A beautiful guide full of plausible-but-wrong feature claims is worse than useless. Treat sourcing as a first-class phase, not an afterthought.

## Sourcing rules

- **Primary sources anchor; secondary sources only support.** Primary: official docs, the vendor's engineering blog, a named conference talk, the creator's own posts/quotes. Secondary: community blogs, aggregators. A claim may cite a secondary source for color, but if a feature/number/date rests *only* on a secondary blog, either confirm it against a primary source or soften it.
- **Verbatim quotes are verbatim.** Fetch the actual source and match wording exactly. A condensed paraphrase must not be wrapped in quotation marks.
- **Numbers and dates are exact.** "About 40 turns" invented as a fixed cadence is a hallucination; "as it nears the limit" is honest. Pull the real figure or do not state one.
- **Separate claims from illustrations.** An invented code snippet or scenario that *demonstrates* a real mechanism is fine. An invented statistic, feature name, or attribution is not. When in doubt, mark a figure as illustrative.
- **Make the tier visible.** Label secondary references as "secondary" in the reference list so the reader sees the sourcing strength.

## The hallucination audit (do this before shipping)

1. **Extract every claim.** Walk the guide and list every number, date, feature/behavior assertion, attribution, and quote.
2. **Verify each against the live primary source.** Fetch the actual page/talk; compare. Watch the high-risk spots: very specific stats, future-ish dates, verbatim quotes, "X always does Y" feature claims, and anything you authored as a "general pattern".
3. **Fan out for scale.** For a large guide, dispatch parallel research agents, one per cluster of sections, each told: read these passages, extract every factual claim, verify against this allow-list of primary sources (with web access), and return a structured list: `[SEVERITY] line N , CLAIM , VERDICT (confirmed | contradicted | unverifiable | invented | only-secondary) , EVIDENCE , FIX`. Tell them NOT to edit the file, only report. Tell them to also list "CONFIRMED OK" high-stakes claims so you know they were checked.
4. **Verify suspicious corrections yourself** before applying sweeping changes. If an agent says a core claim is backwards, fetch the primary doc and confirm the exact wording yourself, then fix every instance.
5. **Re-ground, do not just delete.** When a claim was real but cited to a secondary blog, add the primary source as a new reference and re-cite. When a general pattern is not in your named talk, find the vendor's canonical doc for it (most "patterns" have an official home) and cite that, rather than leaving it unsourced.

### Agent prompt skeleton

```
You are a skeptical fact-checker auditing <FILE>. Audit ONLY lines A-B (sections X, Y, Z).
ALLOWED PRIMARY SOURCES (verify against the LIVE pages with web access): <list of URLs>.
Flag: specific numbers/limits, feature/behavior claims, attributions, dates. Verify each.
Do NOT flag illustrative snippets that merely demonstrate a real concept.
Return ONLY: per issue ->
  [SEVERITY: HIGH/MED/LOW] line N , CLAIM: "..." , VERDICT: confirmed|contradicted|unverifiable|invented|only-secondary , EVIDENCE: <source + value> , FIX: <concrete edit>
Then a "CONFIRMED OK" list of high-stakes claims you checked and that hold. Do NOT edit the file.
```

## QA checklist (run before declaring done)

- `python assets/qa.py guide.html` , passes (em dashes 0, citations resolve, anchors resolve).
- Em dashes: zero (U+2014). Use commas, colons, parentheses, or restructure. (User rule; en dashes only for ranges.)
- Citations: every `[N]` resolves to an `id="ref-N"`; no dangling, ideally no orphans.
- Anchors: every internal `href="#..."` resolves to a matching `id`.
- Routing: each deep-dive page activates, the guide hides, the parent nav item re-highlights, scroll resets. Search ignores hidden pages.
- Motion: everything is gated behind `prefers-reduced-motion` (with at most one justified slow-decorative exception).
- Browser check: serve locally and verify in a headless browser, do not trust eyeballing the source.

## Local verification loop

```bash
python -m http.server 8765    # serve the folder
# then drive a headless browser:
#   navigate to the page and each deep-dive hash
#   assert: .doc-page.active present, #guide-view hidden, parent nav active
#   assert content thresholds (N worked examples, N do/avoid items)
#   take a screenshot to eyeball design, then clean up (kill server, remove temp files)
```

Always clean up after verifying: stop the server and delete any screenshots or scratch files you created.
