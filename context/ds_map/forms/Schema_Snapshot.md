# Schema_Snapshot

- Display name: Schema Snapshot
- .ds line: 7016
- Fields (excluding sections): 3
- Parent form: -

## Fields

| Link name | Display name | Type | Lookup target |
|---|---|---|---|
| Section | - | section | - |
| Snapshot_Data | Snapshot Data | textarea | - |
| Captured_On | Captured On | datetime | - |
| Change_Summary | Change Summary | textarea | - |

## Workflows

- none
## Reverse index

Every item that references a field of this form.

- Schema_Snapshot.Snapshot_Data: function run_schema_monitor [insert, read]
- Schema_Snapshot.Captured_On: function run_schema_monitor [insert, read]
- Schema_Snapshot.Change_Summary: function run_schema_monitor [insert, read]
