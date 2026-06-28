# Visual defects catalog

Every item on this list has shipped in a deck that "looked clean" on a first pass and then been flagged by a client or stakeholder. Check every one on every slide. Self-review and subagent review both.

The catalog is organized by failure mode, not by severity. Severity depends on context: a 0.3" empty band is fine on a section divider and a blocker on a content slide. See `severity-rubric.md`.

## Footers and chrome

- **Dark-background footer contrast.** Default dark-on-white footer text becomes invisible on cover, section-divider, key-message, and closing slides. Every coloured-background slide needs a light-text footer variant.
- **Section divider footer under coloured block.** On a divider with a coloured left block, default footer placement puts the footer text ON the coloured block and invisible. Either move the footer text into the white area OR use light text over the coloured block.
- **Page number contrast on coloured slides.** Medium-gray page numbers disappear on dark backgrounds. Bold + a light tint.
- **Duplicate footers.** Closing / thank-you slides that render the template footer AND an on-slide "Date | Version | Confidential" block. Pick one.
- **Footer overlap with content.** A bottom-anchored content strip (callout bar, source citation) that drops down onto the footer text or page number. Leave at least 0.15" breathing room above the footer band.
- **Wrong client name or wrong stamp.** Footer says "Internal use only" on a client-facing deck, or the wrong client name. Caught in the content track too, but flag here as visual chrome.

## Vertical balance

