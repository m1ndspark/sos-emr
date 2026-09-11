# SOS Code CHECKPOINT - 2026-09-11 (Session 45)

Scope: work completed between session start and this checkpoint. Zoho Creator v6,
Deluge. Medical context, data integrity critical.

--------------------------------------------------------------------------------
## 1. ROOT CAUSE FOUND: the referral notification regression
--------------------------------------------------------------------------------

Symptom carried since 2026-09-10: referrals arrived from the Zoho Form, a
notification email went out, and the Creator record had a blank Referral_ID,
blank Referral_ID_Stamp, blank Referral_Date, no partner resolution and no
assignment. Separately, notification subjects showed Referral IDs that existed
nowhere in the data, with the same ID reused across different patients
(REF-1464 on Barry Hall, Linda Haines and Barbara Basista; REF-1444 on Ramon
Anglada Alvarez and Linda Brown).

Cause, confirmed: Assignments.Patient_DOB is a TEXT field with maxchar 11. The
On Create master wrote a date object into it. That insert is the LAST statement
in the script, so it failed with "Value of the field Patient_DOB length should
be lesser than or equal to MaxLength 11", Creator rolled back every record write
in the transaction, and the ZeptoMail send that had already fired could not be
rolled back. The email survived; the data did not.

A second, independent defect was found in mint_referral_id: it assigned with
rec.Referral_ID = ... instead of an update block, and incremented
Sequence_Tracker the same way. Rewritten with update blocks, tracker incremented
BEFORE the record is stamped so a failure cannot reissue a number. Verified
persisting: REF-1465, REF-1466 and REF-1467 minted and stuck.

Correction to an earlier claim in this session: the bare assignment syntax was
first named as the root cause. It is a real defect but it is not what caused
this. The rollback from the Patient_DOB overflow is.

--------------------------------------------------------------------------------
## 2. NEW: process_new_referral, the single source of the create path
--------------------------------------------------------------------------------

The 15,012 character body of Referrals_Main_On_Create_ was extracted into
`process_new_referral(string p_refKey, string p_notify)`. The workflow body is
now one line:

    thisapp.process_new_referral(input.ID.toString(),"YES");

so the create path and the repair path can never drift.

Differences from the original body, all deliberate:

- Patient_DOB into Assignments is written as MM/dd/yyyy text, matching the house
  convention already used for Referral_Date on that form.
- File intake is skipped when Referral_Files rows already exist, so a repair
  cannot double attach.
- Referral_Date and Notified_Time are stamped BEFORE the send, and reverted to
  null if none of the three senders returned SENT. Commit first, send second.
- Referral_Date is derived from Creator's system Added_Time and ONLY for
  form-origin records (Form_Token present). It never defaults to today and never
  uses an import date. When no trusted arrival date exists, nothing is stamped
  and nothing is sent.
- The Patient_Address.address_line_1 references that were missing `input.` in the
  live body are fixed.
- p_notify "NO" repairs everything but sends nothing and leaves the record
  queued as un-notified, so notifications can be released later in batches.
- A SKIP-AMBIGUOUS guard aborts when a key matches more than one record. Note
  that Referral_ID is declared `unique` on the form, so this can never fire; it
  is insurance only.

--------------------------------------------------------------------------------
## 3. NEW: sos_referral_health, one function for find and fix
--------------------------------------------------------------------------------

`sos_referral_health(string p_mode, string p_scope, int p_limit)`

- p_mode: REPORT, FIX, FIX_NOTIFY. Unrecognized values fall back to REPORT.
- p_scope: ALL, an issue code, or a comma separated list of Referral IDs or
  record IDs. Blank returns SKIP-NOSCOPE so a missing argument can never sweep
  the whole table.
- p_limit: records repaired per run, default 5.

Issue codes: NOID, NOSTAMP, NOPARTNER, NOASSIGN, UNNOTIFIED, NONOTIFIER.

Billed records are skipped entirely. A referral counts as billed when any
Encounter_PatientVisit with Referral_Link pointing at it has Invoice_Link
populated. Neil's rule: "we will only skip records if they have been billed."

Performance: limit 5 hits Creator's execution timeout. Limit 2 is stable. The
cost is three full table scans before the loop plus, per record, a WorkDrive
download, a Creator file upload, a full Partner_Referral_Contacts scan and up to
three ZeptoMail calls.

