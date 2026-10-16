# Assignments

- Display name: -
- .ds line: 111
- Fields (excluding sections): 19
- Parent form: -

## Fields

| Link name | Display name | Type | Lookup target |
|---|---|---|---|
| Referral_Details_Section | Referral Details Section | section | - |
| Referral_Link | Referral Link | picklist | Referrals_Main |
| Referral_Date | Referral Date | text | - |
| Referral_Partner | Referral Partner | text | - |
| Referral_POC | Referral POC | text | - |
| Patient_Details_Section | Patient Details Section | section | - |
| Patient_First_Name | Patient First Name | text | - |
| Patient_Last_Name | Patient Last Name | text | - |
| Patient_DOB | Patient DOB | text | - |
| Patient_Phone | Patient Phone | text | - |
| Patient_Location | Patient Location | radiobuttons | - |
| Facility_Name | Facility Name | text | - |
| Patient_Address | Patient Address | address | - |
| Facility_Phone | Facility Phone | text | - |
| Facility_Room_Number | Facility Room Number | text | - |
| Employee_Details | Assigned Provider | section | - |
| Employee_Link | Employee Link | picklist | Employees |
| Assignment_Details | Assignment Details | section | - |
| Assignment_Notes | Assignment Notes | textarea | - |
| Visit_Status_Section | Visit Status Section | section | - |
| Visit_Status | Status | picklist | - |
| System_Fields_Section | System Fields Section | section | - |
| Assignment_ID | Assignment ID | text | - |
| Assignment_ID_Stamp | Assignment ID Stamp | text | - |
| Notified_Employee_ID | Notified Employee ID | text | - |

## Workflows

### Assignment_Change_Log

- Display: Assignment Change Log
- Record event: on edit
- Form event: OnValidate
- Status: ENABLED
- .ds line: 32309
- Fields read: Assignment_ID, Assignment_Notes, Employee_Link, Facility_Name, Facility_Phone, Facility_Room_Number, ID, Patient_Address, Patient_Location
- Fields set: -
- Fields shown/hidden/enabled/disabled: -
- Functions called: log_change
- Other forms: fetch Assignments (ID); fetch Employees (ID); read Assignments (Assignment_Notes, Employee_Link, Facility_Name, Facility_Phone, Facility_Room_Number, Patient_Address, Patient_Location); read Employees (Employee_Name_Title)

### Assignment_ID_Generator

- Display: Assignment ID Generator
- Record event: on add
- Form event: OnSuccess
- Status: ENABLED
- .ds line: 32290
- Fields read: ID
- Fields set: -
- Fields shown/hidden/enabled/disabled: -
- Functions called: mint_assignment_id
- Other forms: -

### Assignment_Lock_Immutable

- Display: Assignment Lock Immutable Fields
- Record event: on add or edit
- Form event: OnLoad
- Status: ENABLED
- .ds line: 32370
- Fields read: -
- Fields set: -
- Fields shown/hidden/enabled/disabled: Patient_DOB, Patient_First_Name, Patient_Last_Name
- Functions called: -
- Other forms: -

### Assignment_Notify_Provide

- Display: Assignment Notify Provider
- Record event: on add or edit
- Form event: OnSuccess
- Status: ENABLED
- .ds line: 36596
- Fields read: ID
- Fields set: -
- Fields shown/hidden/enabled/disabled: -
- Functions called: is_portal_admin, send_assignment_notification
- Other forms: -

### Assignment_Pull_From_Refe1

- Display: Assignment_Pull_From_Referral
- Record event: on add or edit
- Form event: OnUserInput of Referral_Link
- Status: ENABLED
- .ds line: 35181
- Fields read: Referral_Link
- Fields set: Facility_Name, Facility_Phone, Facility_Room_Number, Patient_Address, Patient_DOB, Patient_First_Name, Patient_Last_Name, Patient_Location, Patient_Phone, Referral_Date, Referral_POC, Referral_Partner
- Fields shown/hidden/enabled/disabled: -
- Functions called: -
- Other forms: fetch Referrals_Main (ID); read Referrals_Main (Facility_Name, Facility_Phone, Facility_Room_Number, Partner_Branch, Partner_Organization, Partner_POC_Name_Title, Patient_Address, Patient_DOB, Patient_First_Name, Patient_Last_Name, Patient_Location, Patient_Phone, Referral_Date)

