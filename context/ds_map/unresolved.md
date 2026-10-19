# Unresolved references

References that could not be matched to a known form, field, function, report or page, plus string-built or dynamic references. None of these are guessed. Location is the item, its .ds start line, and the line within its body.

Total: 63

| Kind | Reference | Location | Body line | Snippet |
|---|---|---|---|---|
| dynamic: invokeUrl | v_url | function admin_set_field (.ds line 8824) | 13 | v_find = invokeurl |
| dynamic: invokeUrl | "https://www.zohoapis.com/creator/v2.1/data" + zoho.appuri + "report/" + p_report + "/" + v_id | function admin_set_field (.ds line 8824) | 49 | v_upd = invokeurl |
| dynamic: invokeUrl | "https://platform.ringcentral.com/restapi/v1.0/account/~/extension/~/fax" | function api_fax_send_console (.ds line 9049) | 177 | v_resp = invokeurl |
| dynamic: invokeUrl | "https://platform.ringcentral.com/restapi/v1.0/account/~/extension/~/fax" | function api_fax_send_console (.ds line 9049) | 211 | v_resp = invokeurl |
| dynamic: invokeUrl | "https://workdrive.zoho.com/api/v1/download/" + v_ResId | function backfill_referral_uploads (.ds line 14445) | 144 | v_File = invokeurl |
| dynamic: invokeUrl | "https://www.zohoapis.com/creator/v2.1/data" + zoho.appuri + "report/Referrals_Main_Report/" + v_Rec | function backfill_referral_uploads (.ds line 14445) | 174 | v_Resp = invokeurl |
| dynamic: invokeUrl | "https://www.zohoapis.com/creator/v2.1/data" + zoho.appuri + "report/Referrals_Main_Report/" + p_rec | function build_creator_attachments (.ds line 15047) | 64 | v_file = invokeurl |
| dynamic: invokeUrl | "https://api.zeptomail.com/v1.1/files?name=" + zoho.encryption.urlEncode(v_name.toString()) | function build_creator_attachments (.ds line 15047) | 73 | v_resp = invokeurl |
| dynamic: invokeUrl | "https://workdrive.zoho.com/api/v1/download/" + v_ResId | function build_zepto_attachments (.ds line 15958) | 29 | v_File = invokeurl |
| dynamic: invokeUrl | "https://api.zeptomail.com/v1.1/files?name=" + zoho.encryption.urlEncode(v_name) | function build_zepto_attachments (.ds line 15958) | 43 | v_resp = invokeurl |
| dynamic: invokeUrl | "https://www.zohoapis.com/books/v3/contacts?organization_id=911048634" | function create_books_customers (.ds line 16539) | 58 | v_resp = invokeurl |
| dynamic: invokeUrl | "https://www.zohoapis.com/books/v3/invoices?organization_id=911048634" | function create_invoice_from_selection (.ds line 16629) | 235 | v_resp = invokeurl |
| dynamic: invokeUrl | "https://platform.ringcentral.com/restapi/v1.0/account/~/extension/~/message-store/" + v_mid | function diag_fax_repair_errors (.ds line 20078) | 16 | v_resp = invokeurl |
| dynamic: invokeUrl | baseUrl + "/forms" | function diag_form_fields (.ds line 20242) | 28 | formsResp = invokeurl |
| dynamic: invokeUrl | baseUrl + "/form/" + p_formLink + "/fields" | function diag_form_fields (.ds line 20242) | 52 | fieldsResp = invokeurl |
| dynamic: invokeUrl | "https://platform.ringcentral.com/restapi/v1.0/account/~/extension/~/message-store?messageType=Fax&d | function diag_rc_fax_history (.ds line 23593) | 19 | v_resp = invokeurl |
| dynamic: invokeUrl | "https://platform.ringcentral.com/restapi/v1.0/account/~/extension/~" | function diag_rc_token (.ds line 23692) | 18 | v_chk = invokeurl |
| dynamic: invokeUrl | "https://platform.ringcentral.com/restapi/v1.0/account/~/extension/~/message-store/" + v_mid | function diag_stuck_faxes (.ds line 24949) | 23 | v_resp = invokeurl |
| dynamic: invokeUrl | "https://workdrive.zoho.com/api/v1/download/" + v_ResId | function diag_upload_probe (.ds line 25408) | 37 | v_File = invokeurl |
| dynamic: invokeUrl | "https://www.zohoapis.com/creator/v2.1/data" + zoho.appuri + "report/Referrals_Main_Report/" + v_Rec | function diag_upload_probe (.ds line 25408) | 47 | v_Resp = invokeurl |
| dynamic: invokeUrl | "https://workdrive.zoho.com/api/v1/download/" + p_resId.trim() | function diag_workdrive_download (.ds line 25474) | 4 | v_resp = invokeurl |
| dynamic: invokeUrl | "https://www.zohoapis.com/creator/v2.1/data" + zoho.appuri + "report/PVS_Report/" + pPvsID.toString( | function get_pvs_fax_files (.ds line 25993) | 79 | v_file = invokeurl |
| dynamic: invokeUrl | "https://platform.ringcentral.com/restapi/oauth/token" | function get_rc_token (.ds line 26097) | 17 | v_resp = invokeurl |
| dynamic: invokeUrl | "https://platform.ringcentral.com/restapi/v1.0/account/~/extension/~/message-store/" + v_row.RC_Mess | function poll_fax_status (.ds line 26631) | 30 | v_resp = invokeurl |
| dynamic: invokeUrl | "https://workdrive.zoho.com/api/v1/download/" + v_ResId | function process_new_referral (.ds line 27077) | 347 | v_File = invokeurl |
| dynamic: invokeUrl | "https://www.zohoapis.com/creator/v2.1/data" + zoho.appuri + "report/Referrals_Main_Report/" + v_Rec | function process_new_referral (.ds line 27077) | 368 | v_UpResp = invokeurl |
| dynamic: invokeUrl | "https://workdrive.zoho.com/api/v1/download/" + v_ResId | function process_new_referral (.ds line 27077) | 381 | v_File2 = invokeurl |
| dynamic: invokeUrl | "https://platform.ringcentral.com/restapi/v1.0/account/~/extension/~/message-store/" + v_mid | function repair_fax_log_status (.ds line 27897) | 30 | v_resp = invokeurl |
| dynamic: invokeUrl | "https://api.zeptomail.com/v1.1/email" | function resend_referral_notifications (.ds line 28920) | 123 | v_resp = invokeurl |
| dynamic: invokeUrl | "https://www.zohoapis.com/books/v3/invoices/" + v_inv.Books_Invoice_ID + "/status/void?organization_ | function reset_invoice (.ds line 29078) | 51 | v_voidResp = invokeurl |
| dynamic: invokeUrl | "https://www.zohoapis.com/books/v3/invoices/" + v_Bid + "/status/void?organization_id=911048634" | function reset_invoice_by_id (.ds line 29160) | 93 | v_VoidResp = invokeurl |
| dynamic: invokeUrl | baseUrl + "/forms" | function run_schema_monitor (.ds line 31352) | 31 | formsResp = invokeurl |
| dynamic: invokeUrl | baseUrl + "/form/" + formLink + "/fields" | function run_schema_monitor (.ds line 31352) | 47 | fieldsResp = invokeurl |
| dynamic: invokeUrl | "https://api.github.com/repos/" + repoOwner + "/" + repoName + "/contents/" + bPath + "?ref=" + bran | function run_schema_monitor (.ds line 31352) | 194 | bGet = invokeurl |
| dynamic: invokeUrl | "https://api.github.com/repos/" + repoOwner + "/" + repoName + "/contents/" + bPath | function run_schema_monitor (.ds line 31352) | 204 | invokeurl |
| dynamic: invokeUrl | "https://api.github.com/repos/" + repoOwner + "/" + repoName + "/contents/" + tPath + "?ref=" + bran | function run_schema_monitor (.ds line 31352) | 386 | tGet = invokeurl |
| dynamic: invokeUrl | "https://api.github.com/repos/" + repoOwner + "/" + repoName + "/contents/" + tPath | function run_schema_monitor (.ds line 31352) | 396 | invokeurl |
| dynamic: invokeUrl | "https://api.github.com/repos/" + repoOwner + "/" + repoName + "/contents/" + cPath + "?ref=" + bran | function run_schema_monitor (.ds line 31352) | 421 | cGet = invokeurl |
| dynamic: invokeUrl | "https://api.github.com/repos/" + repoOwner + "/" + repoName + "/contents/" + cPath | function run_schema_monitor (.ds line 31352) | 431 | cPut = invokeurl |
| dynamic: invokeUrl | baseUrl + "/forms" | function seed_schema_to_github (.ds line 31862) | 31 | formsResp = invokeurl |
| dynamic: invokeUrl | baseUrl + "/form/" + formLink + "/fields" | function seed_schema_to_github (.ds line 31862) | 53 | fieldsResp = invokeurl |
| dynamic: invokeUrl | "https://api.github.com/repos/" + repoOwner + "/" + repoName + "/contents/" + filePath + "?ref=" + b | function seed_schema_to_github (.ds line 31862) | 150 | getResp = invokeurl |
| dynamic: invokeUrl | "https://api.github.com/repos/" + repoOwner + "/" + repoName + "/contents/" + filePath | function seed_schema_to_github (.ds line 31862) | 160 | putResp = invokeurl |
| dynamic: invokeUrl | "https://api.zeptomail.com/v1.1/email" | function send_3008_notification (.ds line 32058) | 68 | v_resp = invokeurl |
| dynamic: invokeUrl | "https://api.zeptomail.com/v1.1/email" | function send_activity_digest (.ds line 32141) | 975 | v_resp = invokeurl |
| dynamic: invokeUrl | "https://api.zeptomail.com/v1.1/email" | function send_assignment_notification (.ds line 33138) | 225 | v_Resp = invokeurl |
| dynamic: invokeUrl | "https://api.zeptomail.com/v1.1/email" | function send_fax_digest (.ds line 33399) | 158 | v_resp = invokeurl |
| dynamic: invokeUrl | "https://api.zeptomail.com/v1.1/email" | function send_imaging_notification (.ds line 33575) | 77 | v_resp = invokeurl |
| dynamic: invokeUrl | "https://platform.ringcentral.com/restapi/v1.0/account/~/extension/~/fax" | function send_pvs_fax (.ds line 33667) | 131 | v_resp = invokeurl |
| dynamic: invokeUrl | "https://platform.ringcentral.com/restapi/v1.0/account/~/extension/~/fax" | function send_pvs_fax (.ds line 33667) | 165 | v_resp = invokeurl |
| dynamic: invokeUrl | "https://api.zeptomail.com/v1.1/email" | function send_referral_confirmation (.ds line 33887) | 71 | v_resp = invokeurl |
| dynamic: invokeUrl | "https://api.zeptomail.com/v1.1/email" | function send_referral_notification (.ds line 33976) | 77 | v_resp = invokeurl |
| dynamic: invokeUrl | "https://api.sendgrid.com/v3/mail/send" | function send_via_sendgrid (.ds line 34068) | 22 | sgResponse = invokeurl |
| dynamic: invokeUrl | "https://api.github.com/repos/" + repoOwner + "/" + repoName + "/contents/" + filePath + "?ref=" + b | function test_github_commit (.ds line 35919) | 11 | getResp = invokeurl |
| dynamic: invokeUrl | "https://api.github.com/repos/" + repoOwner + "/" + repoName + "/contents/" + filePath | function test_github_commit (.ds line 35919) | 21 | putResp = invokeurl |
| dynamic: invokeUrl | "https://www.zohoapis.com/creator/v2.1/meta/sosmmc/sos-referrals-app/form/Partners/fields" | function test_schema_connection (.ds line 35950) | 1 | response = invokeurl |
| thisapp call to unknown function | portal.profileForUser | workflow Employees/Portal_Access_By_Status (.ds line 38689) | 27 | v_Existing = ifnull(thisapp.portal.profileForUser(v_Email),"").toString().trim(); |
| thisapp call to unknown function | portal.assignUserInProfile | workflow Employees/Portal_Access_By_Status (.ds line 38689) | 34 | thisapp.portal.assignUserInProfile(v_Email,v_Target); |
| thisapp call to unknown function | portal.loginUserEmailid | workflow Encounter_PatientVisit/Diag_Session_Identity (.ds line 40220) | 6 | v_portalEmail = thisapp.portal.loginUserEmailid().toString(); |
| thisapp call to unknown function | portal.loginUserName | workflow Encounter_PatientVisit/Diag_Session_Identity (.ds line 40220) | 13 | v_portalName = thisapp.portal.loginUserName().toString(); |
| update target not resolvable to a form | v_T | function run_import_backfills (.ds line 30216) | 617 | update v_T |
| update target not resolvable to a form | v_target | function set_pvs_equipment_charge (.ds line 34581) | 38 | update v_target |
| update target not resolvable to a form | v_target | function set_pvs_equipment_charge (.ds line 34581) | 45 | update v_target |

## By kind

- dynamic: invokeUrl: 56
- thisapp call to unknown function: 4
- update target not resolvable to a form: 3
