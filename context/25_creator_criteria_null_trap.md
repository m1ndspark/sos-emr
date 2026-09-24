# Creator Criteria Null Trap

Found 2026-09-24 (Session 53). The highest-value finding of that session. It
invalidated a Session 52 conclusion. Related: `context/05_deluge_learnings.md`.

## The rule

In a Zoho Creator criteria, `Field != "value"` does NOT match records where
`Field` is null. They are dropped silently. No error, no warning.

```
// WRONG - skips every record where Fax_Status is null
for each r in Encounter_PatientVisit[Fax_Status != "Sent"]

// RIGHT - fetch wider, test in the loop
for each r in Encounter_PatientVisit[ID != 0]
{
    if(r.Fax_Status == "Sent") { continue; }
    ...
}
```

Test in the loop, not the criteria. Any `!=` in a criteria is a bug until
proven the field can never be null.

## How it was found: 59 vs 402

- `diag_unfaxed_by_branch` reported 59 unfaxed notes.
- The rewritten `send_fax_digest` reported 402 on the same data.
- The diag used `Fax_Status != "Sent"`. A note never faxed has a null
  `Fax_Status`, so the diag excluded every note that had never been faxed,
  which was most of them. The gap was 343 notes.
- This also explains the Session 52 "447 vs 59" discrepancy between
  `diag_fax_readiness` and `diag_unfaxed_by_branch`.

Consequence: the Session 52 finding "only 3 notes are blocked by a missing fax
number" was wrong. The real number is 20.

## Fixed (three places)

| Object | Type | Status |
|---|---|---|
| `resolve_pvs_fax_target` | function, the shared fax gate | LIVE |
| Fax This Note Preview And Gate | workflow, the PVS-form tickbox gate | LIVE |
| `diag_fax_readiness` | diagnostic function | fixed |

Both live fixes also corrected a second defect. The old code took the first
matching contact and stopped, so the duplicate count was computed separately
from the contact it picked. Both now come from one pass.

## Still unfixed

Each silently drops nulls. From the Session 53 log, PART 6.

| Criteria | Note |
|---|---|
| `Fax_Status != "Sent"` in `diag_unfaxed_by_branch` | the original offender; not yet fixed |
| `Partner_PVS_Fax != ""` | fixed in the three places found; re-sweep for others |
| `Referral_ID != ""` | two occurrences |
| `Primary_Office == "Yes" && ID != input.ID` | |
| `QC_Reviewed != "Yes"` | |
| `Employee_Initials == "" && Employee_Email != ""` | |
| `Current_Rate != "Yes"` | |
| `Partner_Code == v_partnerCode && ID != input.ID` | |
| `Visit_Status != "Cancelled"` in `diag_sept_pvs_completeness` | |

`ID != input.ID` is safe on its own (ID is never null); the risk in those rows
is only if another clause in the same criteria can be null. Check each one
when swept.

## Sweep procedure

1. Grep the current .ds for `!=` inside `[ ]` criteria.
2. For each hit, ask: can this field be null on a real record?
3. If yes, move the `!=` test into the loop body.
4. For diagnostics, re-run and record the before and after counts.
