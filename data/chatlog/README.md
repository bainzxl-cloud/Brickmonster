# Chat memory layout

This folder holds **raw conversation logs** (everything).

- One NDJSON file per channel/session.
- Each line is one JSON object: {ts, channel, author, messageId, text}

Curated memory lives in:
- `MEMORY.md` (long-term, distilled)
- `memory/YYYY-MM-DD.md` (daily notes)

Raw logs are **not** searched by default memory tools to keep latency low.
Use `scripts/recall.ps1` to quickly pull relevant lines.
