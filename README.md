# Claude Skills

A working collection of [Claude Code skills](https://code.claude.com/docs/en/skills): each folder
is one skill, a `SKILL.md` with YAML frontmatter plus any reference files it reads on demand. The
frontmatter description is what Claude sees every session; the body loads only when the skill is
invoked (`/skill-name`) or when Claude decides it applies.

**Install:** copy a folder into `~/.claude/skills/` (all projects) or `.claude/skills/` (one
project). No build step, no dependencies beyond what a given skill documents.

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

## Decks

| Skill | What it does |
|---|---|
| [conference-talk-deck](conference-talk-deck/) | Interviews you, then generates a self-contained offline HTML slide deck with author mode |
| [qa-deck](qa-deck/) | Two-track QA on a .pptx: renders every slide for visual defects, and checks every verifiable claim against source material |

## Personal and meta

| Skill | What it does |
|---|---|
| [personal-skill](personal-skill/) | Tailors my resume to a specific job posting (personal; kept as a worked example) |
| [toolbox](toolbox/) | Index of the hand-typed skills: what each is for and when to reach for it |
| [writing-great-skills](writing-great-skills/) | Reference for writing and editing skills well: the vocabulary and principles that make a skill predictable |

## Credits

`codebase-design`, `prototype`, `resolving-merge-conflicts`, `setup-matt-pocock-skills`, and
`writing-great-skills` are adapted from [mattpocock/skills](https://github.com/mattpocock/skills).
Everything else grew out of daily use.

## License

[MIT](LICENSE)
