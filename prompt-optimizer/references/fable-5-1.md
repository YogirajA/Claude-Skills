# Target model: Claude Fable 5.1 and Claude Mythos 5.1

Source: [Prompting Claude Fable 5.1](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-1).
Snippets in `text` blocks are quoted from that page and meant to be pasted verbatim, so their
punctuation is left exactly as published.

Existing Fable 5 prompts perform well without changes. Default effort is `high`. This is the longest
of the model guides: start from the symptom you actually observe rather than applying everything.

## Symptom index

| What you see | Section |
|---|---|
| Latency or cost higher than the task warrants | Effort |
| Agent goes quiet for minutes during long tool chains | Progress updates |
| One tool call per turn in coding or computer-use loops | Tool-call batching |
| A 400 on replayed thinking blocks, or cache thrash | Append-only history |
| Prose is dense, long sentences, few paragraph breaks | Writing density |
| Too little bold, few headers or lists | Formatting in chat |
| Source passages reproduced unmarked when summarizing | Quoting sources |
| "Next, I'll…" or "Shall I apply this?" instead of doing it | Finish the whole task |
| Unrequested fixes, extra test files | Keep changes to scope |
| Answers from memory instead of searching, at `low` effort | Search triggering |
| Spurious refusals | Safeguard false positives |
| Whole-file rewrites for small edits | Targeted edits |
| Long wait then a truncated deliverable at `xhigh`/`max` | Room for long outputs |

## Subtract before you add

| Remove | Why |
|---|---|
| "Hold all findings for the final response" and similar narration suppressors | Written for older, chattier models. Fable 5.1 already under-narrates. |
| Anti-formatting rules ("no bullets", "no bold") | It already leans sparse. These compound. Replace with a rule saying when formatting *is* appropriate. |
| Client-side history rewriting: injecting and removing per-turn reminders, summarizing older turns in place, changing the system prompt mid-session | Breaks thinking-block binding (400) and restarts the prompt cache. |

## Effort

Start at `high`, then sweep `low`, `medium`, `xhigh`, `max` against your own evals. Re-run the sweep
even if you ran one on Fable 5: effort names do not correspond to the same amount of thinking across
models. At `medium`, results roughly match Fable 5 at lower cost. At `low` it is often competitive
with Opus and Sonnet models on cost per task while scoring higher, so include it wherever you would
otherwise run a smaller model at higher effort.

Two effort-specific behaviours have their own sections below: search triggering at `low`, and long
outputs at `xhigh`/`max`.

## Progress updates

It writes fewer user-facing updates during long tool-calling turns than Fable 5, more so at higher
effort and in longer chains.

**Check the plumbing first.** Its short between-tool notes come back as progress-update `thinking`
blocks, and those are **empty under the default `thinking.display` of `"omitted"`**. Set
`display: "updates"` (beta header `thinking-display-updates-2026-08-18`) and render each non-empty
block as a status line, or `"summarized"`. If you are not requesting them, they are not reaching
users at all. Then audit the prompt for suppressors. Only then add:

```text
Before you start, say in a line what you're about to do; brief updates while you work help the user follow along. Close with a short recap that stands on its own — what you found, what you did, and what's next — so a reader who only sees the last message has the full picture.
```

If your UI collapses or hides tool output, say so, or it will run commands to "show" the user things
your UI never displays. Deliver as a turn-scoped system message (`clear_at: "next_user_message"`):

```text
Only you see that command's output — the user's terminal shows at most a few lines of it. If the user needs to read any of it, put it in your reply.
```

## Tool-call batching in agent loops

Parallel calls work as expected when a request names several things to fetch. The exception is
coding and computer-use loops where the next independent calls are *implied* rather than requested:
there it may issue one per turn. Quality is unaffected, but each extra turn costs tokens, a round
trip, and wall-clock time.

```text
First privately list what you need next; then request every item that doesn't depend on another's result in this one response.
```

