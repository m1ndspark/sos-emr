# Unresolved references

References that could not be matched to a known form, field, function, report or page, plus string-built or dynamic references. None of these are guessed. Location is the item, its .ds start line, and the line within its body.

Total: 70

| Kind | Reference | Location | Body line | Snippet |
|---|---|---|---|---|
| dynamic: invokeUrl | v_url | function admin_set_field (.ds line 9213) | 13 | v_find = invokeurl |
| dynamic: invokeUrl | "https://www.zohoapis.com/creator/v2.1/data" + zoho.appuri + "report/" + p_report + "/" + v_id | function admin_set_field (.ds line 9213) | 49 | v_upd = invokeurl |
| dynamic: invokeUrl | "https://platform.ringcentral.com/restapi/v1.0/account/~/extension/~/fax" | function api_fax_send_console (.ds line 9438) | 177 | v_resp = invokeurl |
| dynamic: invokeUrl | "https://platform.ringcentral.com/restapi/v1.0/account/~/extension/~/fax" | function api_fax_send_console (.ds line 9438) | 211 | v_resp = invokeurl |
| dynamic: invokeUrl | "https://workdrive.zoho.com/api/v1/download/" + v_ResId | function backfill_referral_uploads (.ds line 14834) | 144 | v_File = invokeurl |
| dynamic: invokeUrl | "https://www.zohoapis.com/creator/v2.1/data" + zoho.appuri + "report/Referrals_Main_Report/" + v_Rec | function backfill_referral_uploads (.ds line 14834) | 174 | v_Resp = invokeurl |
| dynamic: invokeUrl | "https://www.zohoapis.com/creator/v2.1/data" + zoho.appuri + "report/Referrals_Main_Report/" + p_rec | function build_creator_attachments (.ds line 15436) | 64 | v_file = invokeurl |
| dynamic: invokeUrl | "https://api.zeptomail.com/v1.1/files?name=" + zoho.encryption.urlEncode(v_name.toString()) | function build_creator_attachments (.ds line 15436) | 73 | v_resp = invokeurl |
| dynamic: invokeUrl | "https://workdrive.zoho.com/api/v1/download/" + v_ResId | function build_zepto_attachments (.ds line 16347) | 29 | v_File = invokeurl |
| dynamic: invokeUrl | "https://api.zeptomail.com/v1.1/files?name=" + zoho.encryption.urlEncode(v_name) | function build_zepto_attachments (.ds line 16347) | 43 | v_resp = invokeurl |
| dynamic: invokeUrl | "https://www.zohoapis.com/books/v3/contacts?organization_id=911048634" | function create_books_customers (.ds line 17163) | 58 | v_resp = invokeurl |
| dynamic: invokeUrl | "https://www.zohoapis.com/books/v3/invoices?organization_id=911048634" | function create_invoice_from_selection (.ds line 17253) | 235 | v_resp = invokeurl |
| dynamic: invokeUrl | "https://platform.ringcentral.com/restapi/v1.0/account/~/extension/~/message-store/" + v_mid | function diag_fax_repair_errors (.ds line 20702) | 16 | v_resp = invokeurl |
| dynamic: invokeUrl | baseUrl + "/forms" | function diag_form_fields (.ds line 20866) | 28 | formsResp = invokeurl |
| dynamic: invokeUrl | baseUrl + "/form/" + p_formLink + "/fields" | function diag_form_fields (.ds line 20866) | 52 | fieldsResp = invokeurl |
| dynamic: invokeUrl | "https://platform.ringcentral.com/restapi/v1.0/account/~/extension/~/message-store?messageType=Fax&d | function diag_rc_fax_history (.ds line 24217) | 19 | v_resp = invokeurl |
| dynamic: invokeUrl | "https://platform.ringcentral.com/restapi/v1.0/account/~/extension/~" | function diag_rc_token (.ds line 24316) | 18 | v_chk = invokeurl |
| dynamic: invokeUrl | "https://platform.ringcentral.com/restapi/v1.0/account/~/extension/~/message-store/" + v_mid | function diag_stuck_faxes (.ds line 25573) | 23 | v_resp = invokeurl |
| dynamic: invokeUrl | "https://workdrive.zoho.com/api/v1/download/" + v_ResId | function diag_upload_probe (.ds line 26032) | 37 | v_File = invokeurl |
| dynamic: invokeUrl | "https://www.zohoapis.com/creator/v2.1/data" + zoho.appuri + "report/Referrals_Main_Report/" + v_Rec | function diag_upload_probe (.ds line 26032) | 47 | v_Resp = invokeurl |
| dynamic: invokeUrl | "https://workdrive.zoho.com/api/v1/download/" + p_resId.trim() | function diag_workdrive_download (.ds line 26098) | 4 | v_resp = invokeurl |
| dynamic: invokeUrl | "https://www.zohoapis.com/creator/v2.1/data" + zoho.appuri + "report/PVS_Report/" + pPvsID.toString( | function get_pvs_fax_files (.ds line 26617) | 79 | v_file = invokeurl |
| dynamic: invokeUrl | "https://platform.ringcentral.com/restapi/oauth/token" | function get_rc_token (.ds line 26721) | 17 | v_resp = invokeurl |
| dynamic: invokeUrl | "https://platform.ringcentral.com/restapi/v1.0/account/~/extension/~/message-store/" + v_row.RC_Mess | function poll_fax_status (.ds line 27255) | 30 | v_resp = invokeurl |
| dynamic: invokeUrl | "https://workdrive.zoho.com/api/v1/download/" + v_ResId | function process_new_referral (.ds line 27701) | 347 | v_File = invokeurl |
| dynamic: invokeUrl | "https://www.zohoapis.com/creator/v2.1/data" + zoho.appuri + "report/Referrals_Main_Report/" + v_Rec | function process_new_referral (.ds line 27701) | 368 | v_UpResp = invokeurl |
| dynamic: invokeUrl | "https://workdrive.zoho.com/api/v1/download/" + v_ResId | function process_new_referral (.ds line 27701) | 381 | v_File2 = invokeurl |
| dynamic: invokeUrl | v_base + "customerpayments?organization_id=" + v_org + "&reference_number=" + zoho.encryption.urlEnc | function remit_build_allocation (.ds line 28521) | 16 | v_pr = invokeurl |
| dynamic: invokeUrl | v_base + "invoices?organization_id=" + v_org + "&invoice_number=" + zoho.encryption.urlEncode(v_num) | function remit_build_allocation (.ds line 28521) | 56 | v_ir = invokeurl |
| dynamic: invokeUrl | v_base + "invoices?organization_id=" + v_org + "&customer_id=" + v_cid + "&filter_by=Status.Unpaid&s | function remit_build_allocation (.ds line 28521) | 130 | v_or = invokeurl |
| dynamic: invokeUrl | "https://api.zeptomail.com/v1.1/email" | function remit_build_allocation (.ds line 28521) | 322 | v_resp = invokeurl |
| dynamic: invokeUrl | "https://platform.ringcentral.com/restapi/v1.0/account/~/extension/~/message-store/" + v_mid | function repair_fax_log_status (.ds line 28868) | 30 | v_resp = invokeurl |
| dynamic: invokeUrl | "https://api.zeptomail.com/v1.1/email" | function resend_referral_notifications (.ds line 29891) | 123 | v_resp = invokeurl |
| dynamic: invokeUrl | "https://www.zohoapis.com/books/v3/invoices/" + v_inv.Books_Invoice_ID + "/status/void?organization_ | function reset_invoice (.ds line 30049) | 51 | v_voidResp = invokeurl |
| dynamic: invokeUrl | "https://www.zohoapis.com/books/v3/invoices/" + v_Bid + "/status/void?organization_id=911048634" | function reset_invoice_by_id (.ds line 30131) | 93 | v_VoidResp = invokeurl |
| dynamic: invokeUrl | baseUrl + "/forms" | function run_schema_monitor (.ds line 32323) | 31 | formsResp = invokeurl |
| dynamic: invokeUrl | baseUrl + "/form/" + formLink + "/fields" | function run_schema_monitor (.ds line 32323) | 47 | fieldsResp = invokeurl |
| dynamic: invokeUrl | "https://api.github.com/repos/" + repoOwner + "/" + repoName + "/contents/" + bPath + "?ref=" + bran | function run_schema_monitor (.ds line 32323) | 194 | bGet = invokeurl |
| dynamic: invokeUrl | "https://api.github.com/repos/" + repoOwner + "/" + repoName + "/contents/" + bPath | function run_schema_monitor (.ds line 32323) | 204 | invokeurl |
| dynamic: invokeUrl | "https://api.github.com/repos/" + repoOwner + "/" + repoName + "/contents/" + tPath + "?ref=" + bran | function run_schema_monitor (.ds line 32323) | 386 | tGet = invokeurl |
| dynamic: invokeUrl | "https://api.github.com/repos/" + repoOwner + "/" + repoName + "/contents/" + tPath | function run_schema_monitor (.ds line 32323) | 396 | invokeurl |
| dynamic: invokeUrl | "https://api.github.com/repos/" + repoOwner + "/" + repoName + "/contents/" + cPath + "?ref=" + bran | function run_schema_monitor (.ds line 32323) | 421 | cGet = invokeurl |
| dynamic: invokeUrl | "https://api.github.com/repos/" + repoOwner + "/" + repoName + "/contents/" + cPath | function run_schema_monitor (.ds line 32323) | 431 | cPut = invokeurl |
| dynamic: invokeUrl | baseUrl + "/forms" | function seed_schema_to_github (.ds line 32833) | 31 | formsResp = invokeurl |
| dynamic: invokeUrl | baseUrl + "/form/" + formLink + "/fields" | function seed_schema_to_github (.ds line 32833) | 53 | fieldsResp = invokeurl |
| dynamic: invokeUrl | "https://api.github.com/repos/" + repoOwner + "/" + repoName + "/contents/" + filePath + "?ref=" + b | function seed_schema_to_github (.ds line 32833) | 150 | getResp = invokeurl |
| dynamic: invokeUrl | "https://api.github.com/repos/" + repoOwner + "/" + repoName + "/contents/" + filePath | function seed_schema_to_github (.ds line 32833) | 160 | putResp = invokeurl |
| dynamic: invokeUrl | "https://api.zeptomail.com/v1.1/email" | function send_3008_notification (.ds line 33029) | 68 | v_resp = invokeurl |
| dynamic: invokeUrl | "https://workdrive.zoho.com/api/v1/download/oizckb2ee8535c42c4b609ea87fc165baa36d" | function send_3008_status (.ds line 33112) | 394 | v_tpl = invokeurl |
| dynamic: invokeUrl | "https://api.zeptomail.com/v1.1/files?name=" + zoho.encryption.urlEncode(v_attName) | function send_3008_status (.ds line 33112) | 403 | v_up = invokeurl |
| dynamic: invokeUrl | "https://api.zeptomail.com/v1.1/email" | function send_3008_status (.ds line 33112) | 461 | v_resp = invokeurl |
| dynamic: invokeUrl | "https://api.zeptomail.com/v1.1/email" | function send_activity_digest (.ds line 33627) | 975 | v_resp = invokeurl |
| dynamic: invokeUrl | "https://api.zeptomail.com/v1.1/email" | function send_assignment_notification (.ds line 34624) | 225 | v_Resp = invokeurl |
| dynamic: invokeUrl | "https://api.zeptomail.com/v1.1/email" | function send_fax_digest (.ds line 34885) | 158 | v_resp = invokeurl |
| dynamic: invokeUrl | "https://api.zeptomail.com/v1.1/email" | function send_imaging_notification (.ds line 35061) | 77 | v_resp = invokeurl |
| dynamic: invokeUrl | "https://platform.ringcentral.com/restapi/v1.0/account/~/extension/~/fax" | function send_pvs_fax (.ds line 35153) | 131 | v_resp = invokeurl |
| dynamic: invokeUrl | "https://platform.ringcentral.com/restapi/v1.0/account/~/extension/~/fax" | function send_pvs_fax (.ds line 35153) | 165 | v_resp = invokeurl |
| dynamic: invokeUrl | "https://api.zeptomail.com/v1.1/email" | function send_referral_confirmation (.ds line 35373) | 71 | v_resp = invokeurl |
| dynamic: invokeUrl | "https://api.zeptomail.com/v1.1/email" | function send_referral_notification (.ds line 35462) | 77 | v_resp = invokeurl |
| dynamic: invokeUrl | "https://api.sendgrid.com/v3/mail/send" | function send_via_sendgrid (.ds line 35554) | 22 | sgResponse = invokeurl |
| dynamic: invokeUrl | "https://api.github.com/repos/" + repoOwner + "/" + repoName + "/contents/" + filePath + "?ref=" + b | function test_github_commit (.ds line 37614) | 11 | getResp = invokeurl |
| dynamic: invokeUrl | "https://api.github.com/repos/" + repoOwner + "/" + repoName + "/contents/" + filePath | function test_github_commit (.ds line 37614) | 21 | putResp = invokeurl |
| dynamic: invokeUrl | "https://www.zohoapis.com/creator/v2.1/meta/sosmmc/sos-referrals-app/form/Partners/fields" | function test_schema_connection (.ds line 37645) | 1 | response = invokeurl |
| thisapp call to unknown function | portal.profileForUser | workflow Employees/Portal_Access_By_Status (.ds line 40384) | 27 | v_Existing = ifnull(thisapp.portal.profileForUser(v_Email),"").toString().trim(); |
| thisapp call to unknown function | portal.assignUserInProfile | workflow Employees/Portal_Access_By_Status (.ds line 40384) | 34 | thisapp.portal.assignUserInProfile(v_Email,v_Target); |
| thisapp call to unknown function | portal.loginUserEmailid | workflow Encounter_PatientVisit/Diag_Session_Identity (.ds line 41915) | 6 | v_portalEmail = thisapp.portal.loginUserEmailid().toString(); |
| thisapp call to unknown function | portal.loginUserName | workflow Encounter_PatientVisit/Diag_Session_Identity (.ds line 41915) | 13 | v_portalName = thisapp.portal.loginUserName().toString(); |
| update target not resolvable to a form | v_T | function run_import_backfills (.ds line 31187) | 617 | update v_T |
| update target not resolvable to a form | v_target | function set_pvs_equipment_charge (.ds line 36067) | 38 | update v_target |
| update target not resolvable to a form | v_target | function set_pvs_equipment_charge (.ds line 36067) | 45 | update v_target |

## By kind

- dynamic: invokeUrl: 63
- thisapp call to unknown function: 4
- update target not resolvable to a form: 3
