# SOS Code Checkpoint - 2026-09-08 - Session 41

Covers work since the Session 40 EOD log (2026-09-05). Session ran 09-06 -> 09-08.

--------------------------------------------------------------------------------
## 1. DOB standardization (DONE)
--------------------------------------------------------------------------------

Permanent convention established:
- `Patient_DOB` (date) is the canonical field everything reads and writes.
- `Patient_DOB1` (text) is the intake landing pad the Zoho Form writes into;
  workflows parse it across.

Delivered and saved:

1. `Referrals Main On Create - Master` - added the `Patient_DOB1` ->
   `Patient_DOB` parse (month/day/leap-year validated) and fixed
   `Assignments.Patient_DOB`, which was receiving text into a date field.
2. `backfill_patient_dob("COMMIT")` - filled history. 4 eligible, 1 parsed and
   written (REF-1112), 3 unparseable (REF-1096 / REF-1097 test records,
   REF-1108 with `44/44/4444`).
3. Assignments pre-fill workflows consolidated. `Assignment_Pull_From_Referral`
   (Created or Edited) kept and repointed to `Patient_DOB`; `Assignment Pull
   From Referral` (Created) deleted. Both fired on create and disagreed on
   `Facility_Phone`, so which value landed depended on execution order.
4. `build_referral_email_html` and `build_3008_email_html` - both now read
   `Patient_DOB` formatted `M/d/yyyy`. Subject lines carried forward as
   `REF Visit: [Patient] - [REF-ID]` and `REF 3008: [Patient] - [REF-ID]`.
5. `Referrals_Main_Report` - `Patient_DOB1` column removed from the list and
   detail views, replaced with the date field displayed as "Patient DOB".

Follow-on items found during the full sweep, also closed:

6. `Referral DOB Sync On Edit` - NEW workflow on `Referrals_Main` (Edited,
   On Success). Parses `Patient_DOB1` into `Patient_DOB` on edit. Guarded by
   `v_Rec.Patient_DOB != v_DobDate` so the update does not re-trigger the
   workflow. This was the gap that caused REF-1098's notification to keep
   showing a blank DOB after a manual entry.
7. `Referral Link Pre-Fill` - the 46-line DOB1 parse fallback removed; now
   reads `input.Patient_DOB = v_Rec.Patient_DOB;`.
8. Provider portal profile - `Patient_DOB1` hidden via Field Permissions;
   `Patient DOB (system)` left visible.

The date field `Patient_DOB` was given the display name "Patient DOB (system)".
Link name unchanged. Necessary because the Forms -> Creator mapping picker
showed two fields both labeled "Patient DOB" with no way to tell them apart.

Verification: `diag_dob_coverage()` returned
`records=340 | both=45 | DOB only=284 | DOB1 only=0 | neither=11 | mismatched=0`.
Zero DOB1-only and zero mismatches proves the date field holds everything the
text field does. A live zform Patient Visit submission was then confirmed to
populate both fields.

--------------------------------------------------------------------------------
## 2. Root cause - DOB missing on every non-3008 referral
--------------------------------------------------------------------------------

Every Patient Visit and Imaging Order referral from REF-1109 onward arrived
with no DOB. Ruled out in order: the Creator mapping target (correct - pointed
at `Patient_DOB1`), the Forms question (only one exists), the field's own
visibility (Show, mandatory), and the grid's default visibility (not hidden).

Actual cause: `Patient DOB` sat inside a grid that was named as the target of
the 3008 rule's Show action, which makes Zoho Forms hide that grid at runtime
until the rule fires. SSN rendered because it is outside that grid. Neil fixed
it by adding a second rule covering Patient Visit and Imaging Order.

LESSON: in Zoho Forms, naming a field or grid in a rule's Show action
implicitly hides it by default at runtime, regardless of what the Builder shows.

--------------------------------------------------------------------------------
## 3. Data_Issues guard (NEW)
--------------------------------------------------------------------------------

New field `Data_Issues` (multi-line) on `Referrals_Main`.

