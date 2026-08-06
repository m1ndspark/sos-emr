# July Billing Run (Session 28, 2026-08-05)

Record of the first real invoicing run: the July visits (200-record PVS import
plus the June partial) invoiced through the Invoice Batch into Zoho Books, one
invoice per branch. This file captures the branch totals, the two billing
defects found and their causes, the VITAS rate correction, and the standing
rules the run confirmed.

Status of this record: branch totals, per-visit premium and equipment
breakdowns, and the VITAS invoice void chain are all confirmed live (2026-08-05,
read back off the Invoice Batch Result Message). The one open cross-check is the
Super STAT premium rate: context/10 lists $250, the run applied $200 (see
section 2). Record IDs and dates are used throughout; patient names are
deliberately omitted to keep the repo PHI-clean.

--------------------------------------------------------------------------------
## 1. Branch totals (16 branches)
--------------------------------------------------------------------------------

Read back off the Invoice Batch Result Message and confirmed live (2026-08-05).
One row per branch = one Books invoice. The Visits column includes No Charge
visits, billed at $0 by design, so it runs slightly ahead of the billable count.

| Partner / Branch | Visits | Invoice total | Notes |
|---|---|---|---|
| VITAS / Sumter | 4 | $513 | incl. $25 equipment |
| VITAS / Villages | 2 | $378 | |
| Chapters / LifePath | 1 | $323 | |
| Chapters / Good Shepherd | 1 | $545 | |
| Chapters / HPH Hospice | 1 | $545 | |
| AccentCare / Miami | 1 | $545 | |
| AccentCare / Pasco | 5 | $1,139 | |
| AccentCare / Hernando | 6 | $1,194 | |
| AccentCare / Hillsborough | 21 | $5,704 | understated pending equipment |
| AccentCare / Pinellas | 19 | $7,566 | understated pending equipment |
| Empath / Polk | 3 | $1,531 | incl. $300 premiums |
| Empath / Trustbridge | 5 | $2,033 | understated pending equipment |
| Empath / Marion | 14 | $4,970 | incl. $175 equipment |
| Empath / Suncoast - HIL | 17 | $6,179 | |
| Empath / Suncoast - PIN | 46 | $17,900 | incl. $300 premiums |
| Empath / Tidewell | 38 | $16,425 | incl. $700 premiums; understated pending equipment |
| TOTAL | 184 (182 billable) | $67,490 | |

Notes:
- Visit counts include No Charge visits at $0; 182 of the 184 are billable.
- Hillsborough, Pinellas, Tidewell and Trustbridge are still understated pending
  five equipment amounts from Josh and Ann (tracked in context/23). Their totals
  will rise once those are entered.
- Arithmetic (reconciled): the 16 confirmed rows sum to $67,490 = $65,990
  complexity + $1,300 premiums (Polk $300, Suncoast - PIN $300, Tidewell $700)
  + $200 equipment (Sumter $25, Marion $175).

--------------------------------------------------------------------------------
## 2. Defect: premium fees not populated on imported visits
--------------------------------------------------------------------------------

Premium fees are the After Hours (After_Hours_Fee) and Super STAT
(Super_Stat_Fee) add-ons. They are manual-entry currency fields on the PVS and
no workflow auto-fills them from Partner_Rates, which does carry both premium
rate types (see context/23 open item and context/10). The July PVS import did
not set them, so premium-eligible visits carried blank premium fields and would
have under-billed.

Fix: the new function backfill_pvs_premium_fees was built to backfill the
premium fee fields for the affected visits. (Its exact selection logic will be
recorded against the v20 body once synced; do not describe its internals from
memory.)

Applied rates on the run: After Hours $100, Super STAT $200. All premiums were
recovered by backfill_pvs_premium_fees: $1,300 across 5 visits.

Per-visit breakdown:

| Branch | Referral | Date | Complexity | Premiums |
|---|---|---|---|---|
| Empath / Polk | REF-072326-1423 | 7/23 | High | After Hours + Super STAT |
| Empath / Suncoast - PIN | REF-072826-1466 | 7/28 | Moderate | After Hours + Super STAT |
| Empath / Tidewell | REF-073026-1489 | 7/30 | High | After Hours + Super STAT |
| Empath / Tidewell | REF-072726-1459 | 7/27 | High | After Hours + Super STAT |
| Empath / Tidewell | REF-072626-1447 | 7/27 | High | After Hours only |

