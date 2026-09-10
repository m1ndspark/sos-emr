# Handoff channel

Purpose: move task instructions and reports between cchat (Claude in the
desktop app) and ccode (Claude Code in this repo) through git instead of
through Neil's clipboard.

## How it works

Outbound, cchat to ccode:
  1. cchat writes the task to NEXT.md and commits.
  2. Neil types `/handoff` in ccode.
  3. ccode pulls, reads NEXT.md, does the work.

Inbound, ccode to cchat:
  4. ccode appends its report to LOG.md, resets NEXT.md, commits and pushes.
  5. Neil says "ccode's done" in the desktop app.
  6. cchat reads LOG.md directly off the mounted repo.

Neil's part is `/handoff` in one window and three words in the other. Nothing
is copied or pasted.

## Rules

- NEXT.md holds exactly one task at a time. cchat overwrites it.
- ccode never leaves NEXT.md populated after a run. Reset it to
  "No handoff pending." so a stale task cannot be run twice.
- LOG.md is append only. Never rewrite history in it.
- If ccode is blocked, that goes in LOG.md as BLOCKED with the reason. Do not
  leave the task in NEXT.md hoping it resolves.
- cchat writes to this repo through the desktop mount and can read LOG.md
  without Neil relaying it.
