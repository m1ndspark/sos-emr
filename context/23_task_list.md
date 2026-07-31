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
## CLOSED (Session 27, 2026-07-30)
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

--------------------------------------------------------------------------------
## OPEN, BLOCKING MONDAY 2026-08-03
--------------------------------------------------------------------------------

| Task | Owner | Status | Blocking | Deadline |
|---|---|---|---|---|
| Load rates for Chapters HIL / HPH / LIF, VITAS CIT / LEE / SUM / VIL, InnoVage ORL. | Neil / Josh | OPEN | Y | 2026-08-03 |
| Enter Books customer IDs for VITAS x4 and Chapters HPH / LIF. | Neil / Josh | OPEN | Y | 2026-08-03 |
| Turn OFF "hide zero value items" in Books. | Neil / Josh | OPEN | Y | 2026-08-03 |
| Empath: verify whether Empath - ESI carries a Hospital at Home rate flagged Current_Rate = Yes. ESI (not MAR) is the computed source branch; add_missing_rate_to_uniform_branches returned 0 inserts, meaning no Empath branch can receive a rate type ESI does not already have. Fixing MAR alone does nothing. | Neil / Josh | OPEN | Y | 2026-08-03 |
| Chapters: hand-enter a source rate card. replicate_uniform_rates has nothing to copy from and reports "SKIPPED - no source branch". | Neil / Josh | OPEN | Y | 2026-08-03 |
| Deliver the 250-visit charge file (Cognito export + charge columns + billing branch), one row per visit. OVERDUE since 2026-07-28. | Neil / Josh | OPEN | Y | 2026-07-28 (OVERDUE) |

--------------------------------------------------------------------------------
## OPEN, NOT BLOCKING
--------------------------------------------------------------------------------

| Task | Owner | Status | Blocking | Deadline |
|---|---|---|---|---|
| Delete run_reset_test from Creator after launch testing ends (throwaway wrapper for reset_invoice; also clears the intentional repo DRIFT on functions/run_reset_test.dg). | Neil | OPEN | N | post-launch |
| Books line-item description is capped at 2000 characters and create_invoice_from_selection does not truncate. Per-visit blocks embed Reason_for_Referral, which is unbounded; will break on large batches. | cchat / ccode | OPEN | N | post-launch |
| create_invoice_from_selection has no guard if invokeurl returns a non-map on a transport failure. | cchat / ccode | OPEN | N | post-launch |
| run_invoice_batch does not filter Clinical_Note_Type, so a Preliminary note is invoiceable. | cchat / ccode | OPEN | N | post-launch |
| After_Hours_Fee and Super_Stat_Fee are manual entry; Partner_Rates carries both rate types but no workflow reads them. | cchat / ccode | OPEN | N | post-launch |
| Referrals_Main Patient_Full_Name and Partner_POC_Name_Title generators are On Success; move to On Validate post-launch. | cchat / ccode | OPEN | N | post-launch |
| Re-export the .ds and commit at the start of Session 28. v13 is one line stale: create_invoice_from_selection and resync_location_labels are ahead of it. | ccode | OPEN | N | Session 28 start |
| Audit the rest of the form for the hidden-on-load / shown-on-user-input pattern. Sections, Facility fields, Type_of_Diversion and the Equipment/Other charge fields are fixed; others may remain. | cchat / ccode | OPEN | N | post-launch |

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
