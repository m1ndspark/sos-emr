# Remit_Intake

- Display name: Remit Intake
- .ds line: 7176
- Fields (excluding sections): 12
- Parent form: -

## Fields

| Link name | Display name | Type | Lookup target |
|---|---|---|---|
| Section | - | section | - |
| Remit_File | Remit File | upload file | - |
| Source_Email_ID | Source Email ID | text | - |
| Received_Time | Received Time | datetime | - |
| Payer_Name | Payer Name | text | - |
| Payment_Reference | Payment Reference | text | - |
| Payment_Date | Payment Date | date | - |
| Payment_Total | Payment Total | USD | - |
| Extracted_Lines | Extracted Lines | textarea | - |
| Proposed_Allocation | Proposed Allocation | textarea | - |
| Remit_Status | Remit Status | picklist | - |
| Books_Payment_IDs | Books Payment IDs | text | - |
| Process_Log | Process Log | textarea | - |

## Workflows

### Remit_Intake_Read

- Display: Remit Intake Read
- Record event: on add
- Form event: OnSuccess
- Status: ENABLED
- .ds line: 43424
- Fields read: ID, Remit_File
- Fields set: -
- Fields shown/hidden/enabled/disabled: -
- Functions called: remit_build_allocation
- Other forms: fetch Remit_Intake (ID); update Remit_Intake (Extracted_Lines, Payer_Name, Payment_Date, Payment_Reference, Payment_Total, Process_Log, Received_Time, Remit_Status); read Remit_Intake (Received_Time)

## Reverse index

Every item that references a field of this form.

- Remit_Intake.Remit_File: workflow Remit_Intake/Remit_Intake_Read [read]
- Remit_Intake.Source_Email_ID: no references
- Remit_Intake.Received_Time: workflow Remit_Intake/Remit_Intake_Read [read, update]
- Remit_Intake.Payer_Name: function remit_build_allocation [read]; workflow Remit_Intake/Remit_Intake_Read [update]
- Remit_Intake.Payment_Reference: function remit_build_allocation [read]; workflow Remit_Intake/Remit_Intake_Read [update]
- Remit_Intake.Payment_Date: function remit_build_allocation [read]; workflow Remit_Intake/Remit_Intake_Read [update]
- Remit_Intake.Payment_Total: function remit_build_allocation [read]; workflow Remit_Intake/Remit_Intake_Read [update]
- Remit_Intake.Extracted_Lines: function remit_build_allocation [read]; workflow Remit_Intake/Remit_Intake_Read [update]
- Remit_Intake.Proposed_Allocation: function remit_build_allocation [update]
- Remit_Intake.Remit_Status: function remit_build_allocation [update]; workflow Remit_Intake/Remit_Intake_Read [update]
- Remit_Intake.Books_Payment_IDs: no references
- Remit_Intake.Process_Log: function remit_build_allocation [read, update]; workflow Remit_Intake/Remit_Intake_Read [update]
