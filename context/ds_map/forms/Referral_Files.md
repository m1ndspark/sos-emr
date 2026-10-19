# Referral_Files

- Display name: Referral Files
- .ds line: 5596
- Fields (excluding sections): 5
- Parent form: -

## Fields

| Link name | Display name | Type | Lookup target |
|---|---|---|---|
| Section | - | section | - |
| Form_Token | Form Token | text | - |
| Referrals_Main | Referrals Main | picklist | Referrals_Main |
| File_Category | File Category | picklist | - |
| File_Name | File Name | text | - |
| File_Upload | File Upload | upload file | - |

## Workflows

- none
## Reverse index

Every item that references a field of this form.

- Referral_Files.Form_Token: function process_new_referral [insert]
- Referral_Files.Referrals_Main: function build_3008_email_html [fetch]; function build_imaging_email_html [fetch]; function build_referral_email_html [fetch]; function diag_orphan_referral [fetch]; function diag_orphaned_records [read]; function diag_referral_imaging [fetch]; function diag_safe_test_referrals [fetch]; function process_new_referral [fetch, insert]
- Referral_Files.File_Category: function diag_orphaned_records [read]; function diag_referral_imaging [read]; function process_new_referral [insert]
- Referral_Files.File_Name: function build_3008_email_html [read]; function build_imaging_email_html [read]; function build_referral_email_html [read]; function diag_orphaned_records [read]; function diag_referral_imaging [read]; function process_new_referral [insert]
- Referral_Files.File_Upload: function process_new_referral [insert]
