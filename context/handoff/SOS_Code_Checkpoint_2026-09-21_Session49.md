# SOS Code Checkpoint, 2026-09-21, Session 49

Mid-session checkpoint. Covers work since the Session 48 checkpoint
(context/handoff/SOS_Code_Checkpoint_2026-09-17_Session48.md).
Scope set by Neil: August 3008 invoices only. July is out of scope.

--------------------------------------------------------------------------------
## 1. Defect: August 3008 invoices sent with blank NAME and MRN
--------------------------------------------------------------------------------

INV-000091 (InnoVage - Tampa, 12 visits, $2,100, sent 2026-09-20) printed a
blank NAME and MRN on every visit block, and a blank REF DATE on 10 of 12.

Cause, verified: create_invoice_from_selection (v47) builds each visit block
from the PVS record itself. NAME = Patient_Full_Name_1, MRN =
Patient_Hospice_ID, REF DATE = the linked referral's Referral_Date. On the
affected PVS those fields and Referral_Link were blank. No earlier fix covered
this: the Session 48 relink touched 5 Patient Visit records only, and
create_3008_pvs_july (the only 3008 creator in the repo) fills both fields.

Books search (item name contains 3008) returned 10 invoices. Diagnostic across
all 10:

| Invoice | Branch | Visits | Total | State before repair |
|---|---|---|---|---|
| INV-000090 | InnoVage - Orlando | 9 | $1,575 | Name/MRN blank all 9, 7 unlinked |
| INV-000091 | InnoVage - Tampa | 12 | $2,100 | Name/MRN blank all 12, 10 unlinked |
| INV-000094 | InnoVage - Orlando | 32 | $5,600 | Name/MRN blank all 32, all unlinked |
| INV-000095 | InnoVage - Tampa | 28 | $4,900 | Name/MRN blank all 28, all unlinked |
| INV-000088, 089, 092, 093 | both | 5 | $875 | Clean |
| INV-000056, 057 (July) | both | 76 | $13,300 | Names present, MRN blank on PVS and referral (out of scope) |

All 81 affected PVS: IDs end in "--M" (minted with no employee initials),
Added_User sosmmc, Added_Time 2026-09-20 14:39 and 21:11/21:27.
Patient_Full_Name_2, first/last name, DOB and Referral_ID text were filled.
Creation path is NOT identified. Open, blocking before the next 3008 batch.

All 8 August invoices were already emailed to InnoVage on 2026-09-20.

--------------------------------------------------------------------------------
## 2. Functions written (live in Creator only, not in the repo .ds)
--------------------------------------------------------------------------------

diag_invoice_patient_gaps(string p_invoiceNumbers)                NEW, read only
  Comma-separated Books invoice numbers. Per PVS on each invoice: PVS_ID,
  type, Added_User/Time, blank or filled flags for both full-name fields,
  first/last, Patient_Hospice_ID, Referral_ID, PVS_Referral_ID, Referral_Link,
  and the linked referral's name/MRN. Subtotals and a grand total. No PHI
  printed.

repair_invoice_pvs_from_referral(string p_invoiceNumbers, string p_mode)  NEW
  PREVIEW / COMMIT. Scoped to PVS on the named invoices only. Resolves the
  referral by Referral_Link, else by Referral_ID text. Guards: CONFLICT when
  link and text point to different referrals (no write); DOB BLOCKED when PVS
  DOB differs from referral DOB or referral has none (no write). Fills blanks
  only: both full-name fields, first, MI, last, DOB, gender, hospice ID,
  reason, and Referral_Link when resolved by text. Never touches billing,
  branch or invoice fields. Prints a full TRACE.

diag_pvs_referral_match(string p_pvsIds)                           NEW, read only
  Per PVS: DOB, DOS, Referral_ID text, linked referral and text referral with
  DOB/type/date/branch, and every referral whose Patient_DOB matches.

set_pvs_referral_link(string p_pvsId, string p_refId, string p_mode)       NEW
  PREVIEW / COMMIT. Sets Referral_Link only, by custom IDs, after a DOB match.
  Exists because changing Referral Link in the form clears patient fields.

--------------------------------------------------------------------------------
## 3. Repair results
--------------------------------------------------------------------------------

