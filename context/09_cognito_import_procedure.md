# SOS Module - Cognito → Creator Referral Import Procedure

Purpose: repeatable procedure for importing historical/live referrals exported
from Cognito Forms into the Creator `Referrals_Main` form. Reuse this for every
Cognito import. Live Creator app is the source of truth; this documents the
agreed field mapping, data transforms, and post-import steps.

First established: 2026-07-03 (Session 7), importing the July Cognito export
"PatientReferral (30).xlsx" (32 referrals).

--------------------------------------------------------------------------------
0. TOOLS / FILES
--------------------------------------------------------------------------------
- Empty template (headers only, Creator link names): SOS_Referrals_Import_Template.xlsx
- Filled output per run: SOS_Referrals_Cognito_July_Filled.xlsx (rename per month)
- Authoritative field list: sos-referrals-main-form-field-mapping-07032026.csv
  (Zoho Form -> Referrals_Main mapping = the Creator field LINK names)

--------------------------------------------------------------------------------
1. TARGET COLUMNS (Creator link names, in order)
--------------------------------------------------------------------------------
45 columns = 44 importable Referrals_Main fields + Referral_Date.
EXCLUDE from import: section headings; the 3 file-upload fields
(General_Files_Upload, Upload_X_Ray_Request_Files, Upload_Lab_Request_Files);
and custom-script/system fields that are BACKFILLED, not imported:
Referral_ID, Referral_ID_Stamp, Partners (lookup), Partner_ID, Partner_ID_Stamp,
Patient_Full_Name.

Column order:
Referral_Type, Requested_Priority, SOS_Prior_Service, Patient_First_Name,
Patient_MI, Patient_Last_Name, Patient_DOB, Patient_SSN, Patient_Gender,
Patient_Phone, Patient_Email, Patient_Responsibility, DM_First_Name, DM_Last_Name,
Decision_Maker_Phone, Decision_Maker_Email, Decision_Maker_Relationship_to_Patient,
Patient_Location, Facility_Name, Patient_Address, Facility_Phone,
Patient_Room_Number, Referral_Reason, Goals_of_Care, X_Ray_Needed,
Patient_Has_Allergies, List_Patient_Allergies, Patient_Has_Anticoagulants,
List_Patient_Anticoagulants, Patient_Has_Advanced_Directives,
Advanced_Directives_Details, Additional_Information, Reason_for_X_Ray_Request,
Reason_for_Lab_Request, Requested_Lab_Vendor, Partner_POC_Email,
Partner_Organization, Partner_Branch, Partner_POC_Team, Patient_Hospice_ID,
Partner_POC_First_Name, Partner_POC_Last_Name, Partner_POC_Title,
Partner_POC_Phone, Referral_Date.

(Note: the empty template still labels field 40 "Partner_Billing_ID"; for Cognito
imports that column carries the patient Hospice ID and is relabeled
Patient_Hospice_ID. Neil: Hospice ID / Patient_Hospice_ID / Partner_Billing_ID are
equivalent for this value.)

--------------------------------------------------------------------------------
2. FIELD MAPPING (Cognito column -> Creator field)
--------------------------------------------------------------------------------
Cognito repeats field labels across sections, so map by DATA, not by header:
- Select Service                         -> Referral_Type  (see transforms)
- (no source)                            -> Requested_Priority = "Routine" (default)
- Has this patient ever been enrolled with SOS before? -> SOS_Prior_Service (blank in July export; field IS mapped so future values carry)
- Name (PATIENT name, single field)      -> Patient_First_Name / Patient_MI / Patient_Last_Name (split)
- Date of Birth                          -> Patient_DOB (yyyy-MM-dd)
- (no source; MBI is not SSN)            -> Patient_SSN = blank (hospice patients have no SSN)
- Gender                                 -> Patient_Gender (Female/Male)
- Phone.3 (patient phone)                -> Patient_Phone
- (no source)                            -> Patient_Email = blank
- (no source)                            -> Patient_Responsibility = blank ("Are you the person in need of care?" is NOT this field)
- Name.2 (responsible party / coordinate-a-visit contact) -> DM_First_Name / DM_Last_Name (split)
- Phone.4                                -> Decision_Maker_Phone
- (no source)                            -> Decision_Maker_Email = blank
- Relationship to Patient                -> Decision_Maker_Relationship_to_Patient
- Current Patient Location               -> Patient_Location (Home/Facility)
- Facility Name                          -> Facility_Name
- Address (Home) / Address.1 (Facility)  -> Patient_Address (COMPOSITE field, see Section 3 address split)
- Facility Phone                         -> Facility_Phone
- Access Instructions for Property (gate code, room number, etc.) -> Patient_Room_Number
- Primary Complaint                      -> Referral_Reason
- Goals of Care                          -> Goals_of_Care
- (no source)                            -> X_Ray_Needed = blank
- Allergies                              -> Patient_Has_Allergies  ("Known Allergy" -> "Yes"; blank -> blank)
- List All Allergies                     -> List_Patient_Allergies
- Does the patient currently take blood thinning medication? -> Patient_Has_Anticoagulants (normalize case)
- List Meds                              -> List_Patient_Anticoagulants
- Does the patient have Advanced Directives? -> Patient_Has_Advanced_Directives
- Advanced Directives                    -> Advanced_Directives_Details (Creator field mistyped as Radio - VERIFY)
- (no source)                            -> Additional_Information = blank
- (no source)                            -> Reason_for_X_Ray_Request / Reason_for_Lab_Request / Requested_Lab_Vendor = blank
- Email.1 (referrer/"Your Email")        -> Partner_POC_Email
- Organization/Affiliate Name            -> Partner_Organization + Partner_Branch (see partner parsing)
- Clinical Team                          -> Partner_POC_Team
- Hospice ID                             -> Patient_Hospice_ID
- First Name / Last Name / Title / Phone.1 (referrer POC) -> Partner_POC_First_Name / Last_Name / Title / Phone
- Date Submitted                         -> Referral_Date (yyyy-MM-dd) -- PRESERVES true submission date; do NOT rely on Added Time (import stamps today)

