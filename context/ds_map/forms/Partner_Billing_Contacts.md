# Partner_Billing_Contacts

- Display name: Partner Billing Contacts
- .ds line: 3915
- Fields (excluding sections): 15
- Parent form: -

## Fields

| Link name | Display name | Type | Lookup target |
|---|---|---|---|
| Section | - | section | - |
| Partner_Link | Partner Link | picklist | Partners |
| Partner_Location_Link | Partner Location | picklist | - |
| Partner_Billing_Address | Address | address | - |
| Partner_Billing_POC_First_Name | Partner Billing POC First Name | text | - |
| Partner_Billing_POC_Last_Name | Partner Billing POC Last Name | text | - |
| Partner_Billing_POC_Title | Partner Billing POC Title | text | - |
| Partner_Billing_POC_Email | Partner Billing POC Email | email | - |
| Partner_Billing_POC_Phone | Partner Billing POC Phone | text | - |
| Partner_Billing_POC_Fax | Partner Billing POC Fax | text | - |
| Partner_PVS_Fax | Partner PVS Fax | phonenumber | - |
| Partner_Billing_Invoice_Delivery | Partner Billing Invoice Delivery | radiobuttons | - |
| Partner_PVS_Delivery | Partner PVS Delivery | picklist | - |
| Partner_Billing_POC_Status | Partner Billing POC Status | radiobuttons | - |
| Books_Customer_ID | Books Customer ID | text | - |
| System_Fields_Section | System Fields Section | section | - |
| Partner_Billing_Contact_ID_Stamp | Partner Billing Contact ID Stamp  | text | - |

## Workflows

### Partner_Billing_Contact_B

- Display: Partner Billing Contact Branch Match
- Record event: on add or edit
- Form event: OnValidate
- Status: ENABLED
- .ds line: 32724
- Fields read: Partner_Billing_POC_Fax, Partner_Billing_POC_Phone, Partner_Link, Partner_Location_Link
- Fields set: -
- Fields shown/hidden/enabled/disabled: -
- Functions called: -
- Other forms: fetch Partner_Locations (ID); read Partner_Locations (Partner_Link)

### Partner_Billing_Contact_S

- Display: Partner Billing Contact Stamp Generator
- Record event: on add
- Form event: OnSuccess
- Status: ENABLED
- .ds line: 32131
- Fields read: ID
- Fields set: Partner_Billing_Contact_ID_Stamp
- Fields shown/hidden/enabled/disabled: -
- Functions called: -
- Other forms: -

### Partner_Billing_POC_Fax_F

- Display: Partner Billing POC Fax Format
- Record event: on add or edit
- Form event: OnUserInput of Partner_Billing_POC_Fax
- Status: ENABLED
- .ds line: 32985
- Fields read: -
- Fields set: Partner_Billing_POC_Fax
- Fields shown/hidden/enabled/disabled: -
- Functions called: -
- Other forms: -

### Partner_Billing_POC_Phone

- Display: Partner Billing POC Phone Format
- Record event: on add or edit
- Form event: OnUserInput of Partner_Billing_POC_Phone
- Status: ENABLED
- .ds line: 32951
- Fields read: -
- Fields set: Partner_Billing_POC_Phone
- Fields shown/hidden/enabled/disabled: -
- Functions called: -
- Other forms: -

## Reverse index

Every item that references a field of this form.

- Partner_Billing_Contacts.Partner_Link: function api_fax_recipients [read]; function api_fax_send_console [read]; function resolve_pvs_fax_target [read]; workflow Partner_Billing_Contacts/Partner_Billing_Contact_B [read]
- Partner_Billing_Contacts.Partner_Location_Link: function api_fax_recipients [read]; function api_fax_send_console [read]; function create_books_customers [fetch]; function diag_esi_references [fetch]; function diag_fax_readiness [fetch]; function diag_fax_target [fetch]; function diag_missing_pvs_fax [fetch]; function diag_pvs_email_branches [read]; function diag_pvs_fax_number [fetch]; function diag_unfaxed_by_branch [fetch]; function is_pvs_email_branch [fetch]; function resolve_pvs_fax_target [fetch]; workflow Encounter_PatientVisit/Fax_This_Note_Preview_And [fetch]; workflow Partner_Billing_Contacts/Partner_Billing_Contact_B [read]
- Partner_Billing_Contacts.Partner_Billing_Address: function create_books_customers [read]
- Partner_Billing_Contacts.Partner_Billing_POC_First_Name: function api_fax_recipients [read]; function api_fax_send_console [read]; function create_books_customers [read]; function diag_fax_target [read]; function resolve_pvs_fax_target [read]; workflow Encounter_PatientVisit/Fax_This_Note_Preview_And [read]
- Partner_Billing_Contacts.Partner_Billing_POC_Last_Name: function api_fax_recipients [read]; function api_fax_send_console [read]; function create_books_customers [read]; function diag_fax_target [read]; function resolve_pvs_fax_target [read]; workflow Encounter_PatientVisit/Fax_This_Note_Preview_And [read]
- Partner_Billing_Contacts.Partner_Billing_POC_Title: no references
- Partner_Billing_Contacts.Partner_Billing_POC_Email: function create_books_customers [read]; function diag_pvs_email_branches [read]
- Partner_Billing_Contacts.Partner_Billing_POC_Phone: function create_books_customers [read]; workflow Partner_Billing_Contacts/Partner_Billing_Contact_B [read]; workflow Partner_Billing_Contacts/Partner_Billing_POC_Phone [set, trigger]
- Partner_Billing_Contacts.Partner_Billing_POC_Fax: workflow Partner_Billing_Contacts/Partner_Billing_Contact_B [read]; workflow Partner_Billing_Contacts/Partner_Billing_POC_Fax_F [set, trigger]
- Partner_Billing_Contacts.Partner_PVS_Fax: function api_fax_recipients [read]; function api_fax_send_console [read]; function diag_fax_readiness [read]; function diag_fax_target [read]; function diag_missing_pvs_fax [read]; function diag_pvs_fax_number [read]; function diag_unfaxed_by_branch [read]; function resolve_pvs_fax_target [read]; workflow Encounter_PatientVisit/Fax_This_Note_Preview_And [read]
- Partner_Billing_Contacts.Partner_Billing_Invoice_Delivery: no references
- Partner_Billing_Contacts.Partner_PVS_Delivery: function diag_pvs_email_branches [fetch]; function is_pvs_email_branch [fetch]
- Partner_Billing_Contacts.Partner_Billing_POC_Status: function api_fax_recipients [fetch]; function create_books_customers [fetch]; function diag_fax_readiness [fetch]; function diag_fax_target [fetch]; function diag_missing_pvs_fax [read]; function diag_pvs_email_branches [fetch]; function diag_unfaxed_by_branch [fetch]; function is_pvs_email_branch [fetch]; function resolve_pvs_fax_target [fetch]; workflow Encounter_PatientVisit/Fax_This_Note_Preview_And [fetch]
- Partner_Billing_Contacts.Books_Customer_ID: no references
- Partner_Billing_Contacts.Partner_Billing_Contact_ID_Stamp: workflow Partner_Billing_Contacts/Partner_Billing_Contact_S [set]
