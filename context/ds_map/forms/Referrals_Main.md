# Referrals_Main

- Display name: Referrals Main
- .ds line: 5797
- Fields (excluding sections): 70
- Parent form: -

## Fields

| Link name | Display name | Type | Lookup target |
|---|---|---|---|
| Referral_Type_Section | Referral Type | section | - |
| Referral_Source | Referral Source | radiobuttons | - |
| Referral_Type | Service | radiobuttons | - |
| Patient_Details_Section | Patient Details | section | - |
| Patient_First_Name | Patient First Name | text | - |
| Patient_MI | Patient MI | text | - |
| Patient_Last_Name | Patient Last Name | text | - |
| Patient_DOB | Patient DOB | date | - |
| Patient_DOB1 | Patient DOB | text | - |
| Patient_Gender | Patient Gender | radiobuttons | - |
| Patient_Hospice_ID | Patient Hospice ID | text | - |
| Patient_MBI | Patient MBI | text | - |
| Patient_SSN | Patient SSN | text | - |
| Patient_Phone | Patient Phone | text | - |
| Has_Additional_Contact | Is there an additional contact? | radiobuttons | - |
| Additional_Contact_Section | Additional Contact Info | section | - |
| AC_First_Name | AC First Name | text | - |
| AC_Last_Name | AC Last Name | text | - |
| AC_Phone | AC Phone | text | - |
| AC_Relationship_to_Patient | AC Relationship to Patient | picklist | - |
| Patient_Location_Section | Patient Location | section | - |
| Patient_Location | Patient Location | radiobuttons | - |
| Facility_Name | Facility Name | text | - |
| Facility_Phone | Facility Phone | text | - |
| Facility_Room_Number | Facility Room Number | text | - |
| Patient_Address | Patient Address | address | - |
| Patient_Full_Address | Patient Full Address | text | - |
| Patient_Medical_Details_Section | Patient Medical Details | section | - |
| Referral_Reason | Reason for Referral | textarea | - |
| Partner_ICD_Codes | Partner ICD Codes | text | - |
| X_Ray_Needed | Will an X-Ray be needed for this referral? | radiobuttons | - |
| Patient_Has_Allergies | Does this patient have allergies? | radiobuttons | - |
| List_Patient_Allergies | List Patient Allergies | textarea | - |
| Patient_Has_Anticoagulants | Does the patient take anticoagulants? | radiobuttons | - |
| List_Patient_Anticoagulants | List Patient Anticoagulants | textarea | - |
| Patient_Advanced_Directives_Section | Patient Advanced Directives | section | - |
| Patient_Has_Advanced_Directives | Does the patient have Advanced Directives? | radiobuttons | - |
| Advanced_Directives_Details | Advanced Directives Details | textarea | - |
| General_Information_Section | General Information | section | - |
| Additional_Information | Additional Information | textarea | - |
| General_Files_Upload | General Files Upload | upload file | - |
| Imaging_Order_Details | Imaging Order Details | section | - |
| Imaging_Type_Order | Imaging Test(s) to be Ordered | text | - |
| Imaging_Body_Site | Body Part / Affected Area | text | - |
| Imaging_Order_Indication | Reason for Imaging Order(s) | textarea | - |
| Imaging_Orders_Upload | Imaging Orders Upload | upload file | - |
| Details_Section_3008 | 3008 Details Section | section | - |
| File_Upload_3008 | 3008 File Upload | upload file | - |
| Referral_Partner_Details_Section | Referral Partner Details | section | - |
| Partner_Link | Partner Lookup | picklist | Partners |
| Partner_Branch_Link | Partner Branch Lookup | picklist | Partner_Locations |
| Partner_Organization | Partner Organization | text | - |
| Partner_Branch | Partner Branch/Location | text | - |
| Partner_POC_First_Name | Partner POC First Name | text | - |
| Partner_POC_Last_Name | Partner POC Last Name | text | - |
| Partner_POC_Title | Partner POC Title | picklist | - |
| Partner_POC_Team | Partner POC Team | text | - |
| Partner_POC_Phone | Partner POC Phone | text | - |
| Partner_POC_Email | Partner POC Email | email | - |
| Referral_Attachments_Section | Referral Attachments Section | section | - |
| Files_3008_URLs | 3008 File URLs | textarea | - |
| General_Files_URLs | General Files URLs | textarea | - |
| Imaging_Orders_URLs | Imaging Orders URLs | textarea | - |
| System_Fields_Section | System Fields | section | - |
| Data_Issues | Data Issues | textarea | - |
| Referral_ID | Referral ID | text | - |
| Referral_Date | Referral Date | date | - |
| Referral_Date1 | Referral Date (Don't Use) | text | - |
| Referral_ID_Stamp | Referral ID Stamp | text | - |
| Patient_Full_Name | Patient Full Name | text | - |
| AC_Full_Name | AC Full Name | text | - |
| Partner_POC_Name_Title | Partner POC Name & Title | text | - |
| Partner_ID | Partner ID | text | - |
| Partner_ID_Stamp | Partner ID Stamp | text | - |
| Partner_Location_Label | Partner Location Label | text | - |
| Referral_Added_Time | Referral Added Time | datetime | - |
| Form_Token | Form Token | text | - |
| Assignment_Status | Assignment Status | picklist | - |
| Employee_Link | Employee Link | picklist | Employees |
| Cognito_Referral_ID | Cognito Referral ID | text | - |
| Partner_Branch_Submitted | Partner Branch Submitted | text | - |
| Notified_Time | Notified Time | datetime | - |

## Workflows

### Branch_Sets_Partner

- Display: Branch Sets Partner
- Record event: on add or edit
- Form event: OnUserInput of Partner_Branch_Link
- Status: ENABLED
- .ds line: 37963
- Fields read: Partner_Branch_Link
- Fields set: Partner_Branch, Partner_ID, Partner_Link, Partner_Location_Label, Partner_Organization
- Fields shown/hidden/enabled/disabled: -
- Functions called: -
- Other forms: fetch Partner_Locations (ID); read Partner_Locations (Partner_Link, Partner_Location_Label, Partner_Location_Name); read Partners (Partner_Display_Name, Partner_ID)

### Branch_Sets_Partner_Link

- Display: Branch Sets Partner Link
- Record event: on add or edit
- Form event: OnSuccess
- Status: DISABLED
- .ds line: 37998
- Fields read: Partner_Branch_Link
- Fields set: Partner_ID
- Fields shown/hidden/enabled/disabled: -
- Functions called: -
- Other forms: fetch Partner_Locations (ID); fetch Partners (ID); read Partner_Locations (Partner_Link); read Partners (ID, Partner_ID)

### Build_Patient_Full_Addres1

- Display: Build Patient Full Address
- Record event: on add or edit
- Form event: OnUserInput of Patient_Address
- Status: ENABLED
- .ds line: 37443
- Fields read: Patient_Address
- Fields set: Patient_Full_Address
- Fields shown/hidden/enabled/disabled: -
- Functions called: -
- Other forms: -

### DM_Full_Name_Generator

- Display: DM Full Name Generator
- Record event: on add or edit
- Form event: OnUserInput of AC_Last_Name
- Status: ENABLED
- .ds line: 37608
- Fields read: AC_First_Name, AC_Last_Name
- Fields set: AC_Full_Name
- Fields shown/hidden/enabled/disabled: -
- Functions called: -
- Other forms: -

### Decision_Maker_Phone_Form1

- Display: Decision Maker Phone Format
- Record event: on add or edit
- Form event: OnUserInput of AC_Phone
- Status: ENABLED
- .ds line: 35636
- Fields read: -
- Fields set: AC_Phone
- Fields shown/hidden/enabled/disabled: -
- Functions called: -
- Other forms: -

### Default_Hide_On_Load1

- Display: Default Hide On Load
- Record event: on add or edit
- Form event: OnLoad
- Status: ENABLED
- .ds line: 37484
- Fields read: -
- Fields set: -
- Fields shown/hidden/enabled/disabled: Patient_Full_Address
- Functions called: -
- Other forms: -

### Facility_Phone_Format1

- Display: Facility Phone Format
- Record event: on add or edit
- Form event: OnUserInput of Facility_Phone
- Status: ENABLED
- .ds line: 35694
- Fields read: -
- Fields set: Facility_Phone
- Fields shown/hidden/enabled/disabled: -
- Functions called: -
- Other forms: -

### Partner_Contact_Lookup

- Display: Partner Contact Lookup
- Record event: on add
- Form event: OnUserInput of Partner_POC_Email
- Status: ENABLED
- .ds line: 37927
- Fields read: Partner_POC_Email
- Fields set: Partner_POC_First_Name, Partner_POC_Last_Name, Partner_POC_Phone, Partner_POC_Team, Partner_POC_Title
- Fields shown/hidden/enabled/disabled: -
- Functions called: -
- Other forms: fetch Partner_Referral_Contacts (Partner_POC_Email); read Partner_Referral_Contacts (Partner_POC_First_Name, Partner_POC_Last_Name, Partner_POC_Phone, Partner_POC_Team, Partner_POC_Title)

### Partner_POC_Name_Title_Ge

- Display: Partner POC Name & Title Generator
- Record event: on edit
- Form event: OnSuccess
- Status: ENABLED
- .ds line: 38655
- Fields read: Partner_POC_First_Name, Partner_POC_Last_Name, Partner_POC_Title
- Fields set: Partner_POC_Name_Title
- Fields shown/hidden/enabled/disabled: -
- Functions called: -
- Other forms: -

### Patient_Full_Name_Generat

- Display: Patient Full Name Generator
- Record event: on edit
- Form event: OnSuccess
- Status: ENABLED
- .ds line: 38615
- Fields read: Patient_First_Name, Patient_Last_Name, Patient_MI
- Fields set: Patient_Full_Name
- Fields shown/hidden/enabled/disabled: -
- Functions called: -
- Other forms: -

### Patient_Phone_Format1

- Display: Patient Phone Format
- Record event: on add or edit
- Form event: OnUserInput of Patient_Phone
- Status: ENABLED
- .ds line: 35607
- Fields read: -
- Fields set: Patient_Phone
- Fields shown/hidden/enabled/disabled: -
- Functions called: -
- Other forms: -

### Referral_DOB_Sync_On_Edit

- Display: Referral DOB Sync On Edit
- Record event: on edit
- Form event: OnSuccess
- Status: ENABLED
- .ds line: 39105
- Fields read: ID, Patient_DOB1
- Fields set: -
- Fields shown/hidden/enabled/disabled: -
- Functions called: parse_patient_dob
- Other forms: fetch Referrals_Main (ID); update Referrals_Main (Patient_DOB); read Referrals_Main (Patient_DOB)

### Referral_Data_Issues_Chec

- Display: Referral Data Issues Check
- Record event: on add or edit
- Form event: OnSuccess
- Status: ENABLED
- .ds line: 39027
- Fields read: ID
- Fields set: -
- Fields shown/hidden/enabled/disabled: -
- Functions called: compute_data_issues
- Other forms: fetch Referrals_Main (ID); update Referrals_Main (Data_Issues); read Referrals_Main (Partner_Organization, Patient_First_Name, Patient_Last_Name, Referral_ID, Referral_Type)

### Referral_Data_Issues_Sync

- Display: Referral Data Issues Sync On Edit
- Record event: on edit
- Form event: OnSuccess
- Status: ENABLED
- .ds line: 39137
- Fields read: ID
- Fields set: -
- Fields shown/hidden/enabled/disabled: -
- Functions called: compute_data_issues
- Other forms: fetch Referrals_Main (ID); update Referrals_Main (Data_Issues); read Referrals_Main (Data_Issues)

### Referral_Partner_POC_Phon

- Display: Referral Partner POC Phone Format
- Record event: on add or edit
- Form event: OnUserInput of Partner_POC_Phone
- Status: ENABLED
- .ds line: 35665
- Fields read: -
- Fields set: Partner_POC_Phone
- Fields shown/hidden/enabled/disabled: -
- Functions called: -
- Other forms: -

### Referral_Resolves_Partner

- Display: Referral Resolves Partner On Save
- Record event: on add or edit
- Form event: OnValidate
- Status: ENABLED
- .ds line: 40212
- Fields read: Partner_POC_Email
- Fields set: Partner_Branch, Partner_Branch_Link, Partner_Branch_Submitted, Partner_ID, Partner_ID_Stamp, Partner_Link, Partner_Location_Label, Partner_Organization
- Fields shown/hidden/enabled/disabled: -
- Functions called: partner_branch_values, resolve_branch_id
- Other forms: fetch Partner_Locations (Partner_Location_ID); read Partner_Locations (ID)

### Referrals_Main_On_Create_

- Display: Referrals Main On Create - Master
- Record event: on add
- Form event: OnSuccess
- Status: ENABLED
- .ds line: 38596
- Fields read: ID
- Fields set: -
- Fields shown/hidden/enabled/disabled: -
- Functions called: process_new_referral
- Other forms: -

### SSN_Format1

- Display: SSN Format
- Record event: on add or edit
- Form event: OnUserInput of Patient_SSN
- Status: ENABLED
- .ds line: 35579
- Fields read: -
- Fields set: Patient_SSN
- Fields shown/hidden/enabled/disabled: -
- Functions called: -
- Other forms: -

### Sender_Sets_Branch

- Display: Sender Sets Branch
- Record event: on add or edit
- Form event: OnUserInput of Partner_POC_Email
- Status: ENABLED
- .ds line: 38228
- Fields read: Partner_POC_Email
- Fields set: Partner_Branch_Link
- Fields shown/hidden/enabled/disabled: -
- Functions called: -
- Other forms: fetch Partner_Referral_Contacts (Partner_POC_Email); read Partner_Referral_Contacts (ID, Partner_Locations_Link)

## Reverse index

Every item that references a field of this form.

- Referrals_Main.Referral_Source: function assign_direct_partner [update]; function backfill_pvs_referral_source [read]; function backfill_pvs_system_fields_range [read]; function diag_mpu_readiness [read]; function diag_referral_dump [read]; function run_import_backfills [read]; function send_activity_digest [read]; workflow Encounter_PatientVisit/PVS_System_Fields_Stamp_O [read]; workflow Encounter_PatientVisit/Referral_Link_Pre_Fill [read]
- Referrals_Main.Referral_Type: function audit_month_integrity [read]; function build_3008_email_html [read]; function build_imaging_email_html [read]; function build_referral_confirmation_html [read]; function build_referral_email_html [read]; function compute_data_issues [read]; function dash_metrics [read]; function dash_metrics_range [read]; function diag_3008_link_check [fetch]; function diag_3008_no_pvs_list [fetch]; function diag_3008_no_pvs_sheet [fetch]; function diag_3008_overdue [fetch]; function diag_blank_referral_id [read]; function diag_compliance_gap [read]; function diag_duplicate_patient_referrals [read]; function diag_imaging_notify_check [read]; function diag_invoice_pvs [read]; function diag_map_cognito_refs [read]; function diag_match_3008_refs [read]; function diag_missing_dob [read]; function diag_month_billing_gap [read]; function diag_mpu_3008_export [fetch]; function diag_mpu_readiness [read]; function diag_mpu_referral_export [read]; function diag_orphan_referral [read]; function diag_pvs_blank_reason [read]; function diag_pvs_referral_match [read]; function diag_ref_patient_pvs_match [read]; function diag_referral_branch [read]; function diag_referral_by_name [read]; function diag_referral_collision [read]; function diag_referral_dump [read]; function diag_referral_id_records [read]; function diag_referral_imaging [read]; function diag_referrals_missing_pvs [read]; function diag_safe_test_referrals [read]; function diag_unnotified_referrals [read]; function resend_referral_notifications [read]; function send_3008_notification [read]; function send_activity_digest [read]; function send_assignment_notification [read]; function send_imaging_notification [read]; function send_referral_notification [read]; function sos_referral_health [read]; function widget_today_visits [read]; page Drilldown_Data [read]; workflow Assignments/Assignment_Visit_Status_C [read]; workflow Referrals_Main/Referral_Data_Issues_Chec [read]
- Referrals_Main.Patient_First_Name: function audit_month_integrity [read]; function backfill_referral_uploads [read]; function compute_data_issues [read]; function create_3008_pvs_july [read]; function create_3008_pvs_sept [read]; function diag_blank_referral_id [read]; function diag_duplicate_patient_referrals [read]; function diag_duplicate_referral_ids [read]; function diag_find_referral [read]; function diag_import_ref_matches [read]; function diag_match_3008_refs [read]; function diag_missing_dob [read]; function diag_month_billing_gap [read]; function diag_mpu_3008_export [read]; function diag_pvs_names [read]; function diag_pvs_vs_referral [read]; function diag_ref_names [read]; function diag_referral_by_name [read]; function diag_referral_id_records [read]; function diag_safe_test_referrals [read]; function diag_unnotified_referrals [read]; function process_new_referral [read]; function relink_pvs_to_referral [read]; function repair_invoice_pvs_from_referral [read]; function run_import_backfills [read]; function set_patient_full_name [read]; function sos_referral_health [read]; function sync_pvs_from_referral [read]; workflow Assignments/Assignment_Pull_From_Refe1 [read]; workflow Encounter_PatientVisit/Referral_Link_Pre_Fill [read]; workflow Referrals_Main/Patient_Full_Name_Generat [read]; workflow Referrals_Main/Referral_Data_Issues_Chec [read]
- Referrals_Main.Patient_MI: function create_3008_pvs_july [read]; function create_3008_pvs_sept [read]; function process_new_referral [read]; function relink_pvs_to_referral [read]; function repair_invoice_pvs_from_referral [read]; function run_import_backfills [read]; function set_patient_full_name [read]; workflow Encounter_PatientVisit/Referral_Link_Pre_Fill [read]; workflow Referrals_Main/Patient_Full_Name_Generat [read]
- Referrals_Main.Patient_Last_Name: function audit_month_integrity [read]; function backfill_mint_missing_referral_ids [read]; function backfill_referral_uploads [read]; function compute_data_issues [read]; function create_3008_pvs_july [read]; function create_3008_pvs_sept [read]; function diag_blank_referral_id [read]; function diag_duplicate_patient_referrals [read]; function diag_duplicate_referral_ids [read]; function diag_find_referral [read]; function diag_import_ref_matches [read]; function diag_map_cognito_refs [read]; function diag_match_3008_refs [read]; function diag_missing_dob [read]; function diag_month_billing_gap [read]; function diag_mpu_3008_export [read]; function diag_orphan_referral [read]; function diag_pvs_names [read]; function diag_pvs_vs_referral [read]; function diag_ref_names [read]; function diag_ref_patient_pvs_match [read]; function diag_referral_by_name [read]; function diag_referral_id_records [read]; function diag_referral_ids [read]; function diag_safe_test_referrals [read]; function diag_unnotified_referrals [read]; function diag_zztest_referrals [read]; function process_new_referral [read]; function relink_pvs_to_referral [read]; function repair_invoice_pvs_from_referral [read]; function run_import_backfills [read]; function set_patient_full_name [read]; function sos_referral_health [read]; function sync_pvs_from_referral [read]; workflow Assignments/Assignment_Pull_From_Refe1 [read]; workflow Encounter_PatientVisit/Referral_Link_Pre_Fill [read]; workflow Referrals_Main/Patient_Full_Name_Generat [read]; workflow Referrals_Main/Referral_Data_Issues_Chec [read]
- Referrals_Main.Patient_DOB: function audit_month_integrity [read]; function backfill_patient_dob [fetch, update]; function build_3008_email_html [read]; function build_imaging_email_html [read]; function build_referral_email_html [read]; function compute_data_issues [read]; function create_3008_pvs_july [read]; function create_3008_pvs_sept [read]; function diag_3008_no_pvs_sheet [read]; function diag_blank_referral_id [read]; function diag_dob_coverage [read]; function diag_duplicate_patient_referrals [read]; function diag_map_cognito_refs [fetch]; function diag_match_3008_refs [fetch]; function diag_missing_dob [fetch]; function diag_month_billing_gap [read]; function diag_mpu_3008_export [read]; function diag_orphan_referral [fetch, read]; function diag_pvs_names [read]; function diag_pvs_referral_match [fetch, read]; function diag_pvs_vs_referral [read]; function diag_ref_names [read]; function diag_ref_patient_pvs_match [fetch, read]; function diag_referral_dump [read]; function diag_referral_id_records [read]; function process_new_referral [update]; function relink_pvs_to_referral [read]; function repair_invoice_pvs_from_referral [read]; function resync_patient_dob [read, update]; function run_import_backfills [read, update]; function set_pvs_referral_link [read]; function sos_referral_health [read]; function sync_pvs_from_referral [read]; workflow Assignments/Assignment_Pull_From_Refe1 [read]; workflow Encounter_PatientVisit/PVS_Patient_Data_Push_Bac [read, update]; workflow Encounter_PatientVisit/Referral_Link_Pre_Fill [read]; workflow Imaging_Orders/Imaging_Referral_Link_Pre [read]; workflow Referrals_Main/Referral_DOB_Sync_On_Edit [read, update]
- Referrals_Main.Patient_DOB1: function audit_month_integrity [read]; function backfill_patient_dob [read]; function compute_data_issues [read]; function diag_blank_referral_id [read]; function diag_dob_coverage [read]; function diag_missing_dob [read]; function diag_referral_dump [read]; function diag_referral_id_records [read]; function process_new_referral [read]; function resync_patient_dob [read]; function run_import_backfills [read]; function sos_referral_health [read]; workflow Encounter_PatientVisit/PVS_Patient_Data_Push_Bac [update]; workflow Referrals_Main/Referral_DOB_Sync_On_Edit [read]
- Referrals_Main.Patient_Gender: function audit_month_integrity [read]; function build_3008_email_html [read]; function build_imaging_email_html [read]; function build_referral_email_html [read]; function create_3008_pvs_july [read]; function create_3008_pvs_sept [read]; function diag_referral_dump [read]; function relink_pvs_to_referral [read]; function repair_invoice_pvs_from_referral [read]; function sync_pvs_from_referral [read]; workflow Encounter_PatientVisit/Referral_Link_Pre_Fill [read]; workflow Imaging_Orders/Imaging_Referral_Link_Pre [read]
- Referrals_Main.Patient_Hospice_ID: function audit_month_integrity [read]; function build_3008_email_html [read]; function build_imaging_email_html [read]; function build_pvs_fax_html [read]; function build_referral_email_html [read]; function compute_data_issues [read]; function create_3008_pvs_july [read]; function create_3008_pvs_sept [read]; function diag_invoice_patient_gaps [read]; function diag_pvs_hospice_ids [read]; function diag_referral_dump [read]; function relink_pvs_to_referral [read]; function repair_invoice_pvs_from_referral [read]; function run_import_backfills [read]; function sync_pvs_from_referral [read]; workflow Encounter_PatientVisit/Referral_Link_Pre_Fill [read]; workflow Imaging_Orders/Imaging_Referral_Link_Pre [read]; workflow PVS_Fax_Review/PVS_Fax_Review_Fax_Now [read]
- Referrals_Main.Patient_MBI: function diag_referral_dump [read]
- Referrals_Main.Patient_SSN: function compute_data_issues [read]; function process_new_referral [read, update]; function run_import_backfills [read]; workflow Encounter_PatientVisit/Referral_Link_Pre_Fill [read]; workflow Referrals_Main/SSN_Format1 [set, trigger]
- Referrals_Main.Patient_Phone: function audit_month_integrity [read]; function build_3008_email_html [read]; function build_imaging_email_html [read]; function build_referral_email_html [read]; function compute_data_issues [read]; function create_3008_pvs_july [read]; function create_3008_pvs_sept [read]; function diag_referral_dump [read]; function process_new_referral [read, update]; function relink_pvs_to_referral [read]; function run_import_backfills [read]; workflow Assignments/Assignment_Pull_From_Refe1 [read]; workflow Encounter_PatientVisit/PVS_Patient_Data_Push_Bac [read, update]; workflow Encounter_PatientVisit/Referral_Link_Pre_Fill [read]; workflow Imaging_Orders/Imaging_Referral_Link_Pre [read]; workflow Referrals_Main/Patient_Phone_Format1 [set, trigger]
- Referrals_Main.Has_Additional_Contact: function build_3008_email_html [read]; function build_imaging_email_html [read]; function build_referral_email_html [read]; function compute_data_issues [read]; workflow Imaging_Orders/Imaging_Referral_Link_Pre [read]
- Referrals_Main.AC_First_Name: function backfill_dm_full_names [read]; function compute_data_issues [read]; function process_new_referral [read]; workflow Referrals_Main/DM_Full_Name_Generator [read]
- Referrals_Main.AC_Last_Name: function backfill_dm_full_names [read]; function compute_data_issues [read]; function process_new_referral [read]; workflow Referrals_Main/DM_Full_Name_Generator [read, trigger]
- Referrals_Main.AC_Phone: function build_3008_email_html [read]; function build_imaging_email_html [read]; function build_referral_email_html [read]; function compute_data_issues [read]; function diag_referral_dump [read]; function process_new_referral [read, update]; workflow Referrals_Main/Decision_Maker_Phone_Form1 [set, trigger]
- Referrals_Main.AC_Relationship_to_Patient: function compute_data_issues [read]; function diag_referral_dump [read]
- Referrals_Main.Patient_Location: function audit_month_integrity [read]; function build_3008_email_html [read]; function build_imaging_email_html [read]; function build_referral_email_html [read]; function compute_data_issues [read]; function create_3008_pvs_july [read]; function create_3008_pvs_sept [read]; function diag_pvs_vs_referral [read]; function diag_referral_dump [read]; function process_new_referral [read]; function relink_pvs_to_referral [read]; function sync_pvs_from_referral [read]; workflow Assignments/Assignment_Pull_From_Refe1 [read]; workflow Encounter_PatientVisit/Referral_Link_Pre_Fill [read]; workflow Imaging_Orders/Imaging_Referral_Link_Pre [read]
- Referrals_Main.Facility_Name: function audit_month_integrity [read]; function build_3008_email_html [read]; function build_imaging_email_html [read]; function build_referral_email_html [read]; function compute_data_issues [read]; function create_3008_pvs_july [read]; function create_3008_pvs_sept [read]; function diag_pvs_vs_referral [read]; function diag_referral_dump [read]; function diag_room_number_gaps [read]; function process_new_referral [read]; function relink_pvs_to_referral [read]; function sync_pvs_from_referral [read]; workflow Assignments/Assignment_Pull_From_Refe1 [read]; workflow Encounter_PatientVisit/Referral_Link_Pre_Fill [read]; workflow Imaging_Orders/Imaging_Referral_Link_Pre [read]
- Referrals_Main.Facility_Phone: function audit_month_integrity [read]; function build_3008_email_html [read]; function build_imaging_email_html [read]; function build_referral_email_html [read]; function compute_data_issues [read]; function create_3008_pvs_july [read]; function create_3008_pvs_sept [read]; function diag_referral_dump [read]; function diag_room_number_gaps [read]; function process_new_referral [read, update]; function relink_pvs_to_referral [read]; function run_import_backfills [read]; workflow Assignments/Assignment_Pull_From_Refe1 [read]; workflow Encounter_PatientVisit/Referral_Link_Pre_Fill [read]; workflow Imaging_Orders/Imaging_Referral_Link_Pre [read]; workflow Referrals_Main/Facility_Phone_Format1 [set, trigger]
- Referrals_Main.Facility_Room_Number: function build_3008_email_html [read]; function build_imaging_email_html [read]; function build_referral_email_html [read]; function compute_data_issues [read]; function create_3008_pvs_july [read]; function create_3008_pvs_sept [read]; function diag_room_number_gaps [read]; function process_new_referral [read]; function relink_pvs_to_referral [read]; function run_import_backfills [read]; workflow Assignments/Assignment_Pull_From_Refe1 [read]; workflow Encounter_PatientVisit/Referral_Link_Pre_Fill [read]; workflow Imaging_Orders/Imaging_Referral_Link_Pre [read]
- Referrals_Main.Patient_Address: function audit_month_integrity [read]; function backfill_patient_full_addresses [read]; function backfill_pvs_address_from_referral [read]; function compute_data_issues [read]; function process_new_referral [read]; function run_import_backfills [read]; function sync_pvs_from_referral [read]; workflow Assignments/Assignment_Pull_From_Refe1 [read]; workflow Encounter_PatientVisit/PVS_Patient_Data_Push_Bac [read]; workflow Encounter_PatientVisit/Referral_Link_Pre_Fill [read]; workflow Imaging_Orders/Imaging_Referral_Link_Pre [read]; workflow Referrals_Main/Build_Patient_Full_Addres1 [read, trigger]
- Referrals_Main.Patient_Full_Address: function backfill_patient_full_addresses [fetch, update]; function build_3008_email_html [read]; function build_imaging_email_html [read]; function build_referral_email_html [read]; function create_3008_pvs_july [read]; function create_3008_pvs_sept [read]; function diag_referral_dump [read]; function process_new_referral [update]; function run_import_backfills [read, update]; workflow Referrals_Main/Build_Patient_Full_Addres1 [set]; workflow Referrals_Main/Default_Hide_On_Load1 [show/hide]
- Referrals_Main.Referral_Reason: function audit_month_integrity [read]; function backfill_pvs_system_fields_range [read]; function build_imaging_email_html [read]; function build_referral_email_html [read]; function compute_data_issues [read]; function create_3008_pvs_july [read]; function create_3008_pvs_sept [read]; function diag_pvs_blank_reason [read]; function diag_referral_dump [read]; function diag_unnotified_referrals [read]; function relink_pvs_to_referral [read]; function repair_invoice_pvs_from_referral [read]; function run_import_backfills [read]; function send_activity_digest [read]; workflow Encounter_PatientVisit/Referral_Link_Pre_Fill [read]
- Referrals_Main.Partner_ICD_Codes: function diag_referral_dump [read]; function run_import_backfills [read]; workflow Encounter_PatientVisit/Referral_Link_Pre_Fill [read]
- Referrals_Main.X_Ray_Needed: function build_referral_email_html [read]; function compute_data_issues [read]
- Referrals_Main.Patient_Has_Allergies: no references
- Referrals_Main.List_Patient_Allergies: function build_referral_email_html [read]; function run_import_backfills [read]; workflow Encounter_PatientVisit/Referral_Link_Pre_Fill [read]
- Referrals_Main.Patient_Has_Anticoagulants: no references
- Referrals_Main.List_Patient_Anticoagulants: function build_referral_email_html [read]; function run_import_backfills [read]; workflow Encounter_PatientVisit/Referral_Link_Pre_Fill [read]
- Referrals_Main.Patient_Has_Advanced_Directives: function compute_data_issues [read]
- Referrals_Main.Advanced_Directives_Details: function build_referral_email_html [read]; function compute_data_issues [read]; function run_import_backfills [read]; workflow Encounter_PatientVisit/Referral_Link_Pre_Fill [read]
- Referrals_Main.Additional_Information: function diag_referral_dump [read]; function run_import_backfills [read]; workflow Encounter_PatientVisit/Referral_Link_Pre_Fill [read]
- Referrals_Main.General_Files_Upload: function backfill_referral_uploads [read]; function build_creator_attachments [read]; function diag_referral_intake [read]; function diag_upload_field_usage [read]; function diag_upload_field_values [read]
- Referrals_Main.Imaging_Type_Order: function build_imaging_email_html [read]; function build_referral_email_html [read]; function compute_data_issues [read]; function diag_referral_imaging [read]
- Referrals_Main.Imaging_Body_Site: function build_imaging_email_html [read]; function build_referral_email_html [read]; function compute_data_issues [read]; function diag_referral_imaging [read]
- Referrals_Main.Imaging_Order_Indication: function build_imaging_email_html [read]; function build_referral_email_html [read]; function compute_data_issues [read]; function diag_referral_imaging [read]
- Referrals_Main.Imaging_Orders_Upload: function backfill_referral_uploads [read]; function build_creator_attachments [read]; function diag_referral_intake [read]; function diag_upload_field_usage [read]; function diag_upload_field_values [read]
- Referrals_Main.File_Upload_3008: function backfill_referral_uploads [read]; function build_creator_attachments [read]; function diag_referral_intake [read]; function diag_upload_field_usage [read]; function diag_upload_field_values [read]
- Referrals_Main.Partner_Link: function assign_direct_partner [update]; function assign_partner_branch [update]; function audit_month_integrity [read]; function backfill_partner_resolver [read, update]; function backfill_referral_branch [update]; function backfill_referral_partner_fields [read, update]; function dash_metrics [read]; function dash_metrics_range [read]; function diag_referral_branch [read]; function diag_referral_dump [read]; function diag_referral_intake [read]; function process_new_referral [update]; function run_import_backfills [update]; workflow Referrals_Main/Branch_Sets_Partner [set]; workflow Referrals_Main/Referral_Resolves_Partner [set]
- Referrals_Main.Partner_Branch_Link: function assign_direct_partner [read, update]; function assign_partner_branch [update]; function audit_month_integrity [read]; function backfill_partner_resolver [read, update]; function backfill_pvs_billing_branch [read]; function backfill_referral_branch [fetch, read]; function backfill_referral_branch_from_contact [fetch, update]; function backfill_referral_partner_fields [read, update]; function create_3008_pvs_july [read]; function create_3008_pvs_sept [read]; function diag_esi_references [fetch]; function diag_fax_readiness [fetch, read]; function diag_mpu_readiness [read]; function diag_pvs_billing_vs_referral [read]; function diag_pvs_vs_referral [read]; function diag_referral_branch [read]; function diag_referral_contact_match [fetch]; function diag_referral_dump [read]; function diag_referral_intake [read]; function diag_referral_partner_resolve [read]; function diag_safe_test_referrals [read]; function diag_zztest_referrals [read]; function prepare_month_for_billing [read]; function process_new_referral [read, update]; function relink_pvs_to_referral [read]; function resolve_referral_branch_from_text [fetch, update]; function resync_location_labels [read]; function resync_location_names [read]; function run_import_backfills [read, update]; function sos_referral_health [read]; function sync_pvs_branch_from_referral [read]; workflow Encounter_PatientVisit/PVS_Sets_Billing_Branch_O [read]; workflow Encounter_PatientVisit/Referral_Sets_Billing_Bra [read]; workflow Referrals_Main/Branch_Sets_Partner [read, trigger]; workflow Referrals_Main/Branch_Sets_Partner_Link [read]; workflow Referrals_Main/Referral_Resolves_Partner [set]; workflow Referrals_Main/Sender_Sets_Branch [set]
- Referrals_Main.Partner_Organization: function assign_direct_partner [update]; function assign_partner_branch [update]; function audit_month_integrity [read]; function backfill_partner_resolver [read, update]; function backfill_pvs_billing_branch [read]; function backfill_referral_branch [update]; function backfill_referral_partner_fields [read, update]; function backfill_referral_uploads [read]; function build_3008_email_html [read]; function build_imaging_email_html [read]; function build_referral_email_html [read]; function compute_data_issues [read]; function create_3008_pvs_july [read]; function create_3008_pvs_sept [read]; function diag_blank_referral_id [read]; function diag_duplicate_patient_referrals [read]; function diag_missing_dob [read]; function diag_month_billing_gap [read]; function diag_mpu_referral_export [read]; function diag_pvs_vs_referral [read]; function diag_ref_branch_candidates [read]; function diag_ref_patient_pvs_match [read]; function diag_referral_branch [read]; function diag_referral_by_name [read]; function diag_referral_dump [read]; function diag_referral_intake [read]; function diag_referral_partner_resolve [read]; function diag_safe_test_referrals [read]; function diag_unnotified_referrals [read]; function process_new_referral [read, update]; function relink_pvs_to_referral [read]; function run_import_backfills [read, update]; function send_activity_digest [read]; function sos_referral_health [read]; function sync_pvs_from_referral [read]; workflow Assignments/Assignment_Pull_From_Refe1 [read]; workflow Encounter_PatientVisit/PVS_Sets_Billing_Branch_O [read]; workflow Encounter_PatientVisit/Referral_Link_Pre_Fill [read]; workflow Encounter_PatientVisit/Referral_Sets_Billing_Bra [read]; workflow Referrals_Main/Branch_Sets_Partner [set]; workflow Referrals_Main/Referral_Data_Issues_Chec [read]; workflow Referrals_Main/Referral_Resolves_Partner [set]
- Referrals_Main.Partner_Branch: function assign_direct_partner [update]; function assign_partner_branch [update]; function audit_month_integrity [read]; function backfill_partner_resolver [read, update]; function backfill_pvs_billing_branch [read]; function backfill_referral_branch [update]; function backfill_referral_partner_fields [read, update]; function backfill_referral_uploads [read]; function build_3008_email_html [read]; function build_imaging_email_html [read]; function build_referral_email_html [read]; function create_3008_pvs_july [read]; function create_3008_pvs_sept [read]; function diag_3008_no_pvs_sheet [read]; function diag_missing_dob [read]; function diag_month_billing_gap [read]; function diag_pvs_vs_referral [read]; function diag_ref_branch_candidates [read]; function diag_ref_patient_pvs_match [read]; function diag_referral_branch [read]; function diag_referral_by_name [read]; function diag_referral_dump [read]; function diag_referral_intake [read]; function diag_referral_partner_resolve [read]; function diag_safe_test_referrals [read]; function diag_unnotified_referrals [read]; function process_new_referral [update]; function relink_pvs_to_referral [read]; function resolve_referral_branch_from_text [read]; function resync_location_names [update]; function run_import_backfills [read, update]; function sos_referral_health [read]; function sync_pvs_from_referral [read]; workflow Assignments/Assignment_Pull_From_Refe1 [read]; workflow Encounter_PatientVisit/Referral_Link_Pre_Fill [read]; workflow Encounter_PatientVisit/Referral_Sets_Billing_Bra [read]; workflow Referrals_Main/Branch_Sets_Partner [set]; workflow Referrals_Main/Referral_Resolves_Partner [set]
- Referrals_Main.Partner_POC_First_Name: function compute_data_issues [read]; function diag_mpu_referral_export [read]; function process_new_referral [read]; function run_import_backfills [read]; function set_partner_poc_name_title [read]; workflow Encounter_PatientVisit/Referral_Link_Pre_Fill [read]; workflow Referrals_Main/Partner_Contact_Lookup [set]; workflow Referrals_Main/Partner_POC_Name_Title_Ge [read]
- Referrals_Main.Partner_POC_Last_Name: function compute_data_issues [read]; function diag_mpu_referral_export [read]; function process_new_referral [read]; function run_import_backfills [read]; function set_partner_poc_name_title [read]; workflow Encounter_PatientVisit/Referral_Link_Pre_Fill [read]; workflow Referrals_Main/Partner_Contact_Lookup [set]; workflow Referrals_Main/Partner_POC_Name_Title_Ge [read]
- Referrals_Main.Partner_POC_Title: function diag_mpu_referral_export [read]; function process_new_referral [read]; function run_import_backfills [read]; function set_partner_poc_name_title [read]; workflow Encounter_PatientVisit/Referral_Link_Pre_Fill [read]; workflow Referrals_Main/Partner_Contact_Lookup [set]; workflow Referrals_Main/Partner_POC_Name_Title_Ge [read]
- Referrals_Main.Partner_POC_Team: function build_3008_email_html [read]; function build_imaging_email_html [read]; function build_referral_email_html [read]; function create_3008_pvs_july [read]; function create_3008_pvs_sept [read]; function diag_referral_dump [read]; function process_new_referral [read]; function run_import_backfills [read]; workflow Encounter_PatientVisit/Referral_Link_Pre_Fill [read]; workflow Referrals_Main/Partner_Contact_Lookup [set]
- Referrals_Main.Partner_POC_Phone: function build_3008_email_html [read]; function build_imaging_email_html [read]; function build_referral_email_html [read]; function create_3008_pvs_july [read]; function create_3008_pvs_sept [read]; function diag_referral_dump [read]; function process_new_referral [read, update]; function run_import_backfills [read]; workflow Encounter_PatientVisit/Referral_Link_Pre_Fill [read]; workflow Referrals_Main/Partner_Contact_Lookup [set]; workflow Referrals_Main/Referral_Partner_POC_Phon [set, trigger]
- Referrals_Main.Partner_POC_Email: function backfill_partner_resolver [read]; function backfill_referral_branch_from_contact [read]; function build_3008_email_html [read]; function build_imaging_email_html [read]; function build_referral_email_html [read]; function compute_data_issues [read]; function create_3008_pvs_july [read]; function create_3008_pvs_sept [read]; function diag_blank_referral_id [read]; function diag_missing_dob [read]; function diag_ref_branch_candidates [read]; function diag_referral_branch [read]; function diag_referral_contact_match [read]; function diag_referral_dump [read]; function diag_referral_partner_resolve [read]; function diag_unnotified_referrals [read]; function process_new_referral [read]; function run_import_backfills [read]; function send_referral_confirmation [read]; function sos_referral_health [read]; workflow Encounter_PatientVisit/PVS_Sets_Billing_Branch_O [read]; workflow Encounter_PatientVisit/Referral_Link_Pre_Fill [read]; workflow Referrals_Main/Partner_Contact_Lookup [read, trigger]; workflow Referrals_Main/Referral_Resolves_Partner [read]; workflow Referrals_Main/Sender_Sets_Branch [read, trigger]
- Referrals_Main.Files_3008_URLs: function backfill_referral_uploads [fetch, read]; function build_zepto_attachments [read]; function compute_data_issues [read]; function diag_referral_intake [read]; function diag_upload_probe [read]; function process_new_referral [read]
- Referrals_Main.General_Files_URLs: function backfill_referral_uploads [fetch, read]; function build_zepto_attachments [read]; function diag_referral_intake [read]; function process_new_referral [read]
- Referrals_Main.Imaging_Orders_URLs: function backfill_referral_uploads [fetch, read]; function build_zepto_attachments [read]; function compute_data_issues [read]; function diag_referral_imaging [read]; function diag_referral_intake [read]; function process_new_referral [read]
- Referrals_Main.Data_Issues: function backfill_data_issues [read, update]; function diag_referral_dump [read]; function flag_duplicate_referrals [read, update]; function run_import_backfills [update]; workflow Referrals_Main/Referral_Data_Issues_Chec [update]; workflow Referrals_Main/Referral_Data_Issues_Sync [read, update]
- Referrals_Main.Referral_ID: function assign_direct_partner [fetch]; function assign_partner_branch [fetch]; function audit_month_integrity [read]; function backfill_data_issues [read]; function backfill_mint_missing_referral_ids [fetch, read]; function backfill_partner_resolver [read]; function backfill_patient_dob [read]; function backfill_pvs_billing_branch [read]; function backfill_pvs_referral_id_from_link [read]; function backfill_referral_date [read]; function backfill_referral_employee_link [read]; function backfill_referral_id_from_token [read, update]; function backfill_referral_ids [read]; function backfill_referral_partner_fields [read]; function backfill_referral_uploads [fetch, read]; function build_3008_email_html [read]; function build_imaging_email_html [read]; function build_referral_confirmation_html [read]; function build_referral_email_html [read]; function create_3008_pvs_july [fetch]; function create_3008_pvs_sept [fetch]; function dash_metrics [read]; function dash_metrics_range [read]; function diag_3008_link_check [read]; function diag_3008_no_pvs_list [read]; function diag_3008_no_pvs_sheet [read]; function diag_3008_overdue [read]; function diag_blank_referral_id [read]; function diag_compliance_gap [read]; function diag_dob_coverage [read]; function diag_duplicate_patient_referrals [read]; function diag_duplicate_referral_ids [read]; function diag_fax_readiness [read]; function diag_find_referral [fetch, read]; function diag_imaging_notify_check [read]; function diag_import_ref_matches [fetch, read]; function diag_invoice_patient_gaps [read]; function diag_map_cognito_refs [read]; function diag_match_3008_refs [read]; function diag_missing_dob [read]; function diag_month_billing_gap [read]; function diag_mpu_3008_export [read]; function diag_mpu_readiness [read]; function diag_mpu_referral_export [read]; function diag_orphan_referral [read]; function diag_pvs_billing_vs_referral [read]; function diag_pvs_for_refs [fetch]; function diag_pvs_names [read]; function diag_pvs_referral_match [fetch, read]; function diag_pvs_vs_referral [read]; function diag_ref_branch_candidates [fetch]; function diag_ref_names [fetch]; function diag_ref_patient_pvs_match [fetch, read]; function diag_referral_branch [fetch, read]; function diag_referral_by_name [read]; function diag_referral_collision [fetch, read]; function diag_referral_date_source [fetch]; function diag_referral_dates [read]; function diag_referral_dump [fetch]; function diag_referral_id_records [fetch]; function diag_referral_ids [read]; function diag_referral_imaging [fetch]; function diag_referral_intake [fetch, read]; function diag_referral_origin [read]; function diag_referral_partner_resolve [fetch]; function diag_referrals_missing_pvs [read]; function diag_room_number_gaps [read]; function diag_safe_test_referrals [read]; function diag_sequence_trackers [read]; function diag_unmatched_branch_labels [read]; function diag_unnotified_referrals [read]; function diag_upload_field_usage [read]; function diag_upload_field_values [fetch, read]; function diag_upload_probe [fetch, read]; function diag_zztest_referrals [read]; function flag_duplicate_referrals [fetch]; function link_pvs_to_referral [fetch]; function mint_referral_id [fetch, read, update]; function prepare_month_for_billing [fetch]; function process_new_referral [fetch, read]; function relink_pvs_to_referral [fetch]; function repair_invoice_pvs_from_referral [fetch, read]; function resend_referral_notifications [fetch]; function resync_patient_dob [read]; function run_import_backfills [fetch, read]; function run_pvs_exclusion_monitor [fetch, read]; function send_3008_notification [fetch]; function send_activity_digest [read]; function send_assignment_notification [read]; function send_imaging_notification [fetch, read]; function send_referral_confirmation [fetch, read]; function send_referral_notification [fetch, read]; function set_pvs_referral_link [fetch, read]; function sos_referral_health [read]; function sweep_unnotified_referrals [fetch, read]; function sync_pvs_branch_from_referral [read]; function sync_pvs_from_referral [read]; function widget_today_visits [read]; page Drilldown_Data [read]; workflow Encounter_PatientVisit/Referral_Link_Pre_Fill [read]; workflow PVS_Fax_Review/PVS_Fax_Review_On_Load [read]; workflow Referrals_Main/Referral_Data_Issues_Chec [read]
- Referrals_Main.Referral_Date: function audit_month_integrity [read]; function backfill_pvs_referral_date [read]; function backfill_pvs_system_fields_range [read]; function backfill_referral_date [fetch, update]; function build_3008_email_html [read]; function build_console_docs [read]; function build_imaging_email_html [read]; function build_pvs_fax_html [read]; function build_referral_confirmation_html [read]; function build_referral_email_html [read]; function create_invoice_from_selection [read]; function dash_metrics [fetch, read]; function dash_metrics_range [fetch, read]; function diag_3008_link_check [read]; function diag_3008_no_pvs_list [fetch, read]; function diag_3008_no_pvs_sheet [read]; function diag_3008_overdue [fetch]; function diag_august_pvs_gap [read]; function diag_blank_referral_id [read]; function diag_compliance_gap [read]; function diag_duplicate_patient_referrals [fetch, read]; function diag_duplicate_referral_ids [read]; function diag_find_referral [read]; function diag_imaging_notify_check [read]; function diag_import_ref_matches [read]; function diag_map_cognito_refs [read]; function diag_match_3008_refs [read]; function diag_month_billing_gap [read]; function diag_mpu_3008_export [fetch, read]; function diag_mpu_readiness [fetch]; function diag_mpu_referral_export [fetch, read]; function diag_pvs_referral_match [read]; function diag_ref_patient_pvs_match [read]; function diag_referral_by_name [read]; function diag_referral_collision [fetch]; function diag_referral_date_source [read]; function diag_referral_dates [read]; function diag_referral_dump [read]; function diag_referral_id_records [read]; function diag_referral_imaging [read]; function diag_referral_origin [read]; function diag_referrals_missing_pvs [fetch, read]; function diag_safe_test_referrals [fetch, read]; function diag_unnotified_referrals [fetch]; function process_new_referral [read, update]; function run_import_backfills [read]; function send_activity_digest [fetch, read]; function sos_referral_health [read]; function sweep_unnotified_referrals [fetch]; function sync_pvs_from_referral [read]; function widget_today_visits [fetch, read]; page Drilldown_Data [read]; workflow Assignments/Assignment_Pull_From_Refe1 [read]; workflow Encounter_PatientVisit/Fax_This_Note_Preview_And [read]; workflow Encounter_PatientVisit/PVS_System_Fields_Stamp_O [read]; workflow Encounter_PatientVisit/Referral_Link_Pre_Fill [read]
- Referrals_Main.Referral_Date1: function diag_referral_date_source [read]
- Referrals_Main.Referral_ID_Stamp: function backfill_referral_id_stamp [read, update]; function diag_referral_by_name [read]; function diag_referral_collision [read]; function diag_referral_ids [read]; function mint_referral_id [update]; function run_import_backfills [fetch, read, update]; function sos_referral_health [read]; workflow Encounter_PatientVisit/Referral_Link_Pre_Fill [read]
- Referrals_Main.Patient_Full_Name: function audit_month_integrity [read]; function backfill_patient_full_names [read]; function build_3008_email_html [read]; function build_imaging_email_html [read]; function build_referral_confirmation_html [read]; function build_referral_email_html [read]; function create_3008_pvs_july [read]; function create_3008_pvs_sept [read]; function dash_metrics [read]; function dash_metrics_range [read]; function diag_3008_no_pvs_sheet [read]; function diag_blank_referral_id [read]; function diag_invoice_patient_gaps [read]; function diag_pvs_vs_referral [read]; function diag_referral_branch [read]; function diag_referral_by_name [read]; function diag_referral_dump [read]; function process_new_referral [update]; function relink_pvs_to_referral [read]; function repair_invoice_pvs_from_referral [read]; function run_import_backfills [read, update]; function send_activity_digest [read]; function set_patient_full_name [update]; page Drilldown_Data [read]; workflow Encounter_PatientVisit/Referral_Link_Pre_Fill [read]; workflow Imaging_Orders/Imaging_Referral_Link_Pre [read]; workflow Referrals_Main/Patient_Full_Name_Generat [set]
- Referrals_Main.AC_Full_Name: function backfill_dm_full_names [fetch, update]; function build_3008_email_html [read]; function build_imaging_email_html [read]; function build_referral_email_html [read]; function diag_referral_dump [read]; function process_new_referral [update]; workflow Imaging_Orders/Imaging_Referral_Link_Pre [read]; workflow Referrals_Main/DM_Full_Name_Generator [set]
- Referrals_Main.Partner_POC_Name_Title: function backfill_partner_poc_name_title [read]; function build_3008_email_html [read]; function build_imaging_email_html [read]; function build_referral_confirmation_html [read]; function build_referral_email_html [read]; function create_3008_pvs_july [read]; function create_3008_pvs_sept [read]; function diag_referral_dump [read]; function process_new_referral [update]; function set_partner_poc_name_title [update]; workflow Assignments/Assignment_Pull_From_Refe1 [read]; workflow Referrals_Main/Partner_POC_Name_Title_Ge [set]
- Referrals_Main.Partner_ID: function assign_direct_partner [update]; function assign_partner_branch [update]; function audit_month_integrity [read]; function backfill_partner_resolver [read, update]; function backfill_referral_branch [update]; function backfill_referral_partner_fields [read, update]; function create_3008_pvs_july [read]; function create_3008_pvs_sept [read]; function diag_pvs_vs_referral [read]; function diag_referral_branch [read]; function diag_referral_dump [read]; function diag_referral_intake [read]; function process_new_referral [update]; function run_import_backfills [read, update]; function sync_pvs_from_referral [read]; workflow Encounter_PatientVisit/Referral_Link_Pre_Fill [read]; workflow Referrals_Main/Branch_Sets_Partner [set]; workflow Referrals_Main/Branch_Sets_Partner_Link [set]; workflow Referrals_Main/Referral_Resolves_Partner [set]
- Referrals_Main.Partner_ID_Stamp: function assign_direct_partner [update]; function assign_partner_branch [update]; function backfill_partner_resolver [read, update]; function backfill_referral_partner_fields [update]; function process_new_referral [update]; function run_import_backfills [read, update]; workflow Encounter_PatientVisit/Referral_Link_Pre_Fill [read]; workflow Referrals_Main/Referral_Resolves_Partner [set]
- Referrals_Main.Partner_Location_Label: function assign_direct_partner [update]; function assign_partner_branch [update]; function audit_month_integrity [read]; function backfill_partner_resolver [read, update]; function backfill_referral_branch [update]; function backfill_referral_partner_fields [read, update]; function compute_data_issues [read]; function create_3008_pvs_july [read]; function create_3008_pvs_sept [read]; function diag_3008_no_pvs_sheet [read]; function diag_map_cognito_refs [read]; function diag_mpu_3008_export [read]; function diag_mpu_referral_export [read]; function diag_orphan_referral [read]; function diag_pvs_billing_vs_referral [read]; function diag_pvs_referral_match [read]; function diag_pvs_vs_referral [read]; function diag_referral_branch [read]; function diag_referral_collision [read]; function diag_referral_dump [read]; function diag_referral_id_records [read]; function diag_referral_intake [read]; function diag_referral_partner_resolve [read]; function diag_referrals_missing_pvs [read]; function diag_unmatched_branch_labels [read]; function process_new_referral [read, update]; function resync_location_labels [update]; function run_import_backfills [read, update]; function sync_pvs_from_referral [read]; page Drilldown_Data [read]; workflow Encounter_PatientVisit/PVS_Sets_Billing_Branch_O [read]; workflow Encounter_PatientVisit/Referral_Link_Pre_Fill [read]; workflow Encounter_PatientVisit/Referral_Sets_Billing_Bra [read]; workflow Referrals_Main/Branch_Sets_Partner [set]; workflow Referrals_Main/Referral_Resolves_Partner [set]
- Referrals_Main.Referral_Added_Time: function audit_month_integrity [read]; function backfill_referral_added_time [fetch, update]; function backfill_referral_date [read]; function diag_3008_link_check [read]; function diag_3008_no_pvs_sheet [read]; function diag_blank_referral_id [read]; function diag_compliance_gap [read]; function diag_month_billing_gap [read]; function diag_mpu_referral_export [read]; function diag_referral_date_source [read]; function diag_referral_dump [read]
- Referrals_Main.Form_Token: function backfill_referral_id_from_token [read, update]; function diag_blank_referral_id [read]; function diag_imaging_notify_check [read]; function diag_referral_collision [read]; function diag_referral_dump [read]; function diag_referral_ids [read]; function diag_referral_imaging [read]; function diag_referral_origin [read]; function process_new_referral [read]
- Referrals_Main.Assignment_Status: function diag_3008_no_pvs_list [read]; function diag_compliance_gap [read]; function diag_month_billing_gap [read]; function diag_ref_patient_pvs_match [read]; function diag_referrals_missing_pvs [read]
- Referrals_Main.Employee_Link: function audit_month_integrity [read]; function backfill_referral_employee_link [read, update]; function diag_ref_patient_pvs_match [read]; workflow Assignments/Assignment_Referral_Emplo [update]
- Referrals_Main.Cognito_Referral_ID: function backfill_pvs_link_by_cognito [fetch]; function diag_3008_no_pvs_list [read]; function diag_blank_referral_id [read]; function diag_duplicate_patient_referrals [read]; function diag_import_ref_matches [fetch, read]; function diag_map_cognito_refs [read]; function diag_mpu_3008_export [read]; function diag_mpu_referral_export [read]; function diag_referral_date_source [read]; function diag_referral_dump [read]; function diag_referral_origin [read]; function run_import_backfills [fetch, read]
- Referrals_Main.Partner_Branch_Submitted: function diag_ref_branch_candidates [read]; function diag_referral_branch [read]; function diag_referral_dump [read]; function diag_referral_partner_resolve [read]; function diag_unmatched_branch_labels [read]; function process_new_referral [read, update]; workflow Referrals_Main/Referral_Resolves_Partner [set]
- Referrals_Main.Notified_Time: function diag_imaging_notify_check [read]; function diag_referral_date_source [read]; function diag_referral_dump [read]; function diag_referral_imaging [read]; function process_new_referral [read, update]
