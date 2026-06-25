# Zoho Form reference - Referrals_Main

The public-facing referral form is a Zoho Form, NOT a Creator form. Respondents
never touch the Creator Referrals_Main form; the Zoho Form is mapped into it and
only stores data for backend processing. All conditional field logic (show/hide,
required, page skips) lives in Zoho Forms, not in Creator. Record it here so the
Creator side is not rebuilt to duplicate it. This is reference only, not Deluge.

Zoho Form name: "Patient Referral"  (link name: PatientReferralsHCO; org: SOSReferralForm)
URL: forms.zoho.com/SOSReferralForm/form/PatientReferralsHCO
Maps to Creator form: Referrals_Main
Integration (Zoho Forms > Integrations > Zoho Creator): Workspace "sosmmc",
Application "SOS Referrals App", Form "Referrals Main". A submission automatically
adds a record to the Creator Referrals_Main form.
Front-end formatting handled by Zoho Forms: phone (NOT SSN; SSN is formatted in
Creator, see _INDEX.md NOTE 7).

--------------------------------------------------------------------------------
RULE CATEGORIES PRESENT (Zoho Forms > Rules)
--------------------------------------------------------------------------------
- Field Rules               show/hide fields based on input  (all 6 captured below)
- Page Rules                skip to pages based on input      (captured below)
- Choice-based Field Rules  show/hide choices in a field      (none configured yet)
- Form Rules                actions on form submission         (none configured yet)
- Deny Submissions          block submission based on input    (none configured yet)

--------------------------------------------------------------------------------
FIELD RULES (all 6 captured)
--------------------------------------------------------------------------------
Action key: Show = reveal field (eye icon); Hide = conceal field (eye-slash icon).

1. Patient Allergies
     IF   "Does the patient have allergies?" Is "Yes"
     THEN Show "List all allergies"

2. Patient Anticoagulants
     IF   "Does the patient use anticoagulant meds?" Is "Yes"
     THEN Show "List anticoagulant medications"

3. Patient Advanced Directives
     IF   "Does the patient have Advanced Directives?" Is "Yes"
     THEN Show "Advanced Directives Details"

4. 3008
     IF   "Service Requested" Is "3008"
     THEN Hide "Grid - Patient Email, Reason for X-Ray Request, Reason for Lab Request"
     NOTE: this is the only Hide rule; a 3008 assessment suppresses the email +
           X-Ray/Lab reason grid that other service types show.

5. Patient Location - Home
     IF   "Where is the patient currently located?" Is Not Empty
     THEN Show "Patient Address"
     NOTE: condition is "Is Not Empty", not "Is Home". Patient Address shows for any
           non-empty location value. Confirm this is intended (rule name implies Home).

6. Patient Location - Facility
     IF   "Where is the patient currently located?" Is "Facility"
     THEN Show "Facility Name, Grid - Facility Phone & Room #"

--------------------------------------------------------------------------------
PAGE RULES (page-skip navigation; grouped by source page)
--------------------------------------------------------------------------------
Routing field is "Service Requested". Form pages seen: Patient Details, Patient
Location, Patient Medical Info, General Information, X-Ray Request Details, Lab
Request Details, Legal Decision Maker, Referral Partner Authentication.

PAGE: Patient Details
  Rule 1: IF Service Requested Is "3008"                -> skip to Patient Location
  Rule 2: IF Service Requested Is "X-Ray Order (only)"  -> skip to X-Ray Request Details
  Rule 3: IF Service Requested Is "Lab Draw (only)"     -> skip to Lab Request Details
  Finally (no rule matches):                            -> skip to Legal Decision Maker

PAGE: Patient Location
  Rule 1: IF Service Requested Is "3008"                -> skip to General Information
  Finally (no rule matches):                            -> skip to Patient Medical Info

PAGE: General Information
  Rule 1: IF Service Requested Is "3008"                -> skip to Referral Partner Authentication
  Finally (no rule matches):                            -> skip to Referral Partner Authentication
  NOTE: Rule 1 and Finally share the same destination, so this rule is currently a
        no-op (both paths reach Referral Partner Authentication). Possibly a
        placeholder for future divergence; confirm intent.

3008 PATH TRACE: a 3008 service routes Patient Details -> Patient Location ->
General Information -> Referral Partner Authentication, bypassing Patient Medical
Info, X-Ray Request Details, Lab Request Details, and Legal Decision Maker. This
matches field-rule 4 (3008 hides the email + X-Ray/Lab reason grid).

CONNECTS TO open contradiction 4-D (radiology/lab handling): the intake form has
dedicated X-Ray Request Details and Lab Request Details pages and routes to them
by Service Requested. Evidence that X-Ray and Lab are distinct intake flows. Does
not resolve 4-D (that is about the Creator form/section structure) but is input.

