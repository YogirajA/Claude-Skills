---
name: qa-deck
description: QA pass on a PowerPoint deck. Renders every slide and checks it for visual defects and fabricated facts. Use when the user asks to QA or check over a .pptx, and proactively before a deck is delivered or after its slides are edited.
---

# QA Deck

A rigorous two-track QA pass for a PowerPoint deck:

- **Visual track**: render every slide to an image, run a fresh-eyes subagent against a deep defect catalog, fix, re-render, re-verify until clean.
- **Content track**: extract every verifiable claim (numbers, names, dates, quotes, technical specs) and check each one against the source material the deck was built from. Flag fabrications, paraphrase drift, and outdated facts.

The visual and content tracks are independent failure modes. Decks routinely ship with one or the other broken even when the slide looks fine on a first pass, which is why this skill insists on both.

## When to invoke this skill

Use whenever the user wants confidence a deck is correct before it goes out the door. Triggers include:

- Explicit: "QA this deck", "review the slides", "audit the pptx", "/qa-deck", "is this deck ready", "tear it apart"
- Implicit: after generating or editing slides, before client delivery, after merging multiple decks, after a content rewrite, before printing or exporting to PDF

Use proactively right after generating a non-trivial deck. Do not wait for the user to ask.

## The four-phase workflow

### Phase 1: Setup and render

Establish:

- **Deck path**: the `.pptx` the user wants checked. If multiple files are open in the conversation, confirm which one.
- **Source documents** (optional but strongly preferred for the content track): any files, decks, transcripts, web pages, or notes the deck was built from. Ask the user explicitly if not obvious. Without sources, the content track degrades to "flag claims that LOOK verifiable" instead of "verify each claim".
- **Workspace**: a temp directory for renders. Default: `<deck_dir>/.qa-deck-workspace/<timestamp>/`.

Render every slide to a JPG at ~150 dpi.

```bash
python "${SKILL_DIR}/scripts/render_slides.py" <deck.pptx> <workspace>/slides
```

This script handles LibreOffice → PDF → per-slide JPG conversion and works on Windows, macOS, and Linux. If it errors, fall back to running `soffice --headless --convert-to pdf` and then `pdftoppm` or `PyMuPDF` directly.

Also extract the deck's text content for the content track:

```bash
python -m markitdown <deck.pptx> > <workspace>/deck.md
```

### Phase 2: Visual QA (subagent pass)

Spawn a **fresh** subagent. The current model already has expectations about what the deck should look like from generating it; only a model that has not seen the generation can give honest visual feedback.

Hand the subagent the rendered images and the full defect catalog from `references/visual-defects.md`. Use the prompt template in `references/visual-qa-prompt.md`.

Ask the subagent to:

1. Assume issues exist. Look for them, do not confirm.
2. Group findings per slide by severity: Blocking, Important, Minor, Nit.
3. Quote rough coordinates so issues can be re-located.
4. Explicitly note clean slides ("clean for client delivery") to avoid silent passes.
5. Keep total response tight (under 600 words for an 8-slide pass, scale linearly).

### Phase 3: Content / hallucination QA

This is the part most decks fail and most QA passes skip. Decks contain three classes of risky content:

- **Sourced claims**: pulled from a specific source document the user provided
- **Public claims**: pulled from public knowledge (customer case studies, model specs, public announcements)
- **Inferred claims**: paraphrases, summaries, or extrapolations the model wrote that may have drifted from the source

For every verifiable claim in the deck, check it. Read `references/hallucination-checks.md` for the full taxonomy and verification protocol. The high-level move:

1. Extract every claim from `<workspace>/deck.md` that has a specific number, named entity, date, quote, or technical spec.
2. For each claim, find the source. If sources were provided, grep them. If not, use WebFetch / WebSearch with caution and ALWAYS cite the URL you verified against.
3. Tag each claim: **Verified**, **Wrong**, **Unverifiable**, **Stale** (true but outdated), or **Drift** (close but paraphrased imprecisely).
4. Produce a content findings table.

**Pay special attention to:**

- Customer case study stats (e.g., "80 percent faster", "650+ PRs/month"): these are the most-fabricated category
- Model names and versions (Claude 4.6 vs Claude 4.7, Haiku/Sonnet/Opus assignments)
- Dates and timeframes ("Q4 2025", "by Thursday", "next quarter")
- Product names spelled exactly (CLAUDE.md not Claude.md, MCP not MPC)
- Direct quotes attributed to people or companies
- Statistical claims (percentages, multipliers, "X times faster")
- Source citations and URLs (every URL must resolve, every source must exist)

### Phase 4: Synthesize, fix, re-verify

Combine visual + content findings into one prioritized report. Order by severity, then by slide number. For each Blocking and Important issue, propose a concrete fix.

If the user asks for fixes, apply them, then **rerun Phase 1 and Phase 2** on the affected slides. Do not declare the deck done until a fresh subagent pass on the fixed slides returns clean. One fix often introduces a new defect; the loop is mandatory until clean.

If only minor / nit issues remain, ask the user whether to fix or ship as is.

## Output format

Deliver findings as a single report with this structure:

```
# QA report: <deck name>

## Summary
- N slides inspected
- M visual issues (B blocking, I important, m minor, n nit)
- K content issues (W wrong, U unverifiable, D drift, S stale)
- Verdict: <Ready / Fix before ship / Major rework>

## Visual findings
### Slide N — <title>
- **Blocking**: <issue> (location)
- **Important**: <issue> (location)
- ...

## Content findings
| Slide | Claim | Status | Source | Note |
| ...

## Recommended fixes
1. <concrete action>
2. ...
```

Lead with the verdict. Executives skim summaries; details only if the verdict is concerning.

## What this skill does NOT do

- It does not rewrite the deck unprompted. Apply fixes only when the user asks.
- It does not pass judgment on narrative strength, tone, or persuasiveness. Those are subjective and belong to the human reviewer.
- It does not check legal, brand, or compliance language unless the user provides the relevant guidelines as source documents.

## Common false positives to avoid

- **"Empty space below content"** is not always a defect. Cover slides, section dividers, and big-stat slides are intentionally airy. Only flag when content is clearly truncated or when a card has a top-anchored body AND a bottom-anchored footer with a >0.8" gap between them.
- **"Title and body misaligned"** is correct ONLY if the title's left edge differs from the body's left edge with no semantic reason. Indented body under a centered title is intentional.
- **"Customer name not in my training data"** does not mean fabricated. Verify with WebFetch before flagging.
- **Off-by-one slide numbering** (e.g., page number is 5 but PowerPoint slide is the 6th because of a hidden slide) is not a defect; it is a config choice.

## Toolchain

- LibreOffice (`soffice`) for `.pptx` → `.pdf`
- PyMuPDF or `pdftoppm` for `.pdf` → JPG
- `markitdown` for `.pptx` → text
- Subagent (general-purpose) for the visual pass and optionally for the content pass
- WebFetch / WebSearch for verifying public claims

If LibreOffice or PyMuPDF are missing, install them or fall back to whatever the user's environment has. `scripts/render_slides.py` documents the fallbacks.

## Further reading

- `references/visual-defects.md`: the full defect catalog. Hand this to the visual-QA subagent verbatim.
- `references/visual-qa-prompt.md`: the subagent prompt template.
- `references/hallucination-checks.md`: claim taxonomy and verification protocol.
- `references/severity-rubric.md`: what counts as Blocking vs Important vs Minor vs Nit.
