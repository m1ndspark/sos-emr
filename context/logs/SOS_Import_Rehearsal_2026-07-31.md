# SOS EMR Go-Live Import Rehearsal - 2026-07-31 (Session 28)

Status: PASSED END TO END. Run against small throwaway ZZTEST sample files, not
the real 250-visit backlog. Hard launch: Monday, 2026-08-03.

--------------------------------------------------------------------------------
## Sequence proven
--------------------------------------------------------------------------------
1. Import Referrals (Referrals_Main), branch value in the Partner_Branch text
   field (lookups do not import; see findings).
2. resolve_referral_branch_from_text - match Partner_Branch text to
   Partner_Locations.Partner_Location_Label, set the Partner_Branch_Link lookup.
3. backfill_referral_branch - resolve remaining referral branch links.
4. Import PVS (Encounter_PatientVisit).
5. backfill_pvs_ids - mint PVS_ID, build PVS_Referral_ID, repair Has_Referral_ID.
6. link_pvs_to_referral - link each PVS to its referral.
7. backfill_pvs_billing_branch - set Billing_Branch from the location record.
8. backfill_pvs_complexity_charge - fill Complexity_Charge from the rate card
   (Billing_Branch + Complexity_Level + Current_Rate = "Yes").
9. Invoice Batch -> create_invoice_from_selection -> Zoho Books.

--------------------------------------------------------------------------------
## Result
--------------------------------------------------------------------------------
- Books invoice INV-000005 created: 2 visits, $888.00.
- Then voided cleanly via reset_invoice (both Creator and Books; PVS returned to
  Draft). Void-never-delete path re-confirmed.

--------------------------------------------------------------------------------
## New functions exercised (all created live 2026-07-31, ahead of v14)
--------------------------------------------------------------------------------
- backfill_pvs_ids - mints PVS_ID from Sequence_Tracker where blank, builds
  PVS_Referral_ID as "PVS-<Referral_ID>", repairs blank Has_Referral_ID from
  whether Referral_ID is populated. Writes all three fields in ONE update
  statement per record. GOTCHA FOUND THE HARD WAY: two separate update
  statements on the same record inside one for-each pass do not both take effect
  - the second is dropped. Combine into a single update.
- resolve_referral_branch_from_text - see step 2 above; reports unmatched values.
- backfill_pvs_complexity_charge - fills Complexity_Charge only where blank or
  zero, never overwrites; skips Complexity_Level "No Charge"; reports missing
  branch/level rate combinations.
- backfill_pvs_patient_full_address - builds Patient_Full_Address from the PVS
  address sub-fields. First run: 18 built.

--------------------------------------------------------------------------------
## Creator import findings
--------------------------------------------------------------------------------
See context/09_cognito_import_procedure.md (Section 5A, hand-verify mapping) and
the CREATOR IMPORT FINDINGS gotchas in _INDEX.md. Headline: Creator's auto-map
silently mis-assigns columns, so every column mapping must be verified by hand
before any import.

--------------------------------------------------------------------------------
## Test fixtures
--------------------------------------------------------------------------------
Committed under context/test-fixtures/ so the rehearsal is repeatable:
DRYRUN_1_Referrals_ZZTEST.csv (21 cols), DRYRUN_1_Referrals_ZZTEST_v2.csv
(21 cols, branch to text field), DRYRUN_2_PVS_ZZTEST.csv (20 cols),
COVERAGE_Referrals_ZZTEST.csv (every importable referral field),
COVERAGE_PVS_ZZTEST.csv (every importable PVS field). Both coverage files
imported with ALL fields landing (address sub-fields included) once the mapping
was set by hand. DRYRUN_RUNBOOK.txt (the 9-step runbook) was NOT found in
~/Downloads and is not yet committed - pending from Neil.
NOTE: the two COVERAGE files carried two synthetic SSN-shaped placeholder values
in Patient_SSN; both were scrubbed to "REDACTED" in the committed copies to keep
the repo clear of SSN-shaped data per the standing rule. Field coverage is
unaffected.
