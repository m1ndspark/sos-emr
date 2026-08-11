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
| Chapters rates: 3 branches (HIL / HPH / LIF). No rate card exists anywhere to copy from, so it must be hand-entered. | Neil / Josh | OPEN | Y | 2026-08-03 (overdue) |
| VITAS rates: 4 branches (CIT / LEE / SUM / VIL). | Neil / Josh | OPEN | Y | 2026-08-03 (overdue) |
| Books customer IDs missing: Chapters (6), VITAS (4), Cornerstone (5). Without these the invoice batch fails at the Books call even when rates exist. | Neil / Josh | OPEN | Y | 2026-08-03 (overdue) |
| Turn OFF "hide zero value items" in Books. | Neil / Josh | OPEN | Y | 2026-08-03 (overdue) |
| Set branch on Empath/Polk referrals 1444, 1423, 1297, then re-run backfill_pvs_billing_branch and backfill_pvs_complexity_charge. | Neil / cchat | OPEN | Y | 2026-08-05 |
| REF-070326-1254: run set_pvs_provider to stamp Josh and repair the PVS_ID "PVS-1199-" (missing initials). | Neil / cchat | OPEN | Y | 2026-08-05 |
| Deliver the 250-visit charge file. UPDATE 2026-08-05: fulfilled by the July PVS import (200 records) plus the June partial; data is in. Keep OPEN only if additional visits remain to be delivered - otherwise close. backfill_pvs_complexity_charge resolves charges from the rate card and never overwrites an existing value. | Neil / Josh | OPEN | Y | 2026-08-03 |
| Books billing contacts for all 16 customers. Gates SENDING live invoices FROM THE BOOKS UI. UPDATE 2026-08-08: does NOT gate the planned approval dashboard - POST /invoices/{id}/email takes to_mail_ids as raw email addresses, so the dashboard can send to a recipient list built in Creator with no Books contact persons at all. See context/05. | Neil / Josh | OPEN | Y | 2026-08-05 |
| Five equipment amounts from Josh and Ann, needed to finalize equipment charges on the affected visits. | Josh / Ann | OPEN | Y | 2026-08-05 |
| InnoVage 3008 completion list. | Neil / Josh | OPEN | Y | 2026-08-05 |
| Capped re-batch of the three Empath branches. DONE 2026-08-11: all of Empath billed and sent (Tidewell visits confirmed on INV-000044/45, Sent). $27,574 gap closed. | Neil | DONE | N | 2026-08-08 |
| Reprice Empath premiums. CLOSED 2026-08-11, no action: diag_pvs_premium_mismatches found 9 mismatches (4 Super STAT $200 vs card $400, 5 After Hours $100 vs card $150, $1,050 total) but ALL are on Sent invoices and Neil confirmed the sent rates were INTENTIONAL. Zero mismatches on Draft visits, so reprice_draft_pvs_premiums is unnecessary and was never built. Rate card confirmed correct going forward: Empath After Hours $150, Super STAT $400 (fee schedule 2025-01-22). | Neil | CLOSED | N | 2026-08-08 |
| Zoho Forms to Creator integration rebuild, 43 partner-entered fields. The field map cannot be edited, so the integration must be deleted and every field re-selected. Gates the form remap. See context/24. | Neil | OPEN | Y | 2026-08-08 |
| Fresh .ds export. DONE: v20 committed 2026-08-08; v21 exported and committed 2026-08-11 (SOS_Referrals_App_2026-08-11_v21.ds, canonical SOS_Referrals_App.ds overwritten). Note: v21 predates the four Session 30 workflow edits and the new PVS Required Fields workflow - next export captures them. | Neil | DONE | N | 2026-08-11 |
| VITAS rebill at updated rates - IN PROGRESS at EOD 2026-08-11. Rates updated in Partner_Rates. Plan: reset_invoice the 2 VITAS invoices that carry Books numbers; the remaining batched invoice records have NO Books number so reset_invoice (keyed on Books_Invoice_Number) cannot touch them - a reset variant keyed on the record is needed and NOT YET WRITTEN; then reprice_draft_pvs per VITAS branch label with REPRICE; then fresh batches (no cap). | Neil / cchat | OPEN | Y | 2026-08-12 |
| Verify PVS Required Fields On Validate workflow end-to-end and UNSET the field-level Mandatory flag on all 16 listed fields (workflow pasted 2026-08-11; both validations fire until flags are off). Also verify the address subfield link names survived the editor (district_city / state_province / postal_Code). | Neil | OPEN | Y | 2026-08-12 |
--------------------------------------------------------------------------------
## OPEN, NOT BLOCKING
--------------------------------------------------------------------------------

| Task | Owner | Status | Blocking | Deadline |
|---|---|---|---|---|
| Delete run_reset_test AND all diag_* functions from Creator after launch (diag_pvs_ids, diag_referral_ids, diag_zztest_referrals, diag_accentcare_rates, diag_referral_import_gaps, diag_pvs_import_gaps, diag_empath_labels, diag_esi_references, diag_innovage_rates, and any added since). run_reset_test also clears the intentional repo DRIFT on functions/run_reset_test.dg. | Neil | OPEN | N | post-launch |
| Books line-item description is capped at 2000 characters and create_invoice_from_selection does not truncate. Per-visit blocks embed Reason_for_Referral, which is unbounded; will break on large batches. | cchat / ccode | OPEN | N | post-launch |
| create_invoice_from_selection has no guard if invokeurl returns a non-map on a transport failure. | cchat / ccode | OPEN | N | post-launch |
| run_invoice_batch does not filter Clinical_Note_Type, so a Preliminary note is invoiceable. | cchat / ccode | OPEN | N | post-launch |
| After_Hours_Fee and Super_Stat_Fee are manual entry. UPDATE 2026-07-31 (v15): create_invoice_from_selection now BILLS them (plus Equipment/Other) as their own Books line items when > 0, so the "read by nothing" half is resolved. Still manual entry, though - no workflow auto-fills them from Partner_Rates (which carries both rate types). | cchat / ccode | OPEN | N | post-launch |
| Referrals_Main Patient_Full_Name and Partner_POC_Name_Title generators are On Success; move to On Validate post-launch. | cchat / ccode | OPEN | N | post-launch |
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
| Partner_Contact_Upsert never updates Partner_Link or Partner_Locations_Link on a match, so a POC who changes branch keeps the old lookup and their next prefill pulls the wrong branch. | cchat | OPEN | N | 2026-08-08 |
| Empath Super STAT rate question. RESOLVED 2026-08-11: fee schedule (2025-01-22) confirms Super STAT $400, After Hours $150. Sent July invoices billed lower rates intentionally; no rebill. | Neil | CLOSED | N | 2026-08-08 |
| Approval dashboard (weekly billing review, per-record APPROVE, multi-visit invoice assembly, running total, warning above $2,999, reviewers Neil and Josh only). Specced, not built. Estimated 1.5-2 days with a staging-record total, 2.5-3 days with a client-side widget. | cchat / ccode | OPEN | N | fast-follow |
| Convert text-typed phone fields to Phone Number type for click-to-call in report popouts: Referrals_Main (Patient_Phone, AC_Phone, Facility_Phone, Partner_POC_Phone) and Imaging_Orders (Patient_Phone, Facility_Phone). PVS phone fields are already phonenumber. Risk: Phone Number fields validate format on CSV import, so convert only after any remaining referral/PVS CSV loads; test with a 2-row import first. | Neil / cchat | OPEN | N | post-launch |
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
