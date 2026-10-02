SOS Code - CHECKPOINT - 2026-10-02 (Session 56, started 2026-10-01)
Source of truth: SOS_Referrals_App_2026-10-02_v57.ds (committed this checkpoint)
Checkpoint commit: e319cc4. ds_sync v57 committed c9868ca.
Workflow Note Finalized Stamp | Form Encounter_PatientVisit | Created or Edited | On Validate | Added 2026-10-01, Session 56 (saved from v57 .ds).

1. ACTIVITY DIGEST EMAILS (send_activity_digest)
- New function send_activity_digest(p_type, p_from, p_to). Types: referrals, pvs, weekly. Blank dates = rolling defaults; MM/dd/yyyy dates = custom range with hard cutoff at To. LIVE in v57.
- Delivery via ZeptoMail (API_Config ZEPTOMAIL), to neil.heird@sosmmc.com only.
- Daily referrals: Referral_Date = yesterday; columns Date, Ref ID, Patient, Service, Reason; "Referrals by Visit Type" count table on top (highest first).
- Daily PVS: completed = Visit_Status Completed or blank, note Final/Addendum, Row_Status not Duplicate/Cancelled/Folded, windowed by Note_Finalized_Time; In Progress = Preliminary.
- Weekly: Partner x Service summary (Comp PVS), Visit Type counts, Goal Scorecard, Referral Compliance table (newest first). Open items: last 30 days back from To.
- Goals: Referral to Visit 1 day; Referral to 3008 3 business days (weekends only); Visit to PVS 1 day; Visit to Fax 2 days. Statuses judged as of today.
- 3008 done = Was_3008_Completed Yes + Cares_3008_Completion_Date. Imported PVS (blank Visit_Status + Final) treated as completed, report-only.
- Fax counted from Fax_Log Sent + Fax_Attachments (PVS Note) on Sent faxes.
- Compliance column order: Date, Ref ID, PVS ID, Faxed ?, Patient, Partner, Service, Reason, PVS Date, R to V, Status, Finalized, V to PVS, PVS Status, Notes. Reason = PVS Type_of_Procedures, else referral reason capped at 40 chars.
- Scorecard heading "Imported ?". Tables fit content; Reason wraps 250px.

2. NOTE FINALIZED TIME
- New field Encounter_PatientVisit.Note_Finalized_Time (Date-Time, System Fields). LIVE.
- New workflow Note Finalized Stamp (Created or Edited, On Validate): stamps first Final/Addendum. LIVE.
- Backfill: 109 native records set from Added_Time; 387 imported (import minutes 2026-08-05 11:28 and 2026-09-09 22:47) left blank by decision.

3. FAX POLLING FIXES
- Root cause of 76 stuck Queued faxes: poll_fax_status crashed (Line 56) on a Fax_Log whose PVS no longer existed; every run aborted.
- poll_fax_status v2 LIVE: missing-PVS guard, max 40 per run, blank RC reply = error (row stays Queued), Completed_Time = RC lastModifiedTime (UTC via toTime(...,"UTC")).
- repair_fax_log_status run: all 76 now Sent with real RC delivery times. RC rate limit CMN-301 hit at ~40-76 calls/min.
- Learned: Creator faxes are single-PVS (only 1 bundled fax exists); pre-09/22 faxes and 17 RC desktop faxes since 09/01 have no Creator record, no file names, batched.
- NOT YET LIVE: poll_fax_status v3 (stamps Fax_Status on every PVS in Fax_Attachments for bundled faxes); send_pvs_fax update (writes Fax_Attachments + Attachments_Included for PVS note and every uploaded file). Code delivered in chat; Neil to paste/test.

4. DIAGNOSTICS ADDED (read-only)
diag_pvs_added_time_clusters, diag_compliance_gap, diag_pvs_status_mix, diag_fax_coverage, diag_stuck_faxes, diag_fax_repair_errors, diag_3008_overdue, diag_3008_no_pvs_list, diag_rc_fax_history, diag_fax_attachments.

5. FINDINGS
- 72 native September 3008 referrals (09/02-10/01) have no 3008 PVS; Neil confirms done but never entered. REF-1499 has Was_3008_Completed blank. Catch-up PARKED pending Neil's list.
- Zoho Forms recovered referrals carry old Referral_Date; report now keys on Referral_Date.
- Deluge OCR exists (zoho.ai.recognizeText, PDF <=20MB, 40s timeout); Neil declined PDF matching for desktop faxes for now.

6. OPEN / NEXT
- Paste + save schedule "Activity Digest Daily 6am" (not in v57).
- Build Friday 6am weekly schedule.
- Paste/test send_pvs_fax attachment logging and poll_fax_status v3.
- Decide handling of pre-09/22 / desktop-app faxes in report.
- September 3008 catch-up (ask Neil Mon 10/05).
- Stamp Fax_Status on the 2 PVS in the one bundled Sent fax (optional).

7. MISSES THIS SESSION
- Did not read 05_deluge_learnings before writing full-history loops (statement limit, second instance).
- for-each over expression (diag_rc_fax_history) despite existing learning.
- Wrongly ruled out RC rate limit on 8 errors; it was CMN-301.
- Told Neil Deluge cannot OCR; it can.
