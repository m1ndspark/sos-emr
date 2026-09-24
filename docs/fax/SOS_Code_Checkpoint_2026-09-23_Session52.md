# SOS Code - CHECKPOINT 2026-09-23 (Session 52)

September referral export cleaned and re-imported. Null Billing_Branch root
cause closed. Four read-only diagnostics run. Generic field editor live over the
Creator v2.1 API.

Source: SOS Code Session Log 2026-09-23 (Session 52, EOD). Patients are
referenced by PVS and REF ID only.

## September referral import

- Export of all September referrals: 107 rows, 47 columns. 60 rows correctly
  shaped. 47 had the FULL partner label in Partner Organization, leaving Partner
  Branch and Partner Lookup empty.
- The clean rows set the four-column convention and twelve canonical labels.
  See `docs/data/SOS_Referral_Partner_Field_Convention.md`.
- 46 of 47 resolved. REF-1545 resolved to AccentCare - Broward, not among the
  twelve September labels but confirmed as a real active location (code BRO)
  against a Partner_Locations export. REF-1500 was blank on all four partner
  columns and could not be resolved.
- Delivered `Referrals_Partner_Fix_Sept2026.xlsx`: 46 rows, Referral ID plus the
  four partner columns, headers matching the export exactly. Imported into
  Creator successfully on the first attempt.

## Null Billing_Branch - root cause closed

- Defect: `Referral_Sets_Billing_Branch` fires only on user input of
  `Referral_Link`, so a PVS that acquires its referral any other way never got a
  `Billing_Branch`. The only guard, Billing Branch Required, was disabled in
  Session 51.
- The v52 export shows that workflow as `Referral_Sets_Billing_Bra`. The export
  truncates workflow link names to 25 characters; the live link name is
  `Referral_Sets_Billing_Branch`.
- NEW workflow `PVS Sets Billing Branch On Save`, Encounter_PatientVisit,
  Created or Edited, On Validate. Fills `Billing_Branch` only when empty.
  Derives from the referral's `Partner_Branch_Link`, falling back to matching
  Partner_Locations on the referral's organization and branch text when that
  link is null. Copies the three partner text fields, then sets
  `Complexity_Charge` from the current Partner_Rates row, because Branch Sets
  Charge fires only on user input and does not fire when Deluge sets the field.
- NEIL RULING: fill blanks only. A Billing_Branch that disagrees with its
  referral is left alone, so a manual override survives.
- `backfill_pvs_billing_branch` REWRITTEN: return type String to Map, `p_mode`
  added, report mode writes nothing. The prior version overwrote every PVS
  carrying a referral, had no fallback and never set Complexity_Charge.
  - Report: 8 resolved, 0 unresolved, 0 without a referral.
  - Applied: the same 8, plus 79 no-referral PVS whose partner TEXT was
    refreshed from Partner_Locations. Billing_Branch untouched on those 79.
  - Verified: re-run in report mode returned resolved 0.
  - The 8: PVS-1052-JK, PVS-1053-JK, PVS-1504-JK, PVS-1505-JK (Direct -
    Individual); PVS-1742-AS, PVS-1743-AS (InnoVage - Orlando); PVS-1750-JK
    (Empath - Suncoast - PIN); PVS-1751-JK (AccentCare - Pinellas).

## Diagnostics run

All four are read-only. Results and the open discrepancy are recorded in
`docs/fax/SOS_Fax_Console_Design.md` section 13.

- `diag_fax_readiness`, p_days 180: 447 unfaxed, 389 ready to fax. Blocked: no
  billing branch 4, no fax number 22, duplicate contacts 0, not Final 5, empty
  note 27. Referrals missing branch link 1 (REF-1500).
- `diag_missing_pvs_fax` (NEW): 24 Partner_Locations, 16 with a usable PVS fax
  on an Active billing contact.
- `diag_unfaxed_by_branch` (NEW): 59 unfaxed, 0 without a billing branch, 3
  blocked by a missing fax number.
- `diag_sept_pvs_completeness` (NEW): September, 60 Patient Visits, 54 complete.
  Only gap: six missing Facility Room Number.

## Generic field editor

- Deluge cannot assign a field by name string (`rec.(v_name) = v_val` is not
  valid), so a generic editor goes through the Creator REST API.
- NEW connection `creator_api` (Zoho OAuth) and NEW function `admin_set_field`.
  See `docs/admin/SOS_Admin_Set_Field.md`.
- Proven on REF-1500: Partner_Organization set to a test value, confirmed on the
  form, then cleared.

## Decisions taken

- PVS Sets Billing Branch On Save fills blanks only (NEIL RULING).

## Findings

- Deluge has NO backslash escape for a double quote. `"\""` is an Improper
  Statement error. Build the string another way or pre-encode it: `%22` for the
  quote, `%3D%3D` for `==`.
- Creator v2.1 `max_records` accepts ONLY 200, 500 or 1000. Any other value
  returns code 9250.
- The .ds export truncates workflow link names to 25 characters. Never quote an
  export link name of exactly 25 characters as the real one.
- A field set by Deluge does NOT fire that field's on-user-input workflow.
  Anything that workflow would do must be repeated inline.
- Search the .ds for an existing function before writing a new one.
  `backfill_pvs_billing_branch` already existed and a duplicate was written
  before the miss was caught.

## Open

BLOCKING
- Six September PVS missing Facility_Room_Number: PVS-1528-JK, PVS-1534-AS,
  PVS-1535-AS, PVS-1539-AS, PVS-1544-JK, PVS-1754-JK. Neil only.
- 447 vs 59 unfaxed discrepancy between `diag_fax_readiness` and
  `diag_unfaxed_by_branch`. The 389 backlog figure is not trustworthy until
  settled.
- Fresh .ds export. v52 (13:12) predates Sessions 51 and 52.

NEXT UP
- REF-1500: no partner on any of the four fields, and the only referral
  missing Partner_Branch_Link.
- PVS fax numbers for AccentCare - Pasco and Chapters - LifePath, the only two
  branches blocking notes. Chapters - Good Shepherd, Chapters - HPH Hospice,
  Cornerstone - Main and Direct - Individual have no billing contact but block
  nothing today.
- PVS-1479 to PVS-1504 empty-note block. Never investigated.
- How the unfaxed backlog gets sent, once the count is trusted.

CARRIED FROM SESSION 51
- Expose the four api_ functions as Custom APIs and build the Fax Console
  widget.
- `retry_failed_faxes` permanently fails console faxes.
- `fmt_referral_source` not wired into `build_pvs_fax_html` or
  `build_console_docs`.
- Fax Attachments related block add-record control.
- `Partner_POC_Name_Title` holding an email on at least one referral.
- Mandatory PVS field marking, PARKED.

## Cold start notes

- Billing_Branch now has two backstops: the On Validate workflow fills it on
  every save, and `backfill_pvs_billing_branch` cleans up in bulk with a dry run
  first. Zero PVS are currently without one.
- `admin_set_field` is the general-purpose single-record repair tool.
- The four diagnostics never write.
- The fax backlog is far smaller than it first appeared: only three notes are
  blocked by a missing fax number.

## Repo drift

None of this session's Creator objects are in any export. v52 predates both
Sessions 51 and 52. See the REPO DRIFT row in `context/23_task_list.md`.