### Assignment_Referral_Emplo

- Display: Assignment Referral Employee
- Record event: on add or edit
- Form event: OnSuccess
- Status: ENABLED
- .ds line: 35562
- Fields read: Employee_Link, Referral_Link
- Fields set: -
- Fields shown/hidden/enabled/disabled: -
- Functions called: -
- Other forms: fetch Referrals_Main (ID); update Referrals_Main (Employee_Link)

### Assignment_Required_Refer

- Display: Assignment Required Referral
- Record event: on add or edit
- Form event: OnValidate
- Status: ENABLED
- .ds line: 32391
- Fields read: Employee_Link, ID, Referral_Link
- Fields set: -
- Fields shown/hidden/enabled/disabled: -
- Functions called: -
- Other forms: fetch Assignments (ID)

### Assignment_Status_From_Pr

- Display: Assignment Status From Provider
- Record event: on add or edit
- Form event: OnValidate
- Status: ENABLED
- .ds line: 36620
- Fields read: Employee_Link
- Fields set: -
- Fields shown/hidden/enabled/disabled: -
- Functions called: -
- Other forms: -

### Assignment_Visit_Status_C

- Display: Assignment_Visit_Status_Choices
- Record event: on edit
- Form event: OnLoad
- Status: ENABLED
- .ds line: 35247
- Fields read: Referral_Link
- Fields set: Visit_Status
- Fields shown/hidden/enabled/disabled: -
- Functions called: -
- Other forms: fetch Referrals_Main (ID); read Referrals_Main (Referral_Type)

### Show_Hide_Facility_Name_P

- Display: Show/Hide Facility Name, Phone, Room
- Record event: on add or edit
- Form event: OnLoad
- Status: ENABLED
- .ds line: 32515
- Fields read: Patient_Location
- Fields set: -
- Fields shown/hidden/enabled/disabled: Facility_Name, Facility_Phone, Facility_Room_Number
- Functions called: -
- Other forms: -

### Show_Hide_Facility_Name_P1

- Display: Show/Hide Facility Name, Phone, Room
- Record event: on add or edit
- Form event: OnUserInput of Patient_Location
- Status: ENABLED
- .ds line: 32545
- Fields read: Patient_Location
- Fields set: -
- Fields shown/hidden/enabled/disabled: Facility_Name, Facility_Phone, Facility_Room_Number
- Functions called: -
- Other forms: -

## Reverse index

Every item that references a field of this form.

