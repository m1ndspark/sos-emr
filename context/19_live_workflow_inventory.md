# SOS EMR Live Workflow Inventory

Purpose: the authoritative record of what is actually live in the Creator app,
captured from on-screen state (Workflow tab, Form workflows). The .ds export gives
structural definitions; this file gives live binding, enable/disable state, and event
scope (Created vs Created or Edited). On any conflict about live state, this file wins.

Source: live screenshots from Neil, captured 7/19/2026, reconciled against the 7/17
.ds. Dates shown are Created On in MM-DD-YYYY.

--------------------------------------------------------------------------------
## Encounter_PatientVisit (PVS) - Form workflows
--------------------------------------------------------------------------------
All 11 visible workflows below are on Encounter_PatientVisit.

| Display name | Event | Status | Created |
| --- | --- | --- | --- |
| Pre-fills provider section from employee record | Created, Load of the form | Enabled | 05-08-2026 |
| Additional Charges Show Hide | Created, User input of Additional Charges | Enabled | 05-08-2026 |
| Diversion Type Show Hide | Created, User input of Did this visit result in a Diversion? | Enabled | 05-08-2026 |
| Patient Fields Editability Toggle | Created, User input of Do you have a Referral ID? | DISABLED | 05-08-2026 |
| Referral Link Pre-Fill | Created, User input of Referral Link | Enabled | 07-09-2026 |
| Entry Type Section Visibility | Created, User input of Type of Entry | Enabled | 05-08-2026 |
| PVS ID Stamp Generator | Created, Successful form submission | Enabled | 05-08-2026 |
| Default Hide On Load | Created or Edited, Load of the form | Enabled | 07-10-2026 |
| Has Referral_ID Show_Hide | Created or Edited, User input of Do you have a Referral ID? | Enabled | 07-10-2026 |
| Edit_Needed Unlock | Created or Edited, User input of Edit Needed | Enabled | 07-10-2026 |
| Provider ICD Print Builder | Created or Edited, User input of ICD-10 Codes Lookup | Enabled | 07-13-2026 |

Event scope notes:
- "Created" fires only on new-record entry. "Created or Edited" fires on both.
- Provider pre-fill is Created only (on add), matching the .ds. It does not re-run on
  edit.
- PVS ID Stamp Generator runs on successful submission of a new record only.

--------------------------------------------------------------------------------
## Reconciliation against the .ds punch list (context/16)
--------------------------------------------------------------------------------
- Patient Fields Editability Toggle is DISABLED live. This corrects context/16, which
  read it as still live and double-handling Has_Referral_ID. Because it is off, there
  is no live double-handling with "Has Referral_ID Show_Hide" (Enabled). Deleting the
  disabled legacy workflow is now optional tidiness, not a live-bug fix.
- Two handlers still exist on the same event (User input of Do you have a Referral ID?):
  the disabled legacy toggle and the enabled Has Referral_ID Show_Hide. Only the
  enabled one is active.

--------------------------------------------------------------------------------
## Pending capture (not yet inventoried)
--------------------------------------------------------------------------------
These need screenshots to complete the live picture:
- Form workflows for the other forms: Referrals_Main, Partner_Rates, Partners
  (confirm the suspected stray "Partner Rate Stamp Generator" bound here), Partner_
  Contracts, Partner_Billing_Contacts, Partner_Locations, Employees, Assignments,
  Encounters_PVSAddendum, and any others in the form list.
- The other Workflow tabs: Schedules, Approvals, Payments, Blueprints, Batch workflows,
  and Functions (standalone functions such as send_via_sendgrid, run_schema_monitor,
  and the mint_/backfill_ set).

