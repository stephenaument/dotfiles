# Step 4: Write Outputs

## Goal
Write all synthesized outputs from step 3 to their target locations in the vault.

## File Safety Rules (apply to ALL writes)

- **Never modify user-written content** in any file
- **Append-only** for standup file and activity log
- **Field-population only** for inline Dataview fields - populate if empty, never overwrite
- **Insert-into** for today's daily note - add content to specific locations, never modify existing

---

## Write A: Daily Summary (Story 2.2)

### Populate `daily-summary::` on the target daily note

**Target file:** `journal/daily/{target_date}.md`

**Action:** Find the `daily-summary::` field in the file. If it exists and is empty (just `daily-summary::` with no value after it), populate it with the summary from step 3 Part A.

**If the field doesn't exist:** Add it to the frontmatter section, on a new line before the closing `---`. Format: `daily-summary:: {value}`

**If the field already has a value:** Do NOT overwrite. Skip this write.

**If step 3 produced no summary** (should not happen, but as a safeguard): Write `daily-summary:: No activity recorded` rather than leaving the field empty. An empty field means "unprocessed" to the orchestrator and will cause re-processing on the next run.

**Syntax:** Must exactly match `daily-summary:: {value}` - Dataview requires this format. No quotes, no extra spaces, value on the same line.

**Verify:** After writing, confirm the field is populated by reading it back.

---

## Write B: Standup Entry (Story 2.3)

### Prepend standup draft to `Daily Standup.md`

*For today's processing only - skip for missed day catch-up.*

**Target file:** `Daily Standup.md`

**Action:** Prepend a new entry at the top of the file (after the frontmatter `---\n\n---` block if present). The new entry goes ABOVE all existing entries.

**Exact format:**
```
# [[YYYY-MM-DD]]

## My Update

Done
- {done item 1}
- {done item 2}

Doing
- {doing item 1}
- {doing item 2}

---
```

The `---` goes at the **bottom** as a separator before the next entry. Do NOT prepend `---` at the top (it confuses Obsidian). Existing content below is never modified.

---

## Write C: Day Kickoff (Story 2.4)

### Insert open loops, Open PRs, focus items, and ONE THING into today's daily note

*For today's processing only - skip for missed day catch-up.*

**Target file:** `journal/daily/{today}.md` (today's note, not yesterday's)

**Open loops:** Insert as a bullet list in a new section `## Open Loops (from {weekday})` between `## 🌱 New Today` and the Meeting Log. Format each as a scheduled task:
- `- [ ] #task {loop description} ⏳ {today's date}`

This ensures they surface in the "Scheduled Today" query. Do not overwrite existing content.

**Open PRs table:** If step 3 produced a carried-forward Open PRs table, insert it as a `# Open PRs` section after the Open Loops section (or after `## 🌱 New Today` if no open loops). Use the exact markdown table format from the previous day, minus any merged PRs. If no table was carried forward, skip this.

**Today's Focus (conditional):** Only insert if step 3 produced actionable focus items. If generated, insert as `## Today's Focus (from standup)` after the Open Loops section (before Open PRs). Format each as:
- `- [ ] #task {Doing item} ⏳ {today's date}`

**If no actionable items exist, do NOT write a Today's Focus section.** Waiting/PR-status items belong in the Open PRs table, not here.

**ONE THING scheduling:** Populate the ONE THING placeholder in today's note with the task identified in step 3 Part C. Format with `⏳ {today's date}` scheduling. ONE THING can be an actionable task OR a critical waiting item that needs active pushing.

**Where-to-start:** Insert as a brief note near the top of the daily note, after the nav line or under the ONE THING section.

---

## Report

After all writes are complete, summarize to the user:

```
Good morning! Here's what I've done:

- Daily summary written for {target_date}: "{summary_preview}"
- Standup draft ready in Daily Standup.md - review before 10:05
- {open_loop_count} open loop(s) surfaced in today's note
- Open PRs table: {carried forward N PRs / not present}
- {If Today's Focus written: "Today's Focus: N actionable items" | "Today's Focus: skipped (no actionable items beyond PR tracking)"}
- Suggested ONE THING: {task_description}
- Where to start: {recommendation}

{If Monday: "Weekly summary and cold start briefing also generated - see step 5."}
```
