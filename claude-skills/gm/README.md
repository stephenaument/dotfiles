# /gm - Good Morning Workflow

A Claude Code skill that processes yesterday's work and prepares today. Designed as a cognitive prosthetic for AuDHD - replacing the executive function that organizational discipline requires, rather than optimizing intact function.

## What It Does

One invocation (`/gm`) each morning:

1. **Cleans yesterday's daily note** - Removes empty template sections (Python script, no LLM tokens)
2. **Gathers signals** - Daily log, completed tasks, git commits, dev agent activity
3. **Synthesizes outputs**:
   - Daily summary (populates `Daily Summary::` field)
   - Standup draft (Done/Doing in today's note)
   - Open loops surfaced as scheduled tasks
   - ONE THING suggestion for focus
4. **Monday extras** - Weekly summary, cold start briefing, patterns & observations
5. **First Monday of month** - Monthly summary, impact highlights, collaboration moments

## Design Principles

- **Zero new input required** - Works with what's already captured
- **Graceful degradation** - Rich log → polish it. Sparse → supplement. Blank → reconstruct. Nothing → carry forward
- **Draft-and-review** - Every output touching professional communication is a draft you review
- **Organized for retrieval** - Dataview fields cascade summaries upward automatically

## Installation

```bash
./install.sh /path/to/your/vault
```

This copies:
- Skill files → `.claude/skills/gm/`
- Python cleanup script → `_scripts/`

## Configuration

After installing, customize:

### `config/repos.md`
Git repos to scan for commit history:
```markdown
- ~/src/project-one/
- ~/src/project-two/
```

### `config/style-reference.md`
- Example standup entries showing your preferred framing
- Work vocabulary (your team's terms)
- What's standup-worthy vs noise

## Vault Structure Required

```
journal/
├── daily/YYYY-MM-DD.md
├── weekly/YYYY-WWW.md
└── monthly/YYYY-MM.md
```

Daily notes need these sections (Templater generates them):
- `# 📣 Standup Update` with Done/Doing
- `# 🌞 Daily Log`
- `Daily Summary::` field in tracking section

## Triggering

Invoke via `/gm` in Claude Code, or through Claudian plugin in Obsidian.

**Prerequisite:** Open today's daily note in Obsidian first so Templater creates it.

## The Pattern

The core architecture is role-agnostic:
1. Morning ritual trigger
2. Gather signals from whatever's already captured
3. Synthesize for communication
4. Draft, never autopublish
5. Cascade upward (daily → weekly → monthly → annual)
6. Graceful degradation when input is sparse

Swap the signal sources and output formats for any role where work evidence doesn't organize itself.
