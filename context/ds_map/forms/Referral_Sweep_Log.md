# Referral_Sweep_Log

- Display name: Referral Sweep Log
- .ds line: 5634
- Fields (excluding sections): 9
- Parent form: -

## Fields

| Link name | Display name | Type | Lookup target |
|---|---|---|---|
| Section | - | section | - |
| Run_Time | Run Time | datetime | - |
| Run_Status | Run Status | picklist | - |
| Found_Count | Referrals Found | number | - |
| Repaired_Count | Repaired  | number | - |
| Failed_Count | Failed | number | - |
| Repaired_List | Repaired Referrals | textarea | - |
| Failure_Detail | Failures | textarea | - |
| FRun_Detail | Full Run Detail | textarea | - |
| Emailed | - | picklist | - |

## Workflows

- none
## Reverse index

Every item that references a field of this form.

- Referral_Sweep_Log.Run_Time: function sweep_unnotified_referrals [insert, read]
- Referral_Sweep_Log.Run_Status: function sweep_unnotified_referrals [insert, read]
- Referral_Sweep_Log.Found_Count: function sweep_unnotified_referrals [insert, read]
- Referral_Sweep_Log.Repaired_Count: function sweep_unnotified_referrals [insert, read]
- Referral_Sweep_Log.Failed_Count: function sweep_unnotified_referrals [insert, read]
- Referral_Sweep_Log.Repaired_List: function sweep_unnotified_referrals [insert, read]
- Referral_Sweep_Log.Failure_Detail: function sweep_unnotified_referrals [insert, read]
- Referral_Sweep_Log.FRun_Detail: function sweep_unnotified_referrals [insert]
- Referral_Sweep_Log.Emailed: function sweep_unnotified_referrals [fetch, insert, update]
