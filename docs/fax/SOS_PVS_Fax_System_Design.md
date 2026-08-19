# SOS PVS Fax System - Design Spec

Designed 2026-08-19 (Session 34). Build started the same day and is roughly half
complete. This document is the spec: it stands on its own and is the file to read
first before touching any of this code.

Platform: Zoho Creator (Deluge) plus the RingCentral Fax API.
Session log: [docs/sessions/SOS_Code_Session_Log_2026-08-19_Session34_EOD.md](../sessions/SOS_Code_Session_Log_2026-08-19_Session34_EOD.md)

---

## 1. The problem

PVS notes must reach the partner by fax within 24 hours. Today it is manual:
complete the PVS in Cognito, generate the note, save to a device, open SRFax,
look up the branch fax number, send. One fax per note.

## 2. The target flow

Complete a PVS, everything downstream updates, the draft invoice is created, the
notification email fires, and the fax goes out through RingCentral with a
dynamically populated cover sheet. RingCentral is set up and the number is
ported.

---

## 3. Logic map, 11 steps

Plain language, in order. This is the contract the code implements.

1. **PVS save.** The provider completes the PVS and saves. Normal downstream
   workflows run.
2. **Draft invoice is created here**, at the initial save, not after the fax.
3. **Gate check.** Fax is offered only when `Visit_Status != Cancelled` AND
   `Clinical_Note_Type` is `Final` or `Addendum`. Anything else stops at step 2.
4. **Redirect to the review page.** The save redirects to `PVS_Fax_Review`, which
   renders the note exactly as it will print, with two actions: Edit and Fax Now.
5. **Provider reviews.** Edit returns to the PVS. A review-stage edit that
   changes complexity, after hours or billing branch causes the draft invoice to
   re-sync. The invoice locks once the fax goes.
6. **Resolve the destination.** The number comes from `Partner_PVS_Fax` on
   `Partner_Billing_Contacts` for the billing branch. No number on file means Fax
   Now is blocked with an alert. The provider may override the number (see
   section 5).
7. **Provider picks attachments.** Which uploaded files ride along is the
   provider's choice, not automatic.
8. **Provider edits Remarks.** A textarea, pre-filled with
   `Clinical notes for [Patient]`, fully editable per fax. The confidentiality
   notice is appended by the template, so it cannot be deleted.
9. **Fax Now.** `send_pvs_fax` stamps the fax ID from `Sequence_Tracker` (FAX
   prefix), inserts the `Fax_Log` record, builds the HTML via
   `build_pvs_fax_html`, renders the PDF through `zoho.file.convertToPDF`,
   attaches the PDF to the log, gets a token from `get_rc_token`, and posts
   multipart to RingCentral. The PVS `Fax_Status` becomes `Queued` or `Failed`.
10. **Poll.** `poll_fax_status` runs on a schedule against every `Queued` record.
    Sent closes the record. A failure records `faxErrorCode` and routes to
    `Retry Pending` or `Permanent Fail`. Anything still `Queued` past 4 hours is
    marked `Stuck`. `retry_failed_faxes` picks up `Retry Pending` (up to 3
    attempts, see section 5).
11. **4:00 am digest.** A fixed 4:00 am Eastern scheduled function emails
    joshua.kolanko@sosmmc.com and neil.heird@sosmmc.com. It covers unfaxed Final
    notes past 24 hours from Added Time, Preliminary notes past 24 hours,
    permanent failures, anything stuck in Queued, and every number override.

---

## 4. New objects

### 4.1 `Partner_Billing_Contacts` - add `Partner_PVS_Fax`

A NEW field. The existing `Partner_Billing_POC_Fax` is deliberately not reused,
because invoices are not faxed and that field is unused. `Partner_PVS_Fax` is the
clinical-note fax destination for the branch.

Status: **not created.**

### 4.2 `Encounter_PatientVisit` - add `Visit_Status` and `Fax_Status`

| Field | Type | Choices |
|---|---|---|
| `Visit_Status` | dropdown | Completed, Attempted (Not Completed), Cancelled |
| `Fax_Status` | dropdown | Not Sent, Queued, Sent, Failed |

`Visit_Status` drives the fax gate: never fax a cancelled visit; Attempted (Not
Completed) DOES fax.

Status as of the 2026-08-19 06:01 schema capture: both fields exist on the form,
but `Fax_Status` carries only Not Sent / Queued / Sent. **`Failed` is missing and
must be added**, otherwise `send_pvs_fax` and `poll_fax_status` cannot write the
failure state. See `schema/Encounter_PatientVisit.md`.