- **Empty band below the title.** Title at y ≈ 0.5" and the first content block starts at y ≥ 2.2". The 1–2 inch empty band reads as forgotten content. Either move the content up (start at y ≤ 1.6") or fill the band with a kicker/subtitle/divider line.
- **Content bottom-clustered, top half blank.** All content lives between y = 4.0" and y = 6.8" while the area below the title is empty. Stretch content vertically or vertically centre title+content as one balanced unit. Never ship a slide where the top 40% of the canvas is blank below the title.
- **Card grids floating in the lower half.** A 2x2 or 2x3 grid whose top edge is at y ≥ 3.0" leaves a giant empty band above. Pull the grid up to y ≈ 1.7" and make cards taller, OR add a header strip above.
- **Sparse content stranded at the bottom.** A title and a single short paragraph at y ≈ 5.0" with everything above blank. Switch to a layout designed for sparse content (key-message, big-stat, quote slide).
- **Uneven column lengths leaving a dead corner.** Two-column slide where the left column ends at y = 3.5" and the right column ends at y = 6.2". Fill the short column's tail with a stat, callout, image, or extend the content.
- **Last content line ending well above the footer.** Last content at y ≈ 5.0", footer at y ≈ 7.1" — over 2 inches of trapped empty space.
- **Mid-card vertical gap between top-anchored body and bottom-anchored footnote.** Card body paragraph hugs the top of the card; an italic tag or bullet block is pinned to the bottom of the card; a >0.8" empty band sits between them. The card looks broken even though it is technically "filled". Fix by (a) shrinking the card to hug the actual content, (b) removing the bottom anchor so the tag sits directly under the body with normal paragraph spacing, or (c) adding a middle element to bridge the gap.
- **Sibling cards with mismatched content density and identical heights.** Two cards forced to the same height; one has 6 lines of body, the other has 3 lines + a tagline. The shorter card develops a mid-card void.

## Horizontal balance

- **Right-edge dead zone.** Content stops at x ≈ 8" on a 13.33" slide, leaving a ≈5" empty right strip. Either extend content or commit to a deliberate half-canvas layout with a clear visual reason.
- **Left-edge dead zone.** Mirror of the above. Content sits at x ≥ 4" with the entire left third blank.
- **Title/body x-misalignment ("stair-step").** Title at x = 0.5", body at x = 1.2". Looks like an accidental indent. Title and body left edges should match unless the layout intentionally indents body content.
- **Centred body text on a non-cover slide.** Bullets, paragraphs, and lists centred horizontally — looks amateur. Centre only titles, key-messages, quotes, and big-stat numbers.
- **Asymmetric column widths with no semantic reason.** Two-column slide with col1 = 3" and col2 = 9" where the content is two parallel ideas. Size columns equally or commit to a deliberately asymmetric motif repeated across the deck.
- **Inconsistent gutters across a grid.** Gap between cards 1–2 is 0.3" but between 2–3 is 0.5". Pick one gutter.
- **Floating single column ignoring the right half.** A single text column at x = 0.5–6.0" leaves the right half blank with no visual element.

## Card and grid layout

- **Uneven card heights in a single row.** Copy length differs between cards, so bottom edges are ragged. Fix by normalising copy length, using fixed card heights with content wrapping, or top-aligned content inside equal-height cards.
- **Mid-card whitespace.** A 3-line paragraph inside a 3.5"-tall card leaves a huge blank area that looks like a forgotten second paragraph. Either shrink the card OR add the missing content.
- **5-item grids with a dangling bottom row.** 3+2 layouts (3 top, 2 centred below) create an L-shape that reads as "missing card." Either drop to 4 items, stretch to 5 in a single row, or split into 4 cards + a full-width banner for the fifth.
- **Column headers wrapping unevenly.** One header wraps to 2 lines while siblings are 1 line — header band heights differ. Shorten the long label OR reserve 2-line header space for all.
- **Ragged tag baselines.** When cards have a bottom tag/italic accent, all tags should share a baseline. If body lengths differ and tags flow after body, tags will land at different y values. Bottom-anchor the tag at a uniform offset from the card bottom.

## Overflow and clipping

- **Text overflow at card boundary.** Body wraps to more lines than the card can hold. Text bleeds outside the card fill OR onto the next element.
- **Text cut off at slide edge.** Long title runs to x = 13.5" and gets clipped at the slide boundary.
- **Content past the slide bottom.** A card whose bottom edge exceeds y = 7.3" overlaps the footer or runs off the slide entirely. Rendered from a too-tall card_h or too-much body.
- **Bullets falling off the slide.** Bulleted list that scrolls past the bottom margin.

## Colour and style

- **Non-monotonic colour ramps.** Sequential cards coloured "purple, darker, lighter, lightest, gray" look random. Commit to a clear monotonic gradient OR a single colour.
- **Off-brand colour breaks.** A gray card header in a series of purple card headers. An orange accent in an otherwise purple deck.
- **Mixed callout styles across slides.** A black insight bar on one slide and a purple-tint strip on others. Commit to one callout treatment.
- **Low-contrast text or icons.** Light gray text on cream background, dark icons on dark background. Test against WCAG AA (4.5:1 for body, 3:1 for large text) as a sanity floor.
- **Tiny accent rules under titles.** Decorative 1-pixel lines below every title read as AI-generated. Use whitespace instead.

## Text and character rendering

- **Literal special characters that don't render.** `★`, `✦`, `✓`, `»` and similar glyphs often fall back to a different font or render as an asterisk on LibreOffice. Swap for filled shapes, standard bullets, or Unicode that the target font guarantees.
- **Floating body text with no container.** An italic line sitting below a grid with no background, no strip, no card — looks like a forgotten element. Wrap orphan lines in a styled strip or a card.
- **Trailing content touching the footer.** The last line at y ≈ 7.0", footer bar at y ≈ 7.15" — reads as cramped.
- **Excessively long lines.** Body text running the full 12" of a wide slide is hard to scan. Column-constrain long-form body to ≤ 5" per line.
- **Leftover placeholder text.** "Lorem ipsum", "XXXX", "TBD" (where the TBD was supposed to be filled in), "this slide layout" instructional text from a template.
- **Inconsistent en-dash / em-dash / hyphen usage.** Especially relevant if the user has a documented preference (e.g., "never use em dashes").

## Layout consistency across slides

- **Title position drift.** Slide 3 title at y = 0.4", slide 5 title at y = 0.7". Subtle but visible when the audience pages through.
- **Subtitle present on some slides and missing on others** without a deliberate pattern.
- **Footer text varies slide to slide.** A footer that says "Internal" on slide 4 and "Confidential" on slide 12.
- **Page numbering breaks.** A hidden or template slide that throws the visible page numbers out of sequence.

## What is NOT a defect

- Sparse cover slides, section dividers, big-stat slides, and quote slides are intentionally airy. Their job is to land one big idea.
- Bottom margin on shorter cards in a uniform-height grid is a deliberate design pattern. It is only a defect when there is a top-anchored element AND a bottom-anchored element with a visible empty band between them.
- A two-column slide with intentionally asymmetric columns (e.g., a 60/40 image-text split repeated across the deck as a motif) is intentional.
- Different colour treatments on cover vs body slides are intentional. The contrast IS the design.
