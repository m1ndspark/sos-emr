# Fax_Attachments

- Display name: Fax Attachments
- .ds line: 1200
- Fields (excluding sections): 6
- Parent form: -

## Fields

| Link name | Display name | Type | Lookup target |
|---|---|---|---|
| Section | - | section | - |
| Fax_Log | Fax Log Lookup | picklist | Fax_Log |
| Attachment_Type | Attachment Type | radiobuttons | - |
| Attachment_Name | Attachment Name | text | - |
| Attachment_File | Attachment File | upload file | - |
| Source_PVS_Link | Source PVS | picklist | Encounter_PatientVisit |
| Sequence_Number | Sequence Number | number | - |

## Workflows

- none
## Reverse index

Every item that references a field of this form.

- Fax_Attachments.Fax_Log: function api_fax_send_console [insert]; function diag_fax_attachments [read]; function poll_fax_status [fetch]; function send_activity_digest [read]; function send_pvs_fax [insert]
- Fax_Attachments.Attachment_Type: function api_fax_send_console [insert]; function diag_fax_attachments [read]; function send_activity_digest [fetch]; function send_pvs_fax [insert]
- Fax_Attachments.Attachment_Name: function api_fax_send_console [insert]; function send_pvs_fax [insert]
- Fax_Attachments.Attachment_File: function api_fax_send_console [update]; function send_pvs_fax [update]
- Fax_Attachments.Source_PVS_Link: function api_fax_send_console [insert]; function diag_fax_attachments [read]; function poll_fax_status [read]; function send_activity_digest [read]; function send_pvs_fax [insert]
- Fax_Attachments.Sequence_Number: function api_fax_send_console [insert]; function send_pvs_fax [insert]
