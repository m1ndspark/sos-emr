# Fax_Log

- Display name: Fax Log
- .ds line: 1294
- Fields (excluding sections): 25
- Parent form: -

## Fields

| Link name | Display name | Type | Lookup target |
|---|---|---|---|
| Section | - | section | - |
| Fax_ID | Fax ID | text | - |
| PVS_Link | PVS Link | picklist | Encounter_PatientVisit |
| Partner_Link | Partner Lookup | picklist | Partners |
| Referral_Link | Referral Link | picklist | Referrals_Main |
| Partner_Location_Link | Partner Location Lookup | picklist | Partner_Locations |
| Destination_Fax | Destination Fax | text | - |
| Destination_Name | Destination Name | text | - |
| Fax_Status | Fax Status | radiobuttons | - |
| Number_Source | Number Source | radiobuttons | - |
| Override_Reason | Override Reason | textarea | - |
| Cover_Remarks | Cover Remarks | textarea | - |
| Attachments_Included | Attachments Included | textarea | - |
| Fax_PDF | Fax PDF | upload file | - |
| Page_Count | Page Count | number | - |
| RC_Message_ID | RC Message ID | text | - |
| RC_Conversation_ID | RC Conversation ID | text | - |
| Fax_Error_Code | Fax Error Code | text | - |
| Fax_Error_Reason | Fax Error Reason | textarea | - |
| Attempt_Number | Attempt Number | number | - |
| Sent_By | Sent By | picklist | Employees |
| Submitted_Time | Submitted Time | datetime | - |
| Completed_Time | Completed Time | datetime | - |
| Last_Polled_Time | Last Polled Time | datetime | - |
| Fax_Log_ID_Stamp | Fax Log ID Stamp | text | - |
| Original_Fax_Link | Original Fax Lookup | picklist | Fax_Log |

## Workflows

- none
## Reverse index

Every item that references a field of this form.

- Fax_Log.Fax_ID: function api_fax_send_console [fetch, update]; function diag_bad_remarks_faxes [read]; function diag_fax_error [fetch, read]; function diag_fax_repair_errors [read]; function diag_stuck_faxes [read]; function repair_fax_log_status [read]; function send_fax_digest [read]; function send_pvs_fax [insert]
- Fax_Log.PVS_Link: function diag_fax_coverage [read]; function poll_fax_status [read]; function repair_fax_log_status [read]; function retry_failed_faxes [read]; function send_activity_digest [read]; function send_pvs_fax [insert]
- Fax_Log.Partner_Link: function api_fax_send_console [update]
- Fax_Log.Referral_Link: function send_pvs_fax [insert]
- Fax_Log.Partner_Location_Link: function api_fax_send_console [update]; function send_pvs_fax [insert]
- Fax_Log.Destination_Fax: function api_fax_send_console [update]; function diag_bad_remarks_faxes [read]; function diag_fax_error [read]; function retry_failed_faxes [read]; function send_fax_digest [read]; function send_pvs_fax [insert]
- Fax_Log.Destination_Name: function api_fax_send_console [update]; function diag_bad_remarks_faxes [read]; function diag_fax_error [read]; function retry_failed_faxes [read]; function send_fax_digest [read]; function send_pvs_fax [insert]
- Fax_Log.Fax_Status: function api_fax_begin [insert]; function api_fax_send_console [update]; function diag_bad_remarks_faxes [read]; function diag_fax_attachments [fetch]; function diag_fax_coverage [read]; function diag_fax_error [read]; function diag_fax_repair_errors [fetch, read]; function diag_stuck_faxes [fetch]; function poll_fax_status [fetch, update]; function repair_fax_log_status [fetch, read, update]; function retry_failed_faxes [fetch, update]; function send_activity_digest [fetch]; function send_fax_digest [fetch, read]; function send_pvs_fax [insert, update]; schedule Fax_Poll_Re_arm [fetch]
- Fax_Log.Number_Source: function api_fax_begin [insert]; function api_fax_send_console [update]; function diag_fax_error [read]; function retry_failed_faxes [read]; function send_fax_digest [fetch]; function send_pvs_fax [insert]
- Fax_Log.Override_Reason: function retry_failed_faxes [read]; function send_fax_digest [read]; function send_pvs_fax [insert]
- Fax_Log.Cover_Remarks: function api_fax_send_console [update]; function diag_bad_remarks_faxes [read]; function retry_failed_faxes [read]; function send_pvs_fax [insert]
- Fax_Log.Attachments_Included: function api_fax_send_console [update]; function send_pvs_fax [update]
- Fax_Log.Fax_PDF: function api_fax_send_console [update]; function send_pvs_fax [update]
- Fax_Log.Page_Count: function poll_fax_status [update]
- Fax_Log.RC_Message_ID: function api_fax_send_console [update]; function diag_fax_error [read]; function diag_fax_repair_errors [read]; function diag_rc_fax_history [read]; function diag_stuck_faxes [read]; function poll_fax_status [read]; function repair_fax_log_status [read]; function send_pvs_fax [update]
- Fax_Log.RC_Conversation_ID: function api_fax_send_console [update]; function send_pvs_fax [update]
- Fax_Log.Fax_Error_Code: function diag_fax_error [read]; function poll_fax_status [update]; function send_fax_digest [read]
- Fax_Log.Fax_Error_Reason: function api_fax_send_console [update]; function diag_fax_error [read]; function poll_fax_status [update]; function retry_failed_faxes [update]; function send_pvs_fax [update]
- Fax_Log.Attempt_Number: function api_fax_begin [insert]; function poll_fax_status [read]; function retry_failed_faxes [read]; function send_pvs_fax [insert]
- Fax_Log.Sent_By: function api_fax_begin [update]; function send_fax_digest [read]; function send_pvs_fax [update]
- Fax_Log.Submitted_Time: function api_fax_send_console [update]; function diag_bad_remarks_faxes [read]; function diag_fax_coverage [read]; function poll_fax_status [read]; function send_activity_digest [fetch, read]; function send_fax_digest [fetch]; function send_pvs_fax [insert]
- Fax_Log.Completed_Time: function api_fax_send_console [update]; function diag_fax_coverage [read]; function diag_fax_repair_errors [fetch]; function poll_fax_status [update]; function repair_fax_log_status [fetch, update]; function retry_failed_faxes [update]; function send_activity_digest [read]; function send_pvs_fax [update]
- Fax_Log.Last_Polled_Time: function api_fax_send_console [update]; function poll_fax_status [update]; function send_pvs_fax [update]; schedule Fax_Poll_Re_arm [read]; schedule Fax_Retry_Sweep [read]
- Fax_Log.Fax_Log_ID_Stamp: no references
- Fax_Log.Original_Fax_Link: function retry_failed_faxes [read]; function send_pvs_fax [update]
