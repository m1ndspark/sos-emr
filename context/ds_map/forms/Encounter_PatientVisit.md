# Encounter_PatientVisit

- Display name: -
- .ds line: 2600
- Fields (excluding sections): 116
- Parent form: -

## Fields

| Link name | Display name | Type | Lookup target |
|---|---|---|---|
| Referral_Lookup_Section | Referral Lookup Section | section | - |
| Visit_Status | Visit Status | picklist | - |
| Has_Referral_ID | Do you have a Referral ID? | radiobuttons | - |
| Referral_Link | Referral Link | picklist | Referrals_Main |
| Edit_Needed | Edit Needed | radiobuttons | - |
| Type_of_Entry | Type of Entry | picklist | - |
| spacer1 | - | plaintext | - |
| Cares_3008_Completion_Section | Cares 3008 Completion Section | section | - |
| Patient_Full_Name_2 | Patient Full Name | text | - |
| Was_3008_Completed | Was the 3008 Completed? | radiobuttons | - |
| PVS_3008_Upload | PVS 3008 Upload | upload file | - |
| Cares_3008_Completion_Date | 3008 Completion Date | date | - |
| Notes_3008 | 3008 Notes | textarea | - |
| spacer2 | - | plaintext | - |
| Patient_Details_Section | Patient Details Section | section | - |
| Patient_Full_Name_1 | Patient Full Name | text | - |
| Patient_First_Name | Patient First Name | text | - |
| Patient_MI | Patient MI | text | - |
| Patient_Last_Name | Patient Last Name | text | - |
| Patient_DOB | Patient DOB | date | - |
| Patient_DOB1 | Patient DOB | text | - |
| Patient_Gender | Biological Sex | picklist | - |
| Patient_Hospice_ID | Patient Hospice ID | text | - |
| Patient_SSN | Patient SSN | text | - |
| Patient_Phone | Patient Phone | phonenumber | - |
| Patient_Email | Patient Email | email | - |
| spacer3 | - | plaintext | - |
| Patient_Location_Section | Patient Location Section | section | - |
| Patient_Location | Patient Location | radiobuttons | - |
| Facility_Name | Facility Name | text | - |
| Facility_Phone | Facility Phone | phonenumber | - |
| Facility_Room_Number | Facility Room Number | text | - |
| Patient_Address | Patient Address | address | - |
| Patient_Full_Address | Patient Full Address | text | - |
| spacer4 | - | plaintext | - |
| Referral_Details_Section | Referral Details Section | section | - |
| Reason_for_Referral | Reason for Referral | textarea | - |
| Goals_of_Care | Goals of Care | textarea | - |
| Partner_ICD_Codes | Partner ICD 10 Codes | text | - |
| Additional_Information | Additional Information | textarea | - |
| List_Patient_Allergies | List Patient Allergies | textarea | - |
| List_Patient_Anticoagulants | List Patient Anticoagulants | textarea | - |
| Advanced_Directives_Details | Advanced Directives Details | textarea | - |
| General_Files_Upload | General Files Upload | upload file | - |
| Imaging_Orders_Section | Imaging Orders Section | section | - |
| Imaging_Orders | Imaging Order(s) | text | - |
| Imaging_Order_Indication | Imaging Order Indication | textarea | - |
| Upload_Imaging_Order_Files | Imaging Order Files | upload file | - |
| Imaging_Ordered_Date | Imaging Ordered Date | date | - |
| spacer5 | - | plaintext | - |
| Lab_Orders_Section | Lab Orders Section | section | - |
| Lab_Type_Orders | What labs are being ordered? | text | - |
| Lab_Order_Indication | Lab Order Indication | textarea | - |
| Requested_Lab_Vendor | Requested Lab Vendor | text | - |
| Lab_Files_Upload | Lab Files Upload | upload file | - |
| Lab_Order_Date | Lab Order Date | date | - |
| Final_Clinical_Note_Section | Clinical Note Section | section | - |
| Clinical_Note_Type | Clinical Note Type | picklist | - |
| Final_Clinical_Note | Clinical Note | richtext | - |
| Provider_ICD10_Codes_Link | ICD-10 Codes Lookup (Optional) | list | ICD10_Codes |
| Provider_ICD_Print |  Provider ICD Codes | text | - |
| Clinical_Note_File_Upload | Clinical Note File Upload | upload file | - |
| spacer6 | - | plaintext | - |
| Type_of_Procedure_Section | Type of Procedure Section | section | - |
| Type_of_Procedures | Type of Procedure(s) | list | - |
| spacer7 | - | plaintext | - |
| Visit_Cost_Drivers_Section | Visit Cost Drivers Section | section | - |
| Complexity_Level | Complexity Level | picklist | - |
| Additional_Charges | Additional Charges | checkboxes | - |
| spacer8 | - | plaintext | - |
| Charges_Section | Charges Section | section | - |
| Complexity_Charge | Complexity Charge | USD | - |
| After_Hours_Fee | After Hours ($) | USD | - |
| Super_Stat_Fee | Super STAT ($) | USD | - |
| Equipment_Charge_Amount | Equipment Charge Amount ($) | USD | - |
| Equipment_Charge_Details | Equipment Charge Details | textarea | - |
| Other_Charges_Amount | Other Charges Amount ($) | USD | - |
| Other_Charges_Details | Other Charges Details | textarea | - |
| Files_Upload_Section | Files Upload Section | section | - |
| PVS_File_Upload | PVS File Upload | upload file | - |
| spacer9 | - | plaintext | - |
| Diversion_Tracking_Section | Diversion Tracking Section | section | - |
| Diversion_Tracking | Did this visit result in a Diversion? | radiobuttons | - |
| Type_of_Diversion | Type of Diversion | picklist | - |
| spacer10 | - | plaintext | - |
| Referral_Partner_Section | Referral Partner Section | section | - |
| Partner_Organization | Referral Partner | text | - |
| Partner_Branch | Partner Branch/Location | text | - |
| Partner_POC_Name_Title | Partner POC | text | - |
| Partner_POC_Team | Partner POC Team | text | - |
| Partner_POC_First_Name | PR POC First Name | text | - |
| Partner_POC_Last_Name | PR POC Last Name | text | - |
| Partner_POC_Title | PR POC Title | picklist | - |
| Partner_POC_Phone | PR POC Phone | phonenumber | - |
| Partner_POC_Email | PR POC Email | email | - |
| Partner_Location_Label | Partner Location Label | text | - |
| spacer11 | - | plaintext | - |
| Provider_Signature_Section | Provider Signature Section | section | - |
| Employee_Name_Title | Employee Name & Title | text | - |
| Employee_First_Name | Employee First Name | text | - |
| Employee_Last_Name | Employee Last Name | text | - |
| Employee_Title | Employee Title | picklist | - |
| Employee_Initials | Employee Initials | text | - |
| Employee_Email | Employee Email | email | - |
| Visit_Completion_Date | Visit Completion Date | date | - |
| Invoice_Link | Invoice Connection | picklist | Invoices |
| Hold_From_Invoicing | Hold From Invoicing | radiobuttons | - |
| Billing_Branch | Billing Branch | picklist | Partner_Locations |
| Fax_Preview_Section | Fax Preview Section | section | - |
| Fax_This_Note | Fax This Note | checkbox | - |
| Fax_Override_Unlock | Override Fax? | checkbox | - |
| Fax_Override_Number | Fax Number | text | - |
| Fax_Override_Reason | Override Reason | textarea | - |
| Print_Preview | Print Preview | richtext | - |
| System_Fields_Section | System Fields Section | section | - |
| Note_Finalized_Time | Note Finalized Time | datetime | - |
| PVS_ID | PVS ID | text | - |
| PVS_Referral_ID | PVS Referral ID | text | - |
| Referral_ID | Referral ID | text | - |
| Referral_ID_Stamp | Referral ID Stamp | text | - |
| Partner_ID | Partner ID | text | - |
| Partner_ID_Stamp | Partner ID Stamp | text | - |
| Employee_Full_Name | Employee Full Name | text | - |
| Fax_Status | Fax Status | radiobuttons | - |
| Invoice_Status | Invoice Status | radiobuttons | - |
| QC_Reviewed | QC Reviewed | radiobuttons | - |
| Provider_Login_Email | Provider Login Email | text | - |
| Employee_Link | Employee Link | picklist | Employees |
| Row_Status | Row Status | picklist | - |
| Duplicate_Of_PVS_ID | Duplicate Of | text | - |
| Row_Status_Note | Row Status Note | textarea | - |
| Referral_Date | Referral Date | date | - |
| Referral_Source | Referral Source | text | - |

## Workflows

### Additional_Charges_Show_H1

- Display: Additional Charges Show Hide
- Record event: on add or edit
- Form event: OnUserInput of Additional_Charges
- Status: ENABLED
- .ds line: 38434
- Fields read: Additional_Charges, Billing_Branch
- Fields set: After_Hours_Fee, Equipment_Charge_Amount, Equipment_Charge_Details, Other_Charges_Amount, Other_Charges_Details, Super_Stat_Fee
- Fields shown/hidden/enabled/disabled: -
- Functions called: -
- Other forms: fetch Partner_Rates (Current_Rate, Partner_Location_Link, Rate_Type); read Partner_Rates (Rate_Amount)

### Billing_Branch_Required

- Display: Billing Branch Required
- Record event: on add or edit
- Form event: OnValidate
- Status: DISABLED
- .ds line: 38119
- Fields read: Billing_Branch, Has_Referral_ID
- Fields set: -
- Fields shown/hidden/enabled/disabled: -
- Functions called: -
- Other forms: -

### Branch_Sets_Charge

- Display: Branch Sets Charge
- Record event: on add or edit
- Form event: OnUserInput of Billing_Branch
- Status: ENABLED
- .ds line: 38189
- Fields read: Billing_Branch, Complexity_Level
- Fields set: Complexity_Charge
- Fields shown/hidden/enabled/disabled: -
- Functions called: -
- Other forms: fetch Partner_Rates (Current_Rate, Partner_Location_Link, Rate_Type); read Partner_Rates (Rate_Amount)

### Build_Patient_Full_Addres

- Display: Build Patient Full Address
- Record event: on add or edit
- Form event: OnUserInput of Patient_Address
- Status: DISABLED
- .ds line: 37402
- Fields read: Patient_Address
- Fields set: Patient_Full_Address
- Fields shown/hidden/enabled/disabled: -
- Functions called: -
- Other forms: -

### Complexity_Charge_Require

- Display: Complexity Charge Required
- Record event: on add or edit
- Form event: OnValidate
- Status: DISABLED
- .ds line: 38376
- Fields read: Billing_Branch, Complexity_Charge, Complexity_Level
- Fields set: -
- Fields shown/hidden/enabled/disabled: -
- Functions called: -
- Other forms: fetch Partner_Locations (ID); read Partner_Locations (Partner_Location_Label)

### Complexity_Sets_Charge

- Display: Complexity Sets Charge
- Record event: on add or edit
- Form event: OnUserInput of Complexity_Level
- Status: ENABLED
- .ds line: 38143
- Fields read: Billing_Branch, Complexity_Level
- Fields set: Complexity_Charge
- Fields shown/hidden/enabled/disabled: -
- Functions called: -
- Other forms: fetch Partner_Locations (ID); fetch Partner_Rates (Current_Rate, Partner_Location_Link, Rate_Type); read Partner_Locations (Partner_Location_Label); read Partner_Rates (Rate_Amount)

### Default_Hide_On_Load

- Display: Default Hide On Load
- Record event: on add or edit
- Form event: OnLoad
- Status: ENABLED
- .ds line: 36700
- Fields read: Invoice_Link
- Fields set: -
- Fields shown/hidden/enabled/disabled: Additional_Charges, Additional_Information, Advanced_Directives_Details, After_Hours_Fee, Billing_Branch, Cares_3008_Completion_Date, Cares_3008_Completion_Section, Charges_Section, Clinical_Note_File_Upload, Clinical_Note_Type, Complexity_Charge, Complexity_Level, Diversion_Tracking, Diversion_Tracking_Section, Edit_Needed, Employee_Email, Employee_First_Name, Employee_Full_Name, Employee_Initials, Employee_Last_Name, Employee_Name_Title, Employee_Title, Equipment_Charge_Amount, Equipment_Charge_Details, Facility_Name, Facility_Phone, Facility_Room_Number, Fax_Status, Files_Upload_Section, Final_Clinical_Note, Final_Clinical_Note_Section, General_Files_Upload, Goals_of_Care, Has_Referral_ID, Imaging_Order_Indication, Imaging_Ordered_Date, Imaging_Orders, Imaging_Orders_Section, Invoice_Status, Lab_Files_Upload, Lab_Order_Date, Lab_Order_Indication, Lab_Orders_Section, Lab_Type_Orders, List_Patient_Allergies, List_Patient_Anticoagulants, Notes_3008, Other_Charges_Amount, Other_Charges_Details, PVS_3008_Upload, PVS_File_Upload, PVS_ID, PVS_Referral_ID, Partner_Branch, Partner_ICD_Codes, Partner_ID, Partner_ID_Stamp, Partner_Location_Label, Partner_Organization, Partner_POC_Email, Partner_POC_First_Name, Partner_POC_Last_Name, Partner_POC_Name_Title, Partner_POC_Phone, Partner_POC_Team, Partner_POC_Title, Patient_Address, Patient_DOB, Patient_DOB1, Patient_Details_Section, Patient_Email, Patient_First_Name, Patient_Full_Address, Patient_Full_Name_1, Patient_Full_Name_2, Patient_Gender, Patient_Hospice_ID, Patient_Last_Name, Patient_Location, Patient_Location_Section, Patient_MI, Patient_Phone, Patient_SSN, Provider_ICD10_Codes_Link, Provider_ICD_Print, Provider_Signature_Section, Reason_for_Referral, Referral_Details_Section, Referral_ID, Referral_ID_Stamp, Referral_Link, Referral_Lookup_Section, Referral_Partner_Section, Requested_Lab_Vendor, Super_Stat_Fee, System_Fields_Section, Type_of_Diversion, Type_of_Entry, Type_of_Procedure_Section, Type_of_Procedures, Upload_Imaging_Order_Files, Visit_Completion_Date, Visit_Cost_Drivers_Section, Was_3008_Completed
- Functions called: -
- Other forms: -

### Diag_Session_Identity

- Display: Diag_Session_Identity
- Record event: on add
- Form event: OnLoad
- Status: DISABLED
- .ds line: 39167
- Fields read: -
- Fields set: -
- Fields shown/hidden/enabled/disabled: -
- Functions called: -
- Other forms: -

### Diversion_Type_Show_Hide

- Display: Diversion Type Show Hide
- Record event: on add
- Form event: OnUserInput of Diversion_Tracking
- Status: ENABLED
- .ds line: 35553
- Fields read: Diversion_Tracking
- Fields set: -
- Fields shown/hidden/enabled/disabled: Type_of_Diversion
- Functions called: -
- Other forms: -

### Edit_Needed_Unlock

