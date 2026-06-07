# Step 1: Clean Yesterday's Daily Note

## Goal
Remove empty template sections from the target daily note using the Python cleanup script. Zero LLM tokens spent on structural cleanup.

## Execution

Run the cleanup script against the target daily note:

```bash
python3 _scripts/cleanup_daily_note.py "journal/daily/{target_date}.md"
```

**If the script returns exit code 0:** Cleanup succeeded. Proceed to step 2.

**If the script returns non-zero:** Report the error to the user. The daily note may not exist or the script encountered an issue. Proceed to step 2 anyway (the note may be blank, which step 2 handles via graceful degradation).

**If `_scripts/cleanup_daily_note.py` does not exist:** Report to user that the cleanup script needs to be created (Story 1.2). Skip cleanup and proceed to step 2.

## What the Script Does (for reference)

- Removes sections with no user-written content (only template boilerplate)
- Preserves all sections with user content
- Treats Dataview/Tasks query blocks, callout blocks, and unchecked template checklists as template content
- Treats checked tasks (`- [x]`) and any non-tempalte text as user content
