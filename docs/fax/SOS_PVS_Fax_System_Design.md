# SOS PVS Fax System - Design Spec

Designed 2026-08-19 (Session 34), built through Session 35 the same day, and
finished and proven live 2026-09-22 (Session 50). Sections 1 to 12 are the
original spec, annotated where Session 50 changed or corrected them. **Section 13
is the design as actually built and wins over the spec wherever they differ.**

**State as of 2026-09-22: LIVE.** Eight real faxes sent (FAX-092226-1001 to
1008), seven delivered and confirmed by RingCentral, one failed on a RingCentral
503. The full loop works: Fax PVS button, review modal, send, self re-arming
poll, retry sweep, 4:00 am digest, Fax Log report. Section 11 is the gotchas
list; section 14 is the Session 50 Creator and Deluge findings.

> **Repo drift, read before trusting any function body here.** The bodies in
> `docs/fax/deluge/` and the repo `.ds` (v51, exported 2026-09-22 06:35) both
> PREDATE every Session 50 change: five functions changed, three created,
> diagnostics added, three `PVS_Fax_Review` workflows, three schedules, one
> report, two new form fields. Creator is the source of truth. The next fresh
> `.ds` export resyncs them; until then treat every body in this repo as stale.

Platform: Zoho Creator (Deluge) plus the RingCentral Fax API.
Session logs:
[Session 34](../sessions/SOS_Code_Session_Log_2026-08-19_Session34_EOD.md) (design),
[Session 35](../sessions/SOS_Code_Session_Log_2026-08-19_Session35_EOD.md) (build),
[Session 50](../../context/handoff/SOS_Code_Session_Log_2026-09-22_Session50_EOD.md) (finished, live).

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

Plain language, in order. This was the contract as designed.

> **Superseded in part by Session 50, see section 13.** Steps 4, 5 and 7 did not
> ship as written: there is no redirect on save, no review page on every fax, and
> no attachments. Steps 9 to 11 shipped substantially as written.

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
   multipart to RingCentral. The `Fax_Log` row is inserted as `Building`, then
   moves to `Queued` or `Failed`. The PVS `Fax_Status` becomes `Queued` or
   `Failed`. See section 4.2 on the two different `Fax_Status` fields.
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

Status: **created.** Populated on 19 of 23 rows as of 2026-09-22. Blank on all
four InnoVage rows, and InnoVage has duplicate Orlando and Tampa rows (open).

### 4.2 `Encounter_PatientVisit` - add `Visit_Status` and `Fax_Status`

| Field | Type | Choices |
|---|---|---|
| `Visit_Status` | dropdown | Completed, Attempted (Not Completed), Cancelled |
| `Fax_Status` | dropdown | Not Sent, Queued, Sent, Failed |

`Visit_Status` drives the fax gate: never fax a cancelled visit; Attempted (Not
Completed) DOES fax.

Status: **DONE (Session 35).** Both fields exist and Neil added the `Failed`
choice, so the field now carries all four values.

> Caveat on the mirror, not on the work: `schema/Encounter_PatientVisit.md` was
> captured at 06:01 on 2026-08-19, **before** that change, so it still shows only
> Not Sent / Queued / Sent. The next 06:00 schema-monitor run will catch up. Do
> not read the stale capture as the field being wrong.

> ### There are TWO `Fax_Status` fields and they are NOT the same
>
> This is the single easiest thing to get wrong in this system.
>
> | | `Encounter_PatientVisit.Fax_Status` | `Fax_Log.Fax_Status` |
> |---|---|---|
> | Purpose | the visit's headline state, for reports and the digest | the transmission's full lifecycle, for the audit trail |
> | Choices | Not Sent, Queued, Sent, Failed | Building, Queued, Sent, Failed, Retry Pending, Stuck, Permanent Fail |
> | Count | 4 | 7 |
>
> Written by:
>
> | Function | Writes to PVS | Writes to Fax_Log |
> |---|---|---|
> | `send_pvs_fax` | Queued, Failed | **Building**, Queued, Failed |
> | `poll_fax_status` | Sent, Failed | Sent, **Retry Pending**, **Stuck**, **Permanent Fail** |
>
> A PVS never carries Building, Retry Pending, Stuck or Permanent Fail. Those
> four are lifecycle states of one transmission, and only the log holds them.
>
> The three-option capture in `schema/Encounter_PatientVisit.md` is reading the
> **PVS** field, and it predates Neil adding `Failed`. It says nothing about the
> `Fax_Log` field, which is a separate field on a separate form. That field now
> carries all seven choices (closed Session 50, see section 12).

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