- Display: Edit_Needed Unlock
- Record event: on add or edit
- Form event: OnUserInput of Edit_Needed
- Status: ENABLED
- .ds line: 37083
- Fields read: Edit_Needed, Has_Referral_ID
- Fields set: -
- Fields shown/hidden/enabled/disabled: Facility_Name, Facility_Phone, Facility_Room_Number, Partner_Branch, Partner_Organization, Partner_POC_Email, Partner_POC_Name_Title, Partner_POC_Phone, Partner_POC_Team, Patient_Address, Patient_DOB, Patient_Email, Patient_First_Name, Patient_Full_Name_1, Patient_Gender, Patient_Hospice_ID, Patient_Last_Name, Patient_MI, Patient_Phone, Patient_SSN
- Functions called: -
- Other forms: -

### Entry_Type_Section_Visibi

- Display: Entry Type Section Visibility
- Record event: on add
- Form event: OnUserInput of Type_of_Entry
- Status: ENABLED
- .ds line: 35448
- Fields read: Type_of_Entry
- Fields set: -
- Fields shown/hidden/enabled/disabled: Cares_3008_Completion_Section, Charges_Section, Diversion_Tracking_Section, Files_Upload_Section, Final_Clinical_Note_Section, Imaging_Orders_Section, Lab_Orders_Section, Referral_Details_Section, Type_of_Procedure_Section, Visit_Cost_Drivers_Section
- Functions called: -
- Other forms: -

### Facility_Fields_Show_Hide

- Display: Facility Fields Show Hide
- Record event: on add
- Form event: OnUserInput of Patient_Location
- Status: ENABLED
- .ds line: 37372
- Fields read: Patient_Location
- Fields set: -
- Fields shown/hidden/enabled/disabled: Facility_Name, Facility_Phone, Facility_Room_Number
- Functions called: -
- Other forms: -

### Fax_Override_Number_Forma

- Display: Fax Override Number Format
- Record event: on add or edit
- Form event: OnUserInput of Fax_Override_Number
- Status: ENABLED
- .ds line: 39860
- Fields read: -
- Fields set: Fax_Override_Number
- Fields shown/hidden/enabled/disabled: -
- Functions called: -
- Other forms: -

### Fax_This_Note_On_Submit

- Display: Fax This Note On Submit
- Record event: on add or edit
- Form event: OnSuccess
- Status: ENABLED
- .ds line: 39893
- Fields read: Fax_This_Note, ID
- Fields set: -
- Fields shown/hidden/enabled/disabled: -
- Functions called: resolve_pvs_fax_target, send_pvs_fax
- Other forms: fetch Encounter_PatientVisit (ID); update Encounter_PatientVisit (Fax_Override_Number, Fax_Override_Reason, Fax_Override_Unlock, Fax_This_Note, Print_Preview); read Encounter_PatientVisit (Fax_Override_Number, Fax_Override_Reason, Fax_Override_Unlock, Fax_Status, Partner_Location_Label, Partner_Organization, Patient_Full_Name_1, Visit_Completion_Date)

### Fax_This_Note_On_Submit1

- Display: Fax This Note On Submit
- Record event: on add or edit
- Form event: OnSuccess
- Status: ENABLED
- .ds line: 40421
- Fields read: Fax_This_Note, ID
- Fields set: -
- Fields shown/hidden/enabled/disabled: -
- Functions called: get_pvs_fax_files, resolve_pvs_fax_target, send_pvs_fax
- Other forms: fetch Encounter_PatientVisit (ID); update Encounter_PatientVisit (Fax_Override_Number, Fax_Override_Reason, Fax_Override_Unlock, Fax_This_Note, Print_Preview); read Encounter_PatientVisit (Fax_Override_Number, Fax_Override_Reason, Fax_Override_Unlock, Fax_Status, Partner_Location_Label, Partner_Organization, Patient_Full_Name_1, Visit_Completion_Date)

### Fax_This_Note_Preview_And

- Display: Fax This Note Preview And Gate
- Record event: on add or edit
- Form event: OnUserInput of Fax_This_Note
- Status: ENABLED
- .ds line: 39652
- Fields read: Billing_Branch, Clinical_Note_Type, Complexity_Level, Employee_Name_Title, Fax_Override_Number, Fax_Override_Reason, Fax_Override_Unlock, Final_Clinical_Note, PVS_ID, Partner_Branch, Partner_Location_Label, Partner_Organization, Partner_POC_Name_Title, Partner_POC_Team, Patient_DOB, Patient_First_Name, Patient_Gender, Patient_Last_Name, Patient_MI, Provider_ICD_Print, Referral_ID, Referral_Link, Type_of_Entry, Type_of_Procedures, Visit_Completion_Date, Visit_Status
- Fields set: Fax_This_Note, Print_Preview
- Fields shown/hidden/enabled/disabled: -
- Functions called: build_pvs_note_html, fmt_referral_source
- Other forms: fetch Partner_Billing_Contacts (Partner_Billing_POC_Status, Partner_Location_Link); fetch Referrals_Main (ID); read Partner_Billing_Contacts (Partner_Billing_POC_First_Name, Partner_Billing_POC_Last_Name, Partner_PVS_Fax); read Referrals_Main (Referral_Date)

### Has_Referral_ID_Show_Hide

- Display: Has Referral_ID Show_Hide
- Record event: on add or edit
- Form event: OnUserInput of Has_Referral_ID
- Status: ENABLED
- .ds line: 37154
- Fields read: Has_Referral_ID
- Fields set: Billing_Branch, Edit_Needed, Facility_Name, Facility_Phone, Facility_Room_Number, Partner_Branch, Partner_ID, Partner_ID_Stamp, Partner_Organization, Partner_POC_Email, Partner_POC_First_Name, Partner_POC_Last_Name, Partner_POC_Name_Title, Partner_POC_Phone, Partner_POC_Team, Partner_POC_Title, Patient_Address, Patient_DOB, Patient_Email, Patient_First_Name, Patient_Full_Name_1, Patient_Gender, Patient_Hospice_ID, Patient_Last_Name, Patient_Location, Patient_MI, Patient_Phone, Patient_SSN, Referral_ID, Referral_ID_Stamp, Referral_Link, Type_of_Entry
- Fields shown/hidden/enabled/disabled: Additional_Information, Advanced_Directives_Details, Cares_3008_Completion_Section, Charges_Section, Diversion_Tracking_Section, Files_Upload_Section, Final_Clinical_Note_Section, General_Files_Upload, Goals_of_Care, Imaging_Orders_Section, Lab_Orders_Section, List_Patient_Allergies, List_Patient_Anticoagulants, Partner_ICD_Codes, Referral_Details_Section, Referral_Partner_Section, Type_of_Procedure_Section, Visit_Cost_Drivers_Section
- Functions called: -
- Other forms: -

### Invoice_Status_Lock

- Display: Invoice Status Lock
- Record event: on add or edit
- Form event: OnLoad
- Status: ENABLED
- .ds line: 37503
- Fields read: Clinical_Note_Type, Invoice_Link, Invoice_Status, PVS_ID
- Fields set: -
- Fields shown/hidden/enabled/disabled: Additional_Charges, Additional_Information, Advanced_Directives_Details, After_Hours_Fee, Cares_3008_Completion_Date, Clinical_Note_File_Upload, Complexity_Charge, Complexity_Level, Diversion_Tracking, Edit_Needed, Equipment_Charge_Amount, Equipment_Charge_Details, Facility_Name, Facility_Phone, Facility_Room_Number, Final_Clinical_Note, General_Files_Upload, Goals_of_Care, Has_Referral_ID, Imaging_Order_Indication, Imaging_Ordered_Date, Imaging_Orders, Lab_Files_Upload, Lab_Order_Date, Lab_Order_Indication, Lab_Type_Orders, List_Patient_Allergies, List_Patient_Anticoagulants, Notes_3008, Other_Charges_Amount, Other_Charges_Details, PVS_File_Upload, Partner_ICD_Codes, Patient_Address, Patient_DOB, Patient_Email, Patient_First_Name, Patient_Full_Name_1, Patient_Full_Name_2, Patient_Gender, Patient_Hospice_ID, Patient_Last_Name, Patient_Location, Patient_MI, Patient_Phone, Patient_SSN, Provider_ICD10_Codes_Link, Reason_for_Referral, Referral_Link, Super_Stat_Fee, Type_of_Diversion, Type_of_Entry, Type_of_Procedures, Upload_Imaging_Order_Files, Visit_Completion_Date, Was_3008_Completed
- Functions called: -
- Other forms: -

### Note_Finalized_Stamp

- Display: Note Finalized Stamp
- Record event: on add or edit
- Form event: OnValidate
- Status: ENABLED
- .ds line: 40392
- Fields read: Clinical_Note_Type
- Fields set: Note_Finalized_Time
- Fields shown/hidden/enabled/disabled: -
- Functions called: -
- Other forms: -

### PVS_3008_Billing_Stamp

- Display: PVS 3008 Billing Stamp
- Record event: on add or edit
- Form event: OnValidate
- Status: ENABLED
- .ds line: 39415
- Fields read: Billing_Branch, Type_of_Entry
- Fields set: Cares_3008_Completion_Date, Complexity_Charge, Complexity_Level, Invoice_Status, Visit_Completion_Date
- Fields shown/hidden/enabled/disabled: -
- Functions called: -
- Other forms: fetch Partner_Rates (Current_Rate, Partner_Location_Link, Rate_Type); read Partner_Rates (Rate_Amount)

### PVS_ID_Stamp_Generator

- Display: PVS ID Stamp Generator
- Record event: on add
- Form event: OnSuccess
- Status: ENABLED
- .ds line: 35369
- Fields read: Employee_Initials, Has_Referral_ID, Referral_ID
- Fields set: PVS_ID, PVS_Referral_ID
- Fields shown/hidden/enabled/disabled: -
- Functions called: -
- Other forms: fetch Sequence_Tracker (Object_Prefix); update Sequence_Tracker (Object_Sequence); read Sequence_Tracker (Object_Sequence)

### PVS_Patient_Data_Push_Bac

- Display: PVS Patient Data Push Back
- Record event: on add or edit
- Form event: OnSuccess
- Status: ENABLED
- .ds line: 39291
- Fields read: Patient_Address, Patient_DOB, Patient_Phone, Referral_Link
- Fields set: -
- Fields shown/hidden/enabled/disabled: -
- Functions called: -
- Other forms: fetch Referrals_Main (ID); update Referrals_Main (Patient_DOB, Patient_DOB1, Patient_Phone); read Referrals_Main (ID, Patient_Address, Patient_DOB, Patient_Phone)

### PVS_Required_Fields

- Display: PVS Required Fields
- Record event: on add or edit
- Form event: OnValidate
- Status: ENABLED
- .ds line: 38543
- Fields read: Cares_3008_Completion_Date, Patient_DOB1, Type_of_Entry, Visit_Completion_Date
- Fields set: Patient_DOB, Reason_for_Referral
- Fields shown/hidden/enabled/disabled: -
- Functions called: parse_patient_dob
- Other forms: -

### PVS_Sets_Billing_Branch_O

- Display: PVS Sets Billing Branch On Save
- Record event: on add or edit
- Form event: OnValidate
- Status: ENABLED
- .ds line: 40043
- Fields read: Complexity_Level, Referral_Link
- Fields set: Billing_Branch, Complexity_Charge, Partner_Branch, Partner_Location_Label, Partner_Organization
- Fields shown/hidden/enabled/disabled: -
- Functions called: partner_branch_values, resolve_branch_id
- Other forms: fetch Partner_Locations (Partner_Location_ID); fetch Partner_Rates (Current_Rate, Partner_Location_Link, Rate_Type); fetch Referrals_Main (ID); read Partner_Locations (ID); read Partner_Rates (Rate_Amount); read Referrals_Main (ID, Partner_Branch_Link, Partner_Location_Label, Partner_Organization, Partner_POC_Email)

### PVS_System_Fields_Stamp_O

- Display: PVS System Fields Stamp On Save Type: New
- Record event: on add or edit
- Form event: OnSuccess
- Status: ENABLED
- .ds line: 40317
- Fields read: ID
- Fields set: -
- Fields shown/hidden/enabled/disabled: -
- Functions called: -
- Other forms: fetch Employees (ID); fetch Encounter_PatientVisit (ID); fetch Referrals_Main (ID); update Encounter_PatientVisit (Employee_Link, Referral_Date, Referral_Source, Row_Status); read Employees (Employee_Email, Employee_Portal_Email, ID); read Encounter_PatientVisit (Employee_Email, Employee_Link, Referral_Date, Referral_Link, Referral_Source, Row_Status, Visit_Status); read Referrals_Main (Referral_Date, Referral_Source)

### Pre_fills_provider_sectio

- Display: Pre-fills provider section from employee record
- Record event: on add
- Form event: OnLoad
- Status: ENABLED
- .ds line: 35418
- Fields read: -
- Fields set: Employee_Email, Employee_First_Name, Employee_Full_Name, Employee_Initials, Employee_Last_Name, Employee_Name_Title, Employee_Title
- Fields shown/hidden/enabled/disabled: -
- Functions called: -
- Other forms: fetch Employees (Employee_Email, Employee_Portal_Email); read Employees (Employee_Email, Employee_First_Name, Employee_Initials, Employee_Last_Name, Employee_Title)

### Provider_ICD_Print_Builde

- Display: Provider ICD Print Builder
- Record event: on add or edit
- Form event: OnUserInput of Provider_ICD10_Codes_Link
- Status: ENABLED
- .ds line: 37280
- Fields read: Provider_ICD10_Codes_Link
- Fields set: Provider_ICD_Print
- Fields shown/hidden/enabled/disabled: -
- Functions called: -
- Other forms: fetch ICD10_Codes (ID); read ICD10_Codes (ICD_Code)

### Provider_Identity_Stamp

- Display: Provider Identity Stamp
- Record event: on add or edit
- Form event: OnValidate
- Status: ENABLED
- .ds line: 39204
- Fields read: Employee_Email, ID
- Fields set: Employee_Link, Provider_Login_Email
- Fields shown/hidden/enabled/disabled: -
- Functions called: -
- Other forms: fetch Employees (Employee_Email, Employee_Portal_Email); fetch Encounter_PatientVisit (ID); read Employees (Employee_Email, Employee_Portal_Email, ID); read Encounter_PatientVisit (Employee_Email)

### Provider_Login_Stamp_On_S

- Display: Provider Login Stamp On Success
- Record event: on add or edit
- Form event: OnSuccess
- Status: ENABLED
- .ds line: 40584
- Fields read: ID
- Fields set: -
- Fields shown/hidden/enabled/disabled: -
- Functions called: -
- Other forms: fetch Employees (Employee_Email, Employee_Portal_Email); fetch Encounter_PatientVisit (ID); update Encounter_PatientVisit (Employee_Link, Provider_Login_Email); read Employees (Employee_Email, Employee_Portal_Email, ID); read Encounter_PatientVisit (Employee_Email, Employee_Link, ID, Provider_Login_Email)

### Referral_Link_Pre_Fill