### 4.3 `API_Config` - new form

One record. Six fields. Access locked to Neil and Josh. Only `get_rc_token`
touches it.

| Field | Type |
|---|---|
| `Config_Name` | single line |
| `RC_Client_ID` | single line |
| `RC_Client_Secret` | single line |
| `RC_JWT_Assertion` | multi line |
| `RC_Access_Token` | multi line |
| `RC_Token_Expiry` | date-time |

Status: **DONE, saves clean.** Confirmed in `schema/API_Config.md`. The three
credential values are still empty and are the blocking item (section 8).

### 4.4 `Fax_Log` - new form

Roughly 25 fields. A hidden form: Deluge inserts only, no user entry. It is the
audit record of every transmission, and it holds the rendered PDF as an
attachment so the archive matches exactly what was sent.

It carries, at minimum: the fax ID, the PVS link, destination number, whether the
number was overridden and what the address-book value was, sender identity,
remarks text, attachment selection, the rendered PDF, the RingCentral message ID,
send status, `faxErrorCode`, attempt count, and the timestamps for queued, sent
and failed.

Status: **NOT YET CREATED as specified.** The 2026-08-19 schema capture shows a
`Fax_Log` form with only two fields, `Fax_ID` and `PVS_Link`. This is what
blocked `poll_fax_status` from saving. Creating the full field set, then
re-saving `poll_fax_status`, is the next build step.

### 4.5 `PVS_Fax_Review` - new page

The review screen from step 4. Renders the note exactly as it will print, and
carries Edit, Fax Now, the destination number with its override control, the
attachment picker, and the Remarks textarea.

Status: **not started.**

### 4.6 `Sequence_Tracker` - FAX prefix record

Supplies the fax ID stamped by `send_pvs_fax`.

Status: **DONE.**

---

## 5. Neil's rulings

Every one of these is a decision already made. Do not relitigate them without
Neil.

- **A review step is required before sending.** The PVS saves, then redirects to
  a review page rendering the note exactly as it will print, with Edit and Fax
  Now.
- **The draft invoice is created at the initial save, NOT after the fax.** If a
  review-stage edit changes complexity, after hours or billing branch, the
  invoice re-syncs. It locks once faxed.
- **The fax number lives in a NEW field `Partner_PVS_Fax` on
  `Partner_Billing_Contacts`.** The existing `Partner_Billing_POC_Fax` is unused
  because invoices are not faxed.
- **No fax number on file means Fax Now is blocked with an alert.**
- **Providers CAN override the number.** Reasoning: the address book is a
  convenience, not the authority, and blocking a provider on a stale record costs
  the deadline. Guardrails are an unlock checkbox, re-typing to confirm, the
  override stamped on the log, and every override reported on the daily digest so
  the master record gets corrected.
- **Field providers click Fax Now, not office staff.**
- **Amendments fax as their own transmission** with the cover marked Amendment.
  The path is `Clinical_Note_Type = Addendum`, **NOT** the separate
  `Encounter_Addendum` form.
- **Never fax a cancelled visit. Attempted (Not Completed) DOES fax.**
- **The gate is `Visit_Status != Cancelled` AND `Clinical_Note_Type` is Final or
  Addendum.**
- **Attachments: the provider picks which ones ride along.**
- **The cover sheet is OURS, prepended into the PDF, not RingCentral's.** This
  reversed an earlier call. Reason: Neil may need to print and hand over copies,
  and an archive that does not match what was sent is worthless in an audit.
  RingCentral's cover is set to none via `coverIndex 0`.
- **Remarks is a textarea** pre-filled with `Clinical notes for [Patient]`, fully
  editable per fax, with the confidentiality notice appended by the template so
  it cannot be deleted.
- **The sender is always (813) 626-3312, SOS Mobile Medical Care, Joshua Kolanko
  APRN.**
- **Retry 3 times, but only on codes RingCentral has already given up on, never
  on busy.** RingCentral's carrier already retries a busy line for about 48 hours
  on its own.
- **The daily digest runs at 4:00 am Eastern, fixed, no daylight shift**, to
  joshua.kolanko@sosmmc.com and neil.heird@sosmmc.com. It covers unfaxed Final
  notes past 24 hours from Added Time, Preliminary notes past 24 hours, permanent
  failures, anything stuck in Queued, and every override.
