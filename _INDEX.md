# SOS EMR Code Archive - Master Index

Last updated: June 27, 2026
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
    trigger: On Success (Created) | per docs: WORKING (verified live June 26) | extraction: DONE 2026-06-26 | verified: YES (matches live)
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
  Partner_Locations/OnValidate__LOC_Required_Codes.dg
    trigger: Validation on submit (Created) | per docs: PROVEN | extraction: DONE 2026-06-27 | verified: YES (matches Session 4 export)
  Partner_Locations/OnValidate__Primary_Office_OnePerPartner.dg
    trigger: Validation on submit (Created or Edited) | per docs: PROVEN | extraction: DONE 2026-06-27 | verified: YES (matches Session 4 export)

FORM: Partner_Rates   [Session 4, 2026-06-27]
  Partner_Rates/OnSuccess__Partner_Rate_Stamp_Generator.dg
    trigger: On Success | per docs: BUILT (live test pending) | extraction: DONE 2026-06-27 | verified: YES (matches Session 4 export)

FORM: Partner_Billing_Contacts   [Session 4, 2026-06-27]
  Partner_Billing_Contacts/OnSuccess__Partner_Billing_Contact_Stamp_Generator.dg
    trigger: On Success | per docs: BUILT (live test pending) | extraction: DONE 2026-06-27 | verified: YES (matches Session 4 export)

  PENDING (do NOT make live until backfill + REF tested):
  Referrals_Main/OnSuccess__REF_ID_Generator.PENDING.dg
    note: Session 4 retrofit target. Replaces the June 26 inline REF generator with
    a one-liner that calls mint_referral_id(input.ID), then run backfill_referral_ids().
    The current live REF_ID_Generator.dg (above) stays canonical until this is tested.

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
    sig: mint_referral_id(int recId) | per docs: ADDITIVE (not wired live yet) | extraction: DONE 2026-06-27 | verified: YES (matches Session 4 export)
    REF-seq
  functions/backfill_referral_ids.dg
    sig: backfill_referral_ids() | per docs: ADDITIVE | extraction: DONE 2026-06-27 | verified: YES (matches Session 4 export)
    sweep

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
        Partner_Link). The v1.2 suffix and T011 formats are dead. The June 26 inline
        REF_ID_Generator stays canonical until the Session 4 mint_referral_id retrofit
        is tested. Read context/07 and NOTE 8 before any ID or sequence work.

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
        OPEN / next session:
        - Report: add Partner Code column to Partner_Locations Report, group by partner
        - Auto-demote primary on new Primary_Office=Yes
        - Lock Partner_Link after creation (UI read-only on edit + validation backstop)
        - Live-test stamp generators; run backfill sweeps (LOC, PAR); idempotency check
        - REF retrofit: REF On Success calls mint_referral_id(input.ID), then backfill

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