Status: **DONE and loaded (Session 35).** Confirmed in `schema/API_Config.md`. The
client ID, secret and JWT assertion are populated and authenticating. See section
10.

### 4.4 `Fax_Log` - new form

Roughly 25 fields. A hidden form: Deluge inserts only, no user entry. It is the
audit record of every transmission, and it holds the rendered PDF as an
attachment so the archive matches exactly what was sent.

These are the 22 fields the two functions actually reference. This list is
derived from the delivered bodies in `docs/fax/deluge/`, so it is the minimum
that must exist for either function to save.

| Field | Type | Written by |
|---|---|---|
| `Fax_ID` | single line | send |
| `PVS_Link` | lookup to Encounter_PatientVisit | send |
| `Referral_Link` | lookup to Referrals_Main | send |
| `Partner_Location_Link` | lookup to Partner_Locations | send |
| `Destination_Fax` | single line (E.164) | send |
| `Destination_Name` | single line | send |
| `Number_Source` | single line or dropdown | send |
| `Override_Reason` | multi line | send |
| `Cover_Remarks` | multi line | send |
| `Fax_Status` | dropdown, **7 options** (below) | send and poll |
| `Attempt_Number` | number | send writes, poll reads |
| `Original_Fax_Link` | lookup to Fax_Log (self) | send |
| `Sent_By` | single line or user field | send |
| `Submitted_Time` | date-time | send writes, poll reads |
| `Fax_PDF` | file upload | send |
| `RC_Message_ID` | single line | send writes, poll reads |
| `RC_Conversation_ID` | single line | send |
| `Last_Polled_Time` | date-time | send and poll |
| `Completed_Time` | date-time | send and poll |
| `Fax_Error_Code` | single line | poll |
| `Fax_Error_Reason` | single line, 250 chars | send and poll |
| `Page_Count` | number | poll |

**`Fax_Log.Fax_Status` takes seven options**, and is not the same field as
`Encounter_PatientVisit.Fax_Status`:

```
Building | Queued | Sent | Failed | Retry Pending | Stuck | Permanent Fail
```

`send_pvs_fax` inserts the row as `Building`, then moves it to `Queued` or
`Failed`. `poll_fax_status` moves it to `Sent`, `Retry Pending`, `Stuck` or
`Permanent Fail`. Miss any one option and the corresponding write silently fails.

Status: **BUILT and live. The three gaps below are CLOSED (Session 50):** the
form now carries `Partner_Location_Link`, `Sent_By` and the seven-value
`Fax_Status`. The rest of this status note is kept as the Session 35 record.

Session 35 status: **BUILT, with three gaps.** `schema/Fax_Log.md`, captured
15:05 on 2026-08-19, shows 24 fields. `poll_fax_status` now saves. Two extra
fields exist that the code does not use, `Attachments_Included` and
`Fax_Log_ID_Stamp`, which is fine.

Three things do not line up with the delivered code, and none is caught by the
function compiling:

| Code expects | Live form has |
|---|---|
| `Partner_Location_Link` | `Partner_Locations` |
| `Sent_By` | `Employees` |
| `Fax_Status` with 7 choices | `Fax_Status` with 4 |

**See section 12.** These blocked the first real send until Session 50.

Two write rules added in Session 50: `Original_Fax_Link` (self-lookup) and
`Sent_By` (Employees lookup) are set only AFTER the insert and only when they
resolve. Passing 0 to the self-lookup kills the insert, and `Sent_By` was being
handed a login email.

### 4.5 `PVS_Fax_Review` - new page

The review screen from step 4. Renders the note exactly as it will print, and
carries Edit, Fax Now, the destination number with its override control, the
attachment picker, and the Remarks textarea.

Status: **BUILT, but not as specified (Session 50).** It is a stateless form
opened as an exception-path MODAL, not a review page shown on every fax, and has
no attachment picker. See section 13.

### 4.6 `Sequence_Tracker` - FAX prefix record

Supplies the fax ID stamped by `send_pvs_fax`.

Status: **DONE.**

---

## 5. Neil's rulings

Every one of these is a decision already made. Do not relitigate them without
Neil.

> **Session 50 changed four of these, marked SUPERSEDED below.** Section 13 has
> the replacements.

