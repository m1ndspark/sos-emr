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
## Added in the 2026-07-29 Creator drift sync (source .ds SOS_Referrals_App_2026-07-29.ds)
--------------------------------------------------------------------------------
New standalone functions (functions/):
- create_invoice_from_selection(list p_pvsIds) - invoice engine entry
- run_invoice_batch(int p_batchId) - processes a staged Invoice_Batch record
- create_books_customers() - upserts Zoho Books customers
- diag_invoice_batch(int p_batchId) - diagnostic
- link_pvs_to_referral() - backfill/repair PVS to referral links
- backfill_pvs_billing_branch()
- backfill_pvs_employee_initials()
- backfill_referral_branch()
- backfill_referral_branch_from_contact()
- diag_referral_contact_match() - diagnostic

New workflows:
- Encounter_PatientVisit / OnUserInput Referral_Link / Referral_Sets_Billing_Branch
    sets Billing_Branch, Partner_Branch, Partner_Organization from the referral
- Encounter_PatientVisit / OnUserInput Complexity_Level / Complexity_Sets_Charge
- Encounter_PatientVisit / OnUserInput Billing_Branch / Branch_Sets_Charge
- Encounter_PatientVisit / OnValidate / Billing_Branch_Required
- Referrals_Main / OnUserInput Partner_Branch_Link / Branch_Sets_Partner
- Referrals_Main / OnUserInput Partner_POC_Email / Sender_Sets_Branch
- Referrals_Main / OnUserInput Partner_POC_Email / Partner_Contact_Lookup
- Referrals_Main / OnSuccess / Branch_Sets_Partner_Link  [DISABLED in Creator;
    UI confirmed by Neil 2026-09-10. Committed for the record. Do not treat as
    live. Evidence corrected: this was originally called from the .ds status
    flag, which is not reliable - see the status-flag section below. The verdict
    survived the re-check; the reasoning did not.]
- Invoice_Batch / OnLoad / Invoice_Batch_On_Load_Disable
- Invoice_Batch / OnSuccess / Invoice_Batch_On_Create
- Assignments / OnLoad / Show_Hide_Facility_Name_P
- Assignments / OnUserInput Patient_Location / Show_Hide_Facility_Name_P1
- Assignments / OnUserInput Referral_Link / Assignment_Pull_From_Refe
- Employees / OnSuccess / Portal_Access_By_Status
- Employees / OnUserInput Employee_Status / Show_Hide_Employee_Term_D
- Imaging_Orders / OnLoad / Default_Hide_On_Load

Note: the whole existing set of tracked workflow and function .dg files was also
reconciled to this .ds in the same sync (thisapp. call prefixes, Creator export
formatting, standalone functions stored body-only, plus real logic updates to the
PVS billing-branch show/hide workflows and the Employee phone formatter).

--------------------------------------------------------------------------------
## Session 31 2026-08-12 - Referrals_Main referral pipeline consolidation
--------------------------------------------------------------------------------
Live state of the Referrals_Main form workflows after collapsing the referral
intake pipeline into a single On Success master. Supersedes the piecemeal
generators previously bound to this form.

ADDED:
- Referrals Main On Create - Master (Created / On Success). One script running
  the whole post-insert pipeline in order:
  - mints the referral ID and stamps Referral_Date = current date
  - formats the four phone fields and the SSN
  - builds Patient_Full_Address, AC_Full_Name, Patient_Full_Name, and
    Partner_POC_Name_Title
  - resolves Partner_Location_Label against Active Partner_Locations by name,
    then writes Partner_Organization, Partner_Branch, Partner_Location_Label,
    Partner_Link, Partner_Branch_Link, Partner_ID, and Partner_ID_Stamp
  - runs the contact upsert, including Partner_Link and Partner_Locations_Link
  Consolidated here because integration-inserted records fire On Success but
  never On User Input (see context/05), so any generator built as On User Input
  silently skipped every form-submitted referral.

REMOVED (deleted, absorbed into the master):
- REF ID Generator
- Partner Contact Upsert

CHANGED (record event narrowed from "on add or edit" to "on edit"):
- Patient Full Name Generator
- Partner POC Name & Title Generator
  The On Create path for both now lives in the master; these remain only to
  recompute on a manual edit.

--------------------------------------------------------------------------------
## Session 38 EOD 2026-09-01 - new diagnostic function
--------------------------------------------------------------------------------

NEW standalone function (functions/):

- `diag_form_fields(string p_formLink)` - Deluge, default namespace, returns
  string.

  Behaviour:
  - Called with a **blank** argument, it lists every form in the app.
  - Called with a **form link name**, it dumps every field on that form: link
    name, display name, type, mandatory, unique and detail, plus a total field
    count at the end.

  Uses the `sos_schema_monitor` connection and the same type map as
  `run_schema_monitor`, so its type labels read identically to the generated
  `schema/*.md` files.

  Why it exists: `run_schema_monitor` only reports **changes**. There was no way
  to ask the live app what a form holds right now without waiting for a delta or
  reading a capture that might predate the field you are asking about.
  `diag_form_fields` answers that directly, on demand.

  Written against `Referrals_Main`, which is where the need surfaced: the
  Session 38 integration rebuild introduced a Patient MBI field that postdates
  the 2026-08-31 06:01 schema capture, so its link name could not be confirmed
  from `schema/Referrals_Main.md`. See context/24 section 10.

  It is a `diag_*` function and therefore falls under the existing post-launch
  cleanup row in context/23: delete every `diag_*` function from Creator after
  launch.