- Assignments.Referral_Link: function backfill_referral_employee_link [fetch, read]; function dash_metrics [fetch, read]; function dash_metrics_range [fetch, read]; function diag_orphan_referral [fetch]; function diag_orphaned_records [read]; function diag_safe_test_referrals [fetch]; function diag_unnotified_referrals [fetch]; function process_new_referral [fetch, insert]; function send_assignment_notification [read]; function sos_referral_health [read]; function widget_today_visits [fetch, read]; workflow Assignments/Assignment_Pull_From_Refe1 [read, trigger]; workflow Assignments/Assignment_Referral_Emplo [read]; workflow Assignments/Assignment_Required_Refer [read]; workflow Assignments/Assignment_Visit_Status_C [read]
- Assignments.Referral_Date: page Drilldown_Data [read]; workflow Assignments/Assignment_Pull_From_Refe1 [set]
- Assignments.Referral_Partner: page Drilldown_Data [read]; workflow Assignments/Assignment_Pull_From_Refe1 [set]
- Assignments.Referral_POC: workflow Assignments/Assignment_Pull_From_Refe1 [set]
- Assignments.Patient_First_Name: function dash_metrics [read]; function dash_metrics_range [read]; function diag_orphaned_records [read]; function process_new_referral [insert]; function send_assignment_notification [read]; function widget_today_visits [read]; page Drilldown_Data [read]; workflow Assignments/Assignment_Lock_Immutable [show/hide]; workflow Assignments/Assignment_Pull_From_Refe1 [set]
- Assignments.Patient_Last_Name: function dash_metrics [read]; function dash_metrics_range [read]; function diag_orphaned_records [read]; function process_new_referral [insert]; function send_assignment_notification [read]; function widget_today_visits [read]; page Drilldown_Data [read]; workflow Assignments/Assignment_Lock_Immutable [show/hide]; workflow Assignments/Assignment_Pull_From_Refe1 [set]
- Assignments.Patient_DOB: function process_new_referral [insert]; workflow Assignments/Assignment_Lock_Immutable [show/hide]; workflow Assignments/Assignment_Pull_From_Refe1 [set]
- Assignments.Patient_Phone: function process_new_referral [insert]; workflow Assignments/Assignment_Pull_From_Refe1 [set]
- Assignments.Patient_Location: function process_new_referral [insert]; workflow Assignments/Assignment_Change_Log [read]; workflow Assignments/Assignment_Pull_From_Refe1 [set]; workflow Assignments/Show_Hide_Facility_Name_P [read]; workflow Assignments/Show_Hide_Facility_Name_P1 [read, trigger]
- Assignments.Facility_Name: function process_new_referral [insert]; workflow Assignments/Assignment_Change_Log [read]; workflow Assignments/Assignment_Pull_From_Refe1 [set]; workflow Assignments/Show_Hide_Facility_Name_P [show/hide]; workflow Assignments/Show_Hide_Facility_Name_P1 [show/hide]
- Assignments.Patient_Address: function process_new_referral [insert]; workflow Assignments/Assignment_Change_Log [read]; workflow Assignments/Assignment_Pull_From_Refe1 [set]
- Assignments.Facility_Phone: function process_new_referral [insert]; workflow Assignments/Assignment_Change_Log [read]; workflow Assignments/Assignment_Pull_From_Refe1 [set]; workflow Assignments/Show_Hide_Facility_Name_P [show/hide]; workflow Assignments/Show_Hide_Facility_Name_P1 [show/hide]
- Assignments.Facility_Room_Number: function process_new_referral [insert]; workflow Assignments/Assignment_Change_Log [read]; workflow Assignments/Assignment_Pull_From_Refe1 [set]; workflow Assignments/Show_Hide_Facility_Name_P [show/hide]; workflow Assignments/Show_Hide_Facility_Name_P1 [show/hide]
- Assignments.Employee_Link: function backfill_referral_employee_link [fetch, read]; function dash_metrics [read]; function dash_metrics_range [read]; function send_assignment_notification [read]; function widget_today_visits [read]; workflow Assignments/Assignment_Change_Log [read]; workflow Assignments/Assignment_Referral_Emplo [read]; workflow Assignments/Assignment_Required_Refer [read]; workflow Assignments/Assignment_Status_From_Pr [read]
- Assignments.Assignment_Notes: workflow Assignments/Assignment_Change_Log [read]
- Assignments.Visit_Status: function dash_metrics [read]; function dash_metrics_range [read]; function widget_today_visits [read]; page Drilldown_Data [read]; workflow Assignments/Assignment_Visit_Status_C [set]
- Assignments.Assignment_ID: function backfill_assignment_ids [read]; function diag_orphaned_records [read]; function diag_sequence_trackers [read]; function mint_assignment_id [read, update]; function send_assignment_notification [fetch, read]; function widget_today_visits [read]; page Drilldown_Data [read]; workflow Assignments/Assignment_Change_Log [read]
- Assignments.Assignment_ID_Stamp: function mint_assignment_id [update]
- Assignments.Notified_Employee_ID: function send_assignment_notification [read, update]
