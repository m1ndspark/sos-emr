SOS Code - SOS Session Log - October 02, 2026 (Session 56)
Session span: 2026-10-01 to 2026-10-02
Source of truth: SOS_Referrals_App_2026-10-02_v57.ds (repo). Changes made after v57 are listed below as "saved after v57".

SUMMARY
Built daily and weekly activity digest emails (referrals, PVS, compliance scorecard), added Note_Finalized_Time tracking, fixed the stalled fax status poll, repaired 76 fax records, added per-file fax attachment logging, and found Creator strips parentheses from script conditions.

1. ACTIVITY DIGEST (send_activity_digest)
- Signature: send_activity_digest(p_type, p_from, p_to). p_type = referrals, pvs or weekly. Blank dates = rolling defaults; MM/dd/yyyy dates = custom range, hard cutoff at the To date.
- Sends via ZeptoMail (API_Config ZEPTOMAIL) to neil.heird@sosmmc.com only.
- Daily referrals: referrals with Referral_Date = yesterday. Count table by Service (Referral_Type), highest first. Columns: Date, Ref ID, Patient, Service, Reason.
- Daily PVS: completed = Row_Status not Duplicate/Cancelled/Folded, Visit_Status Completed or blank, note Final or Addendum, windowed by Note_Finalized_Time. In Progress = Preliminary notes.
- Weekly: Partner x Service summary (Referrals, Comp PVS), Visit Type counts, Goal Scorecard, Referral Compliance table.
- Goals: Referral to Visit 1 day; Referral to 3008 3 business days (weekends skipped); Visit to PVS 1 day; Visit to Fax 2 days. Statuses judged as of today. On-Time % = On Time / (On Time + Late + Overdue).
- 3008 done = Was_3008_Completed Yes + Cares_3008_Completion_Date.
- Imported PVS with blank Visit_Status + Final note count as completed (report only, no data change).
- Fax = Fax_Log Sent + Fax_Attachments (PVS Note) on Sent faxes.
- Compliance columns: Date, Ref ID, PVS ID, Faxed ?, Patient, Partner, Service, Reason, PVS Date, R to V, Status, Finalized, V to PVS, PVS Status, Notes. Reason = PVS Type_of_Procedures, else referral reason cut to 40 chars.
- Open items look back 30 days from To. Record tables newest first; count tables highest first.
- Schedules (saved after v57): "Activity Digest Daily 6am" daily from 10/03 (referrals + pvs); "Activity Digest Weekly Fri 6am" weekly from 10/09.
- Rewritten after v57 so no condition mixes && and ||.

2. NOTE FINALIZED TIME
- Field Encounter_PatientVisit.Note_Finalized_Time (Date-Time, System Fields).
- Workflow Note Finalized Stamp (Created or Edited, On Validate) stamps the first Final/Addendum save. Rewritten after v57 with nested ifs. diag_addendum_restamp: 0 records affected by the old version.
- Backfill: 109 native records from Added_Time. 387 imported records (import minutes 2026-08-05 11:28 and 2026-09-09 22:47) left blank by decision.

3. FAX FIXES
- Root cause of the 76 stuck Queued faxes: poll_fax_status crashed (Line 56) on a Fax_Log whose PVS no longer existed, so every run aborted.
- poll_fax_status v2 (in v57): missing-PVS guard, max 40 per run, blank RC reply = error (row stays Queued), Completed_Time = RC lastModifiedTime converted from UTC.
- poll_fax_status v3 (saved after v57): also stamps Fax_Status on every PVS in Fax_Attachments for the fax.
- repair_fax_log_status: all 76 corrected to Sent with real RC delivery times. RC rate limit CMN-301 hits around 40+ calls per minute.
- send_pvs_fax (saved after v57): writes Fax_Attachments rows (PVS Note + each upload) and Attachments_Included. Test fax FAX-100226-1086 confirmed.
- Older repaired faxes have blank Page Count; backfill declined.
- Pre-09/22 faxes and RC desktop-app faxes (17 since 09/01, batched, no file names) have no Creator record. Handling undecided. Deluge OCR exists (zoho.ai.recognizeText, PDF up to 20 MB, 40s timeout); PDF matching declined for now.

4. FINDINGS
- 72 native September 3008 referrals (09/02-10/01) have no 3008 PVS; Neil confirms done but never entered. REF-1499 Was_3008_Completed blank. Parked; reminder set for Mon 10/05 9:00 AM ET.
- Zoho Forms recovered referrals carry old Referral_Date; the report keys on Referral_Date.
- 197 imported July PVS have blank Visit_Status; 213 native 3008 PVS have no note type (by design).

5. LEARNINGS (added to context/05_deluge_learnings.md)
- Statement limit on full-history report loops: always narrow fetches with a date window.
- Creator strips parentheses in script conditions (not in record criteria): never mix && and || in one expression.
- Existing rule reconfirmed: no for-each directly over an expression.

6. REPO
- v57 export committed. Checkpoint e319cc4, ds_sync c9868ca, workflow + MANIFEST b0b098d (pushed by ccode).
- This EOD log + task list + learnings edits committed; push pending (ccode).

7. OPEN / NEXT SESSION
- September 3008 catch-up list from Neil (ask Mon 10/05).
- Decide reporting for pre-09/22 and desktop-app faxes.
- Fresh .ds export to capture post-v57 changes (schedules, stamp workflow, digest, poll v3, send_pvs_fax).
- Watch the first daily emails (10/03) and the first weekly (10/09).
- ccode open questions: diag_referrals_no_pvs deleted in Creator (remove from repo?); stale MANIFEST hashes for poll_fax_status and send_fax_digest (full refresh?).

8. MISSES THIS SESSION
- Didn't read 05 learnings before full-history loops.
- For-each over an expression despite the existing rule.
- Wrongly ruled out the RC rate limit.
- Said Deluge can't OCR; it can.
- Repair skipped Page Count.
- Mixed and/or conditions before knowing Creator strips parentheses.