DROPPED (not imported): Primary Diagnosis/Comorbidities, Diagnosis Codes,
"Is this an ACO/Hospice/PACE patient?", Age, all Upload Files columns,
Cognito's own "Referral ID". (Dx-code capture comes later with voice-to-text.)
PARKED: Medicare Beneficiary Identifier (MBI). Add a Patient_MBI field to
Referrals_Main later, then backfill MBI from the export (values preserved there).

--------------------------------------------------------------------------------
3. TRANSFORMS
--------------------------------------------------------------------------------
Name split (patient Name, and DM Name.2):
- Split on whitespace (collapse doubles). First token = first name, last token =
  last name. A single middle token that is one letter (optionally with ".") =
  middle initial (Patient_MI, uppercased). Hyphenated last names stay one token
  (e.g. "Vollmar-Miller"). DM has no MI field: fold any middle token into
  DM_First_Name.

Value normalization (applied 2026-07-03):
- TITLE CASE (with acronym guard) on: patient & DM names, Relationship, POC Title,
  Clinical Team, Organization, Facility Name.
  Acronym guard = leave any all-caps token <=4 chars intact (RN, DO, BSN, CTM,
  PACE, EWE, SHH, ALF/LTC). Lowercase filler words (of, the, and, for, to...)
  except the first word. (Limitation: an acronym typed in lowercase in the source,
  e.g. "rncm", is NOT recovered.)
- SENTENCE CASE (capitalize first char only, leave the rest) on free text:
  Referral_Reason, Goals_of_Care, List_Patient_Allergies,
  List_Patient_Anticoagulants, Advanced_Directives_Details.
- LEFT ALONE: emails, phones, IDs, dates, Patient_Address, Gender, Location.

Address (Patient_Address is a COMPOSITE Address field, NOT single line):
- Coalesce Cognito Address (Home) / Address.1 (Facility), then SPLIT into sub-fields:
  Patient_Address_Line_1 / Line_2 (unit/apt) / City / State / Zip / Country.
- Parse rule: split on commas -> [street, (unit), city, "State Zip"]; State/Zip via
  regex (State = text, Zip = 5 or 5-4 digits). County mis-parse guard: if City
  contains "County" and Line_2 is set, City = Line_2 (fixes "Summerfield, Marion County").
- State kept full ("Florida"); switch to "FL" if the composite State sub-field wants abbrev.
  Country defaulted "United States".
- On IMPORT: map each address sub-column to the composite Patient_Address sub-fields
  (Line 1 -> Address Line 1, etc.). Creator displays them as one address block.

Value maps:
- Referral_Type: "Cares/3008 Eval" -> "3008"; blank -> "Patient Visit" (default).
- Patient_Has_Allergies: "Known Allergy" -> "Yes".
- Patient_Has_Anticoagulants: normalize to Creator choices No / Yes / Unable to Verify
  (Cognito "Unable To Verify" -> "Unable to Verify").
- Requested_Priority: default "Routine" (Cognito has no priority column).

--------------------------------------------------------------------------------
4. PARTNER / BRANCH PARSING  (billing-critical - CONFIRM per import)
--------------------------------------------------------------------------------
Cognito "Organization/Affiliate Name" is free text with many variants. Parse into
parent Partner + Branch; set Partner_Organization = parent, Partner_Branch = branch.
Use canonical Creator spellings (AccentCare, InnoVage, Empath Health).

