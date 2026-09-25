SOS CODE - CHECKPOINT - 2026-09-25 - Session 54 (Cowork)

REPO STATE
- Pushed: 9ae4978 (v54 export), 1236836 (Session 54 main), 75445f6 (hook fix, by ccode).
- This checkpoint adds: context/01_standing_rules.md (single source of truth rule), context/23_task_list.md, functions/diag_pvs_billing_vs_referral.dg, functions/sync_pvs_branch_from_referral.dg, this log.
- New .dg files are not in MANIFEST.tsv until the next .ds export (v55) and ds_sync.

DONE THIS SESSION (all live in Creator and tested by Neil)
1. Partner resolver steps 1 to 7 complete.
   - partner_branch_values, resolve_branch_id, Referral Resolves Partner On Save, PVS Sets Billing Branch On Save (fill blanks), Sender Sets Branch (link only), process_new_referral (uses the resolver; its own label matching removed).
   - NEIL RULING: submitted branch beats the POC contact's saved branch. Resolver order: existing link, exact label, org text as label, contact email.
   - NEIL RULINGS: Referral Link Pre-Fill, Referral Sets Billing Branch, Has Referral_ID Show_Hide and Branch Sets Partner stay unchanged; Branch Sets Partner Link stays inactive.
   - Step 7 backfill (backfill_partner_resolver): referrals 68 changed, 0 unresolved; PVS 83 blank partner fields filled from the referral, 0 left.
   - REF-1500 resolved to InnoVage / Tampa (confirmed). REF-1561 and REF-1590 linked by Neil to Empath - Suncoast - PIN. REF-1560 is a fake test record.
2. Referrals entered directly in Creator now send all staff notifications and the partner confirmation (Added_Time trusted within 10 minutes of creation). Standing rule updated.
3. Partner Contact Lookup hotfix: no longer writes its own trigger field (the form no longer spins; Submit works).
4. Partner confirmation email redesign: patient name + Referral ID in the header, Remarks/Comments section with "Our team has received this referral and is already working on it...", clickable (813) 513-1925 and info@sosreferrals.com.
5. Provider assignment emails: field Notified_Employee_ID, function send_assignment_notification, workflow Assignment Notify Provider (Assignments, Created or Edited, On Success; Neil or Josh only). A new provider gets "New Visit Assignment"; the previous provider gets "Visit Removed"; both are immediate. Link goes to https://portal.sosreferrals.com (home page for now).
6. Assignment_Status dropdown (Assigned / Unassigned, default Unassigned) plus workflow Assignment Status From Provider (On Validate). No backfill: no visits have been assigned yet.
7. Assignments.Patient_Phone max length raised by Neil (was 13; referral phones are 14 characters).
8. Multi-writer field audit: docs/audit/SOS_Multi_Writer_Field_Audit_2026-09-25.md. 72 fields have 2+ live writers; 3 real conflicts (A1 phone format differs by entry path and the formatters throw under 10 digits; A2 Complexity_Charge has 4 live writers with different rules; A3 intake-created Assignments lack Referral_Date / Referral_Partner / Referral_POC). NEIL DIRECTION: change nothing that works; verify with data first.
9. NEIL RULING (standing rule): THE REFERRAL IS THE SINGLE SOURCE OF TRUTH. Every downstream copy derives from it; redundant writers that can disagree are defects.
10. diag_pvs_billing_vs_referral over all referrals: exactly one mismatch. PVS-1757-JK was fixed to AccentCare - Pasco via the new sync_pvs_branch_from_referral (charge unchanged at 343).

LEARNINGS (in context/05)
- No namespace prefix on Default-namespace function headers.
- Full-table loops with per-record thisapp calls hit the statement limit: batch with range and cache lookups.
- An empty "range" or variable-held fetch on Encounter_PatientVisit throws "empty set": iterate fetches inline.
- An on-user-input workflow must never write its own trigger field.
- Use GIT_OPTIONAL_LOCKS=0 for git reads from Cowork.

OPEN (see context/23_task_list.md)
- Staff notification email edits (Visit / 3008 / Imaging): subject by type, preview text, Referral Source without the dash, remove Allergies, footer contact line, keep the header; trace the trailing period on the sender name.
- Phone format defect and conflict A1; conflicts A2 and A3 to verify with data.
- Resolver step 8 (retire the drift backfills) and step 9 (Zoho Form remap).
- Carried from Session 53: != criteria sweep, PVS_Status design decisions, poll_fax_status possibly stalled, PVS-1479 to 1506 empty notes, diag_unfaxed_by_branch fix.
- Next .ds export (v55) plus ds_sync to capture every Session 54 function and workflow.
