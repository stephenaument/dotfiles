#!/bin/bash
# Install /gm skill into an Obsidian vault
#
# Usage: ./install.sh /path/to/vault

set -e

if [ -z "$1" ]; then
    echo "Usage: $0 /path/to/vault"
    exit 1
fi

VAULT="$1"
SOURCE="$(dirname "$0")"

if [ ! -d "$VAULT" ]; then
    echo "Error: Vault directory not found: $VAULT"
    exit 1
fi

echo "Installing /gm skill to: $VAULT"

# Create directories
mkdir -p "$VAULT/.claude/skills/gm/config"
mkdir -p "$VAULT/.claude/skills/gm/steps"
mkdir -p "$VAULT/_scripts"

# Copy skill files
cp "$SOURCE/SKILL.md" "$VAULT/.claude/skills/gm/"
cp "$SOURCE/config/"*.md "$VAULT/.claude/skills/gm/config/"
cp "$SOURCE/steps/"*.md "$VAULT/.claude/skills/gm/steps/"
cp "$SOURCE/_scripts/cleanup_daily_note.py" "$VAULT/_scripts/"

# Make Python script executable
chmod +x "$VAULT/_scripts/cleanup_daily_note.py"

echo ""
echo "Done! Next steps:"
echo "  1. Edit .claude/skills/gm/config/repos.md with your git repo paths"
echo "  2. Edit .claude/skills/gm/config/style-reference.md for your work vocabulary"
echo "  3. Create vault structure: journal/daily/, journal/weekly/, journal/monthly/"
echo "  4. Create Daily Standup.md (or update step files if using different name)"
echo ""
