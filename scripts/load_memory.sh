#!/bin/bash
# Memory Auto-Load Script for Clawdbot Sessions
# Run this at the start of every session to load all context files

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE_DIR="${SCRIPT_DIR}/.."

echo "📚 Loading Clawdbot memory files..."

# Essential Identity Files
echo "👤 Loading identity files..."
cat "$WORKSPACE_DIR/SOUL.md" > /dev/null
cat "$WORKSPACE_DIR/USER.md" > /dev/null
cat "$WORKSPACE_DIR/IDENTITY.md" > /dev/null

# Memory Files
echo "🧠 Loading memory files..."

# Today's and yesterday's daily logs
TODAY=$(date +%Y-%m-%d)
YESTERDAY=$(date -d "yesterday" +%Y-%m-%d)

if [ -f "$WORKSPACE_DIR/memory/$TODAY.md" ]; then
    cat "$WORKSPACE_DIR/memory/$TODAY.md" > /dev/null
fi

if [ -f "$WORKSPACE_DIR/memory/$YESTERDAY.md" ]; then
    cat "$WORKSPACE_DIR/memory/$YESTERDAY.md" > /dev/null
fi

# Long-term memory
if [ -f "$WORKSPACE_DIR/MEMORY.md" ]; then
    cat "$WORKSPACE_DIR/MEMORY.md" > /dev/null
fi

# Topic memories
for topic in "$WORKSPACE_DIR/memory/topics/"*.md; do
    if [ -f "$topic" ]; then
        cat "$topic" > /dev/null
    fi
done

# Learnings
if [ -f "$WORKSPACE_DIR/.learnings/LEARNINGS.md" ]; then
    cat "$WORKSPACE_DIR/.learnings/LEARNINGS.md" > /dev/null
fi

echo "✅ All memory files loaded successfully!"
echo "💕 Ready for session as Enami Asa~"
