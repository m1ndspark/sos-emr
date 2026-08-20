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
NOTE (repair_partner_rate_status is not in any export): it was executed live on
2026-08-05 and recovered roughly 170 Current_Rate flags wiped by
backfill_current_rate. It does not appear in the v19 (08-05 18:25, exported after
the repair ran) or v20 (08-08) exports, so it was a one-off that was deleted
after use and has never existed in a versioned artifact. The outcome is the
recovery recorded just above; the function body is not recoverable from the repo,
and if the same recovery is needed again it must be rewritten. Do not treat its
absence as export drift. The closest existing function is fix_accentcare_current_rate
(present in v20, same shape of repair); worth checking whether the rate-status
recovery was actually run under that name.

STAMPED CHARGES DO NOT FOLLOW A RATE CHANGE
Complexity_Charge is written onto the PVS at the moment of lookup, and
backfill_pvs_complexity_charge only fills BLANKS. Changing a rate card therefore
has no effect on visits already stamped - correct for invoiced visits, a trap
for un-invoiced Drafts, which keep the old price silently.
Found live: INV-000006 billed VITAS Sumter Moderate at 343 after the card said
323. Use reprice_draft_pvs for Draft, un-invoiced visits only.

PREMIUM STAMPS HAVE THE SAME TRAP AS COMPLEXITY
Premium fees (After_Hours_Fee, Super_Stat_Fee) are stamped onto the PVS the same
way as Complexity_Charge, and backfill_pvs_premium_fees only fills BLANKS, so a
wrong non-blank premium never self-corrects. Premium rates are PER-PARTNER, so a
cross-partner value is a live risk (the same error class as the complexity stamp
above). Found live: the July run stamped Empath Super STAT at $200, which is
AccentCare's rate, instead of Empath's $400 on four visits, under-billing $800.
RULE: correcting a stamped premium needs a repricing pass (a reprice_draft_pvs
equivalent for premiums), then void-and-rebill for invoiced visits;
backfill_pvs_premium_fees will not do it. See context/30 section 2.

PROCESS NOTE - READ THIS FILE FIRST
The "cancel submit takes no message" rule was already documented in this file in
two places and was still gotten wrong on 2026-08-05. Read context/05 before
writing any Deluge, not after the parse error.

phonenumber FIELDS REJECT VALUES A FUNCTION WROTE IN LOCAL FORMAT
A phonenumber field with no allowedcountries setting rejects values a function
wrote in local format. Patient_Phone and Facility_Phone declare
allowedcountries={us} and get normalized to E.164 on import; Partner_POC_Phone
did not, and its raw "(352) 237-6979" values made all 200 imported PVS records
unsaveable from the form, surfacing only the generic "Invalid entries found"
popup because the offending field was disabled and showed no error of its own.
RULE: any value a function writes into a format-constrained field must be
normalized first.

HIDING A FIELD DOES NOT CLEAR IT
Hiding a field does not clear it. Unticking Additional Charges hid
Equipment_Charge_Amount but left the value in place, and
create_invoice_from_selection billed it. Always clear the value when hiding an
optional charge field.

--------------------------------------------------------------------------------
SESSION 29 (2026-08-08) - ZOHO FORMS, BOOKS API, .ds STALENESS
--------------------------------------------------------------------------------

ZOHO FORMS FIELD RULES ARE LIVE; ONLY PAGE RULES OFFER AN ELSE
A field rule reverts its action on its own when the condition stops matching,
so no Else branch is needed and none is offered. Else exists only on Page
Rules. Do not build paired show/hide rules to undo each other.

ZOHO FORMS: ONE RULE PER TARGET QUESTION - GROUP RULES BY CONDITION
A rule's action list can target many fields, but a given field should appear
in only one rule. When two branches need to hide the same field, do NOT write
one rule per branch; write one rule whose condition is the OR of both. Group
rules by CONDITION, not by outcome. Use Add Group with the OR operator so the
expression reads ( A1 OR A2 ) - a sub-group inside one group ANDs instead and
will never match.

ZOHO FORMS PAGE SKIP-TO ONLY JUMPS FORWARD
Any page that every branch needs must sit either before the branch point or
after all branches. A skip rule also belongs on the page immediately BEFORE
the page being skipped, not on the page where the deciding question lives -
skipping from page 1 jumps over everything in between.

