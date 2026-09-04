# SOS Code Checkpoint - 2026-09-03 - Session 40

Mid-session checkpoint. Covers everything since the Session 39 checkpoint
(2026-09-02). Written by cchat; repo edits by cchat, Creator edits by Neil.

--------------------------------------------------------------------------------
## 1. Assignments cleanup (DONE)
--------------------------------------------------------------------------------

Fields removed from Assignments: Assignment_Status, Accepted_Date,
Scheduled_Visit_Date, Patient_MI. Fields retyped to Single Line (1):
Referral_Date, Patient_DOB, Patient_Phone, Facility_Phone (text keeps the
formatting Zoho Forms pushes). Confirmed by the 09-03 11:34 schema capture.

Workflows cleaned to match (all pasted live):
- Assignment_Change_Log (Assignments, On Validate): dropped the Accepted Date,
  Scheduled Visit Date and Assignment Status log blocks.
- Assignment_Pull_From_Referral (Assignments, On User Input on Referral_Link,
  Created only): targets Patient_DOB (from referral Patient_DOB1),
  Patient_Phone, Facility_Phone; Patient_MI and Referral_Date dropped.
- Assignment_Lock_Immutable_Fields (Assignments, On Load): disables
  Patient_First_Name, Patient_Last_Name, Patient_DOB only.

Interim link names Patient_DOB1 / Patient_Phone1 / Referral_Date1 were used
during the swap and then renamed back; the live names carry no suffix.

--------------------------------------------------------------------------------
## 2. Assignment model - decisions
--------------------------------------------------------------------------------

- No availability calendars. Josh assigns anyone from Employees. (Josh agreed.)
- Zoho FSM rejected: no Creator integration, REST only.
- One Assignments record per referral, AUTO-CREATED as an incomplete stub by
  Referrals_Main_On_Create_Master, guarded by a count on Referral_Link so a
  referral edit never spawns a second one.
- Josh finalizes by filling Employee_Link (initial assignee). The existing
  On Validate rule (referral + employee required) gates the save; once saved
  the initial assignee is locked. insert into bypasses On Validate, which is
  what lets the empty stub exist.
- Reassignments live in a SUBFORM on Assignments (Reassigned_To lookup to
  Employees, Reassignment_Date, Reassignment_Reason), one row per hop, so the
  full chain of who held the referral is preserved. A Current_Assignee lookup
  on the parent is kept in sync by workflow and is what the provider portal
  filters on.
- Record_State (Active / Superseded) was proposed for a multi-record model and
  DROPPED when the design moved to parent + subform.
- Visit_Status is the clinical lifecycle, ONE dropdown holding the superset,
  trimmed at runtime by referral type (see section 3). Completed is terminal.
- Assignment_Status (Accepted / Pending) is gone: a manual assignment IS
  acceptance; a change is a reassignment.

NOT YET BUILT: the Reassignments subform, Current_Assignee, the sync workflow,
the assignee notification, and the provider dashboard page. Paused for the
attachments work (section 4).

--------------------------------------------------------------------------------
## 3. Visit_Status + choice trimming (DONE, one defect open)
--------------------------------------------------------------------------------

Field: Assignments.Visit_Status, Dropdown, default Received.
Workflow: Assignment_Visit_Status_Choices (Assignments, On Load, Created or
Edited). Fetches the linked referral's Referral_Type through Referral_Link and
replaces the dropdown choices with ui.add (doc-verified: ui.add replaces all
choices, works On Load and On User Input, not in functions):
- Patient Visit: Received, Contacted, Scheduled, Awaiting Equipment,
  Pending Results, Completed
- 3008: Received, Pending Info, Completed
- Imaging Order (only): Received, Ordered, Pending Results, Report Sent,
  Completed
- unknown type: full superset

DEFECT: the 20:42 capture shows the field's choice list holds only Received,
Contacted, Scheduled, Awaiting Equipment, Pending Results. Ordered,
Report Sent, Pending Info and Completed must be added to the field definition.

--------------------------------------------------------------------------------
## 4. Attachments: files into Creator and onto the notification emails (DONE)
--------------------------------------------------------------------------------

Root cause of "12 3008 referrals, no attachments": neither notification function
ever attached anything (the 3008 email printed "See the Zoho Forms entry"), and
the Zoho Forms integration cannot map upload fields to Creator file fields.

Routes tried and rejected this session:
- Direct file-to-file mapping: not offered by the integration.
- Zoho Flow: relocates the download/upload code, adds a product, no gain.
- Zoho Forms webhook (multipart carries the files) into a Creator Custom API:
  DEAD - Creator functions have no file argument type, so the bytes cannot
  reach Deluge.

