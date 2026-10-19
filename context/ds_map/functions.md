# Functions

Per function: forms and fields it fetches, inserts, updates, deletes or reads through a fetched record; functions it calls; callers; integrations (INTEG_KEYS).

## add_missing_rate_to_uniform_branches

- Signature: Deluge.add_missing_rate_to_uniform_branches() returns string
- .ds line: 8450
- Fetch: Partner_Locations (ID, Partner_Link, Partner_Location_Status); Partner_Rates (Current_Rate, ID, Partner_Location_Link); Partners (Partner_Status, Rate_Structure)
- Insert: Partner_Rates (Added_User, Current_Rate, Partner_Link, Partner_Location_Link, Partner_Rate_Status, Partner_Rates_Effective_Date, Rate_Amount, Rate_Category, Rate_Type)
- Update: Partner_Rates (Partner_Rate_ID_Stamp)
- Delete: -
- Read: Partner_Locations (ID, Partner_Location_Label); Partner_Rates (Partner_Rates_Effective_Date, Rate_Amount, Rate_Category, Rate_Type); Partners (ID, Partner_Display_Name)
- Calls: -
- Called by: -
- Integrations: -

## admin_set_field

- Signature: Deluge.admin_set_field(string p_report, string p_key_field, string p_key_value, string p_field, string p_value, string p_mode) returns map
- .ds line: 8520
- Fetch: -
- Insert: -
- Update: -
- Delete: -
- Read: -
- Calls: -
- Called by: -
- Integrations: HTTP

## api_fax_begin

- Signature: Deluge.api_fax_begin() returns map
- .ds line: 8589
- Fetch: Employees (Employee_Email); Fax_Log (ID)
- Insert: Fax_Log (Added_User, Attempt_Number, Fax_Status, Number_Source)
- Update: Fax_Log (Sent_By)
- Delete: -
- Read: Employees (ID)
- Calls: -
- Called by: -
- Integrations: -

## api_fax_pvs_search

- Signature: Deluge.api_fax_pvs_search(string p_branchId, string p_query, string p_unsentOnly) returns map
- .ds line: 8610
- Fetch: Encounter_PatientVisit (Added_Time, Billing_Branch, ID, Type_of_Entry); Partner_Locations (ID)
- Insert: -
- Update: -
- Delete: -
- Read: Encounter_PatientVisit (Billing_Branch, Clinical_Note_Type, Fax_Status, ID, PVS_ID, Patient_Full_Name_1, Patient_Hospice_ID, Referral_ID, Visit_Completion_Date); Partner_Locations (Partner_Location_Name)
- Calls: -
- Called by: -
- Integrations: -

## api_fax_recipients

- Signature: Deluge.api_fax_recipients() returns map
- .ds line: 8701
- Fetch: Partner_Billing_Contacts (Partner_Billing_POC_Status); Partner_Locations (ID); Partners (ID)
- Insert: -
- Update: -
- Delete: -
- Read: Partner_Billing_Contacts (ID, Partner_Billing_POC_First_Name, Partner_Billing_POC_Last_Name, Partner_Link, Partner_Location_Link, Partner_PVS_Fax); Partner_Locations (Partner_Location_Name); Partners (Partner_Display_Name)
- Calls: -
- Called by: -
- Integrations: -

## api_fax_send_console

- Signature: Deluge.api_fax_send_console(string pLogId, string pContactId, list pPvsIds, string pRemarks) returns map
- .ds line: 8745
- Fetch: API_Config (Config_Name); Encounter_PatientVisit (ID); Fax_Attachments (ID); Fax_Log (Fax_ID, ID); Partner_Billing_Contacts (ID); Partner_Locations (ID); Partners (ID); Sequence_Tracker (Object_Prefix)
- Insert: Fax_Attachments (Added_User, Attachment_Name, Attachment_Type, Fax_Log, Sequence_Number, Source_PVS_Link)
- Update: API_Config (RC_Access_Token, RC_Token_Expiry); Encounter_PatientVisit (Fax_Status); Fax_Attachments (Attachment_File); Fax_Log (Attachments_Included, Completed_Time, Cover_Remarks, Destination_Fax, Destination_Name, Fax_Error_Reason, Fax_ID, Fax_PDF, Fax_Status, Last_Polled_Time, Number_Source, Partner_Link, Partner_Location_Link, RC_Conversation_ID, RC_Message_ID, Submitted_Time); Sequence_Tracker (Object_Sequence)
- Delete: -
- Read: Partner_Billing_Contacts (Partner_Billing_POC_First_Name, Partner_Billing_POC_Last_Name, Partner_Link, Partner_Location_Link, Partner_PVS_Fax); Partner_Locations (Partner_Location_Name); Partners (Partner_Display_Name); Sequence_Tracker (Object_Sequence)
- Calls: build_console_docs, get_rc_token
- Called by: -
- Integrations: AppFunc, HTTP

## assign_direct_partner

- Signature: Deluge.assign_direct_partner(string p_mode, string p_refIds, string p_source) returns string
- .ds line: 9020
- Fetch: Partner_Locations (Partner_Location_Label, Partner_Location_Status); Referrals_Main (ID, Referral_ID)
- Insert: -
- Update: Referrals_Main (Partner_Branch, Partner_Branch_Link, Partner_ID, Partner_ID_Stamp, Partner_Link, Partner_Location_Label, Partner_Organization, Referral_Source)
- Delete: -
- Read: Partner_Locations (ID, Partner_Link, Partner_Location_Label, Partner_Location_Name); Partners (Partner_Display_Name, Partner_ID); Referrals_Main (ID, Partner_Branch_Link)
- Calls: -
- Called by: -
- Integrations: -

## assign_partner_branch

- Signature: Deluge.assign_partner_branch(string p_mode, string p_map) returns string
- .ds line: 9116
- Fetch: Partner_Locations (Partner_Location_Label, Partner_Location_Status); Referrals_Main (ID, Referral_ID)
- Insert: -
- Update: Referrals_Main (Partner_Branch, Partner_Branch_Link, Partner_ID, Partner_ID_Stamp, Partner_Link, Partner_Location_Label, Partner_Organization)
- Delete: -
- Read: Partner_Locations (ID, Partner_Link, Partner_Location_Label, Partner_Location_Name); Partners (Partner_Display_Name, Partner_ID); Referrals_Main (ID)
- Calls: -
- Called by: -
- Integrations: -

## audit_month_integrity

- Signature: Deluge.audit_month_integrity(string p_mode, date p_from, date p_to) returns string
- .ds line: 9206
- Fetch: Encounter_PatientVisit (ID, Visit_Completion_Date); Invoices (ID); Partner_Rates (Current_Rate); Referrals_Main (ID)
- Insert: -
- Update: -
- Delete: -
- Read: Encounter_PatientVisit (After_Hours_Fee, Billing_Branch, Cares_3008_Completion_Date, Clinical_Note_Type, Complexity_Charge, Complexity_Level, Diversion_Tracking, Employee_Initials, Employee_Link, Employee_Name_Title, Equipment_Charge_Amount, Facility_Name, Facility_Phone, Final_Clinical_Note, Hold_From_Invoicing, ID, Invoice_Link, Invoice_Status, Other_Charges_Amount, PVS_ID, Partner_Branch, Partner_ID, Partner_Location_Label, Partner_Organization, Patient_Address, Patient_DOB, Patient_First_Name, Patient_Full_Name_1, Patient_Gender, Patient_Hospice_ID, Patient_Last_Name, Patient_Location, Patient_Phone, Reason_for_Referral, Referral_Date, Referral_ID, Referral_Link, Row_Status, Super_Stat_Fee, Type_of_Entry, Type_of_Procedures, Visit_Completion_Date, Visit_Status); Invoices (Books_Invoice_Number, Invoice_Record_Status); Partner_Rates (Partner_Location_Link, Partner_Rate_Status, Rate_Amount, Rate_Type); Referrals_Main (Employee_Link, Facility_Name, Facility_Phone, ID, Partner_Branch, Partner_Branch_Link, Partner_ID, Partner_Link, Partner_Location_Label, Partner_Organization, Patient_Address, Patient_DOB, Patient_DOB1, Patient_First_Name, Patient_Full_Name, Patient_Gender, Patient_Hospice_ID, Patient_Last_Name, Patient_Location, Patient_Phone, Referral_Added_Time, Referral_Date, Referral_ID, Referral_Reason, Referral_Type)
- Calls: -
- Called by: -
- Integrations: -

## audit_pvs_billing_readiness

- Signature: Deluge.audit_pvs_billing_readiness(string p_mode, date p_from, date p_to) returns string
- .ds line: 9936
- Fetch: Encounter_PatientVisit (Visit_Completion_Date); Partner_Locations (ID); Partner_Rates (Current_Rate)
- Insert: -
- Update: -
- Delete: -
- Read: Encounter_PatientVisit (Additional_Charges, After_Hours_Fee, Billing_Branch, Clinical_Note_Type, Complexity_Charge, Complexity_Level, Diversion_Tracking, Employee_Email, Employee_First_Name, Employee_Initials, Employee_Last_Name, Employee_Name_Title, Employee_Title, Equipment_Charge_Amount, Facility_Name, Facility_Phone, Final_Clinical_Note, Hold_From_Invoicing, Invoice_Link, Invoice_Status, Other_Charges_Amount, PVS_ID, Partner_Branch, Partner_ID, Partner_Organization, Patient_Address, Patient_DOB, Patient_First_Name, Patient_Gender, Patient_Hospice_ID, Patient_Last_Name, Patient_Location, Patient_Phone, Reason_for_Referral, Referral_ID, Referral_Link, Super_Stat_Fee, Type_of_Entry, Type_of_Procedures, Visit_Completion_Date); Partner_Locations (ID, Partner_Location_Label); Partner_Rates (Partner_Location_Link, Rate_Amount, Rate_Type)
- Calls: -
- Called by: -
- Integrations: -

## backfill_assignment_ids

- Signature: Deluge.backfill_assignment_ids() returns void
- .ds line: 10418
- Fetch: Assignments (ID)
- Insert: -
- Update: -
- Delete: -
- Read: Assignments (Assignment_ID, ID)
- Calls: mint_assignment_id
- Called by: -
- Integrations: AppFunc

## backfill_contact_name_title

- Signature: Deluge.backfill_contact_name_title() returns string
- .ds line: 10434
- Fetch: Partner_Referral_Contacts (ID)
- Insert: -
- Update: Partner_Referral_Contacts (Partner_POC_Name_Title)
- Delete: -
- Read: Partner_Referral_Contacts (Partner_POC_First_Name, Partner_POC_Last_Name, Partner_POC_Title)
- Calls: -
- Called by: -
- Integrations: -

## backfill_current_rate

- Signature: Deluge.backfill_current_rate() returns void
- .ds line: 10464
- Fetch: Partner_Rates (ID)
- Insert: -
- Update: -
- Delete: -
- Read: Partner_Rates (ID)
- Calls: set_current_rate
- Called by: -
- Integrations: AppFunc

## backfill_data_issues

- Signature: Deluge.backfill_data_issues(string p_mode) returns string
- .ds line: 10471
- Fetch: Referrals_Main (ID)
- Insert: -
- Update: Referrals_Main (Data_Issues)
- Delete: -
- Read: Referrals_Main (Data_Issues, ID, Referral_ID)
- Calls: compute_data_issues
- Called by: -
- Integrations: AppFunc

## backfill_dm_full_names

- Signature: Deluge.backfill_dm_full_names() returns void
- .ds line: 10524
- Fetch: Referrals_Main (AC_Full_Name)
- Insert: -
- Update: Referrals_Main (AC_Full_Name)
- Delete: -
- Read: Referrals_Main (AC_First_Name, AC_Last_Name)
- Calls: -
- Called by: -
- Integrations: -

## backfill_employee_ids

- Signature: Deluge.backfill_employee_ids() returns void
- .ds line: 10557
- Fetch: Employees (ID)
- Insert: -
- Update: -
- Delete: -
- Read: Employees (Employee_ID, ID)
- Calls: mint_employee_id
- Called by: -
- Integrations: AppFunc

## backfill_employee_initials

- Signature: Deluge.backfill_employee_initials() returns string
- .ds line: 10573
- Fetch: Employees (Employee_Initials)
- Insert: -
- Update: Employees (Employee_Initials)
- Delete: -
- Read: Employees (Employee_First_Name, Employee_Last_Name)
- Calls: -
- Called by: -
- Integrations: -

## backfill_employee_name_title

- Signature: Deluge.backfill_employee_name_title(string pMode) returns string
- .ds line: 10595
- Fetch: Employees (ID)
- Insert: -
- Update: Employees (Employee_Name_Title)
- Delete: -
- Read: Employees (Employee_First_Name, Employee_ID, Employee_Last_Name, Employee_Name_Title, Employee_Title)
- Calls: -
- Called by: -
- Integrations: -

## backfill_employee_phone_format

- Signature: Deluge.backfill_employee_phone_format() returns void
- .ds line: 10663
- Fetch: Employees (ID)
- Insert: -
- Update: Employees (Employee_Phone)
- Delete: -
- Read: Employees (Employee_Phone)
- Calls: -
- Called by: -
- Integrations: -

## backfill_location_ids

- Signature: Deluge.backfill_location_ids() returns void
- .ds line: 10686
- Fetch: Partner_Locations (ID)
- Insert: -
- Update: -
- Delete: -
- Read: Partner_Locations (ID, Partner_Location_ID)
- Calls: mint_location_id
- Called by: -
- Integrations: AppFunc

## backfill_location_labels

- Signature: Deluge.backfill_location_labels(string p_mode) returns string
- .ds line: 10702
- Fetch: Partner_Locations (ID); Partners (ID)
- Insert: -
- Update: Partner_Locations (Partner_Location_Label)
- Delete: -
- Read: Partner_Locations (Partner_Link, Partner_Location_Label, Partner_Location_Name); Partners (Partner_Display_Name)
- Calls: -
- Called by: -
- Integrations: -

## backfill_mint_missing_referral_ids

- Signature: Deluge.backfill_mint_missing_referral_ids(string p_mode, string p_scope) returns string
- .ds line: 10757
- Fetch: Referrals_Main (ID, Referral_ID); Sequence_Tracker (Object_Prefix)
- Insert: -
- Update: -
- Delete: -
- Read: Referrals_Main (ID, Patient_Last_Name, Referral_ID); Sequence_Tracker (Object_Sequence)
- Calls: mint_referral_id
- Called by: -
- Integrations: AppFunc

## backfill_note_finalized_time

- Signature: Deluge.backfill_note_finalized_time(bool p_commit) returns string
- .ds line: 10839
- Fetch: Encounter_PatientVisit (Clinical_Note_Type, Note_Finalized_Time)
- Insert: -
- Update: Encounter_PatientVisit (Note_Finalized_Time)
- Delete: -
- Read: Encounter_PatientVisit (Added_Time, Clinical_Note_Type, PVS_ID)
- Calls: -
- Called by: -
- Integrations: -

## backfill_partner_ids

- Signature: Deluge.backfill_partner_ids() returns void
- .ds line: 10877
- Fetch: Partners (ID)
- Insert: -
- Update: -
- Delete: -
- Read: Partners (ID, Partner_ID)
- Calls: mint_partner_id
- Called by: -
- Integrations: AppFunc

## backfill_partner_poc_name_title

- Signature: Deluge.backfill_partner_poc_name_title() returns void
- .ds line: 10893
- Fetch: Referrals_Main (ID)
- Insert: -
- Update: -
- Delete: -
- Read: Referrals_Main (ID, Partner_POC_Name_Title)
- Calls: set_partner_poc_name_title
- Called by: -
- Integrations: AppFunc

## backfill_partner_resolver

- Signature: Deluge.backfill_partner_resolver(string p_mode, string p_target, int p_from, int p_to) returns string
- .ds line: 10909
- Fetch: Encounter_PatientVisit (Billing_Branch, Partner_Branch, Partner_Location_Label, Partner_Organization); Partner_Locations (ID); Referrals_Main (ID)
- Insert: -
- Update: Encounter_PatientVisit (Billing_Branch, Partner_Branch, Partner_Location_Label, Partner_Organization); Referrals_Main (Partner_Branch, Partner_Branch_Link, Partner_ID, Partner_ID_Stamp, Partner_Link, Partner_Location_Label, Partner_Organization)
- Delete: -
- Read: Encounter_PatientVisit (Billing_Branch, ID, PVS_ID, Partner_Branch, Partner_Location_Label, Partner_Organization, Referral_Link); Partner_Locations (ID, Partner_Location_ID); Referrals_Main (ID, Partner_Branch, Partner_Branch_Link, Partner_ID, Partner_ID_Stamp, Partner_Link, Partner_Location_Label, Partner_Organization, Partner_POC_Email, Referral_ID)
- Calls: partner_branch_values, resolve_branch_id
- Called by: -
- Integrations: AppFunc

## backfill_patient_dob

- Signature: Deluge.backfill_patient_dob(string p_mode) returns string
- .ds line: 11181
- Fetch: Referrals_Main (Patient_DOB)
- Insert: -
- Update: Referrals_Main (Patient_DOB)
- Delete: -
- Read: Referrals_Main (ID, Patient_DOB1, Referral_ID)
- Calls: -
- Called by: -
- Integrations: -

## backfill_patient_full_addresses

- Signature: Deluge.backfill_patient_full_addresses() returns void
- .ds line: 11296
- Fetch: Referrals_Main (Patient_Full_Address)
- Insert: -
- Update: Referrals_Main (Patient_Full_Address)
- Delete: -
- Read: Referrals_Main (Patient_Address)
- Calls: -
- Called by: -
- Integrations: -

## backfill_patient_full_names

- Signature: Deluge.backfill_patient_full_names() returns void
- .ds line: 11332
- Fetch: Referrals_Main (ID)
- Insert: -
- Update: -
- Delete: -
- Read: Referrals_Main (ID, Patient_Full_Name)
- Calls: set_patient_full_name
- Called by: -
- Integrations: AppFunc

## backfill_provider_login_email

- Signature: Deluge.backfill_provider_login_email(string pMode) returns string
- .ds line: 11348
- Fetch: Employees (ID); Encounter_PatientVisit (ID)
- Insert: -
- Update: Encounter_PatientVisit (Provider_Login_Email)
- Delete: -
- Read: Employees (Employee_Email, Employee_Portal_Email); Encounter_PatientVisit (Employee_Email, PVS_ID, Provider_Login_Email)
- Calls: -
- Called by: -
- Integrations: -

## backfill_pvs_3008_billing

- Signature: Deluge.backfill_pvs_3008_billing(string p_mode, date p_from, date p_to) returns string
- .ds line: 11421
- Fetch: Encounter_PatientVisit (Type_of_Entry); Partner_Locations (ID); Partner_Rates (Current_Rate, Partner_Location_Link, Rate_Type)
- Insert: -
- Update: Encounter_PatientVisit (Complexity_Charge, Complexity_Level, Visit_Completion_Date)
- Delete: -
- Read: Encounter_PatientVisit (Billing_Branch, Cares_3008_Completion_Date, Complexity_Charge, Complexity_Level, Invoice_Link, Invoice_Status, PVS_ID, Visit_Completion_Date); Partner_Locations (Partner_Location_Label); Partner_Rates (Rate_Amount)
- Calls: -
- Called by: -
- Integrations: -

## backfill_pvs_address_from_referral

- Signature: Deluge.backfill_pvs_address_from_referral() returns string
- .ds line: 11603
- Fetch: Encounter_PatientVisit (Referral_Link); Referrals_Main (ID)
- Insert: -
- Update: Encounter_PatientVisit
- Delete: -
- Read: Encounter_PatientVisit (Patient_Address, Referral_Link); Referrals_Main (Patient_Address)
- Calls: -
- Called by: -
- Integrations: -

## backfill_pvs_billing_branch

- Signature: Deluge.backfill_pvs_billing_branch(string p_mode) returns map
- .ds line: 11646
- Fetch: Encounter_PatientVisit (Billing_Branch, Referral_Link); Partner_Locations (ID, Partner_Location_Name); Partner_Rates (Current_Rate, Partner_Location_Link, Rate_Type); Referrals_Main (ID)
- Insert: -
- Update: Encounter_PatientVisit (Billing_Branch, Complexity_Charge, Partner_Branch, Partner_Location_Label, Partner_Organization)
- Delete: -
- Read: Encounter_PatientVisit (Billing_Branch, Complexity_Level, PVS_ID, Referral_Link); Partner_Locations (ID, Partner_Link, Partner_Location_Label, Partner_Location_Name); Partner_Rates (Rate_Amount); Partners (Partner_Display_Name); Referrals_Main (ID, Partner_Branch, Partner_Branch_Link, Partner_Organization, Referral_ID)
- Calls: -
- Called by: -
- Integrations: -

## backfill_pvs_complexity_charge

- Signature: Deluge.backfill_pvs_complexity_charge(string p_mode, string p_pvsIds) returns string
- .ds line: 11774
- Fetch: Encounter_PatientVisit (ID, PVS_ID); Partner_Locations (ID); Partner_Rates (Current_Rate, Partner_Location_Link, Rate_Type)
- Insert: -
- Update: Encounter_PatientVisit (Complexity_Charge)
- Delete: -
- Read: Encounter_PatientVisit (Billing_Branch, Complexity_Charge, Complexity_Level, ID, PVS_ID); Partner_Locations (Partner_Location_Label); Partner_Rates (Rate_Amount)
- Calls: -
- Called by: -
- Integrations: -

## backfill_pvs_employee_email

- Signature: Deluge.backfill_pvs_employee_email() returns string
- .ds line: 11922
- Fetch: Employees (ID); Encounter_PatientVisit (Employee_Last_Name)
- Insert: -
- Update: Encounter_PatientVisit (Employee_Email, Employee_Initials, Employee_Name_Title, Employee_Title)
- Delete: -
- Read: Employees (Employee_Email, Employee_First_Name, Employee_Initials, Employee_Last_Name, Employee_Name_Title, Employee_Title); Encounter_PatientVisit (Employee_Email, Employee_First_Name, Employee_Initials, Employee_Last_Name, Employee_Name_Title, Employee_Title)
- Calls: -
- Called by: -
- Integrations: -

## backfill_pvs_employee_email_alias

- Signature: Deluge.backfill_pvs_employee_email_alias(string pMode, string pOldEmail, string pNewEmail) returns string
- .ds line: 11989
- Fetch: Encounter_PatientVisit (ID)
- Insert: -
- Update: Encounter_PatientVisit (Employee_Email)
- Delete: -
- Read: Encounter_PatientVisit (Employee_Email, Employee_Initials, PVS_ID)
- Calls: -
- Called by: -
- Integrations: -

## backfill_pvs_employee_initials

