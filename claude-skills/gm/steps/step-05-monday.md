# Step 5: Monday Extras

## Goal
On Mondays, generate a weekly summary, update-worthy highlights, patterns & observations, and cold start briefing.

## Condition
Only execute this step if today is Monday. Skip entirely on other days.

---

## A. Determine Previous Week & Weekly Note Path

Calculate the previous work week:
- Previous Monday = today minus 7 days
- Previous Friday = today minus 3 days
- Generate dates for Mon, Tue, Wed, Thu, Fri of the previous week

Determine the weekly note path:
- The weekly note uses ISO week format: `journal/weekly/YYYY-WWW.md`
- Use the ISO week number for the **previous week** - the weekly summary describes last week's work and belongs in last week's note
- Example: if today is Monday 2026-05-18 (start of W21), the target weekly note is `journal/weekly/2026-W20.md` (the week being summarized)

Check if the weekly note file exists. If it does NOT exist:
- Report to the user: "Weekly note {path} doesn't exist yet. Open it in Obsidian so Templater creates it, then re-run /gm."
- Skip all weekly note writes (Weekly Summary, Update Worthy, Patterns) but still generate the cold start briefing for today's daily note.

---

## B. Read Previous Week's Daily Summaries

For each weekday (Mon-Fri) of the previous week:
1. Check if `journal/daily/{date}.md` exists
2. If it exists, extract the `daily-summary::` field value
3. If the file doesn't exist or the field is empty, note the gap and continue

Collect all available daily summaries into a list. Also re-read any signals already gathered in step 2 that cover the previous week (standup entries, git history, activity log) for supplementary context.

---

## C. Weekly Summary

Synthesize the collected daily summaries into a paragraph-length weekly summary:
- Frame toward **accomplishments and open items**
- Use the team's work vocabulary from `config/style-reference.md`
- If some days are missing data, synthesize from what exists and note gaps naturally (e.g., "Early in the week focused on X; later days had lighter signal")
- If NO daily summaries exist at all (first week), build from standup entries and git history instead

### Write Weekly Summary to Weekly Note

1. Read the weekly note file
2. Find the line that starts with `Weekly Summary::` (located after the `# Weekly Summary` header, which appears in the template as `# 📝 Weekly Summary`)
3. Check if the field already has a value (anything after `Weekly Summary:: `)
4. If empty (`Weekly Summary::` with nothing after it): replace that line with `Weekly Summary:: {your synthesized summary}`
5. If already populated: do NOT overwrite - skip this write
6. Exact syntax: `Weekly Summary:: {value}` - single space after `::`, value on same line, no quotes, no line breaks

---

## D. Update Worthy

Review the previous week's daily logs, daily summaries, completed tasks, and git activity. Identify 1-3 highlights that have communication value beyond the immediate team - things Step's manager or engagement manager would want to hear about.

**What qualifies as update-worthy:**
- Shipped a feature or merged significant PRs
- Root-caused a tricky bug (especially one affecting multiple areas)
- Unblocked a teammate or resolved a cross-team dependency
- Proposed a new initiative or architectural improvement
- Resolved radars or customer-facing issues
- Hit a milestone on a workstream

**What doesn't qualify:**
- Routine daily work (PR reviews, branch management)
- Work-in-progress with no clear outcome yet
- Internal tooling/process unless it has team-wide impact

### Write Update Worthy to Weekly Note

1. Find the `# 📣 Update Worthy` section in the weekly note
2. Locate the template placeholder line: `_Highlights worth mentioning up the chain - shipped features, root cause finds, unblocking moments._`
3. Insert 1-3 bullet points on new lines AFTER the placeholder text, BEFORE the next `---` separator
4. Do NOT remove the placeholder text - it serves as context for Step when reviewing
5. These are drafts - Step reviews and decides what to actually share

---

## E. Patterns & Observations

Look across the full week's data - daily logs, standup entries, git history, completed tasks, carry-forward patterns - and surface things Step might not notice from inside the work.

**What to look for:**
- **Time allocation patterns:** "You spent 3 of 5 days on debugging other people's code, not your own features" - invisible work that should be visible
- **Recurring carry-forwards:** "Problem station enhancements has been in Doing for 3+ weeks" - might be blocked, bigger than expected, or needs to be escalated
- **Unblocking patterns:** "You reviewed 4 teammate PRs this week" - that's support work worth highlighting
- **Cross-cutting impact:** "Your run_conditions fix affected VMI, fraud, and manual transitions - that's not a bug fix, that's a systemic quality improvement"
- **Shipping vs. supporting ratio:** are you mostly shipping your own work, or mostly enabling others? Neither is wrong, but awareness matters
- **Energy patterns:** if signal-quality data shows consistent blank Fridays or sparse Thursdays, note it
- **Stale items:** open tasks or loops that have been sitting for a week+ without progress

**Tone:** Gentle observations, not judgments. "I noticed..." not "You should..." These are insights for Step to consider, not directives.

### Write Patterns & Observations to Weekly Note

1. Find the `# 🔮 Patterns & Observations` section in the weekly note
2. Locate the template placeholder line: `_What the agent noticed that you might miss from inside the work._`
3. Insert 1-3 observations on new lines AFTER the placeholder text, BEFORE the next `---` separator
4. Do NOT remove the placeholder text
5. Keep observations brief and specific

---

## F. Cold Start Briefing

Generate a cold start briefing to reload Step's working memory after the weekend. The goal is full context recovery in 90 seconds of reading.

### Gather Briefing Components

1. **Last week's summary** - use the Weekly Summary you just generated in section C. If no weekly summary was generated (e.g., weekly note didn't exist), synthesize a brief recap from whatever daily summaries or standup entries are available.

