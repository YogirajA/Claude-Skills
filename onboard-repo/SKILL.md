---
name: onboard-repo
description: >-
  Onboard Claude onto a code repository so it holds durable, verified context. Explores the repo
  first, lets the user interrogate what it learned, asks only the questions the code cannot answer,
  verifies the test and build commands actually run, then writes a short CLAUDE.md, a project wiki
  that survives a cold-context check, and the repo's enforced .claude/ harness (settings, rules,
  hooks) built from those findings. Use when arriving at an unfamiliar codebase, when a repo
  has no CLAUDE.md and no knowledgebase/, or when the user says "onboard Claude on this repo", "get
  up to speed on this codebase", "learn this repo", "set this repo up for Claude", or "build a wiki
  for this repo". Runs once per repo to establish context. Do NOT use for querying an existing wiki
  (that is read-wiki), for ingesting a single source or linting a wiki (that is write-wiki), for
  interviewing the user about work they want built (that is spec-interview), or for teaching the
  user one file, PR, or concept (that is explain-yogi-like-he-is-5).
---

# onboard-repo

Produces five things and no product code: a **verified feedback loop** (commands actually executed,
with known pass and fail signatures), a **CLAUDE.md block** capped at 40 lines, **wiki pages** that
survive a cold-context check, **your calibration** (where Claude is reliable on this repo and where
it is not), and a **`.claude/` harness** built from those findings. Writing features is out of
scope. This skill ends at verified artifacts and hands off.

## Before you start

**Working directory must be the repo root.** If it is not, say so and stop.

**Infer the repo type, then confirm in one line. Do not ask cold.** Run
`git log --format='%ae' | sort | uniq -c | sort -rn | head -5` and compare the plurality author
against `git config user.email`. If they match, use `references/question-bank-yours.md`; otherwise
`references/question-bank-client.md`. Confirm in a sentence: "Most commits here are yours, so I am
treating this as your repo. Correct me if not." With no git history, ask outright and record that
churn and authorship are unavailable. This applies to yourself the rule Phase 2 imposes: earn the
question by showing the attempt.

**Resume detection.** If `knowledgebase/wiki/repo-onboarding.md` exists, read it, report the last
checkpoint, and offer: resume, re-run one named phase, or full refresh.

**A repo onboarded before the harness existed is the common case.** If the wiki is present but
`.claude/HARNESS.md` is not, say so in the same breath as the resume offer and recommend re-running
**Phase 4b alone**. Phases 0 to 3 are already on record in the wiki, so 4b reads the verified loop
from `verified-loops.md` and the danger zones from `danger-zones.md` rather than re-deriving them.

## The phase machine

| # | Phase | Who acts |
|---|---|---|
| 0 | Recon | Claude alone. Asks nothing |
| 1 | You interrogate Claude | User asks, Claude answers, user grades |
| 2 | Claude interrogates you | Earned questions only |
| 3 | Wire the loop | Discover, then actually execute |
| 4 | Write artifacts | CLAUDE.md block plus wiki via write-wiki |
| 4b | Wire the harness | Interview, then `.claude/`. Skippable, and runnable alone |
| 5 | Fresh-context eval | One subagent, artifacts only |

## Checkpoint protocol

Every phase ends the same way. Report what is now held, state what the next phase costs in time and
attention, then stop and wait for one word:

- **go** proceed to the next phase
- **stop** write the checkpoint and exit cleanly, resumable later
- **deeper** repeat the **current** phase with a wider budget before advancing

**Hard rule: every checkpoint leaves an artifact.** No phase may exit with zero output. If the user
stops after Phase 1, the recon map and calibration so far are already written to
`knowledgebase/wiki/repo-onboarding.md`. Append one line to `knowledgebase/log.md` each checkpoint.

Depth is emergent from this protocol. There is no quick or deep mode flag. Do not add one.

## Phase 0: Recon

Explore alone. **Ask the user nothing in this phase.** Work `references/recon-checklist.md`:

1. A **recon map**, presented in session.
2. An **unknowns ledger**: what you could not determine, and specifically what you tried.

Phase 2 may draw questions only from the ledger. That is what makes its questions earned.

