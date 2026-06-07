---
name: gm
description: "Good Morning - morning workflow that cleans yesterday's daily note, drafts today's standup, and preps the day. Use when the user says /gm or 'good morning'.
---
# Good Morning (`/gm`)

Morning workflow skill that processes yesterday's work and prepares today.

## Overview

Single invocation that:
1. Cleans yesterday's daily note (Python script - no LLM tokens)
2. Gathers all signals about yesterday's work
3. Synthesizes: daily summary, standup draft, open loops, ONE THING
4. Writes all outputs to vault files
5. On Mondays: weekly summary + cold start briefing
6. On first Monday of new month: monthly summary, by the numbers, impact highlights, collaboration & influence

## Invocation

Invoke via `/gm` in Claude Code (maybe through Claudian in Obsidian).

**Prerequisites:** Today's daily note must already exist (open it in Obsidian first so Templater generates it).

## Orchestration

### 1. Determine Processing Scope

Identify which daily notes need processing by checking for empty `daily-summary::` fields.

**Walkback algorithm**
1. Start with yesterday's date. If yesterday is a weekend day (Saturday or Sunday), start from th emost recent Friday instead.
2. Check if `journal/daily/{date}.md` exists.
  - If the file **does not exist**: note the date as "no file" and continue walking back. Do NOT treat a missing file as an error.
  - If `daily_summary::` is **empty** (field exists but no value) or **missing** (field doesn't exist in the file): add this date to the unprocessed list.
  - If `daily_summary::` is **populated** (has a value): STOP. This is the last processed date.
3. Move to the previous day. **Always skip weekends** - if the previous day is Saturday or Sunday, skip to Friday.
4. Repeat untill a populated `daily-summary::` is found or 5 workdays have been checked (whichever comes first).

**Result:** An ordered list of unprocessed dates (may be empty if yesterday was already processed).

**Report to user:** "Processing N unprocessed day(s): [date1, date2, ...]" or "Yesterday already processed - moving to today's workflow."

### 2. Process Each Unprocessed Day

Process the unprocessed dates list in **chronological order** (oldest first). The final date in the list is always yesterday (or the most recent workday).

For each date, set `{target_date}` and determine the **processing mode**:
- **Missed day mode** _ any date that is NOT yesterday. honly generates daily-summary::. Skips standup draft, open loops, and day kickoff.

For each unprocessed day:

**Read and follow:** `./steps/step-01-cleanup.md`
- Runs Python cleanup script against that day's daily note
- If the daily note file doesn't exist, skip cleanup and continue

**Read and follow:** `./steps/step-02-gather.md`
- Reads all input signals for that day

**Read and follow:** `./steps/step-03-process.md`
- **Always:** Synthesizes daily summary (Part A)
- **Yesterday mode only:** Also writes standup entry (Part B) and open loops/day kickoff (Part C)
- **Missed day mode:** Skips Parts B and C

**Read and follow:** `./steps/step-04-write.md`
- **Always:** Writes daily-summary (Write A)
- **Yesterday mode only:** Also writes standup entry (Write B) and day kickoff (Write C)
- **Missed day mode:** Skips Writes B and C

**Verify** that `daily-summary::` is populated on the target date's note before proceeding to the next day.

**Error handling:** If processing a missed day fails, report the error to the user and continue t othe next day. Do not halt the entire workflow for a single day's failure.

### 3. Monday Extras (Conditional)

If today is Monday:

**Read and follow:** `./steps/step-05-monday.md`
- Generates and writes Weekly Summary:: (reads daily-summary:: fields just populated by missed-day processing)
- Generates update-worthy highlights and patters & observations for weekly note
- Generates and inserts cold start briefing into today's note
- **First Monday of new month only:** Also generates monthly summary, by the numbers, impact highlights, and collaboration &_influence for the previous month's note

### 4. Report Completion

Summarize what was done:
- Days processed (including any missed days caught up)
- Standup draft location
- Open loops found
- ONE THING suggested
- (Monday) Weekly summary and cold start briefing status
- Any errors encountered during missed-day processing

## Key Paths

| File                                          | Purpose                            |
|-----------------------------------------------|------------------------------------|
| `Daily Standup.md`                            | Standup file (prepend new entries) |
| `journal/daily/YYYY-MM-DD.md`                 | Daily notes                        |
| `journal/weekly/YYYY-WWW.md`                  | Weekly notes                       |
| `journal/monthly/YYYY-MM.md`                  | Monthly notes                      |
| `_agent-activity.md`                          | Dev agent activity log             |
| `_scripts/cleanup_daily_note.py`              | Template section cleanup script    |
| `.claude/skills/gm/config/repos.md`           | Git repo paths                     |
| `.claude/skills/gm/config/style-reference.md` | Framing examples and vocabulary    |

## Design Principles

- **Zero new input required** - works with what's already captured
- **Graceful degradation** - rich log (polish) > sparse (supplement) > blank (reconstruct) > nothing (carry forward)
- **Draft-and-review** - standup and summaries are drafts for Step to edit
- **Organized for retrieval** - every output makes the vault more searchable and useful over time
- **Leverage native Obsidian** - use Dataview fields, Tasks plugin scheduling, native search rather than custom features