- Signature: Deluge.backfill_pvs_employee_initials() returns string
- .ds line: 12028
- Fetch: Employees (ID); Encounter_PatientVisit (Employee_Email, Employee_Initials)
- Insert: -
- Update: Encounter_PatientVisit (Employee_Initials)
- Delete: -
- Read: Employees (Employee_Email, Employee_Initials); Encounter_PatientVisit (Employee_Email)
- Calls: -
- Called by: -
- Integrations: -

## backfill_pvs_employee_link

- Signature: Deluge.backfill_pvs_employee_link(string pMode) returns string
- .ds line: 12055
- Fetch: Employees (ID); Encounter_PatientVisit (ID)
- Insert: -
- Update: Encounter_PatientVisit (Employee_Link)
- Delete: -
- Read: Employees (Employee_Email, Employee_Name_Title, Employee_Portal_Email, ID); Encounter_PatientVisit (Employee_Email, Employee_Link, PVS_ID)
- Calls: -
- Called by: -
- Integrations: -

## backfill_pvs_employee_link_range

- Signature: Deluge.backfill_pvs_employee_link_range(string p_mode, date p_from, date p_to) returns string
- .ds line: 12124
- Fetch: Employees (ID); Encounter_PatientVisit (Employee_Link, Visit_Completion_Date)
- Insert: -
- Update: Encounter_PatientVisit (Employee_Link)
- Delete: -
- Read: Employees (Employee_Email, Employee_First_Name, Employee_Initials, Employee_Last_Name, Employee_Name_Title, Employee_Portal_Email, ID); Encounter_PatientVisit (Employee_Email, Employee_Initials, ID, PVS_ID)
- Calls: -
- Called by: -
- Integrations: -

## backfill_pvs_from_referral

- Signature: Deluge.backfill_pvs_from_referral() returns string
- .ds line: 12216
- Fetch: Encounter_PatientVisit (Referral_Link); Referrals_Main (ID)
- Insert: -
- Update: Encounter_PatientVisit (Additional_Information, Advanced_Directives_Details, Facility_Phone, Facility_Room_Number, List_Patient_Allergies, List_Patient_Anticoagulants, Partner_ICD_Codes, Partner_ID, Partner_ID_Stamp, Partner_Location_Label, Partner_POC_Email, Partner_POC_First_Name, Partner_POC_Last_Name, Partner_POC_Name_Title, Partner_POC_Phone, Partner_POC_Team, Partner_POC_Title, Patient_Full_Name_1, Patient_Full_Name_2, Patient_Hospice_ID, Patient_MI, Patient_Phone, Patient_SSN, Reason_for_Referral, Referral_ID_Stamp)
- Delete: -
- Read: Encounter_PatientVisit (Additional_Information, Advanced_Directives_Details, Facility_Phone, Facility_Room_Number, List_Patient_Allergies, List_Patient_Anticoagulants, Partner_ICD_Codes, Partner_ID, Partner_ID_Stamp, Partner_Location_Label, Partner_POC_Email, Partner_POC_First_Name, Partner_POC_Last_Name, Partner_POC_Name_Title, Partner_POC_Phone, Partner_POC_Team, Partner_POC_Title, Patient_Address, Patient_Full_Name_1, Patient_Full_Name_2, Patient_Hospice_ID, Patient_MI, Patient_Phone, Patient_SSN, Reason_for_Referral, Referral_ID_Stamp, Referral_Link)
- Calls: -
- Called by: -
- Integrations: -

## backfill_pvs_ids

- Signature: Deluge.backfill_pvs_ids() returns string
- .ds line: 12430
- Fetch: Encounter_PatientVisit (ID); Sequence_Tracker (Object_Prefix)
- Insert: -
- Update: Encounter_PatientVisit (Has_Referral_ID, PVS_ID, PVS_Referral_ID); Sequence_Tracker (Object_Sequence)
- Delete: -
- Read: Encounter_PatientVisit (Employee_Initials, Has_Referral_ID, PVS_ID, PVS_Referral_ID, Referral_ID); Sequence_Tracker (Object_Sequence)
- Calls: -
- Called by: -
- Integrations: -

## backfill_pvs_invoice_status

- Signature: Deluge.backfill_pvs_invoice_status(string p_mode, date p_from, date p_to) returns string
- .ds line: 12547
- Fetch: Encounter_PatientVisit (ID, Visit_Completion_Date)
- Insert: -
- Update: Encounter_PatientVisit (Invoice_Status)
- Delete: -
- Read: Encounter_PatientVisit (ID, Invoice_Link, Invoice_Status, PVS_ID)
- Calls: -
- Called by: -
- Integrations: -

## backfill_pvs_link_by_cognito

- Signature: Deluge.backfill_pvs_link_by_cognito(string p_mode, string p_scope) returns string
- .ds line: 12603
- Fetch: Encounter_PatientVisit (ID, PVS_ID, Referral_ID, Referral_Link); Referrals_Main (Cognito_Referral_ID)
- Insert: -
- Update: Encounter_PatientVisit (Referral_Link)
- Delete: -
- Read: Encounter_PatientVisit (ID, PVS_ID, Referral_ID)
- Calls: -
- Called by: -
- Integrations: -

## backfill_pvs_note_placement

- Signature: Deluge.backfill_pvs_note_placement(string p_mode, date p_from, date p_to) returns string
- .ds line: 12734
- Fetch: Encounter_PatientVisit (ID, Visit_Completion_Date)
- Insert: -
- Update: Encounter_PatientVisit (Final_Clinical_Note, Notes_3008)
- Delete: -
- Read: Encounter_PatientVisit (Final_Clinical_Note, ID, Invoice_Link, Invoice_Status, Notes_3008, PVS_ID, Type_of_Entry)
- Calls: -
- Called by: -
- Integrations: -

## backfill_pvs_patient_full_address

- Signature: Deluge.backfill_pvs_patient_full_address() returns string
- .ds line: 12810
- Fetch: Encounter_PatientVisit (ID)
- Insert: -
- Update: Encounter_PatientVisit (Patient_Full_Address)
- Delete: -
- Read: Encounter_PatientVisit (Patient_Address, Patient_Full_Address)
- Calls: -
- Called by: -
- Integrations: -

## backfill_pvs_premium_fees

- Signature: Deluge.backfill_pvs_premium_fees(string p_confirm) returns string
- .ds line: 12866
- Fetch: Encounter_PatientVisit (Additional_Charges); Partner_Locations (ID); Partner_Rates (Current_Rate, Partner_Location_Link, Rate_Type)
- Insert: -
- Update: Encounter_PatientVisit (After_Hours_Fee, Super_Stat_Fee)
- Delete: -
- Read: Encounter_PatientVisit (Additional_Charges, After_Hours_Fee, Billing_Branch, Invoice_Link, PVS_ID, Super_Stat_Fee); Partner_Locations (Partner_Location_Label); Partner_Rates (Rate_Amount)
- Calls: -
- Called by: -
- Integrations: -

## backfill_pvs_provider_identity

- Signature: Deluge.backfill_pvs_provider_identity(string p_mode, string p_from, string p_to) returns string
- .ds line: 12993
- Fetch: Employees (ID); Encounter_PatientVisit (Visit_Completion_Date)
- Insert: -
- Update: Encounter_PatientVisit (Employee_Email, Employee_First_Name, Employee_Full_Name, Employee_Initials, Employee_Last_Name, Employee_Link, Employee_Name_Title, Employee_Title)
- Delete: -
- Read: Employees (Employee_Email, Employee_First_Name, Employee_Initials, Employee_Last_Name, Employee_Name_Title, Employee_Title, ID); Encounter_PatientVisit (Employee_Email, Employee_First_Name, Employee_Full_Name, Employee_Initials, Employee_Last_Name, Employee_Link, Employee_Name_Title, Employee_Title, Invoice_Status, PVS_ID)
- Calls: -
- Called by: -
- Integrations: -

## backfill_pvs_referral_date

- Signature: Deluge.backfill_pvs_referral_date(string p_mode, string p_pvsKey) returns string
- .ds line: 13198
- Fetch: Encounter_PatientVisit (ID, PVS_ID, Referral_Date); Referrals_Main (ID)
- Insert: -
- Update: Encounter_PatientVisit (Referral_Date)
- Delete: -
- Read: Encounter_PatientVisit (ID, PVS_ID, Referral_Date, Referral_Link); Referrals_Main (Referral_Date)
- Calls: -
- Called by: -
- Integrations: -

## backfill_pvs_referral_id_from_link

- Signature: Deluge.backfill_pvs_referral_id_from_link(string p_mode, string p_scope) returns string
- .ds line: 13334
- Fetch: Encounter_PatientVisit (ID, PVS_ID, Referral_Link); Referrals_Main (ID)
- Insert: -
- Update: Encounter_PatientVisit (PVS_Referral_ID, Referral_ID)
- Delete: -
- Read: Encounter_PatientVisit (ID, Invoice_Link, PVS_ID, Referral_ID, Referral_Link); Referrals_Main (Referral_ID)
- Calls: -
- Called by: -
- Integrations: -

## backfill_pvs_referral_source

- Signature: Deluge.backfill_pvs_referral_source(string p_mode, int p_limit) returns string
- .ds line: 13458
- Fetch: Encounter_PatientVisit (ID, Referral_Link)
- Insert: -
- Update: Encounter_PatientVisit (Referral_Source)
- Delete: -
- Read: Encounter_PatientVisit (ID, PVS_ID, Referral_Link, Referral_Source); Referrals_Main (Referral_Source)
- Calls: -
- Called by: -
- Integrations: -

## backfill_pvs_row_status

- Signature: Deluge.backfill_pvs_row_status(string p_mode, int p_limit) returns string
- .ds line: 13518
- Fetch: Encounter_PatientVisit (ID)
- Insert: -
- Update: Encounter_PatientVisit (Row_Status)
- Delete: -
- Read: Encounter_PatientVisit (ID, PVS_ID, Row_Status, Visit_Status)
- Calls: -
- Called by: -
- Integrations: -

## backfill_pvs_system_fields_range

- Signature: Deluge.backfill_pvs_system_fields_range(string p_mode, date p_from, date p_to) returns string
- .ds line: 13577
- Fetch: Encounter_PatientVisit (Visit_Completion_Date); Referrals_Main (ID)
- Insert: -
- Update: Encounter_PatientVisit (Reason_for_Referral, Referral_Date, Referral_Source, Row_Status, Visit_Status)
- Delete: -
- Read: Encounter_PatientVisit (ID, PVS_ID, Reason_for_Referral, Referral_Date, Referral_Link, Referral_Source, Row_Status, Visit_Status, Was_3008_Completed); Referrals_Main (ID, Referral_Date, Referral_Reason, Referral_Source)
- Calls: -
- Called by: -
- Integrations: -

## backfill_referral_added_time

- Signature: Deluge.backfill_referral_added_time() returns string
- .ds line: 13731
- Fetch: Referrals_Main (Referral_Added_Time)
- Insert: -
- Update: Referrals_Main (Referral_Added_Time)
- Delete: -
- Read: Referrals_Main (Added_Time)
- Calls: -
- Called by: -
- Integrations: -

## backfill_referral_branch

- Signature: Deluge.backfill_referral_branch() returns string
- .ds line: 13750
- Fetch: Partner_Locations (ID); Referrals_Main (Partner_Branch_Link)
- Insert: -
- Update: Referrals_Main (Partner_Branch, Partner_ID, Partner_Link, Partner_Location_Label, Partner_Organization)
- Delete: -
- Read: Partner_Locations (ID, Partner_Link, Partner_Location_Label, Partner_Location_Name); Partners (Partner_Display_Name, Partner_ID); Referrals_Main (Partner_Branch_Link)
- Calls: -
- Called by: -
- Integrations: -

## backfill_referral_branch_from_contact

- Signature: Deluge.backfill_referral_branch_from_contact() returns string
- .ds line: 13773
- Fetch: Partner_Referral_Contacts (Partner_POC_Email); Referrals_Main (Partner_Branch_Link)
- Insert: -
- Update: Referrals_Main (Partner_Branch_Link)
- Delete: -
- Read: Partner_Referral_Contacts (ID, Partner_Locations_Link); Referrals_Main (Partner_POC_Email)
- Calls: -
- Called by: -
- Integrations: -

## backfill_referral_date

- Signature: Deluge.backfill_referral_date(string p_mode) returns string
- .ds line: 13799
- Fetch: Referrals_Main (Referral_Date)
- Insert: -
- Update: Referrals_Main (Referral_Date)
- Delete: -
- Read: Referrals_Main (ID, Referral_Added_Time, Referral_ID)
- Calls: -
- Called by: -
- Integrations: -

## backfill_referral_employee_link

- Signature: Deluge.backfill_referral_employee_link(string pMode) returns string
- .ds line: 13853
- Fetch: Assignments (Employee_Link, Referral_Link); Employees (ID); Referrals_Main (ID)
- Insert: -
- Update: Referrals_Main (Employee_Link)
- Delete: -
- Read: Assignments (Employee_Link, Referral_Link); Employees (Employee_Name_Title, ID); Referrals_Main (Employee_Link, ID, Referral_ID)
- Calls: -
- Called by: -
- Integrations: -

## backfill_referral_id_from_token

- Signature: Deluge.backfill_referral_id_from_token() returns string
- .ds line: 13943
- Fetch: Referrals_Main (ID)
- Insert: -
- Update: Referrals_Main (Form_Token, Referral_ID)
- Delete: -
- Read: Referrals_Main (Form_Token, Referral_ID)
- Calls: -
- Called by: -
- Integrations: -

## backfill_referral_id_stamp

- Signature: Deluge.backfill_referral_id_stamp() returns void
- .ds line: 13980
- Fetch: Referrals_Main (ID)
- Insert: -
- Update: Referrals_Main (Referral_ID_Stamp)
- Delete: -
- Read: Referrals_Main (ID, Referral_ID_Stamp)
- Calls: -
- Called by: -
- Integrations: -

## backfill_referral_ids

- Signature: Deluge.backfill_referral_ids() returns void
- .ds line: 13927
- Fetch: Referrals_Main (ID)
- Insert: -
- Update: -
- Delete: -
- Read: Referrals_Main (ID, Referral_ID)
- Calls: mint_referral_id
- Called by: -
- Integrations: AppFunc

## backfill_referral_partner_fields

- Signature: Deluge.backfill_referral_partner_fields(string p_mode) returns string
- .ds line: 13996
- Fetch: Partner_Locations (ID); Referrals_Main (ID)
- Insert: -
- Update: Referrals_Main (Partner_Branch, Partner_Branch_Link, Partner_ID, Partner_ID_Stamp, Partner_Link, Partner_Location_Label, Partner_Organization)
- Delete: -
- Read: Partner_Locations (ID, Partner_Link, Partner_Location_Label, Partner_Location_Name); Partners (Partner_Display_Name, Partner_ID); Referrals_Main (ID, Partner_Branch, Partner_Branch_Link, Partner_ID, Partner_Link, Partner_Location_Label, Partner_Organization, Referral_ID)
- Calls: -
- Called by: -
- Integrations: -

## backfill_referral_uploads

- Signature: Deluge.backfill_referral_uploads(string p_mode, string p_refKey) returns string
- .ds line: 14141
- Fetch: Referrals_Main (Files_3008_URLs, General_Files_URLs, ID, Imaging_Orders_URLs, Referral_ID)
- Insert: -
- Update: -
- Delete: -
- Read: Referrals_Main (File_Upload_3008, Files_3008_URLs, General_Files_URLs, General_Files_Upload, ID, Imaging_Orders_URLs, Imaging_Orders_Upload, Partner_Branch, Partner_Organization, Patient_First_Name, Patient_Last_Name, Referral_ID)
- Calls: -
- Called by: -
- Integrations: HTTP

## build_3008_email_html

- Signature: Deluge.build_3008_email_html(int p_recId) returns map
- .ds line: 14361
- Fetch: Referral_Files (Referrals_Main); Referrals_Main (ID)
- Insert: -
- Update: -
- Delete: -
- Read: Referral_Files (File_Name); Referrals_Main (AC_Full_Name, AC_Phone, Facility_Name, Facility_Phone, Facility_Room_Number, Has_Additional_Contact, ID, Partner_Branch, Partner_Organization, Partner_POC_Email, Partner_POC_Name_Title, Partner_POC_Phone, Partner_POC_Team, Patient_DOB, Patient_Full_Address, Patient_Full_Name, Patient_Gender, Patient_Hospice_ID, Patient_Location, Patient_Phone, Referral_Date, Referral_ID, Referral_Type)
- Calls: -
- Called by: function resend_referral_notifications, function send_3008_notification
- Integrations: -

## build_console_docs

- Signature: Deluge.build_console_docs(string pFaxID, string pToName, string pToPartner, string pToFax, string pToAttn, string pRemarks, list pPvsIds, list pUploadNames) returns map
- .ds line: 14579
- Fetch: Encounter_PatientVisit (ID); Referrals_Main (ID)
- Insert: -
- Update: -
- Delete: -
- Read: Encounter_PatientVisit (Clinical_Note_Type, Complexity_Level, Employee_Name_Title, Final_Clinical_Note, ID, Modified_Time, PVS_ID, Partner_Branch, Partner_Organization, Partner_POC_Name_Title, Partner_POC_Team, Patient_DOB, Patient_Full_Name_1, Patient_Gender, Provider_ICD_Print, Referral_ID, Referral_Link, Type_of_Procedures, Visit_Completion_Date, Visit_Status); Referrals_Main (Referral_Date)
- Calls: -
- Called by: function api_fax_send_console, workflow PVS_Fax_Review/PVS_Fax_Review_On_Load
- Integrations: -

## build_creator_attachments

- Signature: Deluge.build_creator_attachments(int p_recId, string p_token) returns list
- .ds line: 14743
- Fetch: Referrals_Main (ID)
- Insert: -
- Update: -
- Delete: -
- Read: Referrals_Main (File_Upload_3008, General_Files_Upload, Imaging_Orders_Upload)
- Calls: -
- Called by: function resend_referral_notifications
- Integrations: HTTP

## build_imaging_email_html

- Signature: Deluge.build_imaging_email_html(int p_recId) returns map
- .ds line: 14853
- Fetch: Referral_Files (Referrals_Main); Referrals_Main (ID)
- Insert: -
- Update: -
- Delete: -
- Read: Referral_Files (File_Name); Referrals_Main (AC_Full_Name, AC_Phone, Facility_Name, Facility_Phone, Facility_Room_Number, Has_Additional_Contact, ID, Imaging_Body_Site, Imaging_Order_Indication, Imaging_Type_Order, Partner_Branch, Partner_Organization, Partner_POC_Email, Partner_POC_Name_Title, Partner_POC_Phone, Partner_POC_Team, Patient_DOB, Patient_Full_Address, Patient_Full_Name, Patient_Gender, Patient_Hospice_ID, Patient_Location, Patient_Phone, Referral_Date, Referral_ID, Referral_Reason, Referral_Type)
- Calls: -
- Called by: function resend_referral_notifications, function send_imaging_notification
- Integrations: -

## build_pvs_fax_html

- Signature: Deluge.build_pvs_fax_html(int pPvsID, string pFaxID, string pToName, string pToPartner, string pToFax, string pToAttn, string pRemarks, list pImageUrls) returns string
- .ds line: 15085
- Fetch: Encounter_PatientVisit (ID); Partner_Locations (ID); Referrals_Main (ID)
- Insert: -
- Update: -
- Delete: -
- Read: Encounter_PatientVisit (Billing_Branch, Clinical_Note_Type, Complexity_Level, Employee_Name_Title, Final_Clinical_Note, Modified_Time, PVS_ID, Partner_Branch, Partner_Organization, Partner_POC_Name_Title, Partner_POC_Team, Patient_DOB, Patient_Full_Name_1, Patient_Gender, Patient_Hospice_ID, Provider_ICD_Print, Referral_ID, Referral_Link, Type_of_Procedures, Visit_Completion_Date, Visit_Status); Partner_Locations (Partner_Location_Label); Referrals_Main (Patient_Hospice_ID, Referral_Date)
- Calls: fmt_phone_display
- Called by: function send_pvs_fax
- Integrations: AppFunc

## build_pvs_note_html

- Signature: Deluge.build_pvs_note_html(map pVals) returns string
- .ds line: 15223
- Fetch: -
- Insert: -
- Update: -
- Delete: -
- Read: -
- Calls: -
- Called by: workflow Encounter_PatientVisit/Fax_This_Note_Preview_And
- Integrations: -

## build_referral_confirmation_html

- Signature: Deluge.build_referral_confirmation_html(int p_recId) returns map
- .ds line: 15267
- Fetch: Referrals_Main (ID)
- Insert: -
- Update: -
- Delete: -
- Read: Referrals_Main (Partner_POC_Name_Title, Patient_Full_Name, Referral_Date, Referral_ID, Referral_Type)
- Calls: -
- Called by: function send_referral_confirmation
- Integrations: -

## build_referral_email_html

- Signature: Deluge.build_referral_email_html(int p_recId) returns map
- .ds line: 15398
- Fetch: Referral_Files (Referrals_Main); Referrals_Main (ID)
- Insert: -
- Update: -
- Delete: -
- Read: Referral_Files (File_Name); Referrals_Main (AC_Full_Name, AC_Phone, Advanced_Directives_Details, Facility_Name, Facility_Phone, Facility_Room_Number, Has_Additional_Contact, ID, Imaging_Body_Site, Imaging_Order_Indication, Imaging_Type_Order, List_Patient_Allergies, List_Patient_Anticoagulants, Partner_Branch, Partner_Organization, Partner_POC_Email, Partner_POC_Name_Title, Partner_POC_Phone, Partner_POC_Team, Patient_DOB, Patient_Full_Address, Patient_Full_Name, Patient_Gender, Patient_Hospice_ID, Patient_Location, Patient_Phone, Referral_Date, Referral_ID, Referral_Reason, Referral_Type, X_Ray_Needed)
- Calls: -
- Called by: function resend_referral_notifications, function send_referral_notification
- Integrations: -

## build_zepto_attachments

- Signature: Deluge.build_zepto_attachments(int p_refId, string p_token) returns list
- .ds line: 15654
- Fetch: Referrals_Main (ID)
- Insert: -
- Update: -
- Delete: -
- Read: Referrals_Main (Files_3008_URLs, General_Files_URLs, Imaging_Orders_URLs)
- Calls: -
- Called by: function send_3008_notification, function send_imaging_notification, function send_referral_notification
- Integrations: HTTP

## compute_data_issues

