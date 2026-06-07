# Step 3: Process & Synthesize

## Goal
Synthesize gathered signals into actionable outputs. This step produces drafts; step 4 writes them to files.

Use the framing guidance from `config/style-reference.md` for all synthesis.

---

## Part A: Daily Log Reconstruction & Summary (Story 2.2)

### Reconstruct or Polish the Daily Log

Based on signal quality from step 2:

**If Rich** (substantial daily log exists):
- Read the existing daily log content
- Do NOT modify the original log - it stays as-is in the daily note
- Use it as the primary source for the daily summary

**If Sparse** (few bullets in daily log):
- Read the existing sparse bullets
- Supplement with additional signals: git commits, activity log entries, completed tasks
- Mentally combine into a fuller picture of the day - but do NOT rewrite the daily note's log section
- Use the combined picture for the daily summary

**If Blank** (no user content in daily log):
- Reconstruct the day's narrative from all available signals:
  - Git commits → what code was written/fixed
  - Activity log entries → what dev agent actions happened
  - Completed tasks (`- [x] #task`) → what got done
  - Previous standup "Doing" items → what was planned
- If truly no signals exist at all, use the last standup's "Doing" items as carry-forward context
- Use the reconstruction for the daily summary

**If no signals at all** (no daily log, no git commits, no activity log, no completed tasks, no standup context):
- Generate a minimal summary: "No activity recorded"
- This ensures the `daily-summary::` field is always populated, marking the day as processed
- Do not leave the field empty - an empty field means "unprocessed" to the orchestrator

### Generate Daily Summary

Draft a `daily-summary::` one-liner for the target date.

**Framing rules** (from style reference):
- Frame toward **impact or potential impact**, not activity
- Good: "Shipped watch workflow run_conditions fix affecting VMI, fraud, and manual transitions"
- Good: "Resolved 3 radars and unblocked watch workflow seeding in dev"
- Bad: "Worked on various things including radars and PRs"
- Bad: "Debugging and testing"
- Keep to one line - this populates an inline Dataview field
- Use the team's work vocabulary naturally (radars, PRs, seeding, coverage engine, etc.)

**Output:** A single `daily-summary::` value string, ready for step 4 to write.

---

## Part B: Standup Draft (Story 2.3)

### Generate Standup Entry

*For today's processing only - skip for missed day catch-up.*

Draft a standup entry using all signals gathered in step 2.

**Done section:**
- Synthesize from yesterday's work: daily log, git commits, completed tasks, activity log
- **Priority-filter for communication value** - this is strategic communication, not a log dump
- Frame using team vocabulary per `config/style-reference.md`
- Include: shipped/merged code, root cause analysis findings, blockers/questions, radar resolutions, PR reviews completed, new workstreams started
- Exclude (unless only signal): routine branch management, environment issues, reading docs, minor formatting fixes

**Doing section:**
- Carry forward unresolved items from previous standup's "Doing" that did NOT appear in today's "Done"
- Add any new priorities visible from open loops, scheduled tasks, or active project state
- Keep items high-level: feature or workstream names, not task-level detail

**Output:** A complete standup draft (Done bullets + Doing bullets), ready for step 4 to format and write.

---

## Part C: Open Loops, Open PRs & Day Kickoff (Story 2.4)

### Detect Open Loops

*For today's processing only - skip for missed day catch-up.*

Scan recent daily notes (last 3-5 days) and recent standup entries for:
- Commitment language: "I'll", "need to follow up", "TODO", "action item"
- Unresolved "Doing" items that persist across 3+ consecutive standups without appearing in "Done"
- Questions asked in standup that haven't been answered

Check if any previously identified loop has been resolved:
- Appeared in a "Done" section
- Completed as a task (`- [x]`)
- Explicitly noted as resolved or no longer needed

**Output:** List of unresolved open loops, each formatted as a scheduled task:
- `- [ ] #task {loop description} ⏳ {today's date}`

This format surfaces them in the "Scheduled Today" query at the top of the daily note.

### Carry Forward Open PRs Table

*For today's processing only - skip for missed day catch-up.*

If step 2 gathered an Open PRs table from the previous day's note:
1. For each PR in the table, check if it has been merged by running `git -C {repo_path} log --oneline --all --grep="Merge pull request #{pr_number}"` or checking the PR number against recent git log merge commits.
2. Remove merged PRs from the table.
3. Carry forward the remaining table as-is - preserve the existing Status, Source, and Name columns.

If no previous Open PRs table was found, skip this - do not create one from scratch. The user maintains this table manually.

**Output:** Updated Open PRs markdown table (or nothing if no table existed), ready for step 4.

### Generate Today's Focus (Conditional)

*For today's processing only - skip for missed day catch-up.*

Review the standup Doing items from Part B. Classify each as:
- **Actionable** - Step can write code, investigate, test, or otherwise make direct progress (e.g., "fix spec failures", "investigate radar", "start new feature")
- **Waiting** - Step is waiting on others; the only action is to nudge (e.g., "follow up on PR review", "get PR into QA")

**Only generate a Today's Focus section if there are actionable Doing items.** If all Doing items are waiting/PR-status items, skip Today's Focus entirely - the Open PRs table covers visibility for those.

For each actionable item, format as a scheduled task:
- `- [ ] #task {Doing item} ⏳ {today's date}`

**Output:** List of actionable focus tasks (may be empty), ready for step 4.

### Suggest ONE THING & Where-to-Start

*For today's processing only.*

Based on:
- Open loops (highest urgency first - things that could drop)
- Carry-forward "Doing" items (including waiting items - ONE THING can be "get critical PR approved")
- Active project state from recent daily notes

Produce:
1. **ONE THING suggestion** - the highest-leverage thing for today. Can be an actionable task OR a critical waiting item that needs active pushing. Format with `⏳ {today's date}` scheduling.
2. **Where-to-start recommendation** - a brief sentence suggesting what to turn to first this morning.

**Output:** ONE THING task reference + where-to-start text, ready for step 4 to insert into today's note.
