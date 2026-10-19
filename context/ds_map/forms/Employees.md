# Employees

- Display name: -
- .ds line: 578
- Fields (excluding sections): 31
- Parent form: -

## Fields

| Link name | Display name | Type | Lookup target |
|---|---|---|---|
| Employee_Identity_Section | Employee Identity Section | section | - |
| Employee_First_Name | Employee First Name | text | - |
| Employee_Last_Name | Employee Last Name | text | - |
| Employee_Title | Employee Title | picklist | - |
| Employee_SSN | Employee SSN | text | - |
| Employee_Email | Employee Email | email | - |
| Employee_Portal_Email | Portal Email | email | - |
| Employee_Address_Contact | Employee Address & Contact | section | - |
| Employee_Phone | Employee Phone | text | - |
| Employee_Address | Employee Address | address | - |
| Emergency_Contact_Details | Emergency Contact Details | section | - |
| Emergency_Contact_Name | Emergency Contact Name | text | - |
| Emergency_Contact_Phone | Emergency Contact Phone | phonenumber | - |
| Employee_Notifications_Section | Employee Notifications Section | section | - |
| Email_Notification_Types | Email Notification Types | list | - |
| Portal_Access_Types | Portal Access Types | list | - |
| Employment_Details_Section | Employment Details Section | section | - |
| Employee_Status | Employee Status | radiobuttons | - |
| Employee_Job_Title | Job Title | picklist | - |
| Employee_Start_Date | Employee Start Date | date | - |
| Employee_Term_Date | Employee Term Date | date | - |
| Employee_Term_Reason | Employee Term Reason | picklist | - |
| Compensation_Section | Compensation Section | section | - |
| Pay_Type | Pay Type | picklist | - |
| Pay_Rate | Pay Rate | USD | - |
| Employment_Type | Employment Type | picklist | - |
| License_Information | License Information Section | section | - |
| License_Type | License Type  | picklist | - |
| License_Number | License Number  | text | - |
| License_State | License State | picklist | - |
| License_Issued_Date | License Issued Date | date | - |
| License_Expiration_Date | License Expiration Date | date | - |
| Provider_NPI | Provider NPI | text | - |
| License_File_Upload | License File Upload | upload file | - |
| System_Fields_Section | System Fields Section | section | - |
| Employee_ID | Employee ID | text | - |
| Employee_ID_Stamp | Employee ID Stamp | text | - |
| Employee_Initials | Employee Initials | text | - |
| Employee_Name_Title | Employee Name & Title | text | - |

## Workflows

### Employee_ID_Generator

- Display: Employee ID Generator
- Record event: on add
- Form event: OnSuccess
- Status: ENABLED
- .ds line: 36177
- Fields read: ID
- Fields set: -
- Fields shown/hidden/enabled/disabled: -
- Functions called: mint_employee_id
- Other forms: -

### Employee_Initials_Generat

- Display: Employee Initials Generator
- Record event: on add or edit
- Form event: OnSuccess
- Status: ENABLED
- .ds line: 38999
- Fields read: Employee_First_Name, Employee_Last_Name
- Fields set: Employee_Initials
- Fields shown/hidden/enabled/disabled: -
- Functions called: -
- Other forms: -

### Employee_Name_Title_Gener1

- Display: Employee Name & Title Generator
- Record event: on add or edit
- Form event: OnSuccess
- Status: ENABLED
- .ds line: 36111
- Fields read: Employee_First_Name, Employee_Last_Name, Employee_Title
- Fields set: Employee_Name_Title
- Fields shown/hidden/enabled/disabled: -
- Functions called: -
- Other forms: -

### Employee_Phone_Format

- Display: Employee Phone Format
- Record event: on add or edit
- Form event: OnUserInput of Employee_Phone
- Status: ENABLED
- .ds line: 37689
- Fields read: -
- Fields set: Employee_Phone
- Fields shown/hidden/enabled/disabled: -
- Functions called: -
- Other forms: -

### Portal_Access_By_Status

- Display: Portal Access By Status
- Record event: on add or edit
- Form event: OnSuccess
- Status: ENABLED
- .ds line: 37636
- Fields read: Employee_Email, Employee_Portal_Email, Employee_Status, Portal_Access_Types
- Fields set: -
- Fields shown/hidden/enabled/disabled: -
- Functions called: -
- Other forms: -

