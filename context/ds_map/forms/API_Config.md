# API_Config

- Display name: API Config
- .ds line: 14
- Fields (excluding sections): 7
- Parent form: -

## Fields

| Link name | Display name | Type | Lookup target |
|---|---|---|---|
| Section | - | section | - |
| Config_Name | Config Name | text | - |
| RC_Client_ID | RC Client ID | text | - |
| RC_Client_Secret | RC Client Secret | text | - |
| RC_JWT_Assertion | RC JWT Assertion | textarea | - |
| RC_Access_Token | RC Access Token | textarea | - |
| RC_Token_Expiry | RC Token Expiry | datetime | - |
| Zepto_Send_Token | - | textarea | - |

## Workflows

- none
## Reverse index

Every item that references a field of this form.

- API_Config.Config_Name: function api_fax_send_console [fetch]; function diag_config_write [fetch]; function diag_rc_token [fetch]; function get_rc_token [fetch]; function resend_referral_notifications [fetch]; function send_3008_notification [fetch]; function send_activity_digest [fetch]; function send_assignment_notification [fetch]; function send_fax_digest [fetch]; function send_imaging_notification [fetch]; function send_pvs_fax [fetch]; function send_referral_confirmation [fetch]; function send_referral_notification [fetch]
- API_Config.RC_Client_ID: function diag_rc_token [read]; function get_rc_token [read]
- API_Config.RC_Client_Secret: function diag_rc_token [read]; function get_rc_token [read]
- API_Config.RC_JWT_Assertion: function diag_rc_token [read]; function get_rc_token [read]
- API_Config.RC_Access_Token: function api_fax_send_console [update]; function diag_config_write [read, update]; function diag_rc_token [read]; function get_rc_token [read, update]; function send_pvs_fax [update]
- API_Config.RC_Token_Expiry: function api_fax_send_console [update]; function diag_config_write [update]; function diag_rc_token [read]; function get_rc_token [read, update]; function send_pvs_fax [update]
- API_Config.Zepto_Send_Token: function resend_referral_notifications [read]; function send_3008_notification [read]; function send_activity_digest [read]; function send_assignment_notification [read]; function send_fax_digest [read]; function send_imaging_notification [read]; function send_referral_confirmation [read]; function send_referral_notification [read]
