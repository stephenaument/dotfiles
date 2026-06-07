# Step 2: Gather Signals

## Goal
Read all available input signals for the target date and assess signal quality. hall gathered data carries forward to step 3.

## Execution


### 1. Read the target daily note

Read the full file at `journal/daily/{target_date}.md`.

Extract the following:
- **Daily Log Section** - everything under `# 🌞 Daily Log` (or `# Daily Log`) until the next `#` level header or `---`
- **Completed tasks** - all lines matching `- [x] #task` anywhere in the note
- **New Today tasks** - all lines under `## 🌱 New Today`
- **Meeting Log entries** - any user-written content under meeting sub-headers (not just the template headers)

If the daily note doesn't exist, note this and continue - other signals may still be available.

### 1b. Read the previous day's Open PRs table

Check the target date's daily note (and if not present, the most recent prior daily note) for an `# Open PRs` section containing a markdown table. If found, extract the full table - this will be carried forward to today's note in step 4, with merged PRs removed.

### 2. Read recent standup entries

Read the `# 📣 Standup Update` section from the **last 3 daily notes** (most recent workdays). From these, identify:
- The most recent entry's **Doing** items - these are potential carry-forwards
- Any **Done** items from recent days that provide context

The standup lives in each daily note under `# 📣 Standup Update`, with `Done` and `Doing` sub-sections.

### 3. Run git log

Read `config/repos.md` to get the list of repos. For each repo path, run:

```bash
git -C {repo_path} log --oneline --after="{target_date} 00:00" --before="{target_date} 23:59"
```

Collect all commit one-liners. If a repo doesn't exist or git log returns nothing, skip it silently.

### 4. Read activity log

If `_agent-activity.md` exists, read it and extract entries where the date matches `{target_date}`. Format: `- YYYY-MM-DD HH:MM | {agent} | {action-type} | {one-liner} | {path}`

If the file doesn't exist or has no matching entries, skip silently.

### 5. Read style reference

Read `config/style-reference.md`. This provides:
- Example standup entries showing preferred framing
- Work vocabulary (radars, PRs, seeding, coverage engine, etc.)
- Daily summary framing guidance (impact-oriented, not activity logs)
- Priority filtering guidance (what's standup-worthy vs noise)

Carry this guidance forward to step 3 for synthesis.

### 6. Assess signal quality

Based on the Daily Log section content from step 1:
- **Rich** - substantial daily log with multiple entries, descriptions, technical detail, timestamps, code references
- **Sparse** - a few bullet points or brief notes
- **Blank** - no user-written content in the Daily Log section (empty, or only template boilerplate after cleanup)

### 7. Report gathered signals

Present a brief summary to the user:

```
Signals gathered for {target_date}:
- Daily log: {rich|sparse|blank}
- Completed tasks: {count} items
- Git commits: {count} across {repo_count} repo(s)
- Activity log: {count} entries
- Standup carry-forward: {count} Doing items from previous entry

Proceeding to synthesis...
```

All gathered data is now available for step 3.
