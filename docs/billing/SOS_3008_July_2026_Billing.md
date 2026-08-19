# July 2026 3008 Billing Backfill - COMPLETE

Investigated Session 34, shipped Session 35, both 2026-08-19.

**Status: DONE.** `create_3008_pvs_july` ran COMMIT and created 76 PVS records,
zero skipped. Invoices generated in two batches by branch: **46 Orlando, 30
Tampa**.

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

## 4. What was built, and what it took to run

### The provider column was the wrong organization's staff

The first DRYRUN failed **76 of 76** on "no employee".

The `Provider` column in `sos_3008_log_july_2026.xlsx` holds the **hospice's**
staff, not SOS clinicians. Every name in it (Abboud, Mayo, Keyes, Valentino,
Rasheed) belongs to the partner. None of them are, or should be, in `Employees`.
The whole first pass was matching against the wrong organization's people, which
is why it failed uniformly rather than partially.

The real attribution came from a different file: `Referrals_3008_v1.xlsx`, sheet
**"July 2026"**, column `Provider`.

| SOS clinician | Visits |
|---|---|
| Ann Smith APRN | 41 |
| Kayla Kolanko PA-C | 35 |
| **Total** | **76** |

**All 76 matched on name plus DOB, with none left over.**

### `create_3008_pvs_july(pMode)`

Body: [create_3008_pvs_july.dg](create_3008_pvs_july.dg) (logic verbatim, 76 data
rows redacted).

- **Matches `Employees` on first AND last name.** `Kolanko` alone is ambiguous
  with Joshua, so a surname-only match would attribute Kayla's visits to the wrong
  clinician. The row's `First Last` is split on the space and both halves are
  matched, along with `Employee_Status == "Active"`.
- **Referral IDs are resolved in Python and hardcoded**, so Deluge does zero name
  matching. The matcher is what failed originally, so it is kept out of the
  runtime path entirely.
- **Skips** any row that already has a 3008 PVS, has no active employee for that
  name, or has no current `Cares 3008 Assessment` rate on the branch.
- **Stamps `PVS_ID` inside the insert**, from `Sequence_Tracker`, because form
  workflows do not fire on a Deluge insert. See section 8 for why this is inside
  the insert rather than after it.
- Sets `Invoice_Status = Draft` and `Hold_From_Invoicing = No`, so all 76 land in
  the next invoice run.
- Takes `DRYRUN` or `COMMIT`.

### Branch attribution: the referral wins, not the log

Billing branch comes from each referral's `Partner_Branch_Link`, **not** from the
log's `Location` column. They agree on 72 of 76.

The four that disagree bill to the referral's branch, per Neil's ruling that the
referral is authoritative:

| Patient | Log says | Billed to |
|---|---|---|
| J.L. | Tampa | Orlando |
| M.D.J. | Orlando | Tampa |
| R.D.J. | Orlando | Tampa |
| J.G. | Orlando | Tampa |

Two of the four carry a "De " surname particle, the same import defect tracked
since Session 32. Patient identities are held by Neil, outside the repo.

### Result

COMMIT created **76 PVS records, zero skipped**, zero missing referrals, zero
missing employees, zero missing rates. Invoices then generated in two batches, one
per branch: **46 Orlando, 30 Tampa**.

### Data note

`Employees` had no initials for **Ann Smith** or **Catherine Hardy**. Ann's were
added before COMMIT; without them 41 PVS IDs would have ended in a trailing
hyphen. **Catherine Hardy still has none** and it remains open in
`context/23_task_list.md`.

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

**Decided Session 34, reaffirmed Session 35.** Neither `3008_july_map.csv` nor the
data block inside `create_3008_pvs_july` is committed here.

Why. The rows carry no patient names and no DOBs, only referral ID, completion
date and, as of Session 35, the SOS clinician's name. But a live referral ID bound
to a real date of service is patient-identifying: it is a record locator for a
specific person, and the date of service is itself an identifier. CLAUDE.md
guarantees this repo holds field link names rather than patient data.

**The Session 35 row list is MORE identifying than the Session 34 one, not less.**
The earlier version carried only a hospice surname; this one names the SOS
clinician who saw each patient, so every row now ties a specific person to a
specific encounter on a specific date.

`3008_july_map.csv` is more sensitive still: it has a `Patient` column with real
names alongside dates of service. Wherever it is backed up has to be
PHI-appropriate, not merely durable.

### The three copies, none of them versioned

| Copy | Contains |
|---|---|
| The function in Creator | the row list |
| `MPU Reporting/deluge/create_3008_pvs_july.dg` | the row list |
| `MPU Reporting/3008_july_map.csv` | Patient, Completed, Site, Provider, ReferralID |

`docs/billing/create_3008_pvs_july.dg` is redacted by design and **cannot serve as
the backup.** Pasting the repo copy into Creator produces a function that creates
nothing.

The backfill has now run, so losing the mapping no longer blocks billing. It still
matters as the audit trail for how 76 invoices were attributed.

## 7. Defect 1: PVS_ID sequence off by one - FOUND AND FIXED

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

---

## 8. Defect 2: re-fetching the inserted record - FOUND AND FIXED

Found in Session 35, during the COMMIT run. The second sequence-related defect in
this one function.

### What was wrong

The function stamped `PVS_ID` by inserting the record, then **re-fetching it** to
write the ID onto it:

```
v_new = insert into Encounter_PatientVisit [ ... ];
v_pvsRow = Encounter_PatientVisit[ID == v_new.ID];    // throws
v_pvsRow.PVS_ID = "PVS-" + v_seq + "-" + v_emp.Employee_Initials;
```

That threw `Invalid collection object found`. The cause is a Creator behavior
worth memorising: **`insert into` returns the record ID as a NUMBER, not a
record.** `v_new` is already the ID, so `v_new.ID` is a field access on a number
and fails.

### The fix, now in place

The sequence is read first, and `PVS_ID` is set **inside the insert**:

```
v_seq = 0;
for each  v_st in Sequence_Tracker[Object_Prefix == "PVS"]
{
    v_seq = v_st.Object_Sequence;
    break;
}
if(pMode == "COMMIT")
{
    for each  v_st2 in Sequence_Tracker[Object_Prefix == "PVS"]
    {
        v_st2.Object_Sequence = v_seq + 1;
        break;
    }
    v_new = insert into Encounter_PatientVisit
    [
        PVS_ID = "PVS-" + v_seq + "-" + v_emp.Employee_Initials
        ...
    ];
}
```

There is no re-fetch anywhere in the function now. The sequence read sits outside
the `COMMIT` branch and the increment inside it, so a DRYRUN still reads the
tracker without consuming from it.

Note the ordering consequence: the tracker is incremented immediately before the
insert, so a failed insert consumes a sequence number and leaves a gap in the
`PVS_ID` run. Gaps are harmless; duplicates are not, and this ordering prevents
duplicates.

The same `insert into` behavior is recorded as a general Creator gotcha in
`docs/fax/SOS_PVS_Fax_System_Design.md` section 11, since it will bite anything
else that inserts a record and wants its ID.
