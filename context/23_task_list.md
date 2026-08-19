# SOS EMR Task List (launch tracker)

Created Session 27, 2026-07-30. Seeded from context/18_launch_plan.md (LOCKED
plan to 8/3), context/16_ds_inventory_punch_list.md, the SOS EMR Launch List
2026-07-28 (embedded in CCODE_CHECKIN_2026-07-29.md), and the locked launch
plan. Hard launch: Monday, 2026-08-03. Test 2: Fri 2026-07-31.

This file is the single running task tracker going forward. Status legend:
OPEN, IN PROGRESS, CLOSED. Blocking = gates the Monday 08-03 launch.

Owner legend:
- Neil  = operational lead; pastes Deluge into Creator, Books config, data loads
- Josh  = approvals dashboard + rate/data entry
- ccode = Claude Code (this repo; code, sync, docs)
- cchat = Claude.ai chat (writes/finalizes Deluge for Neil to paste)

--------------------------------------------------------------------------------
## CLOSED
--------------------------------------------------------------------------------

| Task | Owner | Status | Blocking | Deadline |
|---|---|---|---|---|
| Books POST smoke test, end to end. PASSED 2026-07-30. Books accepts ad-hoc line items with no item_id; invoice created, PVS flipped to Final, Invoice Connection resolved, reset path voided both Creator and Books cleanly. | Neil / ccode | CLOSED | was Y | 2026-07-30 |
| Invoice_Batch.Invoice_Link population gap (Session 24). run_invoice_batch now parses the "INVID:" prefix and writes the invoice record ID to Invoice_Batch.Invoice_Link. | ccode | CLOSED | was N | 2026-07-30 |
| Employee_Email not stamped on PVS (Session 24 item c). OnLoad Pre_fills_provider_sectio now sets input.Employee_Email from the Employees record. | ccode | CLOSED | was N | 2026-07-30 |
| Invoice reset path. reset_invoice built, run three times, verified in Creator and Books (INV-000002/003/004 voided, PVS returned to Draft). | Neil / ccode | CLOSED | was Y | 2026-07-30 |
| PVS section visibility on reopen. Default Hide On Load now re-shows sections by Type_of_Entry. | ccode | CLOSED | was N | 2026-07-30 |
| Visit Completion Date lock. Now editable until the visit is invoiced (disable moved to the Invoice_Status == "Final" block). | ccode | CLOSED | was N | 2026-07-30 |
| PVS Invoice Connection rendering blank. Display format was Invoice_ID (never populated), changed to Books_Invoice_Number. Field-property only. | Neil | CLOSED | was N | 2026-07-30 |
| Partner_Location_Label resync across Referrals_Main and Encounter_PatientVisit. resync_location_labels built and run (Referrals 7 updated / 54 skipped, PVS 2 / 16). | ccode | CLOSED | was N | 2026-07-30 |
| create_invoice_from_selection Books-failure return now carries the "INVID:<recordId>|ERROR: ..." prefix (corrected live after v13). run_invoice_batch recovers the invoice ID on a failed POST. (Was flagged Session 27.) | Neil / ccode | CLOSED | was N | 2026-07-30 |
| context/23_task_list.md creation (carried from Session 26). | ccode | CLOSED | was Y | 2026-07-30 |
| Re-export the .ds and commit at the start of Session 28. Done: v14, dated 2026-07-31, committed and set as source of truth. Closed both ahead-of-v13 divergences (create_invoice_from_selection INVID-on-failure prefix, resync_location_labels) with no repo edit. | ccode | CLOSED | was N | 2026-07-31 |
| Re-export the .ds and commit (Session 28 checkpoint item). Done: v15, dated 2026-07-31, captured the Build Patient Full Address workflow fix, the re-added Patient_Full_Address field, the four backfills and six diagnostics (placeholders replaced with verbatim bodies), plus rehearsal-session changes (PVS patient-name field rename, create_invoice fee line items, new backfill_referral_id_from_token). | ccode | CLOSED | was N | 2026-07-31 |
| Rehearse the go-live import sequence against a small throwaway sample. PASSED end to end 2026-07-31: import Referrals -> resolve_referral_branch_from_text -> backfill_referral_branch -> import PVS -> backfill_pvs_ids -> link_pvs_to_referral -> backfill_pvs_billing_branch -> backfill_pvs_complexity_charge -> Invoice Batch -> Books INV-000005 (2 visits, $888.00), then voided via reset_invoice. Log: context/logs/SOS_Import_Rehearsal_2026-07-31.md. | Neil / cchat | CLOSED | was Y | 2026-07-31 |
| Rewrite section 5 of 09_cognito_import_procedure.md per finding 5b (imports fire On Success workflows when "Execute form workflows" is checked; On User Input never fires). Done Session 28; also added section 5A findings and hard-verify-mapping checklist steps. | ccode | CLOSED | was N | 2026-07-31 |
| Empath rates loaded (45 rows, 5 active branches; ESI excluded). | Neil / Josh | CLOSED | was Y | 2026-08-05 |
| AccentCare rates loaded (54 rows, 6 branches). | Neil / Josh | CLOSED | was Y | 2026-08-05 |
| InnoVage rates loaded (2 rows, Cares 3008 Assessment only; SOS is contracted with InnoVage for 3008 evaluations only, so the other rate types are intentionally absent). | Neil / Josh | CLOSED | was Y | 2026-08-05 |
| Empath - ESI deactivated. It is a main contact number, not a branch SOS works with. Zero referral / PVS / invoice / rate references; one billing contact reassigned. Its Books customer remains in Books, unused. | Neil / Josh | CLOSED | was Y | 2026-08-05 |
| July referral import (278 records). | Neil / cchat | CLOSED | was Y | 2026-08-05 |
| June partial referral import (6 records: 1209, 1213, 1215, 1216, 1217, 1220). | Neil / cchat | CLOSED | was Y | 2026-08-05 |
| July PVS import (200 records). | Neil / cchat | CLOSED | was Y | 2026-08-05 |
| PVS post-import backfill sequence: link, billing branch, referral backfill, full address, complexity charge (backfill_pvs_from_referral, link_pvs_to_referral, backfill_pvs_billing_branch, backfill_pvs_patient_full_address, backfill_pvs_complexity_charge). | Neil / cchat | CLOSED | was Y | 2026-08-05 |
| Partner Contact Upsert case-sensitivity defect (Deluge email match is case-sensitive; upsert now does a lowercase fallback scan before insert). See context/28_import_findings.md. | cchat | CLOSED | was Y | 2026-08-05 |
| Telemedicine rates loaded: Empath, AccentCare, VITAS. | Neil / Josh | CLOSED | was Y | 2026-08-05 |
| VITAS Moderate Complexity rates loaded: Sumter, Villages. | Neil / Josh | CLOSED | was Y | 2026-08-05 |
| July invoicing run: all 16 branches invoiced into Books, one invoice per branch (July PVS import plus June partial). See context/30_july_billing_run.md. | Neil / cchat | CLOSED | was Y | 2026-08-05 |
| Premium fee backfill: After_Hours_Fee / Super_Stat_Fee populated on imported visits via new backfill_pvs_premium_fees (import left them blank; no workflow auto-fills them from Partner_Rates). | Neil / cchat | CLOSED | was Y | 2026-08-05 |
| Phone normalization: Partner_POC_Phone normalized to E.164 via new normalize_pvs_phones. Raw local-format values (e.g. "(352) 237-6979") made all 200 imported PVS records unsaveable from the form. See context/05. | Neil / cchat | CLOSED | was Y | 2026-08-05 |
| Partner Rate Status repair: repair_partner_rate_status recovered ~170 Current_Rate flags wiped when backfill_current_rate ran against blank-status rows. See context/05. | Neil / cchat | CLOSED | was Y | 2026-08-05 |
| VITAS rate correction: Sumter Moderate Complexity 343 -> 323 (343 was AccentCare's Moderate rate, a cross-partner value). Draft un-invoiced visits repriced via reprice_draft_pvs. See context/30. | Neil / cchat | CLOSED | was Y | 2026-08-05 |
| Marion and Sumter equipment corrections: stale Equipment_Charge_Amount cleared/corrected; new set_pvs_equipment_charge. See context/30. | Neil / Josh / cchat | CLOSED | was Y | 2026-08-05 |

--------------------------------------------------------------------------------
## OPEN, BLOCKING (launch 2026-08-03; now overdue as of 2026-08-05)
--------------------------------------------------------------------------------

| Task | Owner | Status | Blocking | Deadline |
|---|---|---|---|---|
| Chapters rates: 3 branches (HIL / HPH / LIF). DONE 2026-08-11: rates hand-entered and the 3 July Chapters visits billed. | Neil | DONE | N | 2026-08-11 |
| VITAS rates: 4 branches (CIT / LEE / SUM / VIL). | Neil / Josh | OPEN | Y | 2026-08-03 (overdue) |
| Books customer IDs missing: Cornerstone (5) only. Chapters and VITAS proven working 2026-08-11 - both billed through the batch successfully. | Neil / Josh | OPEN | N | 2026-08-03 (overdue) |
| Turn OFF "hide zero value items" in Books. DONE 2026-08-11. | Neil | DONE | N | 2026-08-11 |
| Empath/Polk referrals 1444, 1423, 1297. DONE 2026-08-11: backfilled and invoiced. | Neil | DONE | N | 2026-08-11 |
| REF-070326-1254 provider stamp. DONE 2026-08-11: Josh's initials confirmed present. | Neil | DONE | N | 2026-08-11 |
| 250-visit charge file. CLOSED 2026-08-11: no such file exists; all July PVSs are imported and billed except InnoVage. | Neil | CLOSED | N | 2026-08-11 |
| Books billing contacts. DONE 2026-08-11: all billing contact emails manually entered in Books. (Approval-dashboard send path never needed them - to_mail_ids takes raw addresses.) | Neil | DONE | N | 2026-08-11 |
| Five equipment amounts. DONE 2026-08-11: all 5 equipment charges finalized. The four understated branch totals (Hillsborough, Pinellas, Trustbridge, Tidewell) are now final. | Josh / Ann | DONE | N | 2026-08-11 |
| InnoVage 3008 completion list. | Neil / Josh | OPEN | Y | 2026-08-05 |
| Capped re-batch of the three Empath branches. DONE 2026-08-11: all of Empath billed and sent (Tidewell visits confirmed on INV-000044/45, Sent). $27,574 gap closed. | Neil | DONE | N | 2026-08-08 |
| Reprice Empath premiums. CLOSED 2026-08-11, no action: diag_pvs_premium_mismatches found 9 mismatches (4 Super STAT $200 vs card $400, 5 After Hours $100 vs card $150, $1,050 total) but ALL are on Sent invoices and Neil confirmed the sent rates were INTENTIONAL. Zero mismatches on Draft visits, so reprice_draft_pvs_premiums is unnecessary and was never built. Rate card confirmed correct going forward: Empath After Hours $150, Super STAT $400 (fee schedule 2025-01-22). | Neil | CLOSED | N | 2026-08-08 |
| Zoho Forms to Creator integration rebuild, 43 fields. DONE 2026-08-11: rebuilt and confirmed working end to end (dummy referral -> Referrals_Main -> Partner_Contact_Upsert). | Neil | DONE | N | 2026-08-11 |
| Fresh .ds export. DONE: v20 committed 2026-08-08; v21 exported and committed 2026-08-11 (SOS_Referrals_App_2026-08-11_v21.ds, canonical SOS_Referrals_App.ds overwritten). Note: v21 predates the four Session 30 workflow edits and the new PVS Required Fields workflow - next export captures them. | Neil | DONE | N | 2026-08-11 |
| VITAS rebill at updated rates. DONE 2026-08-11 (post-EOD): Neil reset and re-billed all VITAS invoices. reprice_draft_pvs was NOT run; Neil verified the new invoices priced correctly regardless (no premium charges on VITAS visits, normal visit pricing correct). The reset variant for no-Books-number invoice records was never needed and was not written. | Neil | DONE | N | 2026-08-11 |
| PVS Required Fields: 16 field-level Mandatory flags UNSET (done 2026-08-11). Remaining: verify the On Validate workflow end-to-end - submit with blanks in each condition branch (Facility, Patient Visit, non-3008, billing-only Complexity Charge) and confirm the alert lists the right fields; verify the address subfield link names (district_city / state_province / postal_Code). | Neil | OPEN | Y | 2026-08-12 |
| Invoice_Batch void-and-rebill: create Batch_Reason (dropdown New Billing / Rebill After Void / Correction / Other, default New Billing) and Replaces_Invoice_Number (single line) on Invoice_Batch, then wire run_invoice_batch to read them and fire the void-and-rebill notice. Confirmed absent in v23. | Neil / cchat | OPEN | Y | 2026-08-13 |
| Run create_3008_pvs_july in DRYRUN, review the output, then run it in COMMIT. Creates the 76 July 3008 PVS records so they can be invoiced. Not yet run at all. See docs/billing/SOS_3008_July_2026_Billing.md. | Neil | OPEN | Y | 2026-08-19 |
--------------------------------------------------------------------------------
## OPEN, NOT BLOCKING
--------------------------------------------------------------------------------

| Task | Owner | Status | Blocking | Deadline |
|---|---|---|---|---|
| Delete run_reset_test AND all diag_* functions from Creator after launch (diag_pvs_ids, diag_referral_ids, diag_zztest_referrals, diag_accentcare_rates, diag_referral_import_gaps, diag_pvs_import_gaps, diag_empath_labels, diag_esi_references, diag_innovage_rates, diag_pvs_premium_mismatches, diag_premium_visit_invoices, diag_duplicate_location_names, diag_duplicate_visits, diag_patient_visits, and any added since). run_reset_test also clears the intentional repo DRIFT on functions/run_reset_test.dg. | Neil | OPEN | N | post-launch |
| Books line-item description is capped at 2000 characters and create_invoice_from_selection does not truncate. Per-visit blocks embed Reason_for_Referral, which is unbounded. NOTE 2026-08-11: Max Invoice Total (~5-8 visits at 2999) mitigates for capped partners (Empath), but uncapped batches (VITAS, AccentCare - Hillsborough ran 21 visits) and long partner-written reasons still expose it; July reasons were short. Fix when it bites: cap REASON length and/or split a tier line into a second line item past 2000. | cchat / ccode | OPEN | N | post-launch |
| create_invoice_from_selection has no guard if invokeurl returns a non-map on a transport failure. | cchat / ccode | OPEN | N | post-launch |
| run_invoice_batch does not filter Clinical_Note_Type, so a Preliminary note is invoiceable. | cchat / ccode | OPEN | N | post-launch |
| After_Hours_Fee and Super_Stat_Fee are manual entry. UPDATE 2026-07-31 (v15): create_invoice_from_selection now BILLS them (plus Equipment/Other) as their own Books line items when > 0, so the "read by nothing" half is resolved. Still manual entry, though - no workflow auto-fills them from Partner_Rates (which carries both rate types). | cchat / ccode | OPEN | N | post-launch |
| Referrals_Main Patient_Full_Name and Partner_POC_Name_Title generators are On Success; move to On Validate post-launch. UPDATE 2026-08-12: both switched to record event Edited only (the master workflow builds these on Create), so they now fire once per event. On Validate move still open. | cchat / ccode | OPEN | N | post-launch |
| Audit the rest of the form for the hidden-on-load / shown-on-user-input pattern. Sections, Facility fields, Type_of_Diversion and the Equipment/Other charge fields are fixed; others may remain. | cchat / ccode | OPEN | N | post-launch |
| Rename Chapters - HIL off "Main Hospice" so no two location names collide. Location labels must be unique across all partners (Partner_Location_Label is now Partner_Location_Name; Empath - ESI also named "Main Hospice" but is Inactive). | Neil | OPEN | N | post-launch |
| Delete two duplicate Empath rate rows (Tidewell / High Complexity and Trustbridge / High Complexity, both 545) if they were imported. | Neil / Josh | OPEN | N | post-launch |
| Delete backfill_referral_id_from_token from Creator. The Form_Token workaround proved unnecessary and that field carries real public-form tokens. | Neil | OPEN | N | post-launch |
| REF-071126-1305: possible cancelled referral, excluded from import. Revisit and confirm whether it should be imported or stays out. | Neil | OPEN | N | post-launch |
| Referrals_Main lookup/text pairs (e.g. Partner_Link vs Partner_Branch text): show the text field for admin only, hide the redundant pair from the standard view. | cchat / ccode | OPEN | N | post-launch |
| Invoice_ID and Invoice_ID_Stamp are never generated on the Invoices. | cchat / ccode | OPEN | N | post-launch |
| Books_Sync_Status still carries placeholder Choice 1 / Choice 2 / Choice 3 values. | Neil | OPEN | N | post-launch |
| Invoice subtotal fields on the Invoices are not populated. The Invoices report shows only visit count and invoice total - no acuity breakdown, no additional-charges breakdown. Estimated 45 min lean / 1.5 hrs full. | cchat / ccode | OPEN | N | post-launch |
| Imaging Order field rule on the Zoho Form: Service Requested is Imaging Order (only) -> hide "Does the patient have allergies?" and "Is the patient self-responsible?". See context/24. | Neil | OPEN | N | 2026-08-08 |
| Patient Medical Info page rule on the Zoho Form: Imaging Order (only) -> skip to Imaging Order Details; Finally -> General Information. See context/24. | Neil | OPEN | N | 2026-08-08 |
| Decide whether Imaging Order (only) also skips the Additional Contact Details page. Undecided. | Neil | OPEN | N | 2026-08-08 |
| Lookup messages on the live Zoho Form. RESOLVED 2026-08-11: the message field was set Hidden, and a hidden field never renders even though the prefill write succeeds. Fix: field visible inside the "Email Typo Alert" grid, grid hidden by default and shown by rule Lookup Status Is not empty; searched email now embedded in both messages so a stale message is self-identifying. Known quirk accepted: clearing the email box does not re-trigger the rule or release the field value until Search is clicked again. | cchat | CLOSED | N | 2026-08-11 |
| Partner_Contact_Upsert lookup fields. DONE 2026-08-12: the upsert was absorbed into "Referrals Main On Create - Master" and now sets Partner_Link and Partner_Locations_Link from the resolved location on both the match and insert paths. Standalone Partner Contact Upsert workflow deleted. | cchat | DONE | N | 2026-08-12 |
| Empath Super STAT rate question. RESOLVED 2026-08-11: fee schedule (2025-01-22) confirms Super STAT $400, After Hours $150. Sent July invoices billed lower rates intentionally; no rebill. | Neil | CLOSED | N | 2026-08-08 |
| Approval dashboard (weekly billing review, per-record APPROVE, multi-visit invoice assembly, running total, warning above $2,999, reviewers Neil and Josh only). Specced, not built. Estimated 1.5-2 days with a staging-record total, 2.5-3 days with a client-side widget. SUPERSEDED 2026-08-13 by the "New batch screen" entry below; build that instead. Kept for the design detail (reviewer list, per-record approve, estimates). | cchat / ccode | OPEN | N | fast-follow |
| Fresh .ds export capturing all Session 31 work. DONE 2026-08-13: v23 exported and committed 6f049d2 (SOS_Referrals_App_2026-08-13_v23.ds, canonical SOS_Referrals_App.ds overwritten). Captured "Referrals Main On Create - Master" (label resolver + Partner_ID_Stamp), the rewritten get_partner_referral_contact (lookup-based branch/org, digits-only phone), the new PVS Required Fields On Validate, the four PVS billing-allowlist workflow edits, run_invoice_batch duplicate guard, five new diag_* functions, the deleted REF ID Generator / Partner Contact Upsert, and the two generators switched to Edited. Repo reconciled via ds_sync. | Neil | DONE | Y | 2026-08-13 |
| Referral notification emails from Creator: SendGrid dynamic template is built (HTML tables, {{#equals}} location variants, {{#if AC_First_Name}} block). UPDATE 2026-08-17 (Session 33): the Patient Visit and Imaging Order HTML templates are DONE (see the two DONE rows below); send_via_sendgrid already exists and works (posts to api.sendgrid.com/v3/mail/send over connection sendgrid_connection, from notifications@sosreferrals.com), so the new function only has to post a template_id plus a data map instead of raw HTML. Still to do: append that send step to the end of the master workflow. BLOCKED on the three Neil items below (template ID, Goal for Care ruling, BAA). Zoho Forms' own notification emails cannot carry the Referral ID (it does not exist at submit time) and must be turned off. Recipients are Josh, Neil and field staff. | cchat / Neil | OPEN | N | 2026-08-13 |
| Zoho Form page rule for Patient Visit: on General Information, If Service Requested Is Patient Visit -> skip to Partner Lookup Details (keeps the existing 3008 rule; Finally handles Imaging Order). Specced, not confirmed built. | Neil | OPEN | N | 2026-08-13 |
| Actions/transaction log report: default Creator audit captures failures only, not all transactions. Extend the existing Change_Log form + log_change function into a full actions log with a report, likely fed from the master workflows. Design TBD. | Neil / cchat | OPEN | N | TBD |
| Unresolved-partner safety net for the label resolver: (1) email alert to Neil from the master workflow when the location match fails, (2) "Referrals - Unresolved Partner" report filtered to blank Partner_Link, (3) On Validate uniqueness guard on Partner_Locations blocking a duplicate Active location name. None built yet. | cchat / Neil | OPEN | N | TBD |
| Convert text-typed phone fields to Phone Number type for click-to-call in report popouts: Referrals_Main (Patient_Phone, AC_Phone, Facility_Phone, Partner_POC_Phone) and Imaging_Orders (Patient_Phone, Facility_Phone). PVS phone fields are already phonenumber. Risk: Phone Number fields validate format on CSV import, so convert only after any remaining referral/PVS CSV loads; test with a 2-row import first. | Neil / cchat | OPEN | N | post-launch |
| New batch screen: a modified PVS report, one visit per line, manual record selection, running total with conditional formatting turning red above $2,999.99, selected records removed or disabled on submit. Creator page plus widget, not a stock report. Supersedes the "Approval dashboard" entry above (cross-referenced). | cchat / ccode | OPEN | N | fast-follow |
| Extend reset_invoice to persist the pre-void invoice total, visit count, and released PVS list onto the Invoices record. | cchat | OPEN | N | post-launch |
| Rename "Partner POC Phone" on the Zoho Form for consistency with its Referral POC siblings. | Neil | OPEN | N | post-launch |
| Delete test referrals REF-1047 through REF-1055 and the neilheird@gmail.com row in Partner_Referral_Contacts. (Replaces the REF-1047 to 1052 range noted at checkpoint.) | Neil | OPEN | N | post-launch |
| RingCentral email notifications configured for new voicemail, fax sent, and fax received. CLOSED 2026-08-13. | Neil | CLOSED | N | 2026-08-13 |
| Fix InnoVage and Chapters DOB records storing a 20xx century: 22 InnoVage rows plus two Chapters records (initials G.S. DOB 2044-10-09, W.W. DOB 2045-07-06). Reports already correct this at read time (subtract 100 years from any DOB with year >= 2000); the stored Creator records are still wrong. Neil holds the identity key. UPDATE 2026-08-19 (Session 34): COST REAL TIME AGAIN. This bug accounted for 18 of the 22 July 3008 completions that falsely appeared to have no referral (patient R.S. is stored 2043-04-16). Second time it has burned a session. Fix the stored records AND the importer. See docs/billing/SOS_3008_July_2026_Billing.md. | Neil | OPEN | N | - |
| Confirm whether "Patient N-1" (Creator) and "Patient N-2" (3008 log) - same surname initial N, same DOB, different first name - are the same patient. Neil holds the identity key (kept out of the repo). UPDATE 2026-08-19 (Session 34): resurfaced as 1 of the 22 July 3008 match failures. Genuine data conflict, not a matcher bug. See docs/billing/SOS_3008_July_2026_Billing.md. | Neil | OPEN | N | - |
| Resolve a DOB conflict for one InnoVage patient (initials C.D.L.R., recorded earlier as C.D. before the particle bug was understood): the 3008 log shows 1958-06-06, Creator shows 1956-10-30. One of the two is wrong. Neil holds the identity key (kept out of the repo). UPDATE 2026-08-19 (Session 34): resurfaced as 1 of the 22 July 3008 match failures. This one is a genuine data conflict, not a matcher bug. See docs/billing/SOS_3008_July_2026_Billing.md. | Neil | OPEN | N | - |
| Review name-particle handling on import: at least two InnoVage patients with a "De " surname particle imported without the "De". Fix the importer so particles are preserved. UPDATE 2026-08-19 (Session 34): COST REAL TIME AGAIN. Accounted for 3 of the 22 July 3008 completions that falsely appeared to have no referral. The exact failure is now known: "De Jesus" imports as MI "D" and last name "Jesus", same for "De La Rosa". Second time it has burned a session. See docs/billing/SOS_3008_July_2026_Billing.md. | cchat | OPEN | N | - |
| Populate the new 3008 section in the PVS, including 3008 Notes, which will carry follow-up and delay reasons for the InnoVage MPU report beginning with the August cycle. | Neil | OPEN | N | - |
| MPU reporting: v2 report template rolled out to all five partner reports (Empath, AccentCare, InnoVage, Chapters, VITAS). Chapters was the last report never built. DONE 2026-08-15. | cchat / Neil | DONE | N | 2026-08-15 |
| MPU hospital savings model rebuilt on verified CY2026 CMS source files; July reissued for all partners. The April-July model double-counted services packaged under J1 Comprehensive APCs (paracentesis / thoracentesis); verified against CY2026 Addendum D1 and Addendum J. DONE 2026-08-15. SUPERSEDED 2026-08-17 by the two-pathway blended rebuild below - the packaging correction stands, but the single-pathway pricing and the Session 32 July figures do not. | cchat / Neil | DONE | N | 2026-08-15 |
| Paste backfill_referral_added_time into Creator and run it. Carried from Session 31, still not done at Session 33 (2026-08-17). | Neil | OPEN | N | - |
| PVS-1112-JK carries a clinical note byte-identical to PVS-1108-JK for a different patient (template copy-paste). Medical-record integrity issue. | Neil | OPEN | N | - |
| Decide whether to notify partners that July MPU reports were reissued under corrected (CY2026) methodology, and in what words. | Neil | OPEN | N | - |
| Imaging / X-Ray benchmark: blocked pending the outsourced vendor's rate. SOS does not perform the study - it is outsourced and the vendor bills the hospice directly, so any benchmark must account for the vendor charge, which Neil does not have to hand. Still blocked at Session 33. | Neil | OPEN | N | - |
| MPU savings model, SECOND rebuild: two-pathway blend. Every procedure now priced twice - Pathway A treated and discharged on the comprehensive APC, Pathway B admitted on the MS-DRG for the whole stay - blended on the Florida place-of-service mix from the 2025 PSPS file (carrier 09102). MS-DRGs 393 (paracentesis, G-tube), 186 (thoracentesis), 695 (catheter), always the with-MCC tier. Blended benchmarks: Paracentesis 5,775.80 / Thoracentesis 10,220.14 / Catheter 3,897.49 / G-Tube 2,549.19. Documented in docs/mpu/SOS_MPU_Savings_Model_CY2026.md. DONE 2026-08-17. | cchat / Neil | DONE | N | 2026-08-17 |
| July partner reports reissued at the blended figures. RESTATED July 2026 savings: Empath 237,682.63; AccentCare 77,884.92; Chapters 5,230.80; VITAS 3,574.49. These supersede BOTH the original April-July figures AND the Session 32 corrections; only these are valid for month-over-month. DONE 2026-08-17. | cchat / Neil | DONE | N | 2026-08-17 |
| CPT correction 32557 -> 32555 for thoracentesis. 32557 is pleural DRAINAGE by indwelling catheter (a chest tube), 98.6% inpatient - not a thoracentesis. The aspiration code is 32555. 32557 was wrong in every report from April through July 2026. DONE 2026-08-17. | cchat | DONE | N | 2026-08-17 |
| Chapters MPU report, first build. DONE 2026-08-15, reissued 2026-08-17 on the blended model (12 pages). | cchat / Neil | DONE | N | 2026-08-17 |
| Referral notification email, Patient Visit template (referral_notification_email.html). Email-safe: nested tables, all styles inline, Arial, 600px max width, mobile media query. Sections: Referral Info, Patient Info, Medical Info, Partner Info. DONE 2026-08-17. | cchat | DONE | N | 2026-08-17 |
| Referral notification email, Imaging Order template (referral_imaging_order_email.html). Same structure, with Imaging Order Details (Imaging Type, Indication, Order Document) replacing Medical Info. Order document is ATTACHED, not linked - a Creator file URL requires a login. DONE 2026-08-17. | cchat | DONE | N | 2026-08-17 |
| MPU annual data refresh checklist: eight data sources, cadence and traps, at docs/mpu/SOS_MPU_Annual_Data_Refresh_Checklist.md. DONE 2026-08-17. | cchat | DONE | N | 2026-08-17 |
| SendGrid Dynamic Template ID (d-...) needed before the Creator send function can be written. | Neil | OPEN | N (blocks the SendGrid send function) | 2026-08-17 |
| Goal for Care ruling: drop the row, or add the field to Referrals_Main. There is NO Goal for Care field on Referrals_Main - Goals_of_Care exists only on Encounter_PatientVisit, so the Medical Info row Neil specified has no source on a referral. Confirmed against SOS_Referrals_App v24. | Neil | OPEN | N (blocks the SendGrid send function) | 2026-08-17 |
| Confirm a signed BAA covers PHI through SendGrid. These emails carry patient name, DOB, address and diagnosis. | Neil | OPEN | N (blocks the SendGrid send function) | 2026-08-17 |
| 3008 referral notification template. Not started - needs the field list from Neil. Referral_Type has FOUR values, not three: Patient Visit, 3008, X-Ray Order (only), Lab Draw (only). | cchat / Neil | OPEN | N | - |
| Lab Draw (only) referral notification template. Not started; needs a template decision. | cchat | OPEN | N | - |
| Nine service lines still have no hospital benchmark: Imaging / X-Ray, Consultation/Evaluation, Wound/Fracture Care, Pleural Catheter/Chest Tube, Tracheostomy Management, IV Access/Infusion, Lab Draw, Foot Care, Ultrasound/Evaluation. 64 of Empath's 118 July visits sit outside the savings model for want of benchmarks. | cchat | OPEN | N | - |
| Clinical Team is free text on the Zoho Form; a partner typed a phone number into it on REF-081626-1638. Convert to a picklist to fix it at the source. | Neil | OPEN | N | - |
| Data quality, carried from Session 32 and still open at Session 33: 20xx-century DOBs, the byte-identical clinical note on PVS-1112-JK, name-particle imports ("De " surnames), and duplicate patients. Tracked individually in the rows above; this row is the Session 33 carry. | cchat / Neil | OPEN | N | - |
| Facility and additional-contact email blocks are built in both templates but commented out pending wiring. | cchat | OPEN | N | - |
| Session 33 documentation closeout: Session 33 log delivered and committed, SOS_MPU_Savings_Model_CY2026.md in MPU Reporting overwritten with the blended two-pathway model (the stale Session 32 single-pathway copy), repo marked canonical in both headers, all em dashes removed. DONE 2026-08-19. | cchat | DONE | N | 2026-08-19 |
| Savings model working copy corrected in MPU Reporting: DRG weights, GMLOS, and the full discharged/admitted component breakdown added. Merged back into the canonical repo copy by ccode 2026-08-19. DONE 2026-08-19. | cchat | DONE | N | 2026-08-19 |
| PVS fax system use case and logic map approved: 11 steps, PVS save through the 4am digest. Every ruling recorded in docs/fax/SOS_PVS_Fax_System_Design.md. DONE 2026-08-19. | cchat | DONE | N | 2026-08-19 |
| Fax HTML template and cover sheet built: one document, cover page + note page + one page per image attachment. Letter, Helvetica, SOS navy 0B0B5B, logo inlined as base64, running footer carrying patient, DOB, PVS ID, fax ID and page x of y. Our cover, not RingCentral's (coverIndex 0). DONE 2026-08-19. | cchat | DONE | N | 2026-08-19 |
| build_pvs_fax_html, get_rc_token, send_pvs_fax and poll_fax_status written and pasted into Creator. poll_fax_status does not save yet - it needs the Fax_Log form. Bodies are PENDING extraction in docs/fax/deluge/ (written in an ephemeral container, no copy reached the repo machine). DONE 2026-08-19. | cchat | DONE | N | 2026-08-19 |
| API_Config form created (6 fields, one record, locked to Neil and Josh) and the FAX prefix record added to Sequence_Tracker. Both confirmed in the 2026-08-19 schema capture. DONE 2026-08-19. | Neil | DONE | N | 2026-08-19 |
| July 3008 referral gap investigated and closed: the apparent 22 missing referrals were a MATCHING failure, not an import failure. All 83 Cognito 3008 referrals imported successfully. Breakdown: 18 century-DOB, 3 name-particle, 1 first-name mismatch, 1 DOB conflict. See docs/billing/SOS_3008_July_2026_Billing.md. DONE 2026-08-19. | cchat | DONE | N | 2026-08-19 |
| create_3008_pvs_july(pMode) written: creates the 76 July 3008 PVS records, referral IDs resolved in Python and hardcoded so Deluge does zero name matching, stamps the PVS ID from Sequence_Tracker, sets Invoice Status Draft / Hold From Invoicing No, takes DRYRUN or COMMIT. Body PENDING extraction at docs/billing/create_3008_pvs_july.dg. DONE 2026-08-19. | cchat | DONE | N | 2026-08-19 |
| RingCentral Client ID, Client Secret and JWT assertion. Create a REST API App with JWT auth, scopes Fax + Read Messages + Read Call Log, bound to the extension that owns (813) 626-3312, graduated to production. The API_Config form exists and is empty. | Neil | OPEN | N (blocks the fax send function) | 2026-08-19 |
| Create the Fax_Log form (~25 fields, hidden, Deluge inserts only), then re-save poll_fax_status. The 2026-08-19 schema capture shows the form exists with only 2 fields (Fax_ID, PVS_Link). This is what blocked poll_fax_status from saving. | Neil | OPEN | N (blocks poll and send) | 2026-08-19 |
| Add Partner_PVS_Fax to Partner_Billing_Contacts. New field, not the unused Partner_Billing_POC_Fax. It is the clinical-note fax destination for the branch. | Neil | OPEN | N | 2026-08-19 |
| Add Visit_Status and Fax_Status to Encounter_PatientVisit. NOTE 2026-08-19 (ccode): the 06:01 schema capture shows both fields already present, but Fax_Status carries only Not Sent / Queued / Sent - the Failed choice is MISSING and must be added or the failure state cannot be written. Verify live. | Neil | OPEN | N | 2026-08-19 |
| Build retry_failed_faxes. Retry 3 times, only on codes RingCentral has already given up on, never on busy (their carrier already retries a busy line for about 48 hours). | cchat | OPEN | N | 2026-08-19 |
| Build the 4am fax digest function. Fixed 4:00 am Eastern, no daylight shift, to joshua.kolanko@sosmmc.com and neil.heird@sosmmc.com. Covers unfaxed Final notes past 24 hours from Added Time, Preliminary notes past 24 hours, permanent failures, anything stuck in Queued, and every number override. | cchat | OPEN | N | 2026-08-19 |
| Build the PVS_Fax_Review page. Renders the note exactly as it will print, with Edit and Fax Now, the destination number and its override control, the attachment picker, and the Remarks textarea. | cchat | OPEN | N | 2026-08-19 |
| Build the Faxes Sent and Fax Exceptions reports. | cchat | OPEN | N | 2026-08-19 |
| Recover or regenerate 3008_july_map.csv (76 rows: referral ID, completion date, provider last name). Built in the ephemeral session container, never reached the repo. The hardcoded ID list inside create_3008_pvs_july in Creator is currently the only copy of the mapping. Decide whether it belongs in a PHI-clean repo before committing it. | Neil / cchat | OPEN | N | 2026-08-19 |
| Decide referrals@sosmmc.com fan-out via a Google Workspace group with Neil and Josh as members, Who Can Post set to External so partner mail does not bounce; then delete the Cloudflare worker. Cloudflare Email Routing is a dead end - it requires Cloudflare to own the MX records and sosmmc.com points at Google Workspace. Neil paused this. | Neil | OPEN | N | 2026-08-19 |

--------------------------------------------------------------------------------
## PRE-EXISTING CLEANUPS (from context/16, still open)
--------------------------------------------------------------------------------

| Task | Owner | Status | Blocking | Deadline |
|---|---|---|---|---|
| Remove the stray "Partner Rate Stamp Generator" bound to the Partners form (correct one is on Partner_Rates). Clears the ds_sync AMBIGUOUS collision on Partner_Rates/OnSuccess__Partner_Rate_Stamp_Generator.dg. | Neil | OPEN | N | post-launch |
| Delete the DISABLED legacy "Patient Fields Editability Toggle" (PVS, on user input of Has_Referral_ID). Optional tidiness; toggle is off so no live double-handling. | Neil | OPEN | N | post-launch |

--------------------------------------------------------------------------------
## DEFERRED / FAST-FOLLOW (post-launch, from context/18 LOCKED plan)
--------------------------------------------------------------------------------

| Task | Owner | Status | Blocking | Deadline |
|---|---|---|---|---|
| Automatic territory resolver: pre-fill hidden Billing_Branch from patient address (address-to-county map + county-to-branch per partner), overridable at approval. | Neil / Josh / cchat | OPEN | N | fast-follow |
| Rate-card auto-pricing on the PVS (lookup Active Partner_Rates by partner/branch/type as of date of service, fill dollar fields instead of manual entry). | cchat / ccode | OPEN | N | fast-follow |
| Primary record-lookup view (referral header + all associated PVS entries) for oversight. | cchat / ccode | OPEN | N | fast-follow |
| Reporting data cards across referrals, PVS, invoicing. | cchat / ccode | OPEN | N | fast-follow |
| Supplemental-addendum billing; in-app subscription record view. | cchat / ccode | OPEN | N | fast-follow |
| Deferred past 8/3: Books-to-QuickBooks sync, WorkDrive, new referral form as August intake, Imaging_Orders + lab build, AWS voice pipeline. | Neil / cchat | OPEN | N | deferred |

--------------------------------------------------------------------------------
END
--------------------------------------------------------------------------------
