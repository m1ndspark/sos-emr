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
- 3-ARG replaceAll(search, replace, true) DOES NOT STRIP (2026-07-23). The 2-arg
  regex form replaceAll("[^0-9]", "") strips non-digits correctly, but adding the
  third boolean regex-flag argument, replaceAll("[^0-9]", "", true), leaves the
  non-digits in place. A formatted 10-digit phone (AAA-BBB-CCCC) kept its dashes,
  so length() was 12 and a length()==10 validation fired a FALSE block on a valid
  number. FIX: use the 2-arg form; every other phone/ID formatter in the repo does.
  Found live on Employees "Validate Employee Phone Block". Do not pass the third
  argument to replaceAll in this build.
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

================================================================================
CREATOR v6 FINDINGS  (from the 2026-07-29 invoice-engine build, source .ds
SOS_Referrals_App_2026-07-29.ds)
================================================================================
- Report custom actions execute once per selected record, so a report action
  cannot pass a whole multi-select to one function. This is why the Invoice_Batch
  form exists as a staging record: the selection is written to the batch, then one
  function (run_invoice_batch) processes the batch.
- There is no read-only field property. Use "disable Field;" in an On Load
  workflow to lock a field.
- There is no conditional-mandatory property. Enforce it with an On Validate
  workflow: alert, then "cancel submit;". "cancel submit" takes no message
  argument.
- Lookup display formats cannot traverse two hops. A second-hop value must be
  denormalized into a text field on the intermediate form (this is why
  Partner_Location_Label exists on the PVS and referral forms).
- Setting a field via Deluge does not fire that field's On User Input workflow.
  Any dependent logic must be triggered explicitly, not assumed to cascade.
- Creator mobile offline mode blocks any form carrying before-submit workflows
  (on load, on user input, field rules). Encounter_PatientVisit and Referrals_Main
  both carry such workflows, so neither can ever be offline-capable.

================================================================================
CREATOR v6 FINDINGS  (2026-08-05, Session 28 - July import + rate repair)
================================================================================

CRITERIA MATCHING ON EMAIL FIELDS IS CASE-SENSITIVE
Partner_Referral_Contacts[Partner_POC_Email == v_Email] MISSES when the stored
value differs only in letter case. If that field is also `unique`, the miss
falls through to the insert branch and violates the constraint at runtime:
"The field 'org' for key 'Email' is configured to reject duplicate values."
FIX PATTERN: exact-match fetch first (fast path), then a full-table fallback
scan comparing .trim().toLowerCase() on both sides, and only insert if both
passes come up empty.
Found live: 20 of 278 referrals failed the July import - LexieJoiner@ vs the
stored lexiejoiner@. See workflow Partner_Contact_Upsert.

PHONENUMBER FIELDS REJECT AN EMPTY STRING
Assigning "" to a field of type phonenumber throws:
"The value of the field 'X' doesn't conform to a phone number format."
Assign null instead when the value is blank.
WATCH WHEN COPYING BETWEEN FORMS: Referrals_Main phone fields are plain `text`;
Encounter_PatientVisit phone fields are `phonenumber`. A value that is legal on
one side is not automatically legal on the other.
Found live: backfill_pvs_from_referral, first execution.

IMPORTS DO NOT FIRE ON USER INPUT
Extends the existing note that a Deluge assignment does not fire On User Input.
The import wizard's "Execute form workflows" checkbox covers On Add, On Success
and On Validate - it does NOT fire On User Input either.
CONSEQUENCE: Referral Link Pre-Fill is On User Input, so setting Referral_Link
from link_pvs_to_referral leaves every referral-derived field blank. Any
programmatic Referral_Link assignment must be followed by
backfill_pvs_from_referral.

REPORT BULK EDIT DOES NOT RELIABLY WRITE RADIOBUTTON FIELDS
Bulk-editing Partner_Rate_Status (type radiobuttons) from the Partner Rates
report reported success and wrote nothing - the field stayed blank across ~170
records across two attempts. Record DELETIONS from the same UI in the same pass
did save. Use a function for bulk writes to radiobutton fields.

THE FUNCTION EDITOR DOES PROMPT FOR ARGUMENTS
Executing a custom function from the Deluge editor opens an "Enter the value for
the input arguments" dialog. A function with arguments does NOT need a no-arg
wrapper to be run by hand. run_reset_test was built on the opposite assumption
and is unnecessary.

set_current_rate DEPENDS ON Partner_Rate_Status - HANDLE WITH CARE
set_current_rate only considers rows where Partner_Rate_Status == "Active". If
no row for a given key qualifies, it finds no winner and then sets EVERY row for
that key to Current_Rate = "No". A blank status therefore SILENTLY UN-PRICES the
whole rate card the next time backfill_current_rate runs.
RULE: never run backfill_current_rate without first confirming every rate row
carries a status. Bulk-imported rate rows arrive with the status blank.
Found live: wiped ~170 Current_Rate flags on 2026-08-05, recovered with
repair_partner_rate_status.

STAMPED CHARGES DO NOT FOLLOW A RATE CHANGE
Complexity_Charge is written onto the PVS at the moment of lookup, and
backfill_pvs_complexity_charge only fills BLANKS. Changing a rate card therefore
has no effect on visits already stamped - correct for invoiced visits, a trap
for un-invoiced Drafts, which keep the old price silently.
Found live: INV-000006 billed VITAS Sumter Moderate at 343 after the card said
323. Use reprice_draft_pvs for Draft, un-invoiced visits only.

PROCESS NOTE - READ THIS FILE FIRST
The "cancel submit takes no message" rule was already documented in this file in
two places and was still gotten wrong on 2026-08-05. Read context/05 before
writing any Deluge, not after the parse error.
