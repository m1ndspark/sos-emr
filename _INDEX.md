# SOS EMR Code Archive - Master Index

Last updated: July 13, 2026 (Session 15)
Source of truth: the live Zoho Creator app. This archive mirrors it.
Sync method: manual. When a workflow is verified working in Creator, paste the
exact Deluge into its .dg file and update the EXTRACTION and VERIFIED columns.

Rule: .dg files hold pure Deluge only, no comment headers, so they round-trip
cleanly back into Creator. All status and metadata live here, not in code files.

Session 4 status legend (Partner Cluster ID work, 2026-06-27):
  PROVEN   = ran clean live in this Creator instance
  BUILT    = compiles, live test pending
  ADDITIVE = built, NOT wired into a live trigger yet
  PENDING  = do not make live yet (gated on a prior step)
Extraction note: the Session 4 entries below were extracted 2026-06-27 from the
live Creator build (Session 4 export). The per-docs status (PROVEN / BUILT /
ADDITIVE / PENDING) reflects live-test state, not extraction state.

--------------------------------------------------------------------------------
EXTRACTION CHECKLIST
--------------------------------------------------------------------------------
Status per docs = what the May 8, 2026 session log claims.
Extraction = whether the live Deluge has been pulled into this archive yet.
Verified-in-Creator = confirmed the archived copy matches what is live.