- ~~**A review step is required before sending.**~~ **SUPERSEDED Session 50.**
  The PVS saves, then redirects to a review page rendering the note exactly as it
  will print, with Edit and Fax Now. Replaced by a Fax PVS button that sends
  immediately; the review form is an exception-path modal only.
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
- ~~**Attachments: the provider picks which ones ride along.**~~ **SUPERSEDED
  Session 50.** No attachments at all. One fax equals our cover plus the note.
- **The cover sheet is OURS, prepended into the PDF, not RingCentral's.** This
  reversed an earlier call. Reason: Neil may need to print and hand over copies,
  and an archive that does not match what was sent is worthless in an audit.
  RingCentral's cover is set to none via `coverIndex 0`.
- **Remarks is a textarea** pre-filled with `Clinical notes for [Patient]`, fully
  editable per fax (as built: the modal's Cover Remarks rich text field, prefilled
  with "Clinical note(s) for:" plus patient name and MRN), with the confidentiality notice appended by the template so
  it cannot be deleted.
- ~~**The sender is always (813) 626-3312, SOS Mobile Medical Care, Joshua
  Kolanko APRN.**~~ **SUPERSEDED Session 50.** The cover FROM block is company
  only, no provider name. See section 13.
- **Retry 3 times, but only on codes RingCentral has already given up on, never
  on busy.** RingCentral's carrier already retries a busy line for about 48 hours
  on its own.
- **The daily digest runs at 4:00 am Eastern, fixed, no daylight shift**
  (DEVIATION, open: as built it fires in the app timezone and so does shift with
  daylight saving), to
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
- **Two-argument Deluge `replaceAll` is regex-based**, so template tokens are
  `@@NAME@@`. Braces break it. **The three-argument form
  `replaceAll(a, b, true)` is LITERAL, not regex** (confirmed again Session 50,
  see section 14), so every regex strip must use the two-argument form.
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
  page x of y, so a loose sheet is still identifiable. **MISSING as of Session
  50:** the footer is set through the `convertToPDF` options argument, which was
  dropped to get a send working. See section 14, item 7.
- As built there are no attachment pages: cover, page break, note.
- The clinical note renders inside a scoped CSS reset.

---

## 8. Deluge functions

Real bodies live in `docs/fax/deluge/`, committed 2026-08-19 and re-extracted
the same day after the five fixes in 8.1. They came from the session container,
not from a Creator export, so treat them as the as-delivered copy. Creator
remains the source of truth; re-extract and diff once a fresh `.ds` export
exists.

| Function | What it does | Status |
|---|---|---|
| `build_pvs_fax_html` | Returns the finished HTML for a PVS. `@@NAME@@` tokens, per-token HTML escaping with the note and amendment banner exempt. | written, in Creator |
| `get_rc_token` | Reads `API_Config`. Returns the cached token if it has more than 5 minutes left, otherwise mints a new one from the JWT bearer grant and stores it with an expiry derived from the response's `expires_in` (3600 second fallback). **Nothing else ever touches a token.** | written, in Creator |
| `send_pvs_fax` | Stamps the fax ID, inserts the `Fax_Log` record as `Building`, renders the PDF through `zoho.file.convertToPDF`, attaches it to the log, posts multipart to RingCentral, records Queued or Failed on both the log and the PVS. | written, in Creator |
| `poll_fax_status` | Polls every Queued record, closes Sent ones, records `faxErrorCode` on failures, routes to Retry Pending or Permanent Fail, marks anything Queued past 4 hours as Stuck. Permanent Fail is taken either from a no-retry error code or from `Attempt_Number >= 3`. Returns a one-line summary so Creator's scheduled-workflow history is a usable run trail. | written, in Creator |

Session 50 status: all four above were changed live and the repo bodies are
stale (see the drift note at the top). New in Session 50, bodies in Creator
only: `retry_failed_faxes`, `send_fax_digest`, `send_referral_confirmation`, and
the diagnostics `diag_pvs_fax_number`, `diag_fax_error`, `diag_rc_token`,
`diag_fax_pdf_image`, `diag_collection_shape`. See section 13.

---

### 8.1 Five defects found and fixed

Found by ccode 2026-08-19 when the real bodies were first committed (`fc4276d`),
except defect 5 which Neil caught. **All five were fixed in the repo source and
the corrected bodies re-extracted here** as of `fc4276d`'s follow-up commit.