- **The 24-hour clock starts at PVS save (Added Time), not date of service.**
- **Flag Neil accepted:** at 24 hours the SLA is already breached, so that digest
  reports misses rather than preventing them.

---

## 6. KEY TECHNICAL FINDINGS

This is the block a cold thread will otherwise rediscover the hard way. Read it
before writing a line.

- **v24 has NO per-section note fields.** `Final_Clinical_Note` is one rich text
  field. Chief Concern, History/Assessment, Indication, Procedure, Post-Procedure
  Assessment and Plan are headings the provider types inside it. There is nothing
  to iterate over. The template renders that rich text inside a scoped CSS reset
  so stray font tags cannot fight the layout.
- **RingCentral fax uses plain multipart form fields, not a JSON part.** The
  fields are `to`, `faxResolution`, `coverIndex`, `coverPageText`, `attachment`.
  `coverIndex 0` disables their cover page.
- **RingCentral does not report the outcome at send time.** The POST returns
  `Queued`. You poll the message store for `Sent` or `SendingFailed`, and the
  reason arrives as `faxErrorCode`. Any design that expects a synchronous result
  is wrong.
- **Deluge `invokeurl` can only attach files it received as an `invokeurl`
  response.** Creator-stored attachments must be re-fetched first before they can
  ride along on the outbound POST.
- **Form workflows do NOT fire on a Deluge insert.** Anything a form workflow
  normally does (ID stamps, derived fields, downstream triggers) has to be
  repeated inside the function. This is why `send_pvs_fax` stamps the fax ID
  itself.
- **Page count cannot go on the cover** because it is unknown until the PDF
  renders. The running footer carries page x of y instead.
- **Deluge `replaceAll` is regex-based**, so template tokens are `@@NAME@@`.
  Braces break it.
- **HTML escaping is per token, with two deliberate exemptions.** Every text
  token is escaped; the clinical note and the amendment banner are NOT, because
  they ARE html. This was verified by extracting the string literals, re-running
  the substitution in Python and rendering. Test data included
  `K94.23 <Gastrostomy malfunction> & Z43.1`, which printed literally instead of
  eating the page.

---

## 7. The HTML template

One document, assembled as: cover page, page break, note page, page break, then
one page per image attachment.

- Letter size, Helvetica, SOS navy `0B0B5B`.
- The logo is inlined as base64, so nothing depends on WordPress staying up.
- A running footer on every page carries patient, DOB, PVS ID, fax ID and
  page x of y, so a loose sheet is still identifiable.
- The clinical note renders inside a scoped CSS reset.

---

## 8. Deluge functions

Bodies live in `docs/fax/deluge/`. Creator is the source of truth for all four.

| Function | What it does | Status |
|---|---|---|
| `build_pvs_fax_html` | Returns the finished HTML for a PVS. `@@NAME@@` tokens, per-token HTML escaping with the note and amendment banner exempt. | written, in Creator |
| `get_rc_token` | Reads `API_Config`. Returns the cached token if it has more than 5 minutes left, otherwise mints a new one from the JWT bearer grant and stores it with a 115 minute expiry. **Nothing else ever touches a token.** | written, in Creator |
| `send_pvs_fax` | Stamps the fax ID, inserts the `Fax_Log` record, renders the PDF through `zoho.file.convertToPDF`, attaches it to the log, posts multipart to RingCentral, records Queued or Failed. | written, in Creator |
| `poll_fax_status` | Polls every Queued record, closes Sent ones, records `faxErrorCode` on failures, routes to Retry Pending or Permanent Fail, marks anything Queued past 4 hours as Stuck. Returns a one-line summary so Creator's scheduled-workflow history is a usable run trail. | written, **does not save** until `Fax_Log` exists in full |

---

## 9. Still to build

- The `Fax_Log` form in full, then re-save `poll_fax_status`.
- `retry_failed_faxes`.
- The 4am digest function.
- The `PVS_Fax_Review` page.
- Faxes Sent and Fax Exceptions reports.
- Add the `Failed` choice to `Fax_Status`.
- Add `Partner_PVS_Fax` to `Partner_Billing_Contacts`.

## 10. Blocking, on Neil

**RingCentral Client ID, Client Secret and JWT assertion.** Create a REST API App
with JWT auth, scopes Fax + Read Messages + Read Call Log, bound to the extension
that owns (813) 626-3312, graduated to production. Nothing sends until these are
in `API_Config`.
