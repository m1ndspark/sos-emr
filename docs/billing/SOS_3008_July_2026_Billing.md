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

## 6. `3008_july_map.csv` - NOT IN THIS REPO

The 76-row map (referral ID, completion date, provider last name) was built in
the ephemeral session container and did not reach the machine that maintains this
repo. It is not committed.

Two things to decide before it is:

1. **Recover it.** The authoritative copy is whatever Neil holds, or it can be
   regenerated from `sos_3008_log_july_2026.xlsx` plus the Creator referral
   records.
2. **Decide whether it belongs here at all.** Referral IDs bound to completion
   dates are patient-identifying in context, and this repo is PHI-clean by hard
   rule. If it is committed, it should carry no patient names.

Until then, the hardcoded ID list inside `create_3008_pvs_july` in Creator is the
only copy of the mapping.