- Display: Referral Link Pre-Fill
- Record event: on add
- Form event: OnUserInput of Referral_Link
- Status: ENABLED
- .ds line: 36454
- Fields read: Referral_Link
- Fields set: Additional_Information, Advanced_Directives_Details, Edit_Needed, Facility_Name, Facility_Phone, Facility_Room_Number, Goals_of_Care, List_Patient_Allergies, List_Patient_Anticoagulants, Partner_Branch, Partner_ICD_Codes, Partner_ID, Partner_ID_Stamp, Partner_Location_Label, Partner_Organization, Partner_POC_Email, Partner_POC_First_Name, Partner_POC_Last_Name, Partner_POC_Name_Title, Partner_POC_Phone, Partner_POC_Team, Partner_POC_Title, Patient_Address, Patient_DOB, Patient_Email, Patient_First_Name, Patient_Full_Name_1, Patient_Full_Name_2, Patient_Gender, Patient_Hospice_ID, Patient_Last_Name, Patient_Location, Patient_MI, Patient_Phone, Patient_SSN, Reason_for_Referral, Referral_Date, Referral_ID, Referral_ID_Stamp, Referral_Source
- Fields shown/hidden/enabled/disabled: Referral_Partner_Section
- Functions called: -
- Other forms: fetch Referrals_Main (ID); read Referrals_Main (Additional_Information, Advanced_Directives_Details, Facility_Name, Facility_Phone, Facility_Room_Number, List_Patient_Allergies, List_Patient_Anticoagulants, Partner_Branch, Partner_ICD_Codes, Partner_ID, Partner_ID_Stamp, Partner_Location_Label, Partner_Organization, Partner_POC_Email, Partner_POC_First_Name, Partner_POC_Last_Name, Partner_POC_Phone, Partner_POC_Team, Partner_POC_Title, Patient_Address, Patient_DOB, Patient_First_Name, Patient_Full_Name, Patient_Gender, Patient_Hospice_ID, Patient_Last_Name, Patient_Location, Patient_MI, Patient_Phone, Patient_SSN, Referral_Date, Referral_ID, Referral_ID_Stamp, Referral_Reason, Referral_Source)

### Referral_Sets_Billing_Bra

- Display: Referral Sets Billing Branch
- Record event: on add or edit
- Form event: OnUserInput of Referral_Link
- Status: ENABLED
- .ds line: 38030
- Fields read: Referral_Link
- Fields set: Billing_Branch, Partner_Branch, Partner_Location_Label, Partner_Organization
- Fields shown/hidden/enabled/disabled: -
- Functions called: -
- Other forms: fetch Referrals_Main (ID); read Referrals_Main (ID, Partner_Branch, Partner_Branch_Link, Partner_Location_Label, Partner_Organization)

### Validate_Complexity_On_Fi

- Display: Validate Complexity On Final
- Record event: on add or edit
- Form event: OnValidate
- Status: DISABLED
- .ds line: 38848
- Fields read: Clinical_Note_Type, Complexity_Level, Type_of_Entry
- Fields set: -
- Fields shown/hidden/enabled/disabled: -
- Functions called: -
- Other forms: -

## Reverse index

Every item that references a field of this form.

