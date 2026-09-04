# Interactive companion (step-through session)

A separate single HTML file that turns the guide's sections into a guided, one-at-a-time **session**. The canonical instance is a "conversation starters" deck: for each section, 2 to 3 open questions that hook the idea to the learner's own experience and open discussion (not a self-quiz). The same engine works for flashcards, drill prompts, review questions, or a facilitator deck, just swap the content of each card.

## What makes it good

- **It is a session, not a list.** One card at a time, with Back / Next, a progress bar ("03 / 29"), and arrow-key navigation. That focus is the whole point; a static list of all questions is far less engaging.
- **Conversation starters, not checks.** Questions are experience-hooking openers ("Have you ever told it to always do X, and it just did not?"), written to lead into the *actual* concept each section teaches. Keep them accurate to the source material, same rigor as the guide.
- **It reuses the guide's identity.** Same fonts, palette, the medallion mark, and the category color-coding (each card tinted to its section's category). The two files feel like one product.
- **It links back.** Each card has an "Open this section in the guide" deep-link to `guide.html#section-id`.

## Data model

```js
const DATA = [
  { id: "loops", s: "cc", title: "Loops and workflows", q: [
    "Have you heard of /loop? What is a task you currently babysit turn by turn?",
    "Run-until-done or repeat-on-a-schedule: which does your task actually need?"
  ]},
  // ... one object per section. id -> deep-links to guide#id. s -> category (drives color). q -> 2 to 3 starters.
];
```

## Engine (the interactions that matter)

- `render(i)`: set the card number, the category chip, the title, the questions, and the guide deep-link; set `card.dataset.surface = d.s` so CSS colors it; re-trigger the enter animation (`card.classList.remove('in'); void card.offsetWidth; card.classList.add('in')`); update the progress bar width to `(i+1)/N`.
- **Navigation:** Back / Next buttons (disable at the ends), plus a `keydown` handler: ArrowRight/Space -> next, ArrowLeft -> prev, `s` -> shuffle, `c` -> contents, Escape -> close.
- **Shuffle:** jump to a random index that is not the current one (good for a facilitator who wants a surprise opener).
- **Contents sheet:** a slide-in panel listing every section (number, category dot, title), click to jump. Highlight the current one.
- **Click to mark asked:** clicking a question toggles a struck-through "asked" style, tracked in a `Set` keyed by `"i:qi"` so marks persist as you move back and forth. This suits live facilitation; it is a usage aid, not a score.

## Color-coding

```css
.card { --c: var(--accent); }              /* category 1 */
.card[data-surface="api"] { --c: var(--blue); }   /* category 2 */
.card::before { content:""; position:absolute; left:0; top:0; bottom:0; width:5px; background: linear-gradient(var(--c), var(--lime)); }
.num, .chip, .qs li::before { color: var(--c); border-color: var(--c); }  /* number, chip, question markers all key off --c */
```

## Reduced motion

Same rule as the guide: collapse animations under `prefers-reduced-motion`, but you may keep one slow decorative loop (the header medallion) alive via a targeted `!important` override.

## Optional polish

A short cover screen ("N ideas, one question at a time, press the right arrow to begin") and an end screen round out the session. Wire a link to the companion into the guide's nav (and vice versa) so the two files connect both ways.
