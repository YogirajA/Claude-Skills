---
name: sonorus
description: Use when the user wants to create a new conference talk / presentation deck (a slide deck), or asks to "make a deck", "start a talk deck", "scaffold slides", or mentions building a PlumDeck-style presentation. Interviews the user, then generates a self-contained, offline HTML slide deck with built-in author mode. Formerly conference-talk-deck.
disable-model-invocation: true
---

# Sonorus

*Amplifying Charm,* makes your voice carry to a room.

Generate a self-contained, offline, projector-ready HTML slide deck styled like PlumDeck, with the
full presentation engine built in (keyboard nav, overview grid, inline **author/edit mode**, save,
help overlay, fullscreen, progress bar). You **interview the user first**, then produce a real
first-draft deck they refine in author mode.

The engine is in `template/deck.html` (in this skill's directory). Never rebuild it from scratch and
never strip its `<script>` engine or author-mode CSS; clone it and inject content.

## Step 1: Interview (one question at a time)

Ask these conversationally, **one per message**, waiting for each answer. Prefer to offer a sensible
default in the question so the user can just confirm. Keep it tight; this is a draft, not an
interrogation.

1. **Talk title** and **subtitle** (one line that frames it).
2. **Event and speaker** (e.g. "KCDC 2026" · the user's name). Default the event if known from memory.
3. **Audience and level**: who's in the room, and is it introductory or deep-dive? (Shapes tone and
   density.)
4. **The thesis**: the single sentence the audience must leave with.
5. **Length**: talk duration, and the **minimum number of slides** to scaffold. Convert duration to a
   floor if they're unsure (rough guide: ~1 slide per minute for fast talks, ~1 per 1.5–2 min for
   dense ones), then confirm the minimum with them. The deck must have **at least** this many slides.
6. **Section arc**: the 3–6 sections the talk moves through (e.g. hook → problem → framework → demo →
   takeaway). Get a name for each.
7. **Key point per section**: one or two sentences per section on what it must land. This is the
   "interview me on the deck" substance that becomes the drafted slide content.
8. **Accent color**: default to the PlumDeck coral (`#ef7d24` / light `#f0a672`). Offer to change it
   (teal `#0f8f86`/`#4fd0c4`, magenta `#c4407e`/`#e57ea9`, or a hex they give). Everything else stays
   the plum theme.

If the user says "just scaffold it" or gives terse answers, fill reasonable defaults and move on; a
draft they can edit beats a long interview.

## Step 2: Generate the deck

1. **Pick a target path.** Default `deck.html` in the current project (or ask). Confirm before
   overwriting an existing file.
2. **Read** `template/deck.html` from this skill's directory.
3. **Replace the top placeholders:**
   - `{{DECK_TITLE}}` (plain text, used in `<title>`, the engine `TITLE` var, and the grid header),
   - `{{DECK_TITLE_HTML}}` (the title slide headline; you may wrap a word in `<i>…</i>` for the accent),
   - `{{SUBTITLE}}`, `{{EYEBROW}}` (e.g. "EVENT · SESSION"), `{{SPEAKER}}`, `{{EVENT}}`,
   - `{{ACCENT}}` / `{{ACCENT_LT}}` with the chosen hex pair.
   Verify no `{{` remains.
4. **Replace the slides** between `<!-- SLIDES_START -->` and `<!-- SLIDES_END -->` with the real deck:
   the title slide, then a section-divider before each section, then content slides drafted from the
   key points, then a closing slide. Meet or exceed the minimum slide count. Use the slide patterns
   below verbatim (they carry `data-ek` so author mode can edit them). Leave `.pg` as `01 / 01`; the
   engine renumbers on load.
5. **Draft real content** (option: hybrid): every slide gets a true title and a first-pass bullet or
   two / a short body from the interview, not empty placeholders. Keep bullets short and specific;
   one idea each. This is a starting draft; the user refines in author mode.
6. Write the file. Do **not** run a live server unless asked; it's a static file the user opens.

## Step 3: Hand off

Tell the user: the deck is at `<path>`; open it in a browser; **arrows/space** to present, **O** for
the overview (drag to reorder, `+` duplicate, `×` delete in author mode), **E** for author mode to
click-edit any text, **Ctrl+S** to save (writes the file back via the browser's save picker, download
fallback otherwise), **F** fullscreen, **?** for help. Offer to adjust content or add sections.

## Slide patterns (use verbatim; `data-ek` marks editable text)

**Section divider** (`{{NN}}` = zero-padded section number, e.g. `02`):
```html
  <div class="slide section-slide"><section>
    <div class="snum" data-ek>{{NN}}</div>
    <h2 data-ek>Section title <i>here.</i></h2>
    <div class="pg">01 / 01</div>
  </section></div>
```

**Content slide with bullets:**
```html
  <div class="slide content-slide"><section>
    <div class="eyebrow" data-ek>Section name</div>
    <h2 class="title" data-ek>The slide's point as a short sentence</h2>
    <ul class="bullets">
      <li data-ek>One idea, with a <b>key phrase</b> emphasized.</li>
      <li data-ek>Another idea, kept to one line.</li>
    </ul>
    <div class="pg">01 / 01</div>
  </section></div>
```

**Content slide with a body statement** (for a single big idea):
```html
  <div class="slide content-slide"><section>
    <div class="eyebrow" data-ek>Section name</div>
    <h2 class="title" data-ek>The claim</h2>
    <div class="body" data-ek>One or two sentences that make the case, with room to breathe.</div>
    <div class="pg">01 / 01</div>
  </section></div>
```

**Closing slide:**
```html
  <div class="slide close-slide"><section>
    <div class="eyebrow" data-ek>Takeaway</div>
    <h1 class="big" data-ek>The one thing to <i>remember.</i></h1>
    <div class="sub" data-ek>A closing line that lands the thesis.</div>
    <div class="pg">01 / 01</div>
  </section></div>
```

## Rules

- **Self-contained and offline.** No build step, no external assets except the Google Fonts link
  already in the template. Everything inline. Ships as one `.html` the user double-clicks.
- **Never touch the engine.** Keep the `<script>` block, the chrome (`#bar`, `#hud`, `#hint`, `#grid`,
  `#help`, `#authorbar`, `.zone`), and the author-mode CSS intact so every deck has full parity.
- **PlumDeck look.** Playfair Display (display), Hanken Grotesk (body), JetBrains Mono (mono), plum
  background. Only the accent changes per the interview.
- **Writing:** sentence case, plain verbs, one idea per bullet. No em dashes in authored copy (use a
  comma, colon, or parentheses). Keep the deck's own thesis in view on every section.
- See `references/features.md` for the full feature-parity checklist and palette spec.
