# ds_map index

- Source: SOS_Referrals_App.ds
- .ds export generated on (from .ds header): 17-Oct-2026 06:46:58
- .ds file modified time: 2026-10-17 13:47:59
- .ds SHA-256: 15a758f65b42e767d2ec2e9ff22aa16d525d50418be65c6674724ec34bffb310
- STATUS: CURRENT

Derived from the .ds. Wins over schema/ when they disagree. Open the .dg or .ds for ground truth before editing.

Relationship columns are regex-derived navigation aids, not an authoritative logic model. Unmatched and dynamic references are listed in unresolved.md and are never guessed.

Files: forms/<Form>.md (fields, workflows, reverse index), functions.md, unresolved.md, changes.md, map.json (diff baseline).

## Counts

| Item | Count |
|---|---|
| Forms | 39 |
| Fields (excluding sections) | 521 |
| Form workflows | 102 |
| Form workflows disabled | 7 |
| Functions | 283 |
| Schedules | 6 |
| Batch workflows | 0 |
| Approval workflows | 0 |
| Reports | 42 |
| Report custom actions | 2 |
| Pages | 7 |

## Forms

| Link name | Display name | Fields | Workflows | Parent form (subform) |
|---|---|---|---|---|
| API_Config | API Config | 7 | 0 | - |
| Assignments | - | 19 | 10 | - |
| Change_Log | Change Log | 8 | 0 | - |
| Dashboard_Range | Dashboard Range | 2 | 1 | - |
| Employees | - | 31 | 7 | - |
| Encounter_ClinicHours | Clinic Hours | 0 | 0 | - |
| Encounter_LabRequest | Lab Request | 0 | 0 | - |
| Encounter_PatientVisit | - | 116 | 32 | - |
| Encounters_PVSAddendum | PVS Addendum | 15 | 0 | - |
| Exam_Catalog | Exam Catalog | 8 | 0 | - |
| Fax_Address_Book | Fax Address Book | 5 | 0 | - |
| Fax_Attachments | Fax Attachments | 6 | 0 | - |
| Fax_Log | Fax Log | 25 | 0 | - |
| ICD10_Codes | ICD-10 Codes | 8 | 0 | - |
| Imaging_Order | Imaging Order | 0 | 0 | - |
| Imaging_Orders | Imaging Orders | 33 | 6 | - |
| Invoice_Batch | Invoice Batch | 10 | 2 | - |
| Invoices | - | 19 | 0 | - |
| MPU_Reporting | MPU Reporting | 0 | 0 | - |
| Messaging_Hub | Messaging Hub | 0 | 0 | - |
| PVS_Fax_Review | PVS Fax Review | 15 | 5 | - |
| Partner_Billing_Contacts | Partner Billing Contacts | 15 | 4 | - |
| Partner_Contracts | Partner Contracts | 8 | 2 | - |
| Partner_Locations | Partner Locations | 9 | 6 | - |
| Partner_Rates | Partner Rates | 9 | 4 | - |
| Partner_Referral_Contact_Lookup | Partner Referral Contact Lookup | 3 | 0 | - |
| Partner_Referral_Contact_Signup | Partner Referral Contact Signup | 7 | 1 | - |
| Partner_Referral_Contacts | Partner Referral Contacts | 11 | 1 | - |
| Partners | - | 12 | 2 | - |
| Procedure_Templates | Procedure Templates | 0 | 0 | - |
| Referral_Categories | Referral Categories | 3 | 0 | - |
| Referral_Files | Referral Files | 5 | 0 | - |
| Referral_Sweep_Log | Referral Sweep Log | 9 | 0 | - |
| Referrals_Main | Referrals Main | 70 | 19 | - |
| Referrals_Main2 | Referrals Main2 | 26 | 0 | - |
| Referrals_Master | Referrals Master | 0 | 0 | - |
| Schema_Snapshot | Schema Snapshot | 3 | 0 | - |
| Sequence_Tracker | Sequence Tracker | 4 | 0 | - |
| Services_Procedures | Services & Procedures | 0 | 0 | - |

