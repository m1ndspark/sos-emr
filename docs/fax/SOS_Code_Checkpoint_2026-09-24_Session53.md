# SOS Code - CHECKPOINT 2026-09-24 (Session 53)

A Creator criteria bug had been under-reporting the fax backlog by 343 notes.
Referral intake defect traced to the Zoho Form. Provider portal and a new
validation model designed. September send cleared.

Source: SOS Code Session Log 2026-09-24 (Session 53, EOD). Patients are
referenced by PVS and REF ID only. This log supersedes several Session 52
conclusions, marked SUPERSEDES below.

## The criteria bug (highest-value finding)

- In a Creator criteria, `Field != "value"` does NOT match records where that
  field is null. It drops them silently. Full write-up:
  `context/24_creator_criteria_null_trap.md`.
- Found because `diag_unfaxed_by_branch` reported 59 unfaxed notes while the
  rewritten fax digest reported 402 on the same data. The diag's
  `Fax_Status != "Sent"` excluded every note never faxed.
- FIXED by moving the test out of the criteria and into the loop:
  `resolve_pvs_fax_target` (LIVE, shared fax gate), Fax This Note Preview And
  Gate (LIVE, PVS-form tickbox gate), `diag_fax_readiness` (diagnostic).
- Both live fixes also corrected a second defect: the old code took the first
  matching contact and stopped, so the duplicate count came from a separate
  pass. Both now come from one pass.
- STILL UNFIXED: `diag_unfaxed_by_branch` and the remaining `!=` criteria.
- SUPERSEDES Session 52: "only 3 notes are blocked by a missing fax number" was
  wrong. The real number is 20.

## Fax digest rewritten

- 33 PVS notes faxed manually did not appear on the digest. By design: the
  digest reports exceptions only and has no sent section.
- The unfaxed section counted only notes added MORE than 24 hours ago and after
  a hardcoded floor of 22-Sep-2026. The failures section had no time window.
- NEIL RULING: cumulative, no date exclusions, drop the floor.
- `send_fax_digest` REWRITTEN: 24-hour cut and floor removed, both note
  sections headed "all outstanding", oldest first, Added date column on both
  tables. The 24-hour window is kept for the overrides section only.
- First run: missed 402, prelim 4, failures 0, overrides 3.
- The digest is now a standing worklist, not an alert. It will be non-empty
  every morning until the backlog clears.

## Referral intake defect, root cause

Full write-up: `docs/data/SOS_Referral_Intake_Root_Cause.md`.

- `referrals_missing_branch_link` went from 1 to 4 overnight: REF-1556,
  REF-1557, REF-1558.
- `process_new_referral` wraps branch resolution in
  `if(v_SubmittedLabel != "")`, reading `Partner_Location_Label`. Empty on all
  three, so it never ran. The label arrived in `Partner_Organization`.
- Sender Sets Branch fires only on user input of `Partner_POC_Email`, never on
  an API or form submission.
- Cause on the form: two dropdowns draw from one nested Large List; users pick
  a location in the required org box and skip the optional branch box.
- Second source: `get_partner_referral_contact` returned
  `Partner_Location_NAME` while the dropdown offers `Partner_Location_LABEL`.
  FIXED, now returns `Partner_Location_Label`.
- NEIL RULING: one flat branch dropdown, drop the org question. Creator derives
  the organization from the location record.

## Zoho Form list reconciled

- InnoVage - Orlando and VITAS - Villages were missing from the form. BOTH ADDED
  by Neil. Reconciliation complete.
- SUPERSEDES Session 52: AccentCare - Broward IS on the form, below the fold.

## Partner data architecture

Full write-up: `docs/data/SOS_Referral_Partner_Field_Convention.md`, Part 2.

- Four-level copy chain, 17 writers on `Partner_Branch` alone.
- NEIL RULING: link is truth, text is display. One resolver writes every text
  field. Nine-step plan agreed, NOT YET BUILT.

## Diagnostics and numbers

`diag_fax_readiness`, p_days 0, after the criteria fix:

| Measure | Count |
|---|---|
| unfaxed | 407 |
| excluded cancelled | 18 |
| ready to fax | 359 |
| no billing branch | 0 |
| no fax number | 20 |
| duplicate contacts | 0 |
| not Final | 5 |
| empty note | 23 |
| referrals missing branch link | 4 |

`diag_missing_pvs_fax`: 24 locations, 16 with a usable fax. Unchanged from
Session 52.

NEW this session: `diag_room_number_gaps` (read-only), `fix_six_room_numbers`
(one-shot, already run).

## September send - CLEARED

- The six PVS missing `Facility_Room_Number` (PVS-1528-JK, PVS-1534-AS,
  PVS-1535-AS, PVS-1539-AS, PVS-1544-JK, PVS-1754-JK) were all REAL gaps:
  the referral lacked the value too. Partners never supplied them. Five
  facilities, six records, one patient twice.
