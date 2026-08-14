# SOS Invoice Corrections - Duplicate Visit Run

Date: 2026-08-13
Session: 31 (EOD)

Record of the duplicate-visit correction run. Five sent invoices carried
duplicated visits and were voided and rebilled. Definition-only record: no PHI.

--------------------------------------------------------------------------------
## Corrections applied
--------------------------------------------------------------------------------

| New invoice | Replaces | Partner / Branch | Amount | Visits |
|---|---|---|---|---|
| INV-000051 | INV-000030 | Empath, Suncoast - PIN | $2,119 | 5 |
| INV-000052 | INV-000016 | AccentCare, Pinellas | $6,966 | 17 |
| INV-000053 | INV-000015 | AccentCare, Hillsborough | $5,649 | 20 |
| INV-000054 | INV-000038 | (not recorded in source) | $2,915 | 9 |
| INV-000055 | INV-000041 | (not recorded in source) | $2,835 | 7 |

INV-000050 was an intermediate invoice, never sent. It was reset and re-batched
as INV-000051.

Total over-billing corrected: $1,451 across the 5 sent invoices.

--------------------------------------------------------------------------------
## Root cause
--------------------------------------------------------------------------------

run_invoice_batch had no duplicate check, so the same visit could be pulled into
more than one batch and billed twice. The v23 rewrite of run_invoice_batch adds a
pre-flight duplicate scan keyed on referral + date of service + complexity level,
with PVS_Referral_ID then patient name + DOB fallbacks (see context/05 and the
Session 31 EOD deltas).

--------------------------------------------------------------------------------
## Diagnostic note (not every "duplicate" was one)
--------------------------------------------------------------------------------

diag_duplicate_visits reported 10 sets totaling $1,996 raw. On review several
were legitimate, not duplicates. For example a Telemedicine x-ray coordination
visit plus a separate post-x-ray intervention visit are two distinct billable
encounters that the raw key flags as a pair. Only the 5 confirmed duplicates
above were corrected; the corrected over-billing ($1,451) is therefore less than
the raw diagnostic figure ($1,996).

--------------------------------------------------------------------------------
END
--------------------------------------------------------------------------------