Subforms: 0 detected. No subform field type is present in this .ds.

## Form-to-form lookups

- Assignments.Employee_Link -> Employees
- Assignments.Referral_Link -> Referrals_Main
- Encounter_PatientVisit.Billing_Branch -> Partner_Locations
- Encounter_PatientVisit.Employee_Link -> Employees
- Encounter_PatientVisit.Invoice_Link -> Invoices
- Encounter_PatientVisit.Provider_ICD10_Codes_Link -> ICD10_Codes
- Encounter_PatientVisit.Referral_Link -> Referrals_Main
- Encounters_PVSAddendum.Encounter_Link -> Encounter_PatientVisit
- Fax_Attachments.Fax_Log -> Fax_Log
- Fax_Attachments.Source_PVS_Link -> Encounter_PatientVisit
- Fax_Log.Original_Fax_Link -> Fax_Log
- Fax_Log.PVS_Link -> Encounter_PatientVisit
- Fax_Log.Partner_Link -> Partners
- Fax_Log.Partner_Location_Link -> Partner_Locations
- Fax_Log.Referral_Link -> Referrals_Main
- Fax_Log.Sent_By -> Employees
- Imaging_Orders.Exam_Catalog -> Exam_Catalog
- Imaging_Orders.Provider_Signature_Link -> Employees
- Imaging_Orders.Referral_Link -> Referrals_Main
- Invoice_Batch.Invoice_Link -> Invoices
- Invoice_Batch.Partner_Link -> Partners
- Invoices.Partner_Link -> Partners
- Partner_Billing_Contacts.Partner_Link -> Partners
- Partner_Contracts.Partner_Link -> Partners
- Partner_Locations.Partner_Link -> Partners
- Partner_Rates.Partner_Link -> Partners
- Partner_Referral_Contact_Signup.Partner_Link -> Partners
- Partner_Referral_Contacts.Partner_Link -> Partners
- Referral_Files.Referrals_Main -> Referrals_Main
- Referrals_Main.Employee_Link -> Employees
- Referrals_Main.Partner_Branch_Link -> Partner_Locations
- Referrals_Main.Partner_Link -> Partners

## Functions