- NEIL DECISION: set to "Unknown". "Not Provided" was rejected:
  `Facility_Room_Number` is capped at 8 characters on Referrals_Main and
  Assignments.
- Six referrals set via `admin_set_field`, six PVS via `fix_six_room_numbers`.
- VERIFIED: `diag_sept_pvs_completeness` returns 60 checked, 60 complete, all
  gap lists empty.
- Source fix identified, not applied: a Zoho Forms field rule can set
  Facility Room # mandatory when patient location is Facility.

## Provider portal and validation model

Full write-up: `docs/portal/SOS_Provider_Portal_Design.md`. Design agreed,
nothing built.

- Dashboard with My Info, My Assignments, My PVS Notes. Both list pages carry an
  action-item column.
- New `PVS_Status`: In Progress, Completed stored; Not Started computed.
- Josh's ruling is now a principle: nothing blocks a PVS save.
- Native field Mandatory RULED OUT. SUPERSEDES the parked Mandatory-PVS-fields
  row.
- Data ownership: inherited values written once at creation and frozen.

## Platform decision - opened, not made

`Claude outputs/SOS_EMR_v2_Platform_Case_2026-09-24.md` already exists in the
repo and is the platform decision record. The log cites it as
`claude/SOS_EMR_v2_Platform_Case_2026-09-24.md`; the file is under
`Claude outputs/`. Not duplicated here. Fly.io compliance pricing ($99/mo)
unconfirmed.

## Everything changed in Creator

FUNCTIONS UPDATED
- `resolve_pvs_fax_target` - criteria fix, single-pass count
- `diag_fax_readiness` - criteria fix, Cancelled excluded and reported
  separately
- `send_fax_digest` - cumulative, floor and 24h cut removed
- `get_partner_referral_contact` - returns `Partner_Location_Label`

FUNCTIONS CREATED
- `admin_set_field` - generic single-record field editor
- `diag_room_number_gaps` - read-only
- `fix_six_room_numbers` - one-shot, already run

WORKFLOW UPDATED
- Fax This Note Preview And Gate - criteria fix

CONNECTION CREATED
- `creator_api` - Zoho OAuth, scopes ZohoCreator.meta.form.READ, report.READ,
  report.UPDATE. Access ON for SOS Referrals App.

DATA WRITTEN
- `Facility_Room_Number = "Unknown"` on 6 referrals and 6 PVS.

ZOHO FORM
- InnoVage - Orlando and VITAS - Villages added to the Partner Locations list.

## Open

DECIDE BEFORE BUILDING
- Do `Type_of_Procedures` and `Provider_ICD10_Codes_Link` count toward
  PVS_Status Completed, or are they advisory? Blocks the completeness set,
  which blocks PVS_Status.
- What happens when a provider starts a second note for the same patient?

NEXT UP
- Fix `diag_unfaxed_by_branch` (still has the bad criteria).
- Sweep the remaining `!=` criteria.
- Build the partner resolver (nine steps).
- Add PVS_Status and repurpose PVS Required Fields.
- Zoho Form conditional mandatory on Facility Room #.
- Delete Build Patient Full Address from Encounter_PatientVisit.
- Decide the fate of `backfill_pvs_from_referral` and
  `relink_pvs_to_referral` given freeze-at-creation.
- Write the provider portal spec.
- Confirm Fly.io compliance pricing in writing.

CARRIED
- 359 notes ready to fax, no decision on how they go out.
- 20 notes blocked on a missing fax number.
- 23 empty notes, PVS-1479 to PVS-1506, never investigated.
- REF-1500 has no partner on any field.
- Expose the four api_ functions as Custom APIs; build the Fax Console widget.
- `retry_failed_faxes` permanently fails console faxes.
- `fmt_referral_source` not wired into either fax builder.
- Fax Attachments related block add-record control.
- `Partner_POC_Name_Title` holding an email on at least one referral.

## Learnings

1. Creator criteria: `Field != "value"` does not match nulls. Test in the loop,
   not the criteria.
2. Zoho Forms: choice-based field rules do not support Global Choices, so a
   saved list cannot drive a dependent dropdown.
3. Zoho Forms: field rules DO include "Set Fields as Mandatory".
4. Creator: native field Mandatory blocks the save and fires before workflows.
   No visual-only setting.
5. Creator: field length caps are silent until the API rejects them.
   `Facility_Room_Number` is 8 characters.
6. Zoho Forms cannot populate a dropdown from Creator. Any list is a
   hand-maintained copy.
7. Deluge: an on-user-input workflow never fires on an API or form submission.

Also: read the .ds before claiming anything about the app. Twice this session a
statement from memory was wrong where the file was right.

## Repo drift

The v53 export and ds_sync were committed earlier this session, but v53
PREDATES every Creator change listed above. Do NOT run ds_sync against v53 for
these. Wait for v54.
