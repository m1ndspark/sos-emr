# July Billing Run (Session 28, 2026-08-05)

Record of the first real invoicing run: the July visits (200-record PVS import
plus the June partial) invoiced through the Invoice Batch into Zoho Books, one
invoice per branch. This file captures the branch totals, the two billing
defects found and their causes, the VITAS rate correction, and the standing
rules the run confirmed.

Status of this record: the branch totals below were read back off the Invoice
Batch Result Message and confirmed live (2026-08-05). The defect narratives and
standing rules are captured from Session 28. Items still marked [CONFIRM] are
held for Neil to verify.

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
- Arithmetic: the 16 confirmed rows sum to $67,490. The live read-back was
  reported as ~$67,290; the $200 delta is unreconciled [CONFIRM].

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

Premiums that made it onto the run (from the branch totals above): Empath / Polk
$300, Empath / Suncoast - PIN $300, Empath / Tidewell $700. Rate card carries
$100 After Hours / $250 Super STAT per context/10.

[CONFIRM - the per-visit breakdown behind each branch's premium subtotal and
whether any premium-eligible visits were still missed.]

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

Still understated pending five equipment amounts from Josh and Ann: AccentCare /
Hillsborough, AccentCare / Pinellas, Empath / Trustbridge, Empath / Tidewell
(tracked in context/23). Those four branch totals will rise once the amounts are
entered.

[CONFIRM - the specific Marion and Sumter records corrected and their before/after
equipment amounts.]

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

[CONFIRM - disposition of INV-000006 itself (already invoiced at 343): whether it
was voided via reset_invoice and rebilled at 323, or left as billed with only the
Draft visits repriced.]

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