ZOHO FORMS: NOTE ELEMENTS ARE NOT TARGETABLE BY RULES
The rule action list only offers fields that accept input. A conditional
message must live in a real input field (read-only Multi Line), not a Note.
Better still, have the API return the message text itself so no rule is
needed at all - the field either has a message or it does not.

ZOHO FORMS PREFILL MAPPING CACHES THE RESPONSE SHAPE
A newly added response key will not appear in the Prefill Mapping dropdown
until step 2 Test & Verify is re-run. Save the Creator function first, then
re-run Test & Verify, then map.

CROSS-ORIGIN: NOTHING ON THE HOST PAGE CAN REACH INSIDE THE FORM
The Zoho form renders in an iframe from forms.zohopublic.com. No CSS or JS
from WordPress or from a Creator portal page can style or script anything
inside it; !important does not help because the rule is never delivered to
that document. Custom CSS is unavailable on the current Forms plan, so
anything inside the form can only be changed through Themes.

ZOHO FORMS HTML/CSS EXPORT DROPS ALL LOGIC
Exporting the form as HTML/CSS gives full styling control but does not
support hidden fields, field rules, page rules, or captcha. For any form with
branching it is not a usable option.

CREATOR'S PAGE-BUILDER HTML ELEMENT STRIPS SCRIPT TAGS
Embeds placed in a Creator page must be a bare iframe with no JavaScript.

THE ZOHO FORMS -> CREATOR FIELD MAP CANNOT BE EDITED
Changing any mapped field requires deleting the integration and re-selecting
every field by hand. Budget for this before renaming or removing fields on
Referrals_Main.

