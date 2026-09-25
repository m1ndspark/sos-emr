# Multi-writer field audit (Session 54, 2026-09-25)

Source: SOS_Referrals_App_2026-09-25_v54.ds, overlaid with the Session 54 repo versions of Sender Sets Branch, Partner Contact Lookup, PVS Sets Billing Branch On Save and Referral Resolves Partner On Save. Static analysis only; no data was read.

"Live" = an active workflow, or a function called (directly or indirectly) from an active workflow. 72 fields have 2+ live writers.

## A. Writers that produce DIFFERENT results (real conflicts)

1. Referrals_Main phone fields (Patient_Phone, Partner_POC_Phone, Facility_Phone, AC_Phone): the on-user-input formatters store "(813) 555-1234"; process_new_referral (On Success, create) rewrites to "813-555-1234". Stored format depends on the entry path. All four formatters also throw on fewer than 10 digits (subString with a negative index).
2. Encounter_PatientVisit.Complexity_Charge: 4 live writers (Branch Sets Charge, Complexity Sets Charge, PVS 3008 Billing Stamp, PVS Sets Billing Branch On Save) plus 9 functions, with different behaviour (only Complexity Sets Charge alerts on a missing rate; 3008 Stamp fills only when the charge is 0; PVS On Save only when Billing_Branch was blank). The Partner_Rates lookup is copied 30 times in the .ds.
3. Assignments: process_new_referral inserts Patient_DOB as "MM/dd/yyyy" text and does NOT set Referral_Date, Referral_Partner or Referral_POC; Assignment_Pull_From_Referral (UI, on user input of Referral_Link) copies the raw DOB date and DOES set those three. Assignments created at intake therefore lack fields that UI-created ones have.

## B. Duplicate writers that produce the SAME result (redundant, not fighting)

- Encounter_PatientVisit Billing_Branch / Partner_Organization / Partner_Branch / Partner_Location_Label: Referral Link Pre-Fill and Referral Sets Billing Branch both copy them on the same trigger (user input of Referral_Link); PVS Sets Billing Branch On Save fills blanks only. Ruling 2026-09-25: leave as is.
- Referrals_Main partner fields (Partner_Link, Partner_Branch, Partner_Location_Label, Partner_Organization, Partner_ID, Partner_ID_Stamp, Partner_Branch_Link): Branch Sets Partner (live display), Referral Resolves Partner On Save and process_new_referral all write the same values. Ruling 2026-09-25: leave as is.
- Referrals_Main Patient_Full_Name and Partner_POC_Name_Title: process_new_referral, set_patient_full_name / set_partner_poc_name_title and the two On Success "Generator" workflows compose the same format.
- Referrals_Main Patient_SSN, Patient_Full_Address, AC_Full_Name; Partner_Referral_Contacts.Partner_POC_Name_Title: formatter/builder plus process_new_referral, same format.

## C. Lifecycle or UI writers (expected, not redundant)

- Fax_Log / Encounter_PatientVisit fax fields (send_pvs_fax, poll_fax_status, retry_failed_faxes), Invoice_Status (3008 Stamp sets Draft, invoicing sets Invoiced), Sequence_Tracker.Object_Sequence (one row per object type), PVS_Fax_Review modal fields, Has Referral_ID Show_Hide clearing PVS fields when answered No, PVS Required Fields filling blank Patient_DOB / Reason_for_Referral.

## Full list of fields with 2+ live writers

