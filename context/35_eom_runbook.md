# SOS EOM Prep Runbook

Draft 2026-11-16 (Session 64). Compiled from every EOM, billing and data rule on record:
context/01, 07, 11, 17, 25, 30, 33, 34; docs/billing; context/logs S28-S63; project docs
(Rebill Resume 09-22, S49); project memory (ways-of-working, preferences, sos-emr, turnaround
goals, parked items); October 2026 EOM session. IDs only, no patient data.

--------------------------------------------------------------------------------
## 0. Standing rules (apply to every step)
--------------------------------------------------------------------------------
1. EOM prep is Claude's job in SOS Code; it starts on the 25th or whenever Neil says EOM.
2. Current month first; prior months are billed, and prior-month adjustments wait until EOM is officially closed.
3. No prior-month data-integrity work unless urgent; park it on the post-close list (step D4).
4. Records on referrals from months whose books are closed are skipped.
5. Deadline: a month's billing is complete within 3 business days of month end.
6. SOS Finance only ever receives vetted data; billing rules, AR and reconciliation stay with Finance.
7. Every data point is read live from Creator at the moment of output, never remembered or computed.
8. Every count is reported with its list and patient names.
9. Whenever revenue looks low or items are open, state the open items with count, names and dollar impact.
10. Action lists hold only records Neil must act on; nothing goes to Neil unchecked.
11. Before classifying, billing or flagging any PVS, read what the clinical note says was done.
12. Before flagging a duplicate, check dates, notes, patient details and linked records.
13. Writes: Claude shows before -> after per record, Neil approves, Claude writes with form workflows skipped, then re-reads to confirm.
14. Bulk writes use PREVIEW/COMMIT functions; Neil reads PREVIEW before COMMIT; Neil can say "done" and Claude verifies.
15. Any single-record fix also comes with the batch version for every record matching the same query.
16. After findings, stop and wait; code only after Neil says go.
17. Report and email tables sort newest first; count tables sort highest first.
18. Spreadsheets for Josh and the providers, not more email.

--------------------------------------------------------------------------------
## A. Data completeness (current month, 1st to last day)
--------------------------------------------------------------------------------
A1. Referrals missing a PVS (first check of every EOM)
1. Run diag_referrals_missing_pvs(p_from, p_to) or read API_Referrals_All against API_PVS_All.
2. Split the result into Patient Visit, 3008 and Imaging Order (only), each with names and dollar impact.
3. Patient Visit gaps go to Josh as a spreadsheet (Seen?, Visit Date, Provider, Notes), with portal links on the Referral IDs.
4. Imaging-only gaps go to Neil/Josh: the PVS is completed when results are faxed to the partner; a missing one is a process miss.
5. Imaging-only referrals need no provider assignment.
6. Unbilled until resolved; supplemental invoices follow once PVS exist.

A2. 3008 reconciliation
1. Count the month's 3008 referrals, completed 3008 PVS and open 3008s; show open count x $175.
2. 3008s are InnoVage only; a 3008 on any other partner's referral is a data-entry error.
3. Providers no longer send a monthly spreadsheet (stopped Oct 2026), so the recap email is the collection tool.
4. Run send_3008_status(p_from, p_to, "No") to preview to Neil only, then "Yes" on Neil's go (first business day of the month).
5. Recap is personalized: each provider sees only her records, unassigned shows "Unassigned", Neil gets the full copy; the update template xlsx is attached; live sends log to Notification_Log.
6. Hardcoded recipients: Ann Smith, Kayla Kolanko, Neil.
7. For completions received, run create_3008_pvs(pMode, pRows) PREVIEW then COMMIT, rows "REF-xxxx|MM-dd-yyyy|First Last;".
8. Bill on the completion date, not the referral date.
9. The referral's branch wins over any log's location.
10. Match providers on first AND last name (Kolanko is ambiguous between Joshua and Kayla).
11. InnoVage patients have no hospice ID; never flag it. 3008s may leave Procedure and Diversion blank.
12. 3008 done = Was_3008_Completed Yes + Cares_3008_Completion_Date; goal is 3 business days from referral.
13. Deluge inserts skip form workflows: after any bulk PVS insert, confirm Partner_Location_Label, Referral_Date, Referral_Source, Row_Status, Visit_Status and SSN are filled (create_3008_pvs now sets them; backfill_pvs_system_fields_range covers gaps).

