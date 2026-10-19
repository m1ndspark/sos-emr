# Partner_Rates

- Display name: Partner Rates
- .ds line: 4454
- Fields (excluding sections): 9
- Parent form: -

## Fields

| Link name | Display name | Type | Lookup target |
|---|---|---|---|
| Partner_Section | Partner Section | section | - |
| Partner_Link | Partner Link | picklist | Partners |
| Partner_Location_Link | Partner Location Name | picklist | - |
| Partner_Rates_Section | Partner Rates Section | section | - |
| Rate_Category | Rate Category | picklist | - |
| Rate_Type | Rate Type | picklist | - |
| Rate_Amount | Rate Amount | USD | - |
| Partner_Rates_Effective_Date | Partner Rates Effective Date | date | - |
| Current_Rate | Current Rate? | radiobuttons | - |
| Partner_Rate_Status | Partner Rate Status | radiobuttons | - |
| System_Fields_Section | System Fields Section | section | - |
| Partner_Rate_ID_Stamp | Partner Rate ID Stamp | text | - |

## Workflows

### Partner_Rate_Branch_Match

- Display: Partner Rate Branch Match
- Record event: on add or edit
- Form event: OnValidate
- Status: ENABLED
- .ds line: 36268
- Fields read: Partner_Link, Partner_Location_Link
- Fields set: -
- Fields shown/hidden/enabled/disabled: -
- Functions called: -
- Other forms: fetch Partner_Locations (ID); read Partner_Locations (Partner_Link)

### Partner_Rate_Current_Flag

- Display: Partner Rate Current Flag Generator
- Record event: on add or edit
- Form event: OnSuccess
- Status: ENABLED
- .ds line: 36299
- Fields read: ID
- Fields set: -
- Fields shown/hidden/enabled/disabled: -
- Functions called: set_current_rate
- Other forms: -

### Partner_Rate_Partner_Stam

- Display: Partner Rate Partner Stamp Generator
- Record event: on add or edit
- Form event: OnSuccess
- Status: ENABLED
- .ds line: 36256
- Fields read: -
- Fields set: -
- Fields shown/hidden/enabled/disabled: -
- Functions called: -
- Other forms: -

### Partner_Rate_Stamp_Genera1

- Display: Partner Rate Stamp Generator
- Record event: on add
- Form event: OnSuccess
- Status: ENABLED
- .ds line: 35952
- Fields read: ID
- Fields set: Partner_Rate_ID_Stamp
- Fields shown/hidden/enabled/disabled: -
- Functions called: -
- Other forms: -

## Reverse index

Every item that references a field of this form.