Above roughly 2,000 source files, cover the import spine only and **say that you did**. Silent
truncation reads as coverage and is worse than admitting the gap. If workspace manifests are present
(`pnpm-workspace.yaml`, `turbo.json`, `lerna.json`, Cargo workspace, `go.work`), stop and make the
user scope to one package first.

## Phase 1: You interrogate Claude

Load the bank for the detected repo type and offer roughly 10 candidates tuned to what recon found.
**Offer a menu. Do not run the questions yourself.** The point of this phase is that the user
calibrates against you, and that only happens if they are the one asking.

Self-score each answer **cold-solid** (from exploration, verifiable), **hedged** (partial,
assumptions stated), or **blocked** (could not determine). Then **ask the user to override the
score**: their verdict is the real signal, since your confidence about a repo you met twenty minutes
ago is not worth much. Record `| question | self-score | user verdict | note |`.

The most valuable row is **confidently wrong**: self-score `cold-solid`, user verdict incorrect.
Flag those; they drive Phase 5's questions and the `prompting-this-repo` page. Every `blocked` item
is copied into the unknowns ledger.

## Phase 2: Claude interrogates you

Draw only from the unknowns ledger and Phase 1's `blocked` rows. Every question must arrive in this
shape or not be asked at all:

    Q:               <the question>
    Tried:           <specific files, searches, history you checked>
    Blocked because: <why the code cannot answer this>

If you cannot fill both lower lines, the question is not earned. Go find the answer instead.

Ask 5 to 7 per pass, one at a time. `deeper` buys another pass. Legitimate categories, all things
code genuinely cannot tell you: intent behind a decision and what was rejected; deprecated code
still present and still looking alive; what is load-bearing in production, especially where
untested; ownership and what is contentious; external constraints such as compliance or client
rules; and what is about to change, so the wiki does not document a moving target.

**"I don't know" is a valid answer.** Record it to the open-questions list. On client work that list
is often the most useful thing handed back.

**Surface contradictions, do not resolve them silently.** When an answer conflicts with recon, say
so, record both, and mark which one the wiki asserts and why. The code is sometimes current and the
memory sometimes a year stale.

## Phase 3: Wire the loop

Not "find the test command". **Run it.** The deliverable is a verified command, not a documented
one, and this phase has the largest effect on every later result.

1. **Present the candidates recon collected and get approval before executing anything.** On a
   client repo a stray script has real side effects.
2. **Execute each approved candidate.** Record exact command, working directory, runtime, and what
   pass and failure each look like.
3. **Triage failures** into "broken in this environment, here is the missing setup" versus "broken,
   period". Very different consequences; never merge them.
4. **Check for a screenshot path** on web or app work (Puppeteer or Playwright MCP, headless
   script) and record its absence as a gap. **Do not write `settings.json` here.** Record which
   commands ran and which are read-only; Phase 4b turns that into a permissions allow-list after
   the user has agreed to it.

**Never execute** anything matching deploy, publish, migrate, push, or release, even under blanket
approval, unless the user names that exact command in that message.

**If nothing runs, that is the finding.** Write it up as the top gap. A repo with no feedback loop
is precisely where Claude produces confident garbage, so naming that is the most valuable thing this
phase can do.

## Phase 4: Write artifacts

**Save the source first:** the recon map plus the full Q&A transcript to
`raw/onboarding-<YYYY-MM-DD>.md`, immutable. Then invoke **write-wiki** to synthesize pages from it.
Do not create wiki structure yourself; bootstrap, page layout, `index.md`, and the global registry
all belong to write-wiki. On a re-run use its **update** operation, not ingest, so pages are revised
rather than duplicated.

Pages: `architecture` (cleaned recon map), `verified-loops` (Phase 3 commands with pass and fail
signatures), `prompting-this-repo` (calibration), `decisions` (Phase 2 harvest: intent, what was
rejected, deprecated zones), `danger-zones` (load-bearing, untested, high-churn), `repo-onboarding`
(state: phase progress, eval results, open questions), plus one entity page per spine module.

