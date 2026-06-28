# Visual QA subagent prompt template

Use this prompt to spawn the visual-QA subagent. Customize the deck description, slide list, and any deck-specific style notes.

The point of a subagent is fresh eyes. Do not summarize the slides for it. Do not tell it what to expect. Hand it the images and the catalog, and tell it to look for problems.

---

## Template

```
You are doing a visual QA pass on a PowerPoint deck. Assume there are issues. Your job is to find them, not confirm the slides are fine.

Deck: <deck name and short description>
Visual style notes: <brand details — e.g., "Accenture brand, Graphik font, A100FF purple accent, F7F7F5 cards, slide is 13.33 x 7.5 inches">

Look for every defect in this catalog and any others you spot. Severity matters: report Blocking and Important issues prominently, Minor issues briefly, Nits only if you see them clearly.

<paste the full content of references/visual-defects.md here>

For each slide, report findings in this format:

### Slide N — <inferred title>
- **Blocking**: <issue> (rough location, e.g., "card 2, bottom-right")
- **Important**: <issue>
- **Minor**: <issue>
- **Nit**: <issue>

If a slide is clean, say "Clean for client delivery." Do not skip clean slides — explicit "clean" calls help us trust the pass.

Slides to inspect:
1. <path-to-slide-01.jpg> — <one-line expected content>
2. <path-to-slide-02.jpg> — <one-line expected content>
...

Keep total response tight. Aim for under <N×75> words where N is the slide count. Lead with Blocking and Important; do not pad with minor items.

If you see the same defect across many slides, call it out as a systemic pattern at the top of your report rather than repeating it per slide.
```

## Why this prompt works

- **"Assume there are issues"** flips the model from confirmation bias to discovery. Without this, the model passes too easily.
- **The full defect catalog** is in-context so the model has a concrete checklist instead of relying on its taste.
- **Severity buckets** force the model to commit to which findings actually block ship vs. which are quibbles.
- **"Do not skip clean slides"** prevents silent passes that leave the reviewer wondering whether the slide was checked at all.
- **A word cap** keeps the report scannable. Long reports get skimmed and the blocking issue gets missed.

## What to hand the subagent

- The rendered JPGs (or PNGs) of every slide
- The full content of `references/visual-defects.md`, inline in the prompt
- Any deck-specific style notes you have (brand colors, font, intent)
- The slide list with one-line expected content per slide

Do not hand the subagent:
- The original source documents (that is the content-track subagent's job)
- The deck's `.pptx` file (it should be judging the rendered visuals, not the XML)
- Your own opinion of how the slide should look

## When to run multiple subagents

For decks longer than ~20 slides, split into batches of 8–10 slides per subagent and run them in parallel. A single subagent reading 30+ images loses focus and produces shallower per-slide findings.

For decks under 10 slides, one subagent is enough.

## When to re-run

After fixing issues, ALWAYS re-render the affected slides and re-run a subagent pass on those slides. Do not trust your own check. One fix often introduces a new defect (especially card-height changes, which ripple through the whole row).

If the second pass returns clean, you are done. If the second pass returns new issues, fix again and re-run a third pass. Stop only when a subagent returns clean.