Route built (all-Zoho, files end up in Creator):
1. Zoho Forms > Settings > Submissions & Storage > Manage Form Attachments:
   WorkDrive, Manage Manually, folder New_Referral_File_Attachments (currently
   under Josh's My Folders). "Store form submission as PDF" left OFF.
2. Referrals_Main: three Multi Line fields Files_3008_URLs, General_Files_URLs,
   Imaging_Orders_URLs (a Multi Line target takes up to 5 URLs from one upload
   question, so the earlier one-file cap does not apply).
3. A FRESH Zoho Forms > Creator integration (the existing one would not list
   the upload fields even after cloud storage was on). Upload questions mapped
   to the three URL fields. The two mapping bugs from Session 38 (Partner
   Organization / Partner Location Label, allergies vs anticoagulants) were
   NOT re-verified in the new integration.
4. New Creator form Referral_Files: Form_Token, Referrals_Main (lookup,
   display Referral_ID), File_Category (3008 / General / Imaging Orders),
   File_Name, File_Upload (single).
5. Creator connection sos_workdrive (Zoho WorkDrive, Quick connect, All
   Actions = WorkDrive.files.ALL, Administrators only).
6. Referrals_Main_On_Create_Master: new block between the referral update and
   the notification calls. For each URL field, split on newline/comma, take
   the resource ID after the last slash, GET
   https://workdrive.zoho.com/api/v1/download/<id> via sos_workdrive, insert a
   Referral_Files row (file object assigned straight to File_Upload,
   getFileName() for File_Name), then PATCH /api/v1/files/<id> status 51 and
   DELETE it. Per-file try/catch.
7. New function build_zepto_attachments(int p_refId, string p_token) returns
   list: for each Referral_Files row, POST the file as a raw binary body to
   https://api.zeptomail.com/v1.1/files?name=<urlEncoded name> with the
   ZeptoMail key, collect file_cache_key + name.
8. send_referral_notification and send_3008_notification: list the filenames
   in an "Attached Documents" / "3008 Documents" row, call the helper, put the
   list on the payload as "attachments". The "Open Referral" button was
   REMOVED from both (Neil). FAIL return now carries the Referral_ID.

Tested: test referral REF-1080 -> Referral_Files row created with the file ->
send_referral_notification returned SENT REF-1080 -> email arrived with the
file attached.

Open from this section:
- WorkDrive cleanup is not effective: the file is still in WorkDrive after
  intake (folder or trash not confirmed). Fix so no PHI lingers.
- Move the staging folder to a Team Folder.
- Connection Access for sos_workdrive on SOS Referrals App must be ON;
  Authorized Account should be Josh.
- The 12 earlier 3008s have no Referral_Files rows (files only in Zoho Forms).
- Retire the three Type 46 upload fields after a workflow audit.
- Zoho's HIPAA page lists WorkDrive, Creator, Forms and ZeptoMail; whether
  WorkDrive is named in SOS's signed BAA is Neil's to confirm.

Deluge facts confirmed this session (add to context/05):
- insert into does NOT fire the target form's On Validate or On Success.
- A whole Address field can be assigned from another Address field in
  insert into (Patient_Address=input.Patient_Address).
- Field:ui.add(list) replaces a dropdown's choices at runtime; On Load and
  On User Input only.
- Creator function arguments have no file type; "Referral Files" in the type
  picker is the form object, not a file.
- invokeurl body accepts a FILE object for raw binary; default content type
  application/octet-stream, overridable by header.
- URL-encode is zoho.encryption.urlEncode(text); there is no .encodeUrl().
- The Creator function editor shows the signature line; paste full editor
  contents including "string fn(string p) { ... }" when replacing.

--------------------------------------------------------------------------------
## 5. Notification calls restored (DONE, incident)
--------------------------------------------------------------------------------

The repo copy of Referrals_Main_On_Create_Master was stale at Session 31 and
did not contain the two Session 39 notification calls. A full-master paste
early in this session removed them from live; the v33 export confirmed no
thisapp.send_referral_notification / send_3008_notification call existed
anywhere. Both were re-added after the referral update block:
thisapp.send_referral_notification(input.ID.toString()) and the 3008 twin.
Referrals submitted in the gap got no email; resend by hand if needed.

--------------------------------------------------------------------------------
## 6. Repo
--------------------------------------------------------------------------------

- SOS_Referrals_App_2026-09-03_v33.ds saved (canonical refreshed), ds_sync
  --apply wrote 3 DRIFT + 11 NEW (both notification functions, the fax stack,
  the diag functions). Commit d8e4239 on top of 7 schema-monitor commits,
  rebased and pushed by ccode as 24f5c49.
- CLAUDE.md: three new rules (any .ds from chat is saved to the repo
  immediately; read schema/ and the newest .ds before field questions, say so
  if unreachable; repo .md edits are Claude's job).
- Session 40 function edits (build_zepto_attachments, both notification
  functions, the master with intake block, Assignments workflow cleanups) are
  in the repo AHEAD of the v33 export and will show DRIFT until the next .ds.
- Stale .git/*.lock files parked as .stale-* (device shell cannot delete).

--------------------------------------------------------------------------------
## 7. Other findings
--------------------------------------------------------------------------------

- send_referral_notification has NO phone-format loop (send_3008_notification
  does). Patient Visit emails print phones unformatted. Add it.
- Assignments has two On User Input pulls on Referral_Link
  (Assignment_Pull_From_Refe and Assignment_Pull_From_Refe1); delete one.
- Referral_Date (now text), Referral_Partner and Referral_POC on Assignments
  are redundant (reachable via Referral_Link); remove.
- Provider portal landing page per permission set: believed to be the first
  enabled component in the Providers permission set (unverified, docs silent).
- Notification recipients are hardcoded per function
  (neil.heird@sosmmc.com, sosreferrals@sosmmc.com), not in API_Config.

--------------------------------------------------------------------------------
## 8. Resume point
--------------------------------------------------------------------------------

1. Fix Visit_Status choice list (add the four missing values).
2. Verify sos_workdrive Connection Access ON; fix WorkDrive cleanup.
3. Create Reassignments subform + Current_Assignee; write the sync workflow
   and the assignee notification.
4. Provider_Dashboard page: 3-button snippet with the two cards.
5. Retire Type 46 upload fields; remove the three redundant Assignments fields;
   delete the duplicate pull workflow.
6. Fresh .ds export to clear the DRIFT.
