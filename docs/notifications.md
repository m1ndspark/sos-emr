# SOS Notifications Architecture

Outbound email from the SOS Referrals Creator app. Written Session 39,
2026-09-02, when the first notifications went live.

Schema and configuration only. No PHI, no live tokens.

---

## 1. Why Creator's `sendmail` is not used

Deluge `sendmail` inside Creator cannot deliver SOS notification mail. Three
distinct failures, all confirmed:

| Failure | Detail |
|---|---|
| Verified-sender restriction | Creator only sends from an address Zoho has verified for the account. `notifications@sosreferrals.com` is not verified there, and verifying it is not something SOS controls from inside Creator. |
| Silent drops | Sending with `zoho.adminuserid` as the sender returns success and delivers nothing. No error, no bounce, no trap. This is the dangerous one: a function can look healthy and send no mail at all. |
| No external SMTP | `sendmail` cannot be pointed at an outside SMTP host, so there is no way to route around the sender restriction while staying inside `sendmail`. |

Do not reopen `sendmail` for notification work.

## 2. Transport: ZeptoMail REST API over `invokeurl`

- Endpoint: `https://api.zeptomail.com/v1.1/email`
- Method: POST
- Called from Deluge with `invokeurl`

### 2.1 Use `body`, not `parameters`

`invokeurl` with `parameters:` **form-encodes** the payload. ZeptoMail expects
JSON and answers a form-encoded POST with a bare **HTTP 500** carrying no
message, which reads like a server-side outage rather than a client mistake.

Pass the payload as `body:` with a JSON content type. This was the single
largest debugging cost in Session 39.

### 2.2 Use `detailed:true`

Without `detailed:true` the response carries no `responseCode`, so there is
nothing to branch on and nothing worth logging. Set it always.

### 2.3 Response codes

| Result | HTTP | Code |
|---|---|---|
| Success | 201 | `EM_104` |
| Form-encoded payload (the `parameters` mistake) | 500 | none returned |

Treat anything other than 201 / `EM_104` as a failure.

## 3. Credentials

| Where | Value |
|---|---|
| Form | `API_Config` |
| Record | `Config_Name = ZEPTOMAIL` |
| Field | `Zepto_Send_Token` (Multi Line) |

The field stores the **key only**. The `Zoho-enczapikey ` prefix is prepended in
code when building the Authorization header - it is not part of the stored
value. Storing the prefix as well produces a doubled prefix and a rejected send.

## 4. Addresses

- From: `notifications@sosreferrals.com`
- To: `neil.heird@sosmmc.com`, `joshua.kolanko@sosmmc.com`

## 5. Functions

| Function | Guard | Wired to |
|---|---|---|
| `send_referral_notification` | `Referral_Type` = "Patient Visit" | Referrals Main On Create - Master |
| `send_3008_notification` | `Referral_Type` = "3008" | Referrals Main On Create - Master |

Both functions hang off the **same** workflow. Because each guards on
`Referral_Type` before doing any work, the two calls are **mutually exclusive**:
one referral produces exactly one notification. A referral of any other type
(currently Imaging Order) produces none - see the open item in
`context/23_task_list.md` for the missing Imaging Order function.

### 5.1 Argument handling

Both functions accept **either** identifier:

- the custom `Referral_ID` (the `REF-MMDDYY-NNNN` form), or
- the numeric Creator record ID.

The function resolves whichever it is given. This means either can be run by
hand from the Execute pane against a record without first looking up which
identifier form is available.

## 6. Related

- `schema/API_Config.md` - the `Zepto_Send_Token` field and ZEPTOMAIL record
- `context/logs/SOS_Code_Checkpoint_2026-09-02_Session39.md` - the session this was built in
- `context/05_deluge_learnings.md` - general Deluge gotchas