--------------------------------------------------------------------------------
FIELD MAPPING (Zoho Forms > Integrations > Zoho Creator)
--------------------------------------------------------------------------------
Direction: Zoho Forms field (source) flows INTO Creator Referrals_Main field
(destination). Listed as: Creator field  <-  Zoho Forms field. Names are the
integration UI display labels; Creator link names may differ (partner contact
fields are PAR_-prefixed per context/02; confirmed phone/SSN link names are in
the .dg files). "..." marks a label truncated in the screenshot. Label wording
differences between the Creator and form sides are cosmetic (form layout/column
width, friendlier respondent-facing wording) and expected, not errors (per Neil).

Service Requested                        <- Service Requested
Requested Priority                       <- Requested Priority
Has the patient been seen by SOS...      <- Has the patient been seen by SOS...
Patient First Name                       <- Patient First Name
Patient MI                               <- Patient MI
Patient Last Name                        <- Patient Last Name
Patient DOB                              <- Patient DOB
Patient Biological Sex                   <- Biological Sex
Patient SSN                              <- Patient SSN
Patient Phone                            <- Patient Phone
Patient Email                            <- Patient Email
Is the patient self responsible?         <- Is the patient self responsible?
Decision Maker First Name                <- Decision Maker First Name
Decision Maker Last Name                 <- Patient Last Name           [SEE FLAG 1]
Decision Maker Phone                     <- Decision Maker Phone
Decision Maker Email                     <- Decision Maker Email
Decision Maker Relationship to Patient   <- Relationship to Patient
Patient Location                         <- Where is the patient currently located?
Facility Name                            <- Facility Name
Facility Phone                           <- Facility Phone
Patient Room Number                      <- Room #
Patient Address                          <- Patient Address
Reason for Referral                      <- What is the reason for... (truncated)
Goals of Care                            <- Goals of Care
Will an X-Ray be needed for this ref...  <- Will an X-Ray be needed... (truncated)
Does this patient have allergies?        <- Does the patient have allergies?
List Patient Allergies                   <- List all allergies
Does the patient take anticoagulants     <- Does the patient use anticoagulant meds?
List Patient Anticoagulants              <- List anticoagulant medications
Does the patient have Advanced Direc...  <- Does the patient have Advanced Directives?
Advanced Directives Details              <- Advanced Directives Details
Additional Information                   <- Provide any additional... (truncated)
Reason for X-Ray Request                 <- Reason for X-Ray Request
Reason for Lab Request                   <- Reason for Lab Request
Requested Lab Vendor                     <- Requested Lab Vendor
Partner Organization                     <- Referral Partner Organization
Partner Branch/Location                  <- Partner Branch/Location
Partner Billing ID                       <- Hospice ID                  [SEE FLAG 2]
Partner POC First Name                   <- Referral POC First Name
Partner POC Last Name                    <- Referral POC Last Name
Partner POC Title                        <- Referral POC Title
Partner POC Team                         <- Partner Clinical Team
Partner POC Phone                        <- Referral POC Phone
Partner POC Email                        <- Referral POC Email

FLAGS (confirm against intent; do not change the integration without Neil's approval):
  FLAG 1  Decision Maker Last Name (Creator) is mapped FROM the form's "Patient
          Last Name", not from a decision-maker last-name field. Almost certainly a
          mis-mapping: the decision maker's last name gets the patient's last name.
          Decision Maker First Name maps correctly. This is an identity field in a
          medical/legal context. Verify and fix the integration mapping.
          CONFIRMED an error by the field-mapping sheet (2026-06-25): the intended
          mapping is DM_Last_Name <- "Decision Maker Last Name". The live integration
          sourcing "Patient Last Name" is the bug to fix.
  FLAG 2  RESOLVED (Neil, 2026-06-25): Partner Billing ID and the form's "Hospice
          ID" are the same identifier. Mapping is correct, no change needed.

--------------------------------------------------------------------------------
OPEN ITEMS
--------------------------------------------------------------------------------
- No Choice-based Field Rules, Form Rules, or Deny Submissions configured yet
  (confirmed by Neil). Revisit if any are added.
- FLAG 1 (mapping): Decision Maker Last Name sourced from form "Patient Last Name".
  Likely mis-mapping; verify and fix. STILL OPEN.
- Confirm field-rule 5 intent ("Is Not Empty" vs "Is Home").
- Confirm General Information page-rule intent (Rule 1 and Finally same destination).
- Some labels are truncated in the screenshots ("Has the patient been seen by SOS...",
  "What is the reason for...", "Provide any additional..."). Expand if exact full
  names are needed for link-name confirmation.
