# SOS Code - Session Log - 2026-08-19 (Session 35) - EOD

Second block of 2026-08-19, after the Session 34 log was written. Two things
finished: the RingCentral fax stack is live and authenticating, and all 76 July
3008s are created and invoiced.

> **Patient identifiers redacted.** The source log named four patients in the
> branch-attribution table. This repo is PHI-clean by hard rule (CLAUDE.md), so
> they appear here as initials and the identity key stays with Neil. SOS employee
> names are not redacted; they are staff, not patients.

---

## Part 1 - July 3008 billing - DONE

### What shipped

`create_3008_pvs_july` ran COMMIT. **76 PVS records created, zero skipped**, zero
missing referrals, zero missing employees, zero missing rates.

Invoices generated in two batches, one per branch:

| Branch | Invoices |
|---|---|
| Orlando | 46 |
| Tampa | 30 |
| **Total** | **76** |

### The provider problem, and how it was solved

The first DRYRUN failed **76 of 76** on "no employee".

The `Provider` column in `sos_3008_log_july_2026.xlsx` holds the **hospice's**
staff (Abboud, Mayo, Keyes, Valentino, Rasheed), not SOS clinicians. None of them
are, or should be, in `Employees`. The whole first pass was matching against the
wrong organization's people.

Neil supplied `Referrals_3008_v1.xlsx`. Its **"July 2026"** sheet carries a sixth
column, `Provider`, with the actual SOS clinician:

| SOS clinician | Visits |
|---|---|
| Ann Smith APRN | 41 |
| Kayla Kolanko PA-C | 35 |

**All 76 matched on name plus DOB, with none left over.**

The function now matches `Employees` on **first AND last name**, because `Kolanko`
alone is ambiguous with Joshua.

### Branch attribution

Billing branch comes from each referral's `Partner_Branch_Link`, **not** from the
log's `Location` column. They agree on 72 of 76. The four that disagree bill to
the referral's branch, per Neil's ruling that the referral is authoritative:

| Patient | Log says | Billed to |
|---|---|---|
| J.L. | Tampa | Orlando |
| M.D.J. | Orlando | Tampa |
| R.D.J. | Orlando | Tampa |
| J.G. | Orlando | Tampa |

Two of the four carry a "De " surname particle, which is the same import defect
tracked since Session 32.

### How 3008s bill

`Type_of_Entry = 3008` and `Complexity_Level = "Cares 3008 Assessment"`, which
matches that `Rate_Type` in `Partner_Rates` for the billing branch, fills
`Complexity_Charge`, and flows to the draft invoice like any other visit.

### Defect found and fixed

The function originally **re-fetched the record it had just inserted** in order to
stamp the PVS ID. That threw `Invalid collection object found`, because
`insert into` returns the record ID as a number rather than a record.

Rewritten so the sequence is read first and `PVS_ID` is set **inside the insert**.
There is no re-fetch anywhere in the function now.

This is the second sequence-related defect in this one function. The first was the
off-by-one caught in Session 34.

### Data note

`Employees` had no initials for **Ann Smith** or **Catherine Hardy**. Ann's were
added before COMMIT; without them 41 PVS IDs would have ended in a trailing
hyphen. **Catherine still has none**, and remains open.

---

## Part 2 - RingCentral fax - auth live

### What is built and working

| Object | State |
|---|---|
| `API_Config` form, one record, client ID + secret + JWT | loaded |
| `Fax_Log` form, hidden, Deluge inserts only | built |
| `Visit_Status` and `Fax_Status` on `Encounter_PatientVisit` | added |
| `Sequence_Tracker` FAX record | done |
| `get_rc_token`, `build_pvs_fax_html`, `send_pvs_fax`, `poll_fax_status` | saved and compiling |

`poll_fax_status` returns `polled 0, sent 0, retry pending 0, permanent fail 0,
stuck 0`. **The whole chain compiles, authenticates and runs.**

### RingCentral app

REST API App, JWT auth, private, refresh tokens on. Scopes confirmed by the live
token response: **ReadMessages, Faxes, ReadCallLog**. Bound to the extension
owning (813) 626-3312.

### Token TTL

The live response returns **`expires_in` 3600**, not the 7199 the docs imply.
`get_rc_token` reads `expires_in` off the response rather than hardcoding, so this
is already handled.

Had it stayed at the original hardcoded 115 minutes, every token would have been
treated as valid for roughly an hour after it died. That is the Session 34 fix
paying for itself on the first live call.

### Things that cost time

Written up in full as
[Creator and RingCentral gotchas](../fax/SOS_PVS_Fax_System_Design.md), section 11
of the design doc. One worth repeating here because it was purely a communication
failure: several turns were lost because "`poll_fax_status` is blank" meant the
**function body** was a stub, and it was read as the **output** being blank.

### Still to build

- `retry_failed_faxes`
- the 4:00 am digest function
- `PVS_Fax_Review` page
- Faxes Sent and Fax Exceptions reports
- `Partner_PVS_Fax` on `Partner_Billing_Contacts`, still not created
- optional validation workflow rejecting a fax number that is not 10 or 11 digits

---

## Part 3 - Other

### referrals@sosmmc.com

Cloudflare Email Routing cannot serve it: Cloudflare must own the domain's MX and
sosmmc.com points at Google Workspace. The correct answer is a Google Workspace
group with Who Can Post set to External. **Not done.**

### Email for @sosreferrals.com

That domain is **not** on Google, so Cloudflare Email Routing does work there.
Forward-only, free. Destination addresses are added under the Destination
addresses tab, verified, then used in rules. Three employees already carry
sosreferrals.com addresses: Kayla, Catherine, Andrew. **Not done.**

### Repo

Five commits during the Session 34 documentation cycle: `de12b67`, `fc4276d`,
`02d534d`, `3e17253`, `1ffab61`. ccode found five defects in the delivered Deluge;
all five were fixed in source and re-extracted.

---

## Part 4 - Cold thread orientation

### Read in this order

1. This log.
2. `docs/fax/SOS_PVS_Fax_System_Design.md` - the full spec. Section 11 is the
   gotchas list; read it before touching Creator or RingCentral.
3. `docs/sessions/SOS_Code_Session_Log_2026-08-19_Session34_EOD.md` - the design
   session that produced it.

### Where things live

| Artifact | Path |
|---|---|
| Deluge source | `/Users/neilheird/Claude/MPU Reporting/deluge/` |
| 3008 mapping | `/Users/neilheird/Claude/MPU Reporting/3008_july_map.csv` |

Both are mirrored into the repo **except the 3008 row list**, which is
deliberately kept out. Neither source file is version controlled.

### Carried forward

- SendGrid template ID, the Goal for Care ruling, and the SendGrid BAA all still
  block the referral notification function.
- 3008 and Lab Draw notification templates not started.
- `backfill_referral_added_time` still not run.
- Nine service lines have no hospital benchmark.
- Catherine Hardy has no employee initials.
- Data quality: century DOBs, name particle imports, duplicate patients.