--------------------------------------------------------------------------------
## 4. Referral queue cleared
--------------------------------------------------------------------------------

All 22 un-notified referrals were repaired and notified. Final board:

    Referrals scanned: 677 | skipped as billed: 237 | flagged: 69
    NOID 0 | NOSTAMP 0 | NOPARTNER 14 | NOASSIGN 58 | UNNOTIFIED 0 | NONOTIFIER 0

NOASSIGN and NOPARTNER that remain are unbilled legacy Cognito era records.

--------------------------------------------------------------------------------
## 5. Imaging Order notifications now exist
--------------------------------------------------------------------------------

Referral_Type has three values: "Patient Visit", "3008", "Imaging Order (only)".
Only the first two had a notifier, so every imaging only referral was silently
never announced.

New: `build_imaging_email_html(int p_recId)` and
`send_imaging_notification(string p_refKey)`, addressed to
get_notification_recipients("Imaging Orders"). That value already existed on
Employees.Email_Notification_Types, so no schema change was needed. Proven live
on REF-1460 and REF-1467.

--------------------------------------------------------------------------------
## 6. Standing rule: all output data comes from Creator
--------------------------------------------------------------------------------

Neil, verbatim: "referral ids should come only from creator. if no id exists,
then we need to know that. data inside of any page, paper, report, module, word
file, pdf file, any item you output, all data must come directly from creator
period."

Implemented:

- build_referral_email_html, build_3008_email_html and build_imaging_email_html
  return an empty map when Referral_ID is blank, so no email can be built
  without an ID.
- send_referral_notification, send_3008_notification and
  send_imaging_notification re-read the committed record and return SKIP-NOID
  rather than sending.
- Subjects are composed from the value read from Creator, not from the template
  map.

Related ruling: when Patient_DOB1 does not parse, a date found elsewhere in the
referral may be SURFACED for Neil's approval but never written. Not yet built.

--------------------------------------------------------------------------------
## 7. New fields on Referrals_Main
--------------------------------------------------------------------------------

- `Partner_Branch_Submitted` Single Line 255, private. The raw branch text the
  form sent, written once and never overwritten, so a mismatch stays visible
  after resolution overwrites Partner_Location_Label.
- `Notified_Time` Date-Time, private. Lag is Notified_Time minus Added_Time.

--------------------------------------------------------------------------------
## 8. Partner Locations and the Zoho Form rebuild
--------------------------------------------------------------------------------

Diagnosis: the form used a GROUP list where the organization header was itself
selectable, which is how "Empath - Main" reached Creator. It matched no active
Partner_Location_Label, so the partner never resolved. Exactly 1 distinct
unmatched value across 677 referrals, on 2 records (REF-1129, REF-1455).

Design confirmed: one location label is sufficient. Partner_Locations links to
Partners, so process_new_referral derives organization, Partner_ID, branch and
billing branch from that single value. No new workflow is needed.

Creator changes made by Neil:
- Created Cornerstone - Main (Partner Loc Name "Main", code CML).
- Deactivated: Chapters - Marathon, Chapters - Okeechobee, Chapters - Alachua,
  Cornerstone - Casa Bella House, Cornerstone - Descipio Hospice House,
  Cornerstone - LPHH, Cornerstone - Mariposa House, Cornerstone - MCHH.

Active label set is now 22. Partner_Location_Label is a plain text field built
by a workflow as "Partner Display Name - Partner Loc Name", which is why the
label reads "AccentCare - Pinellas" while the name cell holds only "Pinellas".

Form work: group list deleted, replaced with a flat Dropdown of the 22 labels.
The Creator integration was removed and rebuilt. The full 42 row mapping was
captured to screenshots and written up before removal; see
SOS_ZohoForm_Creator_Mapping_2026-09-11.md.

Mapping corrections established during the rebuild:
- Left column is the CREATOR field, right column is the ZOHO FORMS field. An
  earlier note in this session had this reversed.
- Creator "Patient DOB" is Patient_DOB1, text, maxchar 11. It takes the form's
  masked dd/dd/dddd question.
- Creator "Patient DOB (system)" is Patient_DOB, date, private. It is left
  unmapped because the parse fills it.
