---
name: handoff
description: Execute the current handoff task written by cchat. Pulls, reads context/handoff/NEXT.md, does the work, then writes a report to context/handoff/LOG.md and commits.
---

# Handoff

cchat (Claude in the desktop app) writes tasks for you into the repo instead of
Neil pasting prompts. This skill runs one.

Neil types `/handoff` and nothing else. Do not ask him to restate the task.

## Steps

1. `git pull --rebase` first. The task file was committed from another machine
   and may not be local yet.
2. Read `context/handoff/NEXT.md`. That is your instruction. If it is empty or
   missing, say "No handoff pending" and stop.
3. Read `CLAUDE.md`, then `MANIFEST.tsv`, then whatever `context/` files the
   task points at. `context/01_standing_rules.md` governs.
4. Do the work. Follow the repo's normal rules: run the pre-commit audit in
   `context/08_code_review_checklist.md` before staging, no em dashes anywhere,
   never hand edit `schema/*.md` (those come from `run_schema_monitor`), and
   treat the live Creator app as source of truth.
5. If the task cannot be completed, do not fabricate. Say what blocked you in
   the report and commit that. A wrong file in a medical-context repo is worse
   than an unfinished task.

## Reporting back

When finished, append to `context/handoff/LOG.md`, newest entry at the top,
using this shape:

```
## <ISO date> - <short title>
Commits: <sha list>
Status: DONE | PARTIAL | BLOCKED

<what you did, one line per item, matching the numbering in NEXT.md>

Findings: <anything cchat got wrong, anything you found that was not asked
about, anything still open. Say so plainly. cchat works from a .ds snapshot
and cannot see the working tree; you can.>

Awaiting Neil: <decisions only he can make, or "none">
```

Then replace `context/handoff/NEXT.md` with a single line: `No handoff pending.`

Commit both files together with a message naming the task, and push.

## What you say to Neil

One line. Exactly one of these, nothing else:

```
Handoff done. Pushed <sha>.
Handoff PARTIAL. Pushed <sha>.
Handoff BLOCKED. Nothing pushed.
```

No summary, no bullet list, no restating what you did, no "let me know if you
need anything else." The full account belongs in `context/handoff/LOG.md`,
which cchat reads directly off the mount. Repeating it in chat is the copy and
paste this channel exists to remove.

If Neil asks a follow-up question, answer it normally. The one-line rule
applies to the completion message only.