| Name | Namespace | Returns | Arguments |
|---|---|---|---|
| add_missing_rate_to_uniform_branches | Deluge | string | - |
| admin_set_field | Deluge | map | string p_report, string p_key_field, string p_key_value, string p_field, string p_value, string p_mode |
| api_fax_begin | Deluge | map | - |
| api_fax_pvs_search | Deluge | map | string p_branchId, string p_query, string p_unsentOnly |
| api_fax_recipients | Deluge | map | - |
| api_fax_send_console | Deluge | map | string pLogId, string pContactId, list pPvsIds, string pRemarks |
| assign_direct_partner | Deluge | string | string p_mode, string p_refIds, string p_source |
| assign_partner_branch | Deluge | string | string p_mode, string p_map |
| audit_month_integrity | Deluge | string | string p_mode, date p_from, date p_to |
| audit_pvs_billing_readiness | Deluge | string | string p_mode, date p_from, date p_to |
| backfill_assignment_ids | Deluge | void | - |
| backfill_contact_name_title | Deluge | string | - |
| backfill_current_rate | Deluge | void | - |
| backfill_data_issues | Deluge | string | string p_mode |
| backfill_dm_full_names | Deluge | void | - |
| backfill_employee_ids | Deluge | void | - |
| backfill_employee_initials | Deluge | string | - |
| backfill_employee_name_title | Deluge | string | string pMode |
| backfill_employee_phone_format | Deluge | void | - |
| backfill_location_ids | Deluge | void | - |
| backfill_location_labels | Deluge | string | string p_mode |
| backfill_mint_missing_referral_ids | Deluge | string | string p_mode, string p_scope |
| backfill_note_finalized_time | Deluge | string | bool p_commit |
| backfill_partner_ids | Deluge | void | - |
| backfill_partner_poc_name_title | Deluge | void | - |
| backfill_partner_resolver | Deluge | string | string p_mode, string p_target, int p_from, int p_to |
| backfill_patient_dob | Deluge | string | string p_mode |
| backfill_patient_full_addresses | Deluge | void | - |
| backfill_patient_full_names | Deluge | void | - |
| backfill_provider_login_email | Deluge | string | string pMode |
| backfill_pvs_3008_billing | Deluge | string | string p_mode, date p_from, date p_to |
| backfill_pvs_address_from_referral | Deluge | string | - |
| backfill_pvs_billing_branch | Deluge | map | string p_mode |
| backfill_pvs_complexity_charge | Deluge | string | string p_mode, string p_pvsIds |
| backfill_pvs_employee_email | Deluge | string | - |
| backfill_pvs_employee_email_alias | Deluge | string | string pMode, string pOldEmail, string pNewEmail |
| backfill_pvs_employee_initials | Deluge | string | - |
| backfill_pvs_employee_link | Deluge | string | string pMode |
| backfill_pvs_employee_link_range | Deluge | string | string p_mode, date p_from, date p_to |
| backfill_pvs_from_referral | Deluge | string | - |
| backfill_pvs_ids | Deluge | string | - |
| backfill_pvs_invoice_status | Deluge | string | string p_mode, date p_from, date p_to |
| backfill_pvs_link_by_cognito | Deluge | string | string p_mode, string p_scope |
| backfill_pvs_note_placement | Deluge | string | string p_mode, date p_from, date p_to |
| backfill_pvs_patient_full_address | Deluge | string | - |
| backfill_pvs_premium_fees | Deluge | string | string p_confirm |
| backfill_pvs_provider_identity | Deluge | string | string p_mode, string p_from, string p_to |
| backfill_pvs_referral_date | Deluge | string | string p_mode, string p_pvsKey |
| backfill_pvs_referral_id_from_link | Deluge | string | string p_mode, string p_scope |
| backfill_pvs_referral_source | Deluge | string | string p_mode, int p_limit |
| backfill_pvs_row_status | Deluge | string | string p_mode, int p_limit |
| backfill_pvs_system_fields_range | Deluge | string | string p_mode, date p_from, date p_to |
| backfill_referral_added_time | Deluge | string | - |
| backfill_referral_branch | Deluge | string | - |
| backfill_referral_branch_from_contact | Deluge | string | - |
| backfill_referral_date | Deluge | string | string p_mode |
| backfill_referral_employee_link | Deluge | string | string pMode |
| backfill_referral_id_from_token | Deluge | string | - |
| backfill_referral_id_stamp | Deluge | void | - |
| backfill_referral_ids | Deluge | void | - |
| backfill_referral_partner_fields | Deluge | string | string p_mode |
| backfill_referral_uploads | Deluge | string | string p_mode, string p_refKey |
| build_3008_email_html | Deluge | map | int p_recId |
| build_console_docs | Deluge | map | string pFaxID, string pToName, string pToPartner, string pToFax, string pToAttn, string pRemarks, list pPvsIds, list pUploadNames |
| build_creator_attachments | Deluge | list | int p_recId, string p_token |
| build_imaging_email_html | Deluge | map | int p_recId |
| build_pvs_fax_html | Deluge | string | int pPvsID, string pFaxID, string pToName, string pToPartner, string pToFax, string pToAttn, string pRemarks, list pImageUrls |
| build_pvs_note_html | Deluge | string | map pVals |
| build_referral_confirmation_html | Deluge | map | int p_recId |
| build_referral_email_html | Deluge | map | int p_recId |
| build_zepto_attachments | Deluge | list | int p_refId, string p_token |
| compute_data_issues | Deluge | string | int p_recId |
| create_3008_pvs_july | Deluge | string | string pMode |
| create_3008_pvs_sept | Deluge | string | string pMode |
| create_books_customers | Deluge | string | - |
| create_invoice_from_selection | Deluge | string | list p_pvsIds, string p_replacesInvoice |
| dash_metrics | Deluge | map | date p_monthStart |
| dash_metrics_range | Deluge | map | date p_from, date p_to, string p_mode, string p_key |
| diag_3008_batch_eligibility | Deluge | string | date p_from, date p_to |
| diag_3008_draft_vs_invoiced | Deluge | string | date p_from, date p_to |
| diag_3008_duplicates | Deluge | string | - |
| diag_3008_link_check | Deluge | string | date p_from, date p_to |
| diag_3008_missing_reason | Deluge | string | - |
| diag_3008_no_pvs_list | Deluge | string | - |
| diag_3008_no_pvs_sheet | Deluge | string | date p_from, date p_to |
| diag_3008_overdue | Deluge | string | - |
| diag_accentcare_rates | Deluge | string | - |
| diag_addendum_restamp | Deluge | string | - |
| diag_august_pvs_gap | Deluge | string | - |
| diag_august_pvs_state | Deluge | string | - |
| diag_bad_remarks_faxes | Deluge | string | - |
| diag_billing_preview | Deluge | string | date p_from, date p_to |
| diag_blank_referral_id | Deluge | string | - |
| diag_branch_books_ids | Deluge | string | - |
| diag_compliance_gap | Deluge | string | - |
| diag_config_write | Deluge | string | - |
| diag_dob_coverage | Deluge | string | - |
| diag_duplicate_location_names | Deluge | string | - |
| diag_duplicate_patient_referrals | Deluge | string | date p_from, date p_to |
| diag_duplicate_referral_ids | Deluge | string | - |
| diag_duplicate_visits | Deluge | string | - |
| diag_empath_labels | Deluge | string | - |
| diag_employees | Deluge | string | - |
| diag_esi_references | Deluge | string | - |
| diag_fax_attachments | Deluge | string | - |
| diag_fax_coverage | Deluge | string | - |
| diag_fax_error | Deluge | string | string p_faxId |
| diag_fax_pdf_image | Deluge | string | int pPvsID |
| diag_fax_readiness | Deluge | map | int p_days |
| diag_fax_repair_errors | Deluge | string | - |
| diag_fax_target | Deluge | string | string p_pvsId |
| diag_find_patients | Deluge | string | string p_rows |
| diag_find_referral | Deluge | string | string p_text |
| diag_form_fields | Deluge | string | string p_formLink |
| diag_held_pvs | Deluge | string | date p_from, date p_to |
| diag_imaging_notify_check | Deluge | string | int p_days |
| diag_import_ref_matches | Deluge | string | - |
| diag_innovage_rates | Deluge | string | - |
| diag_invoice_batch | Deluge | string | int p_batchId |
| diag_invoice_patient_gaps | Deluge | string | string p_invoiceNumbers |
| diag_invoice_pvs | Deluge | string | string p_booksInvoiceId |
| diag_invoice_record | Deluge | string | int p_invoiceId |
| diag_invoice_same_patient_dos | Deluge | string | string p_invoiceNumbers |
| diag_map_cognito_refs | Deluge | string | string p_rows |
| diag_match_3008_refs | Deluge | string | string p_rows |
| diag_match_pvs_by_patient | Deluge | string | string p_rows |
| diag_missing_dob | Deluge | string | - |
| diag_missing_pvs_fax | Deluge | map | - |
| diag_month_billing_gap | Deluge | string | int p_year, int p_month |
| diag_mpu_3008_export | Deluge | string | int p_year, int p_month |
| diag_mpu_pvs_export | Deluge | string | int p_year, int p_month |
| diag_mpu_readiness | Deluge | string | int p_year, int p_month, string p_part |
| diag_mpu_referral_export | Deluge | string | int p_year, int p_month, string p_partner |
| diag_orphan_referral | Deluge | string | string p_recId |
| diag_orphaned_records | Deluge | string | - |
| diag_partner_location_labels | Deluge | string | - |
| diag_partner_rates | Deluge | string | - |
| diag_patient_visits | Deluge | string | string pName |
| diag_premium_visit_invoices | Deluge | string | - |
| diag_provider_backfill_trace | Deluge | string | string p_pvs_id |
| diag_pv_missing_proc_div | Deluge | string | date p_from, date p_to |
| diag_pvs_added_time_clusters | Deluge | string | - |
| diag_pvs_billing_batch | Deluge | string | string p_pvsIds |
| diag_pvs_billing_flags | Deluge | string | - |
| diag_pvs_billing_snapshot | Deluge | string | string p_pvsKey |
| diag_pvs_billing_vs_referral | Deluge | string | int p_from, int p_to |
| diag_pvs_blank_reason | Deluge | string | - |
| diag_pvs_by_recid | Deluge | string | string p_ids |
| diag_pvs_creation_source | Deluge | string | int p_year, int p_month |
| diag_pvs_email_branches | Deluge | string | - |
| diag_pvs_fax_number | Deluge | string | int pPvsID |
| diag_pvs_field_values | Deluge | string | string p_pvsId |
| diag_pvs_for_refs | Deluge | string | string p_refIds |
| diag_pvs_hospice_ids | Deluge | string | string p_pvsIds |
| diag_pvs_ids | Deluge | string | - |
| diag_pvs_login_email_gaps | Deluge | string | - |
| diag_pvs_names | Deluge | string | string p_pvsIds |
| diag_pvs_note_compare | Deluge | string | string p_pvsIds |
| diag_pvs_note_placement | Deluge | string | date p_from, date p_to |
| diag_pvs_note_text | Deluge | string | string p_pvsIds, int p_chars |
| diag_pvs_one | Deluge | string | string p_pvsId |
| diag_pvs_premium_mismatches | Deluge | string | - |
| diag_pvs_provider_fields | Deluge | string | string p_pvs_id |
| diag_pvs_reason_by_entry | Deluge | string | - |
| diag_pvs_referral_match | Deluge | string | string p_pvsIds |
| diag_pvs_stamp_gap | Deluge | string | - |
| diag_pvs_status_mix | Deluge | string | - |
| diag_pvs_vs_referral | Deluge | string | string p_pvsIds |
| diag_rc_fax_history | Deluge | string | - |
| diag_rc_token | Deluge | string | - |
| diag_ref_branch_candidates | Deluge | string | string p_refId |
| diag_ref_names | Deluge | string | string p_refIds |
| diag_ref_patient_pvs_match | Deluge | string | string p_refIds |
| diag_referral_branch | Deluge | string | string p_referral_id |
| diag_referral_by_name | Deluge | string | string p_text |
| diag_referral_collision | Deluge | string | date p_date |
| diag_referral_contact_match | Deluge | string | - |
| diag_referral_date_source | Deluge | string | string p_refIds |
| diag_referral_dates | Deluge | string | - |
| diag_referral_dump | Deluge | string | string p_refIds |
| diag_referral_id_records | Deluge | string | string p_refIds |
| diag_referral_ids | Deluge | string | - |
| diag_referral_imaging | Deluge | string | string p_refIds |
| diag_referral_intake | Deluge | string | string p_refKey |
| diag_referral_origin | Deluge | string | - |
| diag_referral_partner_resolve | Deluge | map | string pRefId |
| diag_referrals_missing_pvs | Deluge | string | date p_from, date p_to |
| diag_room_number_gaps | Deluge | string | - |
| diag_safe_test_referrals | Deluge | string | - |
| diag_sept_pvs_completeness | Deluge | map | date p_start, date p_end |
| diag_sequence_trackers | Deluge | string | - |
| diag_stuck_faxes | Deluge | string | - |
| diag_unfaxed_by_branch | Deluge | map | - |
| diag_unmatched_branch_labels | Deluge | string | - |
| diag_unnotified_referrals | Deluge | string | - |
| diag_upload_field_usage | Deluge | string | - |
| diag_upload_field_values | Deluge | string | string p_refKey |
| diag_upload_probe | Deluge | string | string p_refKey |
| diag_workdrive_download | Deluge | string | string p_resId |
| diag_zztest_referrals | Deluge | string | - |
| fill_3008_reason | Deluge | string | string p_mode, date p_from, date p_to |
| fix_accentcare_current_rate | Deluge | string | - |
| fix_six_room_numbers | Deluge | string | - |
| flag_duplicate_referrals | Deluge | string | string p_mode, string p_pairs |
| fmt_phone_display | Deluge | string | string pRaw |
| fmt_referral_source | Deluge | string | string pOrg, string pBranch |
| get_notification_recipients | Deluge | list | string p_type |
| get_partner_referral_contact | Deluge | map | string pPocEmail |
| get_pvs_fax_files | Deluge | map | int pPvsID, list pSelected, bool pAll |
| get_rc_token | Deluge | string | - |
| is_portal_admin | Deluge | bool | - |
| is_pvs_email_branch | Deluge | bool | int pBranchId |
| link_pvs_to_referral | Deluge | string | - |
| log_change | Deluge | void | string source_form, string source_rec_id, string source_display_id, string field_label, string old_val, string new_val, string changed_by |
| mint_assignment_id | Deluge | void | int recId |
| mint_employee_id | Deluge | void | int recId |
| mint_location_id | Deluge | void | int recId |
| mint_partner_id | Deluge | void | int recId |
| mint_referral_id | Deluge | void | int recId |
| normalize_pvs_phones | Deluge | string | string p_confirm |
| parse_patient_dob | Deluge | date | string p_text |
| partner_branch_values | Deluge | map | string pKey |
| poll_fax_status | Deluge | string | - |
| prepare_month_for_billing | Deluge | string | string p_mode, string p_from, string p_to |
| process_new_referral | Deluge | string | string p_refKey, string p_notify |
| relink_pvs_to_referral | Deluge | string | string p_mode |
| repair_fax_log_status | Deluge | string | bool p_commit |
| repair_invoice_pvs_from_referral | Deluge | string | string p_invoiceNumbers, string p_mode |
| repair_pvs_3008_import | Deluge | string | string p_mode |
| replicate_uniform_rates | Deluge | string | - |
| report_partner_rate_coverage | Deluge | string | - |
| reprice_draft_pvs | Deluge | string | string p_branchLabel, string p_confirm |
| resend_referral_notifications | Deluge | string | string p_refKeys, string p_toEmail |
| reset_invoice | Deluge | string | string p_invoiceNumber, string p_confirm |
| reset_invoice_by_id | Deluge | string | string p_mode, int p_invoiceId, string p_confirm |
| resolve_branch_id | Deluge | string | string pCurrentLink, string pContactEmail, string pLabelText, string pOrgText |
| resolve_pvs_fax_target | Deluge | map | int pPvsID |
| resolve_referral_branch_from_text | Deluge | string | - |
| resync_location_labels | Deluge | string | - |
| resync_location_names | Deluge | string | - |
| resync_patient_dob | Deluge | string | string p_mode |
| retire_3008_duplicates_auto | Deluge | string | string p_mode |
| retire_pvs_duplicate | Deluge | string | string p_mode, string p_dupePvsId, string p_keeperPvsId |
| retire_pvs_duplicate_pairs | Deluge | string | string p_mode, string p_pairs |
| retire_pvs_duplicates | Deluge | string | string p_mode, string p_dupePvsIds |
| retire_pvs_record | Deluge | string | string p_mode, string p_pvsId, string p_reason |
| retry_failed_faxes | Deluge | string | - |
| run_import_backfills | Deluge | string | string p_mode, int p_limit |
| run_invoice_batch | Deluge | string | int p_batchId, decimal p_maxTotal |
| run_pvs_exclusion_monitor | Deluge | string | - |
| run_schema_monitor | Deluge | string | - |
| seed_schema_to_github | Deluge | void | - |
| send_3008_notification | Deluge | string | string p_refKey |
| send_activity_digest | Deluge | string | string p_type, string p_from, string p_to |
| send_assignment_notification | Deluge | string | string p_asgKey |
| send_fax_digest | Deluge | string | - |
| send_imaging_notification | Deluge | string | string p_refKey |
| send_pvs_fax | Deluge | map | int pPvsID, string pToName, string pToPartner, string pToFax, string pToAttn, string pRemarks, string pNumberSource, string pOverrideReason, list pImageUrls, list pAttachFiles, int pAttempt, int pOriginalFaxID |
| send_referral_confirmation | Deluge | string | string p_refKey |
| send_referral_notification | Deluge | string | string p_refKey |
| send_via_sendgrid | Deluge | void | string pTo, string pSubject, string pMessage |
| set_current_rate | Deluge | void | int rateId |
| set_partner_poc_name_title | Deluge | void | int recId |
| set_partner_rate_status | Deluge | string | string p_mode, string p_rateType, string p_skipPartners, string p_status |
| set_patient_full_name | Deluge | void | int recId |
| set_pvs_cancelled_row_status | Deluge | string | string p_mode, date p_from, date p_to |
| set_pvs_complexity | Deluge | string | string p_mode, string p_pvsId, string p_level |
| set_pvs_diversion | Deluge | string | string p_mode, date p_from, date p_to, string p_pairs |
| set_pvs_entry_type | Deluge | string | string p_mode, string p_pvsIds, string p_type |
| set_pvs_equipment_charge | Deluge | string | string p_pvsId, string p_amount, string p_details |
| set_pvs_hold_batch | Deluge | string | string p_mode, string p_pvsIds, string p_hold |
| set_pvs_procedures | Deluge | string | string p_mode, date p_from, date p_to, string p_pairs |
| set_pvs_provider | Deluge | string | string p_mode, string p_pvsId, string p_employeeEmail |
| set_pvs_provider_batch | Deluge | string | string p_mode, string p_pvsIds, string p_employeeEmail |
| set_pvs_referral_link | Deluge | string | string p_pvsId, string p_refId, string p_mode |
| sos_referral_health | Deluge | string | string p_mode, string p_scope, int p_limit |
| sweep_unnotified_referrals | Deluge | string | string p_mode, string p_scope, int p_limit |
| sync_pvs_branch_from_referral | Deluge | string | string p_pvsId, string p_mode |
| sync_pvs_from_referral | Deluge | string | string p_mode, date p_from, date p_to |
| test_github_commit | Deluge | void | - |
| test_schema_connection | Deluge | void | - |
| test_smtp | Deluge | string | - |
| widget_today_visits | Deluge | map | - |