- Creator "3008 File URLs", "General Files URLs" and "Imaging Orders URLs" are
  the Multi Line targets and take the form's three upload questions. The
  similarly named Creator upload fields stay unmapped; process_new_referral
  fills them from the URLs. This depends on Zoho Forms > Manage Form Attachments
  being set to store in WorkDrive, folder New_Referral_File_Attachments.
- Creator "Partner Organization" and "Partner Branch/Location" are left unmapped
  and their old form questions were deleted. Both are derived.
- A Creator field that should not be mapped is removed with the red minus. The
  builder will not save a row left on -Select-.
- Resulting mapping count: 41.

--------------------------------------------------------------------------------
## 9. Invoice INV-000028 voided
--------------------------------------------------------------------------------

Bogus entry that reached billing. `reset_invoice("INV-000028","RESET")` unlinked
PVS-1227-JK back to Invoice_Link null and Invoice_Status Draft, voided the Books
invoice, and marked the Creator Invoices record Void. Void rather than delete
preserves the number and the audit trail.

OPEN: PVS-1227-JK is now Draft and unheld, so the next run_invoice_batch for
that branch and date range will pick it straight back up. It needs
Hold_From_Invoicing = Yes, or Complexity_Level = Visit Cancelled if the visit
itself was bogus.

--------------------------------------------------------------------------------
## 10. PVS billing flag audit
--------------------------------------------------------------------------------

483 PVS records by billing state:

    239  Invoice_Link=set   | Invoice_Status=Final | Hold=No
    191  Invoice_Link=null  | Invoice_Status=blank | Hold=blank
     23  Invoice_Link=null  | Invoice_Status=Draft | Hold=Yes
     17  Invoice_Link=null  | Invoice_Status=Draft | Hold=No
     12  Invoice_Link=null  | Invoice_Status=Draft | Hold=blank
      1  Invoice_Link=set   | Invoice_Status=Final | Hold=Yes

Zero corrupt combinations. The 191 blank status rows are the August import,
which never received the field's initial value.

Agreed write gate for any automated repair on a PVS:

    Invoice_Link == null && Invoice_Status != "Final" && Hold_From_Invoicing != "Yes"

Testing Invoice_Status == "Draft" instead would wrongly lock out all 191
imported rows.

--------------------------------------------------------------------------------
## 11. Sequence tracker audit
--------------------------------------------------------------------------------

All four scanned trackers are SAFE. REF sits at 1464 with 1463 the highest
four digit ID in use. No tracker repair was needed.

Parsing note: Referral_ID has two formats in the data, the legacy Cognito era
REF-MMDDYY-NNNN (284 records) and the current REF-NNNN (389 records). Any
numeric parse must use a strict pattern such as ^REF-[0-9]{4}$ or the legacy
rows corrupt the result. A first attempt reported the max as 731261501.

--------------------------------------------------------------------------------
## 12. Referral origin markers
--------------------------------------------------------------------------------

    284  FormToken=blank   | CognitoID=blank   | ID=legacy   | null date: 0
     84  FormToken=present | CognitoID=blank   | ID=current  | null date: 9
    306  FormToken=blank   | CognitoID=present | ID=current  | null date: 0
      3  FormToken=present | CognitoID=blank   | ID=blank    | null date: 3

Form_Token is the clean discriminator between form created and imported records.
Every record with a null Referral_Date carried a Form Token, so the rule costs
nothing operationally.

--------------------------------------------------------------------------------
## 13. PVS employee link backfill
--------------------------------------------------------------------------------

Committed. 483 scanned, 480 now linked, 0 unmatched. The 3 remaining have a
blank Employee_Email and cannot link until that value exists on the PVS.

--------------------------------------------------------------------------------
## 14. New functions delivered this session
--------------------------------------------------------------------------------

Production:
- process_new_referral(string p_refKey, string p_notify)
- sos_referral_health(string p_mode, string p_scope, int p_limit)
- sweep_unnotified_referrals(string p_mode, string p_scope, int p_limit)
- build_imaging_email_html(int p_recId)
- send_imaging_notification(string p_refKey)

Updated:
- mint_referral_id(int recId)
- send_referral_notification(string p_refKey)
- send_3008_notification(string p_refKey)
- build_referral_email_html(int p_recId)
- build_3008_email_html(int p_recId)

