# SOS Module - PVS (Patient Visit Summary) Design

Working design decisions for the PVS object/form. In progress (field review not
complete). Started 2026-07-03 (Session 8). Live form: "PVS" (repo folder still
named Encounter_PatientVisit; NOTE 1 rename pending). Spec source: uploaded
sos-referral-form-fields.xlsx, tab "Sheet2".

--------------------------------------------------------------------------------
PLATFORM DECISION - PVS = NATIVE CREATOR PORTAL FORM (not Zoho Forms)
--------------------------------------------------------------------------------
Reason: the PVS must (a) prepopulate ALL patient info AND all provider info, with
only the visit-documentation fields open, and (b) be a SIGNED clinical note.
- Auto-filling provider info requires knowing WHO the provider is -> authentication.
- A signed clinical note must be attributable to an authenticated author (legal/audit).
- Provider must see patient data LIVE while documenting -> Creator lookup pull.
Zoho Forms can't know the Creator portal user or show live Creator data, so it can't
do provider auto-fill or a live patient pull. Native Creator (portal) form it is.
Trade accepted: Creator conditional show/hide (Deluge) is more work than Zoho rules.

WHY PVS NEEDS AUTH BUT THE REFERRAL FORM DOESN'T:
- Referral form = COLLECTS data the submitter already has (no auth needed; BAA covers it).
- PVS = DISCLOSES an existing patient record (prefilled) + must be signed -> auth required.

--------------------------------------------------------------------------------
TWO PVS CREATION METHODS (same underlying pull)
--------------------------------------------------------------------------------
1. Portal user opens PVS, selects the referral via Referral_Link lookup
   (display = Patient_Full_Name + Referral_ID + Referral_Date; searchable by name or
   REF id; ideally filtered to referrals assigned to that provider). Selection fires
   the On-User-Input pull.