ZOHO BOOKS: to_mail_ids TAKES RAW EMAIL ADDRESSES
POST /invoices/{invoice_id}/email accepts to_mail_ids as a list of email
addresses, not contact-person IDs, and they go in the request BODY (in the
URL yields error 1038). This means an in-app approval dashboard can send an
invoice to any recipient list assembled in Creator without populating Books
contact persons at all. Error 7008 ("no contact persons associated with this
invoice") means to_mail_ids was omitted or misplaced.

THE CREATOR INVOICE PAYLOAD SENDS NO payment_terms
create_invoice_from_selection posts customer_id, date, reference_number and
line_items only. Books therefore falls back to the customer record's terms.
All customers were Due on Receipt until set to Net 30 by hand on 2026-08-08.
If terms need to be per-invoice, add payment_terms to the payload.

EMAIL MATCHING IS CASE-SENSITIVE EVERYWHERE, NOT JUST IN THE UPSERT
The same defect that broke 20 referral imports (context/28) was present in
get_partner_referral_contact, the prefill lookup: an exact-match fetch on
Partner_POC_Email silently returned nothing when the stored address differed
only in case. Both now carry a lowercase fallback scan. Assume any Deluge
criteria match on an email field needs one.

THE v19 .ds IS STALE - DO NOT TRUST IT FOR FUNCTION BODIES
As of 2026-08-08 the committed .ds predates a growing set of live changes.
Its copy of run_invoice_batch has neither the p_maxTotal cap nor the
Visit Cancelled skip. reset_invoice, get_partner_referral_contact, and the
backfill/repair functions written since do not appear in it at all. Re-export
before relying on it to read any function body.

INTEGRATION-INSERTED RECORDS FIRE ON SUCCESS BUT NEVER ON USER INPUT
A record created by a native Zoho Forms -> Creator integration (or any API
insert) triggers On Success workflows but does NOT trigger On User Input
workflows, because no human typed into a field. Any formatter, generator, or
ID mint built as On User Input silently skips every form-submitted record.
Consolidate that logic into one On Success workflow. This is what drove the
Referrals_Main master-workflow rebuild.

CREATOR DOES NOT GUARANTEE ORDER BETWEEN TWO ON SUCCESS WORKFLOWS
Two On Success workflows on the same form have no defined execution order
relative to each other. If step B depends on a value step A wrote, they cannot
be two separate workflows. Any sequence-dependent chain must live inside a
single script.

ZOHO FORMS THREE-BOX PHONE FIELDS CANNOT PARSE A DASHED STRING
A phone field split into area / prefix / line boxes will not accept a prefill
value like 813-513-1925; the dashes break the split. A prefill webhook feeding
one of these must return digits only.

SENDGRID HANDLEBARS: ROW-LEVEL CONDITIONALS INSIDE A TABLE GET HOISTED
An {{#if}} wrapped around a <tr> (or <td>) inside a <table> is pulled ABOVE the
table by the HTML parser before the template renders, so the conditional row
lands in the wrong place. Conditionals must wrap a whole <table>, not rows
inside one. Build one full table per conditional block.

ZEBRA STRIPING BREAKS WHEN CONDITIONAL ROWS ARE HIDDEN
Alternating row-background striping assumes every row renders. When some rows
are conditional and drop out, the stripe pattern misaligns. On any table that
contains conditional content, use cell/row borders instead of background
striping.

ATTACHMENTS_SELECT:UI.ADD(LIST) DOES POPULATE A MULTI-SELECT AT RUNTIME
Confirmed live 2026-08-20. A multi-select field's choices CAN be built at runtime:
    <field>:ui.clear();
    <field>:ui.add(v_list);
THIS CORRECTS AN EARLIER CLAIM IN THIS REPO THAT IT WAS IMPOSSIBLE. It is not.
Valid in On Load and On User Input ONLY. It does NOT work in On Validate, On
Success, or a standalone function, because those run with no form UI attached.
Used by the PVS Fax Review On Load to build the attachment picker from the PVS
file-upload fields.

A FORM CANNOT BE TOGGLED TO STATELESS AFTER IT EXISTS
"Data will be stored in Zoho Creator" is set at creation and is not editable
afterward. To make an existing form stateless:
  Open Form Builder > More > Duplicate, with "Data will be stored in Zoho
  Creator" UNCHECKED, then delete the original and rename the duplicate.
Everything bound to the original name (workflows, report references, page
links) has to be repointed after the rename. Confirmed 2026-08-20 building
PVS_Fax_Review.

CREATOR V6 KEEPS THE REPORT URL STATIC, SO A RECORD ID CANNOT BE READ FROM THE
ADDRESS BAR
When a record detail or edit view opens from a report, the address bar stays on
#Report:<ReportName>. The record ID never appears in the URL. Any flow that needs
to hand a record ID to another form or page must get it from somewhere else: add
the System ID field as a REPORT COLUMN and read it from there. Confirmed
2026-08-20 wiring the PVS report to PVS_Fax_Review.

STANDALONE FUNCTION .DG FILES ARE BODY-ONLY
Per repo convention a standalone function's .dg holds the body without the
declaration line, so it round-trips as the Creator function editor expects.
Consequence when pasting OUT of the repo INTO Creator: the declaration line has
to be re-added by hand, with the correct return type, name and parameter list.
The signature is recorded in MANIFEST.tsv and in the function's own docs.

CREATOR PHONE FIELDS CANNOT RESOLVE A COUNTRY FROM A ZOHO FORMS "(813) 300-2086"
Confirmed live 2026-08-20. A Creator phone field configured
allowedcountries={us} / defaultcountry="us" stores digits UNFORMATTED. Zoho Forms
sends the display format "(813) 300-2086" with NO country code. Creator cannot
resolve a country from that string, so it:
  - renders the wrong country flag on the field, and
  - marks the field INVALID as soon as the record is opened,
which blocks a save on a record nobody actually edited.
The value is not corrupt, it is unresolvable. Creator needs the country, and
neither the parentheses-and-space format nor a bare ten digits supplies it.
FIX IS TWO PARTS, neither started:
  1. Normalize to +1 plus ten digits AT THE POINT THE REFERRAL IS WRITTEN, so
     nothing new arrives unresolvable.
  2. A one-time backfill over existing rows.
Part 1 without part 2 leaves every existing record broken; part 2 without part 1
re-breaks on the next intake. Tracked in context/23_task_list.md.
RELATED, ALREADY IN THIS FILE: "PHONENUMBER FIELDS REJECT AN EMPTY STRING" and
the Referrals_Main text vs Encounter_PatientVisit phonenumber type mismatch. Same
family of problem, different trigger.