--------------------------------------------------------------------------------
## The .ds status flag is NOT reliable (added 2026-09-10, Session 43)
--------------------------------------------------------------------------------
The `status = inactive` line in a .ds workflow block does not reliably reflect
whether a workflow is on. Only the Creator UI can be trusted for enable state.

Evidence: v44 records `status = inactive` on the Encounter_PatientVisit copy of
**Build Patient Full Address**. Neil confirmed in the Creator UI that the same
workflow shows **Enabled**. The export and the UI disagree, and the UI is right.

Rule: never conclude a workflow is off from the .ds alone. If enable state
matters to a decision, it must be read off the Workflow tab and recorded in this
file. That is what this file is for, and why it wins on any live-state conflict.

The absence of a status line means nothing either. Most live blocks carry no
status line at all, so "no flag" is not evidence of Enabled any more than
`inactive` is evidence of Disabled.

This forced a re-check of the existing note in this file on
`Referrals_Main / OnSuccess / Branch_Sets_Partner_Link`, which read INACTIVE on
the strength of "status = inactive" in the export - the same unsound evidence.
RESOLVED 2026-09-10: Neil checked the Creator UI and confirmed the workflow is
toggled off. The verdict stands; its evidence has been replaced with the UI
confirmation. Right answer, wrong reason, now corrected.

Corroborating symptom, independent of either source: form-submitted referrals
land with Partner_Link and Partner_ID empty, because nothing is setting them on
success. REF-1458 read back as PartnerLink=- and PartnerID= until
`backfill_referral_partner_fields` was run against it. A disabled
Branch_Sets_Partner_Link predicts exactly that failure, which is stronger
evidence than any flag in the export.

The lesson generalizes: when the export and the UI disagree, do not assume the
export's verdict is wrong - assume its evidence is worthless and go re-derive
the answer. Here the conclusion happened to hold. Next time it may not.

Trap: display names are not unique across forms. v44 carries two workflows both
named "Build Patient Full Address" - one on Encounter_PatientVisit (the one
carrying the false `inactive` flag) and one on Referrals_Main. Always resolve a
workflow by form plus trigger, never by display name alone.

--------------------------------------------------------------------------------
## Known drift: v44 was behind live - RESOLVED 2026-09-11 in v45
--------------------------------------------------------------------------------
CLOSED. v45 was exported 2026-09-11 and both items below landed in it exactly as
predicted. Both are now synced into the repo. No hand-writing was ever done and
none was needed.

DRIFT A arrived as functions/backfill_mint_missing_referral_ids.dg.
DRIFT B arrived as the two input.Referral_Date lines in
Encounter_PatientVisit/OnUserInput__Referral_Link__PreFill.dg, in the exact
positions recorded below: after the Referral_ID_Stamp assignment, and in the
clear branch. The Session 43 prediction was correct line for line.

The record below is kept as written, because a prediction that held is worth
more as evidence than a tidied-up summary.

ORIGINAL ENTRY, 2026-09-10:
Two items are live and absent from v44. Both land in v45. Neither is a defect,
and neither may be hand-written into the repo or synced before v45 exists.

DRIFT A: standalone function `backfill_mint_missing_referral_ids`.
Built and run live on 2026-09-10, after v44 was exported, so it appears nowhere
in the export and has no `.dg` file yet. Run history:

    PREVIEW | scope=ALL | scanned=20 | to mint=20 | already had an ID=0
            | REF sequence starts at 1444
    COMMIT  | minted REF-1444 through REF-1463

Confirmed live afterward: `diag_referral_intake("4904890000000561003")` returned
REF=REF-1463. Extract it into `functions/` on the v45 sync, not before. Until
then `ds_sync` cannot see it and its absence from MANIFEST.tsv is expected.

This also settles the Session 43 count dispute: v44 contains FOUR new functions,
not five. The fifth exists, but it postdates the export.

DRIFT B: workflow **Referral Link Pre-Fill**, Encounter_PatientVisit, on user
input of Referral_Link.

Live contains two lines that v44 does NOT have. Neil verified them live.

After the `input.Referral_ID_Stamp = v_Rec.Referral_ID_Stamp;` assignment:

    input.Referral_Date = v_Rec.Referral_Date;

And in the clear branch:

    input.Referral_Date = null;

Confirmed absent from v44: the Referral_ID_Stamp assignment is present in the
export with no Referral_Date assignment following it, and the only two
`input.Referral_Date` occurrences anywhere in v44 belong to
`Assignment_Pull_From_Referral` on the **Assignments** form, which is a different
workflow using `refRec` and assigning `""` rather than `null`.

