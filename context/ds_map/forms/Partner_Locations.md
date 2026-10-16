# Partner_Locations

- Display name: Partner Locations
- .ds line: 4282
- Fields (excluding sections): 9
- Parent form: -

## Fields

| Link name | Display name | Type | Lookup target |
|---|---|---|---|
| Section | - | section | - |
| Partner_Link | Partner Link | picklist | Partners |
| Primary_Office | Primary Office? | radiobuttons | - |
| Partner_Location_Name | Partner Loc Name | text | - |
| Partner_Location_Code | Partner Loc Code | text | - |
| Partner_Location_Status | Partner Loc Status | radiobuttons | - |
| Books_Customer_ID | Books Customer ID | text | - |
| System_Fields_Section | System Fields Section | section | - |
| Partner_Location_ID | Partner Location ID | text | - |
| Partner_Location_ID_Stamp | Partner Location ID Stamp | text | - |
| Partner_Location_Label | Partner Location Label | text | - |

## Workflows

### LOC_ID_Generator

- Display: LOC ID Generator
- Record event: on add
- Form event: OnSuccess
- Status: ENABLED
- .ds line: 32061
- Fields read: ID
- Fields set: -
- Fields shown/hidden/enabled/disabled: -
- Functions called: mint_location_id
- Other forms: -

### LOC_Partner_Lock

- Display: LOC Partner Lock
- Record event: on add or edit
- Form event: OnValidate
- Status: ENABLED
- .ds line: 32217
- Fields read: ID, Partner_Link
- Fields set: -
- Fields shown/hidden/enabled/disabled: -
- Functions called: -
- Other forms: fetch Partner_Locations (ID); read Partner_Locations (Partner_Link)

### LOC_Required_Codes

- Display: LOC Required Codes
- Record event: on add
- Form event: OnValidate
- Status: ENABLED
- .ds line: 32080
- Fields read: Partner_Link, Partner_Location_Code
- Fields set: -
- Fields shown/hidden/enabled/disabled: -
- Functions called: -
- Other forms: fetch Partners (ID); read Partners (Partner_Code)

### Location_Label_Generator

- Display: Location Label Generator
- Record event: on add or edit
- Form event: OnSuccess
- Status: ENABLED
- .ds line: 32687
- Fields read: Partner_Link, Partner_Location_Name
- Fields set: Partner_Location_Label
- Fields shown/hidden/enabled/disabled: -
- Functions called: -
- Other forms: fetch Partners (ID); read Partners (Partner_Display_Name)

### Partner_Location_Primary_

- Display: Partner Location Primary Required
- Record event: on add or edit
- Form event: OnValidate
- Status: DISABLED
- .ds line: 32150
- Fields read: ID, Partner_Link, Primary_Office
- Fields set: -
- Fields shown/hidden/enabled/disabled: -
- Functions called: -
- Other forms: fetch Partner_Locations (ID, Partner_Link, Primary_Office)

### Primary_Office_Auto_Demot

- Display: Primary Office Auto Demote
- Record event: on add or edit
- Form event: OnSuccess
- Status: ENABLED
- .ds line: 32245
- Fields read: ID, Partner_Link, Primary_Office
- Fields set: -
- Fields shown/hidden/enabled/disabled: -
- Functions called: -
- Other forms: fetch Partner_Locations (ID, Partner_Link, Primary_Office); update Partner_Locations (Primary_Office)

## Reverse index

Every item that references a field of this form.

