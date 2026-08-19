# July 2026 3008 Billing Backfill

Session 34, 2026-08-19. Closes the July 3008 billing gap.

> **PHI note.** Patient identifiers are reduced to initials here, per the hard
> rule in CLAUDE.md. Neil holds the identity key outside the repo. This matches
> the convention already used in `context/23_task_list.md`.

---

## 1. The problem

Billing runs off PVS records. No PVS records existed for 3008 completions, so
July 3008s could not be invoiced.

## 2. The source data

- The 3008 log is `sos_3008_log_july_2026.xlsx`, uploaded 2026-08-14.
- 76 completions: 48 Orlando, 28 Tampa.
- No duplicate patients. Every completion date falls inside July.
- **Bill on completion date, not referral date.** Neil's ruling.

---

## 3. The 22 "missing" referrals were a matching failure, not an import failure

The first pass suggested 22 of the 76 completions had no referral in Creator.
That was wrong, and it matters that the record says so plainly:

**All 83 Cognito 3008 referrals imported into Creator successfully. The import
was clean. The matcher failed.**

The 22 break down as follows.

| Cause | Count | Detail |
|---|---|---|
| Century DOB bug | 18 | DOBs stored with a 20xx century. Patient R.S. is stored `2043-04-16`. |
| Name particle bug | 3 | A "De " surname particle was dropped on import: "De Jesus" became MI `D` and last name `Jesus`. Same failure for "De La Rosa". |
| First name mismatch | 1 | Creator and the log carry different first names for the same surname and DOB (patients N-1 / N-2). Genuine data conflict, not a matcher bug. |
| DOB conflict | 1 | Patient C.D.L.R.: Creator says `1956-10-30`, the log says `1958-06-06`. One of the two is wrong. |
| **Total** | **22** | |

The first two causes, 21 of the 22, are the same century-DOB and name-particle
defects already tracked in `context/23_task_list.md`. **This is the second time
they have cost real time.** They are import-side defects and they will keep
recurring until the importer is fixed.

The last two are real data conflicts and need Neil to resolve them against the
identity key.

---

## 4. What was built

### `create_3008_pvs_july(pMode)`

Creates the 76 PVS records. Body: [create_3008_pvs_july.dg](create_3008_pvs_july.dg)
(PENDING extraction from Creator).

- **Referral IDs were resolved in Python and hardcoded into the function**, so
  Deluge does zero name matching. This is deliberate: the matcher is what failed,
  so it is removed from the runtime path entirely.
- Each row is referral ID, completion date and provider last name. The row set is
  `3008_july_map.csv` (see section 6).
- It **skips** any row that already has a 3008 PVS, has no active employee for
  that last name, or has no current `Cares 3008 Assessment` rate on the branch.
- It **stamps the PVS ID from `Sequence_Tracker`**, because form workflows do not
  fire on Deluge inserts.
- It sets `Invoice_Status = Draft` and `Hold_From_Invoicing = No`, so all 76 land
  in the next invoice run.
- It takes `DRYRUN` or `COMMIT`.

**NOT YET RUN.** Neil owes a DRYRUN output before COMMIT.

---

## 5. How 3008s bill, for the record

A 3008 is a PVS with:

```
Type_of_Entry     = 3008
Complexity_Level  = "Cares 3008 Assessment"
```

That `Complexity_Level` matches the same `Rate_Type` in `Partner_Rates` for the
billing branch, fills `Complexity_Charge`, and flows to the draft invoice exactly
like any other visit.

The only thing that breaks it is a branch with no 3008 rate on file, and
`diag_partner_rates` already reports that gap per location.

---

## 6. The 76-row map stays out of this repo

**Decided 2026-08-19.** Neither `3008_july_map.csv` nor the equivalent data block
inside `create_3008_pvs_july` is committed here.

Why. The rows carry no patient names and no DOBs, only referral ID, completion
date and provider last name. But a live referral ID bound to a real date of
service is patient-identifying: it is a record locator for a specific person, and
the date of service is itself an identifier. CLAUDE.md guarantees that this repo
holds field link names rather than patient data, and a 76-row roster of real
referrals with service dates is patient data. It does not belong here.

What that costs, and it is a real cost:

- `docs/billing/create_3008_pvs_july.dg` **does not round-trip into Creator.**
  Every line of logic is there verbatim and reviewable; only the `v_rows.add(...)`
  block is replaced by a comment. Pasting the repo copy into Creator would produce
  a function that creates nothing.
- **The copy in Creator is now the only copy of the mapping.** If that function is
  edited or deleted before the backfill runs, the mapping is gone and has to be
  rebuilt from `sos_3008_log_july_2026.xlsx` against the Creator referral records.

Two things for Neil:

1. **Confirm the call.** If you would rather have the rows tracked, say so and
   they go in.
2. **Keep a copy of the map outside the repo** before the Creator function is
   touched. That is tracked as an OPEN row in `context/23_task_list.md`.

---

## 7. PVS_ID sequence defect - FOUND AND FIXED

Found by ccode 2026-08-19 when the real body was first committed and compared
against the other PVS minters in the repo. **Fixed in source and re-extracted the
same day.** Recorded here because it would have been silent, and because it
explains why the DRYRUN gate matters.

### What was wrong

Every minter in this repo treats `Sequence_Tracker.Object_Sequence` as **the next
free number**. `create_3008_pvs_july` treated it as the last used one:

```
v_seq = v_st.Object_Sequence + 1;   // read N, compute N+1
v_st.Object_Sequence = v_seq;       // store N+1
... "PVS-" + v_seq                  // issue PVS-(N+1)
```

With the tracker at `N`, that issues `PVS-(N+1)` through `PVS-(N+76)` and leaves
the tracker at N+76, the **last used** value rather than the next free one. `PVS-N`
is skipped, which is a harmless gap. The damage is at the other end: the next PVS
created through the form reads N+76, treats it as free, and issues it a second
time. **Two visits, one `PVS_ID`, in a system where `PVS_ID` is the billing record
locator.**

DRYRUN could not have caught it. The mint sits inside `if(pMode == "COMMIT")`, so
a dry run produces a clean report and never touches `Sequence_Tracker`.

### The fix, now in place

```
for each  v_st in Sequence_Tracker[Object_Prefix == "PVS"]
{
    v_seq = v_st.Object_Sequence;
    v_st.Object_Sequence = v_seq + 1;
    break;
}
```

Reads N, issues `PVS-N`, stores N+1, and breaks. This matches
`Encounter_PatientVisit/OnSuccess__PVS_Stamp_Generator.dg` and
`functions/backfill_pvs_ids.dg` exactly.

The `break` matters independently: without it the loop double-increments if a
second `PVS` row ever appears in `Sequence_Tracker`.

The identical defect was in `send_pvs_fax`'s `FAX` minter and is also fixed. See
`docs/fax/SOS_PVS_Fax_System_Design.md` section 8.1, defect 5. All four minters in
the repo now share the one convention.

### What is left

Nothing on this defect. The remaining gate on the backfill is Neil running DRYRUN,
reviewing the output, then COMMIT.
