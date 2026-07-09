# Field Link Names (Creator)

Authoritative reference for Creator field LINK NAMES, the names Deluge must use
(input.X, queries, field assignments). Display labels differ from link names and
are for cross-reference only. Confirm a link name here before writing Deluge that
references it (CLAUDE.md rule). Source of truth is the live Creator app.

Keep this PHI-clean: field metadata only, never data values.

================================================================================
FORM: Referrals_Main   (display name "Referrals Main")
================================================================================
Source: sos-referrals-main-form-field-mapping.xlsx (Neil, 2026-06-25), the Zoho
Forms "Patient Referral" -> Creator "Referrals Main" mapping. Grouped by section.
Format:  Creator_Link_Name   Type   <- Zoho Forms label   [choices]
Notes: an earlier version of the sheet had rows misaligned; the corrected file
(2026-06-25) aligns properly and all link-name rows below are verified. The sheet's
Creator-side Field Type column still has a few residual shifts (see DISCREPANCIES);
the types below are the corrected ones. Phone/SSN fields are Single Line text,
confirmed by the extracted .dg formatters.

SECTION  Referral_Type_Section
  Referral_Type            Radio    <- Service Requested   [Patient Visit, 3008, X-Ray Order (only), Lab Draw (only)]
  Requested_Priority       Radio    <- Requested Priority  [Routine, Priority]
  SOS_Prior_Service        Radio    <- Has the patient been seen by SOS Mobile Medical Care before?  [No, Yes]

SECTION  Patient_Details_Section
  Patient_First_Name       text     <- Patient First Name
  Patient_MI               text     <- Patient MI
  Patient_Last_Name        text     <- Patient Last Name
  Patient_DOB              Date     <- Patient DOB
  Patient_Gender           Radio    <- Biological Sex   [Female, Male]
  Patient_SSN              text     <- Patient SSN          [formatter: OnUserInput__Patient_SSN__Format.dg]
  Patient_Phone            text     <- Patient Phone        [formatter: OnUserInput__Patient_Phone__Format.dg]
  Patient_Email            Email    <- Patient Email

SECTION  Decision_Maker_Section
  Patient_Responsibility               Radio     <- Is the patient self responsible?   [No, Yes]
  DM_First_Name                        text      <- Decision Maker First Name
  DM_Last_Name                         text      <- Decision Maker Last Name           [see _zoho_form.md FLAG 1]
  Decision_Maker_Phone                 text      <- Decision Maker Phone   [formatter: OnUserInput__Decision_Maker_Phone__Format.dg]
  Decision_Maker_Email                 Email     <- Decision Maker Email
  Decision_Maker_Relationship_to_Patient Dropdown <- Relationship to Patient  [Advocate, Family/Friend, Legal Representative, Other]

SECTION  Patient_Location_Section
  Patient_Location         Radio    <- Where is the patient currently located?  [Home, Facility]
  Facility_Name            text     <- Facility Name
  Facility_Phone           text     <- Facility Phone   [formatter: OnUserInput__Facility_Phone__Format.dg]
  Patient_Room_Number      text     <- Room #
  Patient_Address          Address  <- Patient Address

