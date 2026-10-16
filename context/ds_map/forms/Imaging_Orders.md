# Imaging_Orders

- Display name: Imaging Orders
- .ds line: 1700
- Fields (excluding sections): 33
- Parent form: -

## Fields

| Link name | Display name | Type | Lookup target |
|---|---|---|---|
| Order_Details_Section | Order Details Section | section | - |
| Referral_Link | Referral Link | picklist | Referrals_Main |
| Order_Priority | Order Priority | radiobuttons | - |
| Order_Status | Order Status | radiobuttons | - |
| Order_Sent_Time | Order Sent Time | datetime | - |
| Transmit_Error | Transmit Error | text | - |
| Last_Transmit_Attempt | Last Transmit Attempt | text | - |
| Patient_Details_Section | Patient Details Section | section | - |
| Patient_Full_Name | Patient Full Name | text | - |
| Patient_DOB | Patient DOB | date | - |
| Patient_Gender | Patient Gender | radiobuttons | - |
| Patient_MBI | Patient MBI | text | - |
| Patient_Hospice_ID | Patient Hospice ID | text | - |
| Patient_Location | Patient Location | radiobuttons | - |
| Patient_Address | Patient Address | address | - |
| Patient_Phone | Patient Phone | text | - |
| Facility_Name | Facility Name | text | - |
| Facility_Room_Number | Facility Room Number | text | - |
| Facility_Phone | Facility Phone | text | - |
| Is_Self_Responsible | Is the patient self responsible? | radiobuttons | - |
| DM_Full_Name | DM Full Name | text | - |
| Billing_Insurance_Section | Billing/Insurance Section | section | - |
| Primary_Insurance_Name | Primary Insurance Name | text | - |
| Primary_Insurance_ID | Primary Insurance ID | text | - |
| Secondary_Insurance_Name | Secondary Insurance Name | text | - |
| Secondary_Insurance_ID | Secondary Insurance ID | text | - |
| Provider_Details_Section | Provider Details Section | section | - |
| Provider_Signature_Link | Provider Signature Link | picklist | Employees |
| Provider_NPI | Provider NPI | text | - |
| Employee_Phone | Employee Phone | text | - |
| Exam_Clinical_Section | Exam & Clinical Section | section | - |
| Exam_Catalog | Exam Catalog | list | Exam_Catalog |
| Section | - | section | - |
| X_Ray_Order | X-Ray Order | textarea | - |
| Send_X_Ray_Results | Where to Send X-Ray Results | text | - |
| X_Ray_Results_Fax | Fax | phonenumber | - |
| X_Ray_Results_Email | Email | email | - |
| System_Fields_Section | System Fields Section | section | - |
| X_Ray_Order_ID | X-Ray Order ID | text | - |
| X_Ray_Order_ID_Stamp | X-Ray Order ID Stamp | text | - |

## Workflows

### Default_Hide_On_Load2

- Display: Default Hide On Load
- Record event: on add or edit
- Form event: OnLoad
- Status: ENABLED
- .ds line: 34227
- Fields read: -
- Fields set: -
- Fields shown/hidden/enabled/disabled: System_Fields_Section
- Functions called: -
- Other forms: -

### Imaging_Facility_Visibili

- Display: Imaging Facility Visibility On Input
- Record event: on add or edit
- Form event: OnUserInput of Patient_Location
- Status: ENABLED
- .ds line: 34167
- Fields read: Patient_Location
- Fields set: -
- Fields shown/hidden/enabled/disabled: Facility_Name, Facility_Phone, Facility_Room_Number
- Functions called: -
- Other forms: -

### Imaging_Facility_Visibili1

- Display: Imaging Facility Visibility On Load
- Record event: on add or edit
- Form event: OnLoad
- Status: ENABLED
- .ds line: 34197
- Fields read: -
- Fields set: -
- Fields shown/hidden/enabled/disabled: Facility_Name, Facility_Phone, Facility_Room_Number
- Functions called: -
- Other forms: -

### Imaging_Order_Provider_Ga

- Display: Imaging Order Provider Gate
- Record event: on add or edit
- Form event: OnValidate
- Status: ENABLED
- .ds line: 33662
- Fields read: -
- Fields set: -
- Fields shown/hidden/enabled/disabled: -
- Functions called: -
- Other forms: fetch Employees (Employee_Email, Employee_Status)

### Imaging_Order_Provider_St

- Display: Imaging Order Provider Stamp
- Record event: on add
- Form event: OnLoad
- Status: ENABLED
- .ds line: 33634
- Fields read: -
- Fields set: Employee_Phone, Provider_NPI, Provider_Signature_Link
- Fields shown/hidden/enabled/disabled: -
- Functions called: -
- Other forms: fetch Employees (Employee_Email, Employee_Portal_Email); read Employees (Employee_Phone, ID, Provider_NPI)

