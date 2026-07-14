================================================================================
PHONE / FAX FORMATTER LEARNINGS  (PROVEN 2026-07-10, on Partner_Billing_Contacts)
================================================================================
Context: building the app-wide AAA-MMM-LLLL phone/fax formatter (see context/12
Section B for the full standard + template). These are the Creator-behavior
findings that shaped it.

- subString(start, end) end-index is EXCLUSIVE in this build: subString(0,3)
  returns 3 chars (indices 0,1,2). Confirmed live: 8135551234 formatted correctly
  to 813-555-1234 with subString(0,3)/subString(3,6)/subString(6,10). (Reconciles
  the older bare "subString(0,3) works" note with exact boundary behavior.)

- RE-ENTRY LOOP (important): an On-User-Input formatter that WRITES its own field
  (input.FIELD = ...) can RE-TRIGGER the same On-User-Input event -> it reformats
  -> re-triggers -> infinite loop. Symptom live: an endless spinner on the field
  and the form will NOT save. FIX: a re-entry guard - build the target string
  first, and if the field already equals it, return without re-assigning:
    v_Formatted = ...;
    if(v_Raw == v_Formatted) { return; }
    input.FIELD = v_Formatted;

- FIELD MAX-CHARACTERS FIGHTS A FORMATTER: if a field's formatted output is longer
  than its raw input (e.g. 813-555-1234 = 12 chars vs 10 raw digits), a low
  max-char limit blocks the formatter's own output and/or fires Creator's built-in
  validation. Do NOT use max-char as a digit cap for formatted fields; leave it
  generous/unset and enforce length in the formatter + On-Validate.

- GENERIC "Invalid entries found. Rectify and submit again." popup is Creator's
  FIELD-LEVEL validation. Its text is NOT editable, and it fires BEFORE (or instead
  of) a custom On-Validate alert. To surface a field-specific message, remove the
  field-level rule (usually a max-char or pattern) so your On-Validate alert +
  cancel submit is the sole gatekeeper.

- REJECT vs TRIM: for identity/billing numbers, prefer REJECT (leave a wrong-length
  entry unformatted so it visibly reads as broken) over silently trimming to the
  last/first 10 digits (which can hide a typo). Pair with On-Validate to block save.

- Confirms the existing note that On User Input fires on BLUR, not per keystroke:
  mid-typing the field can briefly show an unformatted/half state; the real
  guarantee is On-Validate at submit, not the live formatter.

CONFIRMED WORKS (add)
- input.FIELD = null;  clears a field's value in On User Input (used in the PVS
  wipe-on-deselect logic).
- alert "..."; cancel submit;  in an On Validate workflow shows a custom message
  and blocks the save (per-field validation messaging).

# Deluge Learnings (Creator)

Source: Deluge/Creator module and the May 8 session log. Creator behavior wins
over generic Deluge docs.

