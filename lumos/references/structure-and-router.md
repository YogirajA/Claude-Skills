# Structure and router

## The teaching hierarchy (every concept, same shape)

```
Concept (one-line name + one-line definition)
  |- Example      -> 2 good, 1 bad, each worked (not just labeled)
  |- In Practice  -> Do column / Avoid column, concrete actions
```

Heavy concepts also get two full **deep-dive pages** (one for Example, one for In Practice), each linked from the card with an "Open full page" pill and routed in-app. The Example deep-dive holds 4 to 9 worked examples; the In Practice deep-dive holds 8+ Do/Avoid items plus a symptoms/routing table.

### Concept card template

```html
<div class="concept"><!-- add class "api" for the second category color -->
  <div class="concept-head">
    <span class="concept-bullet"></span>
    <div>
      <div class="concept-name">Ship expertise as a versioned artifact, not a re-pasted prompt</div>
      <div class="concept-def">One-sentence definition with an inline citation<a class="src" href="#ref-4">[4]</a>.</div>
    </div>
  </div>
  <div class="concept-sub">
    <div class="cs-label"><span class="cs-num">1</span> Example <a class="cs-more" href="#page-skills-example">Open full page &rarr;</a></div>
    <div class="ex-grid">
      <div class="ex-card ex-good"><div class="ex-tag">Good</div><div class="ex-body">...</div></div>
      <div class="ex-card ex-good"><div class="ex-tag">Good</div><div class="ex-body">...</div></div>
      <div class="ex-card ex-bad"><div class="ex-tag">Bad</div><div class="ex-body">...</div></div>
    </div>
  </div>
  <div class="concept-sub">
    <div class="cs-label"><span class="cs-num">2</span> In practice <a class="cs-more" href="#page-skills-practice">Open full page &rarr;</a></div>
    <div class="dl-grid">
      <div class="dl-col dl-do"><div class="dl-head">Do</div><ul><li>...</li></ul></div>
      <div class="dl-col dl-avoid"><div class="dl-head">Avoid</div><ul><li>...</li></ul></div>
    </div>
  </div>
</div>
```

### Deep-dive page template

```html
<div class="doc-page" id="page-skills-example" data-parent="skills"><!-- add class "api-page" for blue eyebrow -->
  <div class="dp-top">
    <a class="dp-back" href="#skills"><span class="dpb-arrow">&larr;</span> Back to the guide</a>
    <a class="dp-cross" href="#page-skills-practice">In practice &rarr;</a>
  </div>
  <div class="dp-eyebrow">Example &middot; Agent Skills</div>
  <h1 class="dp-title">The <em>shape</em> of a skill</h1>
  <p class="dp-lede">One-paragraph framing.</p>
  <hr class="dp-rule">
  <div class="we we-good"><div class="we-head"><span class="we-badge">Good</span><span class="we-name">...</span></div>
    <div class="we-body"><div class="we-sample"><pre><code>...</code></pre></div>
      <div class="we-notes"><div class="wn"><strong>Point.</strong> Why<a class="src" href="#ref-N">[N]</a>.</div></div></div></div>
  <!-- more .we ... end with a callout -->
  <div class="dp-foot"><a class="dp-back" href="#skills">&larr; Back to the guide</a></div>
</div>
```

Page-id scheme: `#page-{key}-example` and `#page-{key}-practice`, with `data-parent="{section-id}"` so the router can re-highlight the parent nav item. Keep one short `key` per concept.

## Nav + page-id + references

The left nav lists sections, each with two `.ng-sub` sub-links routing to the Example and In Practice pages. The references live in an ordered list at the bottom of the guide; each entry is `<li id="ref-N">`, and inline citations are `<a class="src" href="#ref-N">[N]</a>`. Label secondary sources as "secondary" in the reference text so the sourcing tier is visible.

## In-app hash router

Wrap the guide content in `<div id="guide-view">`. Deep-dive pages are siblings (each `.doc-page`). `body.paged` hides the guide and shows the active page.

```css
.doc-page { display: none; }
/* Hide the guide AND any sibling that lives OUTSIDE #guide-view. A references
   section rendered after #guide-view is the classic miss: without naming it
   here it stays visible under every deep-dive page. */
body.paged #guide-view, body.paged #references { display: none; }
body.paged .doc-page.active { display: block; animation: dp-in .22s ease both; }
body.paged main { padding-top: 40px; }  /* if main has 0 top padding for a bleeding hero */
```

```js
function isPageHash(h){ return /^page-/.test(h || ''); }
function showPage(id){
  document.querySelectorAll('.doc-page').forEach(p => p.classList.toggle('active', p.id === id));
  document.body.classList.add('paged');
  const page = document.getElementById(id);
  const parent = page ? page.dataset.parent : null;
  // Light up BOTH the deep-dive's own sub-link AND its parent section link, so a
  // reader on a deep-dive sees exactly where they are. (setActive alone lights only one.)
  let sub = null;
  document.querySelectorAll('.ng').forEach(a => {
    const h = a.getAttribute('href');
    a.classList.toggle('active', h === '#'+id || (!!parent && h === '#'+parent));
    if (h === '#'+id) sub = a;
  });
  // Reveal the active sub-link if the sidebar is scrolled past it (long navs hide it).
  const side = document.querySelector('.side');
  if (sub && side) {
    const ar = sub.getBoundingClientRect(), sr = side.getBoundingClientRect();
    if (ar.top < sr.top || ar.bottom > sr.bottom) side.scrollTop += (ar.top - sr.top) - 60;
  }
  window.scrollTo(0, 0);
}
function showGuide(sectionId){
  document.body.classList.remove('paged');
  document.querySelectorAll('.doc-page').forEach(p => p.classList.remove('active'));
  if (sectionId) document.getElementById(sectionId)?.scrollIntoView();
}
function route(h){ isPageHash(h) ? showPage(h) : showGuide(h); }
window.addEventListener('hashchange', () => route(location.hash.slice(1)));
route(location.hash.slice(1));
```

Pause scroll-spy while `body.paged` (early-return in the spy function).

### Search that spans the deep-dive pages (and opens them)

A guide whose deep-dives hold most of the detail should search them too, not just the visible guide. Highlight in `#guide-view` first; if there is a guide hit, stay and scroll to it; if the only matches are on hidden pages, `showPage()` the first matching page and note it in the status ("N matches (opened a deep-dive page)"). Reject only `script`, `style`, and `pre` nodes, not `.doc-page`.

**Tear down highlights cleanly, or repeated searches leak DOM.** The trap: wrapping each matched text node in an outer `<span>` (or `innerHTML`-replacing it) leaves that wrapper behind, because teardown only unwraps the inner `.search-hit`. Over many searches the orphan wrappers accumulate and fragment the text. Fix: splice matches in with a `DocumentFragment` of `[text, span.search-hit, text, ...]` and **no outer wrapper**, so teardown (`replace each .search-hit with its text node, then parent.normalize()`) restores the original DOM exactly. Using `textContent` on the hit span (not `innerHTML`) also sidesteps escaping. Verify with a browser check: run N search/clear cycles and assert total `<span>` count returns to baseline (growth 0).

## Build order tip

Build and verify ONE concept end to end (card + both deep-dive pages + nav sub-links + routing) before scaling to all concepts. A broken router or anchor scheme is far cheaper to fix at 1 concept than at 29.
