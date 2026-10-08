# Operations Dashboard (Reports page) - source of record

Page `Reports` (HTML snippet) + page `Drilldown_Data` + stateless form `Dashboard_Range` + widget `Today's Visits`.
Page snippets, widgets and button scripts are NOT captured by ds_sync; this folder is the versioned copy.

| File | Creator location | Version / status |
|---|---|---|
| reports_page_snippet_v5.3.txt | Reports page > HTML snippet. Page variables r_from, r_to, r_mode (Text) | v5.3 delivered 2026-10-08 (2c tiles, box shadow, no card top border). Pasted live: v5 confirmed; v5.1-v5.3 pending Neil confirm |
| dash_metrics_range.dg | Function dash_metrics_range(date p_from, date p_to, string p_mode, string p_key) returns map | Live (Session 59) |
| dashboard_range_apply.dg | Dashboard_Range stateless form > Apply button > On Click | Live |
| widget_today_visits.dg | Function widget_today_visits() returns map; published as Custom API Widget_Today_Visits (GET, OAuth2, All users), workspace sosmmc | Live (status_map + login allow-list: Neil work, Neil gmail, Josh work, Josh portal) |
| widget_today_visits/ | Settings > Widgets > Today's Visits (Internal, index /widget.html). Packed with zet pack | v3 delivered 2026-10-08, test pending |
| assignment_required_referral.dg | Workflow Assignment_Required_Refer (Assignments, Created or Edited, On Validate) | Live: provider required on create only |
| assignment_notify_provider.dg | Workflow Assignment_Notify_Provide (Assignments, Created or Edited, On Success) | Live: adds Josh portal login; notifies on unassign (Visit Removed) |
