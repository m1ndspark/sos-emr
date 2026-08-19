# SOS Code - Session Log - 2026-08-19 (Session 34) - EOD

Wednesday 2026-08-19. Three tracks: closed out Session 33's documentation,
designed and began building the PVS fax system on RingCentral, and solved the
July 3008 billing gap.

> **Patient identifiers redacted.** The source log named three patients. This
> repo is PHI-clean by hard rule (CLAUDE.md, SECRETS AND PHI), so names are
> reduced to initials here and the identity key stays with Neil, outside the
> repo. This matches the existing convention in `context/23_task_list.md`.

---

## Part 1 - Session 33 cleanup

- Session 33 log delivered, committed to MPU Reporting, written to the project,
  and the ccode prompt issued. ccode pushed as `1dcf155`.
- `SOS_MPU_Savings_Model_CY2026.md` in MPU Reporting was still the stale Session
  32 single-pathway version. Overwritten with the blended two-pathway model,
  plus the DRG weights and the full discharged and admitted component breakdown.
  The same file was written to the project.
- The repo copy is canonical; the MPU Reporting copy now says so in its header.
  The next ccode run should diff the two.
- The repo pre-commit gate blocks em dashes. All docs use hyphens now.
- The task list owner column uses `cchat`, not "Claude". Confirmed correct.

---

## Part 2 - PVS fax system

Full design spec: [docs/fax/SOS_PVS_Fax_System_Design.md](../fax/SOS_PVS_Fax_System_Design.md)

### The problem

PVS notes must reach the partner by fax within 24 hours. Today it is manual:
complete the PVS in Cognito, generate the note, save to a device, open SRFax,
look up the branch fax number, send. One fax per note.

### The target flow

Complete a PVS, everything downstream updates, the draft invoice is created, the
notification email fires, and the fax goes out through RingCentral with a
dynamically populated cover sheet. RingCentral is set up and the number is
ported.

### Neil's rulings

- A review step is required before sending. The PVS saves, then redirects to a
  review page rendering the note exactly as it will print, with Edit and Fax Now.
- The draft invoice is created at the initial save, NOT after the fax. If a
  review-stage edit changes complexity, after hours or billing branch, the
  invoice re-syncs, and it locks once faxed.
- The fax number lives in a NEW field `Partner_PVS_Fax` on
  `Partner_Billing_Contacts`. The existing `Partner_Billing_POC_Fax` is unused
  because invoices are not faxed.
- No fax number on file means Fax Now is blocked with an alert.
- Providers CAN override the number. Reasoning: the address book is a
  convenience, not the authority, and blocking a provider on a stale record costs
  the deadline. Guardrails are an unlock checkbox, re-typing to confirm, the
  override stamped on the log, and every override reported on the daily digest so
  the master record gets corrected.
- Field providers click Fax Now, not office staff.
- Amendments fax as their own transmission with the cover marked Amendment. The
  path is `Clinical_Note_Type = Addendum`, NOT the separate `Encounter_Addendum`
  form.
- Never fax a cancelled visit. Attempted (Not Completed) DOES fax.
- Gate: `Visit_Status != Cancelled` AND `Clinical_Note_Type` is Final or Addendum.
- Attachments: the provider picks which ones ride along.
- The cover sheet is OURS, prepended into the PDF, not RingCentral's. This
  reversed an earlier call. Reason: Neil may need to print and hand over copies,
  and an archive that does not match what was sent is worthless in an audit.
  RingCentral's cover is set to none via `coverIndex 0`.
- Remarks is a textarea pre-filled with "Clinical notes for [Patient]", fully
  editable per fax, with the confidentiality notice appended by the template so
  it cannot be deleted.
- The sender is always (813) 626-3312, SOS Mobile Medical Care, Joshua Kolanko
  APRN.
- Retry 3 times, but only on codes RingCentral has already given up on, never on
  busy. RingCentral's carrier already retries a busy line for about 48 hours on
  its own.
- The daily digest runs at 4:00 am Eastern, fixed, no daylight shift, to
  joshua.kolanko@sosmmc.com and neil.heird@sosmmc.com. It covers unfaxed Final
  notes past 24 hours from Added Time, Preliminary notes past 24 hours, permanent
  failures, anything stuck in Queued, and every override.
- The 24-hour clock starts at PVS save (Added Time), not date of service.
- Flag Neil accepted: at 24 hours the SLA is already breached, so that digest
  reports misses rather than preventing them.

### New objects

