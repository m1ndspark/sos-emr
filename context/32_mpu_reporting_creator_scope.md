# MPU Reporting in Creator - Implementation Scope

Status: DRAFT for Neil's approval. Written 2026-09-09 (Session 42).
Governing spec: claude/SOS_MPU_Reporting_Instructions_v1.md (v1, 2026-08-13).

--------------------------------------------------------------------------------
## 1. Goal
--------------------------------------------------------------------------------
Replace the intermediate normalized spreadsheet
([MONTH][YEAR]_MPU_Normalized_Data.xlsx) with native Creator reports.

Neil still produces the partner-facing Word/PDF report from that output. The
insights narrative, savings model presentation and formatting stay outside
Creator for now.

NOT in scope: the Word/PDF partner report, the insights narrative, chart
generation, and the color-coded workbook formatting.

--------------------------------------------------------------------------------
## 2. What already works
--------------------------------------------------------------------------------
Every canonical column except Date Of Referral is already denormalized onto
`Encounter_PatientVisit` at entry, so the Master export is a single-form report
with no join.

| Canonical column | Source field on Encounter_PatientVisit |
|---|---|
| Referral ID | Referral_ID |
| Date Completed | Visit_Completion_Date |
| Partner | Partner_Organization |
| Branch | Partner_Branch |
| Reason For Referral | Reason_for_Referral |
| First / Last | Patient_First_Name / Patient_Last_Name |
| DOB | Patient_DOB |
| Acuity | Complexity_Level |
| After Hours | Additional_Charges + After_Hours_Fee |
| SuperStat | Additional_Charges + Super_Stat_Fee |
| Equipment / Equip $ | Additional_Charges + Equipment_Charge_Amount |
| Hospice ID | Patient_Hospice_ID |
| Provider | Employee_Name_Title |

Set A (referral-side) insights are fully supported today:
`Referral_Added_Time` gives time-of-day buckets, `Referral_Source` separates
self-generated referrals, `Patient_Hospice_ID` serves as MRN for new vs repeat,
and conversion is referrals with no linked PVS.

--------------------------------------------------------------------------------
## 3. Field additions (Encounter_PatientVisit)
--------------------------------------------------------------------------------
Provider-facing, placed with `Type_of_Procedures`:

| Link Name | Display Name | Type | Choices |
|---|---|---|---|
| Procedures_Performed | Procedure(s) Performed | Multi Select | same 15 choices as Type_of_Procedures |

`Type_of_Procedures` remains what was addressed. `Procedures_Performed` is the
subset actually done. Anything in the first list and not the second is an eval.
This derives Performed vs Eval without a second data-entry step and feeds the
savings model by counting Procedures_Performed entries by type.

QC-only, placed in System_Fields_Section beside `QC_Reviewed`:

| Link Name | Display Name | Type | Choices | Initial value |
|---|---|---|---|---|
| Row_Status | Row Status | Dropdown | Counted, Duplicate, Cancelled, Folded, Needs Review | Counted |
| Duplicate_Of_PVS_ID | Duplicate Of | Single Line (255) | | |
| Row_Status_Note | Row Status Note | Multi Line | | |

System, placed in System_Fields_Section:

| Link Name | Display Name | Type |
|---|---|---|
| Referral_Date | Referral Date | Date |

--------------------------------------------------------------------------------
## 4. Workflow and function additions
--------------------------------------------------------------------------------
| Artifact | Type | Purpose |
|---|---|---|
| OnUserInput__Referral_Link__PreFill | UPDATE | Also pull Referrals_Main.Referral_Date into Encounter_PatientVisit.Referral_Date |
| backfill_pvs_referral_date | NEW function | Stamp Referral_Date on all existing PVS from the linked referral. PREVIEW / COMMIT. |
| backfill_pvs_from_referral | EXISTING | Must run after any imported or programmatic Referral_Link assignment (context/28 rule 1) |

No new workflow is needed for Row_Status. It is set by hand during the monthly
QC pass.

