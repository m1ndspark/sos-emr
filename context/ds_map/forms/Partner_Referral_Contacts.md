# Partner_Referral_Contacts

- Display name: Partner Referral Contacts
- .ds line: 4770
- Fields (excluding sections): 11
- Parent form: -

## Fields

| Link name | Display name | Type | Lookup target |
|---|---|---|---|
| Section | - | section | - |
| Partner_Link | Partner Lookup | picklist | Partners |
| Partner_Locations_Link | Partner Locations Lookup | picklist | - |
| Partner_POC_Email | Partner POC Email | email | - |
| Partner_POC_First_Name | Partner POC First Name | text | - |
| Partner_POC_Last_Name | Partner POC Last Name | text | - |
| Partner_POC_Title | Partner POC Title | picklist | - |
| Partner_POC_Team | Partner POC Team | text | - |
| Partner_POC_Phone | Partner POC Phone | phonenumber | - |
| Hidden_Items_Section | Hidden Items Section | section | - |
| Partner_Organization | Partner Organization* | text | - |
| Partner_Branch | Partner Branch/Location* | text | - |
| Partner_POC_Name_Title | Partner POC Name & Title* | text | - |

## Workflows

### Partner_POC_Name_Title_Bu

- Display: Partner POC Name Title Builder
- Record event: on add or edit
- Form event: OnValidate
- Status: ENABLED
- .ds line: 39390
- Fields read: Partner_POC_First_Name, Partner_POC_Last_Name, Partner_POC_Title
- Fields set: Partner_POC_Name_Title
- Fields shown/hidden/enabled/disabled: -
- Functions called: -
- Other forms: -

## Reverse index

Every item that references a field of this form.

- Partner_Referral_Contacts.Partner_Link: function get_partner_referral_contact [read]; function process_new_referral [update]; workflow Partner_Referral_Contact_Signup/Signup_Upsert_Referral_Co [insert, update]
- Partner_Referral_Contacts.Partner_Locations_Link: function backfill_referral_branch_from_contact [read]; function diag_ref_branch_candidates [read]; function diag_referral_branch [read]; function diag_referral_contact_match [read]; function get_partner_referral_contact [read]; function process_new_referral [update]; function resolve_branch_id [read]; workflow Partner_Referral_Contact_Signup/Signup_Upsert_Referral_Co [insert, update]; workflow Referrals_Main/Sender_Sets_Branch [read]
- Partner_Referral_Contacts.Partner_POC_Email: function backfill_referral_branch_from_contact [fetch]; function diag_ref_branch_candidates [read]; function diag_referral_branch [fetch]; function diag_referral_contact_match [fetch]; function get_partner_referral_contact [fetch, read]; function process_new_referral [fetch, insert, read]; function resolve_branch_id [fetch, read]; workflow Partner_Referral_Contact_Signup/Signup_Upsert_Referral_Co [fetch, insert]; workflow Referrals_Main/Partner_Contact_Lookup [fetch]; workflow Referrals_Main/Sender_Sets_Branch [fetch]
- Partner_Referral_Contacts.Partner_POC_First_Name: function backfill_contact_name_title [read]; function get_partner_referral_contact [read]; function process_new_referral [insert, update]; workflow Partner_Referral_Contact_Signup/Signup_Upsert_Referral_Co [insert, update]; workflow Partner_Referral_Contacts/Partner_POC_Name_Title_Bu [read]; workflow Referrals_Main/Partner_Contact_Lookup [read]
- Partner_Referral_Contacts.Partner_POC_Last_Name: function backfill_contact_name_title [read]; function get_partner_referral_contact [read]; function process_new_referral [insert, update]; workflow Partner_Referral_Contact_Signup/Signup_Upsert_Referral_Co [insert, update]; workflow Partner_Referral_Contacts/Partner_POC_Name_Title_Bu [read]; workflow Referrals_Main/Partner_Contact_Lookup [read]
- Partner_Referral_Contacts.Partner_POC_Title: function backfill_contact_name_title [read]; function get_partner_referral_contact [read]; function process_new_referral [insert, update]; workflow Partner_Referral_Contact_Signup/Signup_Upsert_Referral_Co [insert, update]; workflow Partner_Referral_Contacts/Partner_POC_Name_Title_Bu [read]; workflow Referrals_Main/Partner_Contact_Lookup [read]
- Partner_Referral_Contacts.Partner_POC_Team: function get_partner_referral_contact [read]; function process_new_referral [insert, update]; workflow Referrals_Main/Partner_Contact_Lookup [read]
- Partner_Referral_Contacts.Partner_POC_Phone: function get_partner_referral_contact [read]; function process_new_referral [insert, update]; workflow Partner_Referral_Contact_Signup/Signup_Upsert_Referral_Co [insert, update]; workflow Referrals_Main/Partner_Contact_Lookup [read]
- Partner_Referral_Contacts.Partner_Organization: function get_partner_referral_contact [read]; function process_new_referral [insert, update]; workflow Partner_Referral_Contact_Signup/Signup_Upsert_Referral_Co [insert, update]
- Partner_Referral_Contacts.Partner_Branch: function get_partner_referral_contact [read]; function process_new_referral [insert, update]; workflow Partner_Referral_Contact_Signup/Signup_Upsert_Referral_Co [insert, update]
- Partner_Referral_Contacts.Partner_POC_Name_Title: function backfill_contact_name_title [update]; function process_new_referral [insert, update]; workflow Partner_Referral_Contact_Signup/Signup_Upsert_Referral_Co [insert, update]; workflow Partner_Referral_Contacts/Partner_POC_Name_Title_Bu [set]
