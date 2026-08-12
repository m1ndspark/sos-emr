# SOS Code - CHECKPOINT - 2026-08-12 (Session 31)

Mid-session record. Covers work since the Session 30 EOD log
(claude/SOS_Code_Session_Log_2026-08-11_Session30_EOD.md).

--------------------------------------------------------------------------------
## 1. Headline
--------------------------------------------------------------------------------

The Zoho Form -> Creator referral pipeline was rebuilt end to end and is now
working for both new and returning partner contacts. Four separate
Referrals_Main workflows were consolidated into one master On Success workflow,
and the free-text branch question was replaced by a searchable dropdown of
canonical location names that Creator resolves into the full partner block.

--------------------------------------------------------------------------------
## 2. Referrals Main On Create - Master (NEW, replaces 2 workflows)
--------------------------------------------------------------------------------

**Form:** Referrals_Main | **Record event:** Created | **Form event:** On Success

Why: integration-inserted records never fire On User Input events, so every
formatter and generator built that way silently skipped form-submitted
referrals (phones, SSN, full address, AC full name all arrived raw or blank).
Consolidating also fixed the On Success ordering race - Creator does not
guarantee order between two On Success workflows, so the upsert could copy
unformatted values.

Order of operations inside the master:
1. `mint_referral_id(input.ID)`
2. Stamp `Referral_Date = zoho.currentdate` (always - overrides any mapped value)
3. Format 4 phones to XXX-XXX-XXXX and SSN to XXX-XX-XXXX
4. Build `Patient_Full_Address`, `AC_Full_Name`, `Patient_Full_Name`,
   `Partner_POC_Name_Title`
5. Resolve `Partner_Location_Label` (the dropdown value) against
   `Partner_Locations.Partner_Location_Name`, Active only, exact then
   case-insensitive
6. From the matched location write: `Partner_Organization`, `Partner_Branch`,
   `Partner_Location_Label`, `Partner_Link`, `Partner_Branch_Link`,
   `Partner_ID`, `Partner_ID_Stamp`
7. Contact upsert (email match, case-insensitive fallback) writing the derived
   org/branch plus `Partner_Link` and `Partner_Locations_Link`

Retired into it and DELETED: **REF ID Generator**, **Partner Contact Upsert**.
Switched to record event **Edited** only: **Patient Full Name Generator**,
**Partner POC Name & Title Generator** (master builds these on Create).
All On User Input workflows left intact for in-Creator edits.

Note: `Partner_ID_Stamp` is the Partners record ID (matches mint_partner_id's
convention), not the referral's own ID.

--------------------------------------------------------------------------------
## 3. Branch capture redesign - dropdown replaces free text
--------------------------------------------------------------------------------

Problem: partners were typing branch names free-hand and had no way to know SOS
conventions ("Suncoast - PIN" vs "Pinellas").

Design landed:
- The Forms questions "Referral Partner Organization" and "Partner
  Branch/Location" are both GONE, replaced by one searchable grouped dropdown,
  **Referral Partner Lookup** (~80 options, grouped by partner, values are bare
  location names).
- Maps to Creator field `Partner_Location_Label` in the integration.
- Creator derives organization, branch text, partner ID and both lookups from
  the matched location record. Nothing is parsed or split.

Duplicate-name question settled with `diag_duplicate_location_names`: zero
duplicate Active location names exist. The convention that makes this safe is
Neil's - embed the brand when a county name would repeat across partners
(Empath uses "Suncoast - HIL"/"Suncoast - PIN"; AccentCare uses plain
"Hillsborough"/"Pinellas"). Location CODES do duplicate, but nothing matches on
code. Keep the convention when adding locations.

Residual risk (tracked, not built): if two Active locations ever share a name,
the resolver binds to whichever is found first, silently. Three-part safety net
is on the task list - exactly-one match check, unresolved-partner alert email,
and an On Validate uniqueness guard on Partner_Locations.

--------------------------------------------------------------------------------
## 4. get_partner_referral_contact - rewritten twice
--------------------------------------------------------------------------------

Change 1: read branch and organization through `Partner_Locations_Link` and
`Partner_Link` first, falling back to the text fields. Returning contacts
created by the new upsert had only the lookups populated, so the old
text-only read returned blank and the dropdown had nothing to select.

