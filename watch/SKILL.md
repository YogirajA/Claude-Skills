---
name: watch
description: Watch and analyze any YouTube video by fetching its transcript, then summarizing it, extracting key takeaways, pulling quotes, building timestamped chapter notes, listing action items, or answering a specific question about it. Use this whenever the user shares a YouTube link (youtube.com or youtu.be) and wants to know what's in it, says "watch this", "summarize this video", "give me the key points / notes / takeaways from this talk", "what does this video say about X", "tldr this YouTube video", or wants to skip watching something and get the content fast. Trigger even when the user just pastes a YouTube URL with a brief instruction, and even if they never say the word "watch".
---

# Watch (YouTube-first video analysis)

Point Claude at a YouTube video and get its content back as structured notes, without
watching it yourself. The skill fetches the transcript, then analyzes it for whatever you
need: a summary, timestamped chapters, key takeaways, action items, quotes, or answers to a
specific question.

There is no magic here. The model cannot "see" a video; everything depends on getting a text
transcript first. So the skill's real job is to (1) reliably pull the transcript, (2) clean
it, (3) analyze it well, and (4) be honest when the transcript can't be obtained instead of
inventing content.

## Step 1 - Identify the video

Extract the video ID and note the URL form: `youtube.com/watch?v=ID`, `youtu.be/ID`,
`/shorts/ID`, or `/live/ID`. If the user pasted a non-YouTube link, say this skill is
YouTube-first and offer the paste-the-transcript fallback (Step 4).

## Step 2 - Fetch the transcript

Prefer the most robust method available. Check what is installed and degrade gracefully.

**Method A - yt-dlp (most robust; also gets metadata).** Handles auto-generated captions when
manual ones are absent.

```
yt-dlp --skip-download --write-auto-subs --write-subs --sub-langs "en.*" --sub-format vtt --convert-subs srt -o "%(id)s.%(ext)s" "<URL>"
yt-dlp --skip-download --print "%(title)s :: %(uploader)s :: %(duration_string)s :: %(upload_date)s" "<URL>"
```

Then read the resulting `.srt` / `.vtt`. Auto-captions repeat rolling lines, so dedupe: each
line of speech should appear once, keeping its earliest timestamp.

**Method B - youtube-transcript-api (cleanest timestamped text).**

```
python -c "import json,sys; from youtube_transcript_api import YouTubeTranscriptApi as Y; print(json.dumps(Y.get_transcript(sys.argv[1])))" <VIDEO_ID>
```

Returns `[{text, start, duration}, ...]`, already clean. Good when it works; falls over if
transcripts are disabled for the video.

If neither tool is installed, tell the user once, plainly:

> I need a transcript tool. Install either with `pip install yt-dlp` or
> `pip install youtube-transcript-api`, or paste the transcript here and I'll work from that.

Don't loop on install errors. Surface the problem and offer the paste fallback.

## Step 3 - Analyze for the user's intent

With no specific ask, default to the **Structured summary** template below. Otherwise match the
request:

- **Deep notes** - section-by-section detail, faithful to the speaker's logic.
- **Action items** - concrete, do-able steps the video recommends.
- **Quotes** - the most striking verbatim lines, with timestamps.
- **Chapters** - a timestamped table of contents.
- **Answer a question** - answer only from the transcript; if it isn't covered, say so.

Keep timestamps where useful. Deep-link form: `https://youtu.be/<id>?t=<seconds>`.

### Structured summary (default)

```
# <Title> - <Uploader> (<duration>)
**TL;DR:** <2-3 sentence gist>

## Key takeaways
- <takeaway> [mm:ss]
- ...

## Section notes
### <Section title> [mm:ss]
<what's covered>

## Worth quoting
> "<quote>" [mm:ss]
```

Offer to save the output to a markdown file if it's long or the user wants to keep it.

## Step 4 - Honesty guardrail

If you could not get a transcript, say so and stop, then ask the user to paste it. Never
summarize a video you don't have the transcript for, never guess at content from the title,
and don't present a thumbnail or description as if it were the video. A wrong summary is worse
than an honest "I couldn't fetch it."
