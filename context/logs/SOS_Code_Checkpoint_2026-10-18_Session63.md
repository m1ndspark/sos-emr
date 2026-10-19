# SOS Code - Checkpoint - 2026-10-18 - Session 63

Covers work since the Session 62 EOD (2026-10-16), across 2026-10-17 and 2026-10-18. IDs only, no PHI.

## 1. Four wrong-branch visits fixed and rebilled (10/17)

Cause: referral branch chosen wrong at submission (REF-1592, REF-1472 as Tidewell) or assigned when blank (REF-1510, REF-1134 to Suncoast HIL). Nothing checks branch against patient ZIP/county.

| PVS | Referral | From | To |
|---|---|---|---|
| PVS-1767-AS | REF-1510 | Suncoast HIL (INV-000104) | Suncoast PIN |
| PVS-1542-AS | REF-1134 | Suncoast HIL (INV-000104) | Suncoast PIN |
| PVS-1785-JK | REF-1592 | Tidewell (INV-000122) | Suncoast HIL |
| PVS-1515-JK | REF-1472 | Tidewell (INV-000119) | Suncoast PIN |

Sequence used:
1. fix_pvs_branch_batch PREVIEW. This is new: it is a read-only check of billing branch against the referral's branch, regardless of invoice status.
2. reset_invoice on INV-000122, INV-000119 and INV-000104, which voided them in Books and returned their visits to Draft.
3. fix_pvs_branch_batch COMMIT. It calls sync_pvs_branch_from_referral, and the charges were unchanged.
4. preview_invoice_batch_pool. This is new: it lists exactly what run_invoice_batch will pick up for a branch and date range.
5. Four Invoice_Batch records were run.

Result:

| New invoice | Branch | Replaces | Invoice date | Amount |
|---|---|---|---|---|
| INV-000132 | Tidewell | INV-000119 | 10/16 | $2,904 |
| INV-000133 | Tidewell | INV-000122 | 10/16 | $2,300 |
| INV-000134 | Suncoast HIL | INV-000104 | 10/04 | $1,916 |
| INV-000135 | Suncoast PIN | new Correction invoice | 10/17 | $1,205 |

- The total is $8,325, equal to the 3 voided invoices.
- All four were verified line by line in Books and sent by Neil.
- The second void explanation email went to Asha Johnson from Neil's inbox.

## 2. Empath contract rates corrected, forward only (10/17)

- The SOS Fee Schedule (01/22/2025) sets Telemedicine 65, Minor 170, Moderate 373, Complex 575, Hospital at Home 1,099/day, After Hours 150 and Super STAT 400.
- Creator Partner_Rates held 343/150/55 and 999 at every Empath branch.
- Neil ruled: rates forward only, effective 10/01/2026. Sent invoices stay as billed.
- New function update_partner_rates COMMIT inserted 24 new current rows (6 branches × 4 types) and set the old rows to Current_Rate = No.
- It also re-priced 20 October Draft Empath visits.
- Re-verified with a PREVIEW: 24 at the new amount, 0 to re-price. Empath - Main Hospice has no rate rows.
- MPU ruling (10/18): the MPU uses the rate actually billed. September = 343/150/55; October onward = 373/170/65. Recorded in the project doc claude/SOS_MPU_Reporting_Decisions_Log.md.

## 3. Unbilled Marion July visits billed (10/18)

- New function diag_unbilled_visits(date p_from, date p_to, string p_partner) found the gap for Empath, Jul–Sep:
  - 27 ready
  - 3 needing a fix
  - 34 correctly excluded