A3. Assignment and visit-outcome check (excludes imaging-only)
1. Every referral in the month has an Assignments record with a provider (Employee_Link) or a recorded outcome.
2. Outcome lives on Assignments: Visit_Completed No/Yes; if No, Not_Completed_Reason (Cancelled by Partner, Cancelled by Patient, Cancelled by SOS, Duplicate Referral).
3. A referral counts as assigned when Employee_Link is set.

A4. Duplicate check
1. Match on patient name + DOB within 7 days either side of the visit or referral.
2. Verify before flagging: dates, note text, patient details, linked records.
3. InnoVage sends one referral per patient; a second is usually a double submission (Aug 2026 billed twice).
4. Not duplicates: a telemed imaging-coordination visit plus a separate intervention visit; HeartWorks IV cases carrying 2 charges (telemed coordination + complexity level).
5. Retire confirmed duplicates with retire_pvs_duplicate or retire_pvs_duplicate_pairs (Row_Status Duplicate, Hold Yes); set the duplicate referral's outcome to Duplicate Referral.
6. run_invoice_batch also stops on any pair with the same Referral + DOS + Complexity_Level.

A5. Required fields and dateless PVS
1. Run audit_month_integrity(p_mode, p_from, p_to) in modes PVS, BILLING, REFERRALS, DATELESS.
2. Patient Visit and Imaging Order need Visit_Completion_Date (imaging = coordination date); 3008 needs Cares_3008_Completion_Date.
3. run_invoice_batch selects by Visit_Completion_Date, so a dateless PVS never batches.
4. Dateless PVS go to Josh for a date or retirement.
5. Run diag_invoice_patient_gaps after batching: a blank name or MRN prints blank on the invoice.

A6. Patient and referral data
1. Cognito trumps Creator for patient data, as long as the original Cognito data is kept.
2. Referral_Date stays the Creator submission date, even when Cognito was earlier; never defaulted, never an import date.
3. A value found in free text (DOB in a note) is surfaced for approval, never written automatically.
4. Watch for the import defects: 20xx-century DOBs and dropped "De"/"De La" surname particles.
5. Placeholder DOBs (10/10/1010) clear the Missing DOB flag, so list them by name until replaced.
6. Home vs Facility mismatches between referral and PVS are not flagged.

A7. Branch accuracy (the Sept 2026 rebill lesson)
1. Run fix_pvs_branch_batch PREVIEW over the month's PVS: billing branch vs referral branch.
2. The referral is the single source of truth; sync_pvs_from_referral fills PVS blanks from it.
3. The submitted branch beats the POC contact's saved branch.
4. Billing follows the patient's location, not the referrer's.
5. No check yet compares branch to patient ZIP/county; review any branch that looks wrong before batching.

A8. Classification
1. Imaging-coordination PVS: Type_of_Entry = Imaging Order, Complexity "Telemedicine" (SOS coordinated the vendor).
2. A PVS with -NH initials is a test, not a visit.
3. A "False Patient" visit is excluded from counts, not just unbilled.
4. Notes still holding template [placeholders] go to Josh before billing.

A9. Row_Status and Hold
1. Visit Cancelled = Row_Status Cancelled + Hold_From_Invoicing Yes; cancelled visits are never counted or billed.
2. Services billed at $0 (No Charge) are counted and billed; Books shows $0 lines.
3. run_invoice_batch skips only Complexity "Visit Cancelled", Hold Yes and already-linked rows; it does not read Row_Status, so every non-Counted row needs Hold Yes.
4. Test and bogus records are deleted only with Neil's approval.
5. Null trap: Hold_From_Invoicing != "Yes" drops blank-Hold rows; always run a second query for blank Hold.
6. Imported rows land with Hold Yes; release after review.

