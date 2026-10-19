# Unresolved references

References that could not be matched to a known form, field, function, report or page, plus string-built or dynamic references. None of these are guessed. Location is the item, its .ds start line, and the line within its body.

Total: 63

| Kind | Reference | Location | Body line | Snippet |
|---|---|---|---|---|
| dynamic: invokeUrl | v_url | function admin_set_field (.ds line 8520) | 13 | v_find = invokeurl |
| dynamic: invokeUrl | "https://www.zohoapis.com/creator/v2.1/data" + zoho.appuri + "report/" + p_report + "/" + v_id | function admin_set_field (.ds line 8520) | 49 | v_upd = invokeurl |
| dynamic: invokeUrl | "https://platform.ringcentral.com/restapi/v1.0/account/~/extension/~/fax" | function api_fax_send_console (.ds line 8745) | 177 | v_resp = invokeurl |
| dynamic: invokeUrl | "https://platform.ringcentral.com/restapi/v1.0/account/~/extension/~/fax" | function api_fax_send_console (.ds line 8745) | 211 | v_resp = invokeurl |
| dynamic: invokeUrl | "https://workdrive.zoho.com/api/v1/download/" + v_ResId | function backfill_referral_uploads (.ds line 14141) | 144 | v_File = invokeurl |
| dynamic: invokeUrl | "https://www.zohoapis.com/creator/v2.1/data" + zoho.appuri + "report/Referrals_Main_Report/" + v_Rec | function backfill_referral_uploads (.ds line 14141) | 174 | v_Resp = invokeurl |
| dynamic: invokeUrl | "https://www.zohoapis.com/creator/v2.1/data" + zoho.appuri + "report/Referrals_Main_Report/" + p_rec | function build_creator_attachments (.ds line 14743) | 64 | v_file = invokeurl |
| dynamic: invokeUrl | "https://api.zeptomail.com/v1.1/files?name=" + zoho.encryption.urlEncode(v_name.toString()) | function build_creator_attachments (.ds line 14743) | 73 | v_resp = invokeurl |
| dynamic: invokeUrl | "https://workdrive.zoho.com/api/v1/download/" + v_ResId | function build_zepto_attachments (.ds line 15654) | 29 | v_File = invokeurl |
| dynamic: invokeUrl | "https://api.zeptomail.com/v1.1/files?name=" + zoho.encryption.urlEncode(v_name) | function build_zepto_attachments (.ds line 15654) | 43 | v_resp = invokeurl |
| dynamic: invokeUrl | "https://www.zohoapis.com/books/v3/contacts?organization_id=911048634" | function create_books_customers (.ds line 16235) | 58 | v_resp = invokeurl |
| dynamic: invokeUrl | "https://www.zohoapis.com/books/v3/invoices?organization_id=911048634" | function create_invoice_from_selection (.ds line 16325) | 235 | v_resp = invokeurl |
| dynamic: invokeUrl | "https://platform.ringcentral.com/restapi/v1.0/account/~/extension/~/message-store/" + v_mid | function diag_fax_repair_errors (.ds line 19774) | 16 | v_resp = invokeurl |
| dynamic: invokeUrl | baseUrl + "/forms" | function diag_form_fields (.ds line 19938) | 28 | formsResp = invokeurl |
| dynamic: invokeUrl | baseUrl + "/form/" + p_formLink + "/fields" | function diag_form_fields (.ds line 19938) | 52 | fieldsResp = invokeurl |
| dynamic: invokeUrl | "https://platform.ringcentral.com/restapi/v1.0/account/~/extension/~/message-store?messageType=Fax&d | function diag_rc_fax_history (.ds line 23289) | 19 | v_resp = invokeurl |
| dynamic: invokeUrl | "https://platform.ringcentral.com/restapi/v1.0/account/~/extension/~" | function diag_rc_token (.ds line 23388) | 18 | v_chk = invokeurl |
| dynamic: invokeUrl | "https://platform.ringcentral.com/restapi/v1.0/account/~/extension/~/message-store/" + v_mid | function diag_stuck_faxes (.ds line 24645) | 23 | v_resp = invokeurl |
| dynamic: invokeUrl | "https://workdrive.zoho.com/api/v1/download/" + v_ResId | function diag_upload_probe (.ds line 24960) | 37 | v_File = invokeurl |
| dynamic: invokeUrl | "https://www.zohoapis.com/creator/v2.1/data" + zoho.appuri + "report/Referrals_Main_Report/" + v_Rec | function diag_upload_probe (.ds line 24960) | 47 | v_Resp = invokeurl |
| dynamic: invokeUrl | "https://workdrive.zoho.com/api/v1/download/" + p_resId.trim() | function diag_workdrive_download (.ds line 25026) | 4 | v_resp = invokeurl |
| dynamic: invokeUrl | "https://www.zohoapis.com/creator/v2.1/data" + zoho.appuri + "report/PVS_Report/" + pPvsID.toString( | function get_pvs_fax_files (.ds line 25375) | 79 | v_file = invokeurl |
| dynamic: invokeUrl | "https://platform.ringcentral.com/restapi/oauth/token" | function get_rc_token (.ds line 25479) | 17 | v_resp = invokeurl |
| dynamic: invokeUrl | "https://platform.ringcentral.com/restapi/v1.0/account/~/extension/~/message-store/" + v_row.RC_Mess | function poll_fax_status (.ds line 26013) | 30 | v_resp = invokeurl |
| dynamic: invokeUrl | "https://workdrive.zoho.com/api/v1/download/" + v_ResId | function process_new_referral (.ds line 26363) | 347 | v_File = invokeurl |
| dynamic: invokeUrl | "https://www.zohoapis.com/creator/v2.1/data" + zoho.appuri + "report/Referrals_Main_Report/" + v_Rec | function process_new_referral (.ds line 26363) | 368 | v_UpResp = invokeurl |
| dynamic: invokeUrl | "https://workdrive.zoho.com/api/v1/download/" + v_ResId | function process_new_referral (.ds line 26363) | 381 | v_File2 = invokeurl |
| dynamic: invokeUrl | "https://platform.ringcentral.com/restapi/v1.0/account/~/extension/~/message-store/" + v_mid | function repair_fax_log_status (.ds line 27183) | 30 | v_resp = invokeurl |
| dynamic: invokeUrl | "https://api.zeptomail.com/v1.1/email" | function resend_referral_notifications (.ds line 28085) | 123 | v_resp = invokeurl |
| dynamic: invokeUrl | "https://www.zohoapis.com/books/v3/invoices/" + v_inv.Books_Invoice_ID + "/status/void?organization_ | function reset_invoice (.ds line 28243) | 51 | v_voidResp = invokeurl |
| dynamic: invokeUrl | "https://www.zohoapis.com/books/v3/invoices/" + v_Bid + "/status/void?organization_id=911048634" | function reset_invoice_by_id (.ds line 28325) | 93 | v_VoidResp = invokeurl |
| dynamic: invokeUrl | baseUrl + "/forms" | function run_schema_monitor (.ds line 30517) | 31 | formsResp = invokeurl |
| dynamic: invokeUrl | baseUrl + "/form/" + formLink + "/fields" | function run_schema_monitor (.ds line 30517) | 47 | fieldsResp = invokeurl |
| dynamic: invokeUrl | "https://api.github.com/repos/" + repoOwner + "/" + repoName + "/contents/" + bPath + "?ref=" + bran | function run_schema_monitor (.ds line 30517) | 194 | bGet = invokeurl |
| dynamic: invokeUrl | "https://api.github.com/repos/" + repoOwner + "/" + repoName + "/contents/" + bPath | function run_schema_monitor (.ds line 30517) | 204 | invokeurl |
| dynamic: invokeUrl | "https://api.github.com/repos/" + repoOwner + "/" + repoName + "/contents/" + tPath + "?ref=" + bran | function run_schema_monitor (.ds line 30517) | 386 | tGet = invokeurl |
| dynamic: invokeUrl | "https://api.github.com/repos/" + repoOwner + "/" + repoName + "/contents/" + tPath | function run_schema_monitor (.ds line 30517) | 396 | invokeurl |
| dynamic: invokeUrl | "https://api.github.com/repos/" + repoOwner + "/" + repoName + "/contents/" + cPath + "?ref=" + bran | function run_schema_monitor (.ds line 30517) | 421 | cGet = invokeurl |
| dynamic: invokeUrl | "https://api.github.com/repos/" + repoOwner + "/" + repoName + "/contents/" + cPath | function run_schema_monitor (.ds line 30517) | 431 | cPut = invokeurl |
| dynamic: invokeUrl | baseUrl + "/forms" | function seed_schema_to_github (.ds line 31027) | 31 | formsResp = invokeurl |
| dynamic: invokeUrl | baseUrl + "/form/" + formLink + "/fields" | function seed_schema_to_github (.ds line 31027) | 53 | fieldsResp = invokeurl |
| dynamic: invokeUrl | "https://api.github.com/repos/" + repoOwner + "/" + repoName + "/contents/" + filePath + "?ref=" + b | function seed_schema_to_github (.ds line 31027) | 150 | getResp = invokeurl |
| dynamic: invokeUrl | "https://api.github.com/repos/" + repoOwner + "/" + repoName + "/contents/" + filePath | function seed_schema_to_github (.ds line 31027) | 160 | putResp = invokeurl |
| dynamic: invokeUrl | "https://api.zeptomail.com/v1.1/email" | function send_3008_notification (.ds line 31223) | 68 | v_resp = invokeurl |
| dynamic: invokeUrl | "https://api.zeptomail.com/v1.1/email" | function send_activity_digest (.ds line 31306) | 975 | v_resp = invokeurl |
| dynamic: invokeUrl | "https://api.zeptomail.com/v1.1/email" | function send_assignment_notification (.ds line 32303) | 225 | v_Resp = invokeurl |
| dynamic: invokeUrl | "https://api.zeptomail.com/v1.1/email" | function send_fax_digest (.ds line 32564) | 158 | v_resp = invokeurl |
| dynamic: invokeUrl | "https://api.zeptomail.com/v1.1/email" | function send_imaging_notification (.ds line 32740) | 77 | v_resp = invokeurl |
| dynamic: invokeUrl | "https://platform.ringcentral.com/restapi/v1.0/account/~/extension/~/fax" | function send_pvs_fax (.ds line 32832) | 131 | v_resp = invokeurl |
| dynamic: invokeUrl | "https://platform.ringcentral.com/restapi/v1.0/account/~/extension/~/fax" | function send_pvs_fax (.ds line 32832) | 165 | v_resp = invokeurl |
| dynamic: invokeUrl | "https://api.zeptomail.com/v1.1/email" | function send_referral_confirmation (.ds line 33052) | 71 | v_resp = invokeurl |
| dynamic: invokeUrl | "https://api.zeptomail.com/v1.1/email" | function send_referral_notification (.ds line 33141) | 77 | v_resp = invokeurl |
| dynamic: invokeUrl | "https://api.sendgrid.com/v3/mail/send" | function send_via_sendgrid (.ds line 33233) | 22 | sgResponse = invokeurl |
| dynamic: invokeUrl | "https://api.github.com/repos/" + repoOwner + "/" + repoName + "/contents/" + filePath + "?ref=" + b | function test_github_commit (.ds line 35084) | 11 | getResp = invokeurl |
| dynamic: invokeUrl | "https://api.github.com/repos/" + repoOwner + "/" + repoName + "/contents/" + filePath | function test_github_commit (.ds line 35084) | 21 | putResp = invokeurl |
| dynamic: invokeUrl | "https://www.zohoapis.com/creator/v2.1/meta/sosmmc/sos-referrals-app/form/Partners/fields" | function test_schema_connection (.ds line 35115) | 1 | response = invokeurl |
| thisapp call to unknown function | portal.profileForUser | workflow Employees/Portal_Access_By_Status (.ds line 37636) | 27 | v_Existing = ifnull(thisapp.portal.profileForUser(v_Email),"").toString().trim(); |
| thisapp call to unknown function | portal.assignUserInProfile | workflow Employees/Portal_Access_By_Status (.ds line 37636) | 34 | thisapp.portal.assignUserInProfile(v_Email,v_Target); |
| thisapp call to unknown function | portal.loginUserEmailid | workflow Encounter_PatientVisit/Diag_Session_Identity (.ds line 39167) | 6 | v_portalEmail = thisapp.portal.loginUserEmailid().toString(); |
| thisapp call to unknown function | portal.loginUserName | workflow Encounter_PatientVisit/Diag_Session_Identity (.ds line 39167) | 13 | v_portalName = thisapp.portal.loginUserName().toString(); |
| update target not resolvable to a form | v_T | function run_import_backfills (.ds line 29381) | 617 | update v_T |
| update target not resolvable to a form | v_target | function set_pvs_equipment_charge (.ds line 33746) | 38 | update v_target |
| update target not resolvable to a form | v_target | function set_pvs_equipment_charge (.ds line 33746) | 45 | update v_target |

## By kind

- dynamic: invokeUrl: 56
- thisapp call to unknown function: 4
- update target not resolvable to a form: 3
