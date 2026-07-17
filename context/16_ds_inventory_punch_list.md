# SOS EMR Build-vs-Verify Punch List

Source: SOS_Referrals_App.ds, exported 17-Jul-2026 (287 KB), read directly.
Scope: billing-critical state for the 8/3 launch. Repo-vs-live drift reconciliation
(ds_sync) is a separate track noted at the end.

--------------------------------------------------------------------------------
## Live and working (verified in the export)
--------------------------------------------------------------------------------
- PVS ID Stamp Generator (Encounter_PatientVisit, on success). Referral and walk-in
  paths, shared PVS sequence.
- Provider auto-fill: "Pre-fills provider section from employee record" (on load, on
  add). Matches Employees[Employee_Email == zoho.loginuserid], stamps first/last/
  title/initials. NOTE: no Employee_Status == Active gate (the Imaging_Orders resolver
  has one; this does not). Low risk while launch is admin-operated.
- Referral pull: "Referral Link Pre-Fill" (on user input of Referral_Link). Copies a
  full set: all patient fields, Patient_Hospice_ID, SSN, phone/email, location,
  facility, Referral_ID/Stamp, Partner_ID/Stamp, Partner_Organization, Partner_Branch,
  all Partner_POC fields, Partner_POC_Name_Title, Partner_ICD_Codes. Sets Edit_Needed.
  Does NOT pull DM fields (not needed for billing).
- Charge capture fields on the PVS (Visit Cost Drivers + Charges sections):
    Complexity_Level (picklist): High / Moderate / Low Complexity, Hospital at Home,
      No Charge.
    Additional_Charges (checkboxes): After Hours, Super STAT Fee, Equipment Charge,
      Other, with an Additional Charges Show/Hide workflow.
    Complexity_Charge, After_Hours_Fee, Super_Stat_Fee, Equipment_Charge_Amount,
      Equipment_Charge_Details, Other_Charges_Amount. All plain USD fields, entered
      manually. There is no rate-card auto-lookup.
- Invoice_Status field on the PVS (the Draft/Final billing gate); disabled by workflow.
- ICD capture + print (Provider_ICD10_Codes_Link + Provider ICD Print Builder).
- Partner_Rates infrastructure: stamp generator, Partner stamp, Branch Match (on
  validate), Current Flag generator. Rate rows are ready to receive data.
- DM_Full_Name field exists on Referrals_Main, but as plain text with NO generator, so
  it is currently unpopulated.

--------------------------------------------------------------------------------
## Not built (the real build for launch)
--------------------------------------------------------------------------------
- Billing_Branch on the PVS (and referral). Does not exist. Needed for per-branch
  billing. Launch approach: imported on the July backlog, selected by Josh at review
  for anything manual. Automatic territory resolver stays deferred.
- Finalize-lock. No finalize workflow or on-validate gate on the PVS. Locking today is
  only the Invoice_Status disable plus portal page permissions.
- Rate auto-lookup. None. Charges are manual USD fields. Acceptable for launch and
  consistent with providing July cost info manually. Auto-lookup is a later option.
- Invoice engine (PVS to Zoho Books). None.
- Approval dashboard (table, editable overrides, multi-select, $3000 alert, Create
  Invoice, Send). None.
- Invoice email on button push. None.
- PVS fax/email send (PDF generate + store on record + SRFax + SendGrid). None.
  (The PVS print template HTML exists on the form; generation and send do not.)
- DM_Full_Name generator + backfill on Referrals_Main.
- No line-item subform exists, and none is needed. The flat charge fields above are
  the line-item source for the invoice engine.

--------------------------------------------------------------------------------
## Cleanups confirmed live
--------------------------------------------------------------------------------
- "Patient Fields Editability Toggle" (PVS, on user input of Has_Referral_ID) is still
  live. A second handler, "Has Referral_ID Show_Hide", fires on the same event. Delete
  the toggle to remove the double-handling.
- "Partner Rate Stamp Generator" is bound to the Partners form (on success). The
  correct one is on Partner_Rates. Remove the Partners one.

--------------------------------------------------------------------------------
## Impact on the plan
--------------------------------------------------------------------------------
- Q5 (complexity vs rate-type) drops from BLOCKING to a glossary/consistency task,
  because charges are manual, not looked up. The remaining decision is whether to add
  the missing acuity options (Telemedicine, Care Coordination, General Consultation,
  Cares 3008) to Complexity_Level for categorization, and to align the "No Charge"
  and premium labels PVS to invoice.
- The invoice engine is simpler than the locked spec: read the flat charge fields off
  each finalized PVS, one visit becomes its lines, consolidate selected visits per
  partner and branch into one Books invoice.
- Jul 18 to 20 tasks confirmed: glossary + label alignment, add Billing_Branch, build
  finalize-lock, DM_Full_Name generator + backfill, and the two cleanups.

--------------------------------------------------------------------------------
## Separate track: repo-vs-live drift (ds_sync)
--------------------------------------------------------------------------------
Not part of the billing punch list. Run ds_sync against this fresh .ds, confirm drift
direction per file, then apply. Handle the repo renames flagged in HANDOFF before any
NEW-file writes so duplicates are not created.

--------------------------------------------------------------------------------
END
--------------------------------------------------------------------------------