- Signature: Deluge.compute_data_issues(int p_recId) returns string
- .ds line: 15737
- Fetch: Referrals_Main (ID)
- Insert: -
- Update: -
- Delete: -
- Read: Referrals_Main (AC_First_Name, AC_Last_Name, AC_Phone, AC_Relationship_to_Patient, Advanced_Directives_Details, Facility_Name, Facility_Phone, Facility_Room_Number, Files_3008_URLs, Has_Additional_Contact, Imaging_Body_Site, Imaging_Order_Indication, Imaging_Orders_URLs, Imaging_Type_Order, Partner_Location_Label, Partner_Organization, Partner_POC_Email, Partner_POC_First_Name, Partner_POC_Last_Name, Patient_Address, Patient_DOB, Patient_DOB1, Patient_First_Name, Patient_Has_Advanced_Directives, Patient_Hospice_ID, Patient_Last_Name, Patient_Location, Patient_Phone, Patient_SSN, Referral_Reason, Referral_Type, X_Ray_Needed)
- Calls: parse_patient_dob
- Called by: function backfill_data_issues, function run_import_backfills, workflow Referrals_Main/Referral_Data_Issues_Chec, workflow Referrals_Main/Referral_Data_Issues_Sync
- Integrations: AppFunc

## create_3008_pvs_july

- Signature: Deluge.create_3008_pvs_july(string pMode) returns string
- .ds line: 15889
- Fetch: Employees (Employee_First_Name, Employee_Last_Name, Employee_Status); Encounter_PatientVisit (Referral_Link, Type_of_Entry); Partner_Rates (Current_Rate, Partner_Location_Link, Rate_Type); Referrals_Main (Referral_ID); Sequence_Tracker (Object_Prefix)
- Insert: Encounter_PatientVisit (Added_User, Billing_Branch, Cares_3008_Completion_Date, Complexity_Charge, Complexity_Level, Employee_Email, Employee_First_Name, Employee_Full_Name, Employee_Initials, Employee_Last_Name, Employee_Name_Title, Employee_Title, Facility_Name, Facility_Phone, Facility_Room_Number, Has_Referral_ID, Hold_From_Invoicing, Invoice_Status, PVS_ID, Partner_Branch, Partner_ID, Partner_Organization, Partner_POC_Email, Partner_POC_Name_Title, Partner_POC_Phone, Partner_POC_Team, Patient_DOB, Patient_First_Name, Patient_Full_Address, Patient_Full_Name_1, Patient_Full_Name_2, Patient_Gender, Patient_Hospice_ID, Patient_Last_Name, Patient_Location, Patient_MI, Patient_Phone, Reason_for_Referral, Referral_ID, Referral_Link, Type_of_Entry, Visit_Completion_Date, Was_3008_Completed)
- Update: Sequence_Tracker (Object_Sequence)
- Delete: -
- Read: Employees (Employee_Email, Employee_First_Name, Employee_Initials, Employee_Last_Name, Employee_Name_Title, Employee_Title); Partner_Rates (Rate_Amount); Referrals_Main (Facility_Name, Facility_Phone, Facility_Room_Number, ID, Partner_Branch, Partner_Branch_Link, Partner_ID, Partner_Location_Label, Partner_Organization, Partner_POC_Email, Partner_POC_Name_Title, Partner_POC_Phone, Partner_POC_Team, Patient_DOB, Patient_First_Name, Patient_Full_Address, Patient_Full_Name, Patient_Gender, Patient_Hospice_ID, Patient_Last_Name, Patient_Location, Patient_MI, Patient_Phone, Referral_Reason); Sequence_Tracker (Object_Sequence)
- Calls: -
- Called by: -
- Integrations: -

## create_3008_pvs_sept

- Signature: Deluge.create_3008_pvs_sept(string pMode) returns string
- .ds line: 16082
- Fetch: Employees (Employee_First_Name, Employee_Last_Name, Employee_Status); Encounter_PatientVisit (Referral_Link, Type_of_Entry); Partner_Rates (Current_Rate, Partner_Location_Link, Rate_Type); Referrals_Main (Referral_ID); Sequence_Tracker (Object_Prefix)
- Insert: Encounter_PatientVisit (Added_User, Billing_Branch, Cares_3008_Completion_Date, Complexity_Charge, Complexity_Level, Employee_Email, Employee_First_Name, Employee_Full_Name, Employee_Initials, Employee_Last_Name, Employee_Link, Employee_Name_Title, Employee_Title, Facility_Name, Facility_Phone, Facility_Room_Number, Has_Referral_ID, Hold_From_Invoicing, Invoice_Status, PVS_ID, Partner_Branch, Partner_ID, Partner_Organization, Partner_POC_Email, Partner_POC_Name_Title, Partner_POC_Phone, Partner_POC_Team, Patient_DOB, Patient_First_Name, Patient_Full_Address, Patient_Full_Name_1, Patient_Full_Name_2, Patient_Gender, Patient_Hospice_ID, Patient_Last_Name, Patient_Location, Patient_MI, Patient_Phone, Reason_for_Referral, Referral_ID, Referral_Link, Type_of_Entry, Visit_Completion_Date, Was_3008_Completed)
- Update: Sequence_Tracker (Object_Sequence)
- Delete: -
- Read: Employees (Employee_Email, Employee_First_Name, Employee_Initials, Employee_Last_Name, Employee_Name_Title, Employee_Title, ID); Partner_Rates (Rate_Amount); Referrals_Main (Facility_Name, Facility_Phone, Facility_Room_Number, ID, Partner_Branch, Partner_Branch_Link, Partner_ID, Partner_Location_Label, Partner_Organization, Partner_POC_Email, Partner_POC_Name_Title, Partner_POC_Phone, Partner_POC_Team, Patient_DOB, Patient_First_Name, Patient_Full_Address, Patient_Full_Name, Patient_Gender, Patient_Hospice_ID, Patient_Last_Name, Patient_Location, Patient_MI, Patient_Phone, Referral_Reason); Sequence_Tracker (Object_Sequence)
- Calls: -
- Called by: -
- Integrations: -

## create_books_customers

- Signature: Deluge.create_books_customers() returns string
- .ds line: 16235
- Fetch: Partner_Billing_Contacts (Partner_Billing_POC_Status, Partner_Location_Link); Partner_Locations (ID, Partner_Location_Status)
- Insert: -
- Update: Partner_Locations (Books_Customer_ID)
- Delete: -
- Read: Partner_Billing_Contacts (ID, Partner_Billing_Address, Partner_Billing_POC_Email, Partner_Billing_POC_First_Name, Partner_Billing_POC_Last_Name, Partner_Billing_POC_Phone); Partner_Locations (Books_Customer_ID, ID, Partner_Location_Label, Partner_Location_Name)
- Calls: -
- Called by: -
- Integrations: HTTP

## create_invoice_from_selection

- Signature: Deluge.create_invoice_from_selection(list p_pvsIds, string p_replacesInvoice) returns string
- .ds line: 16325
- Fetch: Encounter_PatientVisit (ID); Invoices (Books_Invoice_Number, ID); Partner_Locations (ID); Referrals_Main (ID)
- Insert: Invoices (Added_User, Books_Customer_ID, Created_By, Invoice_Date, Invoice_Record_Status, Invoice_Total, Partner_Link, Partner_Location_Link, Service_Date_From, Service_Date_To, Visit_Count)
- Update: Encounter_PatientVisit (Invoice_Link, Invoice_Status); Invoices (Books_Invoice_ID, Books_Invoice_Number, Books_Sync_Message, Books_Sync_Timestamp, Invoice_Record_Status, Replaces_Invoice_Number, Revision_Date)
- Delete: -
- Read: Encounter_PatientVisit (After_Hours_Fee, Billing_Branch, Complexity_Charge, Complexity_Level, Equipment_Charge_Amount, ID, Invoice_Link, Other_Charges_Amount, PVS_ID, Patient_DOB, Patient_Full_Name_1, Patient_Hospice_ID, Reason_for_Referral, Referral_Link, Super_Stat_Fee, Visit_Completion_Date); Invoices (ID, Invoice_Date, Invoice_Record_Status); Partner_Locations (Books_Customer_ID, ID, Partner_Link, Partner_Location_Name); Referrals_Main (ID, Referral_Date)
- Calls: -
- Called by: function run_invoice_batch
- Integrations: Books, HTTP

## dash_metrics

- Signature: Deluge.dash_metrics(date p_monthStart) returns map
- .ds line: 16597
- Fetch: Assignments (Referral_Link); Employees (ID); Encounter_PatientVisit (Visit_Completion_Date); Invoices (Invoice_Record_Status); Partners (ID); Referrals_Main (Referral_Date)
- Insert: -
- Update: -
- Delete: -
- Read: Assignments (Employee_Link, ID, Patient_First_Name, Patient_Last_Name, Referral_Link, Visit_Status); Employees (Employee_First_Name, Employee_Last_Name, ID); Encounter_PatientVisit (After_Hours_Fee, Clinical_Note_Type, Complexity_Charge, Complexity_Level, Employee_Full_Name, Equipment_Charge_Amount, Hold_From_Invoicing, ID, Invoice_Link, Note_Finalized_Time, Other_Charges_Amount, Referral_ID, Referral_Link, Row_Status, Super_Stat_Fee, Type_of_Entry, Visit_Completion_Date, Visit_Status); Invoices (ID); Partners (ID, Partner_Display_Name); Referrals_Main (ID, Partner_Link, Patient_Full_Name, Referral_Date, Referral_ID, Referral_Type)
- Calls: -
- Called by: page Drilldown_Data
- Integrations: -

## dash_metrics_range

- Signature: Deluge.dash_metrics_range(date p_from, date p_to, string p_mode, string p_key) returns map
- .ds line: 17105
- Fetch: Assignments (Referral_Link); Employees (ID); Encounter_PatientVisit (Referral_ID, Referral_Link, Visit_Completion_Date); Invoices (Invoice_Record_Status); Partners (ID); Referrals_Main (Referral_Date)
- Insert: -
- Update: -
- Delete: -
- Read: Assignments (Employee_Link, ID, Patient_First_Name, Patient_Last_Name, Referral_Link, Visit_Status); Employees (Employee_First_Name, Employee_Last_Name, ID); Encounter_PatientVisit (After_Hours_Fee, Clinical_Note_Type, Complexity_Charge, Complexity_Level, Diversion_Tracking, Employee_Full_Name, Equipment_Charge_Amount, Hold_From_Invoicing, ID, Invoice_Link, Note_Finalized_Time, Other_Charges_Amount, Referral_Link, Row_Status, Super_Stat_Fee, Type_of_Entry, Visit_Completion_Date, Visit_Status); Invoices (ID); Partners (ID, Partner_Display_Name); Referrals_Main (ID, Partner_Link, Patient_Full_Name, Referral_Date, Referral_ID, Referral_Type)
- Calls: -
- Called by: page Reports
- Integrations: -

## diag_3008_batch_eligibility

- Signature: Deluge.diag_3008_batch_eligibility(date p_from, date p_to) returns string
- .ds line: 17722
- Fetch: Encounter_PatientVisit (Type_of_Entry); Partner_Locations (ID)
- Insert: -
- Update: -
- Delete: -
- Read: Encounter_PatientVisit (Billing_Branch, Complexity_Charge, Complexity_Level, Hold_From_Invoicing, Invoice_Link, Invoice_Status, PVS_ID, Visit_Completion_Date); Partner_Locations (Partner_Location_Label)
- Calls: -
- Called by: -
- Integrations: -

## diag_3008_draft_vs_invoiced

- Signature: Deluge.diag_3008_draft_vs_invoiced(date p_from, date p_to) returns string
- .ds line: 17842
- Fetch: Encounter_PatientVisit (Type_of_Entry, Visit_Completion_Date); Invoices (ID); Partner_Locations (ID)
- Insert: -
- Update: -
- Delete: -
- Read: Encounter_PatientVisit (Billing_Branch, Hold_From_Invoicing, ID, Invoice_Link, Invoice_Status, PVS_ID, Referral_ID, Referral_Link, Visit_Completion_Date); Invoices (Books_Invoice_Number, ID); Partner_Locations (Partner_Location_Label)
- Calls: -
- Called by: -
- Integrations: -

## diag_3008_duplicates

- Signature: Deluge.diag_3008_duplicates() returns string
- .ds line: 17934
- Fetch: Encounter_PatientVisit (Type_of_Entry); Partner_Locations (ID)
- Insert: -
- Update: -
- Delete: -
- Read: Encounter_PatientVisit (Billing_Branch, Complexity_Charge, Hold_From_Invoicing, Invoice_Link, Invoice_Status, PVS_ID, PVS_Referral_ID, Patient_DOB, Patient_Full_Name_1, Referral_ID, Visit_Completion_Date); Partner_Locations (Partner_Location_Label)
- Calls: -
- Called by: -
- Integrations: -

## diag_3008_link_check

- Signature: Deluge.diag_3008_link_check(date p_from, date p_to) returns string
- .ds line: 18019
- Fetch: Encounter_PatientVisit (Referral_ID, Referral_Link, Type_of_Entry); Referrals_Main (ID, Referral_Type)
- Insert: -
- Update: -
- Delete: -
- Read: Encounter_PatientVisit (Added_Time, PVS_ID, Referral_ID, Referral_ID_Stamp, Referral_Link, Row_Status); Referrals_Main (ID, Referral_Added_Time, Referral_Date, Referral_ID)
- Calls: -
- Called by: -
- Integrations: -

## diag_3008_missing_reason

- Signature: Deluge.diag_3008_missing_reason() returns string
- .ds line: 18111
- Fetch: Encounter_PatientVisit (Type_of_Entry)
- Insert: -
- Update: -
- Delete: -
- Read: Encounter_PatientVisit (Cares_3008_Completion_Date, PVS_ID, Patient_Full_Name_1, Patient_Full_Name_2, Reason_for_Referral, Referral_ID, Visit_Status)
- Calls: -
- Called by: -
- Integrations: -

## diag_3008_no_pvs_list

- Signature: Deluge.diag_3008_no_pvs_list() returns string
- .ds line: 18149
- Fetch: Encounter_PatientVisit (Type_of_Entry); Referrals_Main (Referral_Date, Referral_Type)
- Insert: -
- Update: -
- Delete: -
- Read: Encounter_PatientVisit (Referral_ID); Referrals_Main (Added_Time, Assignment_Status, Cognito_Referral_ID, Referral_Date, Referral_ID)
- Calls: -
- Called by: -
- Integrations: -

## diag_3008_no_pvs_sheet

- Signature: Deluge.diag_3008_no_pvs_sheet(date p_from, date p_to) returns string
- .ds line: 18188
- Fetch: Encounter_PatientVisit (Referral_ID, Referral_Link); Referrals_Main (Referral_Type)
- Insert: -
- Update: -
- Delete: -
- Read: Referrals_Main (ID, Partner_Branch, Partner_Location_Label, Patient_DOB, Patient_Full_Name, Referral_Added_Time, Referral_Date, Referral_ID)
- Calls: -
- Called by: -
- Integrations: -

## diag_3008_overdue

- Signature: Deluge.diag_3008_overdue() returns string
- .ds line: 18247
- Fetch: Encounter_PatientVisit (Type_of_Entry); Referrals_Main (Referral_Date, Referral_Type)
- Insert: -
- Update: -
- Delete: -
- Read: Encounter_PatientVisit (Cares_3008_Completion_Date, Referral_ID, Referral_Link, Row_Status, Visit_Status, Was_3008_Completed); Referrals_Main (ID, Referral_ID)
- Calls: -
- Called by: -
- Integrations: -

## diag_accentcare_rates

- Signature: Deluge.diag_accentcare_rates() returns string
- .ds line: 18348
- Fetch: Partner_Locations (Partner_Location_Label); Partner_Rates (Partner_Location_Link)
- Insert: -
- Update: -
- Delete: -
- Read: Partner_Locations (ID, Partner_Location_Label); Partner_Rates (Current_Rate, Partner_Rate_Status, Rate_Amount, Rate_Type)
- Calls: -
- Called by: -
- Integrations: -

## diag_addendum_restamp

- Signature: Deluge.diag_addendum_restamp() returns string
- .ds line: 18367
- Fetch: Encounter_PatientVisit (Clinical_Note_Type)
- Insert: -
- Update: -
- Delete: -
- Read: Encounter_PatientVisit (Added_Time, Modified_Time, Note_Finalized_Time, PVS_ID)
- Calls: -
- Called by: -
- Integrations: -

## diag_august_pvs_gap

- Signature: Deluge.diag_august_pvs_gap() returns string
- .ds line: 18401
- Fetch: Encounter_PatientVisit (ID); Referrals_Main (ID)
- Insert: -
- Update: -
- Delete: -
- Read: Encounter_PatientVisit (PVS_ID, Referral_ID, Referral_Link, Type_of_Entry, Visit_Completion_Date, Visit_Status); Referrals_Main (ID, Referral_Date)
- Calls: -
- Called by: -
- Integrations: -

## diag_august_pvs_state

- Signature: Deluge.diag_august_pvs_state() returns string
- .ds line: 18470
- Fetch: Encounter_PatientVisit (Visit_Completion_Date); Partner_Locations (ID)
- Insert: -
- Update: -
- Delete: -
- Read: Encounter_PatientVisit (Billing_Branch, Complexity_Charge, Complexity_Level, Invoice_Status, Reason_for_Referral, Referral_Link, Type_of_Entry); Partner_Locations (Partner_Location_Label)
- Calls: -
- Called by: -
- Integrations: -

## diag_bad_remarks_faxes

- Signature: Deluge.diag_bad_remarks_faxes() returns string
- .ds line: 18561
- Fetch: Fax_Log (ID)
- Insert: -
- Update: -
- Delete: -
- Read: Fax_Log (Cover_Remarks, Destination_Fax, Destination_Name, Fax_ID, Fax_Status, Submitted_Time)
- Calls: -
- Called by: -
- Integrations: -

## diag_billing_preview

- Signature: Deluge.diag_billing_preview(date p_from, date p_to) returns string
- .ds line: 18576
- Fetch: Encounter_PatientVisit (Invoice_Status, Visit_Completion_Date); Partner_Locations (ID); Partner_Rates (Current_Rate)
- Insert: -
- Update: -
- Delete: -
- Read: Encounter_PatientVisit (After_Hours_Fee, Billing_Branch, Complexity_Charge, Complexity_Level, Equipment_Charge_Amount, Hold_From_Invoicing, Invoice_Link, Other_Charges_Amount, PVS_ID, Super_Stat_Fee, Visit_Completion_Date); Partner_Locations (ID, Partner_Location_Label); Partner_Rates (Partner_Location_Link, Partner_Rate_Status, Rate_Type)
- Calls: -
- Called by: -
- Integrations: -

## diag_blank_referral_id

- Signature: Deluge.diag_blank_referral_id() returns string
- .ds line: 18713
- Fetch: Referrals_Main (ID)
- Insert: -
- Update: -
- Delete: -
- Read: Referrals_Main (Cognito_Referral_ID, Form_Token, ID, Partner_Organization, Partner_POC_Email, Patient_DOB, Patient_DOB1, Patient_First_Name, Patient_Full_Name, Patient_Last_Name, Referral_Added_Time, Referral_Date, Referral_ID, Referral_Type)
- Calls: -
- Called by: -
- Integrations: -

## diag_branch_books_ids

- Signature: Deluge.diag_branch_books_ids() returns string
- .ds line: 18764
- Fetch: Partner_Locations (ID)
- Insert: -
- Update: -
- Delete: -
- Read: Partner_Locations (Books_Customer_ID, ID, Partner_Location_Label, Partner_Location_Status)
- Calls: -
- Called by: -
- Integrations: -

## diag_compliance_gap

- Signature: Deluge.diag_compliance_gap() returns string
- .ds line: 18781
- Fetch: Encounter_PatientVisit (ID); Referrals_Main (ID)
- Insert: -
- Update: -
- Delete: -
- Read: Encounter_PatientVisit (Referral_ID, Referral_ID_Stamp, Referral_Link, Row_Status, Visit_Status); Referrals_Main (Added_Time, Assignment_Status, ID, Referral_Added_Time, Referral_Date, Referral_ID, Referral_Type)
- Calls: -
- Called by: -
- Integrations: -

## diag_config_write

- Signature: Deluge.diag_config_write() returns string
- .ds line: 18938
- Fetch: API_Config (Config_Name)
- Insert: -
- Update: API_Config (RC_Access_Token, RC_Token_Expiry)
- Delete: -
- Read: API_Config (RC_Access_Token)
- Calls: -
- Called by: -
- Integrations: -

## diag_dob_coverage

- Signature: Deluge.diag_dob_coverage() returns string
- .ds line: 18951
- Fetch: Referrals_Main (ID)
- Insert: -
- Update: -
- Delete: -
- Read: Referrals_Main (Patient_DOB, Patient_DOB1, Referral_ID)
- Calls: -
- Called by: -
- Integrations: -

## diag_duplicate_location_names

- Signature: Deluge.diag_duplicate_location_names() returns string
- .ds line: 19040
- Fetch: Partner_Locations (ID, Partner_Location_Status)
- Insert: -
- Update: -
- Delete: -
- Read: Partner_Locations (ID, Partner_Link, Partner_Location_Name); Partners (Partner_Display_Name)
- Calls: -
- Called by: -
- Integrations: -

## diag_duplicate_patient_referrals

- Signature: Deluge.diag_duplicate_patient_referrals(date p_from, date p_to) returns string
- .ds line: 19076
- Fetch: Encounter_PatientVisit (Referral_Link); Invoices (ID); Referrals_Main (ID, Referral_Date)
- Insert: -
- Update: -
- Delete: -
- Read: Encounter_PatientVisit (Invoice_Link, PVS_ID, Visit_Completion_Date); Invoices (Books_Invoice_Number, Invoice_Record_Status); Referrals_Main (Cognito_Referral_ID, ID, Partner_Organization, Patient_DOB, Patient_First_Name, Patient_Last_Name, Referral_Date, Referral_ID, Referral_Type)
- Calls: -
- Called by: -
- Integrations: -

## diag_duplicate_referral_ids

- Signature: Deluge.diag_duplicate_referral_ids() returns string
- .ds line: 19185
- Fetch: Referrals_Main (ID)
- Insert: -
- Update: -
- Delete: -
- Read: Referrals_Main (ID, Patient_First_Name, Patient_Last_Name, Referral_Date, Referral_ID)
- Calls: -
- Called by: -
- Integrations: -

## diag_duplicate_visits

- Signature: Deluge.diag_duplicate_visits() returns string
- .ds line: 19230
- Fetch: Encounter_PatientVisit (ID); Invoices (ID)
- Insert: -
- Update: -
- Delete: -
- Read: Encounter_PatientVisit (Complexity_Charge, Invoice_Link, PVS_ID, Patient_DOB, Patient_Full_Name_1, Visit_Completion_Date); Invoices (Books_Invoice_Number, Invoice_Record_Status)
- Calls: -
- Called by: -
- Integrations: -

## diag_empath_labels

- Signature: Deluge.diag_empath_labels() returns string
- .ds line: 19302
- Fetch: Partner_Locations (ID)
- Insert: -
- Update: -
- Delete: -
- Read: Partner_Locations (Partner_Location_Code, Partner_Location_Label, Partner_Location_Name, Partner_Location_Status)
- Calls: -
- Called by: -
- Integrations: -