--------------------------------------------------------------------------------
## Session update 7/20 to 7/21 (PVS build) - live and mirrored to repo .dg
--------------------------------------------------------------------------------
Changes verified live and written to Encounter_PatientVisit/*.dg:

- OnLoad__Provider_PreFill.dg: now also builds Employee_Full_Name (First Last) and
  Employee_Name_Title (First Last, Title) from the pulled name parts.
- OnUserInput__Patient_Location__Facility_Show_Hide.dg: NEW. Shows the facility fields
  only when Patient_Location is Facility. Paired with Default Hide (default hidden) and
  the referral pull (reveal on pull).
- OnUserInput__Type_of_Entry__Section_Visibility.dg: full 5-type build (Patient Visit,
  3008, Lab Order, X-Ray Order, Clinic Hours) plus else. Manages Referral_Details_
  Section (clinical context) per type and the new Imaging_Orders_Section (shown only on
  X-Ray Order). 3008 shows only Cares 3008 Completion, no charges (flat-rate).
- OnUserInput__Referral_Link__PreFill.dg: now also pulls the clinical context
  (Reason_for_Referral from referral Referral_Reason; Goals_of_Care, List_Patient_
  Allergies, List_Patient_Anticoagulants, Advanced_Directives_Details, Additional_
  Information same-named), disables them on a referral, clears and enables on a walk-in.
- OnLoad__Default_Hide_On_Load.dg: hides Imaging_Orders_Section; shows Employee_Name_
  Title and hides the granular employee fields; locks the six clinical fields plus
  Partner_ICD_Codes when Has_Referral_ID is Yes.

Schema changes this session (per monitor):
- Added on PVS: Billing_Branch (Lookup to Partner_Locations, display Partner_Location_
  Name, hidden in System_Fields_Section, not provider-facing), Employee_Name_Title, and
  the new Imaging_Orders_Section with Imaging_Orders, Imaging_Order_Indication,
  Upload_Imaging_Order_Files, Imaging_Ordered_Date.
- Deleted sections: X_Ray_Section, Lab_Section, old Imaging_Order_Section (Creator
  stripped their workflow references automatically).
- Section renames: old Referral_Details_Section (top) is now Referral_Lookup_Section;
  old Referral_Details_Section1 (clinical context) is now Referral_Details_Section.

Still live but now cleanup candidates: empty Visit_XRay_Section, orphaned
XRay_Ordered_This_Visit field.

--------------------------------------------------------------------------------
## Session 20 continuation 7/21 (walk-in gating + display name) - live and in repo
--------------------------------------------------------------------------------
- OnUserInput__Patient_Last_Name__Build_Display_Name.dg: NEW. Builds Patient_Display_
  Name from First + MI + Last on a walk-in (fires on user input of Patient_Last_Name).
- OnUserInput__Referral_Link__PreFill.dg: also sets Patient_Display_Name from the
  pulled Patient_Full_Name on a referral, and clears it when the referral is removed.
- OnUserInput__Has_Referral_ID__Show_Hide.dg: on No, locks Type_of_Entry to "Patient
  Visit" and reveals the Patient Visit sections (Entry Type Visibility does not fire on
  a programmatic set, so the walk-in branch carries its own copy of that section list);
  hides the seven referral-context fields (Partner_ICD_Codes, Goals_of_Care,
  Additional_Information, General_Files_Upload, List_Patient_Allergies, List_Patient_
  Anticoagulants, Advanced_Directives_Details). On Yes, enables Type_of_Entry and shows
  those seven.
- OnLoad__Default_Hide_On_Load.dg: disables Type_of_Entry on load when Has_Referral_ID
  is No, so a reopened walk-in stays locked to Patient Visit.

Design notes:
- Patient_Display_Name is a plain field (not a formula) so a workflow can write to it.
  Used to show the patient name in more than one section.
- Reason_for_Referral and Primary_Diagnosis are Patient Visit fields (in Referral_
  Details_Section). Order types carry their own reason (Imaging_Order_Indication,
  Lab_Order_Indication). They follow the section, no separate handling.
- Coupling to watch: if the Patient Visit section list changes, update it in BOTH
  Entry Type Section Visibility and the walk-in branch of Has Referral_ID Show_Hide.

Schema deltas this stretch (per monitor):
- Added: Patient_Display_Name.
- Removed: Patient_Full_Name1 (duplicate), XRay_Ordered_This_Visit (orphan),
  Visit_XRay_Section fields, and the old Lab_Section leftovers (Reason_for_Lab_Request,
  Requested_Lab_Vendor1, Upload_Lab_Request_Files).

Open: the Referral_Partner_Section question Neil flagged is still unraised.

--------------------------------------------------------------------------------
## Session 20 EOD 7/21 - finalize-lock, renames, Referrals_Main generators
--------------------------------------------------------------------------------
Verified against the 7/21 19:31 .ds export.

PVS (Encounter_PatientVisit):
- OnLoad__Invoice_Status_Lock.dg: NEW. Event Created or Edited, Load of the form.
  Locks the medical record when Clinical_Note_Type == "Final"; the nine charge fields
  stay editable. A nested check also locks charges once Invoice_Status == "Final"
  (that value is written later by the invoice flow; nothing sets it today).
  Clinical_Note_Type itself is NOT disabled, so Final can be changed to Addendum.
- Lock timing: on load, not on submit. Choosing Final does not lock the open form; the
  record is locked the next time it opens. Accepted for launch.

Schema renames applied live (both workflows updated to match):
- Section Lab_Order_Section is now Lab_Orders_Section.
- Type_of_Entry option "X-Ray Order" is now "Imaging Order".

Referrals_Main:
- OnUserInput__Patient_Address__Build_Full_Address.dg: NEW. Concatenates the address
  subfields into the new plain text field Patient_Full_Address (line1, line2, city,
  state, zip; country omitted).
- OnUserInput__DM_Last_Name__Build_DM_Full_Name.dg: NEW. Builds DM_Full_Name from
  DM_First_Name + DM_Last_Name.
- OnLoad__Default_Hide_On_Load.dg: NEW. Hides Patient_Full_Address on the form.

DEBUGGING NOTE (cost about an hour):
A duplicate Invoice_Status_Lock workflow existed from an earlier create/delete cycle.
The visible copy showed Disabled while the second copy stayed enabled, so the entire
PVS rendered read-only on new records and toggling the visible one changed nothing.
Lesson: when a workflow behaves as though it is running while showing Disabled, scan
the full list for a duplicate name before investigating field properties or
permissions. Deleting outright is safer than disabling when rebuilding.

OTHER DELUGE RULES CONFIRMED LIVE:
- hide/show/enable/disable are valid ONLY in on-load actions. They throw "can be used
  only in on load actions" in on-validate or on-success workflows.
- Formula fields compute on save, not live during entry, and cannot be written by a
  workflow. Use a plain field plus a workflow when a value must appear live.

Still open: DM_Full_Name backfill for existing referrals; Patient_Full_Address
backfill; the two legacy cleanups; the July import path.

--------------------------------------------------------------------------------
END
--------------------------------------------------------------------------------
