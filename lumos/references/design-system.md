# Design system

The look is editorial and calm: a near-white reading sheet on a barely-tinted desk, one dominant color (here a grass green) with a single spark accent (lime) and a secondary accent for a second category (blue), a serif display face (Fraunces) over a clean grotesk body (Hanken Grotesk), generous air, soft shadows, and a signature mark. Pick your own palette and fonts per topic, but keep the same structure: one dominant color, one spark, one secondary, a distinctive display + body pairing, and real atmosphere.

## Fonts (in `<head>`)

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,400..700;1,9..144,400..600&family=Hanken+Grotesk:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap">
```

Avoid generic system fonts (Inter, Roboto, Arial) and the purple-gradient-on-white cliche. Pair a characterful display face with a refined body face.

## Tokens (`:root`)

```css
:root {
  --bg: #f1f4f1;        /* barely-there desk behind the white sheet */
  --bg2: #fbfdfb;       /* near-white tint */
  --card: #ffffff;      /* floating tile */
  --border: #e6e9e4; --border-hi: #d6dbd4;
  --text: #0a1610;      /* near-black ink, headings */
  --text2: #1e2620;     /* body */
  --text3: #586359;     /* muted labels */
  --accent: #0c6e3d;    /* DOMINANT color (category 1) */
  --accent2: #08572f;   /* deeper dominant */
  --lime: #a9c638;      /* spark, used sparingly */
  --green: #0e8a58;
  --blue: #1c6fe0;      /* SECONDARY color (category 2) */
  --grape: #5c2e72;     /* tertiary eyebrow accent */
  --coral: #c2533b;     /* "bad/old" signal */
  --code-bg: #fafcfa;
  --mono: 'JetBrains Mono', ui-monospace, monospace;
  --sans: 'Hanken Grotesk', system-ui, sans-serif;
  --display: 'Fraunces', Georgia, serif;
  --radius: 11px; --radius-lg: 18px; --radius-xl: 24px;
  --pad-x: 56px;        /* sheet inner padding; hero bleeds to this */
  --shadow-sm: 0 1px 2px rgba(20,38,28,.035), 0 4px 14px rgba(20,38,28,.05);
  --shadow-md: 0 2px 8px rgba(20,38,28,.05), 0 16px 38px rgba(20,38,28,.09);
}
```

## Color-coding convention

Color encodes *category*, not decoration. In the prompting guide: green = one product family, blue = the other. Give each concept a category and tint its card border / eyebrow / number accordingly (`.concept` green by default, add `.concept.api` to switch to blue). Keep it to two or three categories so the signal stays legible.

## Type scale

```css
main h1 { font-family: var(--display); font-weight: 600; font-size: clamp(40px,5.4vw,58px); line-height: 1.03; letter-spacing: -.022em; color: var(--text); }
main h1 em { font-style: italic; font-weight: 500; color: var(--accent); }   /* one word in the accent, italic */
main h2 { font-family: var(--display); font-weight: 550; font-size: 30px; border-top: 1px solid var(--border); position: relative; }
main h2::before { content:""; position:absolute; top:-1px; left:0; width:52px; height:2px; background: linear-gradient(90deg,var(--accent),var(--lime)); }
main h3 { font-family: var(--sans); color: var(--grape); font-weight: 600; letter-spacing: .085em; }  /* small caps-ish label */
body { font-family: var(--sans); color: var(--text2); background: var(--bg); }
```

## Masthead: full-bleed banner + atmosphere + a signature seal

The hero is a full-bleed banner (negative horizontal margins to the sheet padding) with layered atmosphere and a distinctive emblem on the right. The emblem here is a "seal": a medallion with slowly rotating engraved microtype around the rim and a small constellation in the center that encodes the guide's thesis. Replace the concept, but keep the principle: a meaningful signature mark, not a stock badge or a dashboard gauge.

```css
.hero { position: relative; overflow: hidden; isolation: isolate;
  display: grid; grid-template-columns: 1fr auto; align-items: center; gap: 36px;
  margin: 0 calc(-1 * var(--pad-x)) 4px; padding: 46px var(--pad-x) 40px;
  background:
    radial-gradient(120% 150% at 90% 4%, rgba(169,198,56,.18) 0, transparent 40%),
    radial-gradient(130% 130% at 2% 116%, rgba(12,110,61,.11) 0, transparent 46%),
    linear-gradient(134deg, #f6faf1 0%, #edf6e9 55%, #e4f1de 100%);
  border-bottom: 1px solid var(--border); }
.hero-bg { position:absolute; inset:0; z-index:0; overflow:hidden; pointer-events:none; }
.hero-grain { position:absolute; inset:0; opacity:.42; mix-blend-mode:soft-light;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='150' height='150'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.82' numOctaves='2' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E"); }
.hero-main { position: relative; z-index: 1; }
.hero-main h1 { font-size: clamp(48px,6.3vw,72px); line-height:.99; letter-spacing:-.03em; }
.hero-main .lede { font-family: var(--sans); font-size: clamp(19px,2vw,23px); color: var(--text2); max-width: 46ch; }
```

The seal SVG (rim text via `textPath`, a 3-node constellation, slow rotation, reduced-motion-exempt because it is slow and decorative):

```html
<aside class="hero-seal" aria-label="One playbook across three surfaces">
  <svg class="seal" viewBox="0 0 200 200" aria-hidden="true">
    <defs><path id="sealArc" d="M100,100 m0,-79 a79,79 0 1,1 0,158 a79,79 0 1,1 0,-158"/></defs>
    <circle class="seal-ring-outer" cx="100" cy="100" r="93"/>
    <circle class="seal-ring-mid" cx="100" cy="100" r="62"/>
    <g class="seal-rot"><text class="seal-text"><textPath href="#sealArc">YOUR THESIS &#183; REPEATED &#183; YOUR THESIS &#183; REPEATED &#183; </textPath></text></g>
    <g class="seal-net"><line x1="100" y1="100" x2="100" y2="65"/><line x1="100" y1="100" x2="130" y2="117.5"/><line x1="100" y1="100" x2="70" y2="117.5"/></g>
    <circle class="seal-node n1" cx="100" cy="65" r="6.5"/><circle class="seal-node n2" cx="130" cy="117.5" r="6.5"/><circle class="seal-node n3" cx="70" cy="117.5" r="6.5"/>
    <circle class="seal-core" cx="100" cy="100" r="9.5"/>
  </svg>
</aside>
```

```css
.seal { width: 196px; height: 196px; overflow: visible; filter: drop-shadow(0 7px 16px rgba(20,38,28,.07)); }
.seal-ring-outer { fill: rgba(255,255,255,.52); stroke: rgba(12,110,61,.16); }
.seal-ring-mid { fill:none; stroke: rgba(12,110,61,.22); stroke-dasharray: .5 5; stroke-linecap: round; }
.seal-text { font-family: var(--mono); font-size: 9px; letter-spacing: 1.7px; fill: var(--text3); }
.seal-rot { transform-origin: 100px 100px; animation: sealspin 18s linear infinite; }
@keyframes sealspin { to { transform: rotate(360deg); } }
.seal-net line { stroke: rgba(12,110,61,.30); }
.seal-node.n1 { fill: var(--accent); } .seal-node.n2 { fill: var(--green); } .seal-node.n3 { fill: var(--lime); }
.seal-node, .seal-core { stroke: #fff; stroke-width: 2.4; } .seal-core { fill: var(--accent2); }
/* keep the slow, decorative seal alive even under reduced motion */
@media (prefers-reduced-motion: reduce) { .seal-rot { animation: sealspin 22s linear infinite !important; } }
```

The nav uses a small version of the same medallion (a 38px constellation, `transform-box: fill-box; transform-origin: center` on the rotating ring) so the sidebar and hero share one identity. Match the wordmark to the hero title.

## Core components (the teaching hierarchy)

```css
/* Concept card: a left accent rule keyed to category */
.concept { border-left: 3px solid var(--accent); padding: 4px 0 4px 22px; margin: 22px 0; }
.concept.api { border-left-color: var(--blue); }
.concept-name { font-weight: 600; color: var(--text); }
.concept-def { color: var(--text2); }
.cs-label { font-size: 13px; color: var(--text3); letter-spacing: .04em; }
.cs-more { margin-left: auto; border: 1px solid var(--border); border-radius: 999px; padding: 2px 10px; }  /* "Open full page" pill */

/* Example: 2 good + 1 bad */
.ex-grid { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 12px; }
.ex-card { border: 1px solid var(--border); border-radius: var(--radius); padding: 14px; background: var(--bg2); }
.ex-card.ex-good { border-top: 3px solid var(--green); }
.ex-card.ex-bad  { border-top: 3px solid var(--coral); }
.ex-tag { font-size: 12px; font-weight: 600; }

/* In Practice: Do / Avoid columns */
.dl-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }
.dl-col.dl-do    { border-left: 3px solid var(--green); }
.dl-col.dl-avoid { border-left: 3px solid var(--coral); }

/* Deep-dive worked example + practice list + routing table */
.we { border:1px solid var(--border); border-radius: var(--radius-lg); padding:18px; margin:14px 0; }
.we-good { border-left: 3px solid var(--green); } .we-bad { border-left: 3px solid var(--coral); }
.prac-item { display:flex; gap:12px; } .prac-item.avoid .prac-mark { color: var(--coral); }
table.symp { width:100%; border-collapse: collapse; } table.symp .s-fix { color: var(--accent); font-weight:600; }

/* Code syntax spans (hand-rolled, no highlighter dependency) */
.c-key{color:#a3258a} .c-str{color:var(--accent)} .c-cmt{color:var(--text3); font-style:italic} .c-fn{color:var(--blue)} .c-val{color:var(--coral)} .c-tag{color:var(--grape)}

@media (max-width: 768px) { .ex-grid, .dl-grid { grid-template-columns: 1fr; } }
```

## Motion

A single, well-orchestrated page-load reveal beats scattered micro-interactions: stagger the hero children with `animation-delay`. Always gate motion:

```css
@keyframes riseIn { from { opacity:0; transform: translateY(15px); } to { opacity:1; transform:none; } }
.hero-main > * { animation: riseIn .72s cubic-bezier(.2,.7,.25,1) backwards; }
.hero-main h1 { animation-delay:.12s; } .hero-main .lede { animation-delay:.22s; }
@media (prefers-reduced-motion: reduce) { *, *::before, *::after { animation: none !important; transition: none !important; } }
```

The reduced-motion block above kills everything; if you want one slow decorative loop to survive (like the seal), re-enable just that selector with `!important` inside a second `@media (prefers-reduced-motion: reduce)` block (higher specificity wins).
