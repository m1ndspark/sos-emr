# PVS_Fax_Review

- Display name: PVS Fax Review
- .ds line: 5365
- Fields (excluding sections): 15
- Parent form: -

## Fields

| Link name | Display name | Type | Lookup target |
|---|---|---|---|
| Section | - | section | - |
| PVS_Link | PVS Link | text | - |
| Patient_Display | Patient Display | text | - |
| Patient_Name | Patient Name | text | - |
| Referral_ID | Referral ID | text | - |
| Gate_Message | Gate Message | text | - |
| Note_Preview | Note Preview | richtext | - |
| Destination_Name | Destination Name | text | - |
| Destination_Fax | Destination Fax | text | - |
| Override_Unlock | Override Unlock | checkbox | - |
| Override_Fax | Override Fax | text | - |
| Override_Fax_Confirm | Override Fax Confirm | text | - |
| Override_Reason | Override Reason | textarea | - |
| Cover_Remarks | Cover Remarks | textarea | - |
| Attachments_Select | Attachments Select | list | - |
| Result_Message | Result Message | text | - |

## Workflows

### PVS_Fax_Review_Fax_Now

- Display: PVS Fax Review Fax Now
- Record event: -
- Form event: OnClick (button Fax_Now)
- Status: ENABLED
- .ds line: 39474
- Fields read: Destination_Fax, Destination_Name, Override_Fax, Override_Fax_Confirm, Override_Reason, Override_Unlock, PVS_Link, Patient_Name, Referral_ID
- Fields set: Result_Message
- Fields shown/hidden/enabled/disabled: -
- Functions called: resolve_pvs_fax_target, send_pvs_fax
- Other forms: fetch Encounter_PatientVisit (ID); fetch Referrals_Main (ID); read Encounter_PatientVisit (Clinical_Note_Type, Final_Clinical_Note, Patient_Hospice_ID, Referral_Link, Type_of_Entry, Visit_Status); read Referrals_Main (Patient_Hospice_ID)

### PVS_Fax_Review_Format_Ove

- Display: PVS Fax Review Format Override Fax
- Record event: on add
- Form event: OnUserInput of Override_Fax
- Status: ENABLED
- .ds line: 40132
- Fields read: -
- Fields set: Override_Fax
- Fields shown/hidden/enabled/disabled: -
- Functions called: fmt_phone_display
- Other forms: -

### PVS_Fax_Review_Format_Ove1

- Display: PVS Fax Review Format Override Fax Confirm
- Record event: on add
- Form event: OnUserInput of Override_Fax_Confirm
- Status: ENABLED
- .ds line: 40172
- Fields read: -
- Fields set: Override_Fax_Confirm
- Fields shown/hidden/enabled/disabled: -
- Functions called: fmt_phone_display
- Other forms: -

### PVS_Fax_Review_On_Load

- Display: PVS Fax Review On Load
- Record event: on add
- Form event: OnLoad
- Status: ENABLED
- .ds line: 38695
- Fields read: -
- Fields set: Destination_Fax, Destination_Name, Gate_Message, Note_Preview, Patient_Name, Referral_ID, Result_Message
- Fields shown/hidden/enabled/disabled: Attachments_Select, Cover_Remarks, Override_Fax, Override_Fax_Confirm, Override_Reason, Override_Unlock, PVS_Link, Patient_Display
- Functions called: build_console_docs, resolve_pvs_fax_target
- Other forms: fetch Encounter_PatientVisit (ID); fetch Referrals_Main (ID); read Encounter_PatientVisit (Clinical_Note_File_Upload, PVS_3008_Upload, PVS_File_Upload, Patient_Full_Name_1, Referral_Link); read Referrals_Main (Referral_ID)

### PVS_Fax_Review_Override_U