A10. Charges and rates
1. Complexity_Charge is stamped at lookup and does not follow a rate change; reprice Draft only (reprice_pvs_batch, reprice_draft_pvs), never invoiced rows.
2. Rate changes are forward only; sent invoices stay as billed.
3. Current Empath card (eff 10/01/2026): Telemedicine 65, Low 170, Moderate 373, High 575, Hospital at Home 1,099/day, After Hours 150, Super STAT 400.
4. 3008 = $175 flat, InnoVage only; non-InnoVage 3008 rate rows are Inactive and the batch stops on them.
5. Premiums (After Hours, Super STAT) and equipment are provider-entered on the PVS; nothing auto-applies from Priority.
6. Hiding a charge field does not clear it; set or clear equipment with set_pvs_equipment_charge.
7. diag_partner_rates reports a branch with no rate; the batch stops on a missing or inactive rate.
8. Rate lookup selects Current_Rate == Yes.

--------------------------------------------------------------------------------
## B. Batch readiness
--------------------------------------------------------------------------------
1. Every billable PVS in the month is Draft, unheld, Counted, dated and priced; report anything else by name.
2. Run both checks: Draft + Hold != Yes + Row_Status != Counted, and the same with Hold blank.
3. Run preview_invoice_batch_pool(p_branchLabel, p_from, p_to) per branch to see exactly what will batch.
4. Run diag_unbilled_visits(p_from, p_to, p_partner) for gaps.
5. Give Neil the outstanding summary: open items, names, dollar impact; then ask "ready to batch?".

--------------------------------------------------------------------------------
## C. Invoicing
--------------------------------------------------------------------------------
1. Neil batches in Creator; one Invoice_Batch record per branch, one branch at a time, verify each Result_Message before the next.
2. Empath: Max Invoice Total 2999 on every Empath branch (under $3,000 per invoice); repeat until no visits are left behind.
3. AccentCare and the others: no cap, one invoice per branch per cycle.
4. Visits batch in Visit_Completion_Date order; one visit is one line.
5. Invoices post to Books with Net 30 (payment_terms in the payload); Creator marks PVS Final with Invoice_Link.
6. A failed or wrong batch is replaced, not edited: reset_invoice(p_invoiceNumber, "RESET") voids in Books and returns PVS to Draft, then re-batch.
7. Void and rebill: the revised invoice keeps the original invoice and due dates, adds Revision_Date and a REVISED note, and carries Batch_Reason and Replaces_Invoice_Number.
8. One explanation email per partner from Neil's own inbox for a void and rebill; late or supplemental invoices need none.
9. Verify every invoice line by line in Books; Neil reviews and sends.
10. Late items (A1, A2) go out as supplemental invoices once their PVS exist.

--------------------------------------------------------------------------------
## D. Close-out
--------------------------------------------------------------------------------
1. Live 3008 recap sent (A2.4) and Josh follow-up spreadsheet delivered.
2. Hand Finance the vetted month: billed total by partner, open items with dollar impact, Finance flags (payments, credits).
3. Credits owed (e.g. a test visit billed) go on the next month's billing once the original invoice is paid.
4. Post-close list: prior-month items found during EOM, worked only after close.
5. MPU runs only after the month's data is released (context/33 Gate 10); MPU filters Referral_Source == Contracted Partner and uses the rate actually billed.
6. Session close: fresh .ds export committed, CHECKPOINT/EOD logs, Apple Notes log, context/23 task list.

--------------------------------------------------------------------------------
## E. Imports during the month (when Cognito or any file enters)
--------------------------------------------------------------------------------
1. Follow context/33 gates 0-10; the round-trip diff (Gate 8) is never skipped.
2. Never map into a lookup; import text, then resolve.
3. Imports fire no workflows: run run_import_backfills PREVIEW then COMMIT.
4. Imported PVS land with Hold Yes and are released after review.

--------------------------------------------------------------------------------
## Flags
--------------------------------------------------------------------------------
- create_3008_pvs, send_3008_status and copy_pvs_ssn_from_referral are live but not in the committed .ds (v68); export needed.
- Open: run_invoice_batch Row_Status skip (task 8); branch vs ZIP/county check; auto Row_Status Cancelled on Visit Cancelled; VITAS rates vs contract.
