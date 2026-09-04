# Claude Skills

A working collection of [Claude Code skills](https://code.claude.com/docs/en/skills): each folder
is one skill, a `SKILL.md` with YAML frontmatter plus any reference files it reads on demand. The
frontmatter description is what Claude sees every session; the body loads only when the skill is
invoked (`/skill-name`) or when Claude decides it applies.

## Install

**As a plugin (recommended).** The repo is a plugin marketplace. Add it once, then install only
the suites a given machine needs:

```bash
claude plugin marketplace add YogirajA/Claude-Skills
claude plugin install kb-wiki@yogi-skills
claude plugin install harness-audit@yogi-skills
```

The nine suites below are separate plugins on purpose. Every skill's frontmatter description
loads into **every session whether or not the skill fires**, so a single 62-skill plugin would
put ~9,260 tokens of standing cost on every repo you open. Installing `kb-wiki` alone costs ~560.
Run `claude plugin details <name>@yogi-skills` to see any suite's exact always-on cost before
installing it.

| Suite | Skills | Always-on |
|---|---:|---:|
| `meta` | 3 | ~360 |
| `token-economy` | 8 | ~540 |
| `kb-wiki` | 3 | ~560 |
| `harness-audit` | 6 | ~770 |
| `engineering-suite` | 15 | ~900 |
| `repo-onboarding` | 4 | ~980 |
| `code-quality` | 6 | ~1,100 |
| `authoring` | 9 | ~1,910 |
| `thinking-and-specs` | 9 | ~2,160 |
| **all nine** | **63** | **~9,260** |

Always-on figures are `claude plugin details` for `harness-audit`, and raw `chars / 4` scaled by
the 1.49 factor calibrated against it for the rest. On-invoke cost (the SKILL.md body) is paid
only when a skill actually fires and is not counted here.

**Or copy by hand.** Each folder is a self-contained skill: drop one into `~/.claude/skills/`
(all projects) or `.claude/skills/` (one project). No build step, no dependencies beyond what a
given skill documents. Do not do both for the same skill: a hand-copied skill and an installed
plugin both register, and you pay the description twice.

**Visual catalog:** [skills-atlas.html](skills-atlas.html) is a single-file field guide to the
whole collection: the three load tiers and their economics, all 56 skills by origin, and the
imports that were refused with reasons. Open it locally in a browser, or via
[githack](https://raw.githack.com/YogirajA/Claude-Skills/main/skills-atlas.html).

A few skills are personal (they carry my name or my resume) and are kept here as worked examples
of the pattern rather than tools you would run as-is.

## Onboarding and repo setup

| Skill | What it does |
|---|---|
| [onboard-repo](onboard-repo/) | Full repo onboarding: recon, mutual interrogation, execution-verified feedback loop, a capped CLAUDE.md, a project wiki that survives a cold-context eval, and an interview-gated `.claude/` harness (settings, path-scoped rules, tested hooks, a `HARNESS.md` manifest with per-item justifications and review dates) |
| [onboard-light](onboard-light/) | The same flow with the harness phase pre-answered "skip": knowledge-only onboarding for repos where `.claude/` is not yours to write |
| [primitive-classifier](primitive-classifier/) | Audits a folder for Claude Code primitives (skills, hooks, MCP, subagents, CLAUDE.md) and classifies each into the primitive that actually fits, as an interactive HTML report |
| [setup-matt-pocock-skills](setup-matt-pocock-skills/) | One-time repo config for the engineering skills: issue tracker, triage labels, domain doc layout |

## Knowledge base (LLM wiki)

| Skill | What it does |
|---|---|
| [write-wiki](write-wiki/) | Ingest sources, update pages, lint, or bootstrap a new wiki; the write half of the LLM-wiki pattern |
| [read-wiki](read-wiki/) | Query the knowledge base before doing work; strictly read-only |
| [wiki](wiki/) | Backward-compatible alias for write-wiki |

## Code quality and review

| Skill | What it does |
|---|---|
| [ponytail](ponytail/) | Forces the laziest solution that works: YAGNI, stdlib before custom code, one line before fifty. Intensity levels: lite, full, ultra |
| [ponytail-review](ponytail-review/) | Diff review focused exclusively on over-engineering: what to delete and what replaces it |
| [ponytail-audit](ponytail-audit/) | Whole-repo version of the same: a ranked list of bloat to delete, simplify, or replace |
| [smells](smells/) | Reviews the current diff for the twelve Fowler code smells, named Fowler-style with concrete fixes |
| [codebase-design](codebase-design/) | Shared vocabulary for designing deep modules: interfaces, seams, testability, AI-navigability |
| [resolving-merge-conflicts](resolving-merge-conflicts/) | Working through an in-progress git merge or rebase conflict |

## Specs, plans, and decisions

| Skill | What it does |
|---|---|
| [spec-interview](spec-interview/) | Interviews you into a written, approved spec instead of prompt-by-prompt iteration |
| [wayfinder](wayfinder/) | Plans work too big for one session as decision tickets on your issue tracker, resolved one at a time |
| [goal-creator](goal-creator/) | Turns rough intent into a `/goal`-ready session goal: verifiable outcome, scope guard, acceptance criteria, explicit authorities |
| [prototype](prototype/) | Throwaway prototype to answer a design question before committing to a direction |
| [mental-models](mental-models/) | Pressure-tests a real decision through named thinking frameworks (inversion, second-order effects, base rates, regret minimization...) and ends with a recommendation |
| [the-llm-council](the-llm-council/) | Five advisors attack a decision from different angles, peer-review each other anonymously, and a Chairman delivers a verdict |
| [scope-creep-check](scope-creep-check/) | A self-awareness brake: names the drift, shows the cost, asks proceed / park / drop, then respects the answer |

## Prompting

| Skill | What it does |
|---|---|
| [prompt-fixer](prompt-fixer/) | Cleans a rough prompt into clear plain English and hands it back to you; no XML, no execution |
| [prompt-optimizer](prompt-optimizer/) | Wraps a messy ask into an XML-structured Claude prompt, validates it with you, then runs it |

## Learning and teaching

| Skill | What it does |
|---|---|
| [explain-yogi-like-he-is-5](explain-yogi-like-he-is-5/) | Deep Socratic teaching session with an incremental mastery loop; teaches rather than summarizes |
| [watch](watch/) | Fetches a YouTube video's transcript and turns it into summaries, timestamped notes, quotes, or answers |
| [field-guide-builder](field-guide-builder/) | Builds a single-file, source-grounded HTML teaching guide with concept hierarchy, citations, and an editorial design system |
| [sdd-workshop-walkthrough](sdd-workshop-walkthrough/) | Generates an animated single-file HTML workshop player with narrated steps and artifact panels |

## Content and validation

| Skill | What it does |
|---|---|
| [geo-content](geo-content/) | Writes content optimized for both classic SEO and AI answer engines (GEO/AEO), with an "what I optimized and why" checklist |
| [anthropic-doc-validator](anthropic-doc-validator/) | Validates claims about Claude Code, the Anthropic API, or SDKs against the latest official docs, with verbatim quotes |
| [excalidraw](excalidraw/) | Generates architecture diagrams as `.excalidraw` files from codebase analysis, with optional PNG/SVG export. Six reference files (JSON format, arrows, colors, validation, export, examples) load only on demand |

## Decks

| Skill | What it does |
|---|---|
| [conference-talk-deck](conference-talk-deck/) | Interviews you, then generates a self-contained offline HTML slide deck with author mode |
| [qa-deck](qa-deck/) | Two-track QA on a .pptx: renders every slide for visual defects, and checks every verifiable claim against source material |

## Engineering and productivity suite (mattpocock/skills)

Adapted from [mattpocock/skills](https://github.com/mattpocock/skills). The issue-tracker skills
(ask-matt, triage, to-spec, to-tickets, implement) work as a set and assume
`setup-matt-pocock-skills` has configured the repo. His `tdd`, `code-review`, `diagnosing-bugs`,
and `handoff` are intentionally omitted: they duplicate superpowers TDD and systematic-debugging,
the bundled `/code-review`, and the remember/handoff system already in use here.

| Skill | What it does |
|---|---|
| [ask-matt](ask-matt/) | Router: which skill in the suite fits your situation |
| [grill-me](grill-me/) | Relentless interview to sharpen a plan; thin wrapper over grilling |
| [grilling](grilling/) | The interview primitive: design-tree questioning in frontier rounds, each question with a recommended answer, facts fetched by subagents |
| [grill-with-docs](grill-with-docs/) | Grilling session that also builds the domain model into `CONTEXT.md` and ADRs |
| [domain-modeling](domain-modeling/) | Actively builds and sharpens a project domain model |
| [improve-codebase-architecture](improve-codebase-architecture/) | Scans the codebase for deepening opportunities, with an HTML report |
| [research](research/) | Investigates questions against primary sources and captures findings |
| [to-spec](to-spec/) | Turns a conversation into a spec published to the issue tracker |
| [to-tickets](to-tickets/) | Breaks plans into tracer-bullet tickets with blocking edges |
| [triage](triage/) | Moves issues through a triage state machine |
| [implement](implement/) | Builds work from specs and tickets, driving TDD and code review |
| [wizard](wizard/) | Generates interactive bash wizards for human-only steps |
| [teach](teach/) | Teaches new skills over multiple sessions in a stateful workspace |
| [to-questionnaire](to-questionnaire/) | Turns open decisions into async markdown questionnaires |
| [wait-what](wait-what/) | Re-pitches a message with missing context in plain English |

## Token economy suite (JuliusBrussee/caveman)

Adapted from [JuliusBrussee/caveman](https://github.com/JuliusBrussee/caveman), the "why use many
token when few do trick" project. Only the MIT-licensed `skills/` surface is copied; the BSL
compression engine, proxy, and cloud skills are not included. Honest caveat from upstream's own
docs: the terse-mode rules cost roughly 1,250 input tokens per turn once active, so net savings can
go negative on short sessions.

The three `cavecrew` subagent presets ship inside [cavecrew/agents/](cavecrew/agents/); copy them
to `~/.claude/agents/` for the cavecrew skill to route to them.

| Skill | What it does |
|---|---|
| [caveman](caveman/) | Ultra-compressed output mode (lite, full, ultra): fluff dies, technical substance stays. Token-aware: no fake abbreviations, no arrow glyphs, grammar kept where mangling saves nothing |
| [caveman-compress](caveman-compress/) | Compresses a CLAUDE.md, todo list, or memory file into caveman format with a readable backup |
| [cavecrew](cavecrew/) | When to delegate to the compressed subagent presets (investigator, builder, reviewer) instead of vanilla Explore: same findings in a third of the main-context tokens |
| [caveman-explore](caveman-explore/) | Haiku-powered read-only explorer returning path:line citations only; for cold-start orientation and broad localization |
| [safe-refactor](safe-refactor/) | Restructure while preserving behavior: verification brackets every structural edit |
| [surgical-patch](surgical-patch/) | Fix at the narrowest responsible layer, with regression proof and preserved surrounding behavior |
| [migration](migration/) | Reversible, compatibility-safe transitions: schema, data, API, config, dependency |
| [caveman-help](caveman-help/) | Quick-reference card for the caveman modes and skills |

## Harness measurement suite (affaan-m/ECC)

Six skills adapted from [affaan-m/ECC](https://github.com/affaan-m/ECC) (MIT), a 286-skill
harness repo. Only these six were taken: the rest was either infrastructure-coupled, duplicated
something already here, or was language and domain filler that would have cost ~14 to 20k tokens
of always-on frontmatter to hold. The full import review, with the measurements behind each
decision, is in the knowledge base as `ecc-import-review.html`.

Two of the six were edited before install, and each records its own change in its frontmatter
`metadata.adapted` field: `loop-design-check` had its description cut from 244 to 136 always-on
tokens, and `gateguard` had its install section rewritten because upstream's hook implementation
was not imported with it.

| Skill | What it does |
|---|---|
| [loop-design-check](loop-design-check/) | The judgement layer for agent loops: a four-condition veto gate on whether to build one at all, a machine-decidable goal test, servo vs regulator typing, then a review against five failure modes and three keep-judgment-with-the-human red lines |
| [skill-comply](skill-comply/) | Measures whether a skill or rule is actually followed: generates a behavioural spec from any .md, generates scenarios at three prompt-strictness levels, runs `claude -p`, classifies the tool trace, and reports a compliance rate. Spends real quota; start with `--dry-run` |
| [context-budget](context-budget/) | Audits context consumption across agents, skills, rules, MCP tool schemas and the CLAUDE.md chain, then ranks fixes by tokens reclaimed |
| [config-gc](config-gc/) | Garbage collection over `~/.claude`: finds stale, orphaned, redundant and low-value items, then walks you through confirm-each deletion |
| [gateguard](gateguard/) | Design for a three-stage fact-forcing gate: deny the first edit, force a named list of facts (importers, affected functions, real data schema, the instruction verbatim), allow the retry. Imported as a design, not a runnable hook |
| [skill-scout](skill-scout/) | Searches local, marketplace, GitHub and web sources before you write a new skill |

## Personal and meta

| Skill | What it does |
|---|---|
| [personal-skill](personal-skill/) | Tailors my resume to a specific job posting (personal; kept as a worked example) |
| [toolbox](toolbox/) | Index of the hand-typed skills: what each is for and when to reach for it |
| [writing-great-skills](writing-great-skills/) | Reference for writing and editing skills well: the vocabulary and principles that make a skill predictable |

## Credits

`codebase-design`, `prototype`, `resolving-merge-conflicts`, `setup-matt-pocock-skills`,
`writing-great-skills`, and the engineering suite section are adapted from
[mattpocock/skills](https://github.com/mattpocock/skills) (MIT). The token economy suite is
adapted from [JuliusBrussee/caveman](https://github.com/JuliusBrussee/caveman) (MIT skills
surface). The harness measurement suite is adapted from
[affaan-m/ECC](https://github.com/affaan-m/ECC) (MIT). `excalidraw` is vendored from
[ooiyeefei/ccc](https://github.com/ooiyeefei/ccc) (MIT). Everything else grew out of daily use.

Third-party work is **copied in, never depended on as a plugin**: this machine installs plugins only
from Anthropic's own repos or mine, so anything useful from elsewhere gets vendored under its licence
with provenance recorded in that skill's frontmatter `metadata` block.

## License

[MIT](LICENSE)
