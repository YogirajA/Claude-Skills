# Deck feature parity + design spec

Every deck the skill generates must have all of this (it all lives in `template/deck.html`). Read this
when verifying a generated deck or extending the template.

## Functionality (built into the engine)

| Feature | Key / control | Notes |
|---|---|---|
| Next / previous | `→` `Space` `PageDown` `l` `j` / `←` `PageUp` `h` `p` | Also left/right click zones (16% edges). |
| Jump to slide | type `1`–`9`… then `Enter` | Multi-digit buffer. |
| First / last | `Home` / `End` | |
| Overview grid | `O` | Thumbnails of every slide; click a thumb to jump (non-author). |
| Author / edit mode | `E` | Click any text to edit inline; author bar shows dirty/saved. |
| Reorder / add / delete | `O` in author mode | Drag thumbs to reorder; `+` duplicate, `×` delete per thumb. |
| Save | `Ctrl+S` / `Cmd+S` | Serializes the live DOM back to a standalone `.html` via File System Access API; download fallback. Remembers the file handle after first save. |
| Fullscreen | `F` | |
| Help overlay | `?` (`Esc` closes) | Keyboard cheat sheet. |
| Progress bar | top edge | Fills with slide position. |
| Page number | `#hud` (top-right) + per-slide `.pg` | Auto-renumbered on load and after structural edits. |
| Deep link | `#N` in the URL | Reflects and restores the current slide. |
| Unsaved guard | `beforeunload` | Warns if there are unsaved edits. |
| Auto-scale | resize | 1280×720 canvas scaled to fit any screen (`--scale`). |
| Reduced motion | `prefers-reduced-motion` | Slide transitions disabled. |

## Palette

- Background plum ramp: `--plum-0 #0a0610`, `--plum-1 #271539`, `--plum-2 #3a2154`, `--plum-3 #5b3663`
- Ink `#fdfbfe`; muted `rgba(253,251,254,.62)`, muted-2 `rgba(253,251,254,.42)`
- Card `#1c1228`, card line `#3a2154`
- Fixed secondary accents: teal `#0f8f86`, magenta `#c4407e`
- **Accent (per-deck, interview-set):** default coral `--accent #ef7d24` / `--accent-lt #f0a672`.
  Alternatives: teal `#0f8f86`/`#4fd0c4`, magenta `#c4407e`/`#e57ea9`. The accent drives the progress
  bar gradient, eyebrows, italic display highlights, bullet ticks, background glow, and author-mode UI.

## Type

- Display: **Playfair Display** (600, italics for accented words): titles, section headers.
- Body: **Hanken Grotesk** (400–700): subtitles, bullets, body copy.
- Mono: **JetBrains Mono**: eyebrows, page numbers, HUD, author bar, code.
- Scale (at 1280×720): title `72px`, section header `64px`, content title `52px`, sub `24–26px`,
  bullets `23px`, eyebrow `14px` uppercase tracked.

## Slide types

`title-slide` (eyebrow, big headline, sub, speaker/event meta) · `section-slide` (section number,
big header) · `content-slide` (eyebrow, title, `.bullets` or `.body`) · `close-slide` (eyebrow, big
headline, sub). All text nodes carry `data-ek` so author mode targets them; the engine also falls back
to editing any text leaf.

## Placeholders in the template

`{{DECK_TITLE}}`, `{{DECK_TITLE_HTML}}`, `{{SUBTITLE}}`, `{{EYEBROW}}`, `{{SPEAKER}}`, `{{EVENT}}`,
`{{ACCENT}}`, `{{ACCENT_LT}}`, and the `<!-- SLIDES_START -->` … `<!-- SLIDES_END -->` block. After
generation, no `{{` should remain.

## Relationship to the demo players

The two KCDC demo players (`Agentic Ruin/demo/Demo.html`, `Agent Lied/demo/Demo.html`) use the same
author-mode *experience* (E to edit, Ctrl+S to save, plum author bar) but a different persistence
mechanism: they are data-driven step-players, so edits are captured into a keyed `EDITS` override map
(`[data-ek="path"]` + `<script id="edits-data">`) and re-applied on every render, rather than
serializing static slide DOM. This skill produces static slide decks, which serialize the DOM
directly (the PlumDeck model). Don't copy the override machinery into generated decks.
