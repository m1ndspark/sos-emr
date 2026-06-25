# Form Architecture (EMR)

Source: SOS EMR App module, May 8 session log. Treat the live Creator app as
ground truth where this disagrees.

MASTER FORM LIST (16, per the locked module)
  Referrals_Main, Referrals_Master, Partners, Partner_Locations,
  Partner_Portal_Users, Employees, Charge_Types, Partner_Rates,
  Encounter_PatientVisit, Encounter_ClinicHours, Encounter_RadiologyRequest,
  Encounter_LabRequest, Assignments, Procedure_Templates, Messaging_Hub,
  Sequence_Tracker.

KEY FORMS
- Referrals_Main is the primary patient referral form.
- Encounter_PatientVisit is the PVS (Patient Visit Summary), the SOS clinical
  note, completed after each patient visit.
- See open contradiction 4-A: the April task master built around a consolidated
  "Encounters_Main" with an Imaging_Order_Section, while the module lists separate
  Encounter_RadiologyRequest and Encounter_LabRequest. Confirm live state.

WORKFLOWS CONFIRMED WORKING (May 8) ON Encounter_PatientVisit
- Provider Pre-Fill (On Load)
- Default Hide On Load (On Load)
- Referral ID Show/Hide (On User Input, Has_Referral_ID)
- Entry Type Section Visibility (On User Input, Type_of_Entry)
- Diversion Type Show/Hide (On User Input, Diversion_Tracking)
- Additional Charges Show/Hide (On User Input, Additional_Charges)
- PVS Stamp Generator (On Success, Script 011)
Built but untested: Referral Link Pre-Fill (On User Input, Referral_Link),
needs dummy referral data.

WORKFLOWS ON Referrals_Main
- SSN Format (On User Input, Patient_SSN): working.
- Phone Format (On User Input, Patient_Phone): blocked. The referral form is in
  Zoho Forms, and the raw value format passed into Creator after integration is
  unknown. Next step is to submit a test record via Zoho Forms and inspect the
  raw value in Creator before deciding if any formatting workflow is needed.

FIELD CONVENTIONS
- PAR_ prefix standardized for all partner/referral contact fields across
  Encounter_PatientVisit and Referrals_Main: PAR_Organization, PAR_Branch,
  PAR_POC_Team, PAR_POC_First_Name, PAR_POC_Last_Name, PAR_POC_Title,
  PAR_POC_Full_Name (computed, display only; the First/Last/Title parts hidden).
- Other_Charges renamed to Other_Charges_Amount.
- Partner_ID present in System_Fields_Section on Encounter_PatientVisit.
- Employee_Initials in Provider_Signature_Section, read from an input field,
  pre-filled on load.

IDENTITY FUNCTION
- fn_resolveUserIdentity: centralized identity resolution by email domain.
  Designed April 18, 2026. Confirm whether it is deployed in the Functions tab.
