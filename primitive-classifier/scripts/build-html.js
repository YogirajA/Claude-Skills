#!/usr/bin/env node
// build-html.js
//
// Take a JSON audit data file, substitute it into the template, write a
// self-contained HTML report.
//
// Usage:
//   node build-html.js --data audit.json --out report.html
//   node build-html.js --data audit.json --out report.html --template path/to/template.html
//   node build-html.js --validate-only --data audit.json
//
// The template ships with the skill and lives at ../template/primitives-categorization.template.html
// relative to this script. The script does targeted JS-literal replacement at marked sites:
//   const NAME = /*<<DATA:key>>*/[ ... ];
// Plus tagged HTML replacement for hero text and verdicts:
//   <!--<<HERO:title>>-->...<!--<</HERO>>-->
//   <!--<<HERO:lede>>-->...<!--<</HERO>>-->
//   <!--<<HERO:meta>>-->...<!--<</HERO>>-->
//   <!--<<VERDICTS>>-->...<!--<</VERDICTS>>-->
// Plus optional phase plan:
//   <!--<<PHASES>>-->...<!--<</PHASES>>-->

const fs = require('node:fs');
const path = require('node:path');

const args = parseArgs(process.argv.slice(2));

if (args.help || (!args.data && !args['validate-only'])) {
  printHelp();
  process.exit(args.help ? 0 : 1);
}

const dataPath = path.resolve(args.data);
const data = JSON.parse(fs.readFileSync(dataPath, 'utf8'));

const errors = validate(data);
if (errors.length) {
  console.error('Validation errors:');
  for (const e of errors) console.error('  - ' + e);
  process.exit(2);
}

if (args['validate-only']) {
  console.log('Validation passed.');
  process.exit(0);
}

const templatePath = args.template
  ? path.resolve(args.template)
  : path.resolve(__dirname, '..', 'template', 'primitives-categorization.template.html');

if (!fs.existsSync(templatePath)) {
  console.error('Template not found at ' + templatePath);
  process.exit(3);
}

let html = fs.readFileSync(templatePath, 'utf8');

// 1) JS-literal replacements at /*<<DATA:key>>*/ markers
const dataKeys = ['buckets', 'items', 'sources', 'decisions', 'disclaimers', 'specificProvenance'];
for (const key of dataKeys) {
  if (data[key] !== undefined) {
    html = replaceJsLiteral(html, key, data[key]);
  }
}

// 2) Hero text
html = replaceTagged(html, 'HERO:title', escapeHtml(data.title || 'Primitive audit'));
html = replaceTagged(html, 'HERO:lede', data.lede || '');
html = replaceTagged(html, 'HERO:meta', data.meta || '');

// 3) Verdicts
html = replaceTagged(html, 'VERDICTS', renderVerdicts(data.verdicts || []));

// 4) Phases (optional)
if (data.phases && data.phases.length) {
  html = replaceTagged(html, 'PHASES', renderPhases(data.phases));
} else {
  // leave the existing phases content if no override
}

// Write
const outPath = args.out
  ? path.resolve(args.out)
  : path.resolve(path.dirname(dataPath), 'primitives-categorization.html');

fs.writeFileSync(outPath, html, 'utf8');
console.log('Wrote ' + outPath + ' (' + html.length + ' bytes)');

// =====================================================================
// Helpers
// =====================================================================

function parseArgs(argv) {
  const out = {};
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a.startsWith('--')) {
      const key = a.slice(2);
      const next = argv[i + 1];
      if (next && !next.startsWith('--')) {
        out[key] = next;
        i++;
      } else {
        out[key] = true;
      }
    }
  }
  return out;
}

function printHelp() {
  console.log(`
build-html.js, render the primitive audit HTML from a JSON data file.

Usage:
  node build-html.js --data <file.json> [--out <file.html>] [--template <file.html>]
  node build-html.js --validate-only --data <file.json>

Options:
  --data            Path to JSON data (matches reference/output-shape.md schema)
  --out             Output HTML path (default: primitives-categorization.html next to data file)
  --template        Override template path (default: bundled template)
  --validate-only   Run validator, exit 0 if data is well-formed, 2 otherwise
  --help            Show this help
  `.trim());
}