- Encounter_PatientVisit.Visit_Status: function audit_month_integrity [read]; function backfill_pvs_row_status [read]; function backfill_pvs_system_fields_range [read, update]; function build_console_docs [read]; function build_pvs_fax_html [read]; function dash_metrics [read]; function dash_metrics_range [read]; function diag_3008_missing_reason [read]; function diag_3008_overdue [read]; function diag_august_pvs_gap [read]; function diag_compliance_gap [read]; function diag_fax_readiness [read]; function diag_month_billing_gap [read]; function diag_mpu_3008_export [read]; function diag_mpu_pvs_export [read]; function diag_mpu_readiness [read]; function diag_pvs_for_refs [read]; function diag_pvs_status_mix [read]; function diag_ref_patient_pvs_match [read]; function diag_sept_pvs_completeness [fetch]; function diag_unfaxed_by_branch [fetch]; function resolve_pvs_fax_target [read]; function run_import_backfills [read]; function send_activity_digest [read]; function send_fax_digest [read]; workflow Encounter_PatientVisit/Fax_This_Note_Preview_And [read]; workflow Encounter_PatientVisit/PVS_System_Fields_Stamp_O [read]; workflow PVS_Fax_Review/PVS_Fax_Review_Fax_Now [read]
- Encounter_PatientVisit.Has_Referral_ID: function backfill_pvs_ids [read, update]; function create_3008_pvs_july [insert]; function create_3008_pvs_sept [insert]; function diag_pvs_by_recid [read]; function diag_pvs_ids [read]; function run_import_backfills [update]; workflow Encounter_PatientVisit/Billing_Branch_Required [read]; workflow Encounter_PatientVisit/Default_Hide_On_Load [show/hide]; workflow Encounter_PatientVisit/Edit_Needed_Unlock [read]; workflow Encounter_PatientVisit/Has_Referral_ID_Show_Hide [read, trigger]; workflow Encounter_PatientVisit/Invoice_Status_Lock [show/hide]; workflow Encounter_PatientVisit/PVS_ID_Stamp_Generator [read]
- Encounter_PatientVisit.Referral_Link: function audit_month_integrity [read]; function audit_pvs_billing_readiness [read]; function backfill_partner_resolver [read]; function backfill_pvs_address_from_referral [fetch, read]; function backfill_pvs_billing_branch [fetch, read]; function backfill_pvs_from_referral [fetch, read]; function backfill_pvs_link_by_cognito [fetch, update]; function backfill_pvs_referral_date [read]; function backfill_pvs_referral_id_from_link [fetch, read]; function backfill_pvs_referral_source [fetch, read]; function backfill_pvs_system_fields_range [read]; function build_console_docs [read]; function build_pvs_fax_html [read]; function create_3008_pvs_july [fetch, insert]; function create_3008_pvs_sept [fetch, insert]; function create_invoice_from_selection [read]; function dash_metrics [read]; function dash_metrics_range [fetch, read]; function diag_3008_draft_vs_invoiced [read]; function diag_3008_link_check [fetch, read]; function diag_3008_no_pvs_sheet [fetch]; function diag_3008_overdue [read]; function diag_august_pvs_gap [read]; function diag_august_pvs_state [read]; function diag_compliance_gap [read]; function diag_duplicate_patient_referrals [fetch]; function diag_invoice_patient_gaps [read]; function diag_invoice_pvs [read]; function diag_match_3008_refs [fetch]; function diag_match_pvs_by_patient [read]; function diag_missing_dob [read]; function diag_month_billing_gap [read]; function diag_mpu_3008_export [fetch]; function diag_mpu_readiness [fetch]; function diag_orphan_referral [fetch]; function diag_orphaned_records [read]; function diag_pvs_billing_vs_referral [fetch]; function diag_pvs_blank_reason [read]; function diag_pvs_by_recid [read]; function diag_pvs_for_refs [fetch]; function diag_pvs_hospice_ids [read]; function diag_pvs_names [read]; function diag_pvs_one [read]; function diag_pvs_referral_match [read]; function diag_pvs_vs_referral [read]; function diag_ref_patient_pvs_match [fetch]; function diag_referral_id_records [fetch]; function diag_referrals_missing_pvs [fetch]; function diag_room_number_gaps [read]; function link_pvs_to_referral [fetch, update]; function prepare_month_for_billing [read, update]; function relink_pvs_to_referral [fetch, update]; function repair_invoice_pvs_from_referral [read, update]; function run_import_backfills [read, update]; function run_pvs_exclusion_monitor [read]; function send_pvs_fax [read]; function set_pvs_referral_link [read, update]; function sos_referral_health [read]; function sync_pvs_branch_from_referral [read]; function sync_pvs_from_referral [read]; function widget_today_visits [fetch]; workflow Encounter_PatientVisit/Default_Hide_On_Load [show/hide]; workflow Encounter_PatientVisit/Fax_This_Note_Preview_And [read]; workflow Encounter_PatientVisit/Has_Referral_ID_Show_Hide [set]; workflow Encounter_PatientVisit/Invoice_Status_Lock [show/hide]; workflow Encounter_PatientVisit/PVS_Patient_Data_Push_Bac [read]; workflow Encounter_PatientVisit/PVS_Sets_Billing_Branch_O [read]; workflow Encounter_PatientVisit/PVS_System_Fields_Stamp_O [read]; workflow Encounter_PatientVisit/Referral_Link_Pre_Fill [read, trigger]; workflow Encounter_PatientVisit/Referral_Sets_Billing_Bra [read, trigger]; workflow PVS_Fax_Review/PVS_Fax_Review_Fax_Now [read]; workflow PVS_Fax_Review/PVS_Fax_Review_On_Load [read]
- Encounter_PatientVisit.Edit_Needed: workflow Encounter_PatientVisit/Default_Hide_On_Load [show/hide]; workflow Encounter_PatientVisit/Edit_Needed_Unlock [read, trigger]; workflow Encounter_PatientVisit/Has_Referral_ID_Show_Hide [set]; workflow Encounter_PatientVisit/Invoice_Status_Lock [show/hide]; workflow Encounter_PatientVisit/Referral_Link_Pre_Fill [set]
- Encounter_PatientVisit.Type_of_Entry: function api_fax_pvs_search [fetch]; function audit_month_integrity [read]; function audit_pvs_billing_readiness [read]; function backfill_pvs_3008_billing [fetch]; function backfill_pvs_note_placement [read]; function create_3008_pvs_july [fetch, insert]; function create_3008_pvs_sept [fetch, insert]; function dash_metrics [read]; function dash_metrics_range [read]; function diag_3008_batch_eligibility [fetch]; function diag_3008_draft_vs_invoiced [fetch]; function diag_3008_duplicates [fetch]; function diag_3008_link_check [fetch]; function diag_3008_missing_reason [fetch]; function diag_3008_no_pvs_list [fetch]; function diag_3008_overdue [fetch]; function diag_august_pvs_gap [read]; function diag_august_pvs_state [read]; function diag_fax_readiness [fetch]; function diag_find_patients [read]; function diag_held_pvs [read]; function diag_invoice_patient_gaps [read]; function diag_invoice_pvs [read]; function diag_match_3008_refs [fetch]; function diag_match_pvs_by_patient [read]; function diag_month_billing_gap [read]; function diag_mpu_pvs_export [fetch]; function diag_mpu_readiness [read]; function diag_pv_missing_proc_div [fetch]; function diag_pvs_billing_batch [read]; function diag_pvs_billing_snapshot [read]; function diag_pvs_blank_reason [read]; function diag_pvs_for_refs [read]; function diag_pvs_names [read]; function diag_pvs_note_placement [read]; function diag_pvs_provider_fields [read]; function diag_pvs_reason_by_entry [read]; function diag_pvs_stamp_gap [read]; function diag_pvs_status_mix [read]; function diag_pvs_vs_referral [read]; function diag_ref_patient_pvs_match [read]; function diag_referrals_missing_pvs [fetch]; function diag_sept_pvs_completeness [fetch]; function diag_unfaxed_by_branch [fetch]; function fill_3008_reason [fetch]; function repair_pvs_3008_import [fetch]; function resolve_pvs_fax_target [read]; function retire_3008_duplicates_auto [fetch]; function retire_pvs_duplicates [fetch]; function run_pvs_exclusion_monitor [fetch]; function send_activity_digest [read]; function send_fax_digest [fetch]; function set_pvs_entry_type [read, update]; page Drilldown_Data [read]; workflow Encounter_PatientVisit/Default_Hide_On_Load [show/hide]; workflow Encounter_PatientVisit/Entry_Type_Section_Visibi [read, trigger]; workflow Encounter_PatientVisit/Fax_This_Note_Preview_And [read]; workflow Encounter_PatientVisit/Has_Referral_ID_Show_Hide [set]; workflow Encounter_PatientVisit/Invoice_Status_Lock [show/hide]; workflow Encounter_PatientVisit/PVS_3008_Billing_Stamp [read]; workflow Encounter_PatientVisit/PVS_Required_Fields [read]; workflow Encounter_PatientVisit/Validate_Complexity_On_Fi [read]; workflow PVS_Fax_Review/PVS_Fax_Review_Fax_Now [read]
- Encounter_PatientVisit.spacer1: no references
- Encounter_PatientVisit.Patient_Full_Name_2: function backfill_pvs_from_referral [read, update]; function create_3008_pvs_july [insert]; function create_3008_pvs_sept [insert]; function diag_3008_missing_reason [read]; function diag_invoice_patient_gaps [read]; function diag_pvs_billing_snapshot [read]; function diag_pvs_blank_reason [read]; function relink_pvs_to_referral [read, update]; function repair_invoice_pvs_from_referral [read, update]; function run_import_backfills [read, update]; page Drilldown_Data [read]; workflow Encounter_PatientVisit/Default_Hide_On_Load [show/hide]; workflow Encounter_PatientVisit/Invoice_Status_Lock [show/hide]; workflow Encounter_PatientVisit/Referral_Link_Pre_Fill [set]
- Encounter_PatientVisit.Was_3008_Completed: function backfill_pvs_system_fields_range [read]; function create_3008_pvs_july [insert]; function create_3008_pvs_sept [insert]; function diag_3008_overdue [read]; function send_activity_digest [read]; workflow Encounter_PatientVisit/Default_Hide_On_Load [show/hide]; workflow Encounter_PatientVisit/Invoice_Status_Lock [show/hide]
- Encounter_PatientVisit.PVS_3008_Upload: function diag_fax_pdf_image [read]; function get_pvs_fax_files [read]; workflow Encounter_PatientVisit/Default_Hide_On_Load [show/hide]; workflow PVS_Fax_Review/PVS_Fax_Review_On_Load [read]
- Encounter_PatientVisit.Cares_3008_Completion_Date: function audit_month_integrity [read]; function backfill_pvs_3008_billing [read]; function create_3008_pvs_july [insert]; function create_3008_pvs_sept [insert]; function diag_3008_missing_reason [read]; function diag_3008_overdue [read]; function diag_pvs_for_refs [read]; function repair_pvs_3008_import [read]; function send_activity_digest [fetch, read]; workflow Encounter_PatientVisit/Default_Hide_On_Load [show/hide]; workflow Encounter_PatientVisit/Invoice_Status_Lock [show/hide]; workflow Encounter_PatientVisit/PVS_3008_Billing_Stamp [set]; workflow Encounter_PatientVisit/PVS_Required_Fields [read]
- Encounter_PatientVisit.Notes_3008: function backfill_pvs_note_placement [read, update]; function diag_pvs_note_placement [read]; workflow Encounter_PatientVisit/Default_Hide_On_Load [show/hide]; workflow Encounter_PatientVisit/Invoice_Status_Lock [show/hide]
- Encounter_PatientVisit.spacer2: no references
- Encounter_PatientVisit.Patient_Full_Name_1: function api_fax_pvs_search [read]; function audit_month_integrity [read]; function backfill_pvs_from_referral [read, update]; function build_console_docs [read]; function build_pvs_fax_html [read]; function create_3008_pvs_july [insert]; function create_3008_pvs_sept [insert]; function create_invoice_from_selection [read]; function diag_3008_duplicates [read]; function diag_3008_missing_reason [read]; function diag_duplicate_visits [read]; function diag_find_patients [read]; function diag_invoice_patient_gaps [read]; function diag_orphaned_records [read]; function diag_patient_visits [read]; function diag_pvs_blank_reason [read]; function diag_pvs_names [read]; function diag_pvs_vs_referral [read]; function diag_room_number_gaps [read]; function relink_pvs_to_referral [read, update]; function repair_invoice_pvs_from_referral [read, update]; function retire_3008_duplicates_auto [read]; function run_import_backfills [read, update]; function run_invoice_batch [read]; function run_pvs_exclusion_monitor [read]; function send_activity_digest [read]; function send_fax_digest [read]; function send_pvs_fax [read]; workflow Encounter_PatientVisit/Default_Hide_On_Load [show/hide]; workflow Encounter_PatientVisit/Edit_Needed_Unlock [show/hide]; workflow Encounter_PatientVisit/Fax_This_Note_On_Submit [read]; workflow Encounter_PatientVisit/Fax_This_Note_On_Submit1 [read]; workflow Encounter_PatientVisit/Has_Referral_ID_Show_Hide [set]; workflow Encounter_PatientVisit/Invoice_Status_Lock [show/hide]; workflow Encounter_PatientVisit/Referral_Link_Pre_Fill [set]; workflow PVS_Fax_Review/PVS_Fax_Review_On_Load [read]
- Encounter_PatientVisit.Patient_First_Name: function audit_month_integrity [read]; function audit_pvs_billing_readiness [read]; function create_3008_pvs_july [insert]; function create_3008_pvs_sept [insert]; function diag_invoice_patient_gaps [read]; function diag_mpu_readiness [read]; function diag_pvs_by_recid [read]; function diag_pvs_names [read]; function diag_pvs_vs_referral [read]; function relink_pvs_to_referral [read, update]; function repair_invoice_pvs_from_referral [read, update]; function sync_pvs_from_referral [read, update]; workflow Encounter_PatientVisit/Default_Hide_On_Load [show/hide]; workflow Encounter_PatientVisit/Edit_Needed_Unlock [show/hide]; workflow Encounter_PatientVisit/Fax_This_Note_Preview_And [read]; workflow Encounter_PatientVisit/Has_Referral_ID_Show_Hide [set]; workflow Encounter_PatientVisit/Invoice_Status_Lock [show/hide]; workflow Encounter_PatientVisit/Referral_Link_Pre_Fill [set]
- Encounter_PatientVisit.Patient_MI: function backfill_pvs_from_referral [read, update]; function create_3008_pvs_july [insert]; function create_3008_pvs_sept [insert]; function relink_pvs_to_referral [read, update]; function repair_invoice_pvs_from_referral [read, update]; function run_import_backfills [read, update]; workflow Encounter_PatientVisit/Default_Hide_On_Load [show/hide]; workflow Encounter_PatientVisit/Edit_Needed_Unlock [show/hide]; workflow Encounter_PatientVisit/Fax_This_Note_Preview_And [read]; workflow Encounter_PatientVisit/Has_Referral_ID_Show_Hide [set]; workflow Encounter_PatientVisit/Invoice_Status_Lock [show/hide]; workflow Encounter_PatientVisit/Referral_Link_Pre_Fill [set]
- Encounter_PatientVisit.Patient_Last_Name: function audit_month_integrity [read]; function audit_pvs_billing_readiness [read]; function create_3008_pvs_july [insert]; function create_3008_pvs_sept [insert]; function diag_find_patients [read]; function diag_invoice_patient_gaps [read]; function diag_match_pvs_by_patient [read]; function diag_mpu_pvs_export [read]; function diag_mpu_readiness [read]; function diag_pvs_by_recid [read]; function diag_pvs_names [read]; function diag_pvs_vs_referral [read]; function diag_ref_patient_pvs_match [read]; function relink_pvs_to_referral [read, update]; function repair_invoice_pvs_from_referral [read, update]; function sync_pvs_from_referral [read, update]; workflow Encounter_PatientVisit/Default_Hide_On_Load [show/hide]; workflow Encounter_PatientVisit/Edit_Needed_Unlock [show/hide]; workflow Encounter_PatientVisit/Fax_This_Note_Preview_And [read]; workflow Encounter_PatientVisit/Has_Referral_ID_Show_Hide [set]; workflow Encounter_PatientVisit/Invoice_Status_Lock [show/hide]; workflow Encounter_PatientVisit/Referral_Link_Pre_Fill [set]
- Encounter_PatientVisit.Patient_DOB: function audit_month_integrity [read]; function audit_pvs_billing_readiness [read]; function build_console_docs [read]; function build_pvs_fax_html [read]; function create_3008_pvs_july [insert]; function create_3008_pvs_sept [insert]; function create_invoice_from_selection [read]; function diag_3008_duplicates [read]; function diag_duplicate_visits [read]; function diag_find_patients [fetch]; function diag_invoice_same_patient_dos [read]; function diag_match_pvs_by_patient [fetch]; function diag_mpu_readiness [read]; function diag_pvs_names [read]; function diag_pvs_referral_match [read]; function diag_pvs_vs_referral [read]; function diag_ref_patient_pvs_match [fetch]; function diag_referral_id_records [read]; function relink_pvs_to_referral [read, update]; function repair_invoice_pvs_from_referral [read, update]; function retire_3008_duplicates_auto [read]; function run_invoice_batch [read]; function set_pvs_referral_link [read]; function sync_pvs_from_referral [read, update]; workflow Encounter_PatientVisit/Default_Hide_On_Load [show/hide]; workflow Encounter_PatientVisit/Edit_Needed_Unlock [show/hide]; workflow Encounter_PatientVisit/Fax_This_Note_Preview_And [read]; workflow Encounter_PatientVisit/Has_Referral_ID_Show_Hide [set]; workflow Encounter_PatientVisit/Invoice_Status_Lock [show/hide]; workflow Encounter_PatientVisit/PVS_Patient_Data_Push_Bac [read]; workflow Encounter_PatientVisit/PVS_Required_Fields [set]; workflow Encounter_PatientVisit/Referral_Link_Pre_Fill [set]
- Encounter_PatientVisit.Patient_DOB1: workflow Encounter_PatientVisit/Default_Hide_On_Load [show/hide]; workflow Encounter_PatientVisit/PVS_Required_Fields [read]
- Encounter_PatientVisit.Patient_Gender: function audit_month_integrity [read]; function audit_pvs_billing_readiness [read]; function build_console_docs [read]; function build_pvs_fax_html [read]; function create_3008_pvs_july [insert]; function create_3008_pvs_sept [insert]; function relink_pvs_to_referral [read, update]; function repair_invoice_pvs_from_referral [read, update]; function sync_pvs_from_referral [read, update]; workflow Encounter_PatientVisit/Default_Hide_On_Load [show/hide]; workflow Encounter_PatientVisit/Edit_Needed_Unlock [show/hide]; workflow Encounter_PatientVisit/Fax_This_Note_Preview_And [read]; workflow Encounter_PatientVisit/Has_Referral_ID_Show_Hide [set]; workflow Encounter_PatientVisit/Invoice_Status_Lock [show/hide]; workflow Encounter_PatientVisit/Referral_Link_Pre_Fill [set]
- Encounter_PatientVisit.Patient_Hospice_ID: function api_fax_pvs_search [read]; function audit_month_integrity [read]; function audit_pvs_billing_readiness [read]; function backfill_pvs_from_referral [read, update]; function build_pvs_fax_html [read]; function create_3008_pvs_july [insert]; function create_3008_pvs_sept [insert]; function create_invoice_from_selection [read]; function diag_invoice_patient_gaps [read]; function diag_mpu_readiness [read]; function diag_pvs_hospice_ids [read]; function relink_pvs_to_referral [read, update]; function repair_invoice_pvs_from_referral [read, update]; function run_import_backfills [read, update]; function sync_pvs_from_referral [read, update]; workflow Encounter_PatientVisit/Default_Hide_On_Load [show/hide]; workflow Encounter_PatientVisit/Edit_Needed_Unlock [show/hide]; workflow Encounter_PatientVisit/Has_Referral_ID_Show_Hide [set]; workflow Encounter_PatientVisit/Invoice_Status_Lock [show/hide]; workflow Encounter_PatientVisit/Referral_Link_Pre_Fill [set]; workflow PVS_Fax_Review/PVS_Fax_Review_Fax_Now [read]
- Encounter_PatientVisit.Patient_SSN: function backfill_pvs_from_referral [read, update]; function run_import_backfills [read, update]; workflow Encounter_PatientVisit/Default_Hide_On_Load [show/hide]; workflow Encounter_PatientVisit/Edit_Needed_Unlock [show/hide]; workflow Encounter_PatientVisit/Has_Referral_ID_Show_Hide [set]; workflow Encounter_PatientVisit/Invoice_Status_Lock [show/hide]; workflow Encounter_PatientVisit/Referral_Link_Pre_Fill [set]
- Encounter_PatientVisit.Patient_Phone: function audit_month_integrity [read]; function audit_pvs_billing_readiness [read]; function backfill_pvs_from_referral [read, update]; function create_3008_pvs_july [insert]; function create_3008_pvs_sept [insert]; function normalize_pvs_phones [read, update]; function relink_pvs_to_referral [read, update]; function run_import_backfills [read, update]; workflow Encounter_PatientVisit/Default_Hide_On_Load [show/hide]; workflow Encounter_PatientVisit/Edit_Needed_Unlock [show/hide]; workflow Encounter_PatientVisit/Has_Referral_ID_Show_Hide [set]; workflow Encounter_PatientVisit/Invoice_Status_Lock [show/hide]; workflow Encounter_PatientVisit/PVS_Patient_Data_Push_Bac [read]; workflow Encounter_PatientVisit/Referral_Link_Pre_Fill [set]
- Encounter_PatientVisit.Patient_Email: workflow Encounter_PatientVisit/Default_Hide_On_Load [show/hide]; workflow Encounter_PatientVisit/Edit_Needed_Unlock [show/hide]; workflow Encounter_PatientVisit/Has_Referral_ID_Show_Hide [set]; workflow Encounter_PatientVisit/Invoice_Status_Lock [show/hide]; workflow Encounter_PatientVisit/Referral_Link_Pre_Fill [set]
- Encounter_PatientVisit.spacer3: no references
- Encounter_PatientVisit.Patient_Location: function audit_month_integrity [read]; function audit_pvs_billing_readiness [read]; function create_3008_pvs_july [insert]; function create_3008_pvs_sept [insert]; function diag_pvs_vs_referral [read]; function diag_sept_pvs_completeness [read]; function relink_pvs_to_referral [read, update]; function sync_pvs_from_referral [read, update]; workflow Encounter_PatientVisit/Default_Hide_On_Load [show/hide]; workflow Encounter_PatientVisit/Facility_Fields_Show_Hide [read, trigger]; workflow Encounter_PatientVisit/Has_Referral_ID_Show_Hide [set]; workflow Encounter_PatientVisit/Invoice_Status_Lock [show/hide]; workflow Encounter_PatientVisit/Referral_Link_Pre_Fill [set]
- Encounter_PatientVisit.Facility_Name: function audit_month_integrity [read]; function audit_pvs_billing_readiness [read]; function create_3008_pvs_july [insert]; function create_3008_pvs_sept [insert]; function diag_pvs_vs_referral [read]; function diag_room_number_gaps [read]; function diag_sept_pvs_completeness [read]; function relink_pvs_to_referral [read, update]; function sync_pvs_from_referral [read, update]; workflow Encounter_PatientVisit/Default_Hide_On_Load [show/hide]; workflow Encounter_PatientVisit/Edit_Needed_Unlock [show/hide]; workflow Encounter_PatientVisit/Facility_Fields_Show_Hide [show/hide]; workflow Encounter_PatientVisit/Has_Referral_ID_Show_Hide [set]; workflow Encounter_PatientVisit/Invoice_Status_Lock [show/hide]; workflow Encounter_PatientVisit/Referral_Link_Pre_Fill [set]
- Encounter_PatientVisit.Facility_Phone: function audit_month_integrity [read]; function audit_pvs_billing_readiness [read]; function backfill_pvs_from_referral [read, update]; function create_3008_pvs_july [insert]; function create_3008_pvs_sept [insert]; function diag_room_number_gaps [read]; function normalize_pvs_phones [read, update]; function relink_pvs_to_referral [read, update]; function run_import_backfills [read, update]; workflow Encounter_PatientVisit/Default_Hide_On_Load [show/hide]; workflow Encounter_PatientVisit/Edit_Needed_Unlock [show/hide]; workflow Encounter_PatientVisit/Facility_Fields_Show_Hide [show/hide]; workflow Encounter_PatientVisit/Has_Referral_ID_Show_Hide [set]; workflow Encounter_PatientVisit/Invoice_Status_Lock [show/hide]; workflow Encounter_PatientVisit/Referral_Link_Pre_Fill [set]
- Encounter_PatientVisit.Facility_Room_Number: function backfill_pvs_from_referral [read, update]; function create_3008_pvs_july [insert]; function create_3008_pvs_sept [insert]; function diag_room_number_gaps [read]; function diag_sept_pvs_completeness [read]; function fix_six_room_numbers [read, update]; function relink_pvs_to_referral [read, update]; function run_import_backfills [read, update]; workflow Encounter_PatientVisit/Default_Hide_On_Load [show/hide]; workflow Encounter_PatientVisit/Edit_Needed_Unlock [show/hide]; workflow Encounter_PatientVisit/Facility_Fields_Show_Hide [show/hide]; workflow Encounter_PatientVisit/Has_Referral_ID_Show_Hide [set]; workflow Encounter_PatientVisit/Invoice_Status_Lock [show/hide]; workflow Encounter_PatientVisit/Referral_Link_Pre_Fill [set]
- Encounter_PatientVisit.Patient_Address: function audit_month_integrity [read]; function audit_pvs_billing_readiness [read]; function backfill_pvs_address_from_referral [read]; function backfill_pvs_from_referral [read]; function backfill_pvs_patient_full_address [read]; function run_import_backfills [read]; function sync_pvs_from_referral [read]; workflow Encounter_PatientVisit/Build_Patient_Full_Addres [read, trigger]; workflow Encounter_PatientVisit/Default_Hide_On_Load [show/hide]; workflow Encounter_PatientVisit/Edit_Needed_Unlock [show/hide]; workflow Encounter_PatientVisit/Has_Referral_ID_Show_Hide [set]; workflow Encounter_PatientVisit/Invoice_Status_Lock [show/hide]; workflow Encounter_PatientVisit/PVS_Patient_Data_Push_Bac [read]; workflow Encounter_PatientVisit/Referral_Link_Pre_Fill [set]
- Encounter_PatientVisit.Patient_Full_Address: function backfill_pvs_patient_full_address [read, update]; function create_3008_pvs_july [insert]; function create_3008_pvs_sept [insert]; function run_import_backfills [read, update]; workflow Encounter_PatientVisit/Build_Patient_Full_Addres [set]; workflow Encounter_PatientVisit/Default_Hide_On_Load [show/hide]
- Encounter_PatientVisit.spacer4: no references
- Encounter_PatientVisit.Reason_for_Referral: function audit_month_integrity [read]; function audit_pvs_billing_readiness [read]; function backfill_pvs_from_referral [read, update]; function backfill_pvs_system_fields_range [read, update]; function create_3008_pvs_july [insert]; function create_3008_pvs_sept [insert]; function create_invoice_from_selection [read]; function diag_3008_missing_reason [read]; function diag_august_pvs_state [read]; function diag_mpu_readiness [read]; function diag_pvs_blank_reason [read]; function diag_pvs_reason_by_entry [read]; function fill_3008_reason [read, update]; function relink_pvs_to_referral [read, update]; function repair_invoice_pvs_from_referral [read, update]; function run_import_backfills [read, update]; workflow Encounter_PatientVisit/Default_Hide_On_Load [show/hide]; workflow Encounter_PatientVisit/Invoice_Status_Lock [show/hide]; workflow Encounter_PatientVisit/PVS_Required_Fields [set]; workflow Encounter_PatientVisit/Referral_Link_Pre_Fill [set]
- Encounter_PatientVisit.Goals_of_Care: workflow Encounter_PatientVisit/Default_Hide_On_Load [show/hide]; workflow Encounter_PatientVisit/Has_Referral_ID_Show_Hide [show/hide]; workflow Encounter_PatientVisit/Invoice_Status_Lock [show/hide]; workflow Encounter_PatientVisit/Referral_Link_Pre_Fill [set]
- Encounter_PatientVisit.Partner_ICD_Codes: function backfill_pvs_from_referral [read, update]; function run_import_backfills [read, update]; workflow Encounter_PatientVisit/Default_Hide_On_Load [show/hide]; workflow Encounter_PatientVisit/Has_Referral_ID_Show_Hide [show/hide]; workflow Encounter_PatientVisit/Invoice_Status_Lock [show/hide]; workflow Encounter_PatientVisit/Referral_Link_Pre_Fill [set]
- Encounter_PatientVisit.Additional_Information: function backfill_pvs_from_referral [read, update]; function run_import_backfills [read, update]; workflow Encounter_PatientVisit/Default_Hide_On_Load [show/hide]; workflow Encounter_PatientVisit/Has_Referral_ID_Show_Hide [show/hide]; workflow Encounter_PatientVisit/Invoice_Status_Lock [show/hide]; workflow Encounter_PatientVisit/Referral_Link_Pre_Fill [set]
- Encounter_PatientVisit.List_Patient_Allergies: function backfill_pvs_from_referral [read, update]; function run_import_backfills [read, update]; workflow Encounter_PatientVisit/Default_Hide_On_Load [show/hide]; workflow Encounter_PatientVisit/Has_Referral_ID_Show_Hide [show/hide]; workflow Encounter_PatientVisit/Invoice_Status_Lock [show/hide]; workflow Encounter_PatientVisit/Referral_Link_Pre_Fill [set]
- Encounter_PatientVisit.List_Patient_Anticoagulants: function backfill_pvs_from_referral [read, update]; function run_import_backfills [read, update]; workflow Encounter_PatientVisit/Default_Hide_On_Load [show/hide]; workflow Encounter_PatientVisit/Has_Referral_ID_Show_Hide [show/hide]; workflow Encounter_PatientVisit/Invoice_Status_Lock [show/hide]; workflow Encounter_PatientVisit/Referral_Link_Pre_Fill [set]
- Encounter_PatientVisit.Advanced_Directives_Details: function backfill_pvs_from_referral [read, update]; function run_import_backfills [read, update]; workflow Encounter_PatientVisit/Default_Hide_On_Load [show/hide]; workflow Encounter_PatientVisit/Has_Referral_ID_Show_Hide [show/hide]; workflow Encounter_PatientVisit/Invoice_Status_Lock [show/hide]; workflow Encounter_PatientVisit/Referral_Link_Pre_Fill [set]
- Encounter_PatientVisit.General_Files_Upload: function diag_upload_field_usage [read]; function get_pvs_fax_files [read]; workflow Encounter_PatientVisit/Default_Hide_On_Load [show/hide]; workflow Encounter_PatientVisit/Has_Referral_ID_Show_Hide [show/hide]; workflow Encounter_PatientVisit/Invoice_Status_Lock [show/hide]
- Encounter_PatientVisit.Imaging_Orders: workflow Encounter_PatientVisit/Default_Hide_On_Load [show/hide]; workflow Encounter_PatientVisit/Invoice_Status_Lock [show/hide]
- Encounter_PatientVisit.Imaging_Order_Indication: workflow Encounter_PatientVisit/Default_Hide_On_Load [show/hide]; workflow Encounter_PatientVisit/Invoice_Status_Lock [show/hide]
- Encounter_PatientVisit.Upload_Imaging_Order_Files: function get_pvs_fax_files [read]; workflow Encounter_PatientVisit/Default_Hide_On_Load [show/hide]; workflow Encounter_PatientVisit/Invoice_Status_Lock [show/hide]
- Encounter_PatientVisit.Imaging_Ordered_Date: workflow Encounter_PatientVisit/Default_Hide_On_Load [show/hide]; workflow Encounter_PatientVisit/Invoice_Status_Lock [show/hide]
- Encounter_PatientVisit.spacer5: no references
- Encounter_PatientVisit.Lab_Type_Orders: workflow Encounter_PatientVisit/Default_Hide_On_Load [show/hide]; workflow Encounter_PatientVisit/Invoice_Status_Lock [show/hide]
- Encounter_PatientVisit.Lab_Order_Indication: workflow Encounter_PatientVisit/Default_Hide_On_Load [show/hide]; workflow Encounter_PatientVisit/Invoice_Status_Lock [show/hide]
- Encounter_PatientVisit.Requested_Lab_Vendor: workflow Encounter_PatientVisit/Default_Hide_On_Load [show/hide]
- Encounter_PatientVisit.Lab_Files_Upload: function get_pvs_fax_files [read]; workflow Encounter_PatientVisit/Default_Hide_On_Load [show/hide]; workflow Encounter_PatientVisit/Invoice_Status_Lock [show/hide]
- Encounter_PatientVisit.Lab_Order_Date: workflow Encounter_PatientVisit/Default_Hide_On_Load [show/hide]; workflow Encounter_PatientVisit/Invoice_Status_Lock [show/hide]
- Encounter_PatientVisit.Clinical_Note_Type: function api_fax_pvs_search [read]; function audit_month_integrity [read]; function audit_pvs_billing_readiness [read]; function backfill_note_finalized_time [fetch, read]; function build_console_docs [read]; function build_pvs_fax_html [read]; function dash_metrics [read]; function dash_metrics_range [read]; function diag_addendum_restamp [fetch]; function diag_fax_readiness [read]; function diag_match_pvs_by_patient [read]; function diag_mpu_readiness [read]; function diag_pvs_added_time_clusters [fetch]; function diag_pvs_billing_batch [read]; function diag_pvs_note_compare [read]; function diag_pvs_stamp_gap [read]; function diag_pvs_status_mix [read]; function diag_unfaxed_by_branch [fetch]; function resolve_pvs_fax_target [read]; function send_activity_digest [fetch, read]; function send_fax_digest [read]; workflow Encounter_PatientVisit/Default_Hide_On_Load [show/hide]; workflow Encounter_PatientVisit/Fax_This_Note_Preview_And [read]; workflow Encounter_PatientVisit/Invoice_Status_Lock [read]; workflow Encounter_PatientVisit/Note_Finalized_Stamp [read]; workflow Encounter_PatientVisit/Validate_Complexity_On_Fi [read]; workflow PVS_Fax_Review/PVS_Fax_Review_Fax_Now [read]
- Encounter_PatientVisit.Final_Clinical_Note: function audit_month_integrity [read]; function audit_pvs_billing_readiness [read]; function backfill_pvs_note_placement [read, update]; function build_console_docs [read]; function build_pvs_fax_html [read]; function diag_fax_readiness [read]; function diag_pvs_note_compare [read]; function diag_pvs_note_placement [read]; function diag_pvs_note_text [read]; function resolve_pvs_fax_target [read]; function run_pvs_exclusion_monitor [read]; workflow Encounter_PatientVisit/Default_Hide_On_Load [show/hide]; workflow Encounter_PatientVisit/Fax_This_Note_Preview_And [read]; workflow Encounter_PatientVisit/Invoice_Status_Lock [show/hide]; workflow PVS_Fax_Review/PVS_Fax_Review_Fax_Now [read]
- Encounter_PatientVisit.Provider_ICD10_Codes_Link: workflow Encounter_PatientVisit/Default_Hide_On_Load [show/hide]; workflow Encounter_PatientVisit/Invoice_Status_Lock [show/hide]; workflow Encounter_PatientVisit/Provider_ICD_Print_Builde [read, trigger]
- Encounter_PatientVisit.Provider_ICD_Print: function build_console_docs [read]; function build_pvs_fax_html [read]; function diag_pvs_note_compare [read]; workflow Encounter_PatientVisit/Default_Hide_On_Load [show/hide]; workflow Encounter_PatientVisit/Fax_This_Note_Preview_And [read]; workflow Encounter_PatientVisit/Provider_ICD_Print_Builde [set]
- Encounter_PatientVisit.Clinical_Note_File_Upload: function diag_fax_pdf_image [read]; function diag_pvs_note_compare [read]; function get_pvs_fax_files [read]; workflow Encounter_PatientVisit/Default_Hide_On_Load [show/hide]; workflow Encounter_PatientVisit/Invoice_Status_Lock [show/hide]; workflow PVS_Fax_Review/PVS_Fax_Review_On_Load [read]
- Encounter_PatientVisit.spacer6: no references
- Encounter_PatientVisit.Type_of_Procedures: function audit_month_integrity [read]; function audit_pvs_billing_readiness [read]; function build_console_docs [read]; function build_pvs_fax_html [read]; function diag_mpu_readiness [read]; function diag_pv_missing_proc_div [read]; function diag_pvs_note_compare [read]; function diag_pvs_note_text [read]; function send_activity_digest [read]; function set_pvs_procedures [read, update]; workflow Encounter_PatientVisit/Default_Hide_On_Load [show/hide]; workflow Encounter_PatientVisit/Fax_This_Note_Preview_And [read]; workflow Encounter_PatientVisit/Invoice_Status_Lock [show/hide]
- Encounter_PatientVisit.spacer7: no references
- Encounter_PatientVisit.Complexity_Level: function audit_month_integrity [read]; function audit_pvs_billing_readiness [read]; function backfill_pvs_3008_billing [read, update]; function backfill_pvs_billing_branch [read]; function backfill_pvs_complexity_charge [read]; function build_console_docs [read]; function build_pvs_fax_html [read]; function create_3008_pvs_july [insert]; function create_3008_pvs_sept [insert]; function create_invoice_from_selection [read]; function dash_metrics [read]; function dash_metrics_range [read]; function diag_3008_batch_eligibility [read]; function diag_august_pvs_state [read]; function diag_billing_preview [read]; function diag_invoice_pvs [read]; function diag_invoice_record [read]; function diag_invoice_same_patient_dos [read]; function diag_month_billing_gap [read]; function diag_mpu_readiness [read]; function diag_patient_visits [read]; function diag_pvs_billing_batch [read]; function diag_pvs_billing_snapshot [read]; function diag_pvs_note_compare [read]; function diag_pvs_note_text [read]; function diag_pvs_provider_fields [read]; function prepare_month_for_billing [read]; function repair_pvs_3008_import [read, update]; function reprice_draft_pvs [read]; function run_import_backfills [read]; function run_invoice_batch [read]; function set_pvs_cancelled_row_status [fetch]; function set_pvs_complexity [read, update]; function sync_pvs_branch_from_referral [read]; page Drilldown_Data [read]; workflow Encounter_PatientVisit/Branch_Sets_Charge [read]; workflow Encounter_PatientVisit/Complexity_Charge_Require [read]; workflow Encounter_PatientVisit/Complexity_Sets_Charge [read, trigger]; workflow Encounter_PatientVisit/Default_Hide_On_Load [show/hide]; workflow Encounter_PatientVisit/Fax_This_Note_Preview_And [read]; workflow Encounter_PatientVisit/Invoice_Status_Lock [show/hide]; workflow Encounter_PatientVisit/PVS_3008_Billing_Stamp [set]; workflow Encounter_PatientVisit/PVS_Sets_Billing_Branch_O [read]; workflow Encounter_PatientVisit/Validate_Complexity_On_Fi [read]
- Encounter_PatientVisit.Additional_Charges: function audit_pvs_billing_readiness [read]; function backfill_pvs_premium_fees [fetch, read]; function diag_mpu_pvs_export [read]; function diag_mpu_readiness [read]; function diag_pvs_premium_mismatches [fetch, read]; function sync_pvs_branch_from_referral [read]; workflow Encounter_PatientVisit/Additional_Charges_Show_H1 [read, trigger]; workflow Encounter_PatientVisit/Default_Hide_On_Load [show/hide]; workflow Encounter_PatientVisit/Invoice_Status_Lock [show/hide]
- Encounter_PatientVisit.spacer8: no references
- Encounter_PatientVisit.Complexity_Charge: function audit_month_integrity [read]; function audit_pvs_billing_readiness [read]; function backfill_pvs_3008_billing [read, update]; function backfill_pvs_billing_branch [update]; function backfill_pvs_complexity_charge [read, update]; function create_3008_pvs_july [insert]; function create_3008_pvs_sept [insert]; function create_invoice_from_selection [read]; function dash_metrics [read]; function dash_metrics_range [read]; function diag_3008_batch_eligibility [read]; function diag_3008_duplicates [read]; function diag_august_pvs_state [read]; function diag_billing_preview [read]; function diag_duplicate_visits [read]; function diag_invoice_pvs [read]; function diag_invoice_record [read]; function diag_month_billing_gap [read]; function diag_patient_visits [read]; function diag_pvs_billing_batch [read]; function diag_pvs_billing_snapshot [read]; function diag_pvs_provider_fields [read]; function prepare_month_for_billing [read, update]; function repair_pvs_3008_import [read, update]; function reprice_draft_pvs [read, update]; function retire_pvs_duplicate [read, update]; function retire_pvs_record [read, update]; function run_import_backfills [read, update]; function run_invoice_batch [read]; function sync_pvs_branch_from_referral [read, update]; page Drilldown_Data [read]; workflow Encounter_PatientVisit/Branch_Sets_Charge [set]; workflow Encounter_PatientVisit/Complexity_Charge_Require [read]; workflow Encounter_PatientVisit/Complexity_Sets_Charge [set]; workflow Encounter_PatientVisit/Default_Hide_On_Load [show/hide]; workflow Encounter_PatientVisit/Invoice_Status_Lock [show/hide]; workflow Encounter_PatientVisit/PVS_3008_Billing_Stamp [set]; workflow Encounter_PatientVisit/PVS_Sets_Billing_Branch_O [set]
- Encounter_PatientVisit.After_Hours_Fee: function audit_month_integrity [read]; function audit_pvs_billing_readiness [read]; function backfill_pvs_premium_fees [read, update]; function create_invoice_from_selection [read]; function dash_metrics [read]; function dash_metrics_range [read]; function diag_billing_preview [read]; function diag_month_billing_gap [read]; function diag_pvs_premium_mismatches [read]; function retire_pvs_record [read, update]; function run_invoice_batch [read]; page Drilldown_Data [read]; workflow Encounter_PatientVisit/Additional_Charges_Show_H1 [set]; workflow Encounter_PatientVisit/Default_Hide_On_Load [show/hide]; workflow Encounter_PatientVisit/Invoice_Status_Lock [show/hide]
- Encounter_PatientVisit.Super_Stat_Fee: function audit_month_integrity [read]; function audit_pvs_billing_readiness [read]; function backfill_pvs_premium_fees [read, update]; function create_invoice_from_selection [read]; function dash_metrics [read]; function dash_metrics_range [read]; function diag_billing_preview [read]; function diag_month_billing_gap [read]; function diag_pvs_premium_mismatches [read]; function retire_pvs_record [read, update]; function run_invoice_batch [read]; page Drilldown_Data [read]; workflow Encounter_PatientVisit/Additional_Charges_Show_H1 [set]; workflow Encounter_PatientVisit/Default_Hide_On_Load [show/hide]; workflow Encounter_PatientVisit/Invoice_Status_Lock [show/hide]
- Encounter_PatientVisit.Equipment_Charge_Amount: function audit_month_integrity [read]; function audit_pvs_billing_readiness [read]; function create_invoice_from_selection [read]; function dash_metrics [read]; function dash_metrics_range [read]; function diag_billing_preview [read]; function diag_month_billing_gap [read]; function diag_mpu_pvs_export [read]; function diag_mpu_readiness [read]; function retire_pvs_record [read, update]; function run_invoice_batch [read]; page Drilldown_Data [read]; workflow Encounter_PatientVisit/Additional_Charges_Show_H1 [set]; workflow Encounter_PatientVisit/Default_Hide_On_Load [show/hide]; workflow Encounter_PatientVisit/Invoice_Status_Lock [show/hide]
- Encounter_PatientVisit.Equipment_Charge_Details: workflow Encounter_PatientVisit/Additional_Charges_Show_H1 [set]; workflow Encounter_PatientVisit/Default_Hide_On_Load [show/hide]; workflow Encounter_PatientVisit/Invoice_Status_Lock [show/hide]
- Encounter_PatientVisit.Other_Charges_Amount: function audit_month_integrity [read]; function audit_pvs_billing_readiness [read]; function create_invoice_from_selection [read]; function dash_metrics [read]; function dash_metrics_range [read]; function diag_billing_preview [read]; function diag_month_billing_gap [read]; function retire_pvs_record [read, update]; function run_invoice_batch [read]; page Drilldown_Data [read]; workflow Encounter_PatientVisit/Additional_Charges_Show_H1 [set]; workflow Encounter_PatientVisit/Default_Hide_On_Load [show/hide]; workflow Encounter_PatientVisit/Invoice_Status_Lock [show/hide]
- Encounter_PatientVisit.Other_Charges_Details: workflow Encounter_PatientVisit/Additional_Charges_Show_H1 [set]; workflow Encounter_PatientVisit/Default_Hide_On_Load [show/hide]; workflow Encounter_PatientVisit/Invoice_Status_Lock [show/hide]
- Encounter_PatientVisit.PVS_File_Upload: function diag_fax_pdf_image [read]; function diag_pvs_note_compare [read]; function get_pvs_fax_files [read]; workflow Encounter_PatientVisit/Default_Hide_On_Load [show/hide]; workflow Encounter_PatientVisit/Invoice_Status_Lock [show/hide]; workflow PVS_Fax_Review/PVS_Fax_Review_On_Load [read]
- Encounter_PatientVisit.spacer9: no references
- Encounter_PatientVisit.Diversion_Tracking: function audit_month_integrity [read]; function audit_pvs_billing_readiness [read]; function dash_metrics_range [read]; function diag_mpu_readiness [read]; function diag_pv_missing_proc_div [read]; function diag_pvs_note_text [read]; function set_pvs_diversion [read, update]; workflow Encounter_PatientVisit/Default_Hide_On_Load [show/hide]; workflow Encounter_PatientVisit/Diversion_Type_Show_Hide [read, trigger]; workflow Encounter_PatientVisit/Invoice_Status_Lock [show/hide]
- Encounter_PatientVisit.Type_of_Diversion: function set_pvs_diversion [update]; workflow Encounter_PatientVisit/Default_Hide_On_Load [show/hide]; workflow Encounter_PatientVisit/Diversion_Type_Show_Hide [show/hide]; workflow Encounter_PatientVisit/Invoice_Status_Lock [show/hide]
- Encounter_PatientVisit.spacer10: no references
- Encounter_PatientVisit.Partner_Organization: function audit_month_integrity [read]; function audit_pvs_billing_readiness [read]; function backfill_partner_resolver [fetch, read, update]; function backfill_pvs_billing_branch [update]; function build_console_docs [read]; function build_pvs_fax_html [read]; function create_3008_pvs_july [insert]; function create_3008_pvs_sept [insert]; function diag_held_pvs [read]; function diag_mpu_readiness [read]; function diag_pvs_vs_referral [read]; function diag_sept_pvs_completeness [read]; function prepare_month_for_billing [update]; function relink_pvs_to_referral [read, update]; function run_import_backfills [update]; function run_pvs_exclusion_monitor [read]; function send_activity_digest [read]; function sync_pvs_branch_from_referral [update]; function sync_pvs_from_referral [read, update]; workflow Encounter_PatientVisit/Default_Hide_On_Load [show/hide]; workflow Encounter_PatientVisit/Edit_Needed_Unlock [show/hide]; workflow Encounter_PatientVisit/Fax_This_Note_On_Submit [read]; workflow Encounter_PatientVisit/Fax_This_Note_On_Submit1 [read]; workflow Encounter_PatientVisit/Fax_This_Note_Preview_And [read]; workflow Encounter_PatientVisit/Has_Referral_ID_Show_Hide [set]; workflow Encounter_PatientVisit/PVS_Sets_Billing_Branch_O [set]; workflow Encounter_PatientVisit/Referral_Link_Pre_Fill [set]; workflow Encounter_PatientVisit/Referral_Sets_Billing_Bra [set]
- Encounter_PatientVisit.Partner_Branch: function audit_month_integrity [read]; function audit_pvs_billing_readiness [read]; function backfill_partner_resolver [fetch, read, update]; function backfill_pvs_billing_branch [update]; function build_console_docs [read]; function build_pvs_fax_html [read]; function create_3008_pvs_july [insert]; function create_3008_pvs_sept [insert]; function diag_mpu_readiness [read]; function diag_pvs_vs_referral [read]; function prepare_month_for_billing [update]; function relink_pvs_to_referral [read, update]; function resolve_pvs_fax_target [read]; function resync_location_names [update]; function run_import_backfills [update]; function sync_pvs_branch_from_referral [update]; function sync_pvs_from_referral [read, update]; workflow Encounter_PatientVisit/Default_Hide_On_Load [show/hide]; workflow Encounter_PatientVisit/Edit_Needed_Unlock [show/hide]; workflow Encounter_PatientVisit/Fax_This_Note_Preview_And [read]; workflow Encounter_PatientVisit/Has_Referral_ID_Show_Hide [set]; workflow Encounter_PatientVisit/PVS_Sets_Billing_Branch_O [set]; workflow Encounter_PatientVisit/Referral_Link_Pre_Fill [set]; workflow Encounter_PatientVisit/Referral_Sets_Billing_Bra [set]
- Encounter_PatientVisit.Partner_POC_Name_Title: function backfill_pvs_from_referral [read, update]; function build_console_docs [read]; function build_pvs_fax_html [read]; function create_3008_pvs_july [insert]; function create_3008_pvs_sept [insert]; function run_import_backfills [read, update]; workflow Encounter_PatientVisit/Default_Hide_On_Load [show/hide]; workflow Encounter_PatientVisit/Edit_Needed_Unlock [show/hide]; workflow Encounter_PatientVisit/Fax_This_Note_Preview_And [read]; workflow Encounter_PatientVisit/Has_Referral_ID_Show_Hide [set]; workflow Encounter_PatientVisit/Referral_Link_Pre_Fill [set]
- Encounter_PatientVisit.Partner_POC_Team: function backfill_pvs_from_referral [read, update]; function build_console_docs [read]; function build_pvs_fax_html [read]; function create_3008_pvs_july [insert]; function create_3008_pvs_sept [insert]; function run_import_backfills [read, update]; workflow Encounter_PatientVisit/Default_Hide_On_Load [show/hide]; workflow Encounter_PatientVisit/Edit_Needed_Unlock [show/hide]; workflow Encounter_PatientVisit/Fax_This_Note_Preview_And [read]; workflow Encounter_PatientVisit/Has_Referral_ID_Show_Hide [set]; workflow Encounter_PatientVisit/Referral_Link_Pre_Fill [set]
- Encounter_PatientVisit.Partner_POC_First_Name: function backfill_pvs_from_referral [read, update]; function run_import_backfills [read, update]; workflow Encounter_PatientVisit/Default_Hide_On_Load [show/hide]; workflow Encounter_PatientVisit/Has_Referral_ID_Show_Hide [set]; workflow Encounter_PatientVisit/Referral_Link_Pre_Fill [set]
- Encounter_PatientVisit.Partner_POC_Last_Name: function backfill_pvs_from_referral [read, update]; function run_import_backfills [read, update]; workflow Encounter_PatientVisit/Default_Hide_On_Load [show/hide]; workflow Encounter_PatientVisit/Has_Referral_ID_Show_Hide [set]; workflow Encounter_PatientVisit/Referral_Link_Pre_Fill [set]
- Encounter_PatientVisit.Partner_POC_Title: function backfill_pvs_from_referral [read, update]; function run_import_backfills [read, update]; workflow Encounter_PatientVisit/Default_Hide_On_Load [show/hide]; workflow Encounter_PatientVisit/Has_Referral_ID_Show_Hide [set]; workflow Encounter_PatientVisit/Referral_Link_Pre_Fill [set]
- Encounter_PatientVisit.Partner_POC_Phone: function backfill_pvs_from_referral [read, update]; function create_3008_pvs_july [insert]; function create_3008_pvs_sept [insert]; function normalize_pvs_phones [read, update]; function run_import_backfills [read, update]; workflow Encounter_PatientVisit/Default_Hide_On_Load [show/hide]; workflow Encounter_PatientVisit/Edit_Needed_Unlock [show/hide]; workflow Encounter_PatientVisit/Has_Referral_ID_Show_Hide [set]; workflow Encounter_PatientVisit/Referral_Link_Pre_Fill [set]
- Encounter_PatientVisit.Partner_POC_Email: function backfill_pvs_from_referral [read, update]; function create_3008_pvs_july [insert]; function create_3008_pvs_sept [insert]; function run_import_backfills [read, update]; workflow Encounter_PatientVisit/Default_Hide_On_Load [show/hide]; workflow Encounter_PatientVisit/Edit_Needed_Unlock [show/hide]; workflow Encounter_PatientVisit/Has_Referral_ID_Show_Hide [set]; workflow Encounter_PatientVisit/Referral_Link_Pre_Fill [set]
- Encounter_PatientVisit.Partner_Location_Label: function audit_month_integrity [read]; function backfill_partner_resolver [fetch, read, update]; function backfill_pvs_billing_branch [update]; function backfill_pvs_from_referral [read, update]; function diag_match_pvs_by_patient [read]; function diag_pvs_fax_number [read]; function diag_pvs_vs_referral [read]; function prepare_month_for_billing [update]; function resolve_pvs_fax_target [read]; function resync_location_labels [update]; function retry_failed_faxes [read]; function run_import_backfills [update]; function send_fax_digest [read]; function sync_pvs_branch_from_referral [update]; function sync_pvs_from_referral [read, update]; workflow Encounter_PatientVisit/Default_Hide_On_Load [show/hide]; workflow Encounter_PatientVisit/Fax_This_Note_On_Submit [read]; workflow Encounter_PatientVisit/Fax_This_Note_On_Submit1 [read]; workflow Encounter_PatientVisit/Fax_This_Note_Preview_And [read]; workflow Encounter_PatientVisit/PVS_Sets_Billing_Branch_O [set]; workflow Encounter_PatientVisit/Referral_Link_Pre_Fill [set]; workflow Encounter_PatientVisit/Referral_Sets_Billing_Bra [set]
- Encounter_PatientVisit.spacer11: no references
- Encounter_PatientVisit.Employee_Name_Title: function audit_month_integrity [read]; function audit_pvs_billing_readiness [read]; function backfill_pvs_employee_email [read, update]; function backfill_pvs_provider_identity [read, update]; function build_console_docs [read]; function build_pvs_fax_html [read]; function create_3008_pvs_july [insert]; function create_3008_pvs_sept [insert]; function diag_mpu_3008_export [read]; function diag_provider_backfill_trace [read]; function diag_pvs_provider_fields [read]; function diag_pvs_vs_referral [read]; function run_import_backfills [update]; function run_pvs_exclusion_monitor [read]; function send_activity_digest [read]; function set_pvs_provider [read, update]; workflow Encounter_PatientVisit/Default_Hide_On_Load [show/hide]; workflow Encounter_PatientVisit/Fax_This_Note_Preview_And [read]; workflow Encounter_PatientVisit/Pre_fills_provider_sectio [set]
- Encounter_PatientVisit.Employee_First_Name: function audit_pvs_billing_readiness [read]; function backfill_pvs_employee_email [read]; function backfill_pvs_provider_identity [read, update]; function create_3008_pvs_july [insert]; function create_3008_pvs_sept [insert]; function diag_provider_backfill_trace [read]; function diag_pvs_provider_fields [read]; function run_import_backfills [update]; function set_pvs_provider [read, update]; workflow Encounter_PatientVisit/Default_Hide_On_Load [show/hide]; workflow Encounter_PatientVisit/Pre_fills_provider_sectio [set]
- Encounter_PatientVisit.Employee_Last_Name: function audit_pvs_billing_readiness [read]; function backfill_pvs_employee_email [fetch, read]; function backfill_pvs_provider_identity [read, update]; function create_3008_pvs_july [insert]; function create_3008_pvs_sept [insert]; function diag_provider_backfill_trace [read]; function diag_pvs_provider_fields [read]; function run_import_backfills [update]; function set_pvs_provider [read, update]; workflow Encounter_PatientVisit/Default_Hide_On_Load [show/hide]; workflow Encounter_PatientVisit/Pre_fills_provider_sectio [set]
- Encounter_PatientVisit.Employee_Title: function audit_pvs_billing_readiness [read]; function backfill_pvs_employee_email [read, update]; function backfill_pvs_provider_identity [read, update]; function create_3008_pvs_july [insert]; function create_3008_pvs_sept [insert]; function diag_provider_backfill_trace [read]; function diag_pvs_provider_fields [read]; function run_import_backfills [update]; function set_pvs_provider [read, update]; workflow Encounter_PatientVisit/Default_Hide_On_Load [show/hide]; workflow Encounter_PatientVisit/Pre_fills_provider_sectio [set]
- Encounter_PatientVisit.Employee_Initials: function audit_month_integrity [read]; function audit_pvs_billing_readiness [read]; function backfill_pvs_employee_email [read, update]; function backfill_pvs_employee_email_alias [read]; function backfill_pvs_employee_initials [fetch, update]; function backfill_pvs_employee_link_range [read]; function backfill_pvs_ids [read]; function backfill_pvs_provider_identity [read, update]; function create_3008_pvs_july [insert]; function create_3008_pvs_sept [insert]; function diag_find_patients [read]; function diag_held_pvs [read]; function diag_provider_backfill_trace [read]; function diag_pvs_provider_fields [read]; function run_import_backfills [read, update]; function set_pvs_provider [read, update]; workflow Encounter_PatientVisit/Default_Hide_On_Load [show/hide]; workflow Encounter_PatientVisit/PVS_ID_Stamp_Generator [read]; workflow Encounter_PatientVisit/Pre_fills_provider_sectio [set]
- Encounter_PatientVisit.Employee_Email: function audit_pvs_billing_readiness [read]; function backfill_provider_login_email [read]; function backfill_pvs_employee_email [read, update]; function backfill_pvs_employee_email_alias [read, update]; function backfill_pvs_employee_initials [fetch, read]; function backfill_pvs_employee_link [read]; function backfill_pvs_employee_link_range [read]; function backfill_pvs_provider_identity [read, update]; function create_3008_pvs_july [insert]; function create_3008_pvs_sept [insert]; function diag_provider_backfill_trace [read]; function diag_pvs_login_email_gaps [read]; function diag_pvs_one [read]; function diag_pvs_provider_fields [read]; function diag_pvs_stamp_gap [read]; function run_import_backfills [read, update]; function set_pvs_provider [read, update]; workflow Encounter_PatientVisit/Default_Hide_On_Load [show/hide]; workflow Encounter_PatientVisit/PVS_System_Fields_Stamp_O [read]; workflow Encounter_PatientVisit/Pre_fills_provider_sectio [set]; workflow Encounter_PatientVisit/Provider_Identity_Stamp [read]; workflow Encounter_PatientVisit/Provider_Login_Stamp_On_S [read]
- Encounter_PatientVisit.Visit_Completion_Date: function api_fax_pvs_search [read]; function audit_month_integrity [fetch, read]; function audit_pvs_billing_readiness [fetch, read]; function backfill_pvs_3008_billing [read, update]; function backfill_pvs_employee_link_range [fetch]; function backfill_pvs_invoice_status [fetch]; function backfill_pvs_note_placement [fetch]; function backfill_pvs_provider_identity [fetch]; function backfill_pvs_system_fields_range [fetch]; function build_console_docs [read]; function build_pvs_fax_html [read]; function create_3008_pvs_july [insert]; function create_3008_pvs_sept [insert]; function create_invoice_from_selection [read]; function dash_metrics [fetch, read]; function dash_metrics_range [fetch, read]; function diag_3008_batch_eligibility [read]; function diag_3008_draft_vs_invoiced [fetch, read]; function diag_3008_duplicates [read]; function diag_august_pvs_gap [read]; function diag_august_pvs_state [fetch]; function diag_billing_preview [fetch, read]; function diag_duplicate_patient_referrals [read]; function diag_duplicate_visits [read]; function diag_fax_coverage [fetch]; function diag_find_patients [read]; function diag_held_pvs [fetch, read]; function diag_invoice_batch [read]; function diag_invoice_pvs [read]; function diag_invoice_same_patient_dos [read]; function diag_match_pvs_by_patient [read]; function diag_month_billing_gap [read]; function diag_mpu_3008_export [read]; function diag_mpu_pvs_export [fetch, read]; function diag_mpu_readiness [fetch]; function diag_patient_visits [read]; function diag_provider_backfill_trace [read]; function diag_pv_missing_proc_div [fetch, read]; function diag_pvs_billing_batch [read]; function diag_pvs_blank_reason [read]; function diag_pvs_by_recid [read]; function diag_pvs_creation_source [fetch]; function diag_pvs_for_refs [read]; function diag_pvs_names [read]; function diag_pvs_note_placement [fetch]; function diag_pvs_one [read]; function diag_pvs_referral_match [read]; function diag_pvs_vs_referral [read]; function diag_ref_patient_pvs_match [read]; function diag_referral_id_records [read]; function diag_sept_pvs_completeness [fetch]; function fill_3008_reason [fetch]; function prepare_month_for_billing [fetch]; function repair_pvs_3008_import [read, update]; function run_invoice_batch [fetch, read]; function run_pvs_exclusion_monitor [read]; function send_activity_digest [fetch, read]; function set_pvs_cancelled_row_status [fetch, read]; function set_pvs_diversion [read]; function set_pvs_procedures [read]; function sync_pvs_from_referral [fetch]; function widget_today_visits [fetch]; page Drilldown_Data [read]; workflow Encounter_PatientVisit/Default_Hide_On_Load [show/hide]; workflow Encounter_PatientVisit/Fax_This_Note_On_Submit [read]; workflow Encounter_PatientVisit/Fax_This_Note_On_Submit1 [read]; workflow Encounter_PatientVisit/Fax_This_Note_Preview_And [read]; workflow Encounter_PatientVisit/Invoice_Status_Lock [show/hide]; workflow Encounter_PatientVisit/PVS_3008_Billing_Stamp [set]; workflow Encounter_PatientVisit/PVS_Required_Fields [read]
- Encounter_PatientVisit.Invoice_Link: function audit_month_integrity [read]; function audit_pvs_billing_readiness [read]; function backfill_pvs_3008_billing [read]; function backfill_pvs_invoice_status [read]; function backfill_pvs_note_placement [read]; function backfill_pvs_premium_fees [read]; function backfill_pvs_referral_id_from_link [read]; function create_invoice_from_selection [read, update]; function dash_metrics [read]; function dash_metrics_range [read]; function diag_3008_batch_eligibility [read]; function diag_3008_draft_vs_invoiced [read]; function diag_3008_duplicates [read]; function diag_billing_preview [read]; function diag_duplicate_patient_referrals [read]; function diag_duplicate_visits [read]; function diag_held_pvs [read]; function diag_invoice_batch [read]; function diag_invoice_patient_gaps [fetch]; function diag_invoice_pvs [fetch]; function diag_invoice_record [fetch]; function diag_invoice_same_patient_dos [fetch]; function diag_missing_dob [fetch]; function diag_month_billing_gap [read]; function diag_patient_visits [read]; function diag_premium_visit_invoices [read]; function diag_pvs_billing_batch [read]; function diag_pvs_billing_flags [read]; function diag_pvs_billing_snapshot [read]; function diag_pvs_premium_mismatches [read]; function diag_pvs_vs_referral [read]; function repair_invoice_pvs_from_referral [fetch]; function repair_pvs_3008_import [read]; function reprice_draft_pvs [read]; function reset_invoice [fetch, update]; function reset_invoice_by_id [fetch, update]; function retire_3008_duplicates_auto [read]; function retire_pvs_duplicate [read]; function retire_pvs_duplicates [read]; function retire_pvs_record [read]; function run_invoice_batch [read]; function set_pvs_hold_batch [read]; function sos_referral_health [fetch]; workflow Encounter_PatientVisit/Default_Hide_On_Load [read]; workflow Encounter_PatientVisit/Invoice_Status_Lock [read]
- Encounter_PatientVisit.Hold_From_Invoicing: function audit_month_integrity [read]; function audit_pvs_billing_readiness [read]; function create_3008_pvs_july [insert]; function create_3008_pvs_sept [insert]; function dash_metrics [read]; function dash_metrics_range [read]; function diag_3008_batch_eligibility [read]; function diag_3008_draft_vs_invoiced [read]; function diag_3008_duplicates [read]; function diag_billing_preview [read]; function diag_find_patients [read]; function diag_held_pvs [fetch]; function diag_invoice_batch [read]; function diag_invoice_same_patient_dos [read]; function diag_month_billing_gap [read]; function diag_patient_visits [read]; function diag_pvs_billing_flags [read]; function retire_3008_duplicates_auto [read, update]; function retire_pvs_duplicate [read, update]; function retire_pvs_duplicates [read, update]; function retire_pvs_record [read, update]; function run_invoice_batch [read]; function set_pvs_hold_batch [read, update]
- Encounter_PatientVisit.Billing_Branch: function api_fax_pvs_search [fetch, read]; function audit_month_integrity [read]; function audit_pvs_billing_readiness [read]; function backfill_partner_resolver [fetch, read, update]; function backfill_pvs_3008_billing [read]; function backfill_pvs_billing_branch [fetch, read, update]; function backfill_pvs_complexity_charge [read]; function backfill_pvs_premium_fees [read]; function build_pvs_fax_html [read]; function create_3008_pvs_july [insert]; function create_3008_pvs_sept [insert]; function create_invoice_from_selection [read]; function diag_3008_batch_eligibility [read]; function diag_3008_draft_vs_invoiced [read]; function diag_3008_duplicates [read]; function diag_august_pvs_state [read]; function diag_billing_preview [read]; function diag_esi_references [fetch]; function diag_fax_readiness [read]; function diag_invoice_batch [read]; function diag_mpu_readiness [read]; function diag_patient_visits [read]; function diag_pvs_billing_batch [read]; function diag_pvs_billing_snapshot [read]; function diag_pvs_billing_vs_referral [fetch, read]; function diag_pvs_fax_number [read]; function diag_pvs_premium_mismatches [read]; function diag_pvs_provider_fields [read]; function diag_pvs_vs_referral [read]; function diag_sept_pvs_completeness [read]; function diag_unfaxed_by_branch [read]; function prepare_month_for_billing [read, update]; function relink_pvs_to_referral [read, update]; function repair_pvs_3008_import [read]; function reprice_draft_pvs [read]; function resolve_pvs_fax_target [read]; function resync_location_labels [read]; function resync_location_names [read]; function run_import_backfills [update]; function run_invoice_batch [fetch]; function send_fax_digest [read]; function send_pvs_fax [read]; function sync_pvs_branch_from_referral [read, update]; workflow Encounter_PatientVisit/Additional_Charges_Show_H1 [read]; workflow Encounter_PatientVisit/Billing_Branch_Required [read]; workflow Encounter_PatientVisit/Branch_Sets_Charge [read, trigger]; workflow Encounter_PatientVisit/Complexity_Charge_Require [read]; workflow Encounter_PatientVisit/Complexity_Sets_Charge [read]; workflow Encounter_PatientVisit/Default_Hide_On_Load [show/hide]; workflow Encounter_PatientVisit/Fax_This_Note_Preview_And [read]; workflow Encounter_PatientVisit/Has_Referral_ID_Show_Hide [set]; workflow Encounter_PatientVisit/PVS_3008_Billing_Stamp [read]; workflow Encounter_PatientVisit/PVS_Sets_Billing_Branch_O [set]; workflow Encounter_PatientVisit/Referral_Sets_Billing_Bra [set]
- Encounter_PatientVisit.Fax_This_Note: workflow Encounter_PatientVisit/Fax_This_Note_On_Submit [read, update]; workflow Encounter_PatientVisit/Fax_This_Note_On_Submit1 [read, update]; workflow Encounter_PatientVisit/Fax_This_Note_Preview_And [set, trigger]
- Encounter_PatientVisit.Fax_Override_Unlock: workflow Encounter_PatientVisit/Fax_This_Note_On_Submit [read, update]; workflow Encounter_PatientVisit/Fax_This_Note_On_Submit1 [read, update]; workflow Encounter_PatientVisit/Fax_This_Note_Preview_And [read]
- Encounter_PatientVisit.Fax_Override_Number: workflow Encounter_PatientVisit/Fax_Override_Number_Forma [set, trigger]; workflow Encounter_PatientVisit/Fax_This_Note_On_Submit [read, update]; workflow Encounter_PatientVisit/Fax_This_Note_On_Submit1 [read, update]; workflow Encounter_PatientVisit/Fax_This_Note_Preview_And [read]
- Encounter_PatientVisit.Fax_Override_Reason: workflow Encounter_PatientVisit/Fax_This_Note_On_Submit [read, update]; workflow Encounter_PatientVisit/Fax_This_Note_On_Submit1 [read, update]; workflow Encounter_PatientVisit/Fax_This_Note_Preview_And [read]
- Encounter_PatientVisit.Print_Preview: workflow Encounter_PatientVisit/Fax_This_Note_On_Submit [update]; workflow Encounter_PatientVisit/Fax_This_Note_On_Submit1 [update]; workflow Encounter_PatientVisit/Fax_This_Note_Preview_And [set]
- Encounter_PatientVisit.Note_Finalized_Time: function backfill_note_finalized_time [fetch, update]; function dash_metrics [read]; function dash_metrics_range [read]; function diag_addendum_restamp [read]; function diag_pvs_added_time_clusters [fetch]; function diag_pvs_note_compare [read]; function send_activity_digest [fetch, read]; workflow Encounter_PatientVisit/Note_Finalized_Stamp [set]
- Encounter_PatientVisit.PVS_ID: function api_fax_pvs_search [read]; function audit_month_integrity [read]; function audit_pvs_billing_readiness [read]; function backfill_note_finalized_time [read]; function backfill_partner_resolver [read]; function backfill_provider_login_email [read]; function backfill_pvs_3008_billing [read]; function backfill_pvs_billing_branch [read]; function backfill_pvs_complexity_charge [fetch, read]; function backfill_pvs_employee_email_alias [read]; function backfill_pvs_employee_link [read]; function backfill_pvs_employee_link_range [read]; function backfill_pvs_ids [read, update]; function backfill_pvs_invoice_status [read]; function backfill_pvs_link_by_cognito [fetch, read]; function backfill_pvs_note_placement [read]; function backfill_pvs_premium_fees [read]; function backfill_pvs_provider_identity [read]; function backfill_pvs_referral_date [fetch, read]; function backfill_pvs_referral_id_from_link [fetch, read]; function backfill_pvs_referral_source [read]; function backfill_pvs_row_status [read]; function backfill_pvs_system_fields_range [read]; function build_console_docs [read]; function build_pvs_fax_html [read]; function create_3008_pvs_july [insert]; function create_3008_pvs_sept [insert]; function create_invoice_from_selection [read]; function diag_3008_batch_eligibility [read]; function diag_3008_draft_vs_invoiced [read]; function diag_3008_duplicates [read]; function diag_3008_link_check [read]; function diag_3008_missing_reason [read]; function diag_addendum_restamp [read]; function diag_august_pvs_gap [read]; function diag_billing_preview [read]; function diag_duplicate_patient_referrals [read]; function diag_duplicate_visits [read]; function diag_fax_pdf_image [read]; function diag_fax_readiness [read]; function diag_fax_target [fetch]; function diag_find_patients [read]; function diag_held_pvs [read]; function diag_import_ref_matches [fetch]; function diag_invoice_patient_gaps [read]; function diag_invoice_pvs [read]; function diag_invoice_record [read]; function diag_invoice_same_patient_dos [read]; function diag_match_pvs_by_patient [read]; function diag_month_billing_gap [read]; function diag_mpu_3008_export [read]; function diag_mpu_pvs_export [read]; function diag_mpu_readiness [read]; function diag_orphaned_records [read]; function diag_patient_visits [read]; function diag_premium_visit_invoices [fetch]; function diag_provider_backfill_trace [fetch]; function diag_pv_missing_proc_div [read]; function diag_pvs_billing_batch [fetch]; function diag_pvs_billing_flags [read]; function diag_pvs_billing_snapshot [read]; function diag_pvs_billing_vs_referral [read]; function diag_pvs_blank_reason [read]; function diag_pvs_by_recid [read]; function diag_pvs_creation_source [read]; function diag_pvs_fax_number [read]; function diag_pvs_field_values [fetch]; function diag_pvs_for_refs [read]; function diag_pvs_hospice_ids [fetch]; function diag_pvs_ids [read]; function diag_pvs_names [fetch]; function diag_pvs_note_compare [fetch]; function diag_pvs_note_placement [read]; function diag_pvs_note_text [fetch]; function diag_pvs_one [fetch]; function diag_pvs_premium_mismatches [read]; function diag_pvs_provider_fields [fetch, read]; function diag_pvs_referral_match [fetch]; function diag_pvs_stamp_gap [read]; function diag_pvs_vs_referral [fetch]; function diag_ref_patient_pvs_match [read]; function diag_referral_id_records [read]; function diag_room_number_gaps [fetch]; function diag_sept_pvs_completeness [read]; function fill_3008_reason [read]; function fix_six_room_numbers [fetch]; function normalize_pvs_phones [read]; function prepare_month_for_billing [read]; function relink_pvs_to_referral [read]; function repair_invoice_pvs_from_referral [read]; function repair_pvs_3008_import [read]; function reprice_draft_pvs [read]; function reset_invoice [read]; function reset_invoice_by_id [read]; function retire_3008_duplicates_auto [read]; function retire_pvs_duplicate [fetch]; function retire_pvs_duplicates [fetch, read]; function retire_pvs_record [fetch]; function run_import_backfills [fetch, update]; function run_invoice_batch [read]; function run_pvs_exclusion_monitor [read]; function send_activity_digest [read]; function send_fax_digest [read]; function send_pvs_fax [read]; function set_pvs_cancelled_row_status [read]; function set_pvs_complexity [fetch]; function set_pvs_diversion [fetch]; function set_pvs_entry_type [fetch]; function set_pvs_equipment_charge [fetch]; function set_pvs_hold_batch [fetch]; function set_pvs_procedures [fetch]; function set_pvs_provider [fetch, read, update]; function set_pvs_referral_link [fetch]; function sync_pvs_branch_from_referral [fetch]; function sync_pvs_from_referral [read]; page Drilldown_Data [read]; workflow Encounter_PatientVisit/Default_Hide_On_Load [show/hide]; workflow Encounter_PatientVisit/Fax_This_Note_Preview_And [read]; workflow Encounter_PatientVisit/Invoice_Status_Lock [read]; workflow Encounter_PatientVisit/PVS_ID_Stamp_Generator [set]
- Encounter_PatientVisit.PVS_Referral_ID: function backfill_pvs_ids [read, update]; function backfill_pvs_referral_id_from_link [update]; function diag_3008_duplicates [read]; function diag_invoice_patient_gaps [read]; function diag_pvs_by_recid [read]; function diag_pvs_for_refs [fetch]; function diag_pvs_ids [read]; function retire_3008_duplicates_auto [read]; function run_import_backfills [update]; function run_invoice_batch [read]; workflow Encounter_PatientVisit/Default_Hide_On_Load [show/hide]; workflow Encounter_PatientVisit/PVS_ID_Stamp_Generator [set]
- Encounter_PatientVisit.Referral_ID: function api_fax_pvs_search [read]; function audit_month_integrity [read]; function audit_pvs_billing_readiness [read]; function backfill_pvs_ids [read]; function backfill_pvs_link_by_cognito [fetch, read]; function backfill_pvs_referral_id_from_link [read, update]; function build_console_docs [read]; function build_pvs_fax_html [read]; function create_3008_pvs_july [insert]; function create_3008_pvs_sept [insert]; function dash_metrics [read]; function dash_metrics_range [fetch]; function diag_3008_draft_vs_invoiced [read]; function diag_3008_duplicates [read]; function diag_3008_link_check [fetch, read]; function diag_3008_missing_reason [read]; function diag_3008_no_pvs_list [read]; function diag_3008_no_pvs_sheet [fetch]; function diag_3008_overdue [read]; function diag_august_pvs_gap [read]; function diag_compliance_gap [read]; function diag_find_patients [read]; function diag_held_pvs [read]; function diag_import_ref_matches [read]; function diag_invoice_patient_gaps [read]; function diag_invoice_pvs [read]; function diag_invoice_same_patient_dos [read]; function diag_match_pvs_by_patient [read]; function diag_month_billing_gap [read]; function diag_mpu_pvs_export [read]; function diag_mpu_readiness [read]; function diag_pv_missing_proc_div [read]; function diag_pvs_billing_batch [read]; function diag_pvs_blank_reason [read]; function diag_pvs_by_recid [read]; function diag_pvs_for_refs [fetch]; function diag_pvs_ids [read]; function diag_pvs_note_text [read]; function diag_pvs_provider_fields [read]; function diag_pvs_referral_match [read]; function diag_pvs_vs_referral [read]; function diag_ref_patient_pvs_match [fetch, read]; function diag_referrals_missing_pvs [fetch]; function link_pvs_to_referral [fetch, read]; function prepare_month_for_billing [read]; function relink_pvs_to_referral [read]; function repair_invoice_pvs_from_referral [read]; function retire_3008_duplicates_auto [read]; function retire_pvs_duplicates [fetch, read]; function run_import_backfills [read, update]; function run_invoice_batch [read]; function run_pvs_exclusion_monitor [read]; function send_activity_digest [read]; function set_pvs_cancelled_row_status [read]; function sync_pvs_from_referral [read, update]; function widget_today_visits [fetch]; page Drilldown_Data [read]; workflow Encounter_PatientVisit/Default_Hide_On_Load [show/hide]; workflow Encounter_PatientVisit/Fax_This_Note_Preview_And [read]; workflow Encounter_PatientVisit/Has_Referral_ID_Show_Hide [set]; workflow Encounter_PatientVisit/PVS_ID_Stamp_Generator [read]; workflow Encounter_PatientVisit/Referral_Link_Pre_Fill [set]
- Encounter_PatientVisit.Referral_ID_Stamp: function backfill_pvs_from_referral [read, update]; function diag_3008_link_check [read]; function diag_compliance_gap [read]; function diag_pvs_by_recid [read]; function diag_pvs_for_refs [fetch]; function run_import_backfills [read, update]; workflow Encounter_PatientVisit/Default_Hide_On_Load [show/hide]; workflow Encounter_PatientVisit/Has_Referral_ID_Show_Hide [set]; workflow Encounter_PatientVisit/Referral_Link_Pre_Fill [set]
- Encounter_PatientVisit.Partner_ID: function audit_month_integrity [read]; function audit_pvs_billing_readiness [read]; function backfill_pvs_from_referral [read, update]; function create_3008_pvs_july [insert]; function create_3008_pvs_sept [insert]; function diag_pvs_vs_referral [read]; function run_import_backfills [read, update]; function sync_pvs_from_referral [read, update]; workflow Encounter_PatientVisit/Default_Hide_On_Load [show/hide]; workflow Encounter_PatientVisit/Has_Referral_ID_Show_Hide [set]; workflow Encounter_PatientVisit/Referral_Link_Pre_Fill [set]
- Encounter_PatientVisit.Partner_ID_Stamp: function backfill_pvs_from_referral [read, update]; function run_import_backfills [read, update]; workflow Encounter_PatientVisit/Default_Hide_On_Load [show/hide]; workflow Encounter_PatientVisit/Has_Referral_ID_Show_Hide [set]; workflow Encounter_PatientVisit/Referral_Link_Pre_Fill [set]
- Encounter_PatientVisit.Employee_Full_Name: function backfill_pvs_provider_identity [read, update]; function create_3008_pvs_july [insert]; function create_3008_pvs_sept [insert]; function dash_metrics [read]; function dash_metrics_range [read]; function diag_provider_backfill_trace [read]; function diag_pv_missing_proc_div [read]; function diag_pvs_provider_fields [read]; function run_import_backfills [update]; function set_pvs_provider [read, update]; page Drilldown_Data [read]; workflow Encounter_PatientVisit/Default_Hide_On_Load [show/hide]; workflow Encounter_PatientVisit/Pre_fills_provider_sectio [set]
- Encounter_PatientVisit.Fax_Status: function api_fax_pvs_search [read]; function api_fax_send_console [update]; function diag_fax_coverage [read]; function diag_fax_readiness [read]; function diag_pvs_note_compare [read]; function diag_unfaxed_by_branch [fetch]; function poll_fax_status [update]; function repair_fax_log_status [update]; function send_fax_digest [read]; function send_pvs_fax [update]; workflow Encounter_PatientVisit/Default_Hide_On_Load [show/hide]; workflow Encounter_PatientVisit/Fax_This_Note_On_Submit [read]; workflow Encounter_PatientVisit/Fax_This_Note_On_Submit1 [read]
- Encounter_PatientVisit.Invoice_Status: function audit_month_integrity [read]; function audit_pvs_billing_readiness [read]; function backfill_pvs_3008_billing [read]; function backfill_pvs_invoice_status [read, update]; function backfill_pvs_note_placement [read]; function backfill_pvs_provider_identity [read]; function create_3008_pvs_july [insert]; function create_3008_pvs_sept [insert]; function create_invoice_from_selection [update]; function diag_3008_batch_eligibility [read]; function diag_3008_draft_vs_invoiced [read]; function diag_3008_duplicates [read]; function diag_august_pvs_state [read]; function diag_billing_preview [fetch]; function diag_invoice_batch [read]; function diag_invoice_pvs [read]; function diag_invoice_record [read]; function diag_patient_visits [read]; function diag_premium_visit_invoices [read]; function diag_provider_backfill_trace [read]; function diag_pvs_billing_batch [read]; function diag_pvs_billing_flags [read]; function diag_pvs_billing_snapshot [read]; function diag_pvs_billing_vs_referral [read]; function diag_pvs_provider_fields [read]; function diag_ref_patient_pvs_match [read]; function diag_referral_id_records [read]; function prepare_month_for_billing [read]; function repair_pvs_3008_import [read, update]; function reprice_draft_pvs [fetch]; function reset_invoice [update]; function reset_invoice_by_id [update]; function retire_3008_duplicates_auto [read]; function retire_pvs_duplicate [read]; function retire_pvs_duplicates [read]; function retire_pvs_record [read]; function run_invoice_batch [fetch]; function set_pvs_complexity [read, update]; function sync_pvs_branch_from_referral [read]; workflow Encounter_PatientVisit/Default_Hide_On_Load [show/hide]; workflow Encounter_PatientVisit/Invoice_Status_Lock [read]; workflow Encounter_PatientVisit/PVS_3008_Billing_Stamp [set]
- Encounter_PatientVisit.QC_Reviewed: function run_pvs_exclusion_monitor [fetch]
- Encounter_PatientVisit.Provider_Login_Email: function backfill_provider_login_email [read, update]; function diag_pvs_provider_fields [read]; function diag_pvs_stamp_gap [read]; function run_import_backfills [update]; function set_pvs_provider [read, update]; report My_PVS_Notes [filter]; workflow Encounter_PatientVisit/Provider_Identity_Stamp [set]; workflow Encounter_PatientVisit/Provider_Login_Stamp_On_S [read, update]
- Encounter_PatientVisit.Employee_Link: function audit_month_integrity [read]; function backfill_pvs_employee_link [read, update]; function backfill_pvs_employee_link_range [fetch, update]; function backfill_pvs_provider_identity [read, update]; function create_3008_pvs_sept [insert]; function diag_mpu_readiness [read]; function diag_pvs_one [read]; function diag_pvs_provider_fields [read]; function run_import_backfills [update]; function set_pvs_provider [read, update]; workflow Encounter_PatientVisit/PVS_System_Fields_Stamp_O [read, update]; workflow Encounter_PatientVisit/Provider_Identity_Stamp [set]; workflow Encounter_PatientVisit/Provider_Login_Stamp_On_S [read, update]
- Encounter_PatientVisit.Row_Status: function audit_month_integrity [read]; function backfill_pvs_row_status [read, update]; function backfill_pvs_system_fields_range [read, update]; function dash_metrics [read]; function dash_metrics_range [read]; function diag_3008_link_check [read]; function diag_3008_overdue [read]; function diag_compliance_gap [read]; function diag_fax_coverage [read]; function diag_find_patients [read]; function diag_held_pvs [read]; function diag_month_billing_gap [read]; function diag_mpu_3008_export [read]; function diag_mpu_pvs_export [read]; function diag_mpu_readiness [read]; function diag_pv_missing_proc_div [read]; function diag_pvs_for_refs [read]; function diag_pvs_one [read]; function diag_pvs_status_mix [read]; function diag_ref_patient_pvs_match [read]; function diag_referrals_missing_pvs [read]; function retire_3008_duplicates_auto [update]; function retire_pvs_duplicate [read, update]; function retire_pvs_duplicates [update]; function retire_pvs_record [read, update]; function run_import_backfills [read, update]; function send_activity_digest [read]; function set_pvs_cancelled_row_status [read, update]; function set_pvs_hold_batch [read]; function sync_pvs_from_referral [read]; function widget_today_visits [read]; workflow Encounter_PatientVisit/PVS_System_Fields_Stamp_O [read, update]
- Encounter_PatientVisit.Duplicate_Of_PVS_ID: function diag_held_pvs [read]; function retire_3008_duplicates_auto [update]; function retire_pvs_duplicate [read, update]; function retire_pvs_duplicates [update]
- Encounter_PatientVisit.Row_Status_Note: function diag_held_pvs [read]; function retire_pvs_duplicate [update]; function retire_pvs_record [update]; function set_pvs_cancelled_row_status [read, update]
- Encounter_PatientVisit.Referral_Date: function audit_month_integrity [read]; function backfill_pvs_referral_date [fetch, read, update]; function backfill_pvs_system_fields_range [read, update]; function diag_mpu_readiness [read]; function diag_pvs_one [read]; function run_import_backfills [read, update]; function sync_pvs_from_referral [read, update]; workflow Encounter_PatientVisit/PVS_System_Fields_Stamp_O [read, update]; workflow Encounter_PatientVisit/Referral_Link_Pre_Fill [set]
- Encounter_PatientVisit.Referral_Source: function backfill_pvs_referral_source [read, update]; function backfill_pvs_system_fields_range [read, update]; function diag_mpu_readiness [read]; function diag_pvs_one [read]; function run_import_backfills [read, update]; function send_activity_digest [read]; workflow Encounter_PatientVisit/PVS_System_Fields_Stamp_O [read, update]; workflow Encounter_PatientVisit/Referral_Link_Pre_Fill [set]
