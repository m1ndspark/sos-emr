# Invoices

- Display name: -
- .ds line: 2249
- Fields (excluding sections): 17
- Parent form: -

## Fields

| Link name | Display name | Type | Lookup target |
|---|---|---|---|
| Section | - | section | - |
| Partner_Link | Partner Lookup | picklist | Partners |
| Partner_Location_Link | Partner Location Lookup | picklist | - |
| Invoice_Date | Invoice Date | date | - |
| Service_Date_From | Service Date From | date | - |
| Service_Date_To | Service Date To | date | - |
| Invoice_Total | Invoice Total | USD | - |
| Invoice_Record_Status | Invoice Record Status | radiobuttons | - |
| Visit_Count | Visit Count | text | - |
| Created_By | Created By | text | - |
| Section1 | Section | section | - |
| Books_Customer_ID | Books Customer ID | text | - |
| Books_Invoice_ID | Books Invoice ID | text | - |
| Books_Invoice_Number | Books Invoice Number | text | - |
| Books_Sync_Status | Books Sync Status | radiobuttons | - |
| Books_Sync_Message | Books Sync Message | textarea | - |
| Books_Sync_Timestamp | Books Sync Timestamp | datetime | - |
| Section2 | Section | section | - |
| Invoice_ID | Invoice ID | text | - |
| Invoice_ID_Stamp | Invoice ID Stamp | text | - |

## Workflows

- none
## Reverse index

Every item that references a field of this form.

- Invoices.Partner_Link: function create_invoice_from_selection [insert]
- Invoices.Partner_Location_Link: function create_invoice_from_selection [insert]; function diag_esi_references [fetch]; function reset_invoice_by_id [read]
- Invoices.Invoice_Date: function create_invoice_from_selection [insert]; function diag_invoice_record [read]; function diag_month_billing_gap [fetch, read]
- Invoices.Service_Date_From: function create_invoice_from_selection [insert]; function diag_month_billing_gap [read]
- Invoices.Service_Date_To: function create_invoice_from_selection [insert]; function diag_month_billing_gap [read]
- Invoices.Invoice_Total: function create_invoice_from_selection [insert]; function diag_invoice_pvs [read]; function diag_invoice_record [read]; function diag_month_billing_gap [read]; function reset_invoice_by_id [read]
- Invoices.Invoice_Record_Status: function create_invoice_from_selection [insert, update]; function dash_metrics [fetch]; function dash_metrics_range [fetch]; function diag_duplicate_visits [read]; function diag_invoice_patient_gaps [read]; function diag_invoice_record [read]; function diag_month_billing_gap [read]; function diag_patient_visits [read]; function diag_premium_visit_invoices [read]; function reset_invoice [update]; function reset_invoice_by_id [read, update]
- Invoices.Visit_Count: function create_invoice_from_selection [insert]; function diag_invoice_patient_gaps [read]; function diag_invoice_pvs [read]; function diag_invoice_record [read]; function diag_month_billing_gap [read]; function reset_invoice_by_id [read]
- Invoices.Created_By: function create_invoice_from_selection [insert]
- Invoices.Books_Customer_ID: function create_invoice_from_selection [insert]; function diag_invoice_record [read]
- Invoices.Books_Invoice_ID: function create_invoice_from_selection [update]; function diag_invoice_pvs [fetch]; function diag_invoice_record [read]; function reset_invoice [read]; function reset_invoice_by_id [read]
- Invoices.Books_Invoice_Number: function create_invoice_from_selection [update]; function diag_3008_draft_vs_invoiced [read]; function diag_duplicate_visits [read]; function diag_invoice_patient_gaps [fetch]; function diag_invoice_pvs [read]; function diag_invoice_record [read]; function diag_invoice_same_patient_dos [fetch]; function diag_month_billing_gap [read]; function diag_patient_visits [read]; function diag_premium_visit_invoices [read]; function repair_invoice_pvs_from_referral [fetch]; function reset_invoice [fetch]; function reset_invoice_by_id [read]
- Invoices.Books_Sync_Status: no references
- Invoices.Books_Sync_Message: function create_invoice_from_selection [update]; function diag_invoice_record [read]; function reset_invoice [read, update]; function reset_invoice_by_id [read, update]
- Invoices.Books_Sync_Timestamp: function create_invoice_from_selection [update]; function diag_invoice_record [read]; function reset_invoice [update]; function reset_invoice_by_id [update]
- Invoices.Invoice_ID: no references
- Invoices.Invoice_ID_Stamp: no references