### Show_Hide_Employee_Term_D

- Display: Show/Hide Employee Term Date
- Record event: on add or edit
- Form event: OnUserInput of Employee_Status
- Status: ENABLED
- .ds line: 36151
- Fields read: Employee_Status
- Fields set: -
- Fields shown/hidden/enabled/disabled: Employee_Term_Date
- Functions called: -
- Other forms: -

### Validate_Employee_Phone_B

- Display: Validate Employee Phone Block
- Record event: on add or edit
- Form event: OnValidate
- Status: ENABLED
- .ds line: 37723
- Fields read: Employee_Phone
- Fields set: -
- Fields shown/hidden/enabled/disabled: -
- Functions called: -
- Other forms: -

## Reverse index

Every item that references a field of this form.

- Employees.Employee_First_Name: function backfill_employee_initials [read]; function backfill_employee_name_title [read]; function backfill_pvs_employee_email [read]; function backfill_pvs_employee_link_range [read]; function backfill_pvs_provider_identity [read]; function create_3008_pvs_july [fetch, read]; function create_3008_pvs_sept [fetch, read]; function dash_metrics [read]; function dash_metrics_range [read]; function diag_employees [read]; function diag_imaging_notify_check [read]; function run_import_backfills [read]; function send_assignment_notification [read]; function set_pvs_provider [read]; function widget_today_visits [read]; workflow Employees/Employee_Initials_Generat [read]; workflow Employees/Employee_Name_Title_Gener1 [read]; workflow Encounter_PatientVisit/Pre_fills_provider_sectio [read]
- Employees.Employee_Last_Name: function backfill_employee_initials [read]; function backfill_employee_name_title [read]; function backfill_pvs_employee_email [read]; function backfill_pvs_employee_link_range [read]; function backfill_pvs_provider_identity [read]; function create_3008_pvs_july [fetch, read]; function create_3008_pvs_sept [fetch, read]; function dash_metrics [read]; function dash_metrics_range [read]; function diag_employees [read]; function diag_imaging_notify_check [read]; function run_import_backfills [read]; function set_pvs_provider [read]; function widget_today_visits [read]; workflow Employees/Employee_Initials_Generat [read]; workflow Employees/Employee_Name_Title_Gener1 [read]; workflow Encounter_PatientVisit/Pre_fills_provider_sectio [read]
- Employees.Employee_Title: function backfill_employee_name_title [read]; function backfill_pvs_employee_email [read]; function backfill_pvs_provider_identity [read]; function create_3008_pvs_july [read]; function create_3008_pvs_sept [read]; function run_import_backfills [read]; function set_pvs_provider [read]; workflow Employees/Employee_Name_Title_Gener1 [read]; workflow Encounter_PatientVisit/Pre_fills_provider_sectio [read]
- Employees.Employee_SSN: no references
- Employees.Employee_Email: function api_fax_begin [fetch]; function backfill_provider_login_email [read]; function backfill_pvs_employee_email [read]; function backfill_pvs_employee_initials [read]; function backfill_pvs_employee_link [read]; function backfill_pvs_employee_link_range [read]; function backfill_pvs_provider_identity [read]; function create_3008_pvs_july [read]; function create_3008_pvs_sept [read]; function diag_imaging_notify_check [read]; function diag_provider_backfill_trace [read]; function diag_pvs_login_email_gaps [read]; function get_notification_recipients [read]; function is_portal_admin [read]; function run_import_backfills [read]; function send_assignment_notification [read]; function set_pvs_provider [read]; workflow Employees/Portal_Access_By_Status [read]; workflow Encounter_PatientVisit/PVS_System_Fields_Stamp_O [read]; workflow Encounter_PatientVisit/Pre_fills_provider_sectio [fetch, read]; workflow Encounter_PatientVisit/Provider_Identity_Stamp [fetch, read]; workflow Encounter_PatientVisit/Provider_Login_Stamp_On_S [fetch, read]; workflow Imaging_Orders/Imaging_Order_Provider_Ga [fetch]; workflow Imaging_Orders/Imaging_Order_Provider_St [fetch]
- Employees.Employee_Portal_Email: function backfill_provider_login_email [read]; function backfill_pvs_employee_link [read]; function backfill_pvs_employee_link_range [read]; function diag_pvs_login_email_gaps [read]; function is_portal_admin [read]; function run_import_backfills [read]; function send_pvs_fax [fetch]; function set_pvs_provider [read]; workflow Employees/Portal_Access_By_Status [read]; workflow Encounter_PatientVisit/PVS_System_Fields_Stamp_O [read]; workflow Encounter_PatientVisit/Pre_fills_provider_sectio [fetch]; workflow Encounter_PatientVisit/Provider_Identity_Stamp [fetch, read]; workflow Encounter_PatientVisit/Provider_Login_Stamp_On_S [fetch, read]; workflow Imaging_Orders/Imaging_Order_Provider_St [fetch]
- Employees.Employee_Phone: function backfill_employee_phone_format [read, update]; workflow Employees/Employee_Phone_Format [set, trigger]; workflow Employees/Validate_Employee_Phone_B [read]; workflow Imaging_Orders/Imaging_Order_Provider_St [read]
- Employees.Employee_Address: no references
- Employees.Emergency_Contact_Name: no references
- Employees.Emergency_Contact_Phone: no references
- Employees.Email_Notification_Types: function diag_imaging_notify_check [read]; function get_notification_recipients [read]
- Employees.Portal_Access_Types: function is_portal_admin [read]; function widget_today_visits [read]; workflow Employees/Portal_Access_By_Status [read]
- Employees.Employee_Status: function create_3008_pvs_july [fetch]; function create_3008_pvs_sept [fetch]; function diag_employees [read]; function diag_imaging_notify_check [read]; function diag_pvs_login_email_gaps [read]; function get_notification_recipients [fetch]; function is_portal_admin [fetch]; function widget_today_visits [fetch]; workflow Employees/Portal_Access_By_Status [read]; workflow Employees/Show_Hide_Employee_Term_D [read, trigger]; workflow Imaging_Orders/Imaging_Order_Provider_Ga [fetch]
- Employees.Employee_Job_Title: function widget_today_visits [read]
- Employees.Employee_Start_Date: no references
- Employees.Employee_Term_Date: workflow Employees/Show_Hide_Employee_Term_D [show/hide]
- Employees.Employee_Term_Reason: no references
- Employees.Pay_Type: no references
- Employees.Pay_Rate: no references
- Employees.Employment_Type: no references
- Employees.License_Type: no references
- Employees.License_Number: no references
- Employees.License_State: no references
- Employees.License_Issued_Date: no references
- Employees.License_Expiration_Date: no references
- Employees.Provider_NPI: workflow Imaging_Orders/Imaging_Order_Provider_St [read]
- Employees.License_File_Upload: no references
- Employees.Employee_ID: function backfill_employee_ids [read]; function backfill_employee_name_title [read]; function diag_sequence_trackers [read]; function mint_employee_id [read, update]; function send_assignment_notification [fetch, read]
- Employees.Employee_ID_Stamp: function mint_employee_id [update]
- Employees.Employee_Initials: function backfill_employee_initials [fetch, update]; function backfill_pvs_employee_email [read]; function backfill_pvs_employee_initials [read]; function backfill_pvs_employee_link_range [read]; function backfill_pvs_provider_identity [read]; function create_3008_pvs_july [read]; function create_3008_pvs_sept [read]; function diag_employees [read]; function diag_provider_backfill_trace [read]; function run_import_backfills [read]; function set_pvs_provider [read]; workflow Employees/Employee_Initials_Generat [set]; workflow Encounter_PatientVisit/Pre_fills_provider_sectio [read]
- Employees.Employee_Name_Title: function backfill_employee_name_title [read, update]; function backfill_pvs_employee_email [read]; function backfill_pvs_employee_link [read]; function backfill_pvs_employee_link_range [read]; function backfill_pvs_provider_identity [read]; function backfill_referral_employee_link [read]; function create_3008_pvs_july [read]; function create_3008_pvs_sept [read]; function diag_provider_backfill_trace [read]; function diag_pvs_provider_fields [read]; function run_import_backfills [read]; function send_fax_digest [read]; function set_pvs_provider [read]; workflow Assignments/Assignment_Change_Log [read]; workflow Employees/Employee_Name_Title_Gener1 [set]