## diag_employees

- Signature: Deluge.diag_employees() returns string
- .ds line: 19319
- Fetch: Employees (ID)
- Insert: -
- Update: -
- Delete: -
- Read: Employees (Employee_First_Name, Employee_Initials, Employee_Last_Name, Employee_Status)
- Calls: -
- Called by: -
- Integrations: -

## diag_esi_references

- Signature: Deluge.diag_esi_references() returns string
- .ds line: 19329
- Fetch: Encounter_PatientVisit (Billing_Branch); Invoices (Partner_Location_Link); Partner_Billing_Contacts (Partner_Location_Link); Partner_Locations (ID); Partner_Rates (Partner_Location_Link); Referrals_Main (Partner_Branch_Link)
- Insert: -
- Update: -
- Delete: -
- Read: Partner_Locations (ID, Partner_Location_Label)
- Calls: -
- Called by: -
- Integrations: -

## diag_fax_attachments

- Signature: Deluge.diag_fax_attachments() returns string
- .ds line: 19378
- Fetch: Fax_Attachments (ID); Fax_Log (Fax_Status)
- Insert: -
- Update: -
- Delete: -
- Read: Fax_Attachments (Attachment_Type, Fax_Log, Source_PVS_Link); Fax_Log (ID)
- Calls: -
- Called by: -
- Integrations: -

## diag_fax_coverage

- Signature: Deluge.diag_fax_coverage() returns string
- .ds line: 19410
- Fetch: Encounter_PatientVisit (Visit_Completion_Date); Fax_Log (ID)
- Insert: -
- Update: -
- Delete: -
- Read: Encounter_PatientVisit (Fax_Status, ID, Row_Status); Fax_Log (Added_Time, Completed_Time, Fax_Status, PVS_Link, Submitted_Time)
- Calls: -
- Called by: -
- Integrations: -

## diag_fax_error

- Signature: Deluge.diag_fax_error(string p_faxId) returns string
- .ds line: 19491
- Fetch: Fax_Log (Fax_ID)
- Insert: -
- Update: -
- Delete: -
- Read: Fax_Log (Destination_Fax, Destination_Name, Fax_Error_Code, Fax_Error_Reason, Fax_ID, Fax_Status, Number_Source, RC_Message_ID)
- Calls: -
- Called by: -
- Integrations: -

## diag_fax_pdf_image

- Signature: Deluge.diag_fax_pdf_image(int pPvsID) returns string
- .ds line: 19513
- Fetch: Encounter_PatientVisit (ID)
- Insert: -
- Update: -
- Delete: -
- Read: Encounter_PatientVisit (Clinical_Note_File_Upload, PVS_3008_Upload, PVS_File_Upload, PVS_ID)
- Calls: -
- Called by: -
- Integrations: Email

## diag_fax_readiness

- Signature: Deluge.diag_fax_readiness(int p_days) returns map
- .ds line: 19590
- Fetch: Encounter_PatientVisit (Added_Time, ID, Type_of_Entry); Partner_Billing_Contacts (Partner_Billing_POC_Status, Partner_Location_Link); Referrals_Main (Added_Time, Partner_Branch_Link)
- Insert: -
- Update: -
- Delete: -
- Read: Encounter_PatientVisit (Billing_Branch, Clinical_Note_Type, Fax_Status, Final_Clinical_Note, ID, PVS_ID, Visit_Status); Partner_Billing_Contacts (Partner_PVS_Fax); Referrals_Main (Partner_Branch_Link, Referral_ID)
- Calls: is_pvs_email_branch
- Called by: -
- Integrations: AppFunc

## diag_fax_repair_errors

- Signature: Deluge.diag_fax_repair_errors() returns string
- .ds line: 19774
- Fetch: Fax_Log (Completed_Time, Fax_Status)
- Insert: -
- Update: -
- Delete: -
- Read: Fax_Log (Fax_ID, Fax_Status, RC_Message_ID)
- Calls: get_rc_token
- Called by: -
- Integrations: AppFunc, HTTP

## diag_fax_target

- Signature: Deluge.diag_fax_target(string p_pvsId) returns string
- .ds line: 19810
- Fetch: Encounter_PatientVisit (PVS_ID); Partner_Billing_Contacts (Partner_Billing_POC_Status, Partner_Location_Link); Partner_Locations (ID)
- Insert: -
- Update: -
- Delete: -
- Read: Partner_Billing_Contacts (ID, Partner_Billing_POC_First_Name, Partner_Billing_POC_Last_Name, Partner_PVS_Fax); Partner_Locations (Partner_Location_Label)
- Calls: resolve_pvs_fax_target
- Called by: -
- Integrations: AppFunc

## diag_find_patients

- Signature: Deluge.diag_find_patients(string p_rows) returns string
- .ds line: 19858
- Fetch: Encounter_PatientVisit (Patient_DOB)
- Insert: -
- Update: -
- Delete: -
- Read: Encounter_PatientVisit (Employee_Initials, Hold_From_Invoicing, PVS_ID, Patient_Full_Name_1, Patient_Last_Name, Referral_ID, Row_Status, Type_of_Entry, Visit_Completion_Date)
- Calls: -
- Called by: -
- Integrations: -

## diag_find_referral

- Signature: Deluge.diag_find_referral(string p_text) returns string
- .ds line: 19907
- Fetch: Referrals_Main (ID, Referral_ID)
- Insert: -
- Update: -
- Delete: -
- Read: Referrals_Main (ID, Patient_First_Name, Patient_Last_Name, Referral_Date, Referral_ID)
- Calls: -
- Called by: -
- Integrations: -

## diag_form_fields

- Signature: Deluge.diag_form_fields(string p_formLink) returns string
- .ds line: 19938
- Fetch: -
- Insert: -
- Update: -
- Delete: -
- Read: -
- Calls: -
- Called by: -
- Integrations: HTTP

## diag_held_pvs

- Signature: Deluge.diag_held_pvs(date p_from, date p_to) returns string
- .ds line: 20073
- Fetch: Encounter_PatientVisit (Hold_From_Invoicing, Visit_Completion_Date)
- Insert: -
- Update: -
- Delete: -
- Read: Encounter_PatientVisit (Added_Time, Duplicate_Of_PVS_ID, Employee_Initials, Invoice_Link, PVS_ID, Partner_Organization, Referral_ID, Row_Status, Row_Status_Note, Type_of_Entry, Visit_Completion_Date)
- Calls: -
- Called by: -
- Integrations: -

## diag_imaging_notify_check

- Signature: Deluge.diag_imaging_notify_check(int p_days) returns string
- .ds line: 20118
- Fetch: Employees (ID); Referrals_Main (Added_Time)
- Insert: -
- Update: -
- Delete: -
- Read: Employees (Email_Notification_Types, Employee_Email, Employee_First_Name, Employee_Last_Name, Employee_Status); Referrals_Main (Added_Time, Form_Token, Notified_Time, Referral_Date, Referral_ID, Referral_Type)
- Calls: get_notification_recipients
- Called by: -
- Integrations: AppFunc

## diag_import_ref_matches

- Signature: Deluge.diag_import_ref_matches() returns string
- .ds line: 20149
- Fetch: Encounter_PatientVisit (PVS_ID); Referrals_Main (Cognito_Referral_ID, ID, Referral_ID)
- Insert: -
- Update: -
- Delete: -
- Read: Encounter_PatientVisit (ID, Referral_ID); Referrals_Main (Added_Time, Added_User, Cognito_Referral_ID, ID, Patient_First_Name, Patient_Last_Name, Referral_Date, Referral_ID)
- Calls: -
- Called by: -
- Integrations: -

## diag_innovage_rates

- Signature: Deluge.diag_innovage_rates() returns string
- .ds line: 20180
- Fetch: Partner_Locations (ID); Partner_Rates (Partner_Location_Link); Partners (ID)
- Insert: -
- Update: -
- Delete: -
- Read: Partner_Locations (Books_Customer_ID, ID, Partner_Link, Partner_Location_Code, Partner_Location_Label, Partner_Location_Name, Partner_Location_Status); Partner_Rates (Current_Rate, Partner_Rate_Status, Rate_Amount, Rate_Category, Rate_Type); Partners (Partner_Display_Name)
- Calls: -
- Called by: -
- Integrations: -

## diag_invoice_batch

- Signature: Deluge.diag_invoice_batch(int p_batchId) returns string
- .ds line: 20213
- Fetch: Encounter_PatientVisit (ID); Invoice_Batch (ID)
- Insert: -
- Update: -
- Delete: -
- Read: Encounter_PatientVisit (Billing_Branch, Hold_From_Invoicing, Invoice_Link, Invoice_Status, Visit_Completion_Date); Invoice_Batch (Date_From, Date_To, ID, Partner_Location_Link)
- Calls: -
- Called by: -
- Integrations: -

## diag_invoice_patient_gaps

- Signature: Deluge.diag_invoice_patient_gaps(string p_invoiceNumbers) returns string
- .ds line: 20278
- Fetch: Encounter_PatientVisit (Invoice_Link); Invoices (Books_Invoice_Number); Referrals_Main (ID)
- Insert: -
- Update: -
- Delete: -
- Read: Encounter_PatientVisit (Added_Time, Added_User, ID, PVS_ID, PVS_Referral_ID, Patient_First_Name, Patient_Full_Name_1, Patient_Full_Name_2, Patient_Hospice_ID, Patient_Last_Name, Referral_ID, Referral_Link, Type_of_Entry); Invoices (ID, Invoice_Record_Status, Visit_Count); Referrals_Main (ID, Patient_Full_Name, Patient_Hospice_ID, Referral_ID)
- Calls: -
- Called by: -
- Integrations: -

## diag_invoice_pvs

- Signature: Deluge.diag_invoice_pvs(string p_booksInvoiceId) returns string
- .ds line: 20390
- Fetch: Encounter_PatientVisit (Invoice_Link); Invoices (Books_Invoice_ID); Referrals_Main (ID)
- Insert: -
- Update: -
- Delete: -
- Read: Encounter_PatientVisit (Complexity_Charge, Complexity_Level, Invoice_Status, PVS_ID, Referral_ID, Referral_Link, Type_of_Entry, Visit_Completion_Date); Invoices (Books_Invoice_Number, ID, Invoice_Total, Visit_Count); Referrals_Main (ID, Referral_Type)
- Calls: -
- Called by: -
- Integrations: -

## diag_invoice_record

- Signature: Deluge.diag_invoice_record(int p_invoiceId) returns string
- .ds line: 20435
- Fetch: Encounter_PatientVisit (Invoice_Link); Invoices (ID)
- Insert: -
- Update: -
- Delete: -
- Read: Encounter_PatientVisit (Complexity_Charge, Complexity_Level, Invoice_Status, PVS_ID); Invoices (Books_Customer_ID, Books_Invoice_ID, Books_Invoice_Number, Books_Sync_Message, Books_Sync_Timestamp, ID, Invoice_Date, Invoice_Record_Status, Invoice_Total, Visit_Count)
- Calls: -
- Called by: -
- Integrations: -

## diag_invoice_same_patient_dos

- Signature: Deluge.diag_invoice_same_patient_dos(string p_invoiceNumbers) returns string
- .ds line: 20468
- Fetch: Encounter_PatientVisit (Invoice_Link); Invoices (Books_Invoice_Number)
- Insert: -
- Update: -
- Delete: -
- Read: Encounter_PatientVisit (Added_Time, Complexity_Level, Hold_From_Invoicing, ID, PVS_ID, Patient_DOB, Referral_ID, Visit_Completion_Date); Invoices (ID)
- Calls: -
- Called by: -
- Integrations: -

## diag_map_cognito_refs

- Signature: Deluge.diag_map_cognito_refs(string p_rows) returns string
- .ds line: 20543
- Fetch: Referrals_Main (Patient_DOB)
- Insert: -
- Update: -
- Delete: -
- Read: Referrals_Main (Cognito_Referral_ID, Partner_Location_Label, Patient_Last_Name, Referral_Date, Referral_ID, Referral_Type)
- Calls: -
- Called by: -
- Integrations: -

## diag_match_3008_refs

- Signature: Deluge.diag_match_3008_refs(string p_rows) returns string
- .ds line: 20581
- Fetch: Encounter_PatientVisit (Referral_Link, Type_of_Entry); Referrals_Main (Patient_DOB)
- Insert: -
- Update: -
- Delete: -
- Read: Referrals_Main (ID, Patient_First_Name, Patient_Last_Name, Referral_Date, Referral_ID, Referral_Type)
- Calls: -
- Called by: -
- Integrations: -

## diag_match_pvs_by_patient

- Signature: Deluge.diag_match_pvs_by_patient(string p_rows) returns string
- .ds line: 20660
- Fetch: Encounter_PatientVisit (Patient_DOB)
- Insert: -
- Update: -
- Delete: -
- Read: Encounter_PatientVisit (Clinical_Note_Type, PVS_ID, Partner_Location_Label, Patient_Last_Name, Referral_ID, Referral_Link, Type_of_Entry, Visit_Completion_Date)
- Calls: -
- Called by: -
- Integrations: -

## diag_missing_dob

- Signature: Deluge.diag_missing_dob() returns string
- .ds line: 20710
- Fetch: Encounter_PatientVisit (Invoice_Link); Referrals_Main (Patient_DOB)
- Insert: -
- Update: -
- Delete: -
- Read: Encounter_PatientVisit (Referral_Link); Referrals_Main (Added_Time, ID, Partner_Branch, Partner_Organization, Partner_POC_Email, Patient_DOB1, Patient_First_Name, Patient_Last_Name, Referral_ID, Referral_Type)
- Calls: -
- Called by: -
- Integrations: -

## diag_missing_pvs_fax

- Signature: Deluge.diag_missing_pvs_fax() returns map
- .ds line: 20753
- Fetch: Partner_Billing_Contacts (Partner_Location_Link); Partner_Locations (ID)
- Insert: -
- Update: -
- Delete: -
- Read: Partner_Billing_Contacts (Partner_Billing_POC_Status, Partner_PVS_Fax); Partner_Locations (ID, Partner_Location_Label, Partner_Location_Name, Partner_Location_Status)
- Calls: is_pvs_email_branch
- Called by: -
- Integrations: AppFunc

## diag_month_billing_gap

- Signature: Deluge.diag_month_billing_gap(int p_year, int p_month) returns string
- .ds line: 20825
- Fetch: Encounter_PatientVisit (ID); Invoices (ID, Invoice_Date); Referrals_Main (ID)
- Insert: -
- Update: -
- Delete: -
- Read: Encounter_PatientVisit (After_Hours_Fee, Complexity_Charge, Complexity_Level, Equipment_Charge_Amount, Hold_From_Invoicing, Invoice_Link, Other_Charges_Amount, PVS_ID, Referral_ID, Referral_Link, Row_Status, Super_Stat_Fee, Type_of_Entry, Visit_Completion_Date, Visit_Status); Invoices (Books_Invoice_Number, ID, Invoice_Date, Invoice_Record_Status, Invoice_Total, Service_Date_From, Service_Date_To, Visit_Count); Referrals_Main (Assignment_Status, ID, Partner_Branch, Partner_Organization, Patient_DOB, Patient_First_Name, Patient_Last_Name, Referral_Added_Time, Referral_Date, Referral_ID, Referral_Type)
- Calls: -
- Called by: -
- Integrations: -

## diag_mpu_3008_export

- Signature: Deluge.diag_mpu_3008_export(int p_year, int p_month) returns string
- .ds line: 21082
- Fetch: Encounter_PatientVisit (Referral_Link); Referrals_Main (Referral_Date, Referral_Type)
- Insert: -
- Update: -
- Delete: -
- Read: Encounter_PatientVisit (Employee_Name_Title, PVS_ID, Row_Status, Visit_Completion_Date, Visit_Status); Referrals_Main (Cognito_Referral_ID, ID, Partner_Location_Label, Patient_DOB, Patient_First_Name, Patient_Last_Name, Referral_Date, Referral_ID)
- Calls: -
- Called by: -
- Integrations: -

## diag_mpu_pvs_export

- Signature: Deluge.diag_mpu_pvs_export(int p_year, int p_month) returns string
- .ds line: 21110
- Fetch: Encounter_PatientVisit (Type_of_Entry, Visit_Completion_Date)
- Insert: -
- Update: -
- Delete: -
- Read: Encounter_PatientVisit (Additional_Charges, Equipment_Charge_Amount, PVS_ID, Patient_Last_Name, Referral_ID, Row_Status, Visit_Completion_Date, Visit_Status)
- Calls: -
- Called by: -
- Integrations: -

## diag_mpu_readiness

- Signature: Deluge.diag_mpu_readiness(int p_year, int p_month, string p_part) returns string
- .ds line: 21132
- Fetch: Encounter_PatientVisit (Referral_Link, Visit_Completion_Date); Referrals_Main (Referral_Date)
- Insert: -
- Update: -
- Delete: -
- Read: Encounter_PatientVisit (Additional_Charges, Billing_Branch, Clinical_Note_Type, Complexity_Level, Diversion_Tracking, Employee_Link, Equipment_Charge_Amount, PVS_ID, Partner_Branch, Partner_Organization, Patient_DOB, Patient_First_Name, Patient_Hospice_ID, Patient_Last_Name, Reason_for_Referral, Referral_Date, Referral_ID, Referral_Source, Row_Status, Type_of_Entry, Type_of_Procedures, Visit_Status); Referrals_Main (ID, Partner_Branch_Link, Referral_ID, Referral_Source, Referral_Type)
- Calls: -
- Called by: -
- Integrations: -

## diag_mpu_referral_export

- Signature: Deluge.diag_mpu_referral_export(int p_year, int p_month, string p_partner) returns string
- .ds line: 21343
- Fetch: Referrals_Main (Referral_Date)
- Insert: -
- Update: -
- Delete: -
- Read: Referrals_Main (Cognito_Referral_ID, Partner_Location_Label, Partner_Organization, Partner_POC_First_Name, Partner_POC_Last_Name, Partner_POC_Title, Referral_Added_Time, Referral_Date, Referral_ID, Referral_Type)
- Calls: -
- Called by: -
- Integrations: -

## diag_orphan_referral

- Signature: Deluge.diag_orphan_referral(string p_recId) returns string
- .ds line: 21455
- Fetch: Assignments (Referral_Link); Encounter_PatientVisit (Referral_Link); Imaging_Orders (Referral_Link); Referral_Files (Referrals_Main); Referrals_Main (ID, Patient_DOB)
- Insert: -
- Update: -
- Delete: -
- Read: Referrals_Main (Added_Time, ID, Partner_Location_Label, Patient_DOB, Patient_Last_Name, Referral_ID, Referral_Type)
- Calls: -
- Called by: -
- Integrations: -

## diag_orphaned_records

- Signature: Deluge.diag_orphaned_records() returns string
- .ds line: 21370
- Fetch: Assignments (ID); Encounter_PatientVisit (ID); Referral_Files (ID); Referrals_Main (ID)
- Insert: -
- Update: -
- Delete: -
- Read: Assignments (Assignment_ID, ID, Patient_First_Name, Patient_Last_Name, Referral_Link); Encounter_PatientVisit (ID, PVS_ID, Patient_Full_Name_1, Referral_Link); Referral_Files (File_Category, File_Name, ID, Referrals_Main); Referrals_Main (ID)
- Calls: -
- Called by: -
- Integrations: -

## diag_partner_location_labels

- Signature: Deluge.diag_partner_location_labels() returns string
- .ds line: 21520
- Fetch: Partner_Locations (Partner_Location_Status)
- Insert: -
- Update: -
- Delete: -
- Read: Partner_Locations (Partner_Link, Partner_Location_Label, Partner_Location_Name); Partners (Partner_Display_Name)
- Calls: -
- Called by: -
- Integrations: -

## diag_partner_rates

- Signature: Deluge.diag_partner_rates() returns string
- .ds line: 21563
- Fetch: Partner_Locations (Partner_Location_Status); Partner_Rates (Current_Rate, Partner_Location_Link)
- Insert: -
- Update: -
- Delete: -
- Read: Partner_Locations (Books_Customer_ID, ID, Partner_Location_Label); Partner_Rates (Rate_Amount, Rate_Type)
- Calls: -
- Called by: -
- Integrations: -

## diag_patient_visits

- Signature: Deluge.diag_patient_visits(string pName) returns string
- .ds line: 21630
- Fetch: Encounter_PatientVisit (ID); Invoices (ID); Partner_Locations (ID)
- Insert: -
- Update: -
- Delete: -
- Read: Encounter_PatientVisit (Billing_Branch, Complexity_Charge, Complexity_Level, Hold_From_Invoicing, Invoice_Link, Invoice_Status, PVS_ID, Patient_Full_Name_1, Visit_Completion_Date); Invoices (Books_Invoice_Number, Invoice_Record_Status); Partner_Locations (Partner_Location_Label, Partner_Location_Name)
- Calls: -
- Called by: -
- Integrations: -

## diag_premium_visit_invoices

- Signature: Deluge.diag_premium_visit_invoices() returns string
- .ds line: 21676
- Fetch: Encounter_PatientVisit (PVS_ID); Invoices (ID)
- Insert: -
- Update: -
- Delete: -
- Read: Encounter_PatientVisit (Invoice_Link, Invoice_Status); Invoices (Books_Invoice_Number, Invoice_Record_Status)
- Calls: -
- Called by: -
- Integrations: -

## diag_provider_backfill_trace

- Signature: Deluge.diag_provider_backfill_trace(string p_pvs_id) returns string
- .ds line: 21708
- Fetch: Employees (ID); Encounter_PatientVisit (PVS_ID)
- Insert: -
- Update: -
- Delete: -
- Read: Employees (Employee_Email, Employee_Initials, Employee_Name_Title); Encounter_PatientVisit (Employee_Email, Employee_First_Name, Employee_Full_Name, Employee_Initials, Employee_Last_Name, Employee_Name_Title, Employee_Title, ID, Invoice_Status, Visit_Completion_Date)
- Calls: -
- Called by: -
- Integrations: -

## diag_pv_missing_proc_div

- Signature: Deluge.diag_pv_missing_proc_div(date p_from, date p_to) returns string
- .ds line: 23259
- Fetch: Encounter_PatientVisit (Type_of_Entry, Visit_Completion_Date)
- Insert: -
- Update: -
- Delete: -
- Read: Encounter_PatientVisit (Diversion_Tracking, Employee_Full_Name, ID, PVS_ID, Referral_ID, Row_Status, Type_of_Procedures, Visit_Completion_Date)
- Calls: -
- Called by: -
- Integrations: -

## diag_pvs_added_time_clusters