SECTION  Patient_Medical_Details_Section
  Referral_Reason              Multi Line  <- What is the reason for this referral?
  Goals_of_Care               Multi Line  <- Goals of Care
  X_Ray_Needed                Radio       <- Will an X-Ray be needed for this referral?  [No, Yes, I'm Not Sure]
  Patient_Has_Allergies       Radio       <- Does the patient have allergies?  [No, Yes, Unable to Verify]
  List_Patient_Allergies      Multi Line  <- List all allergies
  Patient_Has_Anticoagulants  Radio       <- Does the patient use anticoagulant meds?  [No, Yes, Unable to Verify]
  List_Patient_Anticoagulants Multi Line  <- List anticoagulant medications

SECTION  Patient_Advanced_Directives_Section
  Patient_Has_Advanced_Directives  Radio       <- Does the patient have Advanced Directives?  [No, Yes]
  Advanced_Directives_Details      Multi Line  <- Advanced Directives Details   (CONFIRMED Multi Line, Neil 2026-07-04)

SECTION  General_Information_Section
  Additional_Information   Multi Line        <- Provide any additional details that may relate to this referral.
  General_Files_Upload     Multi File Upload <- General Files Upload

SECTION  X_Ray_Request_Details
  Reason_for_X_Ray_Request     Multi Line        <- Reason for X-Ray Request
  Upload_X_Ray_Request_Files   Multi File Upload <- Upload X-Ray Request Files

SECTION  Lab_Request_Reason_Section
  Reason_for_Lab_Request       Multi Line        <- Reason for Lab Request
  Requested_Lab_Vendor         text              <- Requested Lab Vendor
  Upload_Lab_Request_Files     Multi File Upload <- Upload Lab Request Files

SECTION  Referral Partner Details   (Forms pages 10-11; partner authentication + details)
  Partner_POC_Email        Email    <- Your Email   (page 10, prefilled by webhook)
                                    note: page 11 "Referral POC Email" is unmapped in the sheet; confirm if it should also feed Partner_POC_Email
  Partner_Organization     text     <- Referral Partner Organization
  Partner_Branch           text     <- Partner Branch/Location
  Partner_POC_Team         text     <- Partner Clinical Team
  Partner_Billing_ID       text     <- Hospice ID
  Partner_POC_First_Name   text     <- Referral POC First Name
  Partner_POC_Last_Name    text     <- Referral POC Last Name
  Partner_POC_Title        Dropdown <- Referral POC Title  [MD, DO, APRN, PA, Team Leader, RN, MSW, Care Manager, Admin, Other]
  Partner_POC_Phone        text     <- Referral POC Phone   [formatter: OnUserInput__Partner_POC_Phone__Format.dg]

SECTION  System_Fields_Section   (no Forms counterpart; backend / generated)
  Referral_ID              text     Custom script
  Referral_ID_Stamp        text     Custom script
  Partner_Link             Lookup   (lookup to Partners form)
                                    UPDATED June 26, 2026: this field was renamed
                                    from "Partners" to Partner_Link to match the
                                    other lookups. Deluge must use Partner_Link.
  Partner_Location         Lookup   PENDING (June 26, 2026): not yet built. Approved
                                    in principle. Lookup to Partner_Locations. The
                                    On Success resolver writes it from the matched
                                    POC record; the REF ID generator reads Branch_Code
                                    from it. See context/07.
  Partner_ID               text     Custom script
  Partner_ID_Stamp         text     Custom script

--------------------------------------------------------------------------------
DISCREPANCIES / NOTES
--------------------------------------------------------------------------------
- PAR_ vs Partner_ prefix: context/02_form_architecture.md states partner/referral
  contact fields use a PAR_ prefix (PAR_Organization, PAR_POC_First_Name, etc.).
  The live Referrals_Main fields use Partner_ instead (Partner_Organization,
  Partner_POC_First_Name, ...). Live wins; the PAR_ convention does not apply here.
  Confirm whether PVS (Encounter_PatientVisit) still uses PAR_ before relying on it.
- Decision Maker link names mix prefixes: DM_First_Name / DM_Last_Name but
  Decision_Maker_Phone / Decision_Maker_Email / Decision_Maker_Relationship_to_Patient.
  This is the live reality, not an error.
- All 5 extracted formatters' link names are confirmed by this mapping (Patient_SSN,
  Patient_Phone, Decision_Maker_Phone, Facility_Phone, Partner_POC_Phone), and those
  fields are Single Line text, which is why the string formatters work.
- System_Fields_Section has Referral_ID / Referral_ID_Stamp / Partner_ID /
  Partner_ID_Stamp (Custom script) and a Partners lookup. Relevant to the object-ID
  and Sequence_Tracker work (contradictions 4-B, 4-C).
- Source-sheet type-column artifacts (link names correct, Field Type cell shifted):
  Patient_Gender (sheet: Single Line; actual: Radio), Patient_Address (sheet: Single
  Line; actual: Address), Patient_Room_Number (sheet: Address; actual: Single Line),
  Advanced_Directives_Details (sheet: Radio/No,Yes; actual: Multi Line). Types above
  are corrected. Patient_Has_Advanced_Directives = Radio [No, Yes] and
  Advanced_Directives_Details = Multi Line both CONFIRMED live by Neil 2026-07-04.
