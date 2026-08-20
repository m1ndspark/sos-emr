# PVS_Fax_Review - form notes

Non-Deluge facts about this form, recorded here because they do not copy out as
code. Created Session 36, 2026-08-20.

Full system spec: `docs/fax/SOS_PVS_Fax_System_Design.md`.

--------------------------------------------------------------------------------
## The form is STATELESS

`store data in zc = false`. Confirmed in the v28 Creator export. Nothing this
form collects is persisted by the form itself; `send_pvs_fax` writes the durable
record to `Fax_Log`.

**A form cannot be toggled to stateless after it exists.** If this one ever has
to be rebuilt, duplicate it via Open Form Builder > More > Duplicate with "Data
will be stored in Zoho Creator" unchecked, then delete the original and rename
the duplicate, then repoint everything bound to the old name. See
`context/05_deluge_learnings.md`.

--------------------------------------------------------------------------------
## How the page is reached

    #Form:PVS_Fax_Review?PVS_Link=<record ID>

`PVS_Link` is a plain single-line text field carrying the PVS **record ID**, and
the On Load workflow reads `input.PVS_Link` to fetch the visit.

**The record ID must come from a System ID column on `PVS_Report`.** This is not
a preference, it is forced: Creator v6 keeps the report URL static
(`#Report:PVS_Report`) when a record detail or edit view opens, so the record ID
never appears in the address bar and cannot be scraped from it. Add the System ID
field as a report column and build the link from that column's value.

If the System ID column is removed from `PVS_Report`, this page stops being
reachable. Treat that column as load-bearing, not cosmetic.

--------------------------------------------------------------------------------
## Field state at load

The On Load workflow leaves the form in this state. Recorded here because the
disable/hide calls are behavior, not schema, and will not show up in
`schema/PVS_Fax_Review.md`.

| Field | State after load |
|---|---|
| `PVS_Link` | populated from the URL, disabled |
| `Patient_Display` | built, read-only |
| `Gate_Message` | computed, read-only |
| `Note_Preview` | copied from `Final_Clinical_Note`, read-only |
| `Destination_Name` | resolved, read-only |
| `Destination_Fax` | resolved, read-only |
| `Override_Unlock` | visible, editable |
| `Override_Fax` | **hidden** until unlock |
| `Override_Fax_Confirm` | **hidden** until unlock |
| `Override_Reason` | **hidden** until unlock |
| `Cover_Remarks` | prefilled, editable |
| attachment multi-select | cleared and repopulated at runtime, editable |
| `Result_Message` | blank |

The destination resolves from `Partner_Billing_Contacts.Partner_PVS_Fax` for the
PVS's `Billing_Branch`.

`Cover_Remarks` is prefilled with an amendment banner when
`Clinical_Note_Type` is `Addendum`.

The attachment picker is cleared and repopulated from the PVS file-upload fields
(`Clinical_Note_File_Upload` and `PVS_File_Upload`) using `ui.clear()` then
`ui.add(list)`, which works in On Load and On User Input only.

--------------------------------------------------------------------------------
## STATUS - the workflow body is NOT in this repo

`OnLoad__PVS_Fax_Review_On_Load.dg` is **missing**. Neil reports it as written,
deployed and tested live on 2026-08-20, but no copy of it reached this machine:

- It is not in `MPU Reporting/deluge/`.
- It is **not** in the newest local export, `SOS_Referrals_App (28).ds`
  (2026-08-20 09:42). That export contains the form with 13 fields and no On Load
  workflow at all.

The field list above also does not match the export. `schema/PVS_Fax_Review.md`
(captured 09:38 that morning) shows 13 fields with the multi-select still named
`Multi_Select` carrying placeholder choices `Choice 1, Choice 2, Choice 3`. Neil
reports 15 fields with that field renamed to `Attachments_Select` and a Fax Now
button added. Both the rename and the workflow therefore happened after the
09:42 export.

**To close this:** paste the On Load body into `MPU Reporting/deluge/`, or supply
a fresh `.ds` export taken after the rename. Tracked in
`context/23_task_list.md`.