- Signature: Deluge.diag_pvs_added_time_clusters() returns string
- .ds line: 21771
- Fetch: Encounter_PatientVisit (Clinical_Note_Type, Note_Finalized_Time)
- Insert: -
- Update: -
- Delete: -
- Read: Encounter_PatientVisit (Added_Time)
- Calls: -
- Called by: -
- Integrations: -

## diag_pvs_billing_batch

- Signature: Deluge.diag_pvs_billing_batch(string p_pvsIds) returns string
- .ds line: 21808
- Fetch: Encounter_PatientVisit (PVS_ID); Invoices (ID); Partner_Locations (ID)
- Insert: -
- Update: -
- Delete: -
- Read: Encounter_PatientVisit (Billing_Branch, Clinical_Note_Type, Complexity_Charge, Complexity_Level, Invoice_Link, Invoice_Status, Referral_ID, Type_of_Entry, Visit_Completion_Date); Invoices (Books_Invoice_Number, Invoice_Record_Status); Partner_Locations (Partner_Location_Label)
- Calls: -
- Called by: -
- Integrations: -

## diag_pvs_billing_flags

- Signature: Deluge.diag_pvs_billing_flags() returns string
- .ds line: 21860
- Fetch: Encounter_PatientVisit (ID)
- Insert: -
- Update: -
- Delete: -
- Read: Encounter_PatientVisit (Hold_From_Invoicing, ID, Invoice_Link, Invoice_Status, PVS_ID)
- Calls: -
- Called by: -
- Integrations: -

## diag_pvs_billing_snapshot

- Signature: Deluge.diag_pvs_billing_snapshot(string p_pvsKey) returns string
- .ds line: 21910
- Fetch: Encounter_PatientVisit (ID); Partner_Locations (ID); Partner_Rates (Current_Rate, Partner_Location_Link, Rate_Type)
- Insert: -
- Update: -
- Delete: -
- Read: Encounter_PatientVisit (Billing_Branch, Complexity_Charge, Complexity_Level, ID, Invoice_Link, Invoice_Status, PVS_ID, Patient_Full_Name_2, Type_of_Entry); Partner_Locations (Partner_Location_Label); Partner_Rates (Rate_Amount)
- Calls: -
- Called by: -
- Integrations: -

## diag_pvs_billing_vs_referral

- Signature: Deluge.diag_pvs_billing_vs_referral(int p_from, int p_to) returns string
- .ds line: 22007
- Fetch: Encounter_PatientVisit (Billing_Branch, Referral_Link); Partner_Locations (ID); Referrals_Main (ID)
- Insert: -
- Update: -
- Delete: -
- Read: Encounter_PatientVisit (Billing_Branch, Invoice_Status, PVS_ID); Partner_Locations (Partner_Location_Label); Referrals_Main (ID, Partner_Branch_Link, Partner_Location_Label, Referral_ID)
- Calls: -
- Called by: -
- Integrations: -

## diag_pvs_blank_reason

- Signature: Deluge.diag_pvs_blank_reason() returns string
- .ds line: 22044
- Fetch: Encounter_PatientVisit (ID); Referrals_Main (ID)
- Insert: -
- Update: -
- Delete: -
- Read: Encounter_PatientVisit (PVS_ID, Patient_Full_Name_1, Patient_Full_Name_2, Reason_for_Referral, Referral_ID, Referral_Link, Type_of_Entry, Visit_Completion_Date); Referrals_Main (ID, Referral_Reason, Referral_Type)
- Calls: -
- Called by: -
- Integrations: -

## diag_pvs_by_recid

- Signature: Deluge.diag_pvs_by_recid(string p_ids) returns string
- .ds line: 22094
- Fetch: Encounter_PatientVisit (ID)
- Insert: -
- Update: -
- Delete: -
- Read: Encounter_PatientVisit (Has_Referral_ID, ID, PVS_ID, PVS_Referral_ID, Patient_First_Name, Patient_Last_Name, Referral_ID, Referral_ID_Stamp, Referral_Link, Visit_Completion_Date)
- Calls: -
- Called by: -
- Integrations: -

## diag_pvs_creation_source

- Signature: Deluge.diag_pvs_creation_source(int p_year, int p_month) returns string
- .ds line: 22139
- Fetch: Encounter_PatientVisit (Visit_Completion_Date)
- Insert: -
- Update: -
- Delete: -
- Read: Encounter_PatientVisit (Added_Time, Added_User, PVS_ID)
- Calls: -
- Called by: -
- Integrations: -

## diag_pvs_email_branches

- Signature: Deluge.diag_pvs_email_branches() returns string
- .ds line: 22171
- Fetch: Partner_Billing_Contacts (Partner_Billing_POC_Status, Partner_PVS_Delivery); Partner_Locations (ID)
- Insert: -
- Update: -
- Delete: -
- Read: Partner_Billing_Contacts (ID, Partner_Billing_POC_Email, Partner_Location_Link); Partner_Locations (ID, Partner_Location_Label)
- Calls: is_pvs_email_branch
- Called by: -
- Integrations: AppFunc

## diag_pvs_fax_number

- Signature: Deluge.diag_pvs_fax_number(int pPvsID) returns string
- .ds line: 22199
- Fetch: Encounter_PatientVisit (ID); Partner_Billing_Contacts (Partner_Location_Link)
- Insert: -
- Update: -
- Delete: -
- Read: Encounter_PatientVisit (Billing_Branch, PVS_ID, Partner_Location_Label); Partner_Billing_Contacts (ID, Partner_PVS_Fax)
- Calls: -
- Called by: -
- Integrations: -

## diag_pvs_field_values

- Signature: Deluge.diag_pvs_field_values(string p_pvsId) returns string
- .ds line: 22245
- Fetch: Encounter_PatientVisit (PVS_ID)
- Insert: -
- Update: -
- Delete: -
- Read: -
- Calls: -
- Called by: -
- Integrations: -

## diag_pvs_for_refs

- Signature: Deluge.diag_pvs_for_refs(string p_refIds) returns string
- .ds line: 22284
- Fetch: Encounter_PatientVisit (ID, PVS_Referral_ID, Referral_ID, Referral_ID_Stamp, Referral_Link); Referrals_Main (Referral_ID)
- Insert: -
- Update: -
- Delete: -
- Read: Encounter_PatientVisit (Added_Time, Cares_3008_Completion_Date, ID, PVS_ID, Row_Status, Type_of_Entry, Visit_Completion_Date, Visit_Status); Referrals_Main (ID)
- Calls: -
- Called by: -
- Integrations: -

## diag_pvs_hospice_ids

- Signature: Deluge.diag_pvs_hospice_ids(string p_pvsIds) returns string
- .ds line: 22343
- Fetch: Encounter_PatientVisit (PVS_ID); Referrals_Main (ID)
- Insert: -
- Update: -
- Delete: -
- Read: Encounter_PatientVisit (Patient_Hospice_ID, Referral_Link); Referrals_Main (Patient_Hospice_ID)
- Calls: -
- Called by: -
- Integrations: -

## diag_pvs_ids

- Signature: Deluge.diag_pvs_ids() returns string
- .ds line: 22377
- Fetch: Encounter_PatientVisit (ID)
- Insert: -
- Update: -
- Delete: -
- Read: Encounter_PatientVisit (Has_Referral_ID, ID, PVS_ID, PVS_Referral_ID, Referral_ID)
- Calls: -
- Called by: -
- Integrations: -

## diag_pvs_login_email_gaps

- Signature: Deluge.diag_pvs_login_email_gaps() returns string
- .ds line: 22406
- Fetch: Employees (ID); Encounter_PatientVisit (ID)
- Insert: -
- Update: -
- Delete: -
- Read: Employees (Employee_Email, Employee_Portal_Email, Employee_Status); Encounter_PatientVisit (Employee_Email)
- Calls: -
- Called by: -
- Integrations: -

## diag_pvs_names

- Signature: Deluge.diag_pvs_names(string p_pvsIds) returns string
- .ds line: 22452
- Fetch: Encounter_PatientVisit (PVS_ID); Referrals_Main (ID)
- Insert: -
- Update: -
- Delete: -
- Read: Encounter_PatientVisit (Patient_DOB, Patient_First_Name, Patient_Full_Name_1, Patient_Last_Name, Referral_Link, Type_of_Entry, Visit_Completion_Date); Referrals_Main (Patient_DOB, Patient_First_Name, Patient_Last_Name, Referral_ID)
- Calls: -
- Called by: -
- Integrations: -

## diag_pvs_note_compare

- Signature: Deluge.diag_pvs_note_compare(string p_pvsIds) returns string
- .ds line: 22507
- Fetch: Encounter_PatientVisit (PVS_ID)
- Insert: -
- Update: -
- Delete: -
- Read: Encounter_PatientVisit (Clinical_Note_File_Upload, Clinical_Note_Type, Complexity_Level, Fax_Status, Final_Clinical_Note, Note_Finalized_Time, PVS_File_Upload, Provider_ICD_Print, Type_of_Procedures)
- Calls: -
- Called by: -
- Integrations: -

## diag_pvs_note_placement

- Signature: Deluge.diag_pvs_note_placement(date p_from, date p_to) returns string
- .ds line: 22596
- Fetch: Encounter_PatientVisit (Visit_Completion_Date)
- Insert: -
- Update: -
- Delete: -
- Read: Encounter_PatientVisit (Final_Clinical_Note, Notes_3008, PVS_ID, Type_of_Entry)
- Calls: -
- Called by: -
- Integrations: -

## diag_pvs_note_text

- Signature: Deluge.diag_pvs_note_text(string p_pvsIds, int p_chars) returns string
- .ds line: 22670
- Fetch: Encounter_PatientVisit (PVS_ID)
- Insert: -
- Update: -
- Delete: -
- Read: Encounter_PatientVisit (Complexity_Level, Diversion_Tracking, Final_Clinical_Note, Referral_ID, Type_of_Procedures)
- Calls: -
- Called by: -
- Integrations: -

## diag_pvs_one

- Signature: Deluge.diag_pvs_one(string p_pvsId) returns string
- .ds line: 22722
- Fetch: Encounter_PatientVisit (PVS_ID)
- Insert: -
- Update: -
- Delete: -
- Read: Encounter_PatientVisit (Added_Time, Added_User, Employee_Email, Employee_Link, Referral_Date, Referral_Link, Referral_Source, Row_Status, Visit_Completion_Date)
- Calls: -
- Called by: -
- Integrations: -

## diag_pvs_premium_mismatches

- Signature: Deluge.diag_pvs_premium_mismatches() returns string
- .ds line: 22742
- Fetch: Encounter_PatientVisit (Additional_Charges); Partner_Locations (ID); Partner_Rates (Current_Rate, Partner_Location_Link, Rate_Type)
- Insert: -
- Update: -
- Delete: -
- Read: Encounter_PatientVisit (Additional_Charges, After_Hours_Fee, Billing_Branch, Invoice_Link, PVS_ID, Super_Stat_Fee); Partner_Locations (Partner_Location_Label); Partner_Rates (Rate_Amount)
- Calls: -
- Called by: -
- Integrations: -

## diag_pvs_provider_fields

- Signature: Deluge.diag_pvs_provider_fields(string p_pvs_id) returns string
- .ds line: 22842
- Fetch: Employees (ID); Encounter_PatientVisit (PVS_ID); Partner_Locations (ID)
- Insert: -
- Update: -
- Delete: -
- Read: Employees (Employee_Name_Title); Encounter_PatientVisit (Billing_Branch, Complexity_Charge, Complexity_Level, Employee_Email, Employee_First_Name, Employee_Full_Name, Employee_Initials, Employee_Last_Name, Employee_Link, Employee_Name_Title, Employee_Title, ID, Invoice_Status, PVS_ID, Provider_Login_Email, Referral_ID, Type_of_Entry); Partner_Locations (Partner_Location_Label)
- Calls: -
- Called by: -
- Integrations: -

## diag_pvs_reason_by_entry

- Signature: Deluge.diag_pvs_reason_by_entry() returns string
- .ds line: 22898
- Fetch: Encounter_PatientVisit (ID)
- Insert: -
- Update: -
- Delete: -
- Read: Encounter_PatientVisit (Reason_for_Referral, Type_of_Entry)
- Calls: -
- Called by: -
- Integrations: -

## diag_pvs_referral_match

- Signature: Deluge.diag_pvs_referral_match(string p_pvsIds) returns string
- .ds line: 22961
- Fetch: Encounter_PatientVisit (PVS_ID); Referrals_Main (ID, Patient_DOB, Referral_ID)
- Insert: -
- Update: -
- Delete: -
- Read: Encounter_PatientVisit (ID, Patient_DOB, Referral_ID, Referral_Link, Visit_Completion_Date); Referrals_Main (ID, Partner_Location_Label, Patient_DOB, Referral_Date, Referral_ID, Referral_Type)
- Calls: -
- Called by: -
- Integrations: -

## diag_pvs_stamp_gap

- Signature: Deluge.diag_pvs_stamp_gap() returns string
- .ds line: 23070
- Fetch: Encounter_PatientVisit (ID)
- Insert: -
- Update: -
- Delete: -
- Read: Encounter_PatientVisit (Added_Time, Added_User, Clinical_Note_Type, Employee_Email, Modified_Time, PVS_ID, Provider_Login_Email, Type_of_Entry)
- Calls: -
- Called by: -
- Integrations: -

## diag_pvs_status_mix

- Signature: Deluge.diag_pvs_status_mix() returns string
- .ds line: 23093
- Fetch: Encounter_PatientVisit (ID)
- Insert: -
- Update: -
- Delete: -
- Read: Encounter_PatientVisit (Added_Time, Clinical_Note_Type, Row_Status, Type_of_Entry, Visit_Status)
- Calls: -
- Called by: -
- Integrations: -

## diag_pvs_vs_referral

- Signature: Deluge.diag_pvs_vs_referral(string p_pvsIds) returns string
- .ds line: 23148
- Fetch: Encounter_PatientVisit (PVS_ID); Invoices (ID); Partner_Locations (ID); Referrals_Main (ID)
- Insert: -
- Update: -
- Delete: -
- Read: Encounter_PatientVisit (Billing_Branch, Employee_Name_Title, Facility_Name, Invoice_Link, Partner_Branch, Partner_ID, Partner_Location_Label, Partner_Organization, Patient_DOB, Patient_First_Name, Patient_Full_Name_1, Patient_Last_Name, Patient_Location, Referral_ID, Referral_Link, Type_of_Entry, Visit_Completion_Date); Invoices (Books_Invoice_Number, Invoice_Record_Status); Partner_Locations (ID, Partner_Location_Label); Referrals_Main (Facility_Name, Partner_Branch, Partner_Branch_Link, Partner_ID, Partner_Location_Label, Partner_Organization, Patient_DOB, Patient_First_Name, Patient_Full_Name, Patient_Last_Name, Patient_Location, Referral_ID)
- Calls: -
- Called by: -
- Integrations: -

## diag_rc_fax_history

- Signature: Deluge.diag_rc_fax_history() returns string
- .ds line: 23289
- Fetch: Fax_Log (ID)
- Insert: -
- Update: -
- Delete: -
- Read: Fax_Log (RC_Message_ID)
- Calls: get_rc_token
- Called by: -
- Integrations: AppFunc, HTTP

## diag_rc_token

- Signature: Deluge.diag_rc_token() returns string
- .ds line: 23388
- Fetch: API_Config (Config_Name)
- Insert: -
- Update: -
- Delete: -
- Read: API_Config (RC_Access_Token, RC_Client_ID, RC_Client_Secret, RC_JWT_Assertion, RC_Token_Expiry)
- Calls: get_rc_token
- Called by: -
- Integrations: AppFunc, HTTP

## diag_ref_branch_candidates

- Signature: Deluge.diag_ref_branch_candidates(string p_refId) returns string
- .ds line: 24245
- Fetch: Partner_Locations (Partner_Location_Label, Partner_Location_Name); Partner_Referral_Contacts (ID); Referrals_Main (Referral_ID)
- Insert: -
- Update: -
- Delete: -
- Read: Partner_Locations (ID, Partner_Location_ID, Partner_Location_Label, Partner_Location_Status); Partner_Referral_Contacts (ID, Partner_Locations_Link, Partner_POC_Email); Referrals_Main (ID, Partner_Branch, Partner_Branch_Submitted, Partner_Organization, Partner_POC_Email)
- Calls: -
- Called by: -
- Integrations: -

## diag_ref_names

- Signature: Deluge.diag_ref_names(string p_refIds) returns string
- .ds line: 24308
- Fetch: Referrals_Main (Referral_ID)
- Insert: -
- Update: -
- Delete: -
- Read: Referrals_Main (Patient_DOB, Patient_First_Name, Patient_Last_Name)
- Calls: -
- Called by: -
- Integrations: -

## diag_ref_patient_pvs_match

- Signature: Deluge.diag_ref_patient_pvs_match(string p_refIds) returns string
- .ds line: 24338
- Fetch: Encounter_PatientVisit (Patient_DOB, Referral_ID, Referral_Link); Referrals_Main (ID, Patient_DOB, Referral_ID)
- Insert: -
- Update: -
- Delete: -
- Read: Encounter_PatientVisit (Invoice_Status, PVS_ID, Patient_Last_Name, Referral_ID, Row_Status, Type_of_Entry, Visit_Completion_Date, Visit_Status); Referrals_Main (Assignment_Status, Employee_Link, ID, Partner_Branch, Partner_Organization, Patient_DOB, Patient_Last_Name, Referral_Date, Referral_ID, Referral_Type)
- Calls: -
- Called by: -
- Integrations: -

## diag_referral_branch

- Signature: Deluge.diag_referral_branch(string p_referral_id) returns string
- .ds line: 23537
- Fetch: Partner_Locations (ID); Partner_Referral_Contacts (Partner_POC_Email); Referrals_Main (Referral_ID)
- Insert: -
- Update: -
- Delete: -
- Read: Partner_Locations (ID, Partner_Location_Label); Partner_Referral_Contacts (ID, Partner_Locations_Link); Referrals_Main (ID, Partner_Branch, Partner_Branch_Link, Partner_Branch_Submitted, Partner_ID, Partner_Link, Partner_Location_Label, Partner_Organization, Partner_POC_Email, Patient_Full_Name, Referral_ID, Referral_Type)
- Calls: -
- Called by: -
- Integrations: -

## diag_referral_by_name

- Signature: Deluge.diag_referral_by_name(string p_text) returns string
- .ds line: 23607
- Fetch: Referrals_Main (ID)
- Insert: -
- Update: -
- Delete: -
- Read: Referrals_Main (ID, Partner_Branch, Partner_Organization, Patient_First_Name, Patient_Full_Name, Patient_Last_Name, Referral_Date, Referral_ID, Referral_ID_Stamp, Referral_Type)
- Calls: -
- Called by: -
- Integrations: -

## diag_referral_collision

- Signature: Deluge.diag_referral_collision(date p_date) returns string
- .ds line: 23685
- Fetch: Referrals_Main (Added_Time, Referral_Date, Referral_ID)
- Insert: -
- Update: -
- Delete: -
- Read: Referrals_Main (Added_Time, Form_Token, ID, Partner_Location_Label, Referral_ID, Referral_ID_Stamp, Referral_Type)
- Calls: -
- Called by: -
- Integrations: -

## diag_referral_contact_match

- Signature: Deluge.diag_referral_contact_match() returns string
- .ds line: 23745
- Fetch: Partner_Referral_Contacts (ID, Partner_POC_Email); Referrals_Main (Partner_Branch_Link)
- Insert: -
- Update: -
- Delete: -
- Read: Partner_Referral_Contacts (ID, Partner_Locations_Link); Referrals_Main (Partner_POC_Email)
- Calls: -
- Called by: -
- Integrations: -

## diag_referral_date_source

- Signature: Deluge.diag_referral_date_source(string p_refIds) returns string
- .ds line: 23855
- Fetch: Referrals_Main (Referral_ID)
- Insert: -
- Update: -
- Delete: -
- Read: Referrals_Main (Added_Time, Added_User, Cognito_Referral_ID, Notified_Time, Referral_Added_Time, Referral_Date, Referral_Date1)
- Calls: -
- Called by: -
- Integrations: -

## diag_referral_dates

- Signature: Deluge.diag_referral_dates() returns string
- .ds line: 23794
- Fetch: Referrals_Main (ID)
- Insert: -
- Update: -
- Delete: -
- Read: Referrals_Main (Added_Time, Referral_Date, Referral_ID)
- Calls: -
- Called by: -
- Integrations: -

## diag_referral_dump

- Signature: Deluge.diag_referral_dump(string p_refIds) returns string
- .ds line: 23879
- Fetch: Referrals_Main (Referral_ID)
- Insert: -
- Update: -
- Delete: -
- Read: Partner_Locations (Partner_Location_Label); Partners (Partner_Display_Name); Referrals_Main (AC_Full_Name, AC_Phone, AC_Relationship_to_Patient, Added_Time, Additional_Information, Cognito_Referral_ID, Data_Issues, Facility_Name, Facility_Phone, Form_Token, ID, Notified_Time, Partner_Branch, Partner_Branch_Link, Partner_Branch_Submitted, Partner_ICD_Codes, Partner_ID, Partner_Link, Partner_Location_Label, Partner_Organization, Partner_POC_Email, Partner_POC_Name_Title, Partner_POC_Phone, Partner_POC_Team, Patient_DOB, Patient_DOB1, Patient_Full_Address, Patient_Full_Name, Patient_Gender, Patient_Hospice_ID, Patient_Location, Patient_MBI, Patient_Phone, Referral_Added_Time, Referral_Date, Referral_Reason, Referral_Source, Referral_Type)
- Calls: -
- Called by: -
- Integrations: -

## diag_referral_id_records

- Signature: Deluge.diag_referral_id_records(string p_refIds) returns string
- .ds line: 24008
- Fetch: Encounter_PatientVisit (Referral_Link); Referrals_Main (Referral_ID)
- Insert: -
- Update: -
- Delete: -
- Read: Encounter_PatientVisit (ID, Invoice_Status, PVS_ID, Patient_DOB, Visit_Completion_Date); Referrals_Main (ID, Partner_Location_Label, Patient_DOB, Patient_DOB1, Patient_First_Name, Patient_Last_Name, Referral_Date, Referral_Type)
- Calls: -
- Called by: -
- Integrations: -

## diag_referral_ids

- Signature: Deluge.diag_referral_ids() returns string
- .ds line: 23958
- Fetch: Referrals_Main (ID)
- Insert: -
- Update: -
- Delete: -
- Read: Referrals_Main (Form_Token, ID, Patient_Last_Name, Referral_ID, Referral_ID_Stamp)
- Calls: -
- Called by: -
- Integrations: -

## diag_referral_imaging

