---
name: geo-content
description: Write or rewrite content optimized BOTH for classic SEO (ranking in Google search) AND for GEO/AEO - Generative / Answer Engine Optimization, i.e. getting quoted and cited by AI answer engines like ChatGPT, Perplexity, Google AI Overviews, and Gemini. Produces answer-first, well-structured, citable content plus an "what I optimized and why" checklist. Use this whenever the user wants a blog post, article, landing page, FAQ, or web copy that needs to rank or get picked up by AI; mentions SEO, GEO, AEO, "answer engine optimization", "generative engine optimization", keywords, search intent, ranking, or being cited by ChatGPT/Perplexity/AI Overviews; or asks to audit or rewrite existing content to perform better in search and AI answers. Trigger even if they only say "write content optimized for AI search" or "help this article rank" without naming GEO or SEO directly.
---

# GEO + SEO content

Write content that does two jobs at once: rank in traditional search (SEO) and get **lifted
and cited by AI answer engines** (GEO/AEO - Generative / Answer Engine Optimization). The two
overlap but aren't identical, and the difference is the point of this skill.

**Why GEO is its own thing.** Classic SEO optimizes a *page* to rank in a list of blue links.
Answer engines (ChatGPT, Perplexity, Google AI Overviews, Gemini) don't show a list; they
synthesize an answer and cite a few sources. To be one of those sources, your content has to
be *extractable*: a model needs to find a self-contained passage that directly answers a
question and is safe to quote. So GEO rewards answer-first structure, modular passages,
explicit facts with attribution, and clear entities - things that aren't required to merely
rank but are required to get cited.

## Step 1 - Gather the brief

Before writing, get these (ask if missing, infer if obvious):

- **Topic** and the **primary query** a reader would type or ask.
- **Audience** and **content type** (blog post, landing page, FAQ, guide, comparison).
- **Must-include facts / stats / sources**, and the brand's **voice**.
- Whether this is **new content** or an **audit / rewrite** of something existing.

## Step 2 - Map intent and questions

Identify the search intent (informational / commercial / transactional / navigational) and the
cluster of related questions real people ask around the topic. Those questions become your
headings, phrased the way people actually ask them.

## Step 3 - Write answer-first, in extractable chunks

- Open with a **direct answer** in the first 1-2 sentences, then a short **TL;DR**.
- Break the body into **modular passages (~40-120 words)** that each stand alone and fully
  answer one sub-question. A model should be able to quote any single passage without needing
  the rest.
- Use **descriptive, question-shaped H2/H3s** that mirror real queries.
- Name **entities explicitly** and **define key terms** inline (answer engines disambiguate by
  entity).
- Back claims with **concrete statistics + attribution**; engines preferentially surface cited
  facts. Use **comparison tables and lists** - they're trivially extractable.
- Write **quotable declarative sentences** - crisp, factual, standalone.
- Show **E-E-A-T**: author / experience signals, real sources, current dates.
- End with an **FAQ** of 3-6 real questions and tight answers (doubles as extractable Q&A and
  supports FAQ schema).

## Step 4 - Layer the SEO mechanics

- Match search intent; cover the topic to a depth that fits the query (don't pad).
- Primary keyword in the **title, H1, URL slug, and first 100 words**, plus **semantic
  variants and related entities** - naturally, no stuffing.
- Logical **heading hierarchy**; scannable formatting; descriptive **image alt text**.
- Suggest **internal links** and one or two authoritative **external links**.
- Provide a **meta title (~55-60 chars)** and **meta description (~150-160 chars)**.

## Step 5 - Deliver content + a "what I optimized" checklist

Output the finished content, then a short checklist covering: primary query + intent, GEO
elements present (answer-first, modular passages, FAQ, stats, table, entities), SEO metadata
(title / meta / slug / headings / links), and **caveats** - anything the user must verify.

## Honesty guardrail

Never invent statistics, studies, or citations to look authoritative. Fabricated facts get a
page filtered out of AI answers and destroy trust. Where a real number or source is needed and
you don't have it, insert a clear placeholder like `[STAT: add source]` and flag it in the
checklist for the user to fill in.

## Audit / rewrite mode

When improving existing content, first note what's already working and the specific gaps
(missing direct answer, buried lede, no extractable chunks, no stats / sources, weak headings,
thin entities, missing metadata). Then rewrite applying Steps 3-4, and list the changes you
made and why.
