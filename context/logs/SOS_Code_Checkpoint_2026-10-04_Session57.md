SOS Code - CHECKPOINT - 2026-10-04 (Session 57)
Source of truth: SOS_Referrals_App_2026-10-04_v58.ds. Items marked "saved after v58" are not in the export.

1. ZEPTOMAIL: REF-1596 failed TM_5001/LE_102 Credit exhausted (429). Neil bought credits; failed sends re-run.

2. IMAGING-ONLY NOTIFICATIONS (saved after v58): send_referral_notification no longer skips 3008 / "Imaging Order (only)". resend_referral_notifications gained an "Imaging Order (only)" branch using build_imaging_email_html. REF-1661 resent OK. Known side effect, fix declined for now: the intake flow calls all three senders, so new imaging-only and 3008 referrals get the REF Visit email plus their type email.

3. INVOICE BATCH DUPLICATES (run_invoice_batch guard: Referral_ID + DOS + Complexity_Level), resolved with retire_pvs_duplicate:
- REF-1100: keep PVS-1572-AS, retired PVS-1744-AS (verified).
- REF-1507: keep PVS-1743-AS, retired PVS-1805-JK (verified).
- REF-1445: keep PVS-1522-JK (faxed), retire PVS-1508-JK. COMMIT not yet verified.
Batch released with reset_invoice (voids the Books invoice, no preview).

4. NEW (saved after v58): diag_pvs_note_compare(string p_pvsIds), read-only note comparison.

5. OPEN, BLOCKS BATCH: REF-1621 PVS-1802-JK (Foley) vs PVS-1803-JK (abdominal distention, female patient per note, faxed). Both are under the same patient record, AccentCare - Hillsborough, DOS 09-30, $343 each. 1803 is probably the wrong patient. Waiting on Josh.

6. MISS: shipped the send_referral_notification change before reading the .ds.

REPO: v58 committed. ds_sync v58: DRIFT=4 (Note_Finalized_Stamp, poll_fax_status, send_activity_digest, send_pvs_fax), NEW=1 (diag_addendum_restamp), applied; now EMPTY=4, MATCH=337. MANIFEST regenerated (341 rows).
