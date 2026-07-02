# Pre-Commit Code Review / QA Checklist (EMR)

Purpose: this is the QA gate a workflow passes before its .dg file is committed
to the repo. It stands in for the review, linting, and staging test a human dev
team runs before merging. Because this is a medical-context app, a wrong field
name or a colliding workflow has real clinical and billing consequences.

WHEN THIS RUNS
- Automatically whenever Neil asks to commit or push code. Claude runs the full
  checklist and presents the result BEFORE staging anything.
- On request mid-draft ("audit this"), for an early check.
- Neil can override per change ("just commit, skip the audit") when confident.
- Docs-only changes (context files, _INDEX.md) are exempt; this gate is for
  Deluge and workflow changes.

THE HONESTY BOUNDARY (READ FIRST)
The live Creator app is the source of truth and Claude CANNOT see it. Claude can
verify logic, naming against what the repo documents, trigger choice, idempotency,
and collisions against documented workflows. Claude CANNOT confirm the real
current field link names, workflows that were never written down, or live data.
Every audit ends with a "VERIFY LIVE" list: the assumptions only Neil can confirm
by opening the Creator app or a real record. An audit is never a substitute for
Neil's live test (working loop step 4).

--------------------------------------------------------------------------------
1. CORRECTNESS
--------------------------------------------------------------------------------
- Null safety: a `for each ... [ID == x]` loop that finds nothing leaves the var
  at its initial value. Confirm that path is handled, not assumed to always match.
- Data types: dates compared as dates, IDs handled with .toString() where a text
  stamp is written, numbers not compared to text.
- input. vs record reference used correctly for the trigger context.
- Idempotency: any function or backfill is safe to re-run without double-writing
  or drifting. Re-running it on already-correct data must be a no-op.
- Logic matches the plain-language logic map that was agreed before coding.

--------------------------------------------------------------------------------
2. TRIGGER CORRECTNESS
--------------------------------------------------------------------------------
- Right event for the job:
    On Validate  = block or reject bad input (cancel submit).
    On Success   = act after save, e.g. stamp an ID that only exists post-save.
    On Create vs Create-or-Edit = confirm which, and rename the file to match.
- Blocking logic (branch-match, dedupe) is On Validate, not On Success.
- No show()/hide() outside On User Input. No procedural Deluge in field display
  rules (condition expressions only). See context/01 and context/05.

--------------------------------------------------------------------------------
3. COLLISIONS AND REGRESSIONS (the "other parts of the app" check)
--------------------------------------------------------------------------------
- Same form + same event: does another workflow already fire here? Two On Success
  scripts editing the same record can overwrite each other. List every known
  workflow on that form (forms and workflows are one unit) and check for conflict.
- Field dependency: does this change a field that another script, lookup, filter,
  or lookup DISPLAY relies on? (Reference bug: setting a lookup display to a
  generator-populated label that is blank on old records -> "No matches found".
  See context/05.)
- Backfill scope: does a sweep touch records that a live On Success workflow also
  maintains? Confirm they agree, not fight.
- New field added: is anything filtering or deduping on its previous absence?
- Field link name reused across forms with different meaning?

--------------------------------------------------------------------------------
4. FIELD AND SCHEMA ALIGNMENT
--------------------------------------------------------------------------------
- Every field link name referenced is confirmed against context/06_field_link_names
  or flagged as VERIFY LIVE. Never guess a link name. (Recurring bug:
  Partner_Location_Code vs Partner_Loc_Code.)
- Display label vs link name distinction respected.
- Field deletion, if any, follows: remove all workflow references first, then
  delete, after checking View Field References. See context/01.

--------------------------------------------------------------------------------
5. DATA INTEGRITY, SAFETY, PHI
--------------------------------------------------------------------------------
- Object IDs are workflow-generated and read-only; no inline ID generation in
  On User Input.
- Record locking respected on Sequence_Tracker reads (duplicate-ID risk).
- ICD-10 only for any medical coding.
- No PHI, secrets, tokens, or test records in the code or commit.
- No PHI passed to external AI services or into SMS or QuickBooks.

--------------------------------------------------------------------------------
6. REPO HYGIENE
--------------------------------------------------------------------------------
- .dg file is pure Deluge, no comment headers, full function (round-trips into
  Creator cleanly).
- File path encodes form and trigger, matching the OnEvent__Name.dg convention.
- Standalone functions live in functions/.
- Non-Deluge logic (condition-expression show/hide) recorded as a note in the
  form folder, not as a .dg.
- _INDEX.md status row and any relevant context file updated in the same commit.
- No em dashes.

--------------------------------------------------------------------------------
7. OUTPUT OF AN AUDIT
--------------------------------------------------------------------------------
Claude reports each item as one of:
    PASS    - checked, no issue.
    FLAG    - a problem Claude found; fix before commit.
    VERIFY LIVE - an assumption only Neil can confirm in Creator (with the exact
                  thing to check, e.g. "open one Partner_Rates record and confirm
                  the link name is Partner_Location_Link").
Nothing is staged while any FLAG is open. VERIFY LIVE items are listed for Neil
but do not block the commit; they carry into the live test (working loop step 4).
