# anthropic-doc-validator skill

A reusable Claude Code skill that validates claims about Claude Code, the Anthropic API, or Anthropic SDKs against the latest official documentation. Reports findings as a structured markdown report and does not modify the original content unless asked.

## Install

Copy the folder to one of these locations, then restart any open Claude session.

| Scope | Where to copy | Effect |
|---|---|---|
| **User (recommended)** | `~/.claude/skills/anthropic-doc-validator/` | Available in every Claude Code session on this machine. |
| **Project** | `<your-repo>/.claude/skills/anthropic-doc-validator/` | Available only in this repo. Commit if you want the team to use it. |

PowerShell one-liner for user-level install:

```powershell
Copy-Item -Recurse -Force "$PSScriptRoot" "$env:USERPROFILE\.claude\skills\anthropic-doc-validator"
```

POSIX one-liner:

```bash
cp -r ./anthropic-doc-validator ~/.claude/skills/
```

## Use it

Once installed, ask Claude things like:

- "Validate this README against the current Anthropic docs."
- "Is this slide deck still accurate? Check it against the latest Claude Code documentation."
- "Audit the code samples in `examples/agent-sdk.py` against the current Anthropic SDK docs."
- "Verify the claims in `docs/onboarding.md` are still current."

Claude will fetch the relevant doc pages, quote them verbatim, and produce a confirmed / refuted / stale / not-documented / ambiguous breakdown for each claim it identified.

## What it covers

| Domain | Covered? |
|---|---|
| Claude Code CLI (code.claude.com) | Yes |
| Anthropic API and SDKs (docs.anthropic.com) | Yes |
| Anthropic GitHub repos (issues, feature requests) | Yes, as a fallback signal |
| Third-party blogs and community wikis | Discovery aid only, not authoritative |

## How it works under the hood

1. Identifies discrete factual claims in the content.
2. Maps each claim to the most relevant Anthropic doc URL (using the index baked into `SKILL.md`).
3. WebFetches that page with a narrow, quote-asking prompt.
4. Compares each claim to the verbatim quote.
5. Reports findings, grouped by severity (refuted first).

## Customizing

The doc URL index lives in `SKILL.md` under the "Anthropic documentation URL index" section. Add URLs there for products or pages you commonly validate against.

## Known limits

- WebFetch can hit caching layers; if a recent doc change isn't reflected, fall back to `WebSearch` for fresher signal.
- Some Claude Code docs are long; the skill should always ask for a specific quote, not a summary.
- This skill validates against PUBLIC docs only. Internal/preview features won't appear in the validation.
