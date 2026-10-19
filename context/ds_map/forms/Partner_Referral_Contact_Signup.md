# Partner_Referral_Contact_Signup

- Display name: Partner Referral Contact Signup
- .ds line: 4665
- Fields (excluding sections): 7
- Parent form: -

## Fields

| Link name | Display name | Type | Lookup target |
|---|---|---|---|
| Section | - | section | - |
| Partner_POC_First_Name | Partner POC First Name | text | - |
| Partner_POC_Last_Name | Partner POC Last Name | text | - |
| Partner_POC_Title | Partner POC Title | picklist | - |
| Partner_POC_Email | Partner POC Email | email | - |
| Partner_POC_Phone | Partner POC Phone | phonenumber | - |
| Partner_Link | Partner Lookup | picklist | Partners |
| Partner_Location_Link | Partner Location Lookup | picklist | - |

## Workflows

### Signup_Upsert_Referral_Co

- Display: Signup Upsert Referral Contact
- Record event: on add
- Form event: OnSuccess
- Status: ENABLED
- .ds line: 39307
- Fields read: Partner_Link, Partner_Location_Link, Partner_POC_Email, Partner_POC_First_Name, Partner_POC_Last_Name, Partner_POC_Phone, Partner_POC_Title
- Fields set: -
- Fields shown/hidden/enabled/disabled: -
- Functions called: -
- Other forms: fetch Partner_Locations (ID); fetch Partner_Referral_Contacts (Partner_POC_Email); insert Partner_Referral_Contacts (Added_User, Partner_Branch, Partner_Link, Partner_Locations_Link, Partner_Organization, Partner_POC_Email, Partner_POC_First_Name, Partner_POC_Last_Name, Partner_POC_Name_Title, Partner_POC_Phone, Partner_POC_Title); update Partner_Referral_Contacts (Partner_Branch, Partner_Link, Partner_Locations_Link, Partner_Organization, Partner_POC_First_Name, Partner_POC_Last_Name, Partner_POC_Name_Title, Partner_POC_Phone, Partner_POC_Title); read Partner_Locations (ID, Partner_Link, Partner_Location_Name); read Partner_Referral_Contacts (ID); read Partners (Partner_Display_Name)

## Reverse index

Every item that references a field of this form.

- Partner_Referral_Contact_Signup.Partner_POC_First_Name: workflow Partner_Referral_Contact_Signup/Signup_Upsert_Referral_Co [read]
- Partner_Referral_Contact_Signup.Partner_POC_Last_Name: workflow Partner_Referral_Contact_Signup/Signup_Upsert_Referral_Co [read]
- Partner_Referral_Contact_Signup.Partner_POC_Title: workflow Partner_Referral_Contact_Signup/Signup_Upsert_Referral_Co [read]
- Partner_Referral_Contact_Signup.Partner_POC_Email: workflow Partner_Referral_Contact_Signup/Signup_Upsert_Referral_Co [read]
- Partner_Referral_Contact_Signup.Partner_POC_Phone: workflow Partner_Referral_Contact_Signup/Signup_Upsert_Referral_Co [read]
- Partner_Referral_Contact_Signup.Partner_Link: workflow Partner_Referral_Contact_Signup/Signup_Upsert_Referral_Co [read]
- Partner_Referral_Contact_Signup.Partner_Location_Link: workflow Partner_Referral_Contact_Signup/Signup_Upsert_Referral_Co [read]