| Object | Change | Status |
|---|---|---|
| `Partner_Billing_Contacts` | add `Partner_PVS_Fax` | not created |
| `Encounter_PatientVisit` | add `Visit_Status` (Completed, Attempted (Not Completed), Cancelled) and `Fax_Status` (Not Sent, Queued, Sent, Failed) | see note below |
| `API_Config` | new, one record, 6 fields, locked to Neil and Josh | DONE, saves clean |
| `Fax_Log` | new, ~25 fields, hidden form, Deluge inserts only | NOT YET CREATED - this is what blocked `poll_fax_status` from saving |
| `PVS_Fax_Review` | new page | not started |
| `Sequence_Tracker` | FAX prefix record | DONE |

Schema-monitor note, added by ccode at sync time: the 06:01 schema capture on
2026-08-19 shows `Visit_Status` and `Fax_Status` already present on
`Encounter_PatientVisit` (`Fax_Status` carries Not Sent / Queued / Sent, with
**Failed missing**), and a `Fax_Log` form existing with only 2 of its ~25 fields
(`Fax_ID`, `PVS_Link`). See `schema/Encounter_PatientVisit.md`,
`schema/Fax_Log.md`, `schema/API_Config.md`.

### Built and delivered

1. **The HTML template.** One document: cover page, page break, note page, page
   break, one page per image attachment. Letter, Helvetica, SOS navy `0B0B5B`,
   logo inlined as base64 so nothing depends on WordPress staying up. A running
   footer on every page carries patient, DOB, PVS ID, fax ID and page x of y, so
   a loose sheet is still identifiable.
2. **`build_pvs_fax_html`** - returns the finished HTML for a PVS. Tokens are
   `@@NAME@@` because Deluge `replaceAll` is regex-based and braces break it.
   Every text token is HTML-escaped; the clinical note and the amendment banner
   are exempt because they ARE html. Verified by extracting the string literals,
   re-running the substitution in Python and rendering. The test data included
   `K94.23 <Gastrostomy malfunction> & Z43.1` and it printed literally instead of
   eating the page.
3. **`get_rc_token`** - reads `API_Config`, returns the cached token if it has
   more than 5 minutes left, otherwise mints a new one from the JWT bearer grant
   and stores it with a 115 minute expiry. Nothing else ever touches a token.
4. **`send_pvs_fax`** - stamps the fax ID, inserts the `Fax_Log` record, renders
   the PDF through `zoho.file.convertToPDF`, attaches it to the log, posts
   multipart to RingCentral, and records Queued or Failed.
5. **`poll_fax_status`** - polls every Queued record, closes Sent ones, records
   `faxErrorCode` on failures, routes to Retry Pending or Permanent Fail, and
   marks anything Queued past 4 hours as Stuck. Returns a one-line summary so
   Creator's scheduled-workflow history is a usable run trail.

### Key technical findings

- v24 has **no per-section note fields**. `Final_Clinical_Note` is one rich text
  field; Chief Concern, History/Assessment, Indication, Procedure,
  Post-Procedure Assessment and Plan are headings the provider types inside it.
  The template renders that rich text inside a scoped CSS reset so stray font
  tags cannot fight the layout.
- RingCentral fax uses plain multipart form fields, not a JSON part: `to`,
  `faxResolution`, `coverIndex`, `coverPageText`, `attachment`. `coverIndex 0`
  disables their cover page.
- RingCentral does not report the outcome at send time. The POST returns Queued;
  you poll the message store for Sent or SendingFailed, and the reason arrives as
  `faxErrorCode`.
- Deluge `invokeurl` can only attach files it received as an `invokeurl`
  response, so Creator-stored attachments must be re-fetched first.
- Form workflows do NOT fire on a Deluge insert, so anything a form workflow
  normally does has to be repeated inside the function.
- Page count cannot go on the cover because it is unknown until the PDF renders.
  The running footer carries page x of y instead.

### Still to build

- `Fax_Log` form, then re-save `poll_fax_status`
- `retry_failed_faxes`
- the 4am digest function
- `PVS_Fax_Review` page
- Faxes Sent and Fax Exceptions reports

### Blocking - on Neil

RingCentral Client ID, Client Secret and JWT assertion. Create a REST API App
with JWT auth, scopes Fax + Read Messages + Read Call Log, bound to the extension
that owns (813) 626-3312, graduated to production.

---

## Part 3 - July 3008 billing

