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

END
