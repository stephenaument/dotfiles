#!/usr/bin/env python3
"""
cleanup_daily_note.py - Remove empty template sections from an Obsidian daily note.

Usage: python3 _scripts/cleanup_daily_note.py <path-to-daily-note>

Exit codes:
  0 - success (file cleaned or no changes needed)
  1 - error (file not found, parse error, etc.)
"""

import re
import sys
from pathlib import Path

# --- Configuration ---

# Always keep these sections (normalized header text).
PROTECTED_HEADERS = {"daily log"}

# Always remove these sections regardless of content (normalized header text).
ALWAYS_REMOVE_HEADERS = {
    "daily check list", "start of day", "end of day",  # Checklists
    "update worthy",                                    # Rarely used tag query
}

# Keep "# Tasks" parent only if this child section is kept.
TASKS_CHILD_THAT_PRESERVES_PARENT = "new today"


# --- Template vs User Content Detection ---

TEMPLATE_LINE_PATTERNS = [
    re.compile(r"^\s*>?\s*```"),              # Code block fences (including in callouts)
    re.compile(r"^\s*>\s*"),                   # Callout block lines
    re.compile(r"^\s*- \[ \] "),               # Unchecked checklist items
    re.compile(r"^\s*_.*_\s*$"),               # Italic placeholder text
    re.compile(r"^\s*-\s*$"),                  # Empty bullet
    re.compile(r"^\s*---\s*$"),                # Horizontal rules
    re.compile(r"^\s*$"),                      # Blank lines
    re.compile(r"^\s*\|[\s\-:|]+\|\s*$"),      # Table separator rows (| -- | --- |)
]


def is_header(line: str) -> bool:
    return bool(re.match(r"^#{1,6}\s+", line))


def normalize_header(line: str) -> str:
    text = re.sub(r"^#{1,6}\s+", "", line)
    # Remove emoji (broad Unicode ranges)
    text = re.sub(
        r"[\U0001f300-\U0001f9ff\u2600-\u26ff\u2700-\u27bf"
        r"\U0001fa00-\U0001fa6f\U0001fa70-\U0001faff\u2705\u2b50"
        r"\ufe0f]",
        "", text,
    )
    return text.strip().lower()


def line_is_user_content(line: str) -> bool:
    stripped = line.strip()
    if not stripped:
        return False
    if re.match(r"^\s*- \[x\] ", line, re.IGNORECASE):
        return True
    if re.match(r"^\s*- \[ \] ", line):
        return False
    for pattern in TEMPLATE_LINE_PATTERNS:
        if pattern.match(line):
            return False
    return True


TABLE_HEADER_RE = re.compile(r"^\s*\|.*\|\s*$")
TABLE_SEPARATOR_RE = re.compile(r"^\s*\|[\s\-:|]+\|\s*$")


def is_empty_table(lines: list[str]) -> bool:
    """Check if lines form a markdown table with only header + separator (no data rows)."""
    table_lines = [l for l in lines if TABLE_HEADER_RE.match(l)]
    if len(table_lines) < 2:
        return False
    # Must have exactly one separator row and one header row, no data rows
    non_blank = [l for l in lines if l.strip()]
    return all(TABLE_HEADER_RE.match(l) for l in non_blank) and len(non_blank) == 2


def body_has_user_content(body_lines: list[str]) -> bool:
    # An empty markdown table (header + separator only) is template content
    if is_empty_table(body_lines):
        return False
    in_code_block = False
    for line in body_lines:
        clean = re.sub(r"^\s*>\s*", "", line.strip())
        if clean.startswith("```"):
            in_code_block = not in_code_block
            continue
        if in_code_block:
            continue
        if line_is_user_content(line):
            return True
    return False


# --- "Other Tasks" Special Handling ---

def filter_other_tasks_body(body_lines: list[str]) -> list[str]:
    """
    From the '# Other Tasks' section body, remove the 'No Due Date' callout
    but keep 'Done Today', 'Files Created Today', 'Files Modified Today' callouts.
    """
    # Split body into callout blocks separated by ---
    blocks = []
    current_block = []

    for line in body_lines:
        if line.strip() == "---":
            if current_block:
                blocks.append(current_block)
                current_block = []
            # The --- itself is a separator, add as its own block
            blocks.append([line])
        else:
            current_block.append(line)
    if current_block:
        blocks.append(current_block)

    # Filter: remove blocks containing "No Due Date", keep others
    kept = []
    for block in blocks:
        block_text = " ".join(line.strip() for line in block)
        if "No Due Date" in block_text:
            continue
        # Skip standalone --- separators if the block before was removed
        if len(block) == 1 and block[0].strip() == "---":
            # Only keep separator if we have content before it
            if kept and any(line.strip() and line.strip() != "---" for line in kept):
                kept.extend(block)
            continue
        kept.extend(block)

    return kept


