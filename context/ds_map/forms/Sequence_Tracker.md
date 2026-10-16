# Sequence_Tracker

- Display name: Sequence Tracker
- .ds line: 7036
- Fields (excluding sections): 4
- Parent form: -

## Fields

| Link name | Display name | Type | Lookup target |
|---|---|---|---|
| Section | - | section | - |
| Object_Name | Object Name | text | - |
| Object_Prefix | Object Prefix | text | - |
| Object_Sequence | Object Sequence | number | - |
| Object_Lock_Status | Object Lock Status | radiobuttons | - |

## Workflows

- none
## Reverse index

Every item that references a field of this form.

- Sequence_Tracker.Object_Name: no references
- Sequence_Tracker.Object_Prefix: function api_fax_send_console [fetch]; function backfill_mint_missing_referral_ids [fetch]; function backfill_pvs_ids [fetch]; function create_3008_pvs_july [fetch]; function create_3008_pvs_sept [fetch]; function diag_sequence_trackers [read]; function mint_assignment_id [fetch]; function mint_employee_id [fetch]; function mint_location_id [fetch]; function mint_partner_id [fetch]; function mint_referral_id [fetch]; function send_pvs_fax [fetch]; workflow Encounter_PatientVisit/PVS_ID_Stamp_Generator [fetch]
- Sequence_Tracker.Object_Sequence: function api_fax_send_console [read, update]; function backfill_mint_missing_referral_ids [read]; function backfill_pvs_ids [read, update]; function create_3008_pvs_july [read, update]; function create_3008_pvs_sept [read, update]; function diag_sequence_trackers [read]; function mint_assignment_id [read, update]; function mint_employee_id [read, update]; function mint_location_id [read, update]; function mint_partner_id [read, update]; function mint_referral_id [read, update]; function send_pvs_fax [read, update]; workflow Encounter_PatientVisit/PVS_ID_Stamp_Generator [read, update]
- Sequence_Tracker.Object_Lock_Status: no references