- API_Config.RC_Access_Token (2 live / 4 total): get_rc_token [function-update]; send_pvs_fax [function-update]
- API_Config.RC_Token_Expiry (2 live / 4 total): get_rc_token [function-update]; send_pvs_fax [function-update]
- Assignments.Patient_First_Name (2 live / 2 total): process_new_referral [function-insert]; Assignment_Pull_From_Referral [on add or edit / on user input of Referral_Link]
- Assignments.Patient_Last_Name (2 live / 2 total): process_new_referral [function-insert]; Assignment_Pull_From_Referral [on add or edit / on user input of Referral_Link]
- Assignments.Patient_DOB (2 live / 2 total): process_new_referral [function-insert]; Assignment_Pull_From_Referral [on add or edit / on user input of Referral_Link]
- Assignments.Patient_Phone (2 live / 2 total): process_new_referral [function-insert]; Assignment_Pull_From_Referral [on add or edit / on user input of Referral_Link]
- Assignments.Patient_Address (2 live / 2 total): process_new_referral [function-insert]; Assignment_Pull_From_Referral [on add or edit / on user input of Referral_Link]
- Assignments.Patient_Location (2 live / 2 total): process_new_referral [function-insert]; Assignment_Pull_From_Referral [on add or edit / on user input of Referral_Link]
- Assignments.Facility_Name (2 live / 2 total): process_new_referral [function-insert]; Assignment_Pull_From_Referral [on add or edit / on user input of Referral_Link]
- Assignments.Facility_Phone (2 live / 2 total): process_new_referral [function-insert]; Assignment_Pull_From_Referral [on add or edit / on user input of Referral_Link]
- Assignments.Facility_Room_Number (2 live / 2 total): process_new_referral [function-insert]; Assignment_Pull_From_Referral [on add or edit / on user input of Referral_Link]
- Encounter_PatientVisit.Partner_Organization (4 live / 8 total): Has Referral_ID Show_Hide [on add or edit / on user input of Has_Referral_ID]; PVS Sets Billing Branch On Save [on add or edit / on validate]; Referral Link Pre-Fill [on add / on user input of Referral_Link]; Referral Sets Billing Branch [on add or edit / on user input of Referral_Link]
- Encounter_PatientVisit.Partner_Branch (4 live / 9 total): Has Referral_ID Show_Hide [on add or edit / on user input of Has_Referral_ID]; PVS Sets Billing Branch On Save [on add or edit / on validate]; Referral Link Pre-Fill [on add / on user input of Referral_Link]; Referral Sets Billing Branch [on add or edit / on user input of Referral_Link]
- Encounter_PatientVisit.Complexity_Charge (4 live / 13 total): Branch Sets Charge [on add or edit / on user input of Billing_Branch]; Complexity Sets Charge [on add or edit / on user input of Complexity_Level]; PVS 3008 Billing Stamp [on add or edit / on validate]; PVS Sets Billing Branch On Save [on add or edit / on validate]
- Encounter_PatientVisit.Patient_DOB (3 live / 6 total): Has Referral_ID Show_Hide [on add or edit / on user input of Has_Referral_ID]; PVS Required Fields [on add or edit / on validate]; Referral Link Pre-Fill [on add / on user input of Referral_Link]
- Encounter_PatientVisit.Partner_Location_Label (3 live / 7 total): PVS Sets Billing Branch On Save [on add or edit / on validate]; Referral Link Pre-Fill [on add / on user input of Referral_Link]; Referral Sets Billing Branch [on add or edit / on user input of Referral_Link]
- Encounter_PatientVisit.Billing_Branch (3 live / 7 total): Has Referral_ID Show_Hide [on add or edit / on user input of Has_Referral_ID]; PVS Sets Billing Branch On Save [on add or edit / on validate]; Referral Sets Billing Branch [on add or edit / on user input of Referral_Link]
- Encounter_PatientVisit.Patient_Full_Name_1 (2 live / 6 total): Has Referral_ID Show_Hide [on add or edit / on user input of Has_Referral_ID]; Referral Link Pre-Fill [on add / on user input of Referral_Link]
- Encounter_PatientVisit.Patient_First_Name (2 live / 5 total): Has Referral_ID Show_Hide [on add or edit / on user input of Has_Referral_ID]; Referral Link Pre-Fill [on add / on user input of Referral_Link]
- Encounter_PatientVisit.Patient_MI (2 live / 6 total): Has Referral_ID Show_Hide [on add or edit / on user input of Has_Referral_ID]; Referral Link Pre-Fill [on add / on user input of Referral_Link]
- Encounter_PatientVisit.Patient_Last_Name (2 live / 5 total): Has Referral_ID Show_Hide [on add or edit / on user input of Has_Referral_ID]; Referral Link Pre-Fill [on add / on user input of Referral_Link]
- Encounter_PatientVisit.Patient_Gender (2 live / 5 total): Has Referral_ID Show_Hide [on add or edit / on user input of Has_Referral_ID]; Referral Link Pre-Fill [on add / on user input of Referral_Link]
- Encounter_PatientVisit.Patient_Address (2 live / 2 total): Has Referral_ID Show_Hide [on add or edit / on user input of Has_Referral_ID]; Referral Link Pre-Fill [on add / on user input of Referral_Link]
- Encounter_PatientVisit.Patient_Hospice_ID (2 live / 6 total): Has Referral_ID Show_Hide [on add or edit / on user input of Has_Referral_ID]; Referral Link Pre-Fill [on add / on user input of Referral_Link]
- Encounter_PatientVisit.Patient_SSN (2 live / 3 total): Has Referral_ID Show_Hide [on add or edit / on user input of Has_Referral_ID]; Referral Link Pre-Fill [on add / on user input of Referral_Link]
- Encounter_PatientVisit.Patient_Phone (2 live / 6 total): Has Referral_ID Show_Hide [on add or edit / on user input of Has_Referral_ID]; Referral Link Pre-Fill [on add / on user input of Referral_Link]
- Encounter_PatientVisit.Patient_Location (2 live / 4 total): Has Referral_ID Show_Hide [on add or edit / on user input of Has_Referral_ID]; Referral Link Pre-Fill [on add / on user input of Referral_Link]
- Encounter_PatientVisit.Facility_Name (2 live / 4 total): Has Referral_ID Show_Hide [on add or edit / on user input of Has_Referral_ID]; Referral Link Pre-Fill [on add / on user input of Referral_Link]
- Encounter_PatientVisit.Facility_Phone (2 live / 6 total): Has Referral_ID Show_Hide [on add or edit / on user input of Has_Referral_ID]; Referral Link Pre-Fill [on add / on user input of Referral_Link]
- Encounter_PatientVisit.Facility_Room_Number (2 live / 6 total): Has Referral_ID Show_Hide [on add or edit / on user input of Has_Referral_ID]; Referral Link Pre-Fill [on add / on user input of Referral_Link]
- Encounter_PatientVisit.Referral_ID (2 live / 4 total): Has Referral_ID Show_Hide [on add or edit / on user input of Has_Referral_ID]; Referral Link Pre-Fill [on add / on user input of Referral_Link]
- Encounter_PatientVisit.Referral_ID_Stamp (2 live / 3 total): Has Referral_ID Show_Hide [on add or edit / on user input of Has_Referral_ID]; Referral Link Pre-Fill [on add / on user input of Referral_Link]
- Encounter_PatientVisit.Partner_ID (2 live / 4 total): Has Referral_ID Show_Hide [on add or edit / on user input of Has_Referral_ID]; Referral Link Pre-Fill [on add / on user input of Referral_Link]
- Encounter_PatientVisit.Partner_ID_Stamp (2 live / 3 total): Has Referral_ID Show_Hide [on add or edit / on user input of Has_Referral_ID]; Referral Link Pre-Fill [on add / on user input of Referral_Link]
- Encounter_PatientVisit.Partner_POC_Team (2 live / 4 total): Has Referral_ID Show_Hide [on add or edit / on user input of Has_Referral_ID]; Referral Link Pre-Fill [on add / on user input of Referral_Link]
- Encounter_PatientVisit.Partner_POC_First_Name (2 live / 3 total): Has Referral_ID Show_Hide [on add or edit / on user input of Has_Referral_ID]; Referral Link Pre-Fill [on add / on user input of Referral_Link]
- Encounter_PatientVisit.Partner_POC_Last_Name (2 live / 3 total): Has Referral_ID Show_Hide [on add or edit / on user input of Has_Referral_ID]; Referral Link Pre-Fill [on add / on user input of Referral_Link]
- Encounter_PatientVisit.Partner_POC_Title (2 live / 3 total): Has Referral_ID Show_Hide [on add or edit / on user input of Has_Referral_ID]; Referral Link Pre-Fill [on add / on user input of Referral_Link]
- Encounter_PatientVisit.Partner_POC_Phone (2 live / 5 total): Has Referral_ID Show_Hide [on add or edit / on user input of Has_Referral_ID]; Referral Link Pre-Fill [on add / on user input of Referral_Link]
- Encounter_PatientVisit.Partner_POC_Email (2 live / 4 total): Has Referral_ID Show_Hide [on add or edit / on user input of Has_Referral_ID]; Referral Link Pre-Fill [on add / on user input of Referral_Link]
- Encounter_PatientVisit.Partner_POC_Name_Title (2 live / 4 total): Has Referral_ID Show_Hide [on add or edit / on user input of Has_Referral_ID]; Referral Link Pre-Fill [on add / on user input of Referral_Link]
- Encounter_PatientVisit.Reason_for_Referral (2 live / 6 total): PVS Required Fields [on add or edit / on validate]; Referral Link Pre-Fill [on add / on user input of Referral_Link]
- Encounter_PatientVisit.Edit_Needed (2 live / 2 total): Has Referral_ID Show_Hide [on add or edit / on user input of Has_Referral_ID]; Referral Link Pre-Fill [on add / on user input of Referral_Link]
- Encounter_PatientVisit.Patient_Email (2 live / 2 total): Has Referral_ID Show_Hide [on add or edit / on user input of Has_Referral_ID]; Referral Link Pre-Fill [on add / on user input of Referral_Link]
- Encounter_PatientVisit.Invoice_Status (2 live / 8 total): create_invoice_from_selection [function-update]; PVS 3008 Billing Stamp [on add or edit / on validate]
- Encounter_PatientVisit.Fax_Status (2 live / 3 total): poll_fax_status [function-update]; send_pvs_fax [function-update]
- Fax_Log.Fax_Status (3 live / 5 total): send_pvs_fax [function-insert]; poll_fax_status [function-update]; retry_failed_faxes [function-update]; send_pvs_fax [function-update]
- Fax_Log.Fax_Error_Reason (3 live / 4 total): poll_fax_status [function-update]; retry_failed_faxes [function-update]; send_pvs_fax [function-update]
- Fax_Log.Completed_Time (3 live / 4 total): poll_fax_status [function-update]; retry_failed_faxes [function-update]; send_pvs_fax [function-update]
- Fax_Log.Last_Polled_Time (2 live / 3 total): poll_fax_status [function-update]; send_pvs_fax [function-update]
- PVS_Fax_Review.Result_Message (3 live / 3 total): PVS Fax Review Fax Now [ / on click]; PVS Fax Review On Load [on add / on load]; PVS Fax Review Override Unlock [on add / on user input of Override_Unlock]
- PVS_Fax_Review.Override_Fax (2 live / 2 total): PVS Fax Review Format Override Fax [on add / on user input of Override_Fax]; PVS Fax Review Override Unlock [on add / on user input of Override_Unlock]
- PVS_Fax_Review.Override_Fax_Confirm (2 live / 2 total): PVS Fax Review Format Override Fax Confirm [on add / on user input of Override_Fax_Confirm]; PVS Fax Review Override Unlock [on add / on user input of Override_Unlock]
- Partner_Referral_Contacts.Partner_POC_Name_Title (2 live / 4 total): process_new_referral [function-insert]; process_new_referral [function-update]; Partner POC Name Title Builder [on add or edit / on validate]
- Referrals_Main.Partner_POC_Phone (3 live / 3 total): process_new_referral [function-update]; Partner Contact Lookup [on add / on user input of Partner_POC_Email]; Referral Partner POC Phone Format [on add or edit / on user input of Partner_POC_Phone]
- Referrals_Main.Partner_Link (3 live / 7 total): process_new_referral [function-update]; Branch Sets Partner [on add or edit / on user input of Partner_Branch_Link]; Referral Resolves Partner On Save [on add or edit / on validate]
- Referrals_Main.Partner_Branch (3 live / 8 total): process_new_referral [function-update]; Branch Sets Partner [on add or edit / on user input of Partner_Branch_Link]; Referral Resolves Partner On Save [on add or edit / on validate]
- Referrals_Main.Partner_Location_Label (3 live / 8 total): process_new_referral [function-update]; Branch Sets Partner [on add or edit / on user input of Partner_Branch_Link]; Referral Resolves Partner On Save [on add or edit / on validate]
- Referrals_Main.Partner_Organization (3 live / 7 total): process_new_referral [function-update]; Branch Sets Partner [on add or edit / on user input of Partner_Branch_Link]; Referral Resolves Partner On Save [on add or edit / on validate]
- Referrals_Main.Partner_ID (3 live / 7 total): process_new_referral [function-update]; Branch Sets Partner [on add or edit / on user input of Partner_Branch_Link]; Referral Resolves Partner On Save [on add or edit / on validate]
- Referrals_Main.Patient_Full_Name (3 live / 3 total): process_new_referral [function-update]; set_patient_full_name [function-update]; Patient Full Name Generator [on edit / on success]
- Referrals_Main.Partner_POC_Name_Title (3 live / 3 total): process_new_referral [function-update]; set_partner_poc_name_title [function-update]; Partner POC Name & Title Generator [on edit / on success]
- Referrals_Main.Partner_Branch_Link (3 live / 8 total): process_new_referral [function-update]; Referral Resolves Partner On Save [on add or edit / on validate]; Sender Sets Branch [on add or edit / on user input of Partner_POC_Email]
- Referrals_Main.Patient_SSN (2 live / 2 total): process_new_referral [function-update]; SSN Format [on add or edit / on user input of Patient_SSN]
- Referrals_Main.Patient_Phone (2 live / 3 total): process_new_referral [function-update]; Patient Phone Format [on add or edit / on user input of Patient_Phone]
- Referrals_Main.AC_Phone (2 live / 2 total): process_new_referral [function-update]; Decision Maker Phone Format [on add or edit / on user input of AC_Phone]
- Referrals_Main.Facility_Phone (2 live / 2 total): process_new_referral [function-update]; Facility Phone Format [on add or edit / on user input of Facility_Phone]
- Referrals_Main.Patient_Full_Address (2 live / 2 total): process_new_referral [function-update]; Build Patient Full Address [on add or edit / on user input of Patient_Address]
- Referrals_Main.AC_Full_Name (2 live / 2 total): process_new_referral [function-update]; DM Full Name Generator [on add or edit / on user input of AC_Last_Name]
- Referrals_Main.Partner_ID_Stamp (2 live / 5 total): process_new_referral [function-update]; Referral Resolves Partner On Save [on add or edit / on validate]
- Referrals_Main.Partner_Branch_Submitted (2 live / 2 total): process_new_referral [function-update]; Referral Resolves Partner On Save [on add or edit / on validate]
- Sequence_Tracker.Object_Sequence (6 live / 9 total): mint_assignment_id [function-update]; mint_employee_id [function-update]; mint_location_id [function-update]; mint_partner_id [function-update]; mint_referral_id [function-update]; send_pvs_fax [function-update]