1. First repair PREVIEW exposed a defect in my first version: it misread the
   link on PVS-1578/1581/1582. Rewritten with the trace and guards above
   before any COMMIT.
2. COMMIT on INV-000090/091/094/095: 78 written, 3 held.
3. PVS-1660--M: DOB century typo on the PVS (20xx vs 19xx). Neil corrected it
   in Creator; re-run on INV-000094 wrote the name. MRN stays blank because
   referral REF-072326-1422 has none.
4. PVS-1580--M: link pointed to REF-1251, text said REF-1255. Both referrals
   carry the same patient DOB; REF-1255 is dated the same day as the visit,
   REF-1251 the day after. Neil approved REF-1255. Changing the link in the
   form cleared the patient fields (not saved), so set_pvs_referral_link was
   used instead. Repair then wrote name and MRN.
5. Verified with diag_invoice_patient_gaps after COMMIT.

Current state of the 81: 80 repaired. PVS-1579--M still held.

--------------------------------------------------------------------------------
## 4. Open
--------------------------------------------------------------------------------

1. PVS-1579--M: Referral_ID text REF-1251 does not match its DOB. Only DOB
   match is REF-1372 (InnoVage - Orlando), already linked to PVS-1658--M on
   INV-000094. Possible double billing. Next: diag_pvs_referral_match with
   PVS-1579--M,PVS-1658--M. BLOCKING the rebill.
2. Void and rebill INV-000090, 091, 094, 095 via reset_invoice and a new
   Invoice Batch per branch, verify each, send the void-and-rebill notice
   (notice mechanism is still the open Batch_Reason / Replaces_Invoice_Number
   task). BLOCKING.
3. Identify and fix the August 3008 PVS creation path. BLOCKING before the
   next 3008 batch.
4. Form behaviour: changing Referral Link on an existing PVS clears patient
   fields. Referral_Link_Pre_Fill is on add only in v47; clearing workflow
   unidentified. Not blocking.
5. REF-1251 / REF-1255 possible duplicate referral. Not blocking.
6. Fresh .ds export to capture the four new functions. Repo .ds is v47.

--------------------------------------------------------------------------------
## 5. Addendum, 2026-09-22: all 81 repaired
--------------------------------------------------------------------------------

1. .ds v51 (exported 2026-09-22 06:35) saved to repo root as
   SOS_Referrals_App_2026-09-22_v51.ds and refreshed SOS_Referrals_App.ds.
   All four Session 49 functions are in it. v51 is now the authoritative
   source for them. Needs ccode commit.
2. --M suffix explained by v51: backfill_pvs_ids mints PVS-<seq>-<initials>
   and appends -M whenever Has_Referral_ID is not Yes. The 81 had blank
   Employee_Initials and Has_Referral_ID not Yes despite Referral_ID text.
   Consistent with an import that fired no form workflows and skipped the
   link step. Inferred from code, the import itself is unverified.
3. PVS-1579--M resolved. It is not a duplicate of PVS-1658--M. Referral
   record REF-1251 (InnoVage - Tampa) carried the DOB of REF-1255
   (InnoVage - Tampa), two different patients with the same first name and
   referral dates one day apart. Source of truth: Cognito intake export
   REF-081926-1653. Neil corrected Patient_DOB1 and Patient_DOB on REF-1251.
   set_pvs_referral_link linked PVS-1579--M to REF-1251; repair filled name
   and MRN.
4. Duplicate PVS shells found and confirmed already held (Hold From
   Invoicing = Yes, Row Status Duplicate): PVS-1603--M (dup of PVS-1579--M on
   REF-1251) and PVS-1604--M (dup of PVS-1580--M on REF-1255).
5. run_invoice_batch (v51) does NOT check Row_Status. It skips only
   Hold_From_Invoicing = Yes, already-invoiced, and Visit Cancelled. Marking
   a PVS Duplicate alone does not stop it billing.
6. New read-only function diag_referral_id_records(string p_refIds): lists
   every Referrals_Main record holding each REF ID with DOB, DOB text, type,
   branch, and every PVS linked to it. Live in Creator only, not in v51.
