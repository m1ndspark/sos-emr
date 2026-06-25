# SOS EMR Code Archive — Master Index

Last updated: June 25, 2026
Source of truth: the live Zoho Creator app. This archive mirrors it.
Sync method: manual. When a workflow is verified working in Creator, paste the
exact Deluge into its .dg file and update the EXTRACTION and VERIFIED columns.

Rule: .dg files hold pure Deluge only, no comment headers, so they round-trip
cleanly back into Creator. All status and metadata live here, not in code files.

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
  Referrals_Main/OnUserInput__Decision_Maker_Phone__Format.dg
    trigger: On User Input  | per docs: WORKING (live) | extraction: DONE 2026-06-25 | verified: YES (copied from live)
  Referrals_Main/OnUserInput__Patient_SSN__Format.dg
    trigger: On User Input  | per docs: WORKING         | extraction: PENDING | verified: NO
  Referrals_Main/OnUserInput__Patient_Phone__Format.dg
    trigger: On User Input  | per docs: BLOCKED (Zoho Forms raw value unknown) | extraction: PENDING | verified: NO
  Referrals_Main/OnUserInput__Facility_Phone__Format.dg
    trigger: On User Input  | per docs: WORKING (live) | extraction: DONE 2026-06-25 | verified: YES (copied from live)
  Referrals_Main/OnUserInput__Partner_POC_Phone__Format.dg
    trigger: On User Input  | per docs: WORKING (live, aka "Referral Partner POC Phone Format") | extraction: DONE 2026-06-25 | verified: YES (copied from live)

FUNCTIONS (Functions tab, standalone)
  functions/fn_resolveUserIdentity.dg
    per docs: DESIGNED (Apr 18, 2026), confirm whether deployed | extraction: PENDING | verified: NO

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

NOTE 4  Object ID format. May 7 v1.2 reference is authoritative (per-object
        counters from 1001, no date embedded). The older T011 format (global
        counter from 1313, date embedded) is deprecated. Confirm against live
        stamp generators.

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