Subtotals: Polk $300, Suncoast - PIN $300, Tidewell $700 (3 x After Hours + 2 x
Super STAT). Total $1,300.

RATE DISCREPANCY TO RECONCILE: context/10 records Super STAT at $250, but this
run applied $200 (confirmed by the Tidewell arithmetic: 3 x 100 + 2 x 200 =
700). Confirm which is the contract rate and update context/10 to match. [CONFIRM]

--------------------------------------------------------------------------------
## 3. Defect: stale equipment charge billed on hidden field
--------------------------------------------------------------------------------

Hiding a field does not clear it. Unticking Additional Charges hid
Equipment_Charge_Amount but left the stored value in place, and
create_invoice_from_selection billed that stale value. See the matching entry in
context/05_deluge_learnings.md ("HIDING A FIELD DOES NOT CLEAR IT"). The
standing rule going forward is to clear the value whenever an optional charge
field is hidden.

Corrections made in the run: Marion and Sumter equipment amounts were corrected.
Equipment that made it onto the run (from the branch totals above): VITAS /
Sumter $25, Empath / Marion $175. The new function set_pvs_equipment_charge was
built to set/clear the equipment charge deterministically rather than relying on
the form's hidden-field state.

Before/after (recovered from the Equipment Charge Details text):

| Branch | Record | Date | Detail | Before | After | Delta |
|---|---|---|---|---|---|---|
| Empath / Marion | PVS-1164-JK | 7/11 | G-Tube | $4,795 | $4,970 | +$175 |
| VITAS / Sumter | (Sumter visit) | 7/16 | Volar splint | $488 | $513 | +$25 |

Marion's amount was entered via set_pvs_equipment_charge because the form could
not save at the time (the Partner_POC_Phone defect; see context/05).

Still understated pending five equipment amounts from Josh and Ann: AccentCare /
Hillsborough, AccentCare / Pinellas, Empath / Trustbridge, Empath / Tidewell
(tracked in context/23). Those four branch totals will rise once the amounts are
entered.

--------------------------------------------------------------------------------
## 4. VITAS rate correction: 343 vs 323
--------------------------------------------------------------------------------

INV-000006 billed VITAS Sumter Moderate Complexity at 343 when the VITAS rate
card says 323 (recorded in context/05 under "STAMPED CHARGES DO NOT FOLLOW A
RATE CHANGE").

Evidence for 323: the VITAS Partner_Rates card prices Sumter Moderate Complexity
at 323. The 343 figure is AccentCare's Moderate Complexity rate (context/03,
_INDEX.md), i.e. a cross-partner value that did not belong on a VITAS visit.

Mechanism: Complexity_Charge is stamped onto the PVS at the moment of lookup and
backfill_pvs_complexity_charge only fills blanks, so a stamped visit keeps its
original price even after the rate card is corrected. reprice_draft_pvs was built
to re-price Draft, un-invoiced visits to the current card; it is for Draft visits
only and must not touch invoiced ones.

Disposition (void chain, all voids executed through reset_invoice and voided in
Books):
- INV-000006 (VITAS / Sumter, $508): voided. Had billed Moderate at 343 against
  a card that reads 323.
- INV-000007 (replacement after reprice_draft_pvs, $488): voided, to add the $25
  equipment charge.
- Current live Sumter invoice is the third, $513 (the $488 repriced total plus
  the $25 equipment correction from section 3).

--------------------------------------------------------------------------------
## 5. Standing rules confirmed by the run
--------------------------------------------------------------------------------

- Cost fields are editable until the visit is invoiced (they lock only when
  Invoice_Status == "Final").
- No Charge visits are shown on the invoice at $0; cancelled visits (Visit
  Cancelled) are excluded from invoicing entirely.
- One invoice per branch.
- A failed batch is replaced, not re-saved: void/reset the failed attempt and
  run a fresh batch rather than editing and re-saving the failed invoice.

--------------------------------------------------------------------------------
END
--------------------------------------------------------------------------------