- Partner_Rates.Partner_Link: function add_missing_rate_to_uniform_branches [insert]; function replicate_uniform_rates [insert]; function set_current_rate [fetch, read]; function set_partner_rate_status [read]; workflow Partner_Rates/Partner_Rate_Branch_Match [read]
- Partner_Rates.Partner_Location_Link: function add_missing_rate_to_uniform_branches [fetch, insert]; function audit_month_integrity [read]; function audit_pvs_billing_readiness [read]; function backfill_pvs_3008_billing [fetch]; function backfill_pvs_billing_branch [fetch]; function backfill_pvs_complexity_charge [fetch]; function backfill_pvs_premium_fees [fetch]; function create_3008_pvs_july [fetch]; function create_3008_pvs_sept [fetch]; function diag_accentcare_rates [fetch]; function diag_billing_preview [read]; function diag_esi_references [fetch]; function diag_innovage_rates [fetch]; function diag_partner_rates [fetch]; function diag_pvs_billing_snapshot [fetch]; function diag_pvs_premium_mismatches [fetch]; function fix_accentcare_current_rate [read]; function prepare_month_for_billing [fetch]; function repair_pvs_3008_import [fetch]; function replicate_uniform_rates [fetch, insert]; function report_partner_rate_coverage [fetch, read]; function reprice_draft_pvs [fetch]; function run_import_backfills [fetch]; function run_invoice_batch [fetch]; function set_current_rate [fetch, read]; function set_partner_rate_status [read]; function sync_pvs_branch_from_referral [fetch]; workflow Encounter_PatientVisit/Additional_Charges_Show_H1 [fetch]; workflow Encounter_PatientVisit/Branch_Sets_Charge [fetch]; workflow Encounter_PatientVisit/Complexity_Sets_Charge [fetch]; workflow Encounter_PatientVisit/PVS_3008_Billing_Stamp [fetch]; workflow Encounter_PatientVisit/PVS_Sets_Billing_Branch_O [fetch]; workflow Partner_Rates/Partner_Rate_Branch_Match [read]
- Partner_Rates.Rate_Category: function add_missing_rate_to_uniform_branches [insert, read]; function diag_innovage_rates [read]; function replicate_uniform_rates [insert, read]; function report_partner_rate_coverage [read]; function set_current_rate [fetch, read]
- Partner_Rates.Rate_Type: function add_missing_rate_to_uniform_branches [insert, read]; function audit_month_integrity [read]; function audit_pvs_billing_readiness [read]; function backfill_pvs_3008_billing [fetch]; function backfill_pvs_billing_branch [fetch]; function backfill_pvs_complexity_charge [fetch]; function backfill_pvs_premium_fees [fetch]; function create_3008_pvs_july [fetch]; function create_3008_pvs_sept [fetch]; function diag_accentcare_rates [read]; function diag_billing_preview [read]; function diag_innovage_rates [read]; function diag_partner_rates [read]; function diag_pvs_billing_snapshot [fetch]; function diag_pvs_premium_mismatches [fetch]; function prepare_month_for_billing [fetch]; function repair_pvs_3008_import [fetch]; function replicate_uniform_rates [insert, read]; function report_partner_rate_coverage [read]; function reprice_draft_pvs [fetch]; function run_import_backfills [fetch]; function run_invoice_batch [read]; function set_current_rate [fetch, read]; function set_partner_rate_status [fetch]; function sync_pvs_branch_from_referral [fetch]; workflow Encounter_PatientVisit/Additional_Charges_Show_H1 [fetch]; workflow Encounter_PatientVisit/Branch_Sets_Charge [fetch]; workflow Encounter_PatientVisit/Complexity_Sets_Charge [fetch]; workflow Encounter_PatientVisit/PVS_3008_Billing_Stamp [fetch]; workflow Encounter_PatientVisit/PVS_Sets_Billing_Branch_O [fetch]
- Partner_Rates.Rate_Amount: function add_missing_rate_to_uniform_branches [insert, read]; function audit_month_integrity [read]; function audit_pvs_billing_readiness [read]; function backfill_pvs_3008_billing [read]; function backfill_pvs_billing_branch [read]; function backfill_pvs_complexity_charge [read]; function backfill_pvs_premium_fees [read]; function create_3008_pvs_july [read]; function create_3008_pvs_sept [read]; function diag_accentcare_rates [read]; function diag_innovage_rates [read]; function diag_partner_rates [read]; function diag_pvs_billing_snapshot [read]; function diag_pvs_premium_mismatches [read]; function prepare_month_for_billing [read]; function repair_pvs_3008_import [read]; function replicate_uniform_rates [insert, read]; function report_partner_rate_coverage [read]; function reprice_draft_pvs [read]; function run_import_backfills [read]; function set_partner_rate_status [read]; function sync_pvs_branch_from_referral [read]; workflow Encounter_PatientVisit/Additional_Charges_Show_H1 [read]; workflow Encounter_PatientVisit/Branch_Sets_Charge [read]; workflow Encounter_PatientVisit/Complexity_Sets_Charge [read]; workflow Encounter_PatientVisit/PVS_3008_Billing_Stamp [read]; workflow Encounter_PatientVisit/PVS_Sets_Billing_Branch_O [read]
- Partner_Rates.Partner_Rates_Effective_Date: function add_missing_rate_to_uniform_branches [insert, read]; function fix_accentcare_current_rate [read]; function replicate_uniform_rates [insert, read]; function report_partner_rate_coverage [read]; function set_current_rate [read]
- Partner_Rates.Current_Rate: function add_missing_rate_to_uniform_branches [fetch, insert]; function audit_month_integrity [fetch]; function audit_pvs_billing_readiness [fetch]; function backfill_pvs_3008_billing [fetch]; function backfill_pvs_billing_branch [fetch]; function backfill_pvs_complexity_charge [fetch]; function backfill_pvs_premium_fees [fetch]; function create_3008_pvs_july [fetch]; function create_3008_pvs_sept [fetch]; function diag_accentcare_rates [read]; function diag_billing_preview [fetch]; function diag_innovage_rates [read]; function diag_partner_rates [fetch]; function diag_pvs_billing_snapshot [fetch]; function diag_pvs_premium_mismatches [fetch]; function fix_accentcare_current_rate [fetch, update]; function prepare_month_for_billing [fetch]; function repair_pvs_3008_import [fetch]; function replicate_uniform_rates [fetch, insert]; function report_partner_rate_coverage [read]; function reprice_draft_pvs [fetch]; function run_import_backfills [fetch]; function run_invoice_batch [fetch]; function set_current_rate [update]; function set_partner_rate_status [read]; function sync_pvs_branch_from_referral [fetch]; workflow Encounter_PatientVisit/Additional_Charges_Show_H1 [fetch]; workflow Encounter_PatientVisit/Branch_Sets_Charge [fetch]; workflow Encounter_PatientVisit/Complexity_Sets_Charge [fetch]; workflow Encounter_PatientVisit/PVS_3008_Billing_Stamp [fetch]; workflow Encounter_PatientVisit/PVS_Sets_Billing_Branch_O [fetch]
- Partner_Rates.Partner_Rate_Status: function add_missing_rate_to_uniform_branches [insert]; function audit_month_integrity [read]; function diag_accentcare_rates [read]; function diag_billing_preview [read]; function diag_innovage_rates [read]; function fix_accentcare_current_rate [update]; function replicate_uniform_rates [insert]; function report_partner_rate_coverage [read]; function run_invoice_batch [read]; function set_current_rate [fetch]; function set_partner_rate_status [read, update]
- Partner_Rates.Partner_Rate_ID_Stamp: function add_missing_rate_to_uniform_branches [update]; function replicate_uniform_rates [update]; workflow Partner_Rates/Partner_Rate_Stamp_Genera1 [set]
