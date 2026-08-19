# SOS PVS Fax System - Design Spec

Designed 2026-08-19 (Session 34), built through Session 35 the same day. This
document is the spec: it stands on its own and is the file to read first before
touching any of this code.

**State: auth is live, nothing has been faxed yet.** All four functions compile
and authenticate against RingCentral. Section 12 lists the three live-form gaps
standing between that and a working send. Section 11 is the gotchas list.

Platform: Zoho Creator (Deluge) plus the RingCentral Fax API.
Session logs:
[Session 34](../sessions/SOS_Code_Session_Log_2026-08-19_Session34_EOD.md) (design),
[Session 35](../sessions/SOS_Code_Session_Log_2026-08-19_Session35_EOD.md) (build).

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

Status: **not created.**

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
> `Fax_Log` field, which is a separate field on a separate form and is currently
> short four of its seven choices. See section 12.

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

Status: **BUILT (Session 35), with three gaps.** `schema/Fax_Log.md`, captured
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

**See section 12.** These block the first real send.

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
| `poll_fax_status` | Polls every Queued record, closes Sent ones, records `faxErrorCode` on failures, routes to Retry Pending or Permanent Fail, marks anything Queued past 4 hours as Stuck. Permanent Fail is taken either from a no-retry error code or from `Attempt_Number >= 3`. Returns a one-line summary so Creator's scheduled-workflow history is a usable run trail. | written, **does not save** until `Fax_Log` exists in full |

---

### 8.1 Five defects found and fixed

Found by ccode 2026-08-19 when the real bodies were first committed (`fc4276d`),
except defect 5 which Neil caught. **All five are fixed in source and the
corrected bodies are re-extracted here** as of `fc4276d`'s follow-up commit.

| # | Function | Defect | Status |
|---|---|---|---|
| 1 | `create_3008_pvs_july` | `PVS_ID` sequence off by one, would duplicate a billing record locator | FIXED |
| 2 | `send_pvs_fax`, `build_pvs_fax_html` | `&mdash;` rendered an em dash on every faxed page | FIXED |
| 3 | `get_rc_token` | no safety margin on the cached token | FIXED |
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

Both are fixed, and the fix is better than the original design. The read now
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
cache window is correct whatever the app issues. **This closes the VERIFY LIVE
item on token TTL that stood in the previous revision of this document.** Nothing
needs checking against a live response any more.

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

- `retry_failed_faxes`.
- The 4:00 am digest function.
- The `PVS_Fax_Review` page.
- Faxes Sent and Fax Exceptions reports.
- `Partner_PVS_Fax` on `Partner_Billing_Contacts`.
- Optional: a validation workflow rejecting a fax number that is not 10 or 11
  digits.
- The three live-form gaps in section 12.

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
7199 RingCentral's documentation implies. `get_rc_token` reads `expires_in` off the
response rather than hardcoding, so this needs no further action. Had the original
hardcoded 115 minute expiry survived, every token would have been treated as valid
for roughly an hour after it died, and the failure would have shown up as
intermittent, hard-to-reproduce fax failures. The Session 34 fix paid for itself on
the first live call.

Nothing has actually been faxed yet. Auth working is not the same as a send
working, and section 12 lists what stands between the two.

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
confirm it in `schema/<Form>.md` afterwards. This one is still biting: see section
12.

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