7. Verified with diag_invoice_patient_gaps: 81 PVS, Name_1 blank 0,
   MRN blank 1 (PVS-1660--M, referral has none), No Referral_Link 0.

Next: void and rebill INV-000090, 091, 094, 095.

--------------------------------------------------------------------------------
## 6. Addendum, 2026-09-22: void and rebill done
--------------------------------------------------------------------------------

1. diag_3008_draft_vs_invoiced(date p_from, date p_to) NEW, read only. For
   8/1 to 8/31: 59 uninvoiced August 3008 PVS, all DUPLICATE of an invoiced
   PVS (same Referral_ID + DOS), 0 NO MATCH, all 59 already held. 19 blank
   shells (PVS-1605--M to PVS-1622--M, plus PVS-1603--M) have no DOS and
   cannot batch. Not in v51.
2. run_invoice_batch (v51) skips Hold_From_Invoicing = Yes BEFORE its
   duplicate guard, so held duplicates do not stop a batch.
3. reset_invoice(invoice number, "RESET") run on INV-000090 (9), INV-000091
   (12), INV-000094 (32), INV-000095 (28). All four voided in Creator and
   Books; 81 visits returned to Draft.
4. Rebilled one invoice per branch, Invoice Batch 8/1 to 8/31, no cap:
   INV-000096 InnoVage - Orlando, 41 visits, $7,175.00
   INV-000097 InnoVage - Tampa, 40 visits, $7,000.00
   Total $14,175, matches the voided four.
5. Verified with diag_invoice_patient_gaps: INV-000096 Name_1 blank 0, MRN
   blank 1 (PVS-1660--M), no link 0; INV-000097 all 0.
6. Not yet emailed to InnoVage. Void-and-rebill notice is manual (Batch_Reason
   still unbuilt).

--------------------------------------------------------------------------------
## 7. PAUSED 2026-09-22 ~11:00, resume here
--------------------------------------------------------------------------------

Neil decided: ONE August 3008 invoice per InnoVage branch. My error: I voided
only the four broken invoices and left INV-000088/089/092/093 active without
clearing that with Neil.

Resume plan (nothing in it has started):
1. reset_invoice with RESET, one at a time: INV-000088, INV-000089,
   INV-000092, INV-000093 (sent, active) and INV-000096, INV-000097 (Books
   Drafts, unsent). Unverified whether Books voids a Draft; stop on any Books
   error.
2. Invoice Batch InnoVage - Orlando, 08-01-2026 to 08-31-2026, no cap.
   Expect 45 visits, $7,875.00.
3. Invoice Batch InnoVage - Tampa, same window. Expect 41 visits, $7,175.00.
4. diag_invoice_patient_gaps on both new invoices.
5. Set Terms Net 30 on both (096/097 came out due same day), then email with
   a revised void-and-rebill notice naming every voided number.
July INV-000056/057 are out of scope and stay.

--------------------------------------------------------------------------------
## 8. Addendum, 2026-09-22 12:35: one invoice per branch, DONE
--------------------------------------------------------------------------------

1. reset_invoice run on INV-000088 (2), INV-000089 (1), INV-000092 (1),
   INV-000093 (1), INV-000096 (41, Books Draft voided OK), INV-000097 (40).
2. Orlando batch STOPPED on duplicate guard: PVS-1740-JK / PVS-1670--M, same
   visit (REF-1292, DOS 2026-08-17). It had been billed twice on 9/20, on
   INV-000092 and INV-000094, because the guard only checks within one batch
   run. Neil kept PVS-1740-JK and held PVS-1670--M.
3. Final August 3008 invoices:
   INV-000098 InnoVage - Orlando, 44 visits, $7,700.00
   INV-000099 InnoVage - Tampa, 41 visits, $7,175.00
   Total $14,875.00, 85 visits.
4. diag_invoice_patient_gaps: PVS 85, Name_1 blank 0, MRN blank 1
   (PVS-1660--M, referral has none), No Referral_Link 0.
5. Voided in total: INV-000088, 089, 090, 091, 092, 093, 094, 095, 096, 097.
6. Net 30 set by hand (due 2026-10-22, confirmed in Books). Both invoices
   emailed and the void-and-rebill notice sent by Neil 2026-09-22. CLOSED.

END