- Display: PVS Fax Review Override Unlock
- Record event: on add
- Form event: OnUserInput of Override_Unlock
- Status: ENABLED
- .ds line: 39618
- Fields read: Override_Unlock
- Fields set: Override_Fax, Override_Fax_Confirm, Override_Reason, Result_Message
- Fields shown/hidden/enabled/disabled: -
- Functions called: -
- Other forms: -

## Reverse index

Every item that references a field of this form.

- PVS_Fax_Review.PVS_Link: workflow PVS_Fax_Review/PVS_Fax_Review_Fax_Now [read]; workflow PVS_Fax_Review/PVS_Fax_Review_On_Load [show/hide]
- PVS_Fax_Review.Patient_Display: workflow PVS_Fax_Review/PVS_Fax_Review_On_Load [show/hide]
- PVS_Fax_Review.Patient_Name: workflow PVS_Fax_Review/PVS_Fax_Review_Fax_Now [read]; workflow PVS_Fax_Review/PVS_Fax_Review_On_Load [set]
- PVS_Fax_Review.Referral_ID: workflow PVS_Fax_Review/PVS_Fax_Review_Fax_Now [read]; workflow PVS_Fax_Review/PVS_Fax_Review_On_Load [set]
- PVS_Fax_Review.Gate_Message: workflow PVS_Fax_Review/PVS_Fax_Review_On_Load [set]
- PVS_Fax_Review.Note_Preview: workflow PVS_Fax_Review/PVS_Fax_Review_On_Load [set]
- PVS_Fax_Review.Destination_Name: workflow PVS_Fax_Review/PVS_Fax_Review_Fax_Now [read]; workflow PVS_Fax_Review/PVS_Fax_Review_On_Load [set]
- PVS_Fax_Review.Destination_Fax: workflow PVS_Fax_Review/PVS_Fax_Review_Fax_Now [read]; workflow PVS_Fax_Review/PVS_Fax_Review_On_Load [set]
- PVS_Fax_Review.Override_Unlock: workflow PVS_Fax_Review/PVS_Fax_Review_Fax_Now [read]; workflow PVS_Fax_Review/PVS_Fax_Review_On_Load [show/hide]; workflow PVS_Fax_Review/PVS_Fax_Review_Override_U [read, trigger]
- PVS_Fax_Review.Override_Fax: workflow PVS_Fax_Review/PVS_Fax_Review_Fax_Now [read]; workflow PVS_Fax_Review/PVS_Fax_Review_Format_Ove [set, trigger]; workflow PVS_Fax_Review/PVS_Fax_Review_On_Load [show/hide]; workflow PVS_Fax_Review/PVS_Fax_Review_Override_U [set]
- PVS_Fax_Review.Override_Fax_Confirm: workflow PVS_Fax_Review/PVS_Fax_Review_Fax_Now [read]; workflow PVS_Fax_Review/PVS_Fax_Review_Format_Ove1 [set, trigger]; workflow PVS_Fax_Review/PVS_Fax_Review_On_Load [show/hide]; workflow PVS_Fax_Review/PVS_Fax_Review_Override_U [set]
- PVS_Fax_Review.Override_Reason: workflow PVS_Fax_Review/PVS_Fax_Review_Fax_Now [read]; workflow PVS_Fax_Review/PVS_Fax_Review_On_Load [show/hide]; workflow PVS_Fax_Review/PVS_Fax_Review_Override_U [set]
- PVS_Fax_Review.Cover_Remarks: workflow PVS_Fax_Review/PVS_Fax_Review_On_Load [show/hide]
- PVS_Fax_Review.Attachments_Select: workflow PVS_Fax_Review/PVS_Fax_Review_On_Load [show/hide]
- PVS_Fax_Review.Result_Message: workflow PVS_Fax_Review/PVS_Fax_Review_Fax_Now [set]; workflow PVS_Fax_Review/PVS_Fax_Review_On_Load [set]; workflow PVS_Fax_Review/PVS_Fax_Review_Override_U [set]