FORM: Encounter_PatientVisit   [form name PENDING confirmation, see NOTE 1]
  Encounter_PatientVisit/OnLoad__Provider_PreFill.dg
    trigger: On Load        | per docs: LIVE | extraction: DONE 2026-07-14 | verified: YES
      NOTE: live name "Pre-fills provider section from ...". Reads Employees[Employee_Email == zoho.loginuserid], pulls Employee First/Last/Title/Initials onto the PVS. Extracted from the live Application IDE .ds export 2026-07-14 (authoritative live dump).
  Encounter_PatientVisit/OnLoad__Default_Hide_On_Load.dg
    trigger: On Load (Created or Edited) | per docs: DEPLOYED + TESTED LIVE 2026-07-10 (updated 2026-07-12) | extraction: DONE | verified: YES
      NOTE: live workflow name "Default Hide On Load". Includes hide Edit_Needed. Replaced the old "Referral Fields Default Hide" (now DISABLED live). UPDATE 2026-07-12: PVS_Referral_ID relocated into System_Fields_Section; workflow now hides System_Fields_Section on load and disables PVS_Referral_ID (was a field-level hide PVS_Referral_ID). UPDATE 2026-07-12 (b87f047): patient identity disables are now conditional - if(Has_Referral_ID == "Yes") disable First/MI/Last/DOB/Gender/Address, else enable them (+ Phone/Email/Hospice/SSN/Facility) so the walk-in path loads editable. NOTE: this turned out to be a red herring for the walk-in greying bug; the real fix was the Edit_Needed Unlock guard. The change is correct and harmless, kept.
  Encounter_PatientVisit/OnUserInput__Has_Referral_ID__Show_Hide.dg
    trigger: On User Input (Created or Edited) | per docs: DEPLOYED + TESTED LIVE 2026-07-10 (updated 2026-07-12) | extraction: DONE | verified: YES
      NOTE: live name "Has Referral_ID Show_Hide". Option B - Yes shows Referral_Link only (no lock); No wipes all + unlocks + hides Edit_Needed. DONE 2026-07-12: all show/hide PVS_Referral_ID lines removed (all 3 branches); PVS_Referral_ID relocated to System_Fields_Section and hidden + disabled via Default Hide On Load. Supersedes the earlier one-line hide plan.
  Encounter_PatientVisit/OnUserInput__Referral_Link__PreFill.dg
    trigger: On User Input | per docs: DEPLOYED + TESTED LIVE 2026-07-10 (updated 2026-07-14) | extraction: DONE | verified: YES
      NOTE: live name "Referral Link Pre-Fill" (07-09). Conditional lock (Option B) on a real match (v_Found) + wipe-on-deselect + shows Edit_Needed=No + Full_Name/split-name swap. Pull maps referral fields by matching link names (PVS partner fields renamed Partner_* to match Referrals_Main). UPDATE 2026-07-14 (item 2): added Partner_ICD_Codes to the pull (populate loop), the found-lock block (disable), and the else branch (null + enable). Both Referrals_Main.Partner_ICD_Codes and PVS Partner_ICD_Codes are Single Line - no type mismatch. Session 15 "didn't work" cause was simply that the pull line was absent. VERIFIED LIVE 2026-07-14: REF-1028 (Partner ICD "E.22, A.22, G.07") pulled into the PVS and locked read-only. NOTE: most existing referrals have Partner_ICD_Codes blank (Dx codes dropped from Cognito import); nothing yet WRITES partner ICD onto referrals - upstream capture is a separate future piece. UPDATE 2026-07-14 (Session 16): removed `hide System_Fields_Section;` from the if(v_Found) block to match live (repo was ahead; redundant no-op, Default Hide On Load already hides that section). Repo + live now agree.
  Encounter_PatientVisit/OnUserInput__Edit_Needed__Unlock.dg
    trigger: On User Input (Created or Edited) | per docs: DEPLOYED + TESTED LIVE 2026-07-10 (updated 2026-07-12) | extraction: DONE | verified: YES
      NOTE: live name "Edit_Needed Unlock". Edit_Needed=Yes unlocks all prepopulated fields (except System Fields section) + swaps Full_Name for split names; No re-locks. Requires Radio field Edit_Needed (No/Yes) - LIVE. FIX 2026-07-12: entire body now wrapped in if(input.Has_Referral_ID == "Yes"). ROOT CAUSE of a walk-in greying bug: the Has Referral_ID Show_Hide No branch sets input.Edit_Needed = null, which triggers this On-User-Input workflow; its old else (null != "Yes") disabled the patient fields right after Has Referral_ID Show_Hide had enabled them, so clicking No greyed the split name/DOB/etc fields. The guard makes it no-op on walk-ins. Verified live.
      *** DEPLOY GOTCHA (2026-07-10): the OLD workflows "Referral Fields Default Hide" AND "Patient Fields Editability Toggle" must be DISABLED. While enabled they fired alongside the new set and hid Edit_Needed on referral select. Both now DISABLED live (not deleted - delete in a cleanup pass so they cannot be re-enabled). Full 5-step cycle verified: select->lock+Full_Name+Edit_Needed; Edit_Needed=Yes unlock+split names; No relock; deselect clears; Has_Referral_ID=No clears+manual entry. ***
  Encounter_PatientVisit/OnUserInput__Type_of_Entry__Section_Visibility.dg
    trigger: On User Input (Type_of_Entry) | per docs: LIVE + ENABLED | extraction: DONE 2026-07-14 | verified: YES
      NOTE: live name "Entry Type Section Visibility". Show/hide of PVS sections by Type_of_Entry
      (Patient Visit / 3008 / Lab Order / X-Ray Order / Clinic Hours, + else-hide-all fallback).
      Extracted live 2026-07-14. CORRECTS the prior (2026-07-09) "DOES NOT EXIST" note, which was
      wrong - Session 14 workflow inventory already flagged it as live/enabled.
  Encounter_PatientVisit/OnUserInput__Diversion_Tracking__Show_Hide.dg
    trigger: On User Input (Diversion_Tracking) | per docs: LIVE | extraction: DONE 2026-07-14 | verified: YES
      NOTE: live name "Diversion Type Show Hide". Diversion_Tracking=="Yes" shows Type_of_Diversion, else hides. Extracted from live .ds export 2026-07-14.
  Encounter_PatientVisit/OnUserInput__Additional_Charges__Show_Hide.dg
    trigger: On User Input (Additional_Charges) | per docs: LIVE | extraction: DONE 2026-07-14 | verified: YES
      NOTE: live name "Additional Charges Show Hide". Checkbox contains("Equipment Charge") shows Equipment amount/details; contains("Other") shows Other amount/details; else hide. Extracted from live .ds export 2026-07-14.
  Encounter_PatientVisit/OnSuccess__PVS_Stamp_Generator.dg
    trigger: On Success     | per docs: DEPLOYED + TESTED LIVE 2026-07-14 (re-fixed) | extraction: DONE 2026-07-14 | verified: YES
      NOTE: live name "PVS ID Stamp Generator". Mints PVS_ID from the shared "PVS" Sequence_Tracker row (referral = PVS-<seq>-<init>; walk-in = PVS-<seq>-<init>-M) and stamps PVS_Referral_ID = "PVS-"+Referral_ID on the referral path only.
      FIX 2026-07-14 (corrected): the precedence bug (&& binds tighter than ||) was real, but the paren fix DID NOT HOLD. CREATOR QUIRK: a compound if with a parenthesized ||-subgroup, e.g. if(A && B && (C || D)), SILENTLY REVERTS ON SAVE back to the un-parenthesized form. The morning "it saved / tests passed" was a false pass: the ds export (12:53) proved live still had NO parens, and both happy-path tests passed only because a fresh record's PVS_Referral_ID is null (which the buggy precedence handles correctly on both paths). REAL FIX: split into NESTED ifs (no paren grouping): outer if(Has_Referral_ID=="Yes" && Referral_ID present), inner if(PVS_Referral_ID == null || == ""). Verified live on an EDIT/RE-SUBMIT (the case the happy-path test missed): referral PVS-1004 kept PVS-REF-070226-1243 unchanged; walk-in PVS-1002-JK-M stayed blank. PVS Sequence_Tracker row live + incrementing. No-duplicate on PVS_ID SET 2026-07-14.
      LESSON: verify a fix persisted by REOPENING the saved workflow (Creator can silently drop constructs it won't accept), and test the edit/re-submit path, not just fresh creates.

FORM: Referrals_Main   [live form has 5 On-User-Input formatters; see NOTE 6]
  Referrals_Main/OnSuccess__REF_ID_Generator.dg
    trigger: On Success (Created) | per docs: PROVEN (LIVE; retrofit complete 2026-06-27, body now calls mint_referral_id(input.ID), supersedes old inline) | extraction: DONE 2026-06-27 | verified: YES (matches Session 4 export)
  Referrals_Main/OnSuccess__Patient_Full_Name_Generator.dg
    trigger: On Success (Created or Edited) | per docs: PROVEN (LIVE; enabled in Creator "Created or Edited -> Successful form submission"; concat First+MI+Last -> Patient_Full_Name, blank-aware) | extraction: DONE 2026-06-27 | verified: YES
    note (2026-07-03): 4 link names CONFIRMED against the Zoho Form -> Referrals_Main field mapping (Patient_First_Name, Patient_MI, Patient_Last_Name, Patient_Full_Name). .PENDING dropped. Confirmed live that an On-Success ("Successful form submission") stage DOES persist an input.<field> assignment in this Creator instance. DOES NOT fire on CSV/API import -> July backfill still needed (missing-only, require-last-name; see Session 7 block).
  Referrals_Main/OnSuccess__Partner_POC_Name_Title_Generator.dg
    trigger: On Success (Created or Edited) | per docs: BUILT (concat Partner_POC First+Last+Title -> Partner_POC_Name_Title for display on other forms/reports) | extraction: DONE 2026-06-29 | verified: YES (matches Session 5 export)
  Referrals_Main/OnUserInput__Decision_Maker_Phone__Format.dg
    trigger: On User Input  | per docs: WORKING (live) | extraction: DONE 2026-06-25 | verified: YES (copied from live)
  Referrals_Main/OnUserInput__Patient_SSN__Format.dg
    trigger: On User Input  | per docs: WORKING (live) | extraction: DONE 2026-06-25 | verified: YES (copied from live)
  Referrals_Main/OnUserInput__Patient_Phone__Format.dg
    trigger: On User Input  | per docs: WORKING (live; prior BLOCKED note resolved, formatter strips to digits + last 10) | extraction: DONE 2026-06-25 | verified: YES (copied from live)
  Referrals_Main/OnUserInput__Facility_Phone__Format.dg
    trigger: On User Input  | per docs: WORKING (live) | extraction: DONE 2026-06-25 | verified: YES (copied from live)
  Referrals_Main/OnUserInput__Partner_POC_Phone__Format.dg
    trigger: On User Input  | per docs: WORKING (live, aka "Referral Partner POC Phone Format") | extraction: DONE 2026-06-25 | verified: YES (copied from live)

FORM: Partners   [Session 4, 2026-06-27]
  Partners/OnSuccess__PAR_ID_Generator.dg
    trigger: On Success (Created) | per docs: PROVEN | extraction: DONE 2026-06-27 | verified: YES (matches Session 4 export)
  Partners/OnValidate__PAR_Required_Code.dg
    trigger: Validation on submit (Created or Edited) | per docs: PROVEN (blank + duplicate) | extraction: DONE 2026-06-27 | verified: YES (matches Session 4 export)

FORM: Partner_Locations   [Session 4, 2026-06-27]
  Partner_Locations/OnSuccess__LOC_ID_Generator.dg
    trigger: On Success (Created) | per docs: PROVEN | extraction: DONE 2026-06-27 | verified: YES (matches Session 4 export)
  Partner_Locations/OnSuccess__Primary_Office_Auto_Demote.dg
    trigger: On Success (Created or Edited) | per docs: PROVEN (flips a partner's prior Primary_Office=Yes to No; REPLACES the one-per-partner validation) | extraction: DONE 2026-06-27 | verified: YES (matches Session 4 export)
  Partner_Locations/OnValidate__LOC_Required_Codes.dg
    trigger: Validation on submit (Created) | per docs: PROVEN | extraction: DONE 2026-06-27 | verified: YES (matches Session 4 export)
  Partner_Locations/OnValidate__Partner_Link_Lock.dg
    trigger: Validation on submit (Created or Edited) | per docs: PROVEN (blocks changing Partner_Link after creation) | extraction: DONE 2026-06-27 | verified: YES (matches Session 4 export)
  Partner_Locations/OnValidate__Primary_Office_OnePerPartner.dg
    trigger: Validation on submit (Created or Edited) | per docs: DISABLED in app (turned off; superseded by Primary_Office_Auto_Demote; kept in repo for history) | extraction: DONE 2026-06-27 | verified: YES (matches Session 4 export)

FORM: Partner_Rates   [Session 4, 2026-06-27]
  Partner_Rates/OnSuccess__Partner_Rate_Stamp_Generator.dg
    trigger: On Success (Created) | per docs: PROVEN (tested live 2026-06-27) | extraction: DONE 2026-06-27 | verified: YES (matches Session 4 export)

FORM: Partner_Billing_Contacts   [Session 4, 2026-06-27]
  Partner_Billing_Contacts/OnSuccess__Partner_Billing_Contact_Stamp_Generator.dg
    trigger: On Success (Created) | per docs: PROVEN (tested live 2026-06-27) | extraction: DONE 2026-06-27 | verified: YES (matches Session 4 export)

FORM: Assignments   [Session 5, 2026-06-29; one Employee assigned a Referral. See NOTE 10]
  Assignments/OnSuccess__Assignment_ID_Generator.dg
    trigger: On Success (Created) | per docs: BUILT (calls mint_assignment_id(input.ID); ASG-seq) | extraction: DONE 2026-06-29 | verified: YES (matches Session 5 export)
  Assignments/OnUserInput__Assignment_Pull_From_Referral.dg
    trigger: On User Input (Referral_Link) | per docs: PROVEN (pull) (pulls patient/location/facility from referral + facility show/hide; whole-copy address & Added_Time->Date are watch-items) | extraction: DONE 2026-06-29 | verified: YES (matches Session 5 export)
  Assignments/OnValidate__Assignment_Required_Referral.dg
    trigger: Validation on submit (Created or Edited) | per docs: BUILT (requires Referral_Link AND Employee_Link) | extraction: DONE 2026-06-29 | verified: YES (matches Session 5 export)
  Assignments/OnLoad__Assignment_Lock_Immutable_Fields.dg
    trigger: On Load | per docs: DONE (disables identity fields + Referral_Date; read-only, pull still sets them) | extraction: DONE 2026-06-29 | verified: YES (matches Session 5 export)
  Assignments/OnValidate__Assignment_Change_Log.dg
    trigger: Validation on submit (EDITED only) | per docs: BUILT (diffs old vs new, calls log_change per operational field; identity fields excluded) | extraction: DONE 2026-06-29 | verified: YES (matches Session 5 export)
  Assignments/ShowHide_Facility_block.dg
    trigger: condition block (lives in 3 places: end of pull script, On User Input of Patient_Location, On Load) | per docs: BUILT | extraction: DONE 2026-06-29 | verified: YES (matches Session 5 export)

FORM: Employees   [Session 5, 2026-06-29. See NOTE 10]
  Employees/OnSuccess__Employee_ID_Generator.dg
    trigger: On Success (Created) | per docs: PROVEN (calls mint_employee_id(input.ID); EMP-seq) | extraction: DONE 2026-06-29 | verified: YES (matches Session 5 export)
  Employees/OnSuccess__Employee_Name_Title_Generator.dg
    trigger: On Success (Created or Edited) | per docs: PROVEN ("First Last, Title" -> Employee_Name_Title) | extraction: DONE 2026-06-29 | verified: YES (matches Session 5 export)
  Employees/OnLoadAndOnInput__Employee_Term_Date_Visibility.dg
    trigger: On Load AND On User Input (Employee_Status) [same block in two workflows] | per docs: BUILT (show Employee_Term_Date when Employee_Status == "Inactive", else hide) | extraction: DONE 2026-06-29 | verified: YES (matches Session 5 export)

FORM: Change_Log   [Session 5, 2026-06-29; shared audit form, no .dg of its own]
  note: Data form populated ONLY by functions/log_change. Fields: Source_Form,
  Source_Record_ID, Source_Display_ID, Field_Changed, Old_Value, New_Value,
  Changed_By, Change_Log_ID_Stamp. Native Added Time = change timestamp. Reusable
  by any mutable form (one row per changed field).

FUNCTIONS (Functions tab, standalone)
  functions/fn_resolveUserIdentity.dg
    per docs: DESIGNED (Apr 18, 2026), confirm whether deployed | extraction: PENDING | verified: NO

  Session 4 mint + backfill functions (2026-06-27). One mint function per ID type =
  single source of truth for the format; called by BOTH the On Success generator
  (one-liner) AND a backfill sweep. Idempotency guard: act only when ID is blank or
  "<PREFIX>-REVIEW-"; never overwrite a valid ID.
  functions/mint_location_id.dg
    sig: mint_location_id(int recId) | per docs: PROVEN | extraction: DONE 2026-06-27 | verified: YES (matches Session 4 export)
    LOC-<PartnerCode><BranchCode>-seq; reads Partner_Code across Partner_Link; LOC-REVIEW- fallback
  functions/backfill_location_ids.dg
    sig: backfill_location_ids() | per docs: BUILT | extraction: DONE 2026-06-27 | verified: YES (matches Session 4 export)
    sweep; mints blank/LOC-REVIEW- only; idempotent
  functions/mint_partner_id.dg
    sig: mint_partner_id(int recId) | per docs: PROVEN | extraction: DONE 2026-06-27 | verified: YES (matches Session 4 export)
    PAR-<PartnerCode>-seq; PAR-REVIEW- fallback
  functions/backfill_partner_ids.dg
    sig: backfill_partner_ids() | per docs: BUILT | extraction: DONE 2026-06-27 | verified: YES (matches Session 4 export)
    sweep
  functions/mint_referral_id.dg
    sig: mint_referral_id(int recId) | per docs: PROVEN (live; wired into REF_ID_Generator On Success 2026-06-27) | extraction: DONE 2026-06-27 | verified: YES (matches Session 4 export)
    REF-seq
  functions/backfill_referral_ids.dg
    sig: backfill_referral_ids() | per docs: BUILT (pattern proven via LOC) | extraction: DONE 2026-06-27 | verified: YES (matches Session 4 export)
    sweep

  Session 5 functions (2026-06-29). New prefixes ASG (Assignments) and EMP (Employees);
  plus a shared change-logging helper.
  functions/mint_assignment_id.dg
    sig: mint_assignment_id(int recId) | per docs: BUILT | extraction: DONE 2026-06-29 | verified: YES (matches Session 5 export)
    ASG-seq clean sequence
  functions/backfill_assignment_ids.dg
    sig: backfill_assignment_ids() | per docs: BUILT (live test pending) | extraction: DONE 2026-06-29 | verified: YES (matches Session 5 export)
    sweep
  functions/mint_employee_id.dg
    sig: mint_employee_id(int recId) | per docs: PROVEN | extraction: DONE 2026-06-29 | verified: YES (matches Session 5 export)
    EMP-seq
  functions/backfill_employee_ids.dg
    sig: backfill_employee_ids() | per docs: PROVEN (ran clean) | extraction: DONE 2026-06-29 | verified: YES (matches Session 5 export)
    sweep
  functions/log_change.dg
    sig: log_change(string source_form, source_rec_id, source_display_id, field_label, old_val, new_val, changed_by) | per docs: BUILT | extraction: DONE 2026-06-29 | verified: YES (matches Session 5 export)
    inserts a Change_Log row only when old != new; single source for all change logging

  Session 21 backfills (2026-07-22).
  functions/backfill_dm_full_names.dg
    sig: backfill_dm_full_names() | per docs: PROVEN (ran live 2026-07-22) | extraction: DONE | verified: YES
    Missing-only sweep. Builds DM_Full_Name from DM_First_Name + DM_Last_Name on
    Referrals_Main. Requires a last name; skips rows that already have a value.
    Mirrors the live OnUserInput__DM_Last_Name__Build_DM_Full_Name generator.
  functions/backfill_patient_full_addresses.dg
    sig: backfill_patient_full_addresses() | per docs: PROVEN (ran live 2026-07-22) | extraction: DONE | verified: YES
    Missing-only sweep. Concatenates Patient_Address subfields into
    Patient_Full_Address (line1, line2, city, state, zip; country omitted). Mirrors
    the live OnUserInput__Patient_Address__Build_Full_Address generator.
  functions/backfill_employee_phone_format.dg
    sig: backfill_employee_phone_format() | per docs: PROVEN (ran live 2026-07-22) | extraction: PENDING (Filesystem MCP down at session end; file in repo_pending/) | verified: NO
    Reformats existing Employee_Phone values to AAA-MMM-LLLL. Skips anything that is
    not exactly 10 digits rather than mangling it. Idempotent.

SEQUENCE_TRACKER (stamp / sequence scripts)
  Sequence_Tracker/Scripts_001_006__Object_Prefix_Queries.dg
    per docs: ARCHIVE AHEAD OF CREATOR, reconcile (NOTE 3) | extraction: PENDING | verified: NO

PAGES (custom portal pages)
  pages/partner_portal.dg
    per docs: NOT BUILT (T046 open), placeholder | extraction: N/A | verified: NO

--------------------------------------------------------------------------------
NOTES AND OPEN CONTRADICTIONS (resolve while extracting)
--------------------------------------------------------------------------------
Full detail in context/04_open_contradictions.md. Summary:

NOTE 1  Form name unresolved. Encounter_PatientVisit (May 8 log, June module) vs
        Encounters_Main (April 30 task master). Live Creator name is ground truth.
        Confirm on first extraction and rename this folder to match.

NOTE 2  Non-Deluge logic. Some show/hide is a condition expression, not Deluge.
        Record those as short notes in the form folder so they are not lost.

NOTE 3  Known drift. May 8 log flagged Scripts 001-006 as updated in the old
        archive but NOT pushed to Creator. Extract what is actually live; note any
        archive-only version separately. Do not assume they match.

NOTE 4  Object ID format. SUPERSEDED by Session 4 (2026-06-27); see NOTE 8 for the
        canonical architecture. Branch stays DECOUPLED from referral identity:
        Referral_ID = REF-seq only, no branch token, no PHI. Session 4 settled the
        partner/location formats as PAR-<Partner_Code>-seq and
        LOC-<Partner_Code><Partner_Location_Code>-seq (Partner_Code read across
        Partner_Link). The v1.2 suffix and T011 formats are dead. The REF retrofit is
        COMPLETE (2026-06-27): REF_ID_Generator On Success now calls mint_referral_id;
        the old inline generator is superseded. Read context/07 and NOTE 8 before any
        ID or sequence work.

NOTE 8  Partner Cluster ID architecture (Session 4, 2026-06-27). One standalone mint
        function per ID type is the single source of truth for that ID's format. Each
        mint is called by BOTH the form On Success generator (a one-liner) AND a
        backfill sweep, so API/import paths that bypass form workflows are still
        covered. Idempotency guard: act only when the ID is blank or "<PREFIX>-REVIEW-";
        never overwrite a valid ID. Form validations (cancel submit) hard-block at the
        form; the REVIEW- mint branch is the backstop for non-form creation paths.
        ID formats: REF-seq | PAR-<Partner_Code>-seq |
        LOC-<Partner_Code><Partner_Location_Code>-seq.
        Field settings applied: No-duplicate-values on Partner_ID, Partner_Location_ID,
        Partner_Code (Referral_ID already had it). Sequence_Tracker rows REF, PAR, LOC
        seeded at 1001.
        DONE 2026-06-27: auto-demote primary (Primary_Office_Auto_Demote, replaces the
        one-per-partner validation, now DISABLED); Partner_Link lock validation; stamp
        generators live-tested (Partner_Rate, Partner_Billing_Contact); REF retrofit live.
        OPEN / next session:
        - Report: add Partner Code column to Partner_Locations Report, group by partner
        - Run backfill sweeps (LOC, PAR, REF); confirm idempotent, fills only blanks
        - Partner_Link lock: add UI read-only on edit as a second layer (validation done)
        - GUARDRAIL: deleting a Partner ORPHANS its locations (dangling Partner_Link ->
          backfill flags LOC-REVIEW). Block deleting a Partner that still has
          Partner_Locations, or force deactivate instead. Found 2026-06-27 in backfill test.
        - Patient_Full_Name_Generator: confirm the 4 link names, then enable (drop .PENDING).

NOTE 9  NEXT MODULE: Assignments -> PVS (spec, not built; Session 4 2026-06-27).
        Assignment = one Employee assigned a Referral. Form fields: Referral_Link
        (-> Referrals_Main), Employee_Link (-> Employees), Assignment_Status
        (Pending/Acknowledged), Acknowledged_On. On Success: sendmail to
        Employee_Link.Employee_Email (CONFIRM exact email link name). Acknowledge =
        provider flips status. Referral_Link lookup DISPLAY: Patient_Full_Name +
        Referral_Date + Referral_ID (sort newest-first); search by name OR referral id;
        filter to unassigned/open referrals. DECISION 2026-06-27: add a dedicated
        Referral_Date field to Referrals_Main (distinct from native Added Time). This is
        why Patient_Full_Name_Generator exists (feeds the lookup display).
        STATUS: Assignments + Employees forms BUILT in Session 5 (2026-06-29); see NOTE 10.

NOTE 10 Session 5 (2026-06-29): Assignments + Employees + Change_Log built. New ID
        prefixes ASG (Assignments) and EMP (Employees), same mint+backfill pattern.
        - Assignments: one Employee assigned a Referral. Assignment_Status = Pending
          (default) / Accepted. One-per-referral via No-duplicate on Referral_Link.
          On user input of Referral_Link pulls patient/location/facility from the
          referral. Identity fields (Patient name/MI/last/DOB) are immutable-from-
          referral: read-only (On Load disable) and NOT change-logged. Patient_Hospice_ID
          removed from Assignments (flows referral -> PVS). No-duplicate on Assignment_ID;
          Sequence_Tracker ASG row at 1001.
        - Employees: Employee_Name_Title = "First Last, Title". Employee_Term_Date shows
          only when Employee_Status == Inactive. License_Expiration_Date always-visible/
          optional (no renewal management). No-duplicate on Employee_ID; Tracker EMP at 1001.
        - Change_Log: shared audit form, populated only by log_change (one row per changed
          field, only when old != new). Reusable by any mutable form.
        WATCH-ITEMS: Assignment pull does a whole-copy of Patient_Address and maps
        Added_Time -> Referral_Date; confirm these behave on real data.
        OPEN / NEXT:
        - VERIFY (load-bearing): do Creator On Success / Validation workflows fire on
          ZOHO-FORM-mapped referrals? If not, REF ID, Patient Full Name, and Partner POC
          Name Title generators will NOT run on partner submissions -> scheduled backfills
          needed. Ties directly to NOTE 7.
        - Assignment notifications: SMS (Twilio outbound) + email on creation, each linking
          to a new EMPLOYEE PORTAL; acknowledge via portal (no reply-YES). Build portal +
          My Assignments page.
        - Remap Zoho Form -> Referrals_Main for new fields (Referral_Source, Patient_Hospice_ID).
        - PVS build (launch from assignment; pull from referral; field-tiered immutability;
          draft invoice + fax + email on submit). See PVS/Billing design notes.
        - Referral_Source unify decision (Contracted Partner / SOS Internal): conditional
          partner section, M-marker, billing branch.

NOTE 5  Secrets and data. Never commit keys, tokens, secrets, test records, or
        PHI. Code only.

NOTE 6  Referrals_Main has 5 On-User-Input formatters live (Decision_Maker_Phone,
        Patient_Phone, Patient_SSN, Facility_Phone, Partner_POC_Phone), not the 2
        previously tracked. Each appears under both a "Created" trigger group and a
        "Created or Edited" group; the "Created or Edited" copies are the enabled
        canonical set (extract those). Decision Maker Phone Format is enabled under
        BOTH groups, but the contains("(") idempotency guard makes a double-fire
        harmless. The 4 phone formatters share one pattern: strip to digits, take
        the last 10, reformat. UPDATED 2026-07-09: mask changed from (AAA) MMM-LLLL
        to the app-wide standard +1 (AAA) MMM-LLLL; idempotency guard changed to
        startsWith("+1 (") and a <10-digit guard added. See NOTE 8 (phone standard).

NOTE 7  Referrals_Main is NOT entered by humans in Creator. The public form is a
        Zoho Form mapped into this Creator form; the Creator form only stores data
        for backend processing. Implications for the 5 formatters:
        - SSN Format is load-bearing: Zoho Forms cannot format SSN, and the reporting
          dashboard needs XXX-XX-XXXX, so Creator is the only place SSN gets
          normalized. Keep it. Pattern is format-on-write (normalize once at save).
        - The 4 phone formatters are a backstop: Zoho Forms can format phone on its
          front end, so inbound phone may already be formatted (the contains("(")
          guard then no-ops). Kept as insurance for any non-Zoho-Form entry path
          (manual, import, API). Low stakes to disable if trimming.
        - OPEN: trigger type unconfirmed. The .dg filenames say OnUserInput, but the
          live workflow list grouped these under "Created" / "Created or Edited",
          which would fire on the Zoho Form integration (On User Input would NOT,
          since no one types in the Creator form). If confirmed On Create / On Create
          or Edit, rename files to OnCreateOrEdit__*. VERIFY by opening one real
          inbound record and checking whether the SSN/phone value is formatted or raw.

NOTE 8  PHONE FORMAT STANDARD (app-wide, 2026-07-09). Every phone/fax field on every
        form uses the same viewing mask: +1 (AAA) MMM-LLLL. Creator has no input mask,
        so a shared On-User-Input formatter normalizes whatever is typed (strip to
        digits, take last 10, reformat; guard startsWith("+1 (") + <10-digit guard).
        FIELD-TYPE PLAN (Neil, Creator side): native Phone (type 27) fields cannot emit
        this custom string, so each is being deleted and rebuilt as a Single Line text
        field WITH THE SAME LINK NAME, then its formatter pasted. Referrals_Main fields
        were already Single Line; only their mask changed.
        Formatters in repo (15):
          Referrals_Main:        Patient_Phone, Decision_Maker_Phone, Facility_Phone, Partner_POC_Phone  (mask updated; trigger unchanged - see NOTE 7 OPEN)
          Encounter_PatientVisit: Patient_Phone, Facility_Phone, Partner_POC_Phone
          Assignments:           Patient_Phone, Facility_Phone
          Employees:             Employee_Phone
          Partners:              Partner_Phone
          Partner_Billing_Contacts: Partner_Billing_POC_Phone, Partner_Billing_POC_Phone1 (Fax)
          X_Ray_Orders:          Patient_Phone, X_Ray_Results_Fax
        status: BUILT, UNTESTED | extraction: N/A (authored) | verified: NO
        VERIFY LIVE:
          1. Confirm the Zoho Form actually outputs +1 (AAA) MMM-LLLL. On-User-Input
             formatters do NOT fire on the Zoho Form integration path, so inbound
             (Referrals) phones rely on the Zoho Form already matching this mask. If it
             differs, inbound is not normalized and needs an On-Create/Edit normalizer
             or a Zoho Form change.
          2. Any form where phone arrives programmatically (workflow insert / import),
             not typed and not copied from an already-formatted source, bypasses the
             On-User-Input formatter - confirm per form.
          3. Rebuild each converted field as Single Line with the IDENTICAL link name so
             every existing reference (incl. the PVS pre-fill/lock) keeps working.

================================================================================
SESSION 6 ADDITIONS (2026-07-02)
================================================================================
Partner_Rates/
  OnSuccess__Partner_Rate_Current_Flag_Generator.dg  - calls set_current_rate(input.ID). Created or Edited. PROVEN.
  OnValidate__Partner_Rate_Branch_Match.dg           - blocks branch not under selected partner. PROVEN.
  (form config, no .dg) DEPENDENT LOCATION FILTER on Partner_Location_Link:
      Set filter -> Field = "ID" under the Partner Link heading -> equals -> Value = input.Partner_Link. PROVEN.
  NEW field: Current_Rate (radio No/Yes).
Partner_Locations/
  OnSuccess__Location_Label_Generator.dg  - Partner_Location_Label = Partner_Display_Name + " - " + Partner_Location_Code.
  NEW field: Partner_Location_Label. NOTE: Partner_Link_Lock repo copy already guarded; live app was behind, now synced.
Partner_Contracts/  (NEW form/object)
  OnSuccess__Partner_Contract_ID_Stamp_Generator.dg  - native stamp.
  OnValidate__Partner_Contract_Branch_Match.dg        - blocks branch not under selected partner.
  Fields: Partner_Link, Partner_Location_Link, Partner Contract Upload (file), Partner Contract Effective Date,
          Partner Contract Term Date, Partner Contract Status, Contract Notes (RTF), Partner_Contract_ID_Stamp.
  TODO: add dependent location filter (ID equals input.Partner_Link).
functions/
  set_current_rate.dg          - recomputes Current_Rate for a rate's group (latest Active Eff.Date = Yes).
  backfill_current_rate.dg     - sweep -> set_current_rate for all rates. Idempotent.
  backfill_location_labels.dg  - sweep -> sets Partner_Location_Label on existing locations.
NOTES:
  - Rates keep native ID only (Partner_Rate_ID_Stamp); no partner-id stamp (Neil wants partner/branch VISIBLE via lookups/label).
  - Partner_Locations has NO Partner_ID field (partner only via Partner_Link).
  - Branch code field link name = Partner_Location_Code (NOT Partner_Loc_Code).
  - Partners: Partner_Legal_Name (invoice bill-to) + Partner_Display_Name (friendly).
  - Billing Contacts: links via Partner_Location_Link (partner derivable); has Partner_Link w/ existing workflows (review).
TODO (next): dependent filter on Partner_Contracts + Partner_Billing_Contacts location lookups; enter real rate card.

--- Session 6 addendum (2026-07-02) ---
Partner_Billing_Contacts/OnValidate__Partner_Billing_Contact_Branch_Match.dg  - added (blocks branch not under selected partner).
DECISION: location lookups (Rates, Contracts, Billing Contacts) DISPLAY = "Partner Loc Name" (always populated),
NOT Partner_Location_Label (blank on un-backfilled locations -> caused "No matches found"). Label field optional / reports only.

================================================================================
SESSION 7 ADDITIONS (2026-07-03)
================================================================================
PARTNER BILLING CONTACTS - COMPLETE.
  - ID stamp generator: pre-existing (Partner Billing Contact Stamp, Created -> Successful form submission).
  - Dependent location filter (ID equals input.Partner_Link): DONE.
  - Partner_Billing_Contact_Branch_Match (Created or Edited -> Validations on form submission): block CONFIRMED live 2026-07-03.
  - Only two workflows on the form (Stamp On Success + Branch Match Validate) -> no collision; resolves the "review Partner_Link workflows" open item.
  - Note: on a partner with no locations (e.g. ABC Hospice), the dependent filter clears the branch, so Branch Match correctly skips (nothing to catch). Branch Match is the backstop for non-UI writes (Zoho Form / API / import) where the filter does not apply.

PATIENT_FULL_NAME GENERATOR - promoted off .PENDING (see Referrals_Main section). Live, Created or Edited -> Successful form submission.

ACCENTCARE RATE CARD - entered LIVE (6 rates on AccentCare - TPA). Current_Rate=Yes set by the generator (each is sole rate in its group).
  Categorization (Rate_Category -> Rate_Type $): 
    Acuity Level -> Low Complexity $150 / Moderate Complexity $343 / High Complexity $545
    Service      -> Telemedicine $55
    Premium      -> After Hours (7pm-7am) $100 / Super STAT (within 90 min) $250
  CLEANUP TODO: delete two dummy "Partner Legal Name" rate rows ($375 Moderate, $545 High; one has no ID stamp / Current_Rate).
  TODO: InnoVage rate rows have blank location -> assign Tampa/Orlando (or a "Main") once locations-always-exist is enforced.
  Rate-entry ergonomics: CSV import is the pragmatic bulk-entry path now; Rate Sheet + subform (fan-out to Partner_Rates via set_current_rate) parked as a post-Friday enhancement.

REFERRALS IMPORT TEMPLATE (one-time Cognito July load) - built SOS_Referrals_Import_Template.xlsx (downloadable; not committed to repo).
  Source = uploaded mapping "sos-referrals-main-form-field-mapping-07032026.csv" (authoritative Creator field LINK names).
  44 importable fields; headers = Creator link names in form order. EXCLUDES section headings, the 3 file-upload fields,
  and custom-script/system fields (Referral_ID, Referral_ID_Stamp, Partners lookup, Partner_ID, Partner_ID_Stamp = backfilled).
  Import gotchas: workflows DON'T fire on import -> backfills needed (REF-ID, Patient_Full_Name, partner-match); lookups match by value
  (Partner_Organization text must match a Creator Partner); dates yyyy-MM-dd; decide a dupe key (Cognito ref id) if re-importing.
  Data-integrity flags from the mapping to VERIFY on the live form:
    - Advanced_Directives_Details RESOLVED 2026-07-04: field is Multi Line in Creator (CONFIRMED Neil); Patient_Has_Advanced_Directives is Radio [No, Yes].
    - Patient_Gender is Single Line in Creator vs Radio Female/Male in the form -> import exactly "Female"/"Male".
    - Patient_Room_Number typed "Address" (source "Room #" Single Line) -> confirm it accepts a plain room number.

DECISION - REFERRALS_MASTER ARCHITECTURE (hub-and-spoke, AGREED 2026-07-03):
  - Referrals_Master = PASSIVE aggregate hub for referral tracking. NO ID/stamp/generator workflows on it; it only receives.
  - Spokes (Referrals_Main/Patient Visit, and future short forms X-ray, Lab, 3008) own their detail + ID generation and, on CREATE, insert one row into Master.
  - GUARDRAIL 1: every Master row carries a back-reference = Referral_Type + spoke record ID (+ spoke REF ID) so it is traceable to its authoritative spoke.
  - GUARDRAIL 2: spoke->Master insert is CREATE-ONLY or idempotent (no duplicate hub rows on edits).
  - NATURE: Master is a create-time SNAPSHOT / tracking index; spokes stay authoritative for live values. Optional On-Edit sync later (Data-Quality initiative).
  - Short type forms built as CREATOR forms (not Zoho Forms) would get native Deluge alert() MODALS (attention-grab) and write straight into Creator.
    Zoho Forms cannot do per-question modals. Non-Zoho builders (Jotform/Typeform/Formstack) reach Creator only via Zoho Flow/Zapier/webhook+API
    (no native connector) and gate on HIPAA BAA. Not pursuing a builder switch now. (Neil "thinking about it".)

PARKED / NICE-TO-HAVES (revisit later, not built):
  - Completeness Checker (referrals): review vital fields -> Complete/Incomplete status + missing-fields summary -> email flag.
    Auto-fill ONLY deterministic derivations (full name, age from DOB, formatting, DM=patient when self-responsible); NEVER fabricate patient data. Route real gaps to a human.
  - Referral Data-Quality initiative: address validation (NOTE: Patient Referral Zoho Form ALREADY uses Google Maps validation; gaps = non-form paths like import,
    valid-but-wrong entries, and propagation of corrections to already-created vendor orders); reference-based (lookup) vendor orders so pre-dispatch corrections propagate;
    re-sync for open not-yet-dispatched orders; pre-dispatch verification checkpoint; phone verification (Twilio Lookup / NumVerify) OPTIONAL (validates active number, not that it's the patient's).
    Distinction: completeness = "is it filled?" vs correctness = "is it right?".
  - Single/Multi-Unit partner flag (UX): more elegant than always-create-a-location, but blank-branch downstream handling deferred. Kept locations-always-exist for now.
  - Live dashboards: SOS build-tracker (from Open Items) and a Billing/AR dashboard once invoices flow (Zoho Books currently has 1 draft invoice, $575 Loyola Hospice).

functions/set_partner_poc_name_title.dg + functions/backfill_partner_poc_name_title.dg - BUILT 2026-07-03. Backfill for Partner_POC_Name_Title ("First Last, Title" e.g. "John Smith, RN"), mirrors the live OnSuccess__Partner_POC_Name_Title_Generator. Missing-only sweep; deploy set_ first. For the Cognito import.
functions/backfill_referral_id_stamp.dg - BUILT 2026-07-03. Sets Referral_ID_Stamp = rec.ID.toString() where blank. Needed for imported records (Option A kept Cognito Referral_ID, so mint_referral_id did NOT run -> stamp blank). Missing-only; won't disturb mint_referral_id-stamped records.

OPEN / NEXT (carry forward):
  1. Patient_Full_Name BACKFILL - BUILT 2026-07-03, BACKFILL NOT YET RUN. functions/set_patient_full_name.dg (builder, require-last-name; arg recId int, Default namespace) + functions/backfill_patient_full_names.dg (missing-only sweep; no args, Default namespace). Deploy set_ FIRST (backfill line 13 calls it; "function not found" if missing/other namespace). NOTE: REF-1006 ("Fat Albert") confirmed the LIVE On-Success generator populates Patient_Full_Name on NEW records; the backfill function itself is still UNTESTED (execute after July import, spot-check one with/one without last name). DIVERGENCE: live On-Success generator is permissive (first-name-only when no last name); backfill/builder require last name. Optional follow-up (needs approval): refactor live generator to call set_patient_full_name for consistency.
  2. REF-ID backfill + partner-match backfill for July import - verify/exist before load.
  3. Finalize Cognito->Creator crosswalk once July export headers provided.
  4. Enter remaining partners' rate cards (CSV import path).
  5. Delete dummy "Partner Legal Name" rate rows; assign InnoVage rate locations.
  6. RESOLVED 2026-07-03 (load-bearing, NOTE 7/10): Creator ON-SUCCESS workflows DO fire on Zoho-Form-mapped referrals. Proof: REF-1006 submitted via the public Zoho Form received both Referral_ID (REF-1006) and Patient_Full_Name ("Fat Albert") = REF_ID_Generator + Patient_Full_Name generator both ran on the integration path. => generators run on real partner submissions; backfills needed ONLY for the one-time Cognito import. SSN SPOT-CHECK RESOLVED 2026-07-03: SSN formatting is done ENTIRELY by the ZOHO FORM, which passes XXX-XX-XXXX to Creator (REF-1001 shows XXX-XX-XXXX). The CREATOR form CANNOT format SSN on the intake path: its SSN formatter is On User Input, and nobody types in the Creator form (Zoho Form is the only intake), so it never fires (and On User Input won't fire on import/API paths either). This REVERSES NOTE 7, which wrongly called the Creator SSN formatter "load-bearing"; the Zoho Form is what is load-bearing for SSN. Creator's OnUserInput__Patient_SSN__Format is effectively inert on all real paths. STILL TO SPOT-CHECK (lower stakes): On-Validate stage behavior on the integration path.
  DATA-INTEGRITY FLAG 2026-07-03: REF-1001 has Patient_Last_Name = "16025 Muirfiled Dr" (an address in the last-name field). Determine if junk test data OR a Zoho Form -> Creator mapping error (address wired into Patient_Last_Name). If mapping, it corrupts real referrals and the full-name generator. VERIFY before Friday live submissions. (Ties to Referral Data-Quality initiative: correctness vs completeness.)
  7. PVS build.
  8. Build X-ray/Lab/3008 spoke forms + Referrals_Master hub + spoke->Master create-only insert.
  9. DONE 2026-07-04: Advanced_Directives_Details confirmed Multi Line; Patient_Has_Advanced_Directives confirmed Radio [No, Yes].
  ENV NOTE: repo reachable this session at /Users/neilheird/Claude/GitHub/sos-emr (memory's /Users/neilheird/GitHub/sos-emr path is stale).
  GOAL: parallel-test new app vs Cognito Forms - target FRIDAY.

================================================================================
SESSION 8 ADDITIONS (2026-07-03, resumed)
================================================================================
COGNITO IMPORT - records loaded + backfilled.
  - 32 referrals imported into Referrals_Main. Cognito Referral IDs kept (Option A):
    Referral_ID = REF-MMDDYY-#### (do NOT run backfill_referral_ids on these). Added via
    SOS_Referrals_Cognito_July_Filled_2c.xlsx (Referral_ID col, comma cleaned), incrementally uploaded.
  - SSN + Patient Email import blank = CORRECT (Cognito has no SSN column; patient email 0/32).
  - Ran 3 backfills on the imports: backfill_patient_full_names, backfill_partner_poc_name_title,
    backfill_referral_id_stamp. STILL TO RUN: partner-match (needs Partner records + Empath model).
functions/set_partner_poc_name_title.dg + backfill_partner_poc_name_title.dg - BUILT. "First Last, Title".
functions/backfill_referral_id_stamp.dg - BUILT. Referral_ID_Stamp = rec.ID.toString() where blank.
  (Deployed live + the 3 backfills were run by Neil.)

COGNITO FILE ATTACHMENTS (open). Linked folder "PatientReferral (4)": 39 files across 23 records,
  in PatientAdvancedDirectivesUpload (4) + PatientFilesUpload (35). Filenames prefixed with the Cognito
  entry number = numeric suffix of Referral_ID -> clean key. Manifest: SOS_Cognito_File_Manifest.xlsx.
  OPEN: field targets (which Creator file fields); upload method (Creator import-with-attachments vs
  v2.1 API vs manual); FLAG #1255 = 2 files with NO matching referral in the export.

PVS DESIGN - see context/10_pvs_design.md (new). Key decisions:
  - PVS = NATIVE CREATOR PORTAL FORM (not Zoho Forms) - prefill patient + provider, provider signs.
  - Two creation methods (portal lookup; referral-email deep-link, Referral_ID-only in URL).
  - Two pulls to build: patient-from-referral, provider-from-login (Employees).
  - PVS_ID = "PVS-"+Referral_ID (2nd Final PVS -> -v2); walk-in = PVS-1001-M. ADD PVS_ID_Stamp.
    KEEP PVS_Referral_ID (load-bearing: 4 workflows incl. PVS Stamp Generator).
  - Type_of_Entry: partner-determined, LOCKED when pulled; change via addendum. Align option lists.
  - ARCH CONFIRMED: one referral form + one PVS form, both conditional by type; all -> Referrals_Master.
  - OPEN: review PVS Stamp Generator; Patient Details additions; Complexity_Level<->Rate_Type; charges
    auto-vs-manual; Referral Partner POC fields; Employee_Initials/signature; PVS_ID generator build.

CARRY FLAGS: confirm Empath-as-parent before partner-match.
  RESOLVED 2026-07-04: DM Last Name integration bug FIXED (now maps to Decision Maker Last Name);
  Advanced_Directives_Details field type confirmed Multi Line.

================================================================================
SESSION 9-10 ADDITIONS (2026-07-07 / 2026-07-09)
================================================================================
SCHEMA MONITOR SYSTEM (new infrastructure) - PROVEN end-to-end 2026-07-09.
  Purpose: auto-mirror the live Creator field schema to the repo so field lists
  never have to be recalled manually. Creator cannot write to disk, so it commits
  to GitHub; you pull to sync down.
  Connections (Zoho Connections, not in code):
    - sos_schema_monitor : Zoho Creator, Get Forms + Get Fields (Meta API read).
    - sos_github_sync    : GitHub OAuth (custom app, personal acct), commits to
                           m1ndspark/sos-emr. Token never in a field/script.
  Form: Schema_Snapshot (Snapshot_Data, Captured_On, Change_Summary, Added_User) -
    stores compressed schema snapshots for diffing. Storage only, no workflow.
  Functions (Default namespace, standalone):
    - run_schema_monitor  : called by schedule "SOS Schema Monitor (Daily)" 06:00.
      Pulls all forms/fields via Meta API, diffs vs latest snapshot; on change,
      commits per-form schema files to schema/<Form>.md, TOMBSTONES removed forms,
      emails a grouped HTML change alert (adds/removes/changes + active-form list).
      Has a false-removal guard (aborts if >30% of forms vanish in one run).
    - seed_schema_to_github : one-time backfill; wrote all 20 schema/ files 07-09.
    - test_schema_connection / test_github_commit : proof/test helpers.
  schema/ folder = AUTO-GENERATED per-form field mirror (link name, type, mandatory,
    unique, choices, subfields). Authoritative for FIELD LISTS. Pull after a monitor
    run to read current schema locally. context/06 adds Zoho-Form mapping + context;
    on conflict, schema/ wins.

FORM INVENTORY RECONCILED (live vs the 16-form master list at top of this file):
  - RETIRED 2026-07-09: Partner_Branch_Territory. Redundant with Partner_Locations
    (branch identity already covered); no workflows attached. Deleted from Creator,
    tombstoned + removed from repo. Full schema recoverable in git (commit 3b53a34).
  - NOT LIVE (in master list, never built / dropped): Partner_Portal_Users,
    Charge_Types.
  - LIVE but added since the master list: Partner_Billing_Contacts, Partner_Contracts,
    Change_Log, Encounters_PVSAddendum, X_Ray_Orders.
  - X_Ray_Orders = live, built spoke (13 fields; own X_Ray_Order_ID + _Stamp;
    Referral_Link, Provider_Signature_Link, results fax/email). NOTE: no Sequence_
    Tracker prefix confirmed for it yet.
  - Encounter_RadiologyRequest = EMPTY SHELL (0 fields live). Radiology consolidation
    candidate: X_Ray_Orders appears to supersede it. Confirm which is canonical;
    likely retire the empty one (tests the tombstone flow again).

REFERRAL FLOW + BILLING ARCHITECTURE: see context/11_referral_flow_and_billing.md
  (new 2026-07-09). Referrals_Main full walkthrough, partner data model
  (Partners -> Partner_Locations -> rates/contracts/billing at LOCATION level),
  the billing boundary (NOTHING charged at referral; all charges originate at PVS),
  and the branch-reconciliation gap.

CHAT HANDOFF: see context/12_session_handoff_2026-07-09.md (new 2026-07-09).
  Self-contained brief for the claude.ai chat side (chat and code cannot share
  threads). Full decision log + final Deluge for the PVS referral pre-fill/lock
  (Option B) with the Edit_Needed override, the app-wide phone/fax format standard
  (+1 (AAA) MMM-LLLL), open items/VERIFY-LIVE, Creator checklist, and PVS +
  Referrals_Main field link names.

KEY OPEN ITEMS (from Session 10 walkthrough):
  1. BRANCH RECONCILIATION (load-bearing): typed free-text Partner_Branch must
     resolve to a real Partner_Locations billing-location record, since rates are
     location-keyed. Runs on EVERY Referrals_Main submit (alongside REF-ID gen).
     Mechanism TBD. Unmatched is safe (PVS invoices default Draft; review dashboard
     approves single/bulk before billing). Same crosswalk as Cognito import (ctx 09).
  2. SOS Internal (non-hospice) billing basis - partner->location->rate chain assumes
     a contracted partner; internal/subscription referrals bill differently. TBD.
  3. Encounter_RadiologyRequest empty-shell cleanup (see above).

================================================================================
SESSION 11-12 ADDITIONS (2026-07-10)
================================================================================
PHONE / FAX FORMAT STANDARD - SUPERSEDED (Session 11). New mask AAA-MMM-LLLL
(was +1 (AAA) MMM-LLLL). Full spec in context/12 Section B (superseded) and the
formatter learnings in context/05. Three layers per field: tooltip + On-User-Input
formatter (strip/reject + re-entry guard, collapse-to-raw on invalid length) +
On-Validate 10-digit block with per-field message. REJECT not trim. Do NOT use
field max-char as the cap (fires Creator's generic popup before On-Validate).
  DONE + TESTED LIVE: Partner_Billing_Contacts (reference implementation):
    Partner_Billing_Contacts/OnUserInput__Partner_Billing_POC_Phone__Format.dg (final template)
    Partner_Billing_Contacts/OnUserInput__Partner_Billing_POC_Fax__Format.dg (new)
    Partner_Billing_Contacts/OnValidate__Partner_Billing_Contact_Branch_Match.dg (now also validates phone+fax; branch-match block is dead code - filtered lookup + dependent dropdown prevent a mismatch)
    Field changes: Partner_Billing_POC_Phone converted Phone(27)->Single Line;
      new Partner_Billing_POC_Fax; RETIRED Partner_Billing_POC_Phone1 (+ its .dg).
  TODO (roll out new standard, one form at a time, test each; each needs field
    conversion to Single Line same-link-name + formatter + On-Validate + tooltip):
    Referrals_Main (Zoho-Form-fed - formatter only helps manual entry, see NOTE 7),
    Encounter_PatientVisit, Assignments, Employees, Partners, X_Ray_Orders.
  NOTE: NOTE 8 above still documents the OLD +1 (AAA) standard - superseded by this
    block and context/12 Section B. Reconcile NOTE 8 in a future cleanup.

PVS REFERRAL PRE-FILL / EDIT_NEEDED LOCK SYSTEM - DEPLOYED + TESTED LIVE (Session 12).
  The 4-workflow lock system (Default_Hide_On_Load, Has_Referral_ID__Show_Hide,
  Referral_Link__PreFill, Edit_Needed__Unlock) existed in the repo but was NOT in
  Creator; deployed live 2026-07-10 and the full 5-step cycle verified. See the
  PVS form section above for per-workflow status and the deploy gotcha (old
  "Referral Fields Default Hide" + "Patient Fields Editability Toggle" DISABLED).
  Provider_PreFill (Employees-by-email) confirmed working live earlier (logged-in
  user's provider fields populate + lock). Edit_Needed Radio (No/Yes) field is live.
  DONE 2026-07-12 (Session 14): PVS_Referral_ID moved into System_Fields_Section;
  all inline show/hide PVS_Referral_ID removed from Has_Referral_ID Show_Hide (3 branches);
  Default Hide On Load now hides System_Fields_Section + disables PVS_Referral_ID. Commit 20cc4e2.

STANDING BEHAVIOR (set Session 11): "Document everywhere" / "please document
  everywhere" = mid-work doc flush (NOT end of session). "End of day" / "EOD" =
  same four actions (Apple Notes log + downloadable copy + repo updates by Claude
  judgment + Claude Code git prompt) but a fuller wrap-up log; Neil declares it.
  No time-awareness assumptions; no prompting to end. Neil works ~12 hr/day.

CLEANUP BACKLOG (accumulating - do in a pass):
  - Delete disabled PVS workflows "Referral Fields Default Hide" + "Patient Fields
    Editability Toggle" (disabled, not deleted).
  - Delete stale placeholder OnUserInput__Type_of_Entry__Section_Visibility.dg
    ("Entry Type Section Visibility" IS live per 2026-07-10 workflow list - RE-VERIFY:
    the earlier "does not exist" note may be wrong; confirm before deleting the .dg).
  - Reconcile NOTE 8 (old phone standard) with the new AAA-MMM-LLLL standard.
  - Retire empty Encounter_RadiologyRequest (confirm X_Ray_Orders supersedes).

================================================================================
SESSION 14 ADDITIONS (2026-07-12)
================================================================================
PVS_Referral_ID RELOCATION (DONE + committed 20cc4e2, b32f76e). Field moved into
System_Fields_Section; all inline show/hide PVS_Referral_ID removed from Has_Referral_ID
Show_Hide (3 branches); Default Hide On Load hides System_Fields_Section on load + disables
PVS_Referral_ID. Users never see it inline; it is a system-generated stamp.

PVS_ID + PVS_Referral_ID FORMAT FINALIZED (full detail in context/10 Session 14 update).
PVS_ID mints from a single shared "PVS" Sequence_Tracker row: referral = PVS-<seq>-<init>
(e.g. PVS-1001-JK); walk-in = PVS-<seq>-<init>-M (e.g. PVS-1002-JK-M). PVS_Referral_ID =
"PVS-" + Referral_ID on the referral path only (PVS-REF-1001), BLANK on walk-ins. Patient-
initials code DROPPED (no-PHI-in-IDs rule); provider initials kept.
  OPEN: live generator has an && / || precedence bug on the PVS_Referral_ID line (a walk-in
  would stamp "PVS-null"); paren fix supplied, DEPLOY/VERIFY UNCONFIRMED as of EOD. Also seed
  the "PVS" seq row @1001; add No-duplicate on PVS_ID; extract the verified generator into the
  still-placeholder OnSuccess__PVS_Stamp_Generator.dg.

WALK-IN FIELD-GREYING BUG - FIXED + VERIFIED LIVE. Symptom: clicking "No" (walk-in) greyed the
patient entry fields. ROOT CAUSE: the Has Referral_ID Show_Hide No branch sets input.Edit_Needed
= null, which TRIGGERS Edit_Needed Unlock (On User Input of Edit_Needed); its old else (null !=
"Yes") disabled the patient fields immediately after they were enabled. FIX: wrapped the entire
Edit_Needed Unlock body in if(input.Has_Referral_ID == "Yes") so it no-ops on walk-ins. Committed
this session.
  CREATOR LEARNING: setting input.<field> inside one On-User-Input workflow can TRIGGER another
  On-User-Input workflow that watches that field. Two handlers reacting to the same click can fight.
  When a workflow nulls/sets a field that has its own On-User-Input logic, guard that logic.
  (Earlier On-Load enable-quirk hypothesis was WRONG; this cross-workflow trigger was the cause.)

WORKFLOW INVENTORY RECONCILED (live PVS list, 2026-07-12). ENABLED: Pre-fills provider section,
Default Hide On Load, Additional Charges Show Hide, Diversion Type Show Hide, Referral Link Pre-Fill,
Entry Type Section Visibility, Edit_Needed Unlock, Has Referral_ID Show_Hide, PVS ID Stamp Generator.
DISABLED (legacy, not deleted): Referral Fields Default Hide, Patient Fields Editability Toggle.
  INDEX CORRECTIONS:
  - "Entry Type Section Visibility" IS LIVE + ENABLED (On User Input of Type_of_Entry). The
    OnUserInput__Type_of_Entry__Section_Visibility.dg row above (per docs: DOES NOT EXIST) is WRONG.
    Live code captured this session; extract it and correct that row.
  - Has Referral_ID Show_Hide live copy MATCHES repo (null-wipe, no PVS_Referral_ID lines). No drift.

CARRY-FORWARD FOR NEXT SESSION (2026-07-13):
  1. ICD-10 CODE CAPTURE into the PVS (Neil's stated priority): make the ICD-10 fields behave like a
     Creator multi-select, but with options from a LOOKUP linked to the national ICD-10 registry
     instead of manually typed choices - search live + multi-select codes onto the form. See
     context/10 open items.
  2. PVS ID Stamp Generator: apply the paren fix, deploy, verify; seed "PVS" Sequence_Tracker row
     @1001; add No-duplicate on PVS_ID; then extract into the placeholder .dg.
  3. Extract "Entry Type Section Visibility" live code into its .dg; fix the stale _INDEX row.
  4. Phone/fax standard (AAA-MMM-LLLL) rollout to the remaining 6 forms (carry from Session 12).
  5. Cleanup pass: delete the two disabled legacy PVS workflows; retire empty Encounter_RadiologyRequest.

================================================================================
SESSION 15 ADDITIONS (2026-07-13)
================================================================================
ICD-10 CODE CAPTURE (PVS provider side) - BUILT + VERIFIED LIVE.
  Design: partner ICD codes = free text (Referrals_Main), provider ICD codes = validated
  multi-select lookup against a local Creator reference table. No live external API, no
  portal. National registry is the SOURCE of the table, refreshed annually.
  ICD10_Codes reference form (form link name: ICD10_Codes) - CREATED + LOADED.
    Fields: ICD_Code (Single Line, No-duplicate ON), ICD_Description (Single Line),
    ICD_Display (Single Line, "E11.9 - desc", the lookup search/display field), Status
    (Radio Active/Retired), FY_Last (Number), Chapter (Single Line), Category (Single Line),
    Source_FY (Number).
    DATA: CMS FY2027 ICD-10-CM billable set, 74,879 rows, imported via CSV (all unique,
    verified). Source file: cms.gov "2027 Code Descriptions in Tabular Order" ZIP ->
    icd10cm_codes_2027.txt. Codes reformatted to decimal (E119 -> E11.9; 3-char like I10
    stay decimal-free). Import CSV generated by Claude: ICD10_Codes_Import_FY2027.csv.
    Record quota is a non-issue (account was 493/500,000 before load).
  PVS provider field: Provider_ICD10_Codes_Link - Lookup field, source ICD10_Codes,
    display ICD_Display, Multiple selection = Multi Select (set at field CREATION; the
    multi-select option is NOT available on later edit of a lookup). Search felt instant
    live against 74k rows.
  PVS roll-up: Provider_ICD_Print (Single Line) - code-only display ("E11.9, I10"), built
    live by "Provider ICD Print Builder" (On User Input of Provider_ICD10_Codes_Link): loops
    the lookup's selected IDs, queries ICD10_Codes[ID == v_Id], joins ICD_Code. VERIFIED.
    Provider_ICD_Print added to Default Hide On Load disable list (system-built, not typed).
  Partner ICD side: Partner_ICD_Codes free-text field added to Referrals_Main; PVS display
    field + Referral Link Pre-Fill pull/lock lines were drafted but that piece "didn't work"
    on test - PARKED, revisit (the field pull on referral match).
  Chip-style display of both partner + provider codes on the PVS record = PARKED (HTML
    display layer, detail/print view only; report grid renders HTML as literal text).

CREATOR DELUGE LEARNING (insert syntax) - important, cost a lot of trial/error today.
  In a Creator Deluge INSERT block, field assignments use "=", NOT ":".
    insert into Form [ Field = value  Field2 = value2 ];   // CORRECT
    insert into Form [ Field : value ];                     // WRONG -> "Improper Statement"
    error, misreported at line 1 or 2.
  Also: never include SYSTEM fields (Added_Time, etc.) in an insert -> "System fields cannot
  be updated". Update loops (v_Rec.Field = ...) and the "=" insert form both work in an On
  Success form workflow. The guided "Update record" action is update-only (no upsert) and its
  value boxes reject dynamic input.<field> refs in some spots - use Deluge for upserts.

PARTNER RECOGNITION (capture-once, no portal) - BUILT + VERIFIED LIVE.
  GOAL: stop partners re-entering their POC/org details every referral, WITHOUT paying for a
  Creator portal (Neil declined the ~$100 portal + the SSL/Google-auth dependency).
  DECISION: soft identity keyed on POC EMAIL (referral intake is not the HIPAA-sensitive core;
  partners are known business contacts). No login. Email is the handshake.
  New form: Partner_Referral_Contacts (mirrors billing-contacts pattern; SEPARATE population
  from billing contacts - these are referring people). Fields: Partner_POC_Email (Email,
  No-duplicate ON, the key) + Partner_POC_First_Name / Last_Name / Title / Phone,
  Partner_Organization, Partner_Branch.
  UPSERT workflow "Partner Contact Upsert" (Referrals_Main, On Success / Created): if the POC
  email matches an existing contact, update the 6 fields; else insert a new contact. VERIFIED
  live both paths (Zoho Form submission AND Creator-form submission fired it; created first
  time, updated on repeat email, no duplicate).
  NOT YET WIRED: the return-visit PREFILL. Plan = Zoho Forms dynamic-prefill-via-webhook keyed
  on the email field: partner types email -> webhook looks up Partner_Referral_Contacts ->
  prefills the 6 fields (blank if new). One email field handles both new + returning; no second
  field needed. Build next.

PORTAL / TWO-STEP AUTH THREAD - EXPLORED, then SET ASIDE (Neil dropped the portal).
  Explored a Forms-step-1 -> Creator-login-step-2 flow joined by a token, and confirmed:
  - Zoho Forms cannot authenticate (it captures fields; "login" needs a Creator portal or
    Google/MS sign-in). A CRM form can't authenticate either.
  - Creator native lookup reads a Creator FORM only, not a Zoho Sheet. Creator multi-select
    CHOICE list (like Forms) is manual-import + not Deluge-refreshable -> lookup+form wins.
  - JOIN KEY PROVEN: added a Zoho Forms "Form Token" field (Unique/Random ID, 10-digit,
    Restrict-ID-Repetition ON, hidden). Native Forms->Creator mapping writes it into a
    Referrals_Main Form_Token field. Confirmed live (token 6060233452 landed on REF-1025).
    Forms redirect CANNOT pass the Creator-minted Referral_ID (born after mapping), so the
    token is the durable join key if a step-2 page is ever built.
  - Google OAuth client setup was STARTED in Google Cloud (consent screen done, client half-
    configured: JS origin = https://portal.sosreferrals.com, redirect = the Creator
    .../accounts/pfs/.../clientidpcallback URI). BLOCKED: Zoho has not issued the portal SSL
    yet; OAuth needs https. Parked until the cert lands + only if the portal path is revived.
  NET: current direction is the no-portal email-prefill above; portal/token work is parked but
  documented so it's recoverable.

CARRY-FORWARD FOR NEXT SESSION (2026-07-14):
  1. Wire the return-visit PREFILL: Zoho Forms dynamic-prefill-via-webhook against
     Partner_Referral_Contacts, keyed on Partner_POC_Email. Test new vs returning email.
  2. Partner ICD field on the PVS (pull/lock from Referrals_Main on referral match) - the piece
     that "didn't work" today; revisit.
  3. PVS ID Stamp Generator: STILL OPEN from Session 14 - apply the && / || paren fix, deploy,
     verify; seed "PVS" Sequence_Tracker row @1001; add No-duplicate on PVS_ID; extract into the
     placeholder .dg. (Not touched today.)
  4. Optional: chip-style HTML display of partner + provider ICD codes on the PVS record.
  5. Annual ICD-10 refresh function (small delta upsert; re-runnable; early October) - designed,
     not built.
  6. Extract "Entry Type Section Visibility" live code; fix its stale _INDEX row (carry).
  7. Phone/fax standard (AAA-MMM-LLLL) rollout to the remaining 6 forms (carry).
  8. Cleanup pass: delete the two disabled legacy PVS workflows; retire empty Encounter_RadiologyRequest (carry).

================================================================================
SESSION 16 ADDITIONS (2026-07-14)
================================================================================
PVS ID STAMP GENERATOR - paren fix verified live + extracted (see PVS form section).

RETURN-VISIT PREFILL (partner capture-once, no portal) - BUILT + VERIFIED LIVE.
  Wires the Session 15 Partner_Referral_Contacts store to the public Zoho Form so a
  returning partner's POC/org details auto-fill from their email. No login, no portal.
  MECHANISM: Zoho Forms native Dynamic-Prefill-Webhook on the Email field (partner types
  email, taps the inline search icon, mapped fields populate). Forms webhook -> a Creator
  Custom API -> Deluge lookup on Partner_Referral_Contacts by email -> returns the 7 fields
  as JSON (blanks if no match = new partner).
  functions/get_partner_referral_contact.dg - standalone function, Default namespace, return
    type Map, one String arg pPocEmail. Queries Partner_Referral_Contacts[Partner_POC_Email ==
    email], returns First/Last/Title/Phone, Organization, Branch, Team (Partner_POC_Team added
    mid-build). extraction: DONE 2026-07-14 | verified: YES (live prefill test passed).
  CREATOR CUSTOM API "Get Partner Referral Contact" (link name get_partner_referral_contact):
    Microservices > Custom API. GET, OAuth2, User scope Admin only, Argument Type Key-and-Value
    (param key pPocEmail = the function arg), Response STANDARD, bound to the function above.
    Endpoint: www.zohoapis.com/creator/custom/sosmmc/Get_Partner_Referral_Contact.
    Uses existing Zoho Forms connection sos_creator_connection (scopes Zohocreator.customapi.
    EXECUTE + ZohoCreator.report.READ, both present).
  RESPONSE SHAPE LEARNING: Creator Custom API "Standard" response WRAPS the function's Map under
    a "result" key (plus "code":3000). So the Forms prefill mapping paths are /result/<Field>,
    not top-level. Confirmed live via the wizard's Test & Verify.
  ZOHO FORMS SIDE (config, no repo file): Prefill-Webhook field = the Email field; URL param key
    pPocEmail -> Partner POC Email; 7 field mappings /result/<Field> -> the form fields. Note (UX):
    the trigger is a small inline magnifying-glass icon; a Note element/instruction above the field
    is planned to draw attention (deferred; branded PNG asset belongs to SOS Design).
  UPSERT WRITE SIDE - Partner Contact Upsert (Referrals_Main, On Success/Created) now writes all 7
    fields incl. Partner_POC_Team on BOTH branches (update loop via v_Rec.Field= ; and insert). Full
    chain verified live 2026-07-14: Zform -> Referrals_Main -> upsert -> Partner_Referral_Contacts,
    then prefill reads it back.
  ROOT-CAUSE LEARNING (cost time today): a non-choice value assigned to a DROPDOWN field aborts the
    ENTIRE workflow (all-or-nothing) - nothing after it commits, insert included. Partner_POC_Title on
    Partner_Referral_Contacts was a Dropdown with placeholder choices (Choice 1/2/3); the upsert set it
    to "PA"/"RN" (not a listed choice) and the whole write silently failed. FIX: keep passive-store
    fields Single Line, or make the choice set match the source. Symptom to remember: "all fields present
    in source, nothing writes downstream" = one bad field assignment aborting the workflow.
  OPEN / WATCH:
  - Added_User = zoho.loginuser in the insert returns the ORG NAME, not a person, and is empty on the
    Zoho Form integration path (no logged-in user). Harmless if it's just a system stamp; revisit if it
    was meant to capture the submitter (would need a different source).
  - Email match is exact (Creator ==). If stored vs typed case differs, no match. Lowercase-
    normalize on both the upsert (write) and this function (read) if live emails prove inconsistent.
    Not applied yet - left until a real mismatch appears.
  - Exposure (accepted): lookup key is the partner's own email, so any partner could type another
    partner's email and see that POC's business-contact details. Non-PHI (Partner_Referral_Contacts
    holds no patient data); partners are known contacts. Accepted, not mitigated.

APP EXPORT + SYNC TOOL (2026-07-14) - major infrastructure.
  DISCOVERY: Settings > Application IDE > Export produces a .ds file = the WHOLE app definition
  (forms + fields + every workflow/function Deluge), definition-only (no record data / PHI; the 47
  "data" hits are all `personal data = true` field flags). This is authoritative LIVE truth and ends
  the manual paste-from-live relay. IMPORT of a .ds CREATES A NEW APP (clone) - it does NOT patch the
  live app in place - so .ds is a mirror + dev-clone tool, not a production deploy. Import lives under
  Solutions > Create Solution > Applications > Import from file (NOT in the IDE).
  tools/ds_sync.py - reconciles a .ds against the repo .dg files. Dry-run report per item
  (MATCH / DRIFT / NEW / EMPTY / AMBIGUOUS); --apply writes DRIFT + NEW only. SAFETY: never writes
  EMPTY or AMBIGUOUS (incl. target collisions where two live sources map to one repo file), so a
  mis-map can't clobber. Compare is whitespace-insensitive (Deluge nesting is braces, not indent).
  Run in Claude Code: python3 tools/ds_sync.py --ds SOS_Referrals_App.ds --repo . [--apply].
  KEY LESSON: DRIFT DIRECTION IS NOT ALWAYS live->repo. Decide per item. First reconcile (2026-07-14)
  found ~35 old Session 4-6 generators/functions repo-stale (safe to pull), BUT PVS_Stamp_Generator and
  Referral_Link_Pre_Fill were repo-AHEAD (repo correct, live behind - see below). Blanket --apply would
  have regressed the archive. NOT applied yet.
  EXTRACTED FROM THE EXPORT (were PENDING placeholders, now DONE + verified - see PVS form rows):
  OnLoad__Provider_PreFill, OnUserInput__Diversion_Tracking__Show_Hide, OnUserInput__Additional_Charges__Show_Hide.
  DRIFT FINDINGS TO RESOLVE (repo-ahead; push repo->live, do NOT pull):
  - PVS_Stamp_Generator: live lacked the guard fix -> RE-FIXED live this session as nested ifs, verified
    on edit/re-submit (see PVS_Stamp row). Repo + live now agree.
  - Referral_Link_Pre_Fill: RESOLVED 2026-07-14 - dropped `hide System_Fields_Section;` from repo to match live (redundant; Default Hide On Load already hides it on load). Repo + live agree.
  NEW rows that are actually existing files under non-conforming names (rename repo files, do NOT create
  dupes): ShowHide_Facility_block.dg; Assignments/OnUserInput__Assignment_Pull_From_Referral.dg (missing
  the Referral_Link token); Employees/OnLoadAndOnInput__Employee_Term_Date_Visibility.dg. Genuine NEW (safe
  to create): Provider_ICD_Print_Builder + schema-monitor fns (run_schema_monitor, seed_schema_to_github,
  test_github_commit, test_schema_connection).
  AMBIGUOUS collisions surfaced (never written): (1) Assignments OnLoad - Assignment_Lock_Immutable vs the
  facility show/hide block (non-conforming filename); (2) PVS Has_Referral_ID - Has_Referral_ID_Show_Hide
  vs the DISABLED-legacy Patient_Fields_Editability_Toggle (delete it live -> collision clears); (3)
  Partner_Rates OnSuccess - the empty native stamp vs Partner_Rate_Stamp_Generator; (4) Partners OnSuccess -
  PAR_ID_Generator vs a STRAY Partner_Rate_Stamp workflow misplaced on the Partners form (investigate).
  log_change: confirmed live body is genuinely EMPTY (Creator logs errors only) - not an export gap; the
  tool's EMPTY guard correctly leaves the repo copy alone.

EXAM ORDERS + EXAM_CATALOG (2026-07-14) - see context/14_exam_orders_and_catalog.md.
  DECISION: X_Ray_Orders repurposed as a SELF-AUTHORED diagnostic imaging order (X-ray + ultrasound
  + cardiac), NOT a routing destination for order-only referrals (that model dropped). On submit:
  mint order ID -> generate hard-copy PDF -> attach to the order + linked referral -> auto-fax to the
  imaging vendor. Patient/referral/partner pull-lock from Referral_Link (Referral_ID + partner live on
  the order, never on the reference tables).
  TRANSMIT = FAX-FIRST: vendors have no API; they take orders by portal + fax; only one accepts our own
  PDF. Assume all accept fax -> one SRFax path (fax the PDF to the vendor fax on file) covers every
  vendor. Submit always generates the PDF regardless. Portal auto-entry = later OPTIONAL browser-agent
  job. Planned vendor directory form: name, fax, email, accepted-format (our PDF vs portal), portal URL,
  active; lookup on the order so the fax destination travels with the selection.
  EXAM_CATALOG reference form - BUILT + VERIFIED LIVE (59 rows). Fields: Exam_Code (Single Line,
  No-duplicate ON = unique key), CPT_Code (Single Line TEXT; holds dual codes e.g. 76641/76642),
  Exam_Description, Exam_Display ("71046 - Chest AP/LAT 2 View", the lookup search/display field),
  Modality (Radio X-Ray/Ultrasound/Cardiac), Body_Region (Single Line), Laterality_Applicable
  (Radio Yes/No), Status (Radio Active/Retired, initial Active). DATA: 59 exams (37 X-Ray, 18 US,
  4 Cardiac) curated from the XR Mobile order form study list; NOT a full CPT set (no CT/MRI/NM/PET/
  mammo/fluoro/DEXA). Import CSV generated by Claude: Exam_Catalog_Import.csv (seed artifact, NOT
  committed - same handling as the ICD CSV). CPT_Code is NOT unique (Renal+Bladder 76770; Venous
  Upper/Lower 93970/93971) -> Exam_Code is the key. One row per exam + Laterality_Applicable flag
  (25 Yes); NOT exploded into L/R/Bilat rows. Mirrors ICD10_Codes (reference table + multi-select
  lookup + print rollup); no workflows on the form.
  CARRY (order wiring, pending): Ordered_Exams_Link on X_Ray_Orders (Lookup -> Exam_Catalog, display
  Exam_Display, Multi Select set at CREATION) + Ordered_Exam_Print rollup (On User Input, mirror
  Provider_ICD_Print, add to Default Hide On Load); reuse the ICD-10 lookup for indications; PDF gen +
  attach + SRFax auto-fax (engine: Creator print/merge vs Lambda - decide at wire time); laterality per
  exam (subform vs exploded rows vs note - decide at wire time); full order field superset in context/14.

IMAGING_ORDERS FORM (2026-07-14, Session 17) - X_Ray_Orders rebuilt + renamed. See context/14 section 6.
  X_Ray_Orders RENAMED to Imaging_Orders (rename rewrites inbound connections). All legacy fields
  deleted; rebuilt fresh section by section. BUILT + verified: S1 Order Details (Referral_Link display
  "Referral_ID - Patient_Full_Name", Order_Date, Order_Priority Radio Routine/STAT, Order_Status Radio
  Draft/Sent initial Draft), S2 Patient (pull-lock fields; ALL phones Single Line to match the Zoho-Form
  text source; Facility_Room_Number is the live name, not Patient_Room_Number; Patient_MBI manual - no
  referral source yet; DM_Full_Name + DM_Phone), S3 Insurance (manual), S4 Provider Details fields
  (Provider_Name, Provider_NPI, Employee_Phone; dropped manual signature lookup + Signature_Date, use
  Added Time). SPECCED not built: S5 Exam & Clinical (Ordered_Exams_Link multi->Exam_Catalog +
  Ordered_Exam_Print rollup, Order_ICD10_Codes_Link multi->ICD10_Codes + Order_ICD_Print rollup,
  Other_Exam, Reason_For_Study, Reason_For_Portable, Special_Instructions), S6 Vendor & Transmit
  (Imaging_Vendor_Link->Imaging_Vendors [form TBD], Order_PDF, Send_Results_To, Results_Return_Fax/Email).
  ORDER_STATUS: Draft/Sent only; flips to Sent ONLY on SRFax success inside the fax function; failure ->
  Transmit_Error + Last_Transmit_Attempt, stays Draft; success -> Order_Sent_Time. Manual re-send first.
  PROVIDER AUTO-RESOLVE (locked, not written): provider = logged-in user. Match Employees[Employee_Email
  == zoho.loginuserid] AND Employee_Status=="Active". Covers admins (@sosmmc.com) + portal providers
  (@sosreferrals.com) since Employee_Email = login email for all. Active gate is the guard (a departed
  user still matching could sign a live order). On Load stamps name/NPI/phone read-only; On Validate
  blocks inactive/missing with "Your provider profile is inactive or not found. Contact an admin."
  CARRIES: resolver workflows; add Provider_NPI to Employees + backfill; add DM_Full_Name concat +
  backfill on Referrals_Main; build S5/S6 fields + the two rollups + the patient pull-lock (explicit
  DM_Phone map); build Imaging_Vendors form; confirm portal read on Employees; wire PDF + SRFax; decide
  laterality; rename ID fields + add Sequence_Tracker prefix/mint; rename repo folder X_Ray_Orders ->
  Imaging_Orders.

SESSION 18 (2026-07-16, covers Jul 15-16) - provider resolver, PVS X-ray, PVS PDF, fax book, SendGrid.
  See context/15_pvs_pdf_fax_email.md. Highlights:
  PROVIDER RESOLVER on Imaging_Orders - BUILT + VERIFIED. On Load "Imaging Order Provider Stamp" matches
  Employees[Employee_Email==zoho.loginuserid && Employee_Status=="Active"], sets the LOOKUP
  Provider_Signature_Link = v_Emp.ID (not a text name field), stamps Provider_NPI + Employee_Phone,
  disables them. On Validate (Create+Edit) "Imaging Order Provider Gate" blocks inactive/missing with
  "Your provider profile is inactive or not found. Contact an admin." Provider_NPI added to Employees.
  DELUGE LEARNING: NO typed var declarations in body (`string v_X=` throws Improper Statement); untyped only.
  PVS VISIT X-RAY GROUP - fields BUILT (reveal workflow CARRY). SOS orders x-rays (vendors perform); PVS
  documents the ORDER only; results go in the addendum (PVS locks at finalize). New group gated by
  Type_of_Entry=Patient Visit: Visit_XRay_Section, XRay_Ordered_This_Visit (Radio No/Yes), Visit_XRay_Type,
  Visit_XRay_Order_Date, Visit_XRay_Indication (last 3 Default Hide On Load). Separate from Group A
  (referral-inbound Reason_for_X_Ray_Request) and Group B (X-Ray Only, gated by Type_of_Entry=X-Ray Order).
  PVS -> PDF - template BUILT (gen+storage CARRY). Creator Record/Print Template (NOT Zoho Forms editor).
  Field map in PVS_PDF_Field_Map.md, HTML in PVS_template_full.html. SOAP stays a SINGLE field
  (Final_Clinical_Note). PVS PDF is single-purpose (Patient Visit note only); orders are their own docs.
  PVS record = universal audit event. Finalize locks (portal read-only = the lock) + generate + store in
  WorkDrive + redirect to ONE send console (PVS lookup OR upload; fax via Fax_Address_Book/manual + email
  to referral contact; re-sends; send log). Generate-once-store (PDF credit limits).
  FAX_ADDRESS_BOOK - BUILT + SEEDED. Shared flat directory for ALL faxes; NOT linked to Partners (vendors
  are never partners). Fields: Recipient_Name, Fax_Number (Single Line raw digits), Recipient_Category
  (Radio Hospice/PACE/Clinic/Hospital/Vendor/Group/Contact), Recipient_Status, Recipient_Notes (user only).
  Seed Fax_Address_Book_Import.csv, 33/37 filled by name-match; 4 need manual numbers.
  SENDGRID EMAIL - BUILT + VERIFIED. sosreferrals.com SendGrid-authenticated (SPF/DKIM/DMARC). Sends AS
  notifications@sosreferrals.com; Cloudflare routes that -> neil.heird@sosmmc.com; Zoho Mail dropped.
  Connection sendgrid_connection (built-in; Test button fails on all custom connections here, a real send
  is the test). NEW reusable functions/send_via_sendgrid.dg (v3 mail/send, text/html) - VERIFIED. Rewrote
  run_schema_monitor: all 5 Zoho sendmail -> send_via_sendgrid (now archived; was never in repo). ROOT
  CAUSE of no-email: Zoho sendmail needs an approved SENDER (sosmmc has approved domains, no senders) so
  it silently dropped; SendGrid bypasses it. Also: sendmail `from` email must be a QUOTED string.
  REPO WRITES: context/15_pvs_pdf_fax_email.md (new), _INDEX.md (this block), functions/send_via_sendgrid.dg
  (new), functions/run_schema_monitor.dg (new - place the presented SendGrid version). Not committed:
  PVS_template_full.html, PVS_PDF_Field_Map.md, Fax_Address_Book_Import.csv (working/seed artifacts).

================================================================================
SESSION 20 ADDITIONS (2026-07-21) - PVS form hardening + finalize-lock
================================================================================
All items below verified LIVE by Neil and mirrored into the repo. Ground truth =
.ds exported 2026-07-21 19:31. Live workflow inventory: context/19.

FORM: Encounter_PatientVisit
  Encounter_PatientVisit/OnLoad__Invoice_Status_Lock.dg   *** NEW ***
    trigger: On Load (Created or Edited) | live name "Invoice Status Lock" | extraction: DONE 2026-07-21 | verified: YES
      FINALIZE-LOCK. Locks the medical record when Clinical_Note_Type == "Final"; the nine
      charge/cost-driver fields (Complexity_Level, Additional_Charges, Complexity_Charge,
      After_Hours_Fee, Super_Stat_Fee, Equipment_Charge_Amount/Details, Other_Charges_Amount/
      Details) stay EDITABLE so pricing can be set after the note. A nested if also locks those
      nine once Invoice_Status == "Final" (written later by the invoice flow; nothing sets it
      today). Clinical_Note_Type is deliberately NOT disabled so Final can become Addendum.
      TIMING: on load, not on submit - choosing Final does not lock the open form; the record is
      locked the next time it opens. Accepted for launch.
  Encounter_PatientVisit/OnUserInput__Patient_Location__Facility_Show_Hide.dg   *** NEW ***
    trigger: On User Input (Patient_Location) | live name "Facility Fields Show Hide" | verified: YES
      Shows Facility_Name/Phone/Room_Number only when Patient_Location == "Facility". Three
      touchpoints total: this handler, Default Hide On Load (hidden by default), and Referral
      Link Pre-Fill (reveal on pull, since a programmatic set does not fire on-user-input).
  Encounter_PatientVisit/OnUserInput__Patient_Last_Name__Build_Display_Name.dg   *** NEW ***
    trigger: On User Input (Patient_Last_Name) | live name "Build Patient Display Name" | verified: YES
      Builds Patient_Display_Name from First + MI + Last on the walk-in path.
  Encounter_PatientVisit/OnLoad__Provider_PreFill.dg   [UPDATED]
      Now also builds Employee_Full_Name (First Last) and Employee_Name_Title (First Last, Title)
      from the pulled parts. NEW PVS field Employee_Name_Title is the single displayed signature
      line; granular employee fields hidden. Signature reads "Joshua Kolanko, APRN".
      NOTE: the print template renders ${Employee_Full_Name} ${Employee_Title}, so Full_Name must
      stay NAME ONLY or the credential prints twice.
  Encounter_PatientVisit/OnLoad__Default_Hide_On_Load.dg   [UPDATED]
      Hides Imaging_Orders_Section; shows Employee_Name_Title and hides the granular employee
      fields; locks the six referral-context fields + Partner_ICD_Codes when Has_Referral_ID ==
      "Yes"; disables Type_of_Entry on load when Has_Referral_ID == "No" (reopened walk-in stays
      locked to Patient Visit).
  Encounter_PatientVisit/OnUserInput__Has_Referral_ID__Show_Hide.dg   [UPDATED]
      WALK-IN GATING. On "No": sets Type_of_Entry = "Patient Visit" and disables it, then reveals
      the Patient Visit sections and hides the seven referral-context fields (Partner_ICD_Codes,
      Goals_of_Care, Additional_Information, General_Files_Upload, List_Patient_Allergies,
      List_Patient_Anticoagulants, Advanced_Directives_Details). On "Yes": enables Type_of_Entry
      and shows those seven.
      WHY auto-set-and-lock: Deluge cannot hide individual dropdown options, and the walk-in set
      is exactly one option (Patient Visit). 3008 / Lab Order / Imaging Order are referral-only.
      ORDERING GOTCHA: the two Type_of_Entry lines must sit at the TOP of the No branch. Placed
      after the ~30 null-assignments they never ran (a snag upstream stops the branch).
      COUPLING: this branch carries its OWN copy of the Patient Visit section list, because Entry
      Type Section Visibility does NOT fire on a programmatic Type_of_Entry set. If that section
      list changes, update it in BOTH workflows.
  Encounter_PatientVisit/OnUserInput__Referral_Link__PreFill.dg   [UPDATED]
      Now also pulls the clinical context: Reason_for_Referral (from referral field
      Referral_Reason - the ONLY renamed mapping), plus Goals_of_Care, List_Patient_Allergies,
      List_Patient_Anticoagulants, Advanced_Directives_Details, Additional_Information (same link
      names). Disables them on a found referral; nulls + enables on deselect. Also sets
      Patient_Display_Name from Patient_Full_Name, and reveals facility fields when the pulled
      Patient_Location == "Facility".
  Encounter_PatientVisit/OnUserInput__Type_of_Entry__Section_Visibility.dg   [UPDATED]
      Full build for all types + else. Manages Referral_Details_Section (clinical context) per
      type and the new Imaging_Orders_Section (shown ONLY on Imaging Order). 3008 shows only
      Cares_3008_Completion_Section - no charge sections, because 3008 is FLAT RATE (priced from
      Partner_Rates Rate_Type "Cares 3008 Assessment" at invoice time, not from PVS charge fields).

FORM: Referrals_Main
  Referrals_Main/OnUserInput__Patient_Address__Build_Full_Address.dg   *** NEW ***
    trigger: On User Input (Patient_Address) | verified: YES
      Concatenates the address subfields into the new plain-text field Patient_Full_Address
      (line1, line2, city, state, zip; country omitted) for single-line display elsewhere.
  Referrals_Main/OnUserInput__DM_Last_Name__Build_DM_Full_Name.dg   *** NEW ***
    trigger: On User Input (DM_Last_Name) | verified: YES
      Builds DM_Full_Name from DM_First_Name + DM_Last_Name. Closes the long-standing
      "DM_Full_Name exists but has no generator" gap. BACKFILL FOR EXISTING ROWS STILL OPEN.
  Referrals_Main/OnLoad__Default_Hide_On_Load.dg   *** NEW ***
    trigger: On Load (Created or Edited) | verified: YES
      Hides Patient_Full_Address (system-built, not typed). First on-load workflow on this form.

SCHEMA CHANGES THIS SESSION
  ADDED (PVS): Billing_Branch (Lookup -> Partner_Locations, display Partner_Location_Name, in
    System_Fields_Section, hidden, NO form filter), Employee_Name_Title, Patient_Display_Name,
    and the new Imaging_Orders_Section (Imaging_Orders, Imaging_Order_Indication,
    Upload_Imaging_Order_Files, Imaging_Ordered_Date).
  ADDED (Referrals_Main): Patient_Full_Address.
  DELETED (PVS): X_Ray_Section, Lab_Section, old Imaging_Order_Section, Visit_XRay_Section (empty),
    Patient_Full_Name1 (duplicate), XRay_Ordered_This_Visit (orphan), and the old Lab_Section
    fields (Reason_for_Lab_Request, Requested_Lab_Vendor1, Upload_Lab_Request_Files).
  RENAMES: section Referral_Details_Section (top lookup) -> Referral_Lookup_Section, and the old
    Referral_Details_Section1 (clinical context) -> Referral_Details_Section (a SWAP - the name
    Referral_Details_Section now points at the clinical-context section). Section
    Lab_Order_Section -> Lab_Orders_Section. Type_of_Entry option "X-Ray Order" -> "Imaging Order".
  BILLING_BRANCH NOTE: no form filter is set because the PVS carries Partner_Organization as TEXT
    while Partner_Locations references its partner via the Partner_Link LOOKUP - there is no
    matching text field to filter on. Partner scoping is deferred to the approval dashboard in
    Deluge (query Partner_Locations by Partner_Link). The field is hidden and set by import or
    the dashboard, never by a provider, so an unfiltered lookup on the form is harmless.

CREATOR / DELUGE LEARNINGS (cost real time today)
  1. DUPLICATE WORKFLOW, SAME NAME. An earlier create/delete cycle left TWO workflows named
     Invoice_Status_Lock. The visible copy showed Disabled while the second stayed ENABLED, so the
     whole PVS rendered read-only on new records and toggling the visible one changed nothing.
     Ruled out cache, incognito, and permissions before finding it. LESSON: if a workflow behaves
     as though it is running while showing Disabled, scan the FULL list for a duplicate name
     before suspecting field properties or permissions. When rebuilding, DELETE rather than
     disable.
  2. hide / show / enable / disable are valid ONLY in on-load actions. In an on-validate or
     on-success workflow they throw "'disable' can be used only in on load actions". Corollary:
     a finalize LOCK must live on load; only the value-setting can live elsewhere.
  3. FORMULA FIELDS compute on SAVE, not live during entry, and cannot be written by a workflow.
     Tried a formula for Patient_Display_Name, reverted to a plain field + workflow so the value
     appears live like Patient_Full_Name.
  4. Deleting a section makes Creator silently STRIP that section's references out of every
     workflow. Nothing dangles, but the replacement section is wired to nothing - after any
     section rebuild, re-add it to the on-load and visibility workflows by hand.
  5. A field referenced by a report cannot be cleanly deleted - repoint the report column first
     (hit while removing the duplicate Patient_Full_Name1, which fed two report columns).

STATUS VS THE 8/3 LAUNCH PLAN (context/18)
  7/17, 7/18, 7/19 complete. 7/20 mostly done: finalize-lock now BUILT (was the main gap),
  DM_Full_Name generator done but BACKFILL OPEN, two legacy cleanups still open. 7/21 JULY IMPORT
  PATH NOT STARTED - roughly one day behind on that item. Test 1 still 7/26, launch still 8/3.

OPEN / NEXT
  1. July import path (behind): mapping design, template + transforms, backfill plan. Cognito
     export + charge columns + billing branch -> PVS, one row per visit.
  2. Backfills: DM_Full_Name and Patient_Full_Address on existing referrals.
  3. Cleanups: delete the DISABLED legacy "Patient Fields Editability Toggle" (also clears an
     ds_sync AMBIGUOUS collision); confirm + remove the stray "Partner Rate Stamp Generator"
     bound to the Partners form.
  4. Referral_Partner_Section question Neil flagged - still unraised.
  5. Then Books setup, invoice engine, approval dashboard per context/18.