This is expected drift, not a defect. It will appear in v45. Do NOT "fix" the
repo copy by hand and do NOT let a sync tool write it - `ds_sync.py` compares
against the export, so until v45 lands the export is the stale side and a sync
would look correct while being wrong.

--------------------------------------------------------------------------------
## Known drift: v45 was behind live - RESOLVED 2026-09-12 in v47
--------------------------------------------------------------------------------
CLOSED. v47 was exported 2026-09-12 and both items below landed in it. Both are
now in the repo and verified against the export.

DRIFT A landed. Encounter_PatientVisit/OnValidate__PVS_Required_Fields.dg is
132 lines with exactly one cancel submit, one Patient Visit block, no duplicated
tail, and no Facility_Room_Number check. Matches the live body recorded below.

DRIFT B landed, but NOT automatically, and the reason matters for every future
sync. ds_sync reported PVS_Patient_Data_Push_Bac as AMBIGUOUS, colliding onto
OnSuccess__PVS_Stamp_Generator.dg. Root cause is in tools/ds_sync.py
resolve_wf_path: when a form folder holds exactly ONE file for a trigger type,
the resolver returns it for ANY workflow of that type without scoring the name.
PVS Patient Data Push Back is the second On Success workflow on
Encounter_PatientVisit, so it and PVS_ID_Stamp_Generator both resolved to the
single existing file, and the collision guard refused to write either.
The guard worked. Had it not, the push back body would have overwritten the PVS
ID stamp generator.
Resolved by extracting the body with ds_sync's own parse_workflows into
Encounter_PatientVisit/OnSuccess__PVS_Patient_Data_Push_Back.dg, not by hand.
With a second On Success file present the resolver falls through to name
scoring, and a re-run reports BOTH files as MATCH independently, which proves the
extracted file is byte-equivalent to the export and that the stamp generator was
never touched.
EXPECT THIS AGAIN on the next form that gains a second workflow of an existing
trigger type. It fails safe (AMBIGUOUS, nothing written), so the cost is a
manual extraction, not a clobbered file.

The record below is kept as written.

ORIGINAL ENTRY, 2026-09-11:
Two Creator artifacts changed on 2026-09-11 AFTER v45 was exported. Neither is
in any export and neither is in this repo. DO NOT HAND WRITE EITHER ONE. They
arrive on the next .ds and are extracted by ds_sync then, not before.

DRIFT A: Encounter_PatientVisit / OnValidate / PVS_Required_Fields, corrected.
The live body is now 132 lines. The repo copy is 177 lines and still carries the
byte-identical duplicated tail that was flagged in the v45 sync audit: live
lines 133 to 177 were a copy of 88 to 132 and have been deleted in Creator.
Until the next export, the repo copy is KNOWN WRONG in a specific, recorded way.
It is not a new defect and must not be "fixed" by editing the .dg.

DRIFT B: Encounter_PatientVisit / On Success / PVS Patient Data Push Back. NEW
workflow, no repo file yet.
On a referral-linked PVS, DOB, phone and address stay editable by the provider,
and on success the edited values are written back to Referrals_Main so the one
true source stays true.
This closes the loop opened by the v45 prefill unlock. The v45 sync audit raised
exactly this as a VERIFY LIVE item: three workflows had dropped their disable
lines on Patient_DOB, Patient_Address and Patient_Phone, which let a PVS diverge
silently from Referrals_Main. The push back is the answer to that divergence.
The audit question is therefore resolved, and the resolution is a workflow the
repo cannot see yet.

Watch on the next sync: Patient_Phone is type phonenumber on the PVS and plain
text on Referrals_Main, so the push back has to convert. See context/05.

Both are filed in context/23 under the fresh .ds export, which is BLOCKING.

--------------------------------------------------------------------------------
## Known drift: v47 is behind live (added 2026-09-12)
--------------------------------------------------------------------------------
One Creator artifact changed on 2026-09-12 AFTER v47 was exported. It is not in
any export. DO NOT HAND WRITE IT. It arrives on the next .ds and is extracted
then.

DRIFT: Encounter_PatientVisit / On Success / PVS Patient Data Push Back
(link name PVS_Patient_Data_Push_Bac), corrected for address erasure.

The v47 body writes all five Patient_Address subfields to Referrals_Main
unconditionally whenever any one of them changed, while its change detection
ignores blank PVS subfields. A PVS with a new address_line_1 and a blank
district_city therefore wrote a blank city over the real one. Flagged in the v47
sync audit.

Live fix: a blank PVS subfield now preserves the Referrals_Main value instead of
overwriting it.

Until the next export, Encounter_PatientVisit/OnSuccess__PVS_Patient_Data_Push_Back.dg
in the repo is KNOWN to be the pre-fix body. That is recorded, not a new defect.

Watch on the next sync: this file needed manual extraction in v47 because
ds_sync's resolver collided it with OnSuccess__PVS_Stamp_Generator.dg. Both
files now exist, so the resolver should score the names and report a plain
DRIFT this time. If it reports AMBIGUOUS again, extract with parse_workflows as
before rather than by hand.

--------------------------------------------------------------------------------
END
--------------------------------------------------------------------------------
