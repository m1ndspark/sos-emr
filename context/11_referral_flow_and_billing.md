# Referral Flow & Billing Architecture

Source: Neil walkthrough, Session 10 (2026-07-09). Business context behind the
`Referrals_Main` form and how it feeds partner data, PVS, and billing. The live
Creator app + `schema/Referrals_Main.md` are ground truth for FIELDS; this file
holds the WHY and the relationships the schema mirror cannot capture.

PHI-clean: process/architecture only, no patient data.

--------------------------------------------------------------------------------
1. REFERRALS_MAIN = THE STARTING POINT
--------------------------------------------------------------------------------
Referrals_Main is where the whole process begins. A user creates a referral
record; downstream records (PVS, assignments, billing) build off it.

INTAKE IS MANUAL, NO LOGIN. Users do not authenticate to create a referral, so
most of the partner section is hand-typed at referral time. The ONLY true lookup
is `Partner_Link` -> Partners (displays `Partner_Display_Name`). Everything else
in the partner block is manual input:
  Partner_Branch, Partner_POC_First_Name, Partner_POC_Last_Name, Partner_POC_Title,
  Partner_POC_Team, Partner_POC_Phone, Partner_POC_Email.

NICE-TO-HAVE (LOW PRIORITY, not now): an easy way to capture/retain partner POC
detail so users don't retype it every referral. Parked.

