# SOS EMR Code Archive - Master Index

Last updated: June 29, 2026
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
    trigger: On Load        | per docs: WORKING         | extraction: PENDING | verified: NO
  Encounter_PatientVisit/OnLoad__Default_Hide_On_Load.dg
    trigger: On Load        | per docs: WORKING         | extraction: PENDING | verified: NO
  Encounter_PatientVisit/OnUserInput__Has_Referral_ID__Show_Hide.dg
    trigger: On User Input  | per docs: WORKING         | extraction: PENDING | verified: NO
  Encounter_PatientVisit/OnUserInput__Referral_Link__PreFill.dg
    trigger: On User Input  | per docs: BUILT, UNTESTED | extraction: PENDING | verified: NO
  Encounter_PatientVisit/OnUserInput__Type_of_Entry__Section_Visibility.dg
    trigger: On User Input  | per docs: WORKING         | extraction: PENDING | verified: NO
  Encounter_PatientVisit/OnUserInput__Diversion_Tracking__Show_Hide.dg
    trigger: On User Input  | per docs: WORKING         | extraction: PENDING | verified: NO
  Encounter_PatientVisit/OnUserInput__Additional_Charges__Show_Hide.dg
    trigger: On User Input  | per docs: WORKING         | extraction: PENDING | verified: NO
  Encounter_PatientVisit/OnSuccess__PVS_Stamp_Generator.dg
    trigger: On Success     | per docs: WORKING (Script 011) | extraction: PENDING | verified: NO

FORM: Referrals_Main   [live form has 5 On-User-Input formatters; see NOTE 6]
  Referrals_Main/OnSuccess__REF_ID_Generator.dg
    trigger: On Success (Created) | per docs: PROVEN (LIVE; retrofit complete 2026-06-27, body now calls mint_referral_id(input.ID), supersedes old inline) | extraction: DONE 2026-06-27 | verified: YES (matches Session 4 export)
  Referrals_Main/OnSuccess__Patient_Full_Name_Generator.PENDING.dg
    trigger: On Success (Created or Edited) | per docs: PENDING (staged, not live; concat First+MI+Last -> Patient_Full_Name, blank-aware) | extraction: DONE 2026-06-27 | verified: YES (matches Session 4 export)
    note: CONFIRM the four field link names (Patient_First_Name, Patient_MI, Patient_Last_Name, Patient_Full_Name) before enabling; rename off .PENDING when live.
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
        harmless. The 4 phone formatters share one pattern: guard on "(", strip to
        digits, take the last 10, reformat to (AAA) MMM-LLLL.

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