- Signature: Deluge.diag_referral_imaging(string p_refIds) returns string
- .ds line: 24071
- Fetch: Referral_Files (Referrals_Main); Referrals_Main (Referral_ID)
- Insert: -
- Update: -
- Delete: -
- Read: Referral_Files (File_Category, File_Name); Referrals_Main (Form_Token, ID, Imaging_Body_Site, Imaging_Order_Indication, Imaging_Orders_URLs, Imaging_Type_Order, Notified_Time, Referral_Date, Referral_Type)
- Calls: -
- Called by: -
- Integrations: -

## diag_referral_intake

- Signature: Deluge.diag_referral_intake(string p_refKey) returns string
- .ds line: 24114
- Fetch: Referrals_Main (ID, Referral_ID)
- Insert: -
- Update: -
- Delete: -
- Read: Referrals_Main (File_Upload_3008, Files_3008_URLs, General_Files_URLs, General_Files_Upload, Imaging_Orders_URLs, Imaging_Orders_Upload, Partner_Branch, Partner_Branch_Link, Partner_ID, Partner_Link, Partner_Location_Label, Partner_Organization, Referral_ID)
- Calls: -
- Called by: -
- Integrations: -

## diag_referral_origin

- Signature: Deluge.diag_referral_origin() returns string
- .ds line: 24146
- Fetch: Referrals_Main (ID)
- Insert: -
- Update: -
- Delete: -
- Read: Referrals_Main (Cognito_Referral_ID, Form_Token, ID, Referral_Date, Referral_ID)
- Calls: -
- Called by: -
- Integrations: -

## diag_referral_partner_resolve

- Signature: Deluge.diag_referral_partner_resolve(string pRefId) returns map
- .ds line: 24199
- Fetch: Referrals_Main (Referral_ID)
- Insert: -
- Update: -
- Delete: -
- Read: Referrals_Main (Partner_Branch, Partner_Branch_Link, Partner_Branch_Submitted, Partner_Location_Label, Partner_Organization, Partner_POC_Email)
- Calls: partner_branch_values, resolve_branch_id
- Called by: -
- Integrations: AppFunc

## diag_referrals_missing_pvs

- Signature: Deluge.diag_referrals_missing_pvs(date p_from, date p_to) returns string
- .ds line: 23416
- Fetch: Encounter_PatientVisit (Referral_ID, Referral_Link, Type_of_Entry); Referrals_Main (Referral_Date)
- Insert: -
- Update: -
- Delete: -
- Read: Encounter_PatientVisit (Row_Status); Referrals_Main (Assignment_Status, ID, Partner_Location_Label, Referral_Date, Referral_ID, Referral_Type)
- Calls: -
- Called by: -
- Integrations: -

## diag_room_number_gaps

- Signature: Deluge.diag_room_number_gaps() returns string
- .ds line: 24416
- Fetch: Encounter_PatientVisit (PVS_ID); Referrals_Main (ID)
- Insert: -
- Update: -
- Delete: -
- Read: Encounter_PatientVisit (Facility_Name, Facility_Phone, Facility_Room_Number, Patient_Full_Name_1, Referral_Link); Referrals_Main (Facility_Name, Facility_Phone, Facility_Room_Number, Referral_ID)
- Calls: -
- Called by: -
- Integrations: -

## diag_safe_test_referrals

- Signature: Deluge.diag_safe_test_referrals() returns string
- .ds line: 24460
- Fetch: Assignments (Referral_Link); Referral_Files (Referrals_Main); Referrals_Main (Referral_Date)
- Insert: -
- Update: -
- Delete: -
- Read: Referrals_Main (ID, Partner_Branch, Partner_Branch_Link, Partner_Organization, Patient_First_Name, Patient_Last_Name, Referral_Date, Referral_ID, Referral_Type)
- Calls: -
- Called by: -
- Integrations: -

## diag_sept_pvs_completeness

- Signature: Deluge.diag_sept_pvs_completeness(date p_start, date p_end) returns map
- .ds line: 24490
- Fetch: Encounter_PatientVisit (Type_of_Entry, Visit_Completion_Date, Visit_Status)
- Insert: -
- Update: -
- Delete: -
- Read: Encounter_PatientVisit (Billing_Branch, Facility_Name, Facility_Room_Number, PVS_ID, Partner_Organization, Patient_Location)
- Calls: -
- Called by: -
- Integrations: -

## diag_sequence_trackers

- Signature: Deluge.diag_sequence_trackers() returns string
- .ds line: 24541
- Fetch: Assignments (ID); Employees (ID); Partners (ID); Referrals_Main (ID); Sequence_Tracker (ID)
- Insert: -
- Update: -
- Delete: -
- Read: Assignments (Assignment_ID); Employees (Employee_ID); Partners (Partner_ID); Referrals_Main (Referral_ID); Sequence_Tracker (Object_Prefix, Object_Sequence)
- Calls: -
- Called by: -
- Integrations: -

## diag_stuck_faxes

- Signature: Deluge.diag_stuck_faxes() returns string
- .ds line: 24645
- Fetch: Fax_Log (Fax_Status)
- Insert: -
- Update: -
- Delete: -
- Read: Fax_Log (Fax_ID, RC_Message_ID)
- Calls: get_rc_token
- Called by: -
- Integrations: AppFunc, HTTP

## diag_unfaxed_by_branch

- Signature: Deluge.diag_unfaxed_by_branch() returns map
- .ds line: 24701
- Fetch: Encounter_PatientVisit (Clinical_Note_Type, Fax_Status, Type_of_Entry, Visit_Status); Partner_Billing_Contacts (Partner_Billing_POC_Status, Partner_Location_Link); Partner_Locations (ID, Partner_Location_Label)
- Insert: -
- Update: -
- Delete: -
- Read: Encounter_PatientVisit (Billing_Branch); Partner_Billing_Contacts (Partner_PVS_Fax); Partner_Locations (ID, Partner_Location_Label, Partner_Location_Name)
- Calls: -
- Called by: -
- Integrations: -

## diag_unmatched_branch_labels

- Signature: Deluge.diag_unmatched_branch_labels() returns string
- .ds line: 24764
- Fetch: Partner_Locations (Partner_Location_Status); Referrals_Main (ID)
- Insert: -
- Update: -
- Delete: -
- Read: Partner_Locations (Partner_Location_Label, Partner_Location_Name); Referrals_Main (ID, Partner_Branch_Submitted, Partner_Location_Label, Referral_ID)
- Calls: -
- Called by: -
- Integrations: -

## diag_unnotified_referrals

- Signature: Deluge.diag_unnotified_referrals() returns string
- .ds line: 24838
- Fetch: Assignments (Referral_Link); Referrals_Main (Referral_Date)
- Insert: -
- Update: -
- Delete: -
- Read: Referrals_Main (ID, Partner_Branch, Partner_Organization, Partner_POC_Email, Patient_First_Name, Patient_Last_Name, Referral_ID, Referral_Reason, Referral_Type)
- Calls: -
- Called by: -
- Integrations: -

## diag_upload_field_usage

- Signature: Deluge.diag_upload_field_usage() returns string
- .ds line: 24865
- Fetch: Encounter_PatientVisit (ID); Referrals_Main (ID)
- Insert: -
- Update: -
- Delete: -
- Read: Encounter_PatientVisit (General_Files_Upload); Referrals_Main (File_Upload_3008, General_Files_Upload, ID, Imaging_Orders_Upload, Referral_ID)
- Calls: -
- Called by: -
- Integrations: -

## diag_upload_field_values

- Signature: Deluge.diag_upload_field_values(string p_refKey) returns string
- .ds line: 24914
- Fetch: Referrals_Main (ID, Referral_ID)
- Insert: -
- Update: -
- Delete: -
- Read: Referrals_Main (File_Upload_3008, General_Files_Upload, ID, Imaging_Orders_Upload, Referral_ID)
- Calls: -
- Called by: -
- Integrations: -

## diag_upload_probe

- Signature: Deluge.diag_upload_probe(string p_refKey) returns string
- .ds line: 24960
- Fetch: Referrals_Main (ID, Referral_ID)
- Insert: -
- Update: -
- Delete: -
- Read: Referrals_Main (Files_3008_URLs, ID, Referral_ID)
- Calls: -
- Called by: -
- Integrations: HTTP

## diag_workdrive_download

- Signature: Deluge.diag_workdrive_download(string p_resId) returns string
- .ds line: 25026
- Fetch: -
- Insert: -
- Update: -
- Delete: -
- Read: -
- Calls: -
- Called by: -
- Integrations: HTTP

## diag_zztest_referrals

- Signature: Deluge.diag_zztest_referrals() returns string
- .ds line: 25055
- Fetch: Referrals_Main (ID)
- Insert: -
- Update: -
- Delete: -
- Read: Referrals_Main (ID, Partner_Branch_Link, Patient_Last_Name, Referral_ID)
- Calls: -
- Called by: -
- Integrations: -

## fill_3008_reason

- Signature: Deluge.fill_3008_reason(string p_mode, date p_from, date p_to) returns string
- .ds line: 25084
- Fetch: Encounter_PatientVisit (Type_of_Entry, Visit_Completion_Date)
- Insert: -
- Update: Encounter_PatientVisit (Reason_for_Referral)
- Delete: -
- Read: Encounter_PatientVisit (ID, PVS_ID, Reason_for_Referral)
- Calls: -
- Called by: -
- Integrations: -

## fix_accentcare_current_rate

- Signature: Deluge.fix_accentcare_current_rate() returns string
- .ds line: 25108
- Fetch: Partner_Locations (ID); Partner_Rates (Current_Rate); Partners (ID)
- Insert: -
- Update: Partner_Rates (Current_Rate, Partner_Rate_Status)
- Delete: -
- Read: Partner_Locations (ID, Partner_Link, Partner_Location_Code); Partner_Rates (Partner_Location_Link, Partner_Rates_Effective_Date); Partners (ID, Partner_Code)
- Calls: -
- Called by: -
- Integrations: -

## fix_six_room_numbers

- Signature: Deluge.fix_six_room_numbers() returns string
- .ds line: 25127
- Fetch: Encounter_PatientVisit (PVS_ID)
- Insert: -
- Update: Encounter_PatientVisit (Facility_Room_Number)
- Delete: -
- Read: Encounter_PatientVisit (Facility_Room_Number)
- Calls: -
- Called by: -
- Integrations: -

## flag_duplicate_referrals

- Signature: Deluge.flag_duplicate_referrals(string p_mode, string p_pairs) returns string
- .ds line: 25162
- Fetch: Referrals_Main (ID, Referral_ID)
- Insert: -
- Update: Referrals_Main (Data_Issues)
- Delete: -
- Read: Referrals_Main (Data_Issues, ID)
- Calls: -
- Called by: -
- Integrations: -

## fmt_phone_display

- Signature: Deluge.fmt_phone_display(string pRaw) returns string
- .ds line: 25246
- Fetch: -
- Insert: -
- Update: -
- Delete: -
- Read: -
- Calls: -
- Called by: function build_pvs_fax_html, workflow PVS_Fax_Review/PVS_Fax_Review_Format_Ove, workflow PVS_Fax_Review/PVS_Fax_Review_Format_Ove1
- Integrations: -

## fmt_referral_source

- Signature: Deluge.fmt_referral_source(string pOrg, string pBranch) returns string
- .ds line: 25262
- Fetch: -
- Insert: -
- Update: -
- Delete: -
- Read: -
- Calls: -
- Called by: workflow Encounter_PatientVisit/Fax_This_Note_Preview_And
- Integrations: -

## get_notification_recipients

- Signature: Deluge.get_notification_recipients(string p_type) returns list
- .ds line: 25284
- Fetch: Employees (Employee_Status)
- Insert: -
- Update: -
- Delete: -
- Read: Employees (Email_Notification_Types, Employee_Email)
- Calls: -
- Called by: function diag_imaging_notify_check, function send_3008_notification, function send_imaging_notification
- Integrations: -

## get_partner_referral_contact

- Signature: Deluge.get_partner_referral_contact(string pPocEmail) returns map
- .ds line: 25304
- Fetch: Partner_Referral_Contacts (ID, Partner_POC_Email)
- Insert: -
- Update: -
- Delete: -
- Read: Partner_Referral_Contacts (ID, Partner_Branch, Partner_Link, Partner_Locations_Link, Partner_Organization, Partner_POC_Email, Partner_POC_First_Name, Partner_POC_Last_Name, Partner_POC_Phone, Partner_POC_Team, Partner_POC_Title); Partners (Partner_Display_Name)
- Calls: -
- Called by: -
- Integrations: -

## get_pvs_fax_files

- Signature: Deluge.get_pvs_fax_files(int pPvsID, list pSelected, bool pAll) returns map
- .ds line: 25375
- Fetch: Encounter_PatientVisit (ID)
- Insert: -
- Update: -
- Delete: -
- Read: Encounter_PatientVisit (Clinical_Note_File_Upload, General_Files_Upload, Lab_Files_Upload, PVS_3008_Upload, PVS_File_Upload, Upload_Imaging_Order_Files)
- Calls: -
- Called by: workflow Encounter_PatientVisit/Fax_This_Note_On_Submit1
- Integrations: HTTP

## get_rc_token

- Signature: Deluge.get_rc_token() returns string
- .ds line: 25479
- Fetch: API_Config (Config_Name)
- Insert: -
- Update: API_Config (RC_Access_Token, RC_Token_Expiry)
- Delete: -
- Read: API_Config (RC_Access_Token, RC_Client_ID, RC_Client_Secret, RC_JWT_Assertion, RC_Token_Expiry)
- Calls: -
- Called by: function api_fax_send_console, function diag_fax_repair_errors, function diag_rc_fax_history, function diag_rc_token, function diag_stuck_faxes, function poll_fax_status, function repair_fax_log_status, function send_pvs_fax
- Integrations: HTTP

## is_portal_admin

- Signature: Deluge.is_portal_admin() returns bool
- .ds line: 25519
- Fetch: Employees (Employee_Status)
- Insert: -
- Update: -
- Delete: -
- Read: Employees (Employee_Email, Employee_Portal_Email, Portal_Access_Types)
- Calls: -
- Called by: function widget_today_visits, workflow Assignments/Assignment_Notify_Provide
- Integrations: -

## is_pvs_email_branch

- Signature: Deluge.is_pvs_email_branch(int pBranchId) returns bool
- .ds line: 25546
- Fetch: Partner_Billing_Contacts (Partner_Billing_POC_Status, Partner_Location_Link, Partner_PVS_Delivery)
- Insert: -
- Update: -
- Delete: -
- Read: -
- Calls: -
- Called by: function diag_fax_readiness, function diag_missing_pvs_fax, function diag_pvs_email_branches, function send_fax_digest
- Integrations: -

## link_pvs_to_referral

- Signature: Deluge.link_pvs_to_referral() returns string
- .ds line: 25558
- Fetch: Encounter_PatientVisit (Referral_ID, Referral_Link); Referrals_Main (Referral_ID)
- Insert: -
- Update: Encounter_PatientVisit (Referral_Link)
- Delete: -
- Read: Encounter_PatientVisit (Referral_ID); Referrals_Main (ID)
- Calls: -
- Called by: -
- Integrations: -

## log_change

- Signature: Deluge.log_change(string source_form, string source_rec_id, string source_display_id, string field_label, string old_val, string new_val, string changed_by) returns void
- .ds line: 25577
- Fetch: -
- Insert: -
- Update: -
- Delete: -
- Read: -
- Calls: -
- Called by: workflow Assignments/Assignment_Change_Log
- Integrations: -

## mint_assignment_id

- Signature: Deluge.mint_assignment_id(int recId) returns void
- .ds line: 25580
- Fetch: Assignments (ID); Sequence_Tracker (Object_Prefix)
- Insert: -
- Update: Assignments (Assignment_ID, Assignment_ID_Stamp); Sequence_Tracker (Object_Sequence)
- Delete: -
- Read: Assignments (Assignment_ID); Sequence_Tracker (Object_Sequence)
- Calls: -
- Called by: function backfill_assignment_ids, function process_new_referral, function send_assignment_notification, workflow Assignments/Assignment_ID_Generator
- Integrations: -

## mint_employee_id

- Signature: Deluge.mint_employee_id(int recId) returns void
- .ds line: 25606
- Fetch: Employees (ID); Sequence_Tracker (Object_Prefix)
- Insert: -
- Update: Employees (Employee_ID, Employee_ID_Stamp); Sequence_Tracker (Object_Sequence)
- Delete: -
- Read: Employees (Employee_ID); Sequence_Tracker (Object_Sequence)
- Calls: -
- Called by: function backfill_employee_ids, workflow Employees/Employee_ID_Generator
- Integrations: -

## mint_location_id

- Signature: Deluge.mint_location_id(int recId) returns void
- .ds line: 25632
- Fetch: Partner_Locations (ID); Partners (ID); Sequence_Tracker (Object_Prefix)
- Insert: -
- Update: Partner_Locations (Partner_Location_ID, Partner_Location_ID_Stamp); Sequence_Tracker (Object_Sequence)
- Delete: -
- Read: Partner_Locations (Partner_Link, Partner_Location_Code, Partner_Location_ID); Partners (Partner_Code); Sequence_Tracker (Object_Sequence)
- Calls: -
- Called by: function backfill_location_ids, workflow Partner_Locations/LOC_ID_Generator
- Integrations: -

## mint_partner_id

- Signature: Deluge.mint_partner_id(int recId) returns void
- .ds line: 25680
- Fetch: Partners (ID); Sequence_Tracker (Object_Prefix)
- Insert: -
- Update: Partners (Partner_ID, Partner_ID_Stamp); Sequence_Tracker (Object_Sequence)
- Delete: -
- Read: Partners (Partner_Code, Partner_ID); Sequence_Tracker (Object_Sequence)
- Calls: -
- Called by: function backfill_partner_ids, workflow Partners/PAR_ID_Generator
- Integrations: -

## mint_referral_id

- Signature: Deluge.mint_referral_id(int recId) returns void
- .ds line: 25718
- Fetch: Referrals_Main (ID, Referral_ID); Sequence_Tracker (ID, Object_Prefix)
- Insert: -
- Update: Referrals_Main (Referral_ID, Referral_ID_Stamp); Sequence_Tracker (Object_Sequence)
- Delete: -
- Read: Referrals_Main (Referral_ID); Sequence_Tracker (ID, Object_Sequence)
- Calls: -
- Called by: function backfill_mint_missing_referral_ids, function backfill_referral_ids, function process_new_referral
- Integrations: -

## normalize_pvs_phones

- Signature: Deluge.normalize_pvs_phones(string p_confirm) returns string
- .ds line: 25799
- Fetch: Encounter_PatientVisit (ID)
- Insert: -
- Update: Encounter_PatientVisit (Facility_Phone, Partner_POC_Phone, Patient_Phone)
- Delete: -
- Read: Encounter_PatientVisit (Facility_Phone, PVS_ID, Partner_POC_Phone, Patient_Phone)
- Calls: -
- Called by: -
- Integrations: -

## parse_patient_dob

- Signature: Deluge.parse_patient_dob(string p_text) returns date
- .ds line: 25889
- Fetch: -
- Insert: -
- Update: -
- Delete: -
- Read: -
- Calls: -
- Called by: function compute_data_issues, function process_new_referral, function resync_patient_dob, function run_import_backfills, function sos_referral_health, workflow Encounter_PatientVisit/PVS_Required_Fields, workflow Referrals_Main/Referral_DOB_Sync_On_Edit
- Integrations: -

## partner_branch_values

- Signature: Deluge.partner_branch_values(string pKey) returns map
- .ds line: 25963
- Fetch: Partner_Locations (ID, Partner_Location_ID); Partners (ID)
- Insert: -
- Update: -
- Delete: -
- Read: Partner_Locations (ID, Partner_Link, Partner_Location_Label, Partner_Location_Name); Partners (ID, Partner_Display_Name, Partner_ID)
- Calls: -
- Called by: function backfill_partner_resolver, function diag_referral_partner_resolve, function process_new_referral, function sync_pvs_branch_from_referral, workflow Encounter_PatientVisit/PVS_Sets_Billing_Branch_O, workflow Referrals_Main/Referral_Resolves_Partner
- Integrations: -

## poll_fax_status

- Signature: Deluge.poll_fax_status() returns string
- .ds line: 26013
- Fetch: Encounter_PatientVisit (ID); Fax_Attachments (Fax_Log); Fax_Log (Fax_Status)
- Insert: -
- Update: Encounter_PatientVisit (Fax_Status); Fax_Log (Completed_Time, Fax_Error_Code, Fax_Error_Reason, Fax_Status, Last_Polled_Time, Page_Count)
- Delete: -
- Read: Fax_Attachments (Source_PVS_Link); Fax_Log (Attempt_Number, ID, PVS_Link, RC_Message_ID, Submitted_Time)
- Calls: get_rc_token
- Called by: schedule Fax_Poll_Re_arm
- Integrations: AppFunc, HTTP

## prepare_month_for_billing

- Signature: Deluge.prepare_month_for_billing(string p_mode, string p_from, string p_to) returns string
- .ds line: 26171
- Fetch: Encounter_PatientVisit (Visit_Completion_Date); Partner_Locations (ID); Partner_Rates (Current_Rate, Partner_Location_Link, Rate_Type); Referrals_Main (ID, Referral_ID)
- Insert: -
- Update: Encounter_PatientVisit (Billing_Branch, Complexity_Charge, Partner_Branch, Partner_Location_Label, Partner_Organization, Referral_Link)
- Delete: -
- Read: Encounter_PatientVisit (Billing_Branch, Complexity_Charge, Complexity_Level, Invoice_Status, PVS_ID, Referral_ID, Referral_Link); Partner_Locations (ID, Partner_Link, Partner_Location_Label, Partner_Location_Name); Partner_Rates (Rate_Amount); Partners (Partner_Display_Name); Referrals_Main (ID, Partner_Branch_Link)
- Calls: -
- Called by: -
- Integrations: -

## process_new_referral