2. Referral email has a custom BUTTON that opens the PVS pre-filled.
   - Email must be sent FROM CREATOR (On Success), not Zoho Forms, so it can embed the
     referral's ID and build the deep link. (Zoho Forms doesn't know the Creator REF id.)
   - Deep link carries the Referral_ID ONLY (PHI-safe: REF-#### has no PHI by design).
     Creator resolves patient/provider server-side / on load. NEVER put patient PHI in the URL.
   - PVS is a PORTAL (authenticated) form; button routes through login.
VERIFY at build time: exact Creator URL-prefill syntax for a portal form (don't guess).

--------------------------------------------------------------------------------
TWO PULLS TO BUILD (not built yet)
--------------------------------------------------------------------------------
A. Patient + Referral Partner, from the linked referral. Trigger: On User Input of
   Referral_Link (method 1) AND On Load reading the URL param (method 2). Fetch
   Referrals_Main[ID == Referral_Link], copy fields, then LOCK them read-only.
   Proposed map (Referrals_Main -> PVS), CONFIRM link names:
     Patient_First_Name/MI/Last_Name/DOB/Gender -> same
     Patient_Address (composite) -> Patient_Address
     Referral_ID -> (feeds PVS_ID + stored)          Referral_ID_Stamp -> Referral_ID_Stamp
     Partner_Organization -> Referral_Partner        Partner_Branch -> Referral_Branch
     Partner_POC_Team -> Referral_Team               Partner_POC_First/Last/Title -> PR_POC_First/Last/Title
     Partner_ID -> Partner_ID                        Partner_ID_Stamp -> Partner_ID_Stamp
B. Provider, from the logged-in portal user. Trigger: On Load. zoho.loginuser (email)
   -> fetch Employees record -> fill Employee_First_Name/Last_Name/Title (+ Initials), lock.
   CONFIRM: Employees email link name + first/last/title link names; Initials pulled or derived.

--------------------------------------------------------------------------------
PVS_ID SCHEME (DECIDED)
--------------------------------------------------------------------------------
- Referral-linked PVS: PVS_ID = "PVS-" + Referral_ID (e.g. PVS-REF-1234).
  A detected SECOND Final PVS on the same referral -> append -v2 (third -v3, ...).
  (A 2nd Final PVS is rare - most changes use an ADDENDUM (ADR object). It must link to
   the original referral.)
- Walk-in / manual PVS (Has_a_Referral_ID = No, no referral): generate own sequential ID
  PVS-1001-M ... from the PVS row in Sequence_Tracker. "M" = manually created (M-marker).
- Objects need ID + ID Stamp: ADD PVS_ID_Stamp (spec only had PVS_ID). PVS_ID_Stamp = native rec ID.
- PVS_Referral_ID field: DO NOT DELETE. Redundant on paper but LOAD-BEARING - referenced by
  4 workflows incl. PVS Stamp Generator (which builds PVS_ID from it) + referral show/hide.
  Keep it as the working field that stores the referral's ID and feeds PVS_ID. (Creator blocks
  deletion until refs are removed; reworking the ID generator isn't worth the risk.)
  OPEN: review the PVS Stamp Generator to confirm exactly how PVS_ID is built.
- SESSION 14 UPDATE (2026-07-12) - PVS_ID + PVS_Referral_ID FORMAT FINALIZED, supersedes the two
  format bullets above. Live "PVS ID Stamp Generator" (On Success) now mints from a SINGLE shared
  PVS sequence (Sequence_Tracker Object_Prefix "PVS"), incrementing across BOTH paths:
    Referral (Has_Referral_ID=Yes): PVS_ID = "PVS-" + seq + "-" + Employee_Initials        e.g. PVS-1001-JK
    Walk-in  (Has_Referral_ID=No):  PVS_ID = "PVS-" + seq + "-" + Employee_Initials + "-M"   e.g. PVS-1002-JK-M
  PVS_Referral_ID = "PVS-" + Referral_ID, REFERRAL PATH ONLY (e.g. PVS-REF-1001); BLANK on walk-ins
  (walk-ins are tracked by PVS_ID). PVS_ID is NO LONGER derived from PVS_Referral_ID.
  DROPPED: the patient-initials code (first initial + last-3) - it violated the no-PHI-in-IDs rule.
  Provider initials (Employee_Initials) KEPT as the last token before any -M. The old "-v2" second-
  Final rule and PVS_ID_Stamp are still open (not built).
  PVS_Referral_ID field relocated into System_Fields_Section; hidden + disabled during entry; inline
  show/hide removed. Generator guard: mints only when PVS_ID is blank (idempotent).
  OPEN BUG (2026-07-12): the PVS_Referral_ID line in the live generator has an operator-precedence
  error (&& binds tighter than ||); needs the OR wrapped in parens or a walk-in stamps "PVS-null".
  Fix supplied; DEPLOY + VERIFY status UNCONFIRMED as of EOD 07-12 - carry to next session.
  TODO: seed Sequence_Tracker "PVS" row at 1001; add No-duplicate constraint on PVS_ID; extract the
  verified generator into OnSuccess__PVS_Stamp_Generator.dg (still a placeholder in the repo).

--------------------------------------------------------------------------------
FIELD DECISIONS SO FAR
--------------------------------------------------------------------------------
- Type_of_Entry: partner-determined -> READ-ONLY/LOCKED when pulled from a referral.
  Provider who disagrees files an ADDENDUM, not an edit. Manual select only on walk-ins.
  ALIGN the option lists so referral and PVS use identical words (no translation):
    "X-Ray Order (only)" -> "X-Ray Order"; "Lab Draw (only)" -> "Lab Order". PVS adds "Clinic Hours".
- System Fields: PVS_ID + PVS_ID_Stamp (PVS's own); Referral_ID + Referral_ID_Stamp and
  Partner_ID + Partner_ID_Stamp = the ASSOCIATED referral's/partner's (pulled). Invoice_Status
  (Draft default / Final) triggers the billing fan-out.
- Type_of_Procedure: fix typo "Wond Care" -> "Wound Care".
- Final_Clinical_Note: confirm "RTL Box" = Rich Text.

--------------------------------------------------------------------------------
ARCHITECTURE (CONFIRMED) - ONE FORM EACH, CONDITIONAL BY TYPE
--------------------------------------------------------------------------------
The single Zoho referral form ALREADY handles all types conditionally (Patient Visit,
3008, X-Ray only, Lab only). So: ONE referral form + ONE PVS form, both conditional by
type (PVS shows Imaging_Order / Lab_Order / Cares_3008 sections per Type_of_Entry). NO
separate spoke forms per type. All referral data dovetails into Referrals_Master.
This REVERSES the earlier "separate referral form + separate PVS flow for X-Ray/Lab/3008" idea.

--------------------------------------------------------------------------------
OPEN FIELD-REVIEW ITEMS (not yet decided)
--------------------------------------------------------------------------------
- Patient Details: ADD Patient_Phone (to schedule) + Patient_Location/Facility Name/Phone/Room
  (where the visit happens)? (asked, undecided.)
- Charges / billing (the heavy one): Complexity_Level (High/Moderate/Low + "Hospital at Home")
  vs Partner_Rates Rate_Type (Telemedicine/Low/Moderate/High). Lists MUST match Rate_Type or the
  invoice can't find a price. No "Hospital at Home" rate exists; Telemedicine missing from complexity.
- After Hours / Super STAT: checkbox (amount auto-from rate card Premium $100/$250) vs manual $ field?
- Referral Partner section: include Partner POC / PR POC Phone / PR POC Email (screenshot has them,
  spec omits)? PR_POC_Title options differ from referral Partner_POC_Title -> align for the pull.
- Provider Signature: include Employee_Initials (sign-off)? how is signature captured (typed initials + date)?
- Clinical_Note_Type = Final/Addendum: does "Addendum" create a PVS Addendum (ADR) record vs stay on form?
- PVS_ID generator: build/update for referral-derived + -v2 + walk-in -M; add PVS_ID_Stamp generator.
- ICD-10 code capture (NEXT SESSION 2026-07-13 PRIORITY, Neil): make the ICD-10 fields
  (ICD_10_Search / ICD_10_Codes) behave like a Creator multi-select, but with options coming from a
  LOOKUP linked to the national ICD-10 registry instead of manually typed choices. Goal: search live
  against the registry and multi-select codes onto the PVS. Design tomorrow. (An ICD-10 Codes data
  source / lookup is available; the EMR stack already lists NPI + medical-terminology lookups.)
