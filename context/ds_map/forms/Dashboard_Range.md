# Dashboard_Range

- Display name: Dashboard Range
- .ds line: 537
- Fields (excluding sections): 2
- Parent form: -

## Fields

| Link name | Display name | Type | Lookup target |
|---|---|---|---|
| Section | - | section | - |
| From_Date | From | date | - |
| To_Date | To | date | - |

## Workflows

### Dashboard_Range_Apply

- Display: Dashboard Range Apply
- Record event: -
- Form event: OnClick (button Apply)
- Status: ENABLED
- .ds line: 36978
- Fields read: From_Date, To_Date
- Fields set: -
- Fields shown/hidden/enabled/disabled: -
- Functions called: -
- Other forms: -

## Reverse index

Every item that references a field of this form.

- Dashboard_Range.From_Date: workflow Dashboard_Range/Dashboard_Range_Apply [read]
- Dashboard_Range.To_Date: workflow Dashboard_Range/Dashboard_Range_Apply [read]