- Signature: Deluge.process_new_referral(string p_refKey, string p_notify) returns string
- .ds line: 26363
- Fetch: Assignments (Referral_Link); Partner_Locations (Partner_Location_ID); Partner_Referral_Contacts (ID, Partner_POC_Email); Referral_Files (Referrals_Main); Referrals_Main (ID, Referral_ID)
- Insert: Assignments (Added_User, Facility_Name, Facility_Phone, Facility_Room_Number, Patient_Address, Patient_DOB, Patient_First_Name, Patient_Last_Name, Patient_Location, Patient_Phone, Referral_Link); Partner_Referral_Contacts (Added_User, Partner_Branch, Partner_Organization, Partner_POC_Email, Partner_POC_First_Name, Partner_POC_Last_Name, Partner_POC_Name_Title, Partner_POC_Phone, Partner_POC_Team, Partner_POC_Title); Referral_Files (Added_User, File_Category, File_Name, File_Upload, Form_Token, Referrals_Main)
- Update: Partner_Referral_Contacts (Partner_Branch, Partner_Link, Partner_Locations_Link, Partner_Organization, Partner_POC_First_Name, Partner_POC_Last_Name, Partner_POC_Name_Title, Partner_POC_Phone, Partner_POC_Team, Partner_POC_Title); Referrals_Main (AC_Full_Name, AC_Phone, Facility_Phone, Notified_Time, Partner_Branch, Partner_Branch_Link, Partner_Branch_Submitted, Partner_ID, Partner_ID_Stamp, Partner_Link, Partner_Location_Label, Partner_Organization, Partner_POC_Name_Title, Partner_POC_Phone, Patient_DOB, Patient_Full_Address, Patient_Full_Name, Patient_Phone, Patient_SSN, Referral_Date)
- Delete: -
- Read: Partner_Locations (ID); Partner_Referral_Contacts (ID, Partner_POC_Email); Referrals_Main (AC_First_Name, AC_Last_Name, AC_Phone, Added_Time, Facility_Name, Facility_Phone, Facility_Room_Number, Files_3008_URLs, Form_Token, General_Files_URLs, ID, Imaging_Orders_URLs, Notified_Time, Partner_Branch_Link, Partner_Branch_Submitted, Partner_Location_Label, Partner_Organization, Partner_POC_Email, Partner_POC_First_Name, Partner_POC_Last_Name, Partner_POC_Phone, Partner_POC_Team, Partner_POC_Title, Patient_Address, Patient_DOB1, Patient_First_Name, Patient_Last_Name, Patient_Location, Patient_MI, Patient_Phone, Patient_SSN, Referral_Date, Referral_ID)
- Calls: mint_assignment_id, mint_referral_id, parse_patient_dob, partner_branch_values, resolve_branch_id, send_3008_notification, send_imaging_notification, send_referral_confirmation, send_referral_notification
- Called by: function sos_referral_health, function sweep_unnotified_referrals, workflow Referrals_Main/Referrals_Main_On_Create_
- Integrations: AppFunc, HTTP

## relink_pvs_to_referral

- Signature: Deluge.relink_pvs_to_referral(string p_mode) returns string
- .ds line: 26931
- Fetch: Encounter_PatientVisit (Referral_Link); Referrals_Main (Referral_ID)
- Insert: -
- Update: Encounter_PatientVisit (Billing_Branch, Facility_Name, Facility_Phone, Facility_Room_Number, Partner_Branch, Partner_Organization, Patient_DOB, Patient_First_Name, Patient_Full_Name_1, Patient_Full_Name_2, Patient_Gender, Patient_Hospice_ID, Patient_Last_Name, Patient_Location, Patient_MI, Patient_Phone, Reason_for_Referral, Referral_Link)
- Delete: -
- Read: Encounter_PatientVisit (Billing_Branch, Facility_Name, Facility_Phone, Facility_Room_Number, PVS_ID, Partner_Branch, Partner_Organization, Patient_DOB, Patient_First_Name, Patient_Full_Name_1, Patient_Full_Name_2, Patient_Gender, Patient_Hospice_ID, Patient_Last_Name, Patient_Location, Patient_MI, Patient_Phone, Reason_for_Referral, Referral_ID); Referrals_Main (Facility_Name, Facility_Phone, Facility_Room_Number, ID, Partner_Branch, Partner_Branch_Link, Partner_Organization, Patient_DOB, Patient_First_Name, Patient_Full_Name, Patient_Gender, Patient_Hospice_ID, Patient_Last_Name, Patient_Location, Patient_MI, Patient_Phone, Referral_Reason)
- Calls: -
- Called by: -
- Integrations: -

## repair_fax_log_status

- Signature: Deluge.repair_fax_log_status(bool p_commit) returns string
- .ds line: 27183
- Fetch: Encounter_PatientVisit (ID); Fax_Log (Completed_Time, Fax_Status)
- Insert: -
- Update: Encounter_PatientVisit (Fax_Status); Fax_Log (Completed_Time, Fax_Status)
- Delete: -
- Read: Fax_Log (Fax_ID, Fax_Status, PVS_Link, RC_Message_ID)
- Calls: get_rc_token
- Called by: -
- Integrations: AppFunc, HTTP

## repair_invoice_pvs_from_referral

- Signature: Deluge.repair_invoice_pvs_from_referral(string p_invoiceNumbers, string p_mode) returns string
- .ds line: 27294
- Fetch: Encounter_PatientVisit (Invoice_Link); Invoices (Books_Invoice_Number); Referrals_Main (ID, Referral_ID)
- Insert: -
- Update: Encounter_PatientVisit (Patient_DOB, Patient_First_Name, Patient_Full_Name_1, Patient_Full_Name_2, Patient_Gender, Patient_Hospice_ID, Patient_Last_Name, Patient_MI, Reason_for_Referral, Referral_Link)
- Delete: -
- Read: Encounter_PatientVisit (ID, PVS_ID, Patient_DOB, Patient_First_Name, Patient_Full_Name_1, Patient_Full_Name_2, Patient_Gender, Patient_Hospice_ID, Patient_Last_Name, Patient_MI, Reason_for_Referral, Referral_ID, Referral_Link); Invoices (ID); Referrals_Main (ID, Patient_DOB, Patient_First_Name, Patient_Full_Name, Patient_Gender, Patient_Hospice_ID, Patient_Last_Name, Patient_MI, Referral_ID, Referral_Reason)
- Calls: -
- Called by: -
- Integrations: -

## repair_pvs_3008_import

- Signature: Deluge.repair_pvs_3008_import(string p_mode) returns string
- .ds line: 27576
- Fetch: Encounter_PatientVisit (Type_of_Entry); Partner_Locations (ID); Partner_Rates (Current_Rate, Partner_Location_Link, Rate_Type)
- Insert: -
- Update: Encounter_PatientVisit (Complexity_Charge, Complexity_Level, Invoice_Status, Visit_Completion_Date)
- Delete: -
- Read: Encounter_PatientVisit (Billing_Branch, Cares_3008_Completion_Date, Complexity_Charge, Complexity_Level, Invoice_Link, Invoice_Status, PVS_ID, Visit_Completion_Date); Partner_Locations (Partner_Location_Label); Partner_Rates (Rate_Amount)
- Calls: -
- Called by: -
- Integrations: -

## replicate_uniform_rates

- Signature: Deluge.replicate_uniform_rates() returns string
- .ds line: 27760
- Fetch: Partner_Locations (ID, Partner_Link, Partner_Location_Status); Partner_Rates (Current_Rate, ID, Partner_Location_Link); Partners (Partner_Status, Rate_Structure)
- Insert: Partner_Rates (Added_User, Current_Rate, Partner_Link, Partner_Location_Link, Partner_Rate_Status, Partner_Rates_Effective_Date, Rate_Amount, Rate_Category, Rate_Type)
- Update: Partner_Rates (Partner_Rate_ID_Stamp)
- Delete: -
- Read: Partner_Locations (ID, Partner_Location_Label); Partner_Rates (Partner_Rates_Effective_Date, Rate_Amount, Rate_Category, Rate_Type); Partners (ID, Partner_Display_Name)
- Calls: -
- Called by: -
- Integrations: -

## report_partner_rate_coverage

- Signature: Deluge.report_partner_rate_coverage() returns string
- .ds line: 27830
- Fetch: Partner_Locations (ID); Partner_Rates (ID, Partner_Location_Link); Partners (ID)
- Insert: -
- Update: -
- Delete: -
- Read: Partner_Locations (Books_Customer_ID, ID, Partner_Link, Partner_Location_Code, Partner_Location_ID, Partner_Location_Label, Partner_Location_Name, Partner_Location_Status); Partner_Rates (Current_Rate, ID, Partner_Location_Link, Partner_Rate_Status, Partner_Rates_Effective_Date, Rate_Amount, Rate_Category, Rate_Type); Partners (ID, Partner_Code, Partner_Display_Name, Partner_Status, Rate_Structure)
- Calls: -
- Called by: -
- Integrations: -

## reprice_draft_pvs

- Signature: Deluge.reprice_draft_pvs(string p_branchLabel, string p_confirm) returns string
- .ds line: 27998
- Fetch: Encounter_PatientVisit (Invoice_Status); Partner_Locations (ID); Partner_Rates (Current_Rate, Partner_Location_Link, Rate_Type)
- Insert: -
- Update: Encounter_PatientVisit (Complexity_Charge)
- Delete: -
- Read: Encounter_PatientVisit (Billing_Branch, Complexity_Charge, Complexity_Level, Invoice_Link, PVS_ID); Partner_Locations (Partner_Location_Label); Partner_Rates (Rate_Amount)
- Calls: -
- Called by: -
- Integrations: -

## resend_referral_notifications

- Signature: Deluge.resend_referral_notifications(string p_refKeys, string p_toEmail) returns string
- .ds line: 28085
- Fetch: API_Config (Config_Name); Referrals_Main (ID, Referral_ID)
- Insert: -
- Update: -
- Delete: -
- Read: API_Config (Zepto_Send_Token); Referrals_Main (ID, Referral_Type)
- Calls: build_3008_email_html, build_creator_attachments, build_imaging_email_html, build_referral_email_html
- Called by: -
- Integrations: AppFunc, HTTP

## reset_invoice

- Signature: Deluge.reset_invoice(string p_invoiceNumber, string p_confirm) returns string
- .ds line: 28243
- Fetch: Encounter_PatientVisit (Invoice_Link); Invoices (Books_Invoice_Number, ID)
- Insert: -
- Update: Encounter_PatientVisit (Invoice_Link, Invoice_Status); Invoices (Books_Sync_Message, Books_Sync_Timestamp, Invoice_Record_Status)
- Delete: -
- Read: Encounter_PatientVisit (PVS_ID); Invoices (Books_Invoice_ID, Books_Sync_Message, ID)
- Calls: -
- Called by: -
- Integrations: HTTP

## reset_invoice_by_id

- Signature: Deluge.reset_invoice_by_id(string p_mode, int p_invoiceId, string p_confirm) returns string
- .ds line: 28325
- Fetch: Encounter_PatientVisit (Invoice_Link); Invoices (ID); Partner_Locations (ID)
- Insert: -
- Update: Encounter_PatientVisit (Invoice_Link, Invoice_Status); Invoices (Books_Sync_Message, Books_Sync_Timestamp, Invoice_Record_Status)
- Delete: -
- Read: Encounter_PatientVisit (PVS_ID); Invoices (Books_Invoice_ID, Books_Invoice_Number, Books_Sync_Message, ID, Invoice_Record_Status, Invoice_Total, Partner_Location_Link, Visit_Count); Partner_Locations (ID, Partner_Location_Label)
- Calls: -
- Called by: -
- Integrations: HTTP

## resolve_branch_id

- Signature: Deluge.resolve_branch_id(string pCurrentLink, string pContactEmail, string pLabelText, string pOrgText) returns string
- .ds line: 28460
- Fetch: Partner_Locations (ID, Partner_Location_ID, Partner_Location_Label, Partner_Location_Name, Partner_Location_Status); Partner_Referral_Contacts (ID, Partner_POC_Email)
- Insert: -
- Update: -
- Delete: -
- Read: Partner_Locations (ID, Partner_Location_ID); Partner_Referral_Contacts (Partner_Locations_Link, Partner_POC_Email)
- Calls: -
- Called by: function backfill_partner_resolver, function diag_referral_partner_resolve, function process_new_referral, workflow Encounter_PatientVisit/PVS_Sets_Billing_Branch_O, workflow Referrals_Main/Referral_Resolves_Partner
- Integrations: -

## resolve_pvs_fax_target

- Signature: Deluge.resolve_pvs_fax_target(int pPvsID) returns map
- .ds line: 28545
- Fetch: Encounter_PatientVisit (ID); Partner_Billing_Contacts (Partner_Billing_POC_Status, Partner_Location_Link); Partner_Locations (ID); Partners (ID)
- Insert: -
- Update: -
- Delete: -
- Read: Encounter_PatientVisit (Billing_Branch, Clinical_Note_Type, Final_Clinical_Note, Partner_Branch, Partner_Location_Label, Type_of_Entry, Visit_Status); Partner_Billing_Contacts (ID, Partner_Billing_POC_First_Name, Partner_Billing_POC_Last_Name, Partner_Link, Partner_PVS_Fax); Partner_Locations (Partner_Location_Label); Partners (Partner_Display_Name)
- Calls: -
- Called by: function diag_fax_target, workflow Encounter_PatientVisit/Fax_This_Note_On_Submit, workflow Encounter_PatientVisit/Fax_This_Note_On_Submit1, workflow PVS_Fax_Review/PVS_Fax_Review_Fax_Now, workflow PVS_Fax_Review/PVS_Fax_Review_On_Load
- Integrations: -

## resolve_referral_branch_from_text

- Signature: Deluge.resolve_referral_branch_from_text() returns string
- .ds line: 28669
- Fetch: Partner_Locations (Partner_Location_Label); Referrals_Main (Partner_Branch_Link)
- Insert: -
- Update: Referrals_Main (Partner_Branch_Link)
- Delete: -
- Read: Partner_Locations (ID); Referrals_Main (Partner_Branch)
- Calls: -
- Called by: -
- Integrations: -

## resync_location_labels

- Signature: Deluge.resync_location_labels() returns string
- .ds line: 28715
- Fetch: Encounter_PatientVisit (ID); Partner_Locations (ID); Referrals_Main (ID)
- Insert: -
- Update: Encounter_PatientVisit (Partner_Location_Label); Referrals_Main (Partner_Location_Label)
- Delete: -
- Read: Encounter_PatientVisit (Billing_Branch); Partner_Locations (ID, Partner_Location_Label); Referrals_Main (Partner_Branch_Link)
- Calls: -
- Called by: -
- Integrations: -

## resync_location_names

- Signature: Deluge.resync_location_names() returns string
- .ds line: 28769
- Fetch: Encounter_PatientVisit (ID); Partner_Locations (ID); Referrals_Main (ID)
- Insert: -
- Update: Encounter_PatientVisit (Partner_Branch); Referrals_Main (Partner_Branch)
- Delete: -
- Read: Encounter_PatientVisit (Billing_Branch); Partner_Locations (ID, Partner_Location_Name); Referrals_Main (Partner_Branch_Link)
- Calls: -
- Called by: -
- Integrations: -

## resync_patient_dob

- Signature: Deluge.resync_patient_dob(string p_mode) returns string
- .ds line: 28823
- Fetch: Referrals_Main (ID)
- Insert: -
- Update: Referrals_Main (Patient_DOB)
- Delete: -
- Read: Referrals_Main (Patient_DOB, Patient_DOB1, Referral_ID)
- Calls: parse_patient_dob
- Called by: -
- Integrations: AppFunc

## retire_3008_duplicates_auto

- Signature: Deluge.retire_3008_duplicates_auto(string p_mode) returns string
- .ds line: 28899
- Fetch: Encounter_PatientVisit (ID, Type_of_Entry)
- Insert: -
- Update: Encounter_PatientVisit (Duplicate_Of_PVS_ID, Hold_From_Invoicing, Row_Status)
- Delete: -
- Read: Encounter_PatientVisit (Hold_From_Invoicing, ID, Invoice_Link, Invoice_Status, PVS_ID, PVS_Referral_ID, Patient_DOB, Patient_Full_Name_1, Referral_ID)
- Calls: -
- Called by: -
- Integrations: -

## retire_pvs_duplicate

- Signature: Deluge.retire_pvs_duplicate(string p_mode, string p_dupePvsId, string p_keeperPvsId) returns string
- .ds line: 29008
- Fetch: Encounter_PatientVisit (ID, PVS_ID)
- Insert: -
- Update: Encounter_PatientVisit (Complexity_Charge, Duplicate_Of_PVS_ID, Hold_From_Invoicing, Row_Status, Row_Status_Note)
- Delete: -
- Read: Encounter_PatientVisit (Complexity_Charge, Duplicate_Of_PVS_ID, Hold_From_Invoicing, ID, Invoice_Link, Invoice_Status, Row_Status)
- Calls: -
- Called by: function retire_pvs_duplicate_pairs
- Integrations: -

## retire_pvs_duplicate_pairs

- Signature: Deluge.retire_pvs_duplicate_pairs(string p_mode, string p_pairs) returns string
- .ds line: 29193
- Fetch: -
- Insert: -
- Update: -
- Delete: -
- Read: -
- Calls: retire_pvs_duplicate
- Called by: -
- Integrations: AppFunc

## retire_pvs_duplicates

- Signature: Deluge.retire_pvs_duplicates(string p_mode, string p_dupePvsIds) returns string
- .ds line: 29089
- Fetch: Encounter_PatientVisit (ID, PVS_ID, Referral_ID, Type_of_Entry)
- Insert: -
- Update: Encounter_PatientVisit (Duplicate_Of_PVS_ID, Hold_From_Invoicing, Row_Status)
- Delete: -
- Read: Encounter_PatientVisit (Hold_From_Invoicing, ID, Invoice_Link, Invoice_Status, PVS_ID, Referral_ID)
- Calls: -
- Called by: -
- Integrations: -

## retire_pvs_record

- Signature: Deluge.retire_pvs_record(string p_mode, string p_pvsId, string p_reason) returns string
- .ds line: 29226
- Fetch: Encounter_PatientVisit (ID, PVS_ID)
- Insert: -
- Update: Encounter_PatientVisit (After_Hours_Fee, Complexity_Charge, Equipment_Charge_Amount, Hold_From_Invoicing, Other_Charges_Amount, Row_Status, Row_Status_Note, Super_Stat_Fee)
- Delete: -
- Read: Encounter_PatientVisit (After_Hours_Fee, Complexity_Charge, Equipment_Charge_Amount, Hold_From_Invoicing, ID, Invoice_Link, Invoice_Status, Other_Charges_Amount, Row_Status, Super_Stat_Fee)
- Calls: -
- Called by: -
- Integrations: -

## retry_failed_faxes

- Signature: Deluge.retry_failed_faxes() returns string
- .ds line: 29325
- Fetch: Encounter_PatientVisit (ID); Fax_Log (Fax_Status)
- Insert: -
- Update: Fax_Log (Completed_Time, Fax_Error_Reason, Fax_Status)
- Delete: -
- Read: Encounter_PatientVisit (Partner_Location_Label); Fax_Log (Attempt_Number, Cover_Remarks, Destination_Fax, Destination_Name, ID, Number_Source, Original_Fax_Link, Override_Reason, PVS_Link)
- Calls: send_pvs_fax
- Called by: schedule Fax_Retry_Sweep
- Integrations: AppFunc

## run_import_backfills

- Signature: Deluge.run_import_backfills(string p_mode, int p_limit) returns string
- .ds line: 29381
- Fetch: Employees (ID); Encounter_PatientVisit (PVS_ID); Partner_Locations (ID); Partner_Rates (Current_Rate, Partner_Location_Link, Rate_Type); Referrals_Main (Cognito_Referral_ID, ID, Referral_ID, Referral_ID_Stamp); Sequence_Tracker (Object_Prefix)
- Insert: Change_Log (Added_User, Changed_By, Field_Changed, New_Value, Source_Display_ID, Source_Form, Source_Record_ID)
- Update: Encounter_PatientVisit (Additional_Information, Advanced_Directives_Details, Billing_Branch, Complexity_Charge, Employee_Email, Employee_First_Name, Employee_Full_Name, Employee_Initials, Employee_Last_Name, Employee_Link, Employee_Name_Title, Employee_Title, Facility_Phone, Facility_Room_Number, Has_Referral_ID, List_Patient_Allergies, List_Patient_Anticoagulants, PVS_ID, PVS_Referral_ID, Partner_Branch, Partner_ICD_Codes, Partner_ID, Partner_ID_Stamp, Partner_Location_Label, Partner_Organization, Partner_POC_Email, Partner_POC_First_Name, Partner_POC_Last_Name, Partner_POC_Name_Title, Partner_POC_Phone, Partner_POC_Team, Partner_POC_Title, Patient_Full_Address, Patient_Full_Name_1, Patient_Full_Name_2, Patient_Hospice_ID, Patient_MI, Patient_Phone, Patient_SSN, Provider_Login_Email, Reason_for_Referral, Referral_Date, Referral_ID, Referral_ID_Stamp, Referral_Link, Referral_Source, Row_Status); Referrals_Main (Data_Issues, Partner_Branch, Partner_Branch_Link, Partner_ID, Partner_ID_Stamp, Partner_Link, Partner_Location_Label, Partner_Organization, Patient_DOB, Patient_Full_Address, Patient_Full_Name, Referral_ID_Stamp)
- Delete: -
- Read: Employees (Employee_Email, Employee_First_Name, Employee_Initials, Employee_Last_Name, Employee_Name_Title, Employee_Portal_Email, Employee_Title, ID); Encounter_PatientVisit (Additional_Information, Advanced_Directives_Details, Complexity_Charge, Complexity_Level, Employee_Email, Employee_Initials, Facility_Phone, Facility_Room_Number, ID, List_Patient_Allergies, List_Patient_Anticoagulants, Partner_ICD_Codes, Partner_ID, Partner_ID_Stamp, Partner_POC_Email, Partner_POC_First_Name, Partner_POC_Last_Name, Partner_POC_Name_Title, Partner_POC_Phone, Partner_POC_Team, Partner_POC_Title, Patient_Address, Patient_Full_Address, Patient_Full_Name_1, Patient_Full_Name_2, Patient_Hospice_ID, Patient_MI, Patient_Phone, Patient_SSN, Reason_for_Referral, Referral_Date, Referral_ID, Referral_ID_Stamp, Referral_Link, Referral_Source, Row_Status, Visit_Status); Partner_Locations (ID, Partner_Link, Partner_Location_Label, Partner_Location_Name); Partner_Rates (Rate_Amount); Partners (Partner_Display_Name, Partner_ID); Referrals_Main (Additional_Information, Advanced_Directives_Details, Cognito_Referral_ID, Facility_Phone, Facility_Room_Number, ID, List_Patient_Allergies, List_Patient_Anticoagulants, Partner_Branch, Partner_Branch_Link, Partner_ICD_Codes, Partner_ID, Partner_ID_Stamp, Partner_Location_Label, Partner_Organization, Partner_POC_Email, Partner_POC_First_Name, Partner_POC_Last_Name, Partner_POC_Phone, Partner_POC_Team, Partner_POC_Title, Patient_Address, Patient_DOB, Patient_DOB1, Patient_First_Name, Patient_Full_Address, Patient_Full_Name, Patient_Hospice_ID, Patient_Last_Name, Patient_MI, Patient_Phone, Patient_SSN, Referral_Date, Referral_ID, Referral_ID_Stamp, Referral_Reason, Referral_Source); Sequence_Tracker (Object_Sequence)
- Calls: compute_data_issues, parse_patient_dob
- Called by: -
- Integrations: AppFunc

## run_invoice_batch

