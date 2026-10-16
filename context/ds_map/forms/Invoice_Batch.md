# Invoice_Batch

- Display name: Invoice Batch
- .ds line: 2132
- Fields (excluding sections): 8
- Parent form: -

## Fields

| Link name | Display name | Type | Lookup target |
|---|---|---|---|
| Section | - | section | - |
| Partner_Link | Partner Lookup | picklist | Partners |
| Partner_Location_Link | Partner Location Lookup | picklist | - |
| Date_From | Date From | date | - |
| Date_To | Date To | date | - |
| Max_Invoice_Total | Max Invoice Total | decimal | - |
| Batch_Status | Batch Status | radiobuttons | - |
| Result_Message | Result Message | textarea | - |
| Invoice_Link | Invoice Lookup | picklist | Invoices |

## Workflows

### Invoice_Batch_On_Create

- Display: Invoice Batch On Create
- Record event: on add
- Form event: OnSuccess
- Status: ENABLED
- .ds line: 34414
- Fields read: ID, Max_Invoice_Total
- Fields set: -
- Fields shown/hidden/enabled/disabled: -
- Functions called: run_invoice_batch
- Other forms: -

### Invoice_Batch_On_Load_Dis

- Display: Invoice Batch On Load Disable
- Record event: on add or edit
- Form event: OnLoad
- Status: ENABLED
- .ds line: 34393
- Fields read: -
- Fields set: -
- Fields shown/hidden/enabled/disabled: Batch_Status, Invoice_Link, Result_Message
- Functions called: -
- Other forms: -

## Reverse index

Every item that references a field of this form.

- Invoice_Batch.Partner_Link: no references
- Invoice_Batch.Partner_Location_Link: function diag_invoice_batch [read]; function run_invoice_batch [read]
- Invoice_Batch.Date_From: function diag_invoice_batch [read]; function run_invoice_batch [read]
- Invoice_Batch.Date_To: function diag_invoice_batch [read]; function run_invoice_batch [read]
- Invoice_Batch.Max_Invoice_Total: workflow Invoice_Batch/Invoice_Batch_On_Create [read]
- Invoice_Batch.Batch_Status: function run_invoice_batch [update]; workflow Invoice_Batch/Invoice_Batch_On_Load_Dis [show/hide]
- Invoice_Batch.Result_Message: function run_invoice_batch [read, update]; workflow Invoice_Batch/Invoice_Batch_On_Load_Dis [show/hide]
- Invoice_Batch.Invoice_Link: workflow Invoice_Batch/Invoice_Batch_On_Load_Dis [show/hide]
