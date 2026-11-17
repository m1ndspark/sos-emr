# SOS Code - Checkpoint - 2026-11-16 - Session 65b

Covers work after the Session 65 EOD log (same day, 18:00 to 20:10 ET). IDs only, no PHI.
Topic: partner remittance (ACH) close-out automation in Creator + Zoho Books.

## 1. Starting state (verified)
- Books held only 2 customer payments ever (InnoVage ref 113225, entered by hand 10/23).
- 114 unpaid invoices, $249,206 open balance. Empath and AccentCare remits arrive by email weekly; none recorded since August.
- Remit_Intake form + Remit Intake Read workflow + remit_build_allocation existed from 10/23 (read and propose only, 4 InnoVage test records).

## 2. Decisions (Neil)
- Payment ledger = Zoho Books (not QBO).
- Upload path only for now; email intake (remits@) skipped. Option kept: Zoho Mail inbox polled by Creator via Mail API (Flow email trigger attachment handling not documented).
- Review happens in Creator before posting (Books has no draft payments).
- Remit email dropped; the record opens on screen instead.
- Deposit match runs right after posting, plus a retry at 7 AM and 7 PM daily.
- New Remit_Status choice "Deposit Matched" (Posted = waiting for deposit).
- Remit Intake is back end only; no portal access.
- Deposit account: Books "Business Essential Checking" account_id 7971487000001533008 (checking ending 0750).

## 3. Built (all live)
| Item | Type | Notes |
|---|---|---|
| remit_post_payments(string p_mode, string p_remitId) | New function | Re-validates split vs Books, one customer payment per Books customer, bank transfer, ref = remit ref, account 0750. Then calls remit_match_deposit. |
| Remit Intake Read (Remit_Intake, Created, On Success) | Updated workflow | Added openUrl("#Report:All_Intakes?ID=" + v_id) as last line. |
| remit_build_allocation(string p_remit_id) | Updated function | Email removed; logic unchanged. |
| Approve & Post (All_Intakes detail view, custom action) | New report workflow Remit_Approve_And_Post | Shows only when Remit_Status = Ready to Approve; confirmation "Post this payment to Books?". Script calls remit_post_payments COMMIT, info result. |
| diag_remit_deposit(date p_from, date p_to, string p_remitId) | New diag | Read-only; lists feed deposits and Books match candidates. |
| remit_match_deposit(string p_mode, string p_remitId) | New function | Finds uncategorized deposit = remit total (payment date -3 to +10 days), gets candidates via match lookup filtered by reference_number, matches customer_payment items, sets Deposit Matched. |
| remit_match_pending(string p_mode) | New function | Loops Remit_Status = Posted, calls remit_match_deposit. |
| Schedules Remit Deposit Match AM / PM | New schedules | 7:00 AM and 7:00 PM daily, remit_match_pending("COMMIT"). |
| Remit_Status choice "Deposit Matched" | Field choice added | |

## 4. Live results (verified in Books and Creator)
- AccentCare EFT0095346, $3,998, 11/10: 4 payments (#3-#6), INV-000059 to 063 paid, deposit 7971487000003165009 matched (via remit_match_deposit COMMIT). Intake 4904890000001130002 = Deposit Matched.
- Empath EFT-00028713, $19,562, 11/13: 5 payments (#7-#11), INV-000118, 120, 121, 123, 124, 125, 126, 132, 133, 135 paid, deposit 7971487000003209004 matched in the same click. Intake 4904890000001130004.
- Record auto-opened when uploaded via + Add on All Intakes.

## 5. Learnings
- Books customer payments have no draft state; a created payment applies immediately.
- Books match lookup with reference_number returns the posted customer payments (type customer_payment); their match transaction IDs differ from payment IDs. Use the lookup IDs to match.
- Books bank list date filter appears unreliable; filter date and amount again in the loop.
- openUrl in On Success did not redirect when the form was opened from the menu; it worked when opened via + Add on the report.
- getReportMetadata lists report custom actions (use it to verify a button is attached).
- No Duplicate Values ignores blank entries (Zoho doc), so blank Source_Email_ID is fine.
- Books holds 3 copies of checking 0750 (account_ids ...1533008, ...2441353, ...2441582); only ...1533008 carries balances. Cleanup belongs to SOS Finance.

## 6. Open
| Task | Owner | Status | Blocking | Deadline |
|---|---|---|---|---|
| Remit backlog: upload Empath and AccentCare remits since August not yet in Books | Neil / cchat | OPEN | N | TBD |
| Delete the 4 InnoVage test intakes (test-2/3/4/blank) | Neil | OPEN | N | TBD |
| Books_Payment_IDs max 255 chars (about 11 payments per remit) | cchat | OPEN | N | TBD |
| Duplicate Books bank account copies for 0750 | SOS Finance | OPEN | N | TBD |
| Email intake (remits@) | Neil | PARKED | N | - |
| Credit $150 to Empath - Tidewell for PVS-1308-NH on November billing (INV-000118 now paid) | Neil | OPEN | N | Nov billing |
| Export v70 .ds and commit (all remit functions, workflow, action, schedules) | Neil / ccode | OPEN | N | next session |