> **CORRECTION 2026-09-22 (Session 50): defect 3 was fixed in the repo, NOT in
> the app.** The live `get_rc_token` was still the old version, hardcoded 115
> minute cache and no margin, until it was fixed live on 2026-09-22. The repo
> said fixed while the app did not. The lesson: a fix in `docs/fax/deluge/` is
> not live until Neil pastes it into Creator and a fresh `.ds` confirms it. The
> other four were not re-verified against live either.

| # | Function | Defect | Status |
|---|---|---|---|
| 1 | `create_3008_pvs_july` | `PVS_ID` sequence off by one, would duplicate a billing record locator | FIXED |
| 2 | `send_pvs_fax`, `build_pvs_fax_html` | `&mdash;` rendered an em dash on every faxed page | FIXED |
| 3 | `get_rc_token` | no safety margin on the cached token | FIXED in repo 2026-08-19, **live only 2026-09-22** |
| 4 | `poll_fax_status` | busy and no-answer routed to retry, against the ruling | FIXED, one caveat |
| 5 | `send_pvs_fax` | `FAX` sequence off by one, same shape as defect 1 | FIXED |

**1. `create_3008_pvs_july` minted `PVS_ID` off by one.** It read N, issued
`PVS-(N+1)` and stored N+1, leaving the tracker at the last-used value instead of
the next-free one. The next PVS created through the form would then have
duplicated the backfill's last `PVS_ID`. Two visits, one billing record locator.
DRYRUN could not catch it because the mint sits inside the COMMIT branch. Now
reads N, issues `PVS-N`, stores N+1, `break`. Full write-up in
`docs/billing/SOS_3008_July_2026_Billing.md` section 7.

**2. Em dashes on every faxed page.** `send_pvs_fax`'s running footer carried
`Confidential &mdash; Protected Health Information`, and `build_pvs_fax_html`'s
amendment banner carried `AMENDED NOTE &mdash; SUPERSEDES...`. Both are now
hyphens. The entity form is why no literal-character grep and no pre-commit hook
caught them.

The token-escaping line was tightened at the same time. It used to restore a
double-escaped entity back to an em dash:

```
v_val = v_val.replaceAll("&amp;mdash;","&mdash;",true);   // was
v_val = v_val.replaceAll("&amp;mdash;","-",true);         // now
```

So an em dash arriving in source data is now converted to a hyphen rather than
reinstated. The `&nbsp;` repair on the line above is unchanged and still correct.

**3. `get_rc_token` had no safety margin, and hardcoded the TTL.** It read
`RC_Token_Expiry > zoho.currenttime`, so it would hand back a token with one
second left and the fax POST would fail on an expired bearer. It also stored a
fixed 115 minute expiry, which was only correct if the app happened to issue a
7200-second token.

Both were fixed in the repo copy on 2026-08-19, but that copy never reached
Creator; see the correction above. The live fix landed 2026-09-22. The read now
carries a real margin:

```
if(v_cfg.RC_Token_Expiry > zoho.currenttime.addMinutes(5))
```

and the write derives the window from the response instead of assuming it:

```
v_ttl = 3600;
if(v_resp.get("expires_in") != null)
{
    v_ttl = v_resp.get("expires_in").toLong();
}
v_mins = v_ttl / 60;
v_cfg.RC_Token_Expiry = zoho.currenttime.addMinutes(v_mins);
```

`expires_in` is read off the token response with a 3600-second fallback, so the
cache window is correct whatever the app issues. As of 2026-09-22 this is live.

Live symptom of the unfixed version: RingCentral issues 3600-second tokens, so
the 115 minute cache served a dead token for about 55 minutes of every cycle,
surfacing as `TokenInvalid` / OAU-213 "Token not found" on a send. Expiry math
also cannot catch a revoked token, so `send_pvs_fax` now clears the cache and
retries once on `TokenInvalid`. That in-send retry is separate from
`retry_failed_faxes` and does not consume an attempt.

**4. `poll_fax_status` retried busy lines, against the ruling.** The ruling is
"retry 3 times, but only on codes RingCentral has already given up on, never on
busy." The no-retry list contained no busy or no-answer code, so both routed to
`Retry Pending`. `LineBusy` and `NoAnswer` now lead the list:

```
LineBusy | NoAnswer | NoFaxMachine | WrongNumber
NotAcceptingFax | InvalidNumber | NumberBlocked | InternationalDisabled
```

