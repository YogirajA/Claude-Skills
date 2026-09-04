---
name: field-guide-builder
description: Use when building or extending a single-file, source-grounded, visually distinctive teaching guide on a technical topic, the kind with a concept hierarchy of worked examples and do/avoid practice, inline citations to primary sources, an editorial design system, an in-app router, and an optional interactive companion. Triggers on requests like "build a guide", "make a teaching guide / explainer / field guide / learning doc", or polishing and extending one.
disable-model-invocation: true
---

# Field guide builder

Build the kind of guide we build: one self-contained HTML file that teaches a technical topic to a high standard, with **distinctive design, rigorous sourcing, and one consistent teaching hierarchy**. Optionally ship an interactive companion (a step-through "session") next to it. The canonical instance this skill was distilled from is a prompting guide, but the recipe is topic-agnostic.

This file is the recipe. The details live in reference files; load only the one the current phase needs (that is the same progressive-disclosure principle these guides teach):

- `references/design-system.md` , palette, fonts, the masthead seal, component CSS, atmosphere, motion.
- `references/structure-and-router.md` , the concept hierarchy, deep-dive pages, nav, hash router, search, citations.
- `references/sourcing-and-qa.md` , primary-source rigor, the parallel-agent hallucination audit, the QA checklist.
- `references/interactive-companion.md` , the conversation-starters / step-through session pattern.
- `assets/qa.py` , run against the finished file to check em dashes, citation integrity, and links.

## The four pillars (what makes it "this kind of guide")

1. **Single file.** One `.html`, no build step, inline `<style>` and `<script>`, web-font links only. It opens anywhere and is trivially shareable.
2. **Source-grounded.** Every concrete claim (number, date, feature, behavior, quote) traces to a **primary source**: official docs, the vendor's engineering blog, a named conference talk, or the creator's own words. Secondary blogs may support a claim but never anchor it. No invented stats or features. Cite inline with `[N]` linking to a references list.
3. **One teaching hierarchy, everywhere.** Each concept is a card: a one-line definition, then **Example** (2 good + 1 bad, worked) and **In Practice** (Do / Avoid). Heavy concepts also get full deep-dive pages for each half, reached through an in-app router. Same shape for every concept, no exceptions.
4. **Editorial, not generic.** A committed visual identity (a distinctive display font paired with a refined body font, one dominant color with sparing accents, real atmosphere, and a signature mark), never framework defaults or "AI slop". See the design system.

## Build workflow

Work in phases. Do not try to do it all at once.

1. **Scope and source-gather first.** List the concepts. For each, find the primary source and pull the exact facts (quotes verbatim, numbers exact, dates exact). Keep a source map as you go. If a claim cannot be sourced, cut it or mark it plainly as an illustrative example.
2. **Lay down the design system.** Drop in the tokens, fonts, masthead, and base components from `design-system.md`. Make the empty shell look finished before pouring in content.
3. **Build the structure.** Add the nav, the hash router, and one concept card plus its two deep-dive pages as a template (`structure-and-router.md`). Verify routing in a browser before scaling.
4. **Fill content, concept by concept.** Reuse the card + deep-dive template per concept. Color-code by category. Keep every Example at 2 good / 1 bad, every In Practice with concrete Do/Avoid items and a routing table.
5. **Audit for hallucinations.** Extract every claim and verify it against the live primary source. For a large guide, fan out parallel research agents over claim-clusters (one per section group) to flag anything unverifiable or embellished, then fix. See `sourcing-and-qa.md`.
6. **QA and ship.** Run `assets/qa.py`. Verify routing, search, every citation resolves, every anchor resolves, and motion respects reduced-motion. Optionally build the interactive companion (`interactive-companion.md`).

## Non-negotiables

- No em dashes anywhere (use commas, colons, parentheses, or restructure). En dashes are fine for ranges. QA before declaring done.
- Every `[N]` citation resolves to a real reference; every internal `#anchor` resolves both ways.
- No claim without a source. Verbatim quotes are actually verbatim. Numbers and dates are exact, not "about right".
- Distinguish a factual claim (must be true) from an illustrative example (a made-up snippet that demonstrates a real concept is fine; an invented statistic is not).
- One consistent teaching hierarchy across all concepts.
- Animations gated behind `prefers-reduced-motion`, with at most one tiny deliberate exception you can justify.
- Verify in a real browser (local server + a headless check), not by eye alone.

## House rules

Honor the user's stated writing preferences (for this user: never em dashes; en dashes only for numeric or date ranges). When extending an existing guide, read its tokens and conventions first and match them exactly rather than introducing a second style.
