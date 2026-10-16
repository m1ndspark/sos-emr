# Partners

- Display name: -
- .ds line: 4873
- Fields (excluding sections): 12
- Parent form: -

## Fields

| Link name | Display name | Type | Lookup target |
|---|---|---|---|
| Partner_Details_Section | Partner Details Section | section | - |
| Partner_Type | Partner Type | radiobuttons | - |
| Partner_Legal_Name | Partner Legal Name | text | - |
| Partner_Display_Name | Partner Display Name | text | - |
| Partner_Code | Partner Code | text | - |
| Partner_Phone | Partner Phone | phonenumber | - |
| Partner_Address | Partner Address | address | - |
| Rate_Structure | Rate Structure | radiobuttons | - |
| Partner_Contract_Effective_Date | Partner Contract Effective Date | date | - |
| Partner_Contract_Upload | Partner Contract Upload | upload file | - |
| Partner_Status | Partner Status | radiobuttons | - |
| System_Fields_Section | System Fields Section | section | - |
| Partner_ID | Partner ID | text | - |
| Partner_ID_Stamp | Partner ID Stamp | text | - |

## Workflows

### PAR_ID_Generator

- Display: PAR ID Generator
- Record event: on add
- Form event: OnSuccess
- Status: ENABLED
- .ds line: 32042
- Fields read: ID
- Fields set: -
- Fields shown/hidden/enabled/disabled: -
- Functions called: mint_partner_id
- Other forms: -

### PAR_Required_Code1

- Display: PAR Required Code
- Record event: on add or edit
- Form event: OnValidate
- Status: ENABLED
- .ds line: 32178
- Fields read: ID
- Fields set: Partner_Code
- Fields shown/hidden/enabled/disabled: -
- Functions called: -
- Other forms: fetch Partners (ID, Partner_Code)

## Reverse index

Every item that references a field of this form.

- Partners.Partner_Type: no references
- Partners.Partner_Legal_Name: no references
- Partners.Partner_Display_Name: function add_missing_rate_to_uniform_branches [read]; function api_fax_recipients [read]; function api_fax_send_console [read]; function assign_direct_partner [read]; function assign_partner_branch [read]; function backfill_location_labels [read]; function backfill_pvs_billing_branch [read]; function backfill_referral_branch [read]; function backfill_referral_partner_fields [read]; function dash_metrics [read]; function dash_metrics_range [read]; function diag_duplicate_location_names [read]; function diag_innovage_rates [read]; function diag_partner_location_labels [read]; function diag_referral_dump [read]; function get_partner_referral_contact [read]; function partner_branch_values [read]; function prepare_month_for_billing [read]; function replicate_uniform_rates [read]; function report_partner_rate_coverage [read]; function resolve_pvs_fax_target [read]; workflow Partner_Locations/Location_Label_Generator [read]; workflow Partner_Referral_Contact_Signup/Signup_Upsert_Referral_Co [read]; workflow Referrals_Main/Branch_Sets_Partner [read]
- Partners.Partner_Code: function fix_accentcare_current_rate [read]; function mint_location_id [read]; function mint_partner_id [read]; function report_partner_rate_coverage [read]; workflow Partner_Locations/LOC_Required_Codes [read]; workflow Partners/PAR_Required_Code1 [fetch, set]
- Partners.Partner_Phone: no references
- Partners.Partner_Address: no references
- Partners.Rate_Structure: function add_missing_rate_to_uniform_branches [fetch]; function replicate_uniform_rates [fetch]; function report_partner_rate_coverage [read]
- Partners.Partner_Contract_Effective_Date: no references
- Partners.Partner_Contract_Upload: no references
- Partners.Partner_Status: function add_missing_rate_to_uniform_branches [fetch]; function replicate_uniform_rates [fetch]; function report_partner_rate_coverage [read]
- Partners.Partner_ID: function assign_direct_partner [read]; function assign_partner_branch [read]; function backfill_partner_ids [read]; function backfill_referral_branch [read]; function backfill_referral_partner_fields [read]; function diag_sequence_trackers [read]; function mint_partner_id [read, update]; function partner_branch_values [read]; workflow Referrals_Main/Branch_Sets_Partner [read]; workflow Referrals_Main/Branch_Sets_Partner_Link [read]
- Partners.Partner_ID_Stamp: function mint_partner_id [update]
