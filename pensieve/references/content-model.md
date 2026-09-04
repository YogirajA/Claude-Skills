# Content model reference

The deep schema for the `STAGES` array and the surrounding regions of `template.html`.
SKILL.md covers the workflow; read this when you are actually filling in content and
need the exact field semantics, token rules, or scene anatomy.

## Table of contents
- [The mental model](#the-mental-model)
- [Page-level regions](#page-level-regions)
- [Phases and the workflow diagram](#phases-and-the-workflow-diagram)
- [The STAGES array](#the-stages-array)
- [Artifact bodies: kind + body](#artifact-bodies-kind--body)
- [Token highlighting](#token-highlighting)
- [Scenes](#scenes)
- [Writing conventions](#writing-conventions)

---

## The mental model

One page is **one ordered journey of stages**. The learner steps (or auto-plays)
through beats. At every beat, four things stay on screen and update together:

1. **Workflow diagram** (top) - the whole arc, with the current step lit. This is
   the takeaway they should remember even if they forget the details.
2. **Progress meter** - a single bar that fills as the learner moves from the
   "before" state to the "after" state.
3. **Action band** - a badge (what kind of beat this is), an actor (who/what acts),
   and one or two sentences of narration.
4. **Expected outcome** - the green box: what they should see if it worked. This is
   the verification habit, baked into every step.

Plus an **artifact** panel (the right two-thirds) that shows the concrete thing for
this beat: a terminal, a file, a tree, or a rich "scene". And an optional
**trainer note** (toggle with N) for the person teaching.

The point of the format: the learner never loses the forest (diagram + meter) while
looking at a tree (the artifact). Keep that contract intact.

---

## Page-level regions

Marked in `template.html` with `<!-- ===== EDIT ===== -->` comments. Fill all of them.

| Region | What goes there |
|---|---|
| `<title>` | Page title, usually the workshop title. |
| `.hero` | Eyebrow (program / session / type), `<h1>` title with `<b>` on the key words, one-sentence through-line in `<p>`. |
| `.cwd` | The "you are here" chip. State the one-time setup or working directory so it never needs re-explaining. |
| `.loop` | The workflow diagram: 2-5 `.lnode` elements. See [phases](#phases-and-the-workflow-diagram). |
| `.meter` | The two end labels: where the learner starts vs where the workshop lands them. |
| `.foot` | The single crystallizing sentence of the lesson. |
| `STAGES` | The journey. The bulk of the work. |
| `sceneHTML()` | One branch per `scene` name used in STAGES. |
| `PH` array | Short phase tag shown on each rail item, indexed by `ph`. |

---

## Phases and the workflow diagram

`ph` (phase) is the spine that links a stage to the diagram and meter.

- **`ph: 0`** = pre-flight. Lights the `.pre` chip. Use for setup, orientation,
  sanity checks: everything before the "real" workflow starts.
- **`ph: 1..N`** = the workflow nodes. `ph: 2` lights node 2 (`data-p="2"`) and marks
  nodes 1 as done.
- **`ph: N+1`** = recap. Lights every node as done at once. The engine computes this
  automatically as `max(data-p) + 1`, so you do not hardcode it.

The `.lnode` count in `.loop` and the `ph` values in STAGES must agree. If you have a
four-step workflow, you have four `.lnode`s with `data-p="1".."4"`, your workflow
stages use `ph: 1..4`, pre-flight stages use `ph: 0`, and the recap uses `ph: 5`.

Multiple stages can share a phase. A "plan" phase might have three stages (propose,
push back, approve) all at `ph: 2`. They all keep node 2 lit.

**`PH` array**: short uppercase-ish tags shown faintly on each rail row, indexed by
`ph`. For a five-phase page: `["setup","read","plan","verify","recap"]`. Index 0 is
the pre-flight tag, the last index is the recap tag.

---

## The STAGES array

Every stage is one object. Fields:

| Field | Type | Notes |
|---|---|---|
| `rail` | string | 3-5 word nav label. Should read as a verb phrase: "Run the tests", "Push back on a gap". |
| `ph` | number | Phase. See above. |
| `badge` | `[variant, TEXT]` | Variant sets the color. TEXT is a short ALL-CAPS tag. See badge variants below. |
| `actor` | string | Who/what acts: a command (`npm test`), a path (`@spec.md`), or an interaction (`you -> Claude`). Rendered monospace. |
| `file` | string | The artifact title-bar text. A filename, or `terminal · cwd foo/`, or a label like "the loop". |
| `clarity` | number 0-100 | Meter fill. Ramp monotonically across the page (6, 14, 24, 40, ... 100). |
| `say` | string | One or two sentences, plain text (no markup, it is set via textContent). The narration. |
| `outcome` | string | The green box. What the learner should observe if the step worked. Plain text. Frame it as something checkable. |
| `note` | `[TAG, body]` | Optional trainer note. TAG is a short label; body is one or two sentences, may contain inline HTML. |
| `kind` + `body` | string + string[] | A code/terminal artifact. See below. |
| `scene` | string | A rich-HTML artifact instead of `kind`+`body`. Names a branch in `sceneHTML()`. |

A stage has **either** `kind`+`body` **or** `scene`, never both.

### Badge variants

| Variant | Color | Use for |
|---|---|---|
| `cmd` | solid blue | A command to run, the active action. |
| `gate` | amber | A checkpoint / decision point / "no further until..." moment (plan mode, a destructive flag, a hard gate). |
| `ok` | green | A success beat, tests passing, "what you carry forward". |
| `check` | indigo | A verification or sanity-check beat (a softer gate). |
| `idea` | grey | Framing, orientation, "the starting point", concepts. |

### A worked stage

```js
{ rail:"Run the tests", ph:3, badge:["ok","TESTS TRACE TO SCENARIOS"],
  actor:"npm test", file:"terminal · cwd app/", kind:"shell", clarity:84,
  say:"Run the test command for your stack. Each test traces back to a numbered scenario in the spec.",
  outcome:"All scenarios pass, each tied to a numbered test. A failure is diagnosed, not papered over.",
  body:[
    "app $ npm test",
    "» ✓ monthly cadence -> 3 child rows, pending   [Scenario 1]",
    "» ✓ duplicate period -> 409, no dup row         [Scenario 2]",
    "  all green",
  ],
  note:["Three failure modes", "A red test means the spec is ambiguous, Claude misread it, or there is a bug. In all three the spec is the contract."] },
```

---

## Artifact bodies: kind + body

`body` is an array of strings, one per rendered line. Each line is HTML-escaped, then
run through `tok()` for highlighting, then animated in with a staggered rise.

**The `» ` prefix**: a line starting with `» ` (right guillemet + space) is the
**emphasised payload line**. The `» ` is stripped and the line gets a tinted
left-border highlight. Use it for the one or two lines per artifact that carry the
point. Do not highlight everything; if all lines are emphasised, none are.

**`kind`** changes the highlighting and a little of the structure:

- **`shell`** - terminal. Lines like `name $ command` get a muted prompt. Lines
  starting with `#` render as muted comments. Lines starting with `> ` (a user turn,
  e.g. a prompt typed to Claude) render in BDD blue.
- **`md`** - markdown / spec. `---` is a frontmatter delimiter; `key: value` at line
  start colors the key purple; `#`..`####` headings are styled by level.
- **`tree`** - a directory tree. Use box-drawing chars `├──  │  └──`. Annotate each
  line with a trailing purpose. Treated like a generic body for tokens.
- **`json`** - JSON output. Quoted keys color blue; `true`/`false` color green.

**Line-continuation**: a trailing `\` reads as a shell continuation and renders fine.
Indent continuation lines (e.g. four spaces) so they are visually subordinate.

---

## Token highlighting

`tok()` applies these automatically inside body lines. You get them for free by
writing the literal text; you rarely need to think about it, but knowing the set
helps you phrase output so it lights up well.

| You write | Renders as |
|---|---|
| `name $ ` at line start (shell) | muted prompt |
| `# comment` at line start (shell) | muted comment |
| `> text` at line start (shell) | BDD-blue user turn |
| `--flag` | purple flag |
| `[doc] [dir] [skill] [cmd] [link] [copy] [note] [ok]` | teal log tag |
| `[warn] [skip] [err]` | amber log tag |
| `[Test 1] [Cap 2] [Scenario 3] [GAP]` | teal callout |
| `MUST SHALL SHOULD MAY` | amber keyword |
| `GIVEN WHEN THEN AND OR` | BDD blue |
| `pending` / `TODO` | amber chip |
| `PASS` | green chip |
| `404 409 500` | red |
| `✓ ✔` / `✗` | green / red mark |
| `->`  `<-`  `&rarr;`  `&larr;` | muted arrow |

Important: body lines are **escaped first**, so write `<`, `>`, `&` literally and
ASCII arrows as `->`. Do NOT write HTML entities like `&rarr;` inside `body` arrays
(they would be double-escaped and show as literal text). Entities are only for
`scene` strings, which are raw HTML.

---

## Scenes

When a beat is conceptual rather than a literal file or terminal, use a `scene`.
`sceneHTML(scene)` is a `switch`-like function: each `if(scene==="name")` returns a
raw HTML string. Scenes are **not** escaped, so write entities (`&rarr;`, `&middot;`,
`&#10003;`) directly.

Three reusable building blocks ship in the template; copy and rename them per page:

- **Two-panel intro** (`"intro"` in the template): `.sc-row` with two `.sc-spec`
  cards and a `.sc-plus` between them, plus a dashed `.sc-overlay` footnote. Good for
  "here are the two things in play before we start".
- **Reference table** (`"reference"`): a `table.ref`. Rows can get `class="hot"` to
  highlight the standout option. Good for a read-from-screen catalog the learner
  returns to.
- **Recap** (the default branch): `.rc-loop` of `.rc-node`s (the workflow re-stated),
  a `.rc-pit` box of common pitfalls, and a `.rc-win` green band with the Monday
  takeaway. Almost every page ends on a recap.

You are free to write entirely new scenes. The CSS class palette available to scenes:
`.sc-cap .sc-row .sc-spec(.feat) .sc-eyebrow .sc-stack .sc-plus .sc-overlay .sc-tag(.live/.none)`
for layout, and `.rc-loop .rc-node .rc-arr .rc-pit .rc-win` for recap-style content,
and `table.ref` for tables. Reuse them before inventing new CSS.

Children of `.code.scene` animate in staggered for the first five elements; keep a
scene to a handful of top-level children so the entrance reads cleanly.

---

## Writing conventions

- **Faithful content above all.** Run the real commands, paste the real output, use
  the real paths and filenames. A workshop that shows invented output loses anyone
  who knows the tool. Grounding in reality is step one of the workflow for a reason.
- **No em dashes anywhere.** Use a comma, colon, period, or "and". This holds for
  titles, narration, notes, code comments, everything.
- **`say` is the voice; `outcome` is the proof; `note` is the aside.** Keep them
  distinct. `say` narrates the action, `outcome` states what success looks like,
  `note` is the thing a trainer adds out loud.
- **Ramp `clarity` monotonically.** It is the felt sense of progress; never let it
  jump backward.
- **One emphasis per artifact.** Use `» ` on the one or two lines that are the point.
- **Rail labels are verbs.** "Run the tests" reads better than "Tests".
- **End on a recap.** Collapse the journey into one frame: workflow, pitfalls, win.