# --- Preamble Handling ---

def filter_preamble(lines: list[str]) -> list[str]:
    """Remove the Projects callout block from preamble, keep nav line."""
    result = []
    in_callout = False

    for line in lines:
        # Detect Projects callout start
        if not in_callout and ("[[Projects]]" in line or
                               (line.strip().startswith(">[!info]") and "Projects" in line)):
            in_callout = True
            continue

        if in_callout:
            # Callout lines start with > or are code blocks within callouts
            if line.strip().startswith(">") or line.strip().startswith("```"):
                continue
            if line.strip() == "---":
                in_callout = False
                continue
            if line.strip().startswith("LIST") or line.strip().startswith("FROM") or \
               line.strip().startswith("WHERE") or line.strip().startswith("AND"):
                continue
            # Non-callout line means callout ended
            in_callout = False

        result.append(line)

    # Strip trailing blank lines left after callout removal
    while result and result[-1].strip() == "":
        result.pop()

    return result


# --- Main Parsing ---

def parse_document(content: str) -> list[dict]:
    lines = content.split("\n")
    chunks = []
    i = 0

    # Frontmatter
    if lines and lines[0].strip() == "---":
        fm_lines = [lines[0]]
        i = 1
        while i < len(lines):
            fm_lines.append(lines[i])
            if lines[i].strip() == "---":
                i += 1
                break
            i += 1
        chunks.append({"type": "frontmatter", "lines": fm_lines, "keep": True})

    # Preamble
    preamble = []
    while i < len(lines) and not is_header(lines[i]):
        preamble.append(lines[i])
        i += 1
    if preamble:
        filtered = filter_preamble(preamble)
        if filtered:
            chunks.append({"type": "preamble", "lines": filtered, "keep": True})

    # Sections
    while i < len(lines):
        if is_header(lines[i]):
            header = lines[i]
            body = []
            i += 1
            while i < len(lines) and not is_header(lines[i]):
                body.append(lines[i])
                i += 1

            normalized = normalize_header(header)

            # Determine keep/remove
            if any(r in normalized for r in ALWAYS_REMOVE_HEADERS):
                keep = False
            elif any(p in normalized for p in PROTECTED_HEADERS):
                keep = True
            elif "other tasks" in normalized:
                # Special: filter body to remove No Due Date, keep the rest
                filtered_body = filter_other_tasks_body(body)
                if filtered_body and any(l.strip() for l in filtered_body):
                    chunks.append({
                        "type": "section",
                        "header": header,
                        "body": filtered_body,
                        "lines": [header] + filtered_body,
                        "keep": True,
                        "normalized": normalized,
                    })
                    continue
                else:
                    keep = False
            else:
                keep = body_has_user_content(body)

            chunks.append({
                "type": "section",
                "header": header,
                "body": body,
                "lines": [header] + body,
                "keep": keep,
                "normalized": normalized,
            })
        else:
            chunks.append({"type": "stray", "lines": [lines[i]], "keep": True})
            i += 1

    # Second pass: keep "# Tasks" parent if "New Today" child is kept
    new_today_kept = any(
        c.get("normalized", "") and TASKS_CHILD_THAT_PRESERVES_PARENT in c["normalized"]
        and c["keep"]
        for c in chunks
    )

    if new_today_kept:
        for c in chunks:
            if c.get("normalized", "") == "tasks" and not c["keep"]:
                c["keep"] = True
                break

    return chunks


def cleanup(content: str) -> str:
    chunks = parse_document(content)

    kept_lines = []
    for chunk in chunks:
        if chunk["keep"]:
            kept_lines.extend(chunk["lines"])

    result = "\n".join(kept_lines)
    result = re.sub(r"\n{4,}", "\n\n\n", result)
    result = result.rstrip("\n") + "\n"
    return result


def main():
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <path-to-daily-note>", file=sys.stderr)
        sys.exit(1)

    filepath = Path(sys.argv[1])
    if not filepath.exists():
        print(f"Error: File not found: {filepath}", file=sys.stderr)
        sys.exit(1)

    content = filepath.read_text(encoding="utf-8")
    cleaned = cleanup(content)

    if cleaned != content:
        filepath.write_text(cleaned, encoding="utf-8")
        original_count = sum(1 for c in parse_document(content) if c["type"] == "section" and not c["keep"])
        print(f"Cleaned {filepath.name}: removed {original_count} empty section(s)")
    else:
        print(f"No changes needed for {filepath.name}")

    sys.exit(0)


if __name__ == "__main__":
    main()