Crosswalk established 2026-07-03 (confirm the parent model each run):
  AccentCare              <- Accentcare
  AccentCare / Hospice    <- Accentcare Hospice                 [confirm branch]
  Empath Health           <- Empath Health
  Empath Health / Suncoast Hospice of Hillsborough <- "Empath Health/Suncoast Hospice of Hillsborough", "Suncoast Hospice of Hillsborough"
  Empath Health / Hospice of Marion County <- "Empath [,] Hospice of Marion [county]"
  Empath Health / Tidewell Hospice <- "Empath/Tidewell", "Tidewell Hospice"
  Empath Health / Suncoast Hospice <- "Suncoast Hospice"
  Empath Health / Trustbridge <- "Trustbridge"                  [confirm parent]
  InnoVage / PACE         <- "Innovage PACE", "Innovage Pace", "PACE" [confirm standalone PACE]

OPEN QUESTIONS (must be settled before partner-match backfill links records):
1. Is Empath Health the PARENT for Suncoast / Tidewell / Trustbridge, or are those
   their own top-level Partners? (Defines the Partner records.)
2. "AccentCare Hospice": a branch "Hospice" or just AccentCare?
3. Standalone "PACE" = InnoVage?
4. "Empath Health" rows with no branch: assign a branch / "Main" (locations always exist)?
Also: confirm these Partners + branches EXIST as records in Creator before matching.

--------------------------------------------------------------------------------
5. IMPORT GOTCHAS (Creator)
--------------------------------------------------------------------------------
- Workflows DO NOT fire on import -> the ID/name/partner generators won't run;
  backfills are required (Section 6).
- Lookups match by value: Partner_Organization text must match a Creator Partner
  for auto-link; otherwise the crosswalk/backfill handles it.
- Dates: import as yyyy-MM-dd.
- Duplicates: a re-import ADDS rows unless imported as "Update" keyed on a unique
  field. Cognito's own Referral ID is currently NOT imported, so there is no dupe
  key -> consider adding a Cognito_Referral_ID column if re-imports are likely.

LESSONS FROM THE FIRST IMPORT (2026-07-03):
- Import into the RIGHT form. First attempt landed on the Partners report by mistake
  (URL #Report:All_Partners) -> Field-Name dropdown only offered Partner fields and
  auto-mapped garbage. Start the import from Referrals_Main.
- "Invalid column value for Partner_Link" on ALL rows = a column was auto-mapped to
  the Partner_Link LOOKUP in Map Columns (Creator maps a "Partner..." column onto it).
  A lookup only accepts a value that already exists. FIX: set Partner_Link (and the
  Partners lookup) to "Do not import"; resolve it via the partner-match backfill after
  the Partner records exist. Never import into a lookup. (No Referrals_Main field is
  mandatory, so an empty Partner_Link is fine once nothing maps to it.)
- Restricted DROPDOWN mismatch: Decision_Maker_Relationship_to_Patient only allows
  Advocate / Family/Friend / Legal Representative / Other. Cognito values (Spouse,
  Son, Daughter, Wife, Sister, RN Case Manager...) are rejected. Options: expand the
  dropdown to real relationships (recommended), skip the column and backfill, or map
  into the 4 buckets. Check other restricted dropdowns similarly before import.
- Zoho Form -> Creator INTEGRATION mapping is separate from CSV import mapping and does
  NOT affect imports. (While there, found a LIVE BUG: Creator "DM Last Name" is mapped
  to Forms "Patient Last Name" -> fix to "Decision Maker Last Name"; SOS Web task.)

--------------------------------------------------------------------------------
6. POST-IMPORT BACKFILL SEQUENCE
--------------------------------------------------------------------------------
Run in order from the Functions console, then spot-check:
  1. backfill_referral_ids()          -> mints REF-#### where blank
  2. backfill_patient_full_names()    -> First [MI] Last (missing-only, require-last-name)
  3. partner-match backfill           -> resolves Partner lookup / Partner_ID / Stamp
                                         from Partner_Organization (+ Partner_Branch)
  4. Spot-check 3-5 records vs Cognito: names/MI, dates, Yes/No picklists, partner+branch link.

--------------------------------------------------------------------------------
7. PER-IMPORT CHECKLIST
--------------------------------------------------------------------------------
[ ] Export referrals from Cognito (xlsx/csv).
[ ] Confirm/disambiguate duplicate Cognito columns against real data.
[ ] Map -> template; apply transforms + normalization.
[ ] Parse partner/branch; CONFIRM the crosswalk + that partners exist in Creator.
[ ] Verify Referral_Type defaults, Priority default, Hospice ID target.
[ ] Import into Referrals_Main (map columns; dates yyyy-MM-dd).
[ ] Run backfills 1-3; spot-check.
[ ] Re-enable notifications only when going live (kept muted during build).