## Reports

| Report | Type | Source form | Filter | Custom actions |
|---|---|---|---|---|
| API_Config_Report | list (default) | API_Config | - | - |
| All_Assignments | list (default) | Assignments | - | - |
| All_Employees | list (default) | Employees | - | - |
| All_Files | list (default) | Referral_Files | - | - |
| All_Partner_Billing_Contacts | list (default) | Partner_Billing_Contacts | - | - |
| All_Partners | list (default) | Partners | - | - |
| All_Sequence_Trackers | list (default) | Sequence_Tracker | - | - |
| Change_Log_Report | list (default) | Change_Log | - | - |
| Clinic_Hours_Report | list (default) | Encounter_ClinicHours | - | - |
| Exam_Catalog_Report | list (default) | Exam_Catalog | - | - |
| Fax_Address_Book_Report | list (default) | Fax_Address_Book | - | - |
| Fax_Attachments_Report | list (default) | Fax_Attachments | - | - |
| Fax_Attachments_Report1 | list | Fax_Attachments | - | - |
| Fax_Log1 | list | Fax_Log | - | - |
| Fax_Log_Report | list (default) | Fax_Log | - | - |
| ICD_10_Codes_Report | list (default) | ICD10_Codes | - | - |
| Imaging_Orders_Report | list (default) | Imaging_Orders | - | - |
| Imaging_Request_Report | list (default) | Imaging_Order | - | - |
| Invoice_Batch_Report | list (default) | Invoice_Batch | - | - |
| Invoices_Report | list (default) | Invoices | - | - |
| Lab_Request_Report | list (default) | Encounter_LabRequest | - | - |
| MPU_Export | list | Encounter_PatientVisit | - | - |
| MPU_Export_Referrals | list | Referrals_Main | - | - |
| MPU_Reporting_Report | list (default) | MPU_Reporting | - | - |
| Messaging_Hub_Report | list (default) | Messaging_Hub | - | - |
| My_PVS_Notes | list | Encounter_PatientVisit | [Provider_Login_Email == zoho.loginuserid] | "Fax PVS" -> Fax_PVS_Button |
| PVS_Addendum_Report | list (default) | Encounters_PVSAddendum | - | - |
| PVS_Report | list (default) | Encounter_PatientVisit | - | "Fax PVS" -> Fax_PVS |
| Partner_Contracts_Report | list (default) | Partner_Contracts | - | - |
| Partner_Locations_Report | list (default) | Partner_Locations | - | - |
| Partner_Rates_Report | list (default) | Partner_Rates | - | - |
| Partner_Referral_Contact_Lookup_Report | list (default) | Partner_Referral_Contact_Lookup | - | - |
| Partner_Referral_Contact_Signup_Report | list (default) | Partner_Referral_Contact_Signup | - | - |
| Partner_Referral_Contacts_Report | list (default) | Partner_Referral_Contacts | - | - |
| Procedure_Templates_Report | list (default) | Procedure_Templates | - | - |
| Referral_Categories_Report | list (default) | Referral_Categories | - | - |
| Referral_Sweep_Log_Report | list (default) | Referral_Sweep_Log | - | - |
| Referrals_Main2_Report | list (default) | Referrals_Main2 | - | - |
| Referrals_Main_Report | list (default) | Referrals_Main | - | - |
| Referrals_Master_Report | list (default) | Referrals_Master | - | - |
| Schema_Snapshot_Report | list (default) | Schema_Snapshot | - | - |
| Services_Procedures_Report | list (default) | Services_Procedures | - | - |