2. **Open items and carry-forwards** - collect from:
   - Open loops identified by step 3 Part C (commitment language, unresolved Doing items)
   - The most recent standup's "Doing" items that haven't appeared in any "Done" section
   - Any tasks scheduled but not completed from last Friday's daily note
   - If step 3 wasn't run for today yet (e.g., first-run edge case), scan the last 3 standup entries directly

3. **Active project states** - determine what workstreams are in motion:
   - Recent standup "Doing" items grouped by project/workstream
   - Projects referenced in last week's daily notes
   - Use `config/style-reference.md` vocabulary to name workstreams naturally (radars, coverage engine, etc.)

4. **Suggested first move** - reference the ONE THING already selected by step 3 Part C and scheduled by step 4. Don't create a separate recommendation - just point to what's already been prioritized: "Your ONE THING for today is already scheduled: {task description}"

### Format the Briefing

Structure for scannability - Step reads this with zero context after a weekend:

```markdown
## Cold Start Briefing

**Last week:** {1-2 sentence weekly summary}

**Open items:**
- {item 1 - what it is and why it matters}
- {item 2}
- {item 3 if applicable}

**Active workstreams:** {comma-separated list with brief status, e.g., "coverage engine (seeding in dev), problem station enhancements (PR pending review), watch workflow (shipped last week)"}

**Start here:** {reference the ONE THING already scheduled, or highest-priority open item if no ONE THING was set}
```

Keep the entire briefing under 15 lines. This is a RAM reload, not a report.

### Write Briefing to Today's Daily Note

**Target file:** `journal/daily/{today}.md`

**Insertion point:** Insert the `## Cold Start Briefing` section BEFORE the `# Tasks` header. This places it after the nav line and projects callout, making it the first substantive content Step reads.

**Write mechanics:**
1. Read today's daily note
2. Find the line `# Tasks` (which appears in the template as `# ✅ Tasks`)
3. Check if a `## Cold Start Briefing` section already exists (re-run protection) - if it does, skip the insert
4. Insert the formatted briefing block on new lines immediately BEFORE the `# ✅ Tasks` line, followed by a `---` separator
5. Do NOT modify any existing content in the daily note

### Graceful Degradation (First Monday)

If this is Step's first Monday using the system:
- No prior weekly summary exists - build the "Last week" component from recent standup entries and any daily notes that happen to exist
- No open loops were tracked - scan the last 3 standup "Doing" sections for carry-forwards
- Still produce a briefing - even a partial one is better than nothing for a Monday cold start
- Tone: helpful, not apologetic. Don't say "I don't have enough data" - just work with what's available

---

## G. Monthly Summary (First Monday of New Month)

### Condition

Only execute if today's month differs from the previous Friday's month (i.e., we've crossed a month boundary over the weekend). This means the previous month just ended and needs its summary.

### Determine Target Monthly Note

The target is the PREVIOUS month's note: `journal/monthly/{YYYY-MM}.md` where YYYY-MM is last Friday's month.

Check if the file exists. If not:
- Report to the user: "Monthly note {path} doesn't exist yet. Open it in Obsidian so Templater creates it, then re-run /gm."
- Skip all monthly writes.

### Read Previous Month's Weekly Summaries

1. Identify all weekly notes tagged with the previous month (e.g., `#2026-05`)
2. For each weekly note, extract:
   - `Weekly Summary::` field value
   - Update Worthy bullets
   - Patterns & Observations bullets
3. Also scan the month's daily notes for completed tasks, collaboration moments, and any standup entries referencing teammate interactions

### Populate By the Numbers

Count from the month's daily logs, git history, standup entries, and weekly summaries:
- **PRs merged:** count distinct PR numbers mentioned in "merged" or "shipped" context
- **PRs opened:** count distinct PR numbers mentioned in "opened" or "created" context
- **Radars resolved:** count radar references in Done sections
- **Releases shipped:** count release branch references in deployment context

Find the `# 📊 By the Numbers` section. Fill in each `- **{label}:**` line with the count and brief details (PR numbers, release names). If a line already has content after the colon, do NOT overwrite.

### Populate Impact Highlights

Synthesize from the month's Update Worthy sections and weekly summaries. Frame each bullet as **outcome → why it matters**:
- Good: "Watch workflow reached QA validation - unblocking the watch launch timeline"
- Bad: "Merged watch workflow PRs" (that's what, not impact)

Find the `# ⭐ Impact Highlights` section. Insert 3-5 bullets after the placeholder text, before the next `---`. Do NOT remove the placeholder. If bullets already exist, do NOT overwrite.

### Populate Collaboration & Influence

Scan for:
- Teammate names mentioned alongside "helped", "walked through", "paired", "debugged with"
- PR recovery or unblocking actions that benefited others
- Knowledge transfer moments (demos, documentation support)
- Work handed off to others for ownership

Find the `# 🤝 Collaboration & Influence` section. Insert bullets after the placeholder text, before the next `---`. Include the week reference (e.g., "(W22)") for context. If bullets already exist, do NOT overwrite.

### Populate Monthly Summary

If `Monthly Summary::` is empty, synthesize from the weekly summaries into a paragraph-length summary:
- Frame toward the month's arc: what started, what shipped, what's still in motion
- Use the team's work vocabulary
- End with the state of things entering next month

If already populated, do NOT overwrite.

### Report

Include in the completion report:
- "Monthly summary written for {YYYY-MM}"
- Counts populated in By the Numbers
- Number of impact highlights and collaboration moments drafted

---

## Graceful Degradation

- If some daily notes lack `daily-summary::` values: synthesize from what exists, note gaps
- If this is the first Monday using the system: work from whatever signals are available
- If the weekly note doesn't exist: skip weekly note writes, still generate cold start briefing for today's daily note
- If the monthly note doesn't exist: skip monthly writes, report to user