Full write-up: [docs/billing/SOS_3008_July_2026_Billing.md](../billing/SOS_3008_July_2026_Billing.md)

### The problem

Billing runs off PVS records. No PVS records existed for 3008 completions, so
July 3008s could not be invoiced.

### What we found

- The 3008 log is `sos_3008_log_july_2026.xlsx`, uploaded 2026-08-14. 76
  completions, 48 Orlando and 28 Tampa, no duplicate patients, every completion
  date inside July.
- Bill on completion date, not referral date. Neil's ruling.
- The first pass suggested 22 completions had no referral. **Wrong.** All 83
  Cognito 3008 referral IDs imported into Creator. The matcher failed, not the
  import.

| Cause | Count | Detail |
|---|---|---|
| Century DOB bug | 18 | patient R.S. is stored `2043-04-16` |
| Name particle bug | 3 | "De Jesus" became MI "D" and last name "Jesus"; same for "De La Rosa" |
| First name mismatch | 1 | Creator and the log disagree on the first name for the same surname and DOB (patients N-1 / N-2) |
| DOB conflict | 1 | patient C.D.L.R.: `1956-10-30` in Creator against `1958-06-06` in the log. One of the two is wrong. |

### Built

`create_3008_pvs_july(pMode)` creates the 76 PVS records. Referral IDs were
resolved in Python and hardcoded into the function, so Deluge does zero name
matching. Each row is referral ID, completion date and provider last name. It
skips any row that already has a 3008 PVS, has no active employee for that last
name, or has no current "Cares 3008 Assessment" rate on the branch. It stamps the
PVS ID from `Sequence_Tracker` because form workflows do not fire on Deluge
inserts. It sets Invoice Status Draft and Hold From Invoicing No, so all 76 land
in the next invoice run. It takes `DRYRUN` or `COMMIT`.

**NOT YET RUN.** Neil owes a DRYRUN output before COMMIT.

### How 3008s bill, for the record

A 3008 is a PVS with `Type_of_Entry = 3008` and `Complexity_Level = "Cares 3008
Assessment"`. That matches the same `Rate_Type` in `Partner_Rates` for the
billing branch, fills `Complexity_Charge`, and flows to the draft invoice exactly
like any other visit. The only thing that breaks it is a branch with no 3008 rate
on file, and `diag_partner_rates` already reports that gap per location.

---

## Part 4 - referrals@sosmmc.com

Neil wanted a Cloudflare Email Worker to fan referrals@sosmmc.com out to both him
and Josh. Dead end: Cloudflare Email Routing requires Cloudflare to own the
domain's MX records, and sosmmc.com points at Google Workspace. The native answer
is a Google Workspace group with both as members, with Who Can Post set to
External so partner mail does not bounce. The worker should be deleted. Neil
paused this.

---

## Part 5 - cold thread orientation

### Read in this order

1. This log.
2. `docs/mpu/SOS_MPU_Savings_Model_CY2026.md` - the blended model.
3. `docs/mpu/SOS_MPU_Annual_Data_Refresh_Checklist.md` - the eight data sources
   and their traps.
4. `SOS_MPU_Reporting_Decisions_Log.md` - every ruling. (Lives in MPU Reporting,
   not yet mirrored into this repo.)

For the fax work specifically, read `docs/fax/SOS_PVS_Fax_System_Design.md`
first. It is self-contained.

### Where the fax work lives

All artifacts were produced in the session container under `/root/mpu/fax` and
delivered to Neil as files. **The container is ephemeral.** The functions and the
template are pasted into Creator; that is the durable copy.

UPDATE 2026-08-19, after this log was first written: the real bodies were
recovered from the container and committed. All four fax functions are verbatim
in `docs/fax/deluge/`. `create_3008_pvs_july` is in `docs/billing/` with its 76
data rows redacted and all logic intact. Because these came from the container
rather than a Creator export, they should still be re-extracted and diffed once a
fresh `.ds` export exists.

### Carried forward, unchanged

- The SendGrid template ID, the Goal for Care ruling, and the SendGrid BAA
  confirmation still block the referral notification function.
- 3008 and Lab Draw notification templates not started.
- `backfill_referral_added_time` still not run.
- Nine service lines have no hospital benchmark; 64 of Empath's 118 July visits
  sit outside the savings model.
- Data quality: century DOBs, name particle imports, duplicate patients, the
  byte-identical note on PVS-1112-JK. **The century and particle bugs both
  surfaced again today, which is the second time they have cost real time.**