> **Caveat, and it is the only one left open here.** These enum strings have not
> been confirmed against a real RingCentral failure. They are a best read of
> RingCentral's documentation, not verified behavior. The first genuine send
> failure is the moment to check the actual `faxErrorCode` string against this
> list. A mismatch is not loud: an unrecognized code silently falls through to
> `Retry Pending`, which for a busy line is exactly the behavior the ruling
> forbids. `Fax_Error_Reason` stores the raw response, so the real string will be
> on the log record when it happens.
>
> Still open after Session 50: the only live failure (FAX-092226-1004) was a
> RingCentral 503 on the POST, not a `faxErrorCode` from the message store, so the
> enum list remains unverified.

**5. `send_pvs_fax` minted the `FAX` sequence off by one.** Same shape as defect
1: read N, issue N+1, store N+1, no `break`. Caught by Neil, not by the original
audit, which noted the convention mismatch but wrongly judged it self-consistent
and therefore harmless. It was not: every fax ID would have been one ahead of the
tracker, and the tracker left one short. Now reads N, issues `FAX-N`, stores N+1,
`break`, matching `OnSuccess__PVS_Stamp_Generator` and `backfill_pvs_ids`.

**All four minters in the repo now share one convention:**
`Sequence_Tracker.Object_Sequence` is the **next free** number. Read it, issue it,
store it plus one, `break`. Any new minter must follow it.

### 8.2 Two residuals, neither worth blocking on

- **A literal em dash character in source data still passes through.** The
  escaping chain catches the `&mdash;` entity but not U+2014 typed directly into,
  say, the Remarks textarea. Low likelihood, and it is provider-entered text
  rather than SOS-authored content, but the faxed page is still SOS output.
- **`send_pvs_fax` has no guard for a missing `FAX` row in `Sequence_Tracker`.**
  If the row were absent, `v_seqVal` stays 0 and the fax silently gets
  `FAX-MMDDYY-0000`. The row exists, so this is theoretical.
  `functions/backfill_pvs_ids.dg` shows the pattern if a guard is ever wanted: it
  tracks a `v_found` flag and skips the record rather than minting a bad ID.

---

## 9. Still to build

Updated 2026-09-22 (Session 50). Built since the original list:
`retry_failed_faxes`, the digest (`send_fax_digest`), `PVS_Fax_Review` (as a
modal), the Fax Log report, `Partner_PVS_Fax`, and the three section 12 gaps.

Still open:

- `convertToPDF` options argument, to restore the running footer (section 14).
- The Fax Exceptions saved filter view on the Fax Log report.
- Re-fax reason capture. The warn-and-allow ruling has nowhere to store a
  reason: no `Resend_Reason` field, and On Validate does not block or warn on an
  already-Sent PVS.
- `Partner_PVS_Fax` on the four InnoVage rows, and the duplicate InnoVage
  Orlando and Tampa rows.
- Digest timezone, which shifts with daylight saving (section 5).
- Phase 2: the 3008 fax route and imaging order faxing to vendors. Both are
  blocked in v1 with a gate message.
- Optional: a validation workflow rejecting a fax number that is not 10 or 11
  digits.

---

## 10. RingCentral - AUTH IS LIVE

Closed 2026-08-19 (Session 35). This section previously read "Blocking, on Neil".

| Setting | Value |
|---|---|
| App type | REST API App, **private** |
| Auth | **JWT**, refresh tokens on |
| Scopes | `ReadMessages`, `Faxes`, `ReadCallLog` (confirmed by the live token response, not by the console) |
| Bound to | the extension owning (813) 626-3312 |
| Credentials | client ID, secret and JWT assertion loaded into `API_Config` |

`poll_fax_status` returns `polled 0, sent 0, retry pending 0, permanent fail 0,
stuck 0`. **The whole chain compiles, authenticates and runs.**

**Token TTL, settled.** The live response returns `expires_in` **3600**, not the
7199 RingCentral's documentation implies. The repo's `get_rc_token` read
`expires_in` off the response, but **the live function did not until 2026-09-22**
(see the 8.1 correction). The hardcoded 115 minute expiry did survive in Creator,
and it failed exactly as predicted: dead tokens served for roughly an hour after
they died, showing up as `TokenInvalid` on a send. This paragraph previously
claimed the Session 34 fix paid for itself on the first live call; it had not
reached the app.

First real fax: 2026-09-22 (Session 50), FAX-092226-1001.

---

## 11. Creator and RingCentral gotchas

Every one of these cost real time in Session 35. A cold thread will hit all of
them. Read this before touching Creator or the RingCentral console.

### Creator