New workflow `Referral Data Issues Check` (`Referrals_Main`, Created,
On Success): writes "Missing Patient DOB" into `Data_Issues` when both DOB
fields are empty, and emails `neil.heird@sosmmc.com`. Chose flag-and-notify
over an On Validate block so a partner's submission is never rejected outright
- same failure mode as the referral that went missing on 09-05.

New function `backfill_data_issues(string p_mode)` - PREVIEW/COMMIT,
idempotent, recomputes and clears stale flags. Final run:
`records=343 | flagged=0 | cleared=2 | unchanged=341`.

Recipient is deliberately Neil only - Josh's inbox volume is already too high.

--------------------------------------------------------------------------------
## 4. Referral Date - resolved, no code change
--------------------------------------------------------------------------------

The `Referrals_Main_Report` column labeled "Referral Date" was bound to
`Partner_Link.Added_Time`, the partner record's creation timestamp, which is
why whole blocks of referrals shared 07-04-2026 or 06-30-2026. Confirmed by the
field tooltip: Field name Added Time, Related field Partner Lookup, Related
form Partners.

`Referral_Date` itself is correct and is written in exactly one place - the
master workflow's `v_RefDate = zoho.currentdate` on create. It is not sourced
from Zoho Forms at all. `diag_referral_dates()` returned
`records=332 | blank=1 | matches AddedTime=47 | differs=284`, with historical
dates matching the date embedded in each Referral ID.

Decision: `Referral_Date` stays a date field. The typed-input-mask question
only applies to dates a human keys in - Patient DOB and the
`Encounter_PatientVisit` dates.

--------------------------------------------------------------------------------
## 5. New diagnostics
--------------------------------------------------------------------------------

- `diag_referral_dates()` - Referral_Date vs Added_Time distribution.
- `diag_dob_coverage()` - DOB/DOB1 population and mismatch counts.

--------------------------------------------------------------------------------
## 6. Non-EMR work
--------------------------------------------------------------------------------

Removed `asmith@sosmmc.com` from 3008 notifications (Employee record,
`Email_Notification_Types`). Confirmed 3008 recipients are every Active
employee carrying "3008 Evals" plus a hardcoded `sosreferrals@sosmmc.com`.

Wrote the RingCentral AI receptionist master instruction for "Mia" (ext. 1001)
- company description, greeting, 911-first protocol, routing table
(Josh 101 / Neil 102 / voicemail), telemarketer handling, FAQ, and hard rules.
Delivered as `SOS_AI_Receptionist_Master_Instruction.md`.

--------------------------------------------------------------------------------
## 7. Open
--------------------------------------------------------------------------------

- 11 referrals still have no DOB on file and need values keyed in.
- REF-1108 has `44/44/4444` in `Patient_DOB1` - partner submitted junk, needs a
  real DOB.
- Nine 3008 files remain permanently gone from WorkDrive; partners must resend.
- Corrupt originals still sit beside good replacements; REF-1108 is at the
  3-file cap.
- Manual partner branch still needed: REF-072826-1460, REF-072826-1461,
  REF-072326-1413.
- Orphan record 4904890000000480011.

--------------------------------------------------------------------------------
## 8. Queued, not started
--------------------------------------------------------------------------------

- 3008 PVS "Reason for Referral" -> auto-populate "Cares 3008 Evaluation".
- SSN required on 3008 in `PVS_Required_Fields`.
- Imaging Order notification.
- `get_referral_details` Custom API - blocked on `Type_of_Entry` vs
  `Referral_Type` reconciliation.
- PVS zform build and mapping.
- Provider Dashboard portal page buttons.
- 3008 Advanced Directives suppression conflict.
- Reconcile Forms Large List (26 entries) against 29 active partner locations.
- Live create-time notifications still attach via `build_zepto_attachments`
  (WorkDrive); switching them to `build_creator_attachments` was offered and
  not yet approved.

--------------------------------------------------------------------------------
## 9. Process note
--------------------------------------------------------------------------------

Neil flagged that when a field link name changes, the sweep of every reference
must happen immediately and exhaustively - .ds, workflows, functions, reports,
portal permissions, templates - rather than surfacing gaps one symptom at a
time. That full sweep was run and is recorded in section 1.