- Books has no Empath - Marion invoice for July. INV-000017, the gap in the alphabetical 8/5 batch, exists in neither Books nor Creator, and Marion has no Books payments.
- PVS-1502-JK and PVS-1503-JK were retired as duplicates of PVS-1050-JK and PVS-1051-JK (retire_pvs_duplicate_pairs).
- New function reprice_pvs_batch(string p_pvsIds, string p_mode) re-priced High 545 → 575 on PVS-1211-JK, 1201-JK, 1119-JK, 1050-JK and 1164-JK.
- Batch: INV-000136 ($2,736) and INV-000137 ($2,384) = $5,120, 14 visits including 1 No Charge line, dated 10/18.
- Cross-checked against a full Books line index (119 invoices, 1,069 visit blocks) by patient and DOS: no visit appears on any other invoice.
- Neil to send.
- Neil ruled: no prior-month data-integrity work unless urgent. The 14 late-July Pinellas/Tidewell/HIL visits (≈$6,022) shown as unbilled by the diag are NOT being pursued.

## 4. Live Creator access (10/18)

- A Zoho MCP server ("SOS to Zoho Platform") was added as a claude.ai custom connector, and Claude reads Creator records live.
- Seven all-field read-only reports were built and verified against the v66 .ds field lists:
  - API_PVS_All
  - API_Referrals_All
  - API_Invoices_All
  - API_Invoice_Batch_All
  - API_Partner_Rates_All
  - API_Partner_Locations_All
  - API_Partners_All
- Rule changes approved:
  - The diagnostic-function rule for data questions is dropped.
  - No more export uploads.
  - Neil can say "done" in place of pasting PREVIEW/COMMIT output, and Claude verifies by reading the records.
- Unchanged:
  - The .ds stays the only source for code.
  - All writes go through PREVIEW/COMMIT functions, never through the connector.
- Risk: the connector currently exposes delete, schema and publish tools. Remove them in Zoho MCP.

## 5. New functions this session (all Deluge, namespace default, return string)

| Function | Arguments |
|---|---|
| fix_pvs_branch_batch | string p_pvsIds, string p_mode |
| preview_invoice_batch_pool | string p_branchLabel, date p_from, date p_to |
| update_partner_rates | string p_partner, string p_rates, date p_effective, string p_mode |
| diag_unbilled_visits | date p_from, date p_to, string p_partner |
| reprice_pvs_batch | string p_pvsIds, string p_mode |

Flag: all five break the standing argument-order rule (p_mode first, then dates, then IDs). The reorder awaits Neil's go.

## 6. Open items at checkpoint

| Task | Owner | Status | Blocking | Deadline |
|---|---|---|---|---|
| Send INV-000136 / INV-000137 (Marion July) | Neil | OPEN | N | 10/19 |
| Rebuild September MPUs from live data (billed Empath rates; 4 branch moves) | cchat | OPEN | Y (MPU send) | next session |
| VITAS rates vs contract (Creator Mod 343 / AH 150 / SS 500 vs log 323 / 100 / 200) | Neil | OPEN | N | - |
| Remove delete/schema/publish tools from the Zoho MCP connector | Neil | OPEN | N | - |
| Reorder arguments on the 5 new functions | Neil approval | OPEN | N | - |
| Prevention: branch vs ZIP/county check in audit_month_integrity, hard stop in run_invoice_batch, warning at referral save | cchat | OPEN | N | - |
| Auto Row_Status = Cancelled when Complexity_Level = Visit Cancelled | cchat | OPEN | N | - |
| Controls and required-checks docs for essential forms, plus visual graphs | cchat | OPEN | N | - |
| Monthly Data Book template (feeds billing and the MPU) | cchat | OPEN | N | - |
| Knowledge graph of app and processes (graph_v66.json ready) | cchat | OPEN | N | - |
| PVS-1515-JK MRN holds junk value "Hospice" (printed on INV-000135) | Neil | OPEN | N | - |
| Commit v66 sync (74 files + v65/v66 .ds) and this checkpoint | ccode | OPEN | N | next session |
| Parked: Cloudways MCP review; PVS-1308-NH test record on INV-000118; VITAS REF-1556 / PVS-1758-JK; Josh dateless PVS; remittance reconciliation; Books portals / Tiffany; QBO P&L compare; revenue-per-visit | Neil / cchat | PARKED | N | - |
