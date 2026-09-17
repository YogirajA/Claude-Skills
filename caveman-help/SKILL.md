---
name: caveman-help
description: >
  Quick-reference card for caveman modes, skills and commands.
  Trigger: /caveman-help or "caveman help".
---

# Caveman Help

Display this reference card when invoked. One-shot, do NOT change mode, write flag files, or persist anything. Output in caveman style.

## Modes

| Mode | Trigger | What change |
|------|---------|-------------|
| **Lite** | `/caveman lite` | Drop filler. Keep sentence structure. |
| **Full** | `/caveman` | Drop articles, filler, pleasantries, hedging. Fragments OK. Default. |
| **Ultra** | `/caveman ultra` | Extreme compression. Bare fragments. |
| **Wenyan-Lite** | `/caveman wenyan-lite` | Classical Chinese style, light compression. |
| **Wenyan-Full** | `/caveman wenyan-full` | Full 文言文. Maximum classical terseness. |
| **Wenyan-Ultra** | `/caveman wenyan-ultra` | Extreme. Ancient scholar on a budget. |

Mode stick until changed or session end.

## Skills

| Skill | Trigger | What it do |
|-------|---------|-----------|
| **caveman-explore** | `/caveman-explore` | Read-only repo explorer. Forked haiku subagent return path:line citations only. |
| **cavecrew** | `/cavecrew` | When to delegate to compressed subagent presets: investigator, builder, reviewer. |
| **caveman-compress** | `/caveman-compress <file>` | Compress Markdown, text, Typst and TeX files to caveman prose. Saves ~46% input tokens. |
| **caveman-help** | `/caveman-help` | This card. |

## Deactivate

Say "stop caveman" or "normal mode". Resume anytime with `/caveman`.

## Language

Keep user's language by default. User write Portuguese → reply Portuguese caveman. Compress the style, not the language. Technical terms, code, commands, commit types, and exact error strings stay verbatim unless user ask for translation.

## Default Mode

Upstream plugin's env-var and config-file auto-activation not vendored here; set level per session with `/caveman <level>`.

## More

Full docs: https://github.com/JuliusBrussee/caveman
