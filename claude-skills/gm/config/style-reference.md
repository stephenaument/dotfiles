# Style Reference

Framing examples and vocabulary for the morning workflow agent. This file guides how standup drafs, daily summaries, and other outputs are written.

## Standup Framing examples

These are real standup entries showing the preferred style - concise, action-oriented, communication-focused:

```
Done
- investigated radars, sent a couple back
- worked through seeding issues and updates for watch-specific operations to match the new test approach
- PR reviews

Doing
- Point open PRs to release branch
- Problem station enhancements
```

```
Done
- Fix cap assembly and unpair operations. merge the UI PR and deploy to dev
- Added new coverage engine operations to watch workflow
- Added restore test filtering to watch workflow
- Fixed some failing specs in multiple branches
- Merged restore test filtering

Doing
- Testing non-happy path for watch
- Problem station enhancements
```

```
Done
- Addressed a couple of radars, PRs approved and have been merged this morning
- What about the 2nd attempt? Will SDE send it or do we need to handle 1st/2nd attempt ourselves before sending it?

Doing
- Filter cap operations by model for watch workflow
- Problem station enhancements
```

## Draft Philosophy

**Over-include, let Step cut.** The standup draft should capture everything standup-worthy from yesterday's signals. Step will condense to 3-4 items. If he doesn't get a chance to edit, the verbose draft is usable as-is - better than nothing.

**Doing is a guess.** The agent can only carry forward from previous standup's Doing and infer from open loops/tasks. Step will update Doing with what he actualyl plans to focus on today.

## Key Patterns

- **Lead with the action, not the process:** "Fixed failing specs" not "Spent time debugging spec failures"
- **Mention the artifact when relevant:** "Merged restore test filtering" names the PR/branch/radar ticket
- **Questions and blockers are standup-worthy:** "Will SDE send it or do we need to handle..." is valuable communication-focused
- **Group related work:** Multiple items on the same feature can be separate bullets
- **Keep "Doing" items high-level:** Feature or workstream names, not task-level details

## Work vocabulary

Use these terms naturally - they're the team's language:

- **radars** - bug/issue tracking
- **PRs** - pull requests
- **seeding** - test data setup in dev environments
- **branches** - git branches, often feature-specific
- **specs** - test specifications (RSpec)

## Daily Summary Framing

The `daily-summary::` one-liner should be framed toward impact or potential impact:
- "Shipped watch workflow run_conditions fix affecting VMI, fraud, and manual transitions"
- "Resolved 3 radars and unblacked watch workflow seeding in dev"
- "Investigated SDE test code issue - root cause identified in run_conditions entity lookup"

Not activity logs:
- "Worked on various things including radars and PRs"
- "Debugging and testing"

## Priority filtering

**Standup-worthy (include):**
- Shipped/merged code
- Root cause analysis or investigation findings
- Blockers or questions for the team
- Radar resolutions
- PR reviews completed
- New workstream started

**Noise (exclude unless only signal):**
- Routine branch management (rebase, merge conflicts)
- Environment issues (seeding retries, dev env restarts)
- Reading documentation
- Minor formatting fixes