**Execute prints info output only, never return values.** Creator's function
Execute view shows whatever `info` statements write. It does **not** show the
value a function returns. "Executed successfully" with a blank pane is a **PASS**,
not a silent failure. If you want to see a return value, `info` it.

**`insert into` returns the record ID as a NUMBER, not a record.** So `v_new.ID`
is a field access on a number and throws `Invalid collection object found`. Use
the variable directly as the ID, or set the field inside the insert. This is what
broke `create_3008_pvs_july` on its COMMIT run; see
`docs/billing/SOS_3008_July_2026_Billing.md` section 8.

**Creator auto-names a lookup field after the SOURCE FORM.** Add a lookup to
`Partner_Locations` and the field arrives named `Partner_Locations`, not whatever
you intended to call it. Renaming the **display** name does not rename the **link**
name, and Deluge references the link name. Rename the link name explicitly, and
confirm it in `schema/<Form>.md` afterwards. This bit `Fax_Log` twice; see section
12 (closed Session 50).

**A self-lookup works, but the form must be saved first.** You cannot add a lookup
pointing at the form you are currently creating. Save the form, reopen it, then add
the field. `Fax_Log.Original_Fax_Link` is a self-lookup and was built this way.

**"Blank" is ambiguous, and it cost several turns.** "`poll_fax_status` is blank"
meant the **function body** was a stub. It was read as the **output** being blank.
When reporting, say which.

### RingCentral

**The Redirect URI field only appears for the Authorization Code flow.** Selecting
JWT removes it from the app form. Its absence is correct and is not a
misconfiguration to hunt for.

**The JWT credential is created on a separate Console screen**, under the account
menu, not on the app itself. You create the app, then go elsewhere to mint the JWT,
then bring it back.

**`expires_in` is 3600, not the 7199 the docs imply.** Never hardcode a token
lifetime from documentation. Read `expires_in` off the token response, which is
what `get_rc_token` does. A hardcoded window that is too long serves dead tokens
and fails intermittently, which is the worst failure shape to debug.

**Scopes are confirmed by the token response, not the console.** The live response
reported `ReadMessages`, `Faxes`, `ReadCallLog`. Trust that over what the app
screen displays.

---

## 12. Live-form gaps found at sync time

**ALL CLOSED (Session 50, 2026-09-22).** `Fax_Log` now carries the seven-value
`Fax_Status` choice set, `Partner_Location_Link` and `Sent_By`, and fax sends
write to all three. The rest of this section is kept as the 2026-08-19 record.

Found by ccode 2026-08-19 by diffing the delivered Deluge against
`schema/Fax_Log.md`, captured 15:05 that day, **after** the form was built. These
are current, and none of them is caught by "the function compiles".

**1. `Fax_Log.Fax_Status` has 4 choices. The code needs 7.**

| | |
|---|---|
| Live form | `Not Sent`, `Queued`, `Sent`, `Failed` |
| Code writes | `Building`, `Queued`, `Sent`, `Failed`, `Retry Pending`, `Stuck`, `Permanent Fail` |
| Missing | **`Building`, `Retry Pending`, `Stuck`, `Permanent Fail`** |

`send_pvs_fax` inserts every row as `Building`, so **the first real send writes a
choice the field does not have.** `poll_fax_status` cannot route a failure to
`Retry Pending` or `Permanent Fail`, and cannot mark anything `Stuck`. `Not Sent`
is on the form but neither function ever writes it to the log; that value belongs
on the PVS field, not here. See section 4.4.

**2. `Fax_Log.Partner_Location_Link` does not exist. The live field is
`Partner_Locations`.** Exactly the lookup auto-naming gotcha from section 11,
unfixed. `send_pvs_fax` writes `Partner_Location_Link = v_pvs.Billing_Branch`.

**3. `Fax_Log.Sent_By` does not exist. The live field is `Employees`.** Same
gotcha, and note the type differs too: the code writes `zoho.loginuserid` into what
is now a lookup.

**Either the form is renamed to match the code, or the code is changed to match the
form.** Renaming the two link names is the smaller change and keeps the delivered
bodies correct.

> **VERIFY LIVE, and it matters.** Gaps 2 and 3 raise a question this repo cannot
> answer: `send_pvs_fax` is reported as saving and compiling in Creator, yet it
> writes two field names the live form does not have. Either it was edited in
> Creator to match the real names, in which case **the repo copy is stale** and
> needs re-extracting, or Creator did not validate those names at save time and the
> failure is waiting for the first send. Open `send_pvs_fax` in Creator and check
> which. The `Fax_Status` gap is real either way, because a bad choice value is a
> string write that compiles fine and fails at runtime.

