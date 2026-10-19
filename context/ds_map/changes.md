# ds_map changes

Compared against the map committed at 7ecf9f6 (built from .ds SHA-256 f1f3c3ba9ecc5226c196bef3ee107b16c7185b3cf892856cf905a9d2ddc89919).

## Forms
- no change

## Workflows
- removed: Assignments/Assignment_Status_From_Pr
- modified: Encounter_PatientVisit/PVS_Required_Fields

## Functions
- added: audit_month_integrity
- added: backfill_pvs_employee_link_range
- added: backfill_pvs_system_fields_range
- added: diag_billing_preview
- added: diag_duplicate_patient_referrals
- added: diag_find_patients
- added: diag_held_pvs
- added: diag_import_ref_matches
- added: diag_map_cognito_refs
- added: diag_match_pvs_by_patient
- added: diag_pv_missing_proc_div
- added: diag_pvs_billing_batch
- added: diag_pvs_names
- added: diag_pvs_note_text
- added: diag_pvs_vs_referral
- added: diag_ref_names
- added: fill_3008_reason
- added: retire_pvs_duplicate_pairs
- added: run_import_backfills
- added: set_partner_rate_status
- added: set_pvs_cancelled_row_status
- added: set_pvs_diversion
- added: set_pvs_entry_type
- added: set_pvs_hold_batch
- added: set_pvs_procedures
- added: set_pvs_provider_batch
- added: sync_pvs_from_referral
- modified: create_invoice_from_selection
- modified: diag_match_3008_refs
- modified: run_invoice_batch

## Schedules
- no change

## Report actions
- no change

## Reports
- added: MPU_Export
- added: MPU_Export_Referrals

## Pages
- no change

## Fields
- added: Invoice_Batch.Batch_Reason
- added: Invoice_Batch.Replaces_Invoice_Number
- added: Invoices.Replaces_Invoice_Number
- added: Invoices.Revision_Date
- added: Invoices.Section3

Total changes: 39
