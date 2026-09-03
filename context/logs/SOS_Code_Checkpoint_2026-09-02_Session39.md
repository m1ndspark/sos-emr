# SOS Code Checkpoint | 2026-09-02 | Session 39

Covers work since the Session 38 EOD checkpoint (2026-09-01). Scope this session
was Creator outbound email: getting a notification out of Creator at all, then
wiring one for Patient Visit referrals and one for 3008 referrals.

Reconstructed by ccode from the session facts. The project doc
`claude/SOS_Code_Checkpoint_2026-09-02_Session39.md` was not reachable from this
repo, so anything not listed here was not carried over.

---

## 1. Creator's own sendmail is unusable for this, and why

`sendmail` inside Creator is bound to Zoho's verified-sender rules. Three separate
failures, all confirmed this session:

- **Verified-sender restriction.** Creator will only send from an address it has
  verified. `notifications@sosreferrals.com` is not one, and adding it is not a
  path SOS controls from inside Creator.
- **Silent drops.** Sending with `zoho.adminuserid` as the sender produced no
  error and no mail. The function returned success and nothing arrived. There is
  no failure signal to trap, which makes this the worst of the three failures.
- **No external SMTP target.** `sendmail` cannot be pointed at an outside SMTP
  host, so there is no way to route around the restriction while staying in
  `sendmail`.

Conclusion: Creator notifications do not go through `sendmail`. They go out over
HTTP to a transactional mail API.

## 2. ZeptoMail established as the transport

Zoho's own transactional service, reached from Deluge with `invokeurl` against
`https://api.zeptomail.com/v1.1/email`.

Three things had to be right before anything sent:

1. **`body`, not `parameters`.** `invokeurl` with `parameters:` form-encodes the
   payload. ZeptoMail wants a JSON body and answers a form-encoded POST with a
   bare HTTP 500 and no message. Switching to `body:` was the fix. This is the
   single biggest time sink of the session and is written up in
   `docs/notifications.md`.
2. **`detailed:true`.** Without it the response carries no `responseCode` and
   there is nothing to branch on or log. With it, a success is HTTP **201** with
   code **`EM_104`**.
3. **Token placement.** The send token lives in `API_Config.Zepto_Send_Token`
   under `Config_Name = ZEPTOMAIL`. The stored value is the **key only**. The
   `Zoho-enczapikey ` prefix is added in code, not stored in the field.

Sender: `notifications@sosreferrals.com`. Recipients: `neil.heird@sosmmc.com` and
`joshua.kolanko@sosmmc.com`.

## 3. Two notification functions, live

Both are wired to the **Referrals Main On Create - Master** workflow.

| Function | Fires on | Status |
|---|---|---|
| `send_referral_notification` | `Referral_Type` = "Patient Visit" | LIVE |
| `send_3008_notification` | `Referral_Type` = "3008" | LIVE |

Each guards on `Referral_Type` at the top, so the two calls on the shared
workflow are mutually exclusive: exactly one body sends per referral, and an
Imaging Order referral sends neither.

Both accept **either** the custom `Referral_ID` (the `REF-MMDDYY-NNNN` form) **or**
the numeric Creator record ID, so they can be run by hand against a record from
the Execute pane without knowing which identifier is to hand.

## 4. Patient_DOB1 is the live DOB field

The referral form now writes DOB to **`Patient_DOB1`** (text), not `Patient_DOB`
(Date). `Patient_DOB` is still present on the form and still carries historical
values, so it cannot simply be deleted; dependent workflows have to be untangled
first. Recorded in `schema/Referrals_Main.md`. The 09-02 06:01 schema-monitor
capture predates this change, so the monitor will confirm it on the next run.

## 5. Open, carried into Session 40

Blocking:

- **3008 field rule wrongly hides the Advanced Directives question.** 3008
  requires Section H, so this is a correctness defect on a regulated form, not a
  cosmetic one.
- **Zoho Forms to Creator integration rebuild**, including `Imaging_Body_Site`.
- **File uploads still not reaching Creator.**

Not blocking:

- Imaging Order notification function (the third `Referral_Type` has no
  notification yet).
- Confirm the phone-format loop is present in `send_referral_notification`.
- 3008 partner-capture field set, awaiting approval: med list upload, last 4 SSN,
  primary and other diagnoses, advance directives, risk alerts, isolation
  precautions, PCP name and phone, mandatory emergency contact, transferred-from.
- Separate referral forms and pages per service type: Patient Visit, 3008,
  Imaging Order, IV Access.
- Replace the placeholder hrefs in the three-button entry block.
- Remove `Patient_DOB` after untangling dependent workflows.
- Provider CRM in Zoho CRM, parked on per-seat cost.
- Provider `@sosreferrals.com` aliases via Cloudflare Email Routing.
- Portal login page for PVS access.

All of the above are filed in `context/23_task_list.md`. None carry a hard
deadline.

## 6. Notes

- No PHI in this checkpoint or in any file committed this session. Field link
  names, schema and architecture only.
- The architecture write-up, including the `body` vs `parameters` trap and the
  full response-code table, is at `docs/notifications.md`.