- Partner_Locations.Partner_Link: function add_missing_rate_to_uniform_branches [fetch]; function assign_direct_partner [read]; function assign_partner_branch [read]; function backfill_location_labels [read]; function backfill_pvs_billing_branch [read]; function backfill_referral_branch [read]; function backfill_referral_partner_fields [read]; function create_invoice_from_selection [read]; function diag_duplicate_location_names [read]; function diag_innovage_rates [read]; function diag_partner_location_labels [read]; function fix_accentcare_current_rate [read]; function mint_location_id [read]; function partner_branch_values [read]; function prepare_month_for_billing [read]; function replicate_uniform_rates [fetch]; function report_partner_rate_coverage [read]; workflow Partner_Billing_Contacts/Partner_Billing_Contact_B [read]; workflow Partner_Contracts/Partner_Contract_Branch_M [read]; workflow Partner_Locations/LOC_Partner_Lock [read]; workflow Partner_Locations/LOC_Required_Codes [read]; workflow Partner_Locations/Location_Label_Generator [read]; workflow Partner_Locations/Partner_Location_Primary_ [fetch, read]; workflow Partner_Locations/Primary_Office_Auto_Demot [fetch, read]; workflow Partner_Rates/Partner_Rate_Branch_Match [read]; workflow Partner_Referral_Contact_Signup/Signup_Upsert_Referral_Co [read]; workflow Referrals_Main/Branch_Sets_Partner [read]; workflow Referrals_Main/Branch_Sets_Partner_Link [read]
- Partner_Locations.Primary_Office: workflow Partner_Locations/Partner_Location_Primary_ [fetch, read]; workflow Partner_Locations/Primary_Office_Auto_Demot [fetch, read, update]
- Partner_Locations.Partner_Location_Name: function api_fax_pvs_search [read]; function api_fax_recipients [read]; function api_fax_send_console [read]; function assign_direct_partner [read]; function assign_partner_branch [read]; function backfill_location_labels [read]; function backfill_pvs_billing_branch [fetch, read]; function backfill_referral_branch [read]; function backfill_referral_partner_fields [read]; function create_books_customers [read]; function create_invoice_from_selection [read]; function diag_duplicate_location_names [read]; function diag_empath_labels [read]; function diag_innovage_rates [read]; function diag_missing_pvs_fax [read]; function diag_partner_location_labels [read]; function diag_patient_visits [read]; function diag_ref_branch_candidates [fetch]; function diag_unfaxed_by_branch [read]; function diag_unmatched_branch_labels [read]; function partner_branch_values [read]; function prepare_month_for_billing [read]; function report_partner_rate_coverage [read]; function resolve_branch_id [fetch]; function resync_location_names [read]; workflow Partner_Locations/Location_Label_Generator [read]; workflow Partner_Referral_Contact_Signup/Signup_Upsert_Referral_Co [read]; workflow Referrals_Main/Branch_Sets_Partner [read]
- Partner_Locations.Partner_Location_Code: function diag_empath_labels [read]; function diag_innovage_rates [read]; function fix_accentcare_current_rate [read]; function mint_location_id [read]; function report_partner_rate_coverage [read]; workflow Partner_Locations/LOC_Required_Codes [read]
- Partner_Locations.Partner_Location_Status: function add_missing_rate_to_uniform_branches [fetch]; function assign_direct_partner [fetch]; function assign_partner_branch [fetch]; function create_books_customers [fetch]; function diag_branch_books_ids [read]; function diag_duplicate_location_names [fetch]; function diag_empath_labels [read]; function diag_innovage_rates [read]; function diag_missing_pvs_fax [read]; function diag_partner_location_labels [fetch]; function diag_partner_rates [fetch]; function diag_ref_branch_candidates [read]; function diag_unmatched_branch_labels [fetch]; function replicate_uniform_rates [fetch]; function report_partner_rate_coverage [read]; function resolve_branch_id [fetch]
- Partner_Locations.Books_Customer_ID: function create_books_customers [read, update]; function create_invoice_from_selection [read]; function diag_branch_books_ids [read]; function diag_innovage_rates [read]; function diag_partner_rates [read]; function report_partner_rate_coverage [read]
- Partner_Locations.Partner_Location_ID: function backfill_location_ids [read]; function backfill_partner_resolver [read]; function diag_ref_branch_candidates [read]; function mint_location_id [read, update]; function partner_branch_values [fetch]; function process_new_referral [fetch]; function report_partner_rate_coverage [read]; function resolve_branch_id [fetch, read]; workflow Encounter_PatientVisit/PVS_Sets_Billing_Branch_O [fetch]; workflow Referrals_Main/Referral_Resolves_Partner [fetch]
- Partner_Locations.Partner_Location_ID_Stamp: function mint_location_id [update]
- Partner_Locations.Partner_Location_Label: function add_missing_rate_to_uniform_branches [read]; function assign_direct_partner [fetch, read]; function assign_partner_branch [fetch, read]; function audit_pvs_billing_readiness [read]; function backfill_location_labels [read, update]; function backfill_pvs_3008_billing [read]; function backfill_pvs_billing_branch [read]; function backfill_pvs_complexity_charge [read]; function backfill_pvs_premium_fees [read]; function backfill_referral_branch [read]; function backfill_referral_partner_fields [read]; function build_pvs_fax_html [read]; function create_books_customers [read]; function diag_3008_batch_eligibility [read]; function diag_3008_draft_vs_invoiced [read]; function diag_3008_duplicates [read]; function diag_accentcare_rates [fetch, read]; function diag_august_pvs_state [read]; function diag_branch_books_ids [read]; function diag_empath_labels [read]; function diag_esi_references [read]; function diag_fax_target [read]; function diag_innovage_rates [read]; function diag_missing_pvs_fax [read]; function diag_partner_location_labels [read]; function diag_partner_rates [read]; function diag_patient_visits [read]; function diag_pvs_billing_snapshot [read]; function diag_pvs_billing_vs_referral [read]; function diag_pvs_email_branches [read]; function diag_pvs_premium_mismatches [read]; function diag_pvs_provider_fields [read]; function diag_ref_branch_candidates [fetch, read]; function diag_referral_branch [read]; function diag_referral_dump [read]; function diag_unfaxed_by_branch [fetch, read]; function diag_unmatched_branch_labels [read]; function partner_branch_values [read]; function prepare_month_for_billing [read]; function repair_pvs_3008_import [read]; function replicate_uniform_rates [read]; function report_partner_rate_coverage [read]; function reprice_draft_pvs [read]; function reset_invoice_by_id [read]; function resolve_branch_id [fetch]; function resolve_pvs_fax_target [read]; function resolve_referral_branch_from_text [fetch]; function resync_location_labels [read]; function sync_pvs_branch_from_referral [read]; workflow Encounter_PatientVisit/Complexity_Charge_Require [read]; workflow Encounter_PatientVisit/Complexity_Sets_Charge [read]; workflow Partner_Locations/Location_Label_Generator [set]; workflow Referrals_Main/Branch_Sets_Partner [read]