--------------------------------------------------------------------------------
2. REFERRAL_SOURCE - CLASSIFIES THE SENDER
--------------------------------------------------------------------------------
`Referral_Source` (Radio): "Contracted Parnter" [sic - typo in live choice] / "SOS Internal".
  - Contracted Partner = hospice/partner referrals (99% of volume: AccentCare,
    Empath, Vitas, Chapters, InnoVage).
  - SOS Internal = all NON-hospice referrals (the 2-3 recurring monthly
    subscription referrals created by individuals or SOS's own providers).

Ties to the patient-identity split:
  - Non-hospice (SOS Internal) -> `Patient_SSN` used.
  - Hospice (Contracted Partner) -> `Patient_Hospice_ID` used (hospice patients
    have no SSN on file).

OPEN (parked): how does billing resolve for SOS Internal referrals? The
partner->location->rate chain assumes a contracted partner. Internal/subscription
referrals bill on a different basis. Reconciliation-on-submit likely branches on
Referral_Source. TBD.

--------------------------------------------------------------------------------
3. REFERRAL_TYPE (field label "Service") - WHAT'S NEEDED, + RATE INPUT
--------------------------------------------------------------------------------
Options: Patient Visit, 3008, X-Ray Order (only), Lab Draw (only).
Signals the type of visit/service needed AND relates to the rates table (a
billing input alongside location). A category may be added later (not now).

X-RAY: TWO DISTINCT CONCEPTS - do not conflate:
  - `Referral_Type = "X-Ray Order (only)"` = the referral IS just an X-ray order.
  - `X_Ray_Needed` (No/Yes/I'm Not Sure) = on a REGULAR visit, a heads-up flag
    that an X-ray may also be needed. OPERATIONAL PRE-PLANNING, not billing:
    X-rays are subbed out to SOS's own vendor and ordering->scheduling takes
    time, while hospice wants everything STAT. The flag lets ops line up the
    vendor X-ray in advance instead of discovering the need at the visit.

--------------------------------------------------------------------------------
4. REQUESTED_PRIORITY - SPEED (POLICY SIGNAL, NOT AUTO-BILLING)
--------------------------------------------------------------------------------
Options: Routine / Priority.
  - Routine ~ 24-48 hrs. Priority ~ within 4 hrs (CONFIRM exact windows).
  - BILLING TIE (corrected): Priority is a speed/policy signal that makes a Super
    STAT charge APPROPRIATE to consider; it does NOT auto-apply anything. ALL
    charges (including After Hours and Super STAT) are entered MANUALLY by the
    provider at PVS. Nothing is auto-populated from Priority or the rate card.
    Routine implies no Super STAT.
  - After Hours is a separate premium, also provider-entered at PVS, driven by
    time-of-visit.
  - NOTHING is charged from the referral (see Section 7).

--------------------------------------------------------------------------------
5. CLINICAL + TYPE-SPECIFIC INTAKE (why these fields exist)
--------------------------------------------------------------------------------
- Referral_Reason + Goals_of_Care = why SOS was contacted and the intended
  outcome of the intervention.
- Allergies + Anticoagulant use = critical safety data, ESPECIALLY for
  paracentesis (anticoagulants -> bleeding risk).
- Advanced Directives data.
- Additional_Information + General_Files_Upload = extra context/insight.
- Conditional on Referral_Type:
  - X-Ray: Reason_for_X_Ray_Request + Upload_X_Ray_Request_Files.
  - Lab: Reason_for_Lab_Request, Requested_Lab_Vendor (if they have one),
    Upload_Lab_Request_Files.

--------------------------------------------------------------------------------
6. SYSTEM FIELDS - GENERATORS + CONCATENATIONS (backend, not typed)
--------------------------------------------------------------------------------
Populated by workflows; send info elsewhere in the app and pre-build display
strings so other forms/reports/dashboards don't reassemble them:
  Referral_ID (REF-####) + Referral_ID_Stamp (native), Referral_Date (dedicated,
  distinct from native Added Time; feeds the Assignments lookup display),
  Patient_Full_Name (First+MI+Last), Partner_POC_Name_Title ("First Last, Title"),
  Partner_ID + Partner_ID_Stamp.

--------------------------------------------------------------------------------
7. PARTNER DATA MODEL & BILLING (the core relationship)
--------------------------------------------------------------------------------
Partner forms document the referral SOURCE and supply the RATE context for
billing. Hub-and-spoke around Partners:

  Partners (parent org)
    -> Partner_Locations (branches; via Partner_Link -> Partners)
         - rates/contracts/billing attach at the LOCATION level
    -> Partner_Rates      (via Partner_Location_Link)   RATES ARE LOCATION-KEYED
    -> Partner_Contracts  (Partner_Link + Partner_Location_Link)
    -> Partner_Billing_Contacts (Partner_Link + Partner_Location_Link)

  Partner_Branch_Territory: RETIRED 2026-07-09. Was City/Zip service-area mapping
  per branch; added without realizing Partner_Locations already covered branch
  identity. No workflows attached. Deleted from Creator + tombstoned/removed from
  repo. Full schema recoverable in git history (commit 3b53a34). Only revisit if
  per-branch geographic routing is ever wanted.

CRITICAL BILLING BOUNDARY: NOTHING IS CHARGED AT THE REFERRAL. All billing/
charges originate at the PVS form (Encounter_PatientVisit), which drafts the
invoice to Zoho Books. The referral only captures intake + partner linkage +
rate-ELIGIBILITY signals (Priority->Super STAT eligibility, Referral_Type,
resolved location->rate). Division of labor:
  - Referral = who/what/where + partner + eligibility context. No money.
  - PVS (visit) = what actually happened -> charges -> draft invoice.

--------------------------------------------------------------------------------
8. BRANCH RECONCILIATION (load-bearing, mechanism TBD)
--------------------------------------------------------------------------------
THE GAP: on Referrals_Main, partner is a lookup (Partner_Link) but BRANCH is
free text (`Partner_Branch`, hand-typed). Rates are location-keyed, so a referral
must resolve to a real Partner_Locations record for billing to work.

IMPORTANT NUANCE: the branch a referring user TYPES is not necessarily the
BILLING location. Two different things:
  - Partner_Branch (typed) = referral-source branch, human/approximate.
  - Partner_Locations / billing location = canonical, rate-carrying entity.
So this cannot be a naive text match; it needs a reconciliation step (typed
branch -> canonical billing location).

DECIDED:
  - WHEN: runs on EVERY Referrals_Main submit, alongside Referral_ID generation.
    (Mechanism is Claude's to determine.)
  - UNMATCHED IS SAFE (strive for zero, but ok): every PVS-drafted invoice
    defaults to Draft status. A review dashboard displays submitted PVS entries;
    they're approved for billing one-at-a-time or in bulk (checkbox multi-select
    - approval UX not fully decided). So there's time to catch/flag inaccuracies
    before anything bills.

SHARED NEED: this is the SAME crosswalk as the Cognito import's partner/branch
parsing (context/09). A partner-branch -> billing-location crosswalk should be
built once and used both for live reconciliation and historical import.

--------------------------------------------------------------------------------
9. END GOAL - REPORTING
--------------------------------------------------------------------------------
Each referral carries ~25 data points (to be confirmed field-by-field). These
feed billing (Zoho Books invoice generation) and a custom PARTNER-PORTAL
dashboard that evaluates performance across three lenses:
  - Referral performance
  - PVS entries (visits)
  - Billing / receivables (AR)

--------------------------------------------------------------------------------
OPEN ITEMS (from this walkthrough)
--------------------------------------------------------------------------------
1. Branch reconciliation mechanism (Section 8) - DESIGN NEEDED. Runs on referral
   submit; maps typed Partner_Branch -> Partner_Locations billing location.
2. SOS Internal billing basis (Section 2) - how non-hospice/subscription
   referrals bill without a contracted partner.
3. Priority -> which premium: Priority unlocks Super STAT; After Hours is
   time-driven. Mapping to the specific Partner_Rates.Rate_Type applied happens
   at PVS/billing, not 1:1 from the referral.
4. Confirm exact Routine/Priority time windows.
5. Partner POC auto-recall (reduce retyping) - low priority.