### Report custom actions

- My_PVS_Notes "Fax PVS" -> action workflow Fax_PVS_Button (form Encounter_PatientVisit, for each record): calls none; opens Form PVS_Fax_Review
- PVS_Report "Fax PVS" -> action workflow Fax_PVS (form Encounter_PatientVisit, for each record): calls none; opens Form PVS_Fax_Review

## Pages

| Page | Parameters | Source forms | Embeds and links | Functions called |
|---|---|---|---|---|
| Access_Revoked_Page | - | - | - | - |
| Drilldown_Data | string dd_key, string dd_month | Assignments, Encounter_PatientVisit, Referrals_Main | Page Reports | dash_metrics |
| My_Assignments | - | Referrals_Main | Report Referrals_Main_Report | - |
| PVS | - | Encounter_PatientVisit | Report My_PVS_Notes | - |
| Provider_Dashboard | string v_login_email | Encounter_PatientVisit | Report My_PVS_Notes | - |
| Reports | string r_from, string r_mode, string r_to | Encounter_PatientVisit, Referrals_Main | Page Drilldown_Data, Page Reports, Report PVS_Report, Report Referrals_Main_Report | dash_metrics_range |
| User_Lookup | - | Partner_Referral_Contact_Lookup | Form Partner_Referral_Contact_Lookup | - |

## Schedules

| Schedule | Form (criteria) | Start | Frequency | Functions called | Fields touched |
|---|---|---|---|---|---|
| Activity_Digest_Daily_6am | - | 2026-10-03 06:00:00 | daily | send_activity_digest | - |
| Activity_Digest_Weekly_Fr | - | 2026-10-09 06:00:00 | weekly | send_activity_digest | - |
| Fax_Digest_Daily_4am | - | 2026-09-23 04:00:00 | daily | send_fax_digest | - |
| Fax_Poll_Re_arm | Fax_Log [Fax_Status == "Queued"] | after 3 minutes from Last_Polled_Time | - | poll_fax_status | fetch Fax_Log (Fax_Status); read Fax_Log (Last_Polled_Time) |
| Fax_Retry_Sweep | Fax_Log | after 15 minutes from Last_Polled_Time | - | retry_failed_faxes | read Fax_Log (Last_Polled_Time) |
| SOS_Schema_Monitor_Daily_ | - | 2026-07-08 06:00:00 | daily | run_schema_monitor | - |

## Batch and approval workflows

- none present in this .ds
