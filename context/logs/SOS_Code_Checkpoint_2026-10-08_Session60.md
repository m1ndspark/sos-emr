SOS Code - Checkpoint - October 08, 2026 (Session 60)
Span: 2026-10-08 11:50 to 17:50 ET. Ground truth .ds: v62 (commit 61216d4). Export v63 next.

1. WIDGET (Ops Dashboard stage 5)
- v3.1 uploaded; provider set/clear saved. Status saves failed except blank.
- Root cause: Assignments.Visit_Status static choices were Received, Contacted, Scheduled, Awaiting Equipment, Pending Results. Widget saves via API are checked against static choices; the On Load ui.add only changes the form.
- Fix: Neil added Completed, Ordered, Report Sent, Pending Info to the field. Assignment_Visit_Status_Choices (Assignments, Edited, On Load) now runs clear Visit_Status before ui.add. Pending Info and Completed verified on REF-1681. Ordered and Report Sent still to test on an imaging row.
- v3.2: error toast persists and shows Creator's full response. Chrome cannot read the widget iframe (cross-origin).
- v3.3 LIVE: heading "Referral Assignment(s)"; Service column with PVS_Report colors (Visit #e8eefd, 3008 #fcf2e7, Imaging #d2e9d1); list fills widget height; Reports page widget element set to about 380px.
- widget_today_visits: provider list = Active and (Job Title Clinical or Portal Access Types contains Admin).

2. PORTAL ADMIN
- Admin portal profile created: Access/View/Edit on all forms, no Delete, Dashboard Range access only, API_Config no access.
- First save of Neil's Employees record as Admin failed (Profile Admin not valid, Portal Access By Status line 34) before the profile existed; re-saved after.
- Decision: widget and provider-email gate = portal Admins (is_portal_admin), not a named email list. is_portal_admin() delivered; paste unconfirmed. widget_today_visits and Assignment_Notify_Provide gates not yet switched.
- Neil's portal logins: neilheird@gmail.com (on allow-list) and neil.heird@sosreferrals.com (not on allow-list).

3. ASSIGNMENT EMAILS (send_assignment_notification)
- Header: patient name and Referral ID, both linked to the portal referral. Referral ID row added above Assignment ID; patient row linked.
- Portal link format verified: https://portal.sosreferrals.com/#Report:Referrals_Main_Report?Referral_ID=REF-xxxx
- Titles and subjects: Visit Assigned / Visit Removed; service pill in header.
- Behavior: reassign emails the new provider (Assigned) and the old one (Removed); unassign emails Removed. A failed Assigned email reverts the stamp and retries on the next save; a failed Removed email during a reassignment is not retried.
- Field updates from the widget fire Edited workflows (On Validate, On Success) per change. Documented for the v2.1 API; inferred for the widget SDK.

4. EMAIL SUBJECTS (all live, Neil pasted all)
- Pattern: [Title]: [Service] - [Full Name]  |  [REF ID]  (two spaces around the pipe). Service labels: Visit, 3008, Imaging.
- New Referral: build_referral_email_html, build_3008_email_html, build_imaging_email_html. send_referral_notification and send_imaging_notification now use the builder's subject.
- Referral Confirmation (partner): subject and header title renamed from Referral Received. No pill.
- Visit Assigned / Visit Removed: pill.
- Data Issue (Referral Data Issues Check workflow): reads values from the saved record; no longer substitutes the record ID for a missing Referral ID.
- Digests: Daily Referrals | date, Daily PVS | label, Weekly Recap | range, Daily Fax Digest | date, Referral Sweep | counts (headings match).
- Service pill (light blue/peach/green) in the header of the referral and assignment emails only.

5. FINDINGS
- Assignment_Status_From_Pr assigns Assignment_Status, which is not a field on Assignments, so it has no effect.
- Pages snippets and widgets are not in the .ds; dashboard/ in the repo is the source of record.

6. NEW REQUESTS (task list)
- "Assign this visit" button in referral notification emails, landing on an assignment screen.
- Patients form and report showing all linked records on patient search.

7. NEXT
1. Confirm is_portal_admin pasted; switch widget_today_visits and Assignment_Notify_Provide gates.
2. Test Ordered and Report Sent on an imaging row.
3. Josh portal test.
4. Paste Reports snippet v5.3.
5. Drilldown_Data v5.
6. Share.
7. Export v63 and ds_sync.

8. REPO (this checkpoint)
- dashboard/widget_today_visits/app/widget.html = v3.3.
- dashboard/README.md rows updated.
- context/23_task_list.md: 4 CLOSED, 7 OPEN added; stage 5 row updated; Visit_Status verify row closed.
- context/logs/SOS_Code_Checkpoint_2026-10-08_Session60.md (this file).
- Changed functions and workflows reach the repo through v63 ds_sync.
