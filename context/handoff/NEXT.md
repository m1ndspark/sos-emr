# Next

Set by ccode at the Session 49 checkpoint, 2026-09-21. Source:
context/handoff/SOS_Code_Checkpoint_2026-09-21_Session49.md

## Top open item, blocking

1. Resolve PVS-1579--M. It is the one PVS of 81 still held after the August
   repair. Its Referral_ID text says REF-1251 but its DOB does not match
   REF-1251. The only DOB match in Referrals_Main is REF-1372, InnoVage -
   Orlando, which is already linked to PVS-1658--M on INV-000094. That is a
   possible duplicate of one patient billed across Tampa and Orlando. Run
   diag_pvs_referral_match with PVS-1579--M,PVS-1658--M and compare the dates
   of service before writing anything. If it is one patient on two branches,
   the rebill totals change, so this comes first.

2. Then void and rebill the four August 3008 InnoVage invoices: INV-000090,
   INV-000091, INV-000094, INV-000095. 81 visits, $14,175, all emailed
   2026-09-20 with a blank NAME and MRN. The PVS data is repaired but Books is
   untouched, so each invoice stays wrong until it is reset_invoice'd and
   re-batched per branch. Verify each replacement, then send InnoVage the void
   and rebill notice. INV-000088, 089, 092 and 093 are clean and stay.

## Also open, not blocking this item

3. The creation path behind the 81 --M PVS is unidentified. Blocking before the
   next 3008 batch, not before the rebill.

4. Fresh .ds export needed. The repo is still on
   SOS_Referrals_App_2026-09-12_v47.ds and the root SOS_Referrals_App.ds is
   byte-identical to it. A v49 export was provided in chat on 2026-09-17 and
   never written into the repo, so there is no v48 or v49 file here. Four
   functions therefore exist only in Creator and are not under version control:
   diag_invoice_patient_gaps, repair_invoice_pvs_from_referral,
   diag_pvs_referral_match, set_pvs_referral_link. Verified 2026-09-22: each
   returns grep count 0 against v47 and 0 in functions/. The next export must
   capture all four.

Full task list: context/23_task_list.md
