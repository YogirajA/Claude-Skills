# Severity rubric

How to decide whether a finding is Blocking, Important, Minor, or Nit. Apply consistently across the visual and content tracks.

## Blocking

The deck cannot ship. A client, executive, or auditor will notice this and lose trust.

Examples:
- Text overflow that hides content (a stat that ends mid-word, a bullet cut off)
- Content past the slide bottom (a card running off the slide)
- Footer overlapping the page number or content
- Wrong customer name in a customer slide
- Wrong product name or wrong model version
- Fabricated number on a stat slide
- Wrong client name in the footer
- URL that does not resolve (404, made-up domain)
- Leftover placeholder text ("Lorem ipsum", "XXXX", "TBD where TBD wasn't intended")
- Wrong legal disclaimer or compliance language
- Sensitive data leaked (real customer name where redacted, real revenue numbers where rounded was intended)

Rule of thumb: if the user would have to redo a meeting or recall the deck, it is Blocking.

## Important

The deck looks unprofessional or undermines the message. Most clients will notice on a careful read. Must fix before ship except in genuine emergencies.

Examples:
- Mid-card whitespace holes (>0.8" empty band between content blocks)
- Ragged card heights in a row
- Top half of a content slide blank below the title
- Stair-step misalignment between title and body
- Right-edge or left-edge dead zone > 2"
- Centred body text on a non-cover slide
- Inconsistent column widths in a grid
- Low-contrast text that is technically readable but uncomfortable
- Drift on a numeric claim (close to source but not exact)
- Stale fact (was true, now isn't)
- Inconsistent footer text across slides
- Page numbering breaks
- Title position drift across slides

Rule of thumb: if a careful reviewer would flag it in a track-changes review, it is Important.

## Minor

Real defects that should be fixed when time permits. Most viewers will not notice but a designer or QA reviewer will.

Examples:
- Slightly inconsistent gutters (0.3" vs 0.5")
- Mild color drift between similar cards (one shade off)
- Tag baseline misalignment of less than 0.3"
- A single line of body text that runs slightly past the comfortable line width
- A bullet list with mixed periods (some bullets end with "." and some don't)
- Smart quote vs straight quote inconsistency
- An en-dash where the deck convention is em-dash, or vice versa
- A paraphrase that is faithful but slightly looser than the source phrasing

Rule of thumb: ship if time-constrained, fix in the next pass.

## Nit

Cosmetic preferences. The deck is fine. Flag only if asked for an exhaustive pass.

Examples:
- One-line vs two-line kicker variation in a card grid
- Slight color tint difference between two similar shades
- Title kerning preference
- "Word ordering" suggestions that don't change meaning
- Personal style preference about italics vs bold for accents

Rule of thumb: do not lead with these. They are noise unless the user explicitly asked.

## How to weight visual vs content

Content findings are almost always more important than visual findings at the same severity tier. A "Minor" content drift (a customer stat off by 5 percentage points) is more damaging than a "Minor" visual issue (a 0.3" gutter inconsistency).

When in doubt, treat content as the higher-priority track. Visual issues degrade trust gradually; content issues destroy it instantly.

## Reporting templates

For a Blocking finding:

```
**Blocking** — Slide 7, card 3
Text "Up to 9% saved on migrations" appears to overflow the card and clip at the right edge. Source `claude.com/customers/spotify` says "Up to 90 percent saved on migrations" — the leading "0" is missing AND the layout cannot fit the corrected text.
Fix: shorten to "Up to 90% on migrations" OR widen the card.
```

For an Important finding:

```
**Important** — Slide 5, all cards
Cards in the row have ragged bottom edges (card 1 ends at y≈5.8, card 3 ends at y≈6.4). Pre-measure max card height and render all four cards at the max.
```

For a Minor / Nit finding:

```
**Minor** — Slide 11
Italic footnote ends about 0.4" above the footer band. Could compress to leave less trapped whitespace.
```

Specificity (which slide, which card, rough coordinates) is what makes findings actionable. "Card looks off" is not a finding; "card 2 has 0.9" of empty space between its body and its tag" is.
