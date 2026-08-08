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
- Arithmetic (as billed): the 16 confirmed rows sum to $67,490 = $65,990
  complexity + $1,300 premiums (Polk $300, Suncoast - PIN $300, Tidewell $700)
  + $200 equipment (Sumter $25, Marion $175).
- Premium correction pending: the $1,300 premium figure used Empath Super STAT at
  $200 (AccentCare's rate) in error; the correct Empath rate is $400, which raises
  premiums to $2,100 and the grand total to $68,290. See section 2.

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

Rates applied on the run: After Hours $100, Super STAT $200. The Super STAT $200
was WRONG: $200 is AccentCare's Super STAT rate, not Empath's. Empath Super STAT
is $400 (Partner_Rates, Current and Active as of 2026-08-08; full card: Empath
$400, VITAS $500, AccentCare $200, Chapters $200). All five premiums were
written by backfill_pvs_premium_fees.

Per-visit breakdown (Premiums column is what was applied):

| Branch | Referral | Date | Complexity | Premiums |
|---|---|---|---|---|
| Empath / Polk | REF-072326-1423 | 7/23 | High | After Hours + Super STAT |
| Empath / Suncoast - PIN | REF-072826-1466 | 7/28 | Moderate | After Hours + Super STAT |
| Empath / Tidewell | REF-073026-1489 | 7/30 | High | After Hours + Super STAT |
| Empath / Tidewell | REF-072726-1459 | 7/27 | High | After Hours + Super STAT |
| Empath / Tidewell | REF-072626-1447 | 7/27 | High | After Hours only |

Subtotals as billed (Super STAT $200): Polk $300, Suncoast - PIN $300, Tidewell
$700 = $1,300.
Corrected (Super STAT $400): Polk $500, Suncoast - PIN $500, Tidewell $1,100 =
$2,100. Four Super STAT visits were each $200 short, so premiums are under-billed
by $800 and the run grand total rises from $67,490 to $68,290 once repriced.

CROSS-PARTNER PREMIUM ERROR (rate resolved, correction pending): same error class
as the VITAS 343-vs-323 complexity stamp in section 4 - a wrong partner's rate
stamped onto the PVS. backfill_pvs_premium_fees only fills BLANK premium fields,
so it will NOT overwrite the wrong $200 values; the affected visits need a premium
repricing pass (a reprice_draft_pvs equivalent for premiums), then void-and-rebill
for any already on a live invoice. Tracked as a blocking item in context/23;
sequence it before the Session 29 Empath re-batch so the re-run picks up $400.
context/10 corrected 2026-08-08.

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

--------------------------------------------------------------------------------
## SESSION 29 (2026-08-08) - INVOICE CAP, EMPATH RE-BATCH, $27,574 GAP
--------------------------------------------------------------------------------

### Why the cap exists
Empath requires every invoice to be under $3,000. `run_invoice_batch`
previously pulled every eligible visit for a branch, so re-running it after a
reset simply rebuilt the same oversized invoice. Splitting Empath Suncoast-PIN
alone would have meant seven manual selections.

### run_invoice_batch - signature change
`run_invoice_batch(int p_batchId, decimal p_maxTotal)`

- Fetches eligible visits **sorted by Visit_Completion_Date**, so splits are
  chronological and contiguous rather than arbitrary.
- Computes the **true per-visit total**:
  `Complexity_Charge + After_Hours_Fee + Super_Stat_Fee +
  Equipment_Charge_Amount + Other_Charges_Amount`.
  The previous version only looked at Complexity_Charge, so a cap on that
  alone would have undershot on any visit carrying premiums or equipment.
- Adds visits until the next one would push the running total past the cap,
  then leaves every remaining visit for the next run. `p_maxTotal` of 0 means
  no cap.
- A single visit larger than the cap still invoices alone, so the loop cannot
  stall.
- Preserves the `Visit Cancelled` skip.
- Result_Message now reports the batched total and how many visits were left
  behind.

### Supporting changes
- `Invoice_Batch` gained **Max_Invoice_Total** (Decimal, not mandatory,
  blank = no cap), so the limit travels with the batch record rather than
  being hardcoded per partner.
- Workflow **Invoice Batch On Create** (Invoice_Batch, record event Created,
  On Success) now reads that field and passes it as the second argument.
  This workflow is the only caller - batches are created from the purple "+"
  on Invoice_Batch_Report, which just adds a record.

### Invoices reset this session

| Invoice | Branch | Was | Visits released |
|---|---|---|---|
| INV-000022 | Empath Suncoast - PIN | $17,900 | 46 |
| INV-000023 | Empath Tidewell | $16,425 | 38 |
| INV-000021 | Empath Suncoast - HIL | $6,179 | 17 |
| INV-000024 | Empath Marion | $4,970 | 14 |
| INV-000037 | (see Books) | ~$17,000 | - |

AccentCare has no sub-$3,000 requirement; INV-000015 ($5,704) and INV-000016
($7,566) were deliberately left alone.

### Re-batched
Suncoast - PIN only, into seven capped invoices totalling exactly $17,900:
INV-000029 ($2,658), INV-000030 ($2,805), INV-000031 ($2,835),
INV-000032 ($2,633), INV-000033 ($2,921), INV-000034 ($2,817),
INV-000035 ($1,231).

### THE GAP - $27,574 unbatched
Tidewell, Suncoast-HIL and Marion were reset and never re-run.

| Branch | Visits | Value |
|---|---|---|
| Empath Tidewell | 38 | $16,425 |
| Empath Suncoast - HIL | 17 | $6,179 |
| Empath Marion | 14 | $4,970 |

Position at time of check: **$41,091 live in Books** - $38,787 sent plus
$2,304 still draft (LifePath $323, Sumter $513, HPH $545, Good Shepherd $545,
Villages $378).

July PVS export totals: $66,878 complexity + $400 equipment, with premiums
absent from that export. Expected landing point once the three Empath branches
are re-run: roughly **$68,600**.

ACTION: create a capped Invoice_Batch record (Max Invoice Total 2999) for each
of the three branches and repeat until Result_Message reports no visits left.

### Books configuration
- Payment terms set to **Net 30** on all customers, by hand. The Creator
  payload sends no payment_terms, so Books had been falling back to each
  customer record's Due on Receipt.
- Default invoice email subject is editable at Settings -> Templates ->
  Email Templates. Note that once sending moves to the API, the `subject`
  parameter in the request overrides the template.
- `to_mail_ids` on the Books email endpoint takes raw email addresses, so the
  approval dashboard can send without Books contact persons ever being
  populated. This removes the "16 name-only customers" blocker from the
  dashboard send path (it still applies to sending from the Books UI).