### Imaging_Referral_Link_Pre

- Display: Imaging Referral Link Pre-Fill
- Record event: on add or edit
- Form event: OnUserInput of Referral_Link
- Status: ENABLED
- .ds line: 34070
- Fields read: Referral_Link
- Fields set: DM_Full_Name, Facility_Name, Facility_Phone, Facility_Room_Number, Is_Self_Responsible, Patient_Address, Patient_DOB, Patient_Full_Name, Patient_Gender, Patient_Hospice_ID, Patient_Location, Patient_Phone
- Fields shown/hidden/enabled/disabled: -
- Functions called: -
- Other forms: fetch Referrals_Main (ID); read Referrals_Main (AC_Full_Name, Facility_Name, Facility_Phone, Facility_Room_Number, Has_Additional_Contact, Patient_Address, Patient_DOB, Patient_Full_Name, Patient_Gender, Patient_Hospice_ID, Patient_Location, Patient_Phone)

## Reverse index

Every item that references a field of this form.

- Imaging_Orders.Referral_Link: function diag_orphan_referral [fetch]; workflow Imaging_Orders/Imaging_Referral_Link_Pre [read, trigger]
- Imaging_Orders.Order_Priority: no references
- Imaging_Orders.Order_Status: no references
- Imaging_Orders.Order_Sent_Time: no references
- Imaging_Orders.Transmit_Error: no references
- Imaging_Orders.Last_Transmit_Attempt: no references
- Imaging_Orders.Patient_Full_Name: workflow Imaging_Orders/Imaging_Referral_Link_Pre [set]
- Imaging_Orders.Patient_DOB: workflow Imaging_Orders/Imaging_Referral_Link_Pre [set]
- Imaging_Orders.Patient_Gender: workflow Imaging_Orders/Imaging_Referral_Link_Pre [set]
- Imaging_Orders.Patient_MBI: no references
- Imaging_Orders.Patient_Hospice_ID: workflow Imaging_Orders/Imaging_Referral_Link_Pre [set]
- Imaging_Orders.Patient_Location: workflow Imaging_Orders/Imaging_Facility_Visibili [read, trigger]; workflow Imaging_Orders/Imaging_Referral_Link_Pre [set]
- Imaging_Orders.Patient_Address: workflow Imaging_Orders/Imaging_Referral_Link_Pre [set]
- Imaging_Orders.Patient_Phone: workflow Imaging_Orders/Imaging_Referral_Link_Pre [set]
- Imaging_Orders.Facility_Name: workflow Imaging_Orders/Imaging_Facility_Visibili [show/hide]; workflow Imaging_Orders/Imaging_Facility_Visibili1 [show/hide]; workflow Imaging_Orders/Imaging_Referral_Link_Pre [set]
- Imaging_Orders.Facility_Room_Number: workflow Imaging_Orders/Imaging_Facility_Visibili [show/hide]; workflow Imaging_Orders/Imaging_Facility_Visibili1 [show/hide]; workflow Imaging_Orders/Imaging_Referral_Link_Pre [set]
- Imaging_Orders.Facility_Phone: workflow Imaging_Orders/Imaging_Facility_Visibili [show/hide]; workflow Imaging_Orders/Imaging_Facility_Visibili1 [show/hide]; workflow Imaging_Orders/Imaging_Referral_Link_Pre [set]
- Imaging_Orders.Is_Self_Responsible: workflow Imaging_Orders/Imaging_Referral_Link_Pre [set]
- Imaging_Orders.DM_Full_Name: workflow Imaging_Orders/Imaging_Referral_Link_Pre [set]
- Imaging_Orders.Primary_Insurance_Name: no references
- Imaging_Orders.Primary_Insurance_ID: no references
- Imaging_Orders.Secondary_Insurance_Name: no references
- Imaging_Orders.Secondary_Insurance_ID: no references
- Imaging_Orders.Provider_Signature_Link: workflow Imaging_Orders/Imaging_Order_Provider_St [set]
- Imaging_Orders.Provider_NPI: workflow Imaging_Orders/Imaging_Order_Provider_St [set]
- Imaging_Orders.Employee_Phone: workflow Imaging_Orders/Imaging_Order_Provider_St [set]
- Imaging_Orders.Exam_Catalog: no references
- Imaging_Orders.X_Ray_Order: no references
- Imaging_Orders.Send_X_Ray_Results: no references
- Imaging_Orders.X_Ray_Results_Fax: no references
- Imaging_Orders.X_Ray_Results_Email: no references
- Imaging_Orders.X_Ray_Order_ID: no references
- Imaging_Orders.X_Ray_Order_ID_Stamp: no references