---

## 13. As built, Session 50 (2026-09-22)

This is the design as it runs live. Where it differs from sections 3 to 5, this
section wins. Source: the
[Session 50 log](../../context/handoff/SOS_Code_Session_Log_2026-09-22_Session50_EOD.md).
Function bodies are NOT reproduced here; the repo copies are stale until the next
`.ds` export.

### 13.1 Where the design departs from the spec

| Spec (sections 3 to 5) | As built |
|---|---|
| PVS save redirects to a review page | **No redirect on save, deliberately.** `openUrl` is terminal and would kill any On Success jobs not yet run, including the draft invoice. NEIL RULING 2026-09-22: "so lets not create a new problem." |
| Review step on every fax | **No review step.** A Fax PVS Button column on each `PVS_Report` row sends immediately. |
| `PVS_Fax_Review` is the review page | `PVS_Fax_Review` is a stateless form opened as a **modal**, on the exception path only: no number on file, or duplicate contacts. It takes a one-off number with a reason. |
| Provider picks attachments | **No attachments.** One fax equals one document: our cover sheet plus the note. Imaging reports are inbound and separate. |
| Destination from `Partner_PVS_Fax` | Same, and `Partner_PVS_Fax` is the only authority. `Fax_Address_Book` plays no part. |
| Sender line names the provider | Cover FROM block is company only (13.4). |
| Digest fixed at 4:00 am Eastern | Fires daily at 04:00 in the app timezone, so it shifts with daylight saving (open). |

v1 scope is Patient Visit only. 3008 and Imaging Order reach the modal and get a
gate message; both are Phase 2.

Override does NOT unlock the rest of the record. The form is stateless, so edits
there would change what is faxed while the PVS still said something else.

### 13.2 Functions

| Function | Session 50 change |
|---|---|
| `send_pvs_fax` | two-argument regex strip, lookup guards (4.4), `convertToPDF` options dropped, clear-cache-and-retry-once on `TokenInvalid`, try/catch on both POSTs, guarded truncation |
| `get_rc_token` | `expires_in` plus five minute margin, live for the first time (8.1) |
| `poll_fax_status` | try/catch, guarded truncation, error count |
| `retry_failed_faxes` | NEW. Picks up Retry Pending rows, three attempt cap, spawns a new fax linked to the original through `Original_Fax_Link`, retires the old row to Failed |
| `send_fax_digest` | NEW. Five sections, ZeptoMail. Floor hardcoded at 22-Sep-2026 so pre-fax history is excluded |
| `build_pvs_fax_html` | cover FROM block rewritten |
| `send_referral_confirmation` | NEW, not fax. Partner-facing referral confirmation to `Partner_POC_Email` only, wrapping `build_referral_confirmation_html` |
| `process_new_referral` | calls `send_referral_confirmation` in the success branch only |
| `diag_pvs_fax_number`, `diag_fax_error`, `diag_rc_token`, `diag_fax_pdf_image`, `diag_collection_shape` | NEW, diagnostic, read only |

### 13.3 Workflows, schedules, report, form changes

`PVS_Fax_Review` is a stateless form, so the only events available are Field
rules, On Load, On User Input and Click of a button.

| Workflow | Event |
|---|---|
| PVS Fax Review On Load | On Load (the three-argument `replaceAll` defect was here too) |
| PVS Fax Review Override Unlock | On User Input of `Override_Unlock` |
| PVS Fax Review Fax Now | Click of a button: gate checks, calls `send_pvs_fax`, alerts, closes the modal |

| Schedule | Trigger |
|---|---|
| Fax Poll Re-arm | `Fax_Log`, `Last_Polled_Time` + 3 minutes, condition Fax Status is Queued |
| Fax Retry Sweep | `Fax_Log`, `Last_Polled_Time` + 15 minutes, condition Fax Status is Retry Pending |
| Fax Digest Daily 4am | daily at 04:00 |

The poll is a self re-arming schedule on `Last_Polled_Time`, not a cron.
FAX-092226-1008 resolved to Sent through the schedule with no manual poll, which
proved the re-arm works.

Report: Fax Log, sorted by Submitted Time descending. The Fax Exceptions saved
view does not exist yet.