- Signature: Deluge.run_invoice_batch(int p_batchId, decimal p_maxTotal) returns string
- .ds line: 30085
- Fetch: Encounter_PatientVisit (Billing_Branch, Invoice_Status, Visit_Completion_Date); Invoice_Batch (ID); Partner_Rates (Current_Rate, Partner_Location_Link)
- Insert: -
- Update: Invoice_Batch (Batch_Status, Result_Message)
- Delete: -
- Read: Encounter_PatientVisit (After_Hours_Fee, Complexity_Charge, Complexity_Level, Equipment_Charge_Amount, Hold_From_Invoicing, ID, Invoice_Link, Other_Charges_Amount, PVS_ID, PVS_Referral_ID, Patient_DOB, Patient_Full_Name_1, Referral_ID, Super_Stat_Fee, Visit_Completion_Date); Invoice_Batch (Batch_Reason, Date_From, Date_To, ID, Partner_Location_Link, Replaces_Invoice_Number, Result_Message); Partner_Rates (Partner_Rate_Status, Rate_Type)
- Calls: create_invoice_from_selection
- Called by: workflow Invoice_Batch/Invoice_Batch_On_Create
- Integrations: AppFunc

## run_pvs_exclusion_monitor

- Signature: Deluge.run_pvs_exclusion_monitor() returns string
- .ds line: 30387
- Fetch: Encounter_PatientVisit (QC_Reviewed, Type_of_Entry); Referrals_Main (Referral_ID)
- Insert: -
- Update: -
- Delete: -
- Read: Encounter_PatientVisit (Added_Time, Employee_Name_Title, Final_Clinical_Note, ID, PVS_ID, Partner_Organization, Patient_Full_Name_1, Referral_ID, Referral_Link, Visit_Completion_Date); Referrals_Main (Referral_ID)
- Calls: send_via_sendgrid
- Called by: -
- Integrations: AppFunc

## run_schema_monitor

- Signature: Deluge.run_schema_monitor() returns string
- .ds line: 30517
- Fetch: Schema_Snapshot (ID)
- Insert: Schema_Snapshot (Added_User, Captured_On, Change_Summary, Snapshot_Data)
- Update: -
- Delete: -
- Read: Schema_Snapshot (Captured_On, Change_Summary, Snapshot_Data)
- Calls: send_via_sendgrid
- Called by: schedule SOS_Schema_Monitor_Daily_
- Integrations: AppFunc, HTTP

## seed_schema_to_github

- Signature: Deluge.seed_schema_to_github() returns void
- .ds line: 31027
- Fetch: -
- Insert: -
- Update: -
- Delete: -
- Read: -
- Calls: -
- Called by: -
- Integrations: Email, HTTP

## send_3008_notification

- Signature: Deluge.send_3008_notification(string p_refKey) returns string
- .ds line: 31223
- Fetch: API_Config (Config_Name); Referrals_Main (ID, Referral_ID)
- Insert: -
- Update: -
- Delete: -
- Read: API_Config (Zepto_Send_Token); Referrals_Main (ID, Referral_Type)
- Calls: build_3008_email_html, build_zepto_attachments, get_notification_recipients
- Called by: function process_new_referral
- Integrations: AppFunc, HTTP

## send_activity_digest

- Signature: Deluge.send_activity_digest(string p_type, string p_from, string p_to) returns string
- .ds line: 31306
- Fetch: API_Config (Config_Name); Encounter_PatientVisit (Added_Time, Cares_3008_Completion_Date, Clinical_Note_Type, Note_Finalized_Time, Visit_Completion_Date); Fax_Attachments (Added_Time, Attachment_Type); Fax_Log (Fax_Status, Submitted_Time); Referrals_Main (Referral_Date)
- Insert: -
- Update: -
- Delete: -
- Read: API_Config (Zepto_Send_Token); Encounter_PatientVisit (Added_Time, Cares_3008_Completion_Date, Clinical_Note_Type, Employee_Name_Title, ID, Note_Finalized_Time, PVS_ID, Partner_Organization, Patient_Full_Name_1, Referral_ID, Referral_Source, Row_Status, Type_of_Entry, Type_of_Procedures, Visit_Completion_Date, Visit_Status, Was_3008_Completed); Fax_Attachments (Fax_Log, Source_PVS_Link); Fax_Log (Completed_Time, ID, PVS_Link, Submitted_Time); Referrals_Main (Partner_Organization, Patient_Full_Name, Referral_Date, Referral_ID, Referral_Reason, Referral_Source, Referral_Type)
- Calls: -
- Called by: schedule Activity_Digest_Daily_6am, schedule Activity_Digest_Weekly_Fr
- Integrations: HTTP

## send_assignment_notification

- Signature: Deluge.send_assignment_notification(string p_asgKey) returns string
- .ds line: 32303
- Fetch: API_Config (Config_Name); Assignments (Assignment_ID, ID); Employees (Employee_ID, ID); Referrals_Main (ID)
- Insert: -
- Update: Assignments (Notified_Employee_ID)
- Delete: -
- Read: API_Config (Zepto_Send_Token); Assignments (Assignment_ID, Employee_Link, ID, Notified_Employee_ID, Patient_First_Name, Patient_Last_Name, Referral_Link); Employees (Employee_Email, Employee_First_Name, Employee_ID, ID); Referrals_Main (Referral_ID, Referral_Type)
- Calls: mint_assignment_id
- Called by: workflow Assignments/Assignment_Notify_Provide
- Integrations: AppFunc, HTTP

## send_fax_digest

- Signature: Deluge.send_fax_digest() returns string
- .ds line: 32564
- Fetch: API_Config (Config_Name); Employees (ID); Encounter_PatientVisit (Type_of_Entry); Fax_Log (Fax_Status, Number_Source, Submitted_Time)
- Insert: -
- Update: -
- Delete: -
- Read: API_Config (Zepto_Send_Token); Employees (Employee_Name_Title); Encounter_PatientVisit (Added_Time, Billing_Branch, Clinical_Note_Type, Fax_Status, PVS_ID, Partner_Location_Label, Patient_Full_Name_1, Visit_Status); Fax_Log (Added_User, Destination_Fax, Destination_Name, Fax_Error_Code, Fax_ID, Fax_Status, Override_Reason, Sent_By)
- Calls: is_pvs_email_branch
- Called by: schedule Fax_Digest_Daily_4am
- Integrations: AppFunc, HTTP

## send_imaging_notification

- Signature: Deluge.send_imaging_notification(string p_refKey) returns string
- .ds line: 32740
- Fetch: API_Config (Config_Name); Referrals_Main (ID, Referral_ID)
- Insert: -
- Update: -
- Delete: -
- Read: API_Config (Zepto_Send_Token); Referrals_Main (ID, Referral_ID, Referral_Type)
- Calls: build_imaging_email_html, build_zepto_attachments, get_notification_recipients
- Called by: function process_new_referral
- Integrations: AppFunc, HTTP

## send_pvs_fax

- Signature: Deluge.send_pvs_fax(int pPvsID, string pToName, string pToPartner, string pToFax, string pToAttn, string pRemarks, string pNumberSource, string pOverrideReason, list pImageUrls, list pAttachFiles, int pAttempt, int pOriginalFaxID) returns map
- .ds line: 32832
- Fetch: API_Config (Config_Name); Employees (Employee_Portal_Email); Encounter_PatientVisit (ID); Fax_Attachments (ID); Fax_Log (ID); Sequence_Tracker (Object_Prefix)
- Insert: Fax_Attachments (Added_User, Attachment_Name, Attachment_Type, Fax_Log, Sequence_Number, Source_PVS_Link); Fax_Log (Added_User, Attempt_Number, Cover_Remarks, Destination_Fax, Destination_Name, Fax_ID, Fax_Status, Number_Source, Override_Reason, PVS_Link, Partner_Location_Link, Referral_Link, Submitted_Time)
- Update: API_Config (RC_Access_Token, RC_Token_Expiry); Encounter_PatientVisit (Fax_Status); Fax_Attachments (Attachment_File); Fax_Log (Attachments_Included, Completed_Time, Fax_Error_Reason, Fax_PDF, Fax_Status, Last_Polled_Time, Original_Fax_Link, RC_Conversation_ID, RC_Message_ID, Sent_By); Sequence_Tracker (Object_Sequence)
- Delete: -
- Read: Employees (ID); Encounter_PatientVisit (Billing_Branch, PVS_ID, Patient_Full_Name_1, Referral_Link); Sequence_Tracker (Object_Sequence)
- Calls: build_pvs_fax_html, get_rc_token
- Called by: function retry_failed_faxes, workflow Encounter_PatientVisit/Fax_This_Note_On_Submit, workflow Encounter_PatientVisit/Fax_This_Note_On_Submit1, workflow PVS_Fax_Review/PVS_Fax_Review_Fax_Now
- Integrations: AppFunc, HTTP

## send_referral_confirmation

- Signature: Deluge.send_referral_confirmation(string p_refKey) returns string
- .ds line: 33052
- Fetch: API_Config (Config_Name); Referrals_Main (ID, Referral_ID)
- Insert: -
- Update: -
- Delete: -
- Read: API_Config (Zepto_Send_Token); Referrals_Main (ID, Partner_POC_Email, Referral_ID)
- Calls: build_referral_confirmation_html
- Called by: function process_new_referral
- Integrations: AppFunc, HTTP

## send_referral_notification

- Signature: Deluge.send_referral_notification(string p_refKey) returns string
- .ds line: 33141
- Fetch: API_Config (Config_Name); Referrals_Main (ID, Referral_ID)
- Insert: -
- Update: -
- Delete: -
- Read: API_Config (Zepto_Send_Token); Referrals_Main (ID, Referral_ID, Referral_Type)
- Calls: build_referral_email_html, build_zepto_attachments
- Called by: function process_new_referral
- Integrations: AppFunc, HTTP

## send_via_sendgrid

- Signature: Deluge.send_via_sendgrid(string pTo, string pSubject, string pMessage) returns void
- .ds line: 33233
- Fetch: -
- Insert: -
- Update: -
- Delete: -
- Read: -
- Calls: -
- Called by: function run_pvs_exclusion_monitor, function run_schema_monitor
- Integrations: HTTP

## set_current_rate

- Signature: Deluge.set_current_rate(int rateId) returns void
- .ds line: 33266
- Fetch: Partner_Rates (ID, Partner_Link, Partner_Location_Link, Partner_Rate_Status, Rate_Category, Rate_Type)
- Insert: -
- Update: Partner_Rates (Current_Rate)
- Delete: -
- Read: Partner_Rates (ID, Partner_Link, Partner_Location_Link, Partner_Rates_Effective_Date, Rate_Category, Rate_Type)
- Calls: -
- Called by: function backfill_current_rate, workflow Partner_Rates/Partner_Rate_Current_Flag
- Integrations: -

## set_partner_poc_name_title

- Signature: Deluge.set_partner_poc_name_title(int recId) returns void
- .ds line: 33295
- Fetch: Referrals_Main (ID)
- Insert: -
- Update: Referrals_Main (Partner_POC_Name_Title)
- Delete: -
- Read: Referrals_Main (Partner_POC_First_Name, Partner_POC_Last_Name, Partner_POC_Title)
- Calls: -
- Called by: function backfill_partner_poc_name_title
- Integrations: -

## set_partner_rate_status

- Signature: Deluge.set_partner_rate_status(string p_mode, string p_rateType, string p_skipPartners, string p_status) returns string
- .ds line: 33324
- Fetch: Partner_Locations (ID); Partner_Rates (Rate_Type); Partners (ID)
- Insert: -
- Update: Partner_Rates (Partner_Rate_Status)
- Delete: -
- Read: Partner_Locations (ID, Partner_Location_Label); Partner_Rates (Current_Rate, Partner_Link, Partner_Location_Link, Partner_Rate_Status, Rate_Amount); Partners (ID, Partner_Display_Name)
- Calls: -
- Called by: -
- Integrations: -

## set_patient_full_name

- Signature: Deluge.set_patient_full_name(int recId) returns void
- .ds line: 33414
- Fetch: Referrals_Main (ID)
- Insert: -
- Update: Referrals_Main (Patient_Full_Name)
- Delete: -
- Read: Referrals_Main (Patient_First_Name, Patient_Last_Name, Patient_MI)
- Calls: -
- Called by: function backfill_patient_full_names
- Integrations: -

## set_pvs_cancelled_row_status

- Signature: Deluge.set_pvs_cancelled_row_status(string p_mode, date p_from, date p_to) returns string
- .ds line: 33448
- Fetch: Encounter_PatientVisit (Complexity_Level, Visit_Completion_Date)
- Insert: -
- Update: Encounter_PatientVisit (Row_Status, Row_Status_Note)
- Delete: -
- Read: Encounter_PatientVisit (PVS_ID, Referral_ID, Row_Status, Row_Status_Note, Visit_Completion_Date)
- Calls: -
- Called by: -
- Integrations: -

## set_pvs_complexity

- Signature: Deluge.set_pvs_complexity(string p_mode, string p_pvsId, string p_level) returns string
- .ds line: 33496
- Fetch: Encounter_PatientVisit (ID, PVS_ID)
- Insert: -
- Update: Encounter_PatientVisit (Complexity_Level, Invoice_Status)
- Delete: -
- Read: Encounter_PatientVisit (Complexity_Level, ID, Invoice_Status)
- Calls: -
- Called by: -
- Integrations: -

## set_pvs_diversion

- Signature: Deluge.set_pvs_diversion(string p_mode, date p_from, date p_to, string p_pairs) returns string
- .ds line: 33549
- Fetch: Encounter_PatientVisit (PVS_ID)
- Insert: -
- Update: Encounter_PatientVisit (Diversion_Tracking, Type_of_Diversion)
- Delete: -
- Read: Encounter_PatientVisit (Diversion_Tracking, Visit_Completion_Date)
- Calls: -
- Called by: -
- Integrations: -

## set_pvs_entry_type

- Signature: Deluge.set_pvs_entry_type(string p_mode, string p_pvsIds, string p_type) returns string
- .ds line: 33685
- Fetch: Encounter_PatientVisit (PVS_ID)
- Insert: -
- Update: Encounter_PatientVisit (Type_of_Entry)
- Delete: -
- Read: Encounter_PatientVisit (Type_of_Entry)
- Calls: -
- Called by: -
- Integrations: -

## set_pvs_equipment_charge

- Signature: Deluge.set_pvs_equipment_charge(string p_pvsId, string p_amount, string p_details) returns string
- .ds line: 33746
- Fetch: Encounter_PatientVisit (PVS_ID)
- Insert: -
- Update: -
- Delete: -
- Read: -
- Calls: -
- Called by: -
- Integrations: -

## set_pvs_hold_batch

- Signature: Deluge.set_pvs_hold_batch(string p_mode, string p_pvsIds, string p_hold) returns string
- .ds line: 33800
- Fetch: Encounter_PatientVisit (ID, PVS_ID)
- Insert: -
- Update: Encounter_PatientVisit (Hold_From_Invoicing)
- Delete: -
- Read: Encounter_PatientVisit (Hold_From_Invoicing, ID, Invoice_Link, Row_Status)
- Calls: -
- Called by: -
- Integrations: -

## set_pvs_procedures

- Signature: Deluge.set_pvs_procedures(string p_mode, date p_from, date p_to, string p_pairs) returns string
- .ds line: 33884
- Fetch: Encounter_PatientVisit (PVS_ID)
- Insert: -
- Update: Encounter_PatientVisit (Type_of_Procedures)
- Delete: -
- Read: Encounter_PatientVisit (Type_of_Procedures, Visit_Completion_Date)
- Calls: -
- Called by: -
- Integrations: -

## set_pvs_provider

- Signature: Deluge.set_pvs_provider(string p_mode, string p_pvsId, string p_employeeEmail) returns string
- .ds line: 33985
- Fetch: Employees (ID); Encounter_PatientVisit (ID, PVS_ID)
- Insert: -
- Update: Encounter_PatientVisit (Employee_Email, Employee_First_Name, Employee_Full_Name, Employee_Initials, Employee_Last_Name, Employee_Link, Employee_Name_Title, Employee_Title, PVS_ID, Provider_Login_Email)
- Delete: -
- Read: Employees (Employee_Email, Employee_First_Name, Employee_Initials, Employee_Last_Name, Employee_Name_Title, Employee_Portal_Email, Employee_Title, ID); Encounter_PatientVisit (Employee_Email, Employee_First_Name, Employee_Full_Name, Employee_Initials, Employee_Last_Name, Employee_Link, Employee_Name_Title, Employee_Title, ID, PVS_ID, Provider_Login_Email)
- Calls: -
- Called by: function set_pvs_provider_batch
- Integrations: -

## set_pvs_provider_batch

- Signature: Deluge.set_pvs_provider_batch(string p_mode, string p_pvsIds, string p_employeeEmail) returns string
- .ds line: 34123
- Fetch: -
- Insert: -
- Update: -
- Delete: -
- Read: -
- Calls: set_pvs_provider
- Called by: -
- Integrations: AppFunc

## set_pvs_referral_link

- Signature: Deluge.set_pvs_referral_link(string p_pvsId, string p_refId, string p_mode) returns string
- .ds line: 34151
- Fetch: Encounter_PatientVisit (PVS_ID); Referrals_Main (ID, Referral_ID)
- Insert: -
- Update: Encounter_PatientVisit (Referral_Link)
- Delete: -
- Read: Encounter_PatientVisit (ID, Patient_DOB, Referral_Link); Referrals_Main (ID, Patient_DOB, Referral_ID)
- Calls: -
- Called by: -
- Integrations: -

## sos_referral_health

- Signature: Deluge.sos_referral_health(string p_mode, string p_scope, int p_limit) returns string
- .ds line: 34205
- Fetch: Assignments (ID); Encounter_PatientVisit (Invoice_Link); Referrals_Main (ID)
- Insert: -
- Update: -
- Delete: -
- Read: Assignments (Referral_Link); Encounter_PatientVisit (Referral_Link); Referrals_Main (ID, Partner_Branch, Partner_Branch_Link, Partner_Organization, Partner_POC_Email, Patient_DOB, Patient_DOB1, Patient_First_Name, Patient_Last_Name, Referral_Date, Referral_ID, Referral_ID_Stamp, Referral_Type)
- Calls: parse_patient_dob, process_new_referral
- Called by: -
- Integrations: AppFunc

## sweep_unnotified_referrals

- Signature: Deluge.sweep_unnotified_referrals(string p_mode, string p_scope, int p_limit) returns string
- .ds line: 34455
- Fetch: Referral_Sweep_Log (Emailed, ID); Referrals_Main (ID, Referral_Date, Referral_ID)
- Insert: Referral_Sweep_Log (Added_User, Emailed, FRun_Detail, Failed_Count, Failure_Detail, Found_Count, Repaired_Count, Repaired_List, Run_Status, Run_Time)
- Update: Referral_Sweep_Log (Emailed)
- Delete: -
- Read: Referral_Sweep_Log (Failed_Count, Failure_Detail, Found_Count, ID, Repaired_Count, Repaired_List, Run_Status, Run_Time); Referrals_Main (ID, Referral_ID)
- Calls: process_new_referral
- Called by: -
- Integrations: AppFunc, Email

## sync_pvs_branch_from_referral

- Signature: Deluge.sync_pvs_branch_from_referral(string p_pvsId, string p_mode) returns string
- .ds line: 34689
- Fetch: Encounter_PatientVisit (ID, PVS_ID); Partner_Locations (ID); Partner_Rates (Current_Rate, Partner_Location_Link, Rate_Type); Referrals_Main (ID)
- Insert: -
- Update: Encounter_PatientVisit (Billing_Branch, Complexity_Charge, Partner_Branch, Partner_Location_Label, Partner_Organization)
- Delete: -
- Read: Encounter_PatientVisit (Additional_Charges, Billing_Branch, Complexity_Charge, Complexity_Level, ID, Invoice_Status, Referral_Link); Partner_Locations (Partner_Location_Label); Partner_Rates (Rate_Amount); Referrals_Main (ID, Partner_Branch_Link, Referral_ID)
- Calls: partner_branch_values
- Called by: -
- Integrations: AppFunc

## sync_pvs_from_referral

- Signature: Deluge.sync_pvs_from_referral(string p_mode, date p_from, date p_to) returns string
- .ds line: 34778
- Fetch: Encounter_PatientVisit (Visit_Completion_Date); Referrals_Main (ID)
- Insert: -
- Update: Encounter_PatientVisit (Facility_Name, Partner_Branch, Partner_ID, Partner_Location_Label, Partner_Organization, Patient_DOB, Patient_First_Name, Patient_Gender, Patient_Hospice_ID, Patient_Last_Name, Patient_Location, Referral_Date, Referral_ID)
- Delete: -
- Read: Encounter_PatientVisit (Facility_Name, ID, PVS_ID, Partner_Branch, Partner_ID, Partner_Location_Label, Partner_Organization, Patient_Address, Patient_DOB, Patient_First_Name, Patient_Gender, Patient_Hospice_ID, Patient_Last_Name, Patient_Location, Referral_Date, Referral_ID, Referral_Link, Row_Status); Referrals_Main (Facility_Name, Partner_Branch, Partner_ID, Partner_Location_Label, Partner_Organization, Patient_Address, Patient_DOB, Patient_First_Name, Patient_Gender, Patient_Hospice_ID, Patient_Last_Name, Patient_Location, Referral_Date, Referral_ID)
- Calls: -
- Called by: -
- Integrations: -

## test_github_commit

- Signature: Deluge.test_github_commit() returns void
- .ds line: 35084
- Fetch: -
- Insert: -
- Update: -
- Delete: -
- Read: -
- Calls: -
- Called by: -
- Integrations: HTTP

## test_schema_connection

- Signature: Deluge.test_schema_connection() returns void
- .ds line: 35115
- Fetch: -
- Insert: -
- Update: -
- Delete: -
- Read: -
- Calls: -
- Called by: -
- Integrations: HTTP

## test_smtp

- Signature: Deluge.test_smtp() returns string
- .ds line: 35125
- Fetch: -
- Insert: -
- Update: -
- Delete: -
- Read: -
- Calls: -
- Called by: -
- Integrations: Email

## widget_today_visits

- Signature: Deluge.widget_today_visits() returns map
- .ds line: 35136
- Fetch: Assignments (Referral_Link); Employees (Employee_Status, ID); Encounter_PatientVisit (Referral_ID, Referral_Link, Visit_Completion_Date); Referrals_Main (Referral_Date)
- Insert: -
- Update: -
- Delete: -
- Read: Assignments (Assignment_ID, Employee_Link, ID, Patient_First_Name, Patient_Last_Name, Referral_Link, Visit_Status); Employees (Employee_First_Name, Employee_Job_Title, Employee_Last_Name, ID, Portal_Access_Types); Encounter_PatientVisit (Row_Status); Referrals_Main (ID, Referral_Date, Referral_ID, Referral_Type)
- Calls: is_portal_admin
- Called by: -
- Integrations: AppFunc