CONFIRMED WORKS
- zoho.loginuserid returns the full email. Use this for all employee lookups.
- matches("regex") works in On User Input.
- replaceAll("-", "") strips specific characters.
- Escape regex special characters with a double backslash, e.g. replaceAll for an
  open parenthesis must escape it as \\(.
- subString(0, 3) works.
- update v_Rec inside a loop is the confirmed Sequence_Tracker update pattern.
- enable FieldName; enables a disabled field.
- disable FieldName; makes a field read-only.
- if(condition) with parentheses works in On User Input.
- Record fetches return collections and require a for-each loop.
- cancel submit requires no message string in v6.

CONFIRMED DOES NOT WORK
- zoho.loginuser returns the org name, not the email. Do not use for lookups.
- An unescaped open parenthesis in replaceAll fails (regex special character).
- update FormName[ID == v_SeqID.toLong()] is unreliable. Use the loop pattern.
- getPrefix() / getSuffix() do not work. Use subString() instead.
- cancel submit in On User Input does not work. It is available on Validate only.
- Real-time keystroke input masking is not possible in Creator. On User Input
  fires on blur, not on keypress. Best available UX is format-on-blur plus
  placeholder text.
- PARENTHESIZED ||-SUBGROUP INSIDE A COMPOUND if REVERTS ON SAVE (2026-07-14).
  A condition like  if(A && B && (C || D))  -- parentheses grouping an OR inside a
  larger &&-chain -- is SILENTLY STRIPPED by Creator on save, reverting to
  if(A && B && C || D), which parses as (A && B && C) || D (&& binds tighter than
  ||). No error is shown; the grouping is just gone. FIX: split into NESTED ifs,
  which Creator keeps:  if(A && B){ if(C || D){ ... } }  -- equivalent, survives
  the round-trip. Found on PVS_ID_Stamp_Generator. Corollary lessons: VERIFY ANY
  FIX PERSISTED by REOPENING the saved workflow (Creator can silently drop
  constructs it won't accept), and test the EDIT/re-submit path, not just fresh
  creates -- a fresh record's null field can mask a precedence bug that only bites
  on re-submit when the field == "".

SEQUENCE GENERATION PATTERN (REUSABLE)
- Query by the 3-letter prefix code, not the long display name.
  Example: Sequence_Tracker[Object_Prefix == "MPR"]
- Update with update v_Rec inside the loop.
- Typical fields: a long descriptive name (display only), a 3-letter prefix code
  (all queries use this), a numeric sequence (starts at 1001), a lock status.
- "Stamp" means Creator's native 19-digit system ID only. Never use the word
  stamp for custom human-readable IDs.

OAUTH / CUSTOM API
- Creator Custom API requires BOTH scopes: ZohoCreator.report.READ and
  ZohoCreator.customapi.EXECUTE. Report read alone gives an invalid scope error.

CREDENTIALS
- Runtime secrets live in Zoho Connections, invoked by connection name so the
  value never appears in a field, record, export, or script.
- Human and infrastructure logins live in a password manager.
- Never store secrets in a Creator form, field, or record, or in this repo.

================================================================================
DEPENDENT LOOKUP FILTER / DEPENDENT DROPDOWN  (PROVEN 2026-07-02)
================================================================================
Filter a child lookup by a parent selected on the SAME form (e.g. show only the
selected partner's locations in Partner_Location_Link on Partner_Rates):
- Child lookup field -> Field Properties -> Choices -> check "Set filter" -> criteria:
    Field    = "ID" nested UNDER the parent-lookup heading (e.g. under "Partner Link")
    Operator = equals
    Value    = input.<ParentLookupLinkName>   e.g.  input.Partner_Link   (TYPE it)
- KEY: the value box accepts a TYPED field reference  input.<FieldLinkName>  (not just static text).
- Lookup fields do NOT appear as top-level filter criteria; drill into the lookup heading and pick its ID.
- An EMPTY Set filter (checkbox on, no criteria row) applies NO filtering -> shows everything.
- Mirrors Zoho KB "Dynamically Filter Lookup Options Based on Another Lookup Field's Selection"
  (their example: Asset Name filtered by ID equals input.Category).

================================================================================
LOOKUP DISPLAY FIELD MUST BE RELIABLY POPULATED  (2026-07-02)
================================================================================
Symptom: a lookup dropdown shows "No matches found" (or blanks) even for records
that clearly exist and pass the filter.
Cause: the lookup's DISPLAY field was set to a value that is empty on the target
records. Example - Partner_Location_Link display set to Partner_Location_Label,
but that label is populated only by the Location Label Generator (On Success,
Created/Edited); existing locations created earlier had a BLANK label (backfill
never run) -> the dropdown had nothing to display -> "No matches".
Fix: set the lookup display to an always-populated field (Partner Loc Name), OR
run the backfill so the label field is filled before using it as a display field.
Rule: only use a generator-populated field as a lookup DISPLAY after its backfill
has run for all existing records.