Form changes: `PVS_Fax_Review` gained `Patient_Name` and `Referral_ID`, both
prefilled and disabled; `PVS_Link` and `Patient_Display` hidden; `Note_Preview`
relabeled Cover Remarks and made editable rich text that feeds the cover;
`Cover_Remarks` hidden. `PVS_Report` gained a Button column labeled Fax PVS.

### 13.4 Cover sheet and alerts

Cover FROM block:

```
SOS Mobile Medical Care
8270 Woodland Center Blvd, Tampa, FL 33614
Phone (813) 513-1925    Fax (813) 626-3312
```

No provider name. The (561) 560-8302 x101 extension is gone from both the FROM
block and the confidentiality notice.

Alert wording:

```
SUCCESS: [patient] ([REF ID]) Faxing to [destination] at [number]. Fax ID [FAX-...].
FAILURE: FAX NOT SENT. Fax ID [FAX-...]. Check the fax log for details.
```

### 13.5 Live results

| Fax | Result |
|---|---|
| FAX-092226-1001 | Sent, 3 pages |
| FAX-092226-1002 | Sent, 3 pages |
| FAX-092226-1003 | Sent, 3 pages (to 813-626-3312; all others to the test line) |
| FAX-092226-1004 | Failed, RingCentral 503 Service Temporary Unavailable |
| FAX-092226-1005 | Sent, 4 pages |
| FAX-092226-1006 | Sent, 4 pages |
| FAX-092226-1007 | Sent, 4 pages |
| FAX-092226-1008 | Sent, 3 pages, resolved by the schedule |

Digest after the floor was added: missed 0, prelim 0, failures 0, overrides 8.

---

## 14. Creator and Deluge findings, Session 50

Each of these is also recorded in `context/05_deluge_learnings.md`.

1. **Three-argument `replaceAll` does NOT apply a regex.** The third argument
   switches to literal matching. `v_raw.replaceAll("[^0-9]","",true)` returned
   `"+19418062117"`; `v_raw.replaceAll("[^0-9]","")` returned `"19418062117"`.
   It was in `send_pvs_fax` and the PVS Fax Review On Load, so every fax would
   have posted a malformed E.164 like `++19418062117`, and the modal flagged a
   valid number as not 10 digits. Only those two places used the broken form; the
   other seven three-argument calls in the app replace literal strings and are
   correct. This was already recorded in `context/05` on 2026-07-23 and recurred
   anyway.
2. **`alert` is not available in a report action.** Error: "'ALERT' task can be
   used only in on load, on validate and on change actions".
3. **`info` IS visible to the user in a report action**, in a "log messages"
   dialog. This contradicts the assumption that `info` output is invisible.
4. **`openUrl` with "popup window" works from a report button** and opens a
   Creator form as a true modal. The per-row control is a Button COLUMN on the
   report, not the action item; the action item alone renders nothing on the row.
5. **`openUrl("#Script:dialog.close","same window")` DOES close a stateless
   popup form**, contradicting the community thread that said it only refreshes.
6. **`openUrl` is terminal.** An `openUrl` in an On Success workflow would kill
   whatever On Success jobs had not yet run, including the draft invoice. This is
   why the redirect on PVS save was skipped (13.1).
7. **`zoho.file.convertToPDF` options argument: UNRESOLVED, parked at Neil's
   instruction.** `Collection()` plus two-argument `insert` produced a LIST; a
   Map was rejected as the wrong type; a key-value literal was also rejected.
   Zoho's doc says lowercase `collection()` plus `insert`, which is what failed.
   The options argument was dropped entirely to get a send, so the running footer
   (patient, DOB, PVS ID, fax ID, page x of y) is missing from every faxed page.
8. **try/catch IS supported in Deluge custom functions**, and is required around
   `invokeurl`: `invokeurl` THROWS on a 503 rather than returning a body. Unwrapped,
   that aborted `send_pvs_fax` and stranded the `Fax_Log` row at Building.
9. **`left(250)` throws when the string is shorter than 250.** This hid the real
   RingCentral error behind a second failure. Guard every truncation on length.
10. **A self-lookup rejects 0.** Passing 0 to `Original_Fax_Link` kills the
    insert. Set optional lookups after the insert, and only when they resolve.
    Same for `Sent_By`, an Employees lookup that was being handed a login email.
11. **`for each` cannot iterate a variable holding a fetched record set in a
    standalone function.** The query has to sit inline in the `for each`.
12. **A stateless form offers only Field rules, On Load, On User Input and Click
    of a button.** There is no On Validate or On Success to hang logic on.