function validate(data) {
  const errs = [];
  if (!data.title) errs.push('title is required');
  if (!Array.isArray(data.buckets) || data.buckets.length !== 6) {
    errs.push('buckets must be an array of 6 entries (claudemd, subagents, skills, hooks, settings, mcp)');
  }
  const validBucketIds = new Set((data.buckets || []).map(b => b.id));
  if (!Array.isArray(data.items)) {
    errs.push('items must be an array');
  } else {
    for (const it of data.items) {
      if (!it.name) errs.push('item missing name');
      if (!validBucketIds.has(it.recommendedBucket)) {
        errs.push(`item "${it.name}" recommendedBucket "${it.recommendedBucket}" not in buckets`);
      }
      if (!['correct', 'borderline', 'misplaced', 'stub', 'missing'].includes(it.status)) {
        errs.push(`item "${it.name}" status "${it.status}" invalid`);
      }
    }
  }
  if (!Array.isArray(data.sources)) errs.push('sources must be an array');
  const validSourceIds = new Set((data.sources || []).map(s => s.id));
  if (Array.isArray(data.decisions)) {
    for (const d of data.decisions) {
      if (d.cite && d.cite.source && !validSourceIds.has(d.cite.source)) {
        errs.push(`decision cite "${d.cite.source}" not in sources`);
      }
    }
  }
  if (!Array.isArray(data.verdicts) || data.verdicts.length < 2 || data.verdicts.length > 6) {
    errs.push('verdicts should have 2 to 6 entries (4 is the sweet spot)');
  }
  return errs;
}

function escapeHtml(s) {
  if (typeof s !== 'string') return '';
  return s
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}

function renderVerdicts(verdicts) {
  return verdicts.map(v => {
    const tone = ['warn', 'miss', 'good', 'info'].includes(v.tone) ? v.tone : '';
    const cls = tone && tone !== 'info' ? ` ${tone}` : '';
    return `      <div class="verdict${cls}">
        <h3>${escapeHtml(v.title || '')}</h3>
        <p>${v.body || ''}</p>
      </div>`;
  }).join('\n');
}

function renderPhases(phases) {
  return phases.map(p => {
    const items = (p.items || []).map(i => `        <li>${i}</li>`).join('\n');
    return `      <h3>${escapeHtml(p.title || '')}</h3>
      <ul>
${items}
      </ul>`;
  }).join('\n\n');
}

// Replace a tagged HTML region:
// <!--<<TAG>>-->...content...<!--<</TAG>>-->
function replaceTagged(html, tag, content) {
  const open = `<!--<<${tag}>>-->`;
  const close = `<!--<</${tag.split(':')[0]}>>-->`;
  const i = html.indexOf(open);
  if (i === -1) return html;
  const j = html.indexOf(close, i + open.length);
  if (j === -1) return html;
  return html.slice(0, i + open.length) + '\n' + content + '\n' + html.slice(j);
}

// Replace a JS literal that follows a marker:
// /*<<DATA:key>>*/[ ... ]   or   /*<<DATA:key>>*/{ ... }
// Uses a JS-aware bracket matcher that handles strings, regexes, and comments.
function replaceJsLiteral(html, key, value) {
  const marker = `/*<<DATA:${key}>>*/`;
  const idx = html.indexOf(marker);
  if (idx === -1) {
    console.warn(`marker not found: ${marker}`);
    return html;
  }
  let p = idx + marker.length;
  while (p < html.length && /\s/.test(html[p])) p++;
  if (html[p] !== '[' && html[p] !== '{') {
    console.warn(`expected [ or { after ${marker}, got "${html[p]}"`);
    return html;
  }
  const open = html[p];
  const close = open === '[' ? ']' : '}';
  let depth = 1;
  let q = p + 1;
  let inString = null;
  let escape = false;
  while (q < html.length && depth > 0) {
    const c = html[q];
    if (escape) { escape = false; q++; continue; }
    if (c === '\\') { escape = true; q++; continue; }
    if (inString) {
      if (c === inString) inString = null;
      q++;
      continue;
    }
    if (c === "'" || c === '"' || c === '`') {
      inString = c;
      q++;
      continue;
    }
    if (c === '/' && html[q + 1] === '/') {
      while (q < html.length && html[q] !== '\n') q++;
      continue;
    }
    if (c === '/' && html[q + 1] === '*') {
      q += 2;
      while (q < html.length - 1 && !(html[q] === '*' && html[q + 1] === '/')) q++;
      q += 2;
      continue;
    }
    if (c === open) depth++;
    if (c === close) depth--;
    q++;
  }
  if (depth !== 0) {
    console.warn(`unbalanced brackets after ${marker}`);
    return html;
  }
  // Replace [p, q) with stringified value
  const json = JSON.stringify(value, null, 2);
  return html.slice(0, p) + json + html.slice(q);
}