Append it after each user message as a turn-scoped system message (`role: "system"` in `messages`
with `clear_at: "next_user_message"`, beta header `mid-conversation-system-clear-at-2026-08-21`).
Append a fresh copy each turn and leave earlier copies **byte-for-byte** where they are: once cleared
the model does not see them and they cost no input tokens, but deleting or rewriting them is an edit
to earlier turns. Without the beta, put the sentence in a text block after the `tool_result` blocks.

## Append-only history

Append each assistant turn exactly as the API returned it, thinking blocks included. For accounts
created on or after **31 August 2026**, thinking blocks are valid only in the exact conversation that
produced them: replaying one after its prefix changed returns a **400**, or drops the block with
`thinking.block_binding.prefix_mismatch_behavior: "drop_block"` (beta header
`thinking-binding-controls-2026-08-01`). Future models are expected to enforce this for all accounts,
so adopt it now.

Use turn-scoped system messages for per-turn reminders, mid-conversation system messages to change
instructions or tools, and let server-side compaction or context editing do trimming. If compacting
client-side, replace the whole history with one summary message plus the new user turn and replay
nothing else. Because cache reads are cheaper on Fable 5.1, compacting early to save cost may no
longer be the right tradeoff: experiment with later compaction points.

To audit what your harness already rewrites, run a session with `prefix_mismatch_behavior:
"drop_block"` and log `input_transformations`.

## Writing density

Prose is a step up overall, with fewer stock phrases, but sentences can run longer with fewer
paragraph breaks than Fable 5. Defining the anti-pattern works better than asking for shorter
sentences. Put it in a user message (preferred) or the system prompt:

```text
Mannered prose substitutes metaphor and flourish for direct statement. Instead of "a parameter worth varying," the mannered writer produces "a dial worth turning." Instead of "this point still matters," they write "this point earns its keep." The phrases exist to display the writer, not to convey the idea, and readers can tell. That is why mannered prose irritates: it makes the reader work harder so the writer can perform. It is also imprecise. Metaphors drag in connotations the writer did not choose and cannot control. The fix is to say what you mean. When a literal phrase is available, use it.
```

The short form usually works too: `Please remove all mannered prose.`

## Formatting in chat

It uses bold less and reaches for headers, lists, and quotation marks less than earlier models.
Replace inherited anti-formatting rules with a positive rule:

```text
Use lists and bullet points when asked to, or when the content is multifaceted enough that they help with clarity. If the person explicitly requests minimal formatting, always format your responses without bullet points, headers, lists, or bold emphasis, as requested. In conversational, personal, or emotional exchanges, keep to plain prose.
```

## Quoting retrieved sources

More likely than Fable 5 to reproduce source passages without marking them as quotations. The fix is
one complete worked example in the system prompt: the request, the response, and a rationale saying
why it is correct. Structure it as `<example><user>…</user><response>…</response><rationale>CORRECT:
…</rationale></example>`, where the rationale notes that the response is organized around where
sources agree and differ, conveys each in the assistant's own indirect speech, marks the one short
quoted phrase, and rewords every other claim. Template the tool-call lines with your own tool's name
so it reads them as tool output rather than literal text to emit.

## Finish the whole task

On long asynchronous workloads it sometimes describes what it would do next instead of doing it, or
stops to ask permission for a step the original request already covered. Two system prompt additions
together mitigate it; **apply both**, or the first alone if prompt length is tight.

```text
You are operating autonomously. The user is not watching in real time and cannot answer questions mid-task, so asking 'Want me to…?' or 'Shall I…?' will block the work. For reversible actions that follow from the original request, proceed without asking. Stop only for destructive actions or genuine scope changes the user must decide. Offering follow-ups after the task is done is fine; asking permission before doing the work is not.

Exception: when the user is describing a problem, asking a question, or thinking out loud rather than requesting a change, the deliverable is your assessment. Report your findings and stop. Don't apply a fix until they ask for one.

Before ending your turn, check your last paragraph. If it is a plan, an analysis, a question, a list of next steps, or a promise about work you have not done ('I'll…', 'let me know when…'), do that work now with tool calls. That includes retrying after errors and gathering missing information yourself. Do not stop because the context or session is long. End your turn only when the task is complete or you are blocked on input only the user can provide.

Before running a command that changes system state (such as restarts, deletes, or config edits), check that the evidence actually supports that specific action. A signal that pattern-matches to a known failure may have a different cause.
```