Change 2: return `Partner_POC_Phone` as **digits only**. The Forms phone
question is a three-box (###/###/####) field and cannot parse "343-434-3434".
Also strips a leading country-code 1 from 11-digit values.

Both confirmed working live.

--------------------------------------------------------------------------------
## 5. Zoho Forms configuration changes
--------------------------------------------------------------------------------

Prefill mapping (form Builder -> Partner POC Email field -> prefill config,
NOT the Creator integration screen):
- `/result/Partner_Branch` -> **Referral Partner Lookup** (new)
- `/result/Partner_POC_Phone` -> Partner POC Phone
- existing: POC first/last/title/team, Lookup_Status, Lookup_Message
- Test & Verify must be re-run before the key list refreshes

Creator integration map:
- Removed the stray **Prior POC Email <- Partner POC Email** row (that Forms
  field is separately mapped correctly; the prior-email path was dropped in
  Session 29)
- Added **Partner Location Label <- Referral Partner Lookup**
- Removed the Partner Branch/Location row with the deleted question

Page rule specced for Patient Visit (skip Imaging Order Details): on General
Information, If Service Requested Is Patient Visit -> skip to Partner Lookup
Details. Confirmed that Partner Lookup Details follows Imaging Order Details,
so the forward-only skip works. Not confirmed built.

--------------------------------------------------------------------------------
## 6. SendGrid notification template - built, not wired
--------------------------------------------------------------------------------

Decision: Zoho Forms' own notification emails CANNOT show the Referral ID -
they send at submit time, before Creator mints it, and there is no write-back
path that re-fires them. Zoho Flow was also rejected: its record-created
trigger races the On Success mint. The send will be appended to the end of the
master workflow, after the mint, using the existing `sendgrid_connection` and
a `send_via_sendgrid` variant that posts `template_id` +
`dynamic_template_data`.

Template built in SendGrid Dynamic Templates (hand-authored HTML, no drag-drop
for the tables):
- Tables at 16px, 5px cell padding, #d0d5dd borders, no zebra striping
  (striping breaks when conditional rows are hidden)
- Location block uses `{{#equals Patient_Location "Facility"}} ... {{else}} ...
  {{/equals}}` with TWO complete tables. Row-level conditionals inside a table
  get hoisted above it by the HTML parser - conditionals must sit BETWEEN
  tables, not between rows.
- Alternate contact block wrapped in `{{#if AC_First_Name}}`, single row:
  first/last - phone - relationship
- Merge tags match Creator link names exactly, capitalized
  (`{{Patient_Location}}`, `{{AC_Relationship_to_Patient}}`, etc.)
- Navy header cells (#0b0b5b) need `color:#ffffff` on the LABEL cell, not the
  value cell

Recipients are internal only (Neil + providers), so the PHI-to-unencrypted-
inbox concern is deferred until a partner-facing template exists.

Mobile font sizing: media queries in a `<style>` block work in ~85-90% of
clients but are stripped by Gmail-app-with-non-Google-accounts and some
Outlooks. Fluid-hybrid technique does not help - it scales width, not type.
Deferred; 16px is already an acceptable mobile size.

--------------------------------------------------------------------------------
## 7. Other decisions
--------------------------------------------------------------------------------

- **Click-to-call**: Creator renders the call icon only for phonenumber-TYPE
  fields. Referrals_Main and Imaging_Orders phones are text-typed. Conversion
  deferred behind any remaining CSV imports (Phone Number fields validate
  format on import). Tracked.
- **Books 2000-char line-item cap**: Max Invoice Total mitigates for capped
  partners but uncapped batches (VITAS, AccentCare) and long partner-written
  reasons still expose it. Annotated on the task list, not fixed.
- **Actions log**: default Creator audit captures failures only. Neil wants a
  full transaction log built out from Change_Log / log_change. Tracked, design
  TBD.
- **iframe height**: the referral page clips Back/Next when the lookup message
  appears, because the prefill-driven grid does not fire a Zoho resize message.
  Chosen fix is a focus-triggered +220px bump that resets on every page change
  (no permanent whitespace). Delivered; a constant-buffer version and
  `scrolling="auto"` were the rejected alternatives.

--------------------------------------------------------------------------------
## 8. Test records to clean up
--------------------------------------------------------------------------------

REF-1047 through REF-1052 in Referrals_Main are test submissions from this
session, plus the neilheird@gmail.com row in Partner_Referral_Contacts.
Delete before go-live or the fake contact will keep prefilling.

--------------------------------------------------------------------------------
## 9. Immediately next
--------------------------------------------------------------------------------

1. Fresh .ds export - v22 is already stale (BLOCKING repo sync)
2. SendGrid template ID + final merge-tag list from Neil, then the send step
3. Verify PVS Required Fields end to end (16 Mandatory flags already unset)
4. Delete test referrals and the test contact

END
