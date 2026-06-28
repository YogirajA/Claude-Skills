---
name: sdd-workshop-walkthrough
description: >-
  Generate a self-contained, animated, single-file HTML workshop walkthrough in
  the Athena SDD house style (the specworkshop.html / repo.html players): a
  step-by-step player with a workflow diagram, progress meter, narrated action
  band, expected-outcome boxes, a terminal/file/tree/scene artifact panel,
  toggleable trainer notes, autoplay, and keyboard nav. Use this WHENEVER the
  user wants an animated or interactive HTML walkthrough, workshop page, hands-on
  lab page, guided demo, or "click-through" explainer for a tool, script, repo,
  or CLI workflow, and ESPECIALLY when they reference an existing page like
  specworkshop.html or repo.html, say "like that other workshop", "same style",
  "animated HTML for this workshop", "make a repo.html / foo.html for X", or ask
  to turn a set of workshop steps into a playable page. Trigger even if they do
  not say the word "skill". Do NOT use for PowerPoint/Google Slides decks (use a
  pptx skill), for general web apps or dashboards, or for static prose docs.
---

# SDD workshop walkthrough

Build one HTML file that plays a workshop as an animated, steppable journey. The
design system and the player engine are fixed and bundled; your job is to write
faithful, well-paced **content** into a documented data structure. The structure
is the lever, the content is the work.

The output is a single `.html` file with zero dependencies (no build, no network,
no external assets) that opens directly in a browser.

## What you are producing

A page with these always-on parts, all driven by one `STAGES` array:

- a **workflow diagram** of the whole arc, current step lit;
- a **progress meter** filling from a "before" state to an "after" state;
- an **action band**: a colored badge, an actor, and one or two sentences;
- an **expected-outcome** green box for every step (the verification habit);
- an **artifact** panel showing a terminal, file, tree, or rich "scene";
- toggleable **trainer notes**, autoplay, prev/next, and keyboard nav.

See `repo.html` and `specworkshop.html` (if present in the workspace) for finished
examples in two different domains.

## Workflow

### 1. Ground in reality first (do not skip this)

This is the single most important step and the thing that separates a credible
workshop page from a hollow one. Before writing any content, learn the actual
subject the same way a careful author would:

- Read the real files the workshop is about: the script, the repo, the templates,
  the config.
- **Run the real commands** the workshop teaches and capture their **actual
  output**, exact paths, exact filenames, exact log lines. Paste those into the
  artifact bodies verbatim (lightly trimmed for length is fine; invented is not).
- If a command errors or behaves differently on the user's platform, that is
  itself worth a trainer note. Note real caveats (for example, a Windows symlink
  fallback, a UTF-8 console quirk) rather than papering over them.

A room that knows the tool will spot fabricated output instantly. Faithful content
is what earns the page its authority.

### 2. Plan the journey

Decide the workflow's shape before writing stages:

- **How many workflow nodes** (2-5)? These become the diagram. Name them as the
  arc the learner carries away (e.g. Bootstrap, Populate, Brownfield, Commit).
- **Which beats are pre-flight** (`ph: 0`) vs workflow steps (`ph: 1..N`) vs the
  closing **recap** (`ph: N+1`)? Multiple stages can share a phase.
- **What is the before -> after** the meter expresses?
- **One crystallizing sentence** for the footer.

Aim for roughly 8-14 stages: enough to tell the story, few enough to stay crisp.

### 3. Copy the template and fill it in

Copy the bundled template to the destination the user wants (default: a `.html`
named after the workshop, in the workshop's own directory):

```
cp <skill-dir>/assets/template.html <target>/<name>.html
```

(On Windows PowerShell: `Copy-Item <skill-dir>\assets\template.html <target>\<name>.html`.)

Then edit it. Every region you must touch is flagged with an
`<!-- ===== EDIT ===== -->` comment:

- the `<title>` and `.hero` (eyebrow, title with `<b>` on key words, through-line);
- the `.cwd` chip (the "you are here" / one-time-setup line);
- the `.loop` workflow diagram (2-5 `.lnode`s; `data-p` must match your `ph`s);
- the `.meter` end labels;
- the `.foot` crystallizing sentence;
- the **`STAGES`** array (the bulk of the work);
- the **`sceneHTML()`** branches for any `scene` names you use;
- the **`PH`** labels array (short phase tag per `ph` index).

**Do not edit** the engine block (everything under "engine (do not edit)"). It
adapts to any node count on its own.

For the exact field semantics of a stage, the `kind`/`body`/`scene` options, the
badge variants, the `» ` emphasis prefix, the token-highlighting set, and the
reusable scene blocks, read **`references/content-model.md`**. Keep it open while
you write stages; it is the authority on every field.

### 4. Render-check before handing it back

A single-file HTML player is easy to get subtly wrong (a stray quote in `body`, a
`scene` name with no matching branch, a `ph` that does not line up with the nodes).
Verify visually rather than trusting the markup.

First, a fast syntax gate on the embedded script:

```bash
python -c "import re,sys; m=re.search(r'<script>(.*)</script>', open(sys.argv[1],encoding='utf-8').read(), re.S); open('/tmp/_chk.js','w',encoding='utf-8').write(m.group(1))" <name>.html && node --check /tmp/_chk.js && echo "JS OK"
```

Then screenshot a few representative stages with Playwright (Python or Node,
whichever is available) and actually look at them:

```python
from playwright.sync_api import sync_playwright
from pathlib import Path
url = Path("<name>.html").resolve().as_uri()
with sync_playwright() as p:
    pg = p.chromium.launch().new_page(viewport={"width":1360,"height":1024})
    pg.goto(url); pg.wait_for_timeout(600); pg.screenshot(path="_s0.png")
    for i in (2, 4, 7):                       # jump to a few stages via the rail
        pg.eval_on_selector_all(".ri", f"els => els[{i}] && els[{i}].click()")
        pg.wait_for_timeout(900); pg.screenshot(path=f"_s{i}.png")
```

Read the PNGs. Confirm: the diagram lights the right node per phase, highlighted
(`» `) lines stand out, tokens are colored, scenes render (no raw HTML, no missing
branch), and nothing overflows. Fix and re-shoot until it is clean, then delete the
temp PNGs and the `_chk.js`.

## Conventions that matter

- **Faithful content.** Real commands, real output, real paths. This is non-negotiable.
- **No em dashes anywhere** (titles, narration, notes, comments). Use a comma,
  colon, period, or "and".
- **Ramp `clarity` monotonically** (e.g. 6, 14, 24, 40, ... 100) so progress feels real.
- **One emphasis per artifact**: `» ` on the one or two lines that are the point.
- **`say` narrates, `outcome` proves, `note` is the trainer aside.** Keep them distinct.
- **End on a recap** that re-states the workflow, lists common pitfalls, and gives
  the one-sentence Monday takeaway.
- **Match the domain's vocabulary.** If the workshop targets a specific stack or
  team, write in that idiom, not a generic one.

## Files in this skill

- `assets/template.html` - the player: full CSS design system + JS engine +
  a documented `STAGES` skeleton with one example of every stage kind and the three
  reusable scenes. Copy this and fill it in.
- `references/content-model.md` - the complete field-by-field schema, token rules,
  scene anatomy, and writing conventions. Read it while authoring stages.