Diagnostics:
- diag_pvs_billing_flags()
- diag_find_referral(string p_text)
- diag_safe_test_referrals()
- diag_duplicate_referral_ids()
- diag_sequence_trackers()
- diag_referral_by_name(string p_text)
- diag_referral_origin()
- diag_unmatched_branch_labels()

New form: Referral_Sweep_Log, nine fields. Note the third textarea is
FRun_Detail, not Run_Detail.

--------------------------------------------------------------------------------
## 15. Creator v6 and Deluge facts learned
--------------------------------------------------------------------------------

- A form workflow runs in a transaction. Any later error rolls back every record
  write in that script, but an external call already made cannot be rolled back.
  Never send before the record is committed.
- Writing a value longer than a field's maxchar terminates the insert and rolls
  back the whole script.
- Map key test is containKey, with no s. containsKey does not exist.
- getHour() on a date-time returns 24 hour format in the app timezone.
- toDate() accepts a date-time value directly.
- Creator v2.1 meta APIs cover applications, sections, forms, reports, pages and
  fields only. There is no endpoint for workflows, functions or Deluge, so the
  .ds export is the only source for those and it is admin UI only.
- Referral_Added_Time is not a system field. It is populated by
  backfill_referral_added_time, which copies Creator's Added_Time using the same
  non persisting bare assignment as the broken minters. Read Added_Time directly
  instead.

--------------------------------------------------------------------------------
## 16. Decisions taken
--------------------------------------------------------------------------------

- Autonomous worker write gate: unbilled and unbatched, which on
  Encounter_PatientVisit is the single Invoice_Link test since run_invoice_batch
  writes Invoice_Link. Referrals_Main has no billing state of its own.
- Referral_Date is never defaulted. Form origin only, from Added_Time.
- Notifications refuse to send without a Referral ID from Creator.
- A DOB found in free text is flagged, never written.
- The autonomous worker gets workflow and function code from a .ds that Neil
  exports at session start and EOD; it refuses workflow level judgements when
  that export is stale.
- Cornerstone stays as "Cornerstone - Main" rather than a bare label.
- Batch size for sos_referral_health FIX stays at 2 for now rather than
  optimizing the pre-scans.

--------------------------------------------------------------------------------
## 17. OPEN ITEMS
--------------------------------------------------------------------------------

Blocking or near term:
1. Zoho Form integration rebuild is mid flight. Confirm rows for the three URL
   fields, Form Token, Patient DOB and Partner Location Label, then submit a
   test referral and run sos_referral_health REPORT ALL 5.
2. PVS-1227-JK will be re-invoiced unless held or cancelled.
3. mint_assignment_id, mint_employee_id, mint_partner_id and mint_location_id
   all carry the same bare assignment defect as mint_referral_id. Only
   mint_referral_id has been fixed.
4. Reports still display Patient_DOB1 instead of the parsed Patient_DOB:
   Referrals_Main_Report, PVS_Report, and one page layout with two elements.
   Neil's ruling: every Creator report pulls Patient_DOB, full stop.
5. backfill_patient_dob has not been run. Run diag_dob_coverage first.
6. v45 is stale. A fresh .ds export is needed; Creator changed substantially
   today.

Deferred:
7. Zoho Flow trigger for sweep_unnotified_referrals every 30 minutes, and
   exposing the function as a REST endpoint.
8. The autonomous QA worker itself.
9. 14 NOPARTNER and 58 NOASSIGN legacy unbilled referrals.
10. 12 referrals carrying no branch text at all.
11. 3 PVS records with a blank Employee_Email.
12. DOB candidate scan that reports and never writes.
13. WorkDrive cleanup after file intake, carried from Session 40.

Data issues to adjudicate:
14. Duplicate referral pairs: John Simoneschi REF-1449 and REF-1458; Phyllis
    McCoy REF-1457 and REF-1462; Anneice Halloway REF-073126-1499 and REF-1404;
    Marian Hall REF-072926-1480 and REF-1423.
15. REF-1463 POC email is SpindoraDoyon@accentcare.co, missing the m. A
    Partner_Referral_Contacts record was created under that address.
16. Ramon Anglada Alvarez matches no referral record despite two notifications
    sent 2026-09-11 at 11:38 and 11:40.
17. REF-1129 and REF-1455 still carry the dead "Empath - Main" label.

END