Keep the opening sentence as written; it carries much of the effect. This block can make the model
less likely to ask about genuinely ambiguous requests, so check that tradeoff. The second addition
defines the request as the scope of the deliverable and is reproduced in full on the source page
under **Finish the whole task**; fetch it from there when the task is long-horizon and autonomous.

## Keep changes and tests to scope

On open-ended features it may fix nearby code, extend unmentioned behaviour, or commit more test
files than the change warrants.

```text
If, while working or testing, you find a pre-existing bug, a performance concern, or behavior the task doesn't mention, don't fix, optimize or extend it in this change unless the requested behavior cannot work without it; report it as a follow-up in your summary. Where the task is ambiguous, implement the reading its wording and the surrounding code most directly support, state that assumption in your summary, and don't build for the other readings as well. Verify your work however you like; scratch scripts and quick checks need not be kept. Commit tests only where the task asks for them or this repository already keeps tests for this kind of change, sized like the neighboring test files — roughly one focused test per stated behavior — and don't turn scratch checks into additional permanent test files. This is about extras only: implement every behavior the task asks for, completely.
```

## Search triggering at low effort

At `low` it calls search and retrieval tools less than Fable 5 and answers from memory more. Often
the simplest fix is raising effort for the affected turns only. Otherwise:

```text
When a query centers on a name you do not confidently recognize, or recognize from a fast-moving area like AI models and developer tools where the landscape shifts within months, the name itself is the thing to verify: search before answering, and include the name as the user wrote it in at least one query alongside any reformulations. This holds even when you have some background on it — partial background is exactly what makes an out-of-date answer sound authoritative, so familiarity is not a reason to skip the search.
```

## Safeguard false positives

Fewer than Fable 5 at launch, and finding vulnerabilities in source code is permitted. A blocked
request returns `stop_reason: "refusal"`. Three situations raise the odds:

- **Compile-check phrasing.** Ask "Are there any bugs in this program?" rather than "Does this
  program compile without errors?"
- **Lesser-known languages.** Give context about the language, ideally access to its documentation.
- **Base64 in tool output.** Removing it is the recommended fix.

## Targeted edits over whole-file rewrites

More likely than Fable 5 to rewrite an entire file for a small change. The result is usually the same
but costs more output tokens and time.

```text
The number of tokens used to edit files is best minimized, all else being equal. Therefore, when it will not affect the end result, try to surgically edit a file rather than rewrite the entire thing.
```

## Room for long outputs at xhigh and max

At `xhigh` and especially `max` it can draft much of a long deliverable in thinking and then write it
again as the reply: longer wait, more output tokens. Prefer running these at `high`. If you must use
`xhigh` or `max`, set `max_tokens` to cover thinking **and** reply, and append this to the user
message with `[max_tokens]` replaced by the actual value:

```text
Everything produced in one reply, including any reasoning or drafting done before the reply, counts toward a single limit of about [max_tokens] tokens. If that limit is reached before the reply is finished, the person receives a cut-off response and has to start over. Composing an entire output or deliverable in full as reasoning and then again as a reply would double the length of the turn without improving the result, so don't do that.

Instead, when the person has asked for a long or effort-intensive deliverable such as a multi-section document, a large table or dataset, or a complete code file, spend extra effort on understanding the request, checking the inputs the answer depends on, settling the structure and other difficult decisions, and otherwise using the reasoning space to reason and the output space to write an output. Usually it is not needed to draft an output multiple times.
```

## Subagents and vision

Do not force the lead agent to block on each subagent: have the spawn tool return immediately, pass
results back in a later `user` message, and give the lead a separate tool for when it wants to wait.
On coding tasks this lowers average time to completion at similar quality and cost.

For dense visual inputs, give it a container with the raw images and image-processing libraries, or
at minimum a crop tool that returns a chosen region enlarged. That alone delivers most of the uplift.