--------------------------------------------------------------------------------
## 5. Reports to build
--------------------------------------------------------------------------------
| Report | Base form | Filter | Purpose |
|---|---|---|---|
| MPU_Master | Encounter_PatientVisit | Visit_Completion_Date in target month | Master tab equivalent. All canonical columns plus Row_Status, Duplicate Of, Row Status Note. |
| MPU_By_Branch | Encounter_PatientVisit | same, Row_Status = Counted, grouped by Partner_Branch | Per-branch tabs equivalent |
| MPU_QC_Review | Encounter_PatientVisit | same, Row_Status != Counted | QC and Excluded tab equivalent |
| MPU_Missing_PVS | Referrals_Main | Referral_Date in target month, no linked PVS, excluding 3008 and SOS Internal | Conversion gap list for Set A item 10 |

Month selection: a page variable set from a date picker, referenced in each
report's filter, rather than editing the report each month.

--------------------------------------------------------------------------------
## 6. Monthly QC pass (the human step)
--------------------------------------------------------------------------------
1. Open MPU_Master for the target month.
2. Read the clinical note on every row where the classification is not obvious.
3. Set Row_Status to Duplicate, Cancelled or Folded as the spec directs, filling
   Duplicate_Of_PVS_ID and Row_Status_Note.
4. Set Row_Status to Needs Review on anything that hits a QC gate.
5. Confirm Procedures_Performed matches the note on every paracentesis and
   thoracentesis row.
6. Export MPU_By_Branch and MPU_Master.

--------------------------------------------------------------------------------
## 7. Known gaps carried forward, not solved here
--------------------------------------------------------------------------------
- Branch by ZIP. The spec says ZIP resolved to county beats the source label, but
  Partner_Branch and Billing_Branch are user-selected. The territory resolver is
  already on the deferred list. Until it exists, branch accuracy depends on entry.
- Diversion. Diversion_Tracking is a provider Yes/No that the spec calls
  unreliable, with the note governing. No report can apply that. It stays a QC
  read for now.
- Service type list alignment. Type_of_Procedures carries 15 choices against the
  spec's locked 17. The two lists need reconciling before the service-type mix
  metric is trustworthy. Procedures_Performed inherits the same list, so
  reconciling once fixes both.
- Historical months. Creator holds data from the imports forward. Any month
  before the imported range still comes from Cognito.

--------------------------------------------------------------------------------
## 8. Dependency: August 2026 Cognito import
--------------------------------------------------------------------------------
This scope assumes August referral and PVS data is in Creator. Follow
context/09_cognito_import_procedure.md, in particular:

- Verify EVERY column mapping by hand. Creator auto-map silently mis-assigns
  columns (section 5A-a).
- Never map into a lookup. Import branch as plain text into Partner_Branch, then
  resolve with resolve_referral_branch_from_text.
- Set the wizard Date Format to year-month-day when the file uses yyyy-MM-dd.
- Watch the created-count. "Skip corresponding row" silently drops whole rows.
- Run the post-import backfills in order, then spot-check 3 to 5 records.
- Any imported Referral_Link on the PVS must be followed by
  backfill_pvs_from_referral, because On User Input workflows never fire on
  import.
- Partner_Location_Label is now the plain location name. Any file using the old
  "Partner - CODE" format must be rewritten first.

--------------------------------------------------------------------------------
## 9. Open decisions
--------------------------------------------------------------------------------
1. Reconcile Type_of_Procedures (15) against the spec's locked service type list
   (17). Which list wins, and does Type_of_Procedures get renamed choices?
2. Does the August import need a Cognito_Referral_ID column so re-imports can key
   on it rather than adding duplicate rows?
3. Should MPU_Master exclude Clinical_Note_Type = Preliminary, or include it with
   a flag?

--------------------------------------------------------------------------------
## 10. Sequence
--------------------------------------------------------------------------------
1. August Cognito import (referrals, then PVS) with backfills and spot-check.
2. Add the five fields in section 3.
3. Update the referral pre-fill; build and run backfill_pvs_referral_date.
4. Build the four reports in section 5.
5. Dry-run the QC pass against August and compare the output to the July
   spreadsheet.
6. Reconcile the service type lists.

END