**The CLAUDE.md block: hard cap 40 lines, count before writing.** Overflow moves to the wiki, never
solved by trimming with judgment. In priority order: (1) verified commands from Phase 3, exact
invocation and working directory, the highest value per token in the whole set; (2) three to five
distilled calibration rules, imperative form; (3) one pointer to `./knowledgebase/index.md`; (4) if
Phase 4b runs, one pointer to `.claude/HARNESS.md`. Nothing else earns a place. **If CLAUDE.md already exists, propose a diff and wait. Never overwrite.**

## Phase 4b: Wire the harness

Phases 1 to 4 wrote what Claude should *know*. This phase writes what the repo *enforces*:
`.claude/settings.json`, `rules/`, `hooks/`, `agents/`, and a `HARNESS.md` manifest.

**Run no new recon.** Phases 0 to 3 already produced what a harness needs and cannot otherwise get:
commands actually executed, paths that are load-bearing, and the corrections the user had to make.
That inheritance is the entire justification for this phase.

Anthropic's docs, Boris Cherny and Matt Pocock all warn against config you have not earned. Their
real target is **config nobody can audit later**. Three rules close that hole, and are not optional:

1. **Nothing is installed without an explicit yes.** `library/` is a menu, never a default
2. **Every item gets a `HARNESS.md` entry** with the date and the verbatim answer that justified it
3. **Every entry carries a review date**, six months out, with a real checklist

If you cannot write the justification line, do not install the item.

Run the six sections in `references/harness-interview.md` (autonomy, verification, danger zones,
repeated corrections, repeated procedures, knowledge base), leading each with a recommendation drawn
from Phases 0 to 3 and **skipping any section onboarding already settled**. Then follow
`references/harness-build.md` for the mechanism ranking, write order, adaptation and verification.

**Skippable, and runnable alone.** Offer go / skip / later. If this run came through the
`onboard-light` wrapper, the checkpoint is pre-answered **later**: record the skip and move on
without asking. If the user skips, say what they lose:
guardrails stay advisory, and a rule recorded in the wiki is a request the model can decline. On an
already-onboarded repo this phase runs by itself via the resume offer, reading Phases 0 to 3 out of
the wiki instead of re-deriving them.

**Hard rules.** Never duplicate a hook already present at user level, report it as covered. Never
add `permissions.allow` for an unexecuted command, or for anything matching deploy, publish, push,
migrate or release. Merge, never overwrite.

## Phase 5: Fresh-context eval

Same-session quizzing proves nothing: you would answer from files you just read, not from the
artifact. Verification has to run cold. Build 10 to 12 **targeted** questions: every Phase 1
question graded wrong or partly correct, every
answer the user gave in Phase 2 (did the wiki capture it?), and 3 to 5 spine questions from recon.
Then follow `references/eval-rubric.md`: one `general-purpose` subagent, spawned synchronously with
the artifacts inlined into its prompt. **This is the only phase permitted to use a subagent.** Write
results to the `repo-onboarding` page. Do not build a persisted regression suite.

If Phase 4b ran, add two questions the artifacts alone should answer: what is enforced here rather
than merely requested, and what is deliberately not enforced. A harness a cold reader cannot
describe is a harness the next session will violate without noticing.

## Edge cases

| Situation | What you do |
|---|---|
| No test or build command exists | Top finding, not a failed phase. Propose the smallest loop that could exist |
| No git history | Ask repo type outright. Mark churn and authorship **unavailable**, never silently skip |
| Monorepo detected | Stop. Make the user scope to one package or a named subset |
| More than ~2,000 source files | Spine-only recon, and **declare that you truncated** |
| Wiki already exists | Read `repo-onboarding.md`, report last checkpoint, offer resume / one phase / full refresh |
| Wiki exists, no `.claude/HARNESS.md` | Recommend Phase 4b alone. It reads Phases 0 to 3 from the wiki |
| `HARNESS.md` entry past its review date | Ask whether the justification still holds. Removal is the default answer |
| Hook already covered at user level | Do not install a project copy. Report it as covered |
| User answer contradicts recon | Flag it, record both, mark which the wiki asserts and why |
| User does not know either | Valid. Record to the open-questions list |
| Destructive command candidate | Never run under blanket approval. Require it to be named |
| Not in the repo root | Refuse and explain |
