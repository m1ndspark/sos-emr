# Zoho Form reference - Referrals_Main

The public-facing referral form is a Zoho Form, NOT a Creator form. Respondents
never touch the Creator Referrals_Main form; the Zoho Form is mapped into it and
only stores data for backend processing. All conditional field logic (show/hide,
required, page skips) lives in Zoho Forms, not in Creator. Record it here so the
Creator side is not rebuilt to duplicate it. This is reference only, not Deluge.

Zoho Form name: "Patient Referral"  (link name: PatientReferralsHCO; org: SOSReferralForm)
URL: forms.zoho.com/SOSReferralForm/form/PatientReferralsHCO
Maps to Creator form: Referrals_Main
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
  Rule 1: NOT CAPTURED (cut off above Rule 2 in screenshot; re-capture)
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

CONNECTS TO open contradiction 4-D (radiology/lab handling): the intake form has
dedicated X-Ray Request Details and Lab Request Details pages and routes to them
by Service Requested. Evidence that X-Ray and Lab are distinct intake flows. Does
not resolve 4-D (that is about the Creator form/section structure) but is input.

--------------------------------------------------------------------------------
OPEN ITEMS
--------------------------------------------------------------------------------
- Patient Details page Rule 1 was cut off (only Rules 2-3 captured). Re-capture it.
- No Choice-based Field Rules, Form Rules, or Deny Submissions configured yet
  (confirmed by Neil). Revisit if any are added.
- Field mapping: Neil to provide the actual form/field list separately. Map each
  Zoho Form field to its Creator Referrals_Main link name (labels here are Zoho
  Form display labels, which may differ from Creator link names).
- Confirm field-rule 5 intent ("Is Not Empty" vs "Is Home").
- Confirm General Information page-rule intent (Rule 1 and Finally same destination).
