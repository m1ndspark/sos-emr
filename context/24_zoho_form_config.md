# Zoho Form Configuration - Partner-Facing Referral Form

Created Session 29, 2026-08-08.

Living record of everything built in Zoho Forms for the partner referral
intake, plus the platform limits that shaped it. Sections marked
**[NEEDS INPUT]** are things that must be filled in from the Zoho UI.

--------------------------------------------------------------------------------
## 1. Identity
--------------------------------------------------------------------------------

| Item | Value |
|---|---|
| Zoho Forms org | SOSReferralForm |
| Live form (link name) | `PatientReferralsHCO` |
| Title / nickname | Patient Referral |
| Public form perma | `_WhhCPE6GSg7iEZZyE6YGawxwZHr4Izij2oGuzkAGds` |
| Builder URL | forms.zoho.com/SOSReferralForm/form/PatientReferralsHCO/builder |
| Rules URL | forms.zoho.com/SOSReferralForm/form/PatientReferralsHCO/rules |
| Custom domain | referral.sosreferrals.com |
| Target Creator form | `Referrals_Main` |

RESOLVED Session 38, 2026-08-31. `PatientReferralsHCO` is the live form.
`PatientReferral` is the previous app build and is not in use.

**Form link names are fixed at creation.** Only the title and the nickname can
be edited afterwards, which is why the link name still reads PatientReferralsHCO
while the form presents as "Patient Referral". A cleaner URL would require
duplicating the form, which mints a new perma and forces a full integration
rebuild. REJECTED Session 38: the URL is not worth re-selecting every field by
hand and re-testing the whole intake path.

STILL OPEN, separate row in context/23: the Creator page `Patient_Referrals`
embeds form `PatientReferral` in its HTML snippet. That is a stale reference to
the previous build and serves the wrong form to anyone arriving that way.

--------------------------------------------------------------------------------
## 2. Page order
--------------------------------------------------------------------------------

| # | Page |
|---|---|
| 1 | Referral Details |
| 2 | Patient Details |
| 3 | Patient Details Cont'd |
| 4 | Additional Contact Details |
| 5 | Patient Location |
| 6 | Patient Medical Info |
| 7 | General Information |
| 8 | Imaging Order Details |
| 9 | Partner Lookup Details |
| 10 | Referral Partner Details |

Branch point is **Service Requested** on page 1.
Choices: Patient Visit / 3008 / Imaging Order (only).
"Lab Draw (only)" was removed - lab-only ordering is retired.

--------------------------------------------------------------------------------
## 3. The constraint that shaped every rule
--------------------------------------------------------------------------------

**One rule per target question.** A rule's action list can target many
fields, but a given field should appear in only one rule.

Consequence: rules are grouped by **condition**, not by service. The two
fields that 3008 and Imaging Order both hide live in a single OR rule
rather than appearing once in a 3008 rule and again in an Imaging rule.

Related behaviours:
- Field rules are live. They revert on their own when the condition stops
  matching, so no Else branch is needed. Else is only offered on Page Rules.
- Page skip-to only jumps forward. Any page every service needs must sit
  before the branch point or after all branches.
- Note elements are NOT targetable by field rules. Only fields that accept
  input appear in the action list. Any conditional message must therefore
  live in a real input field (a read-only Multi Line), not a Note.

--------------------------------------------------------------------------------
## 4. Field rules
--------------------------------------------------------------------------------

### 3008 Suppression - BUILT
- If: Service Requested `Is` 3008
- Show: 3008 Files Upload
- Hide: Does the patient have Advanced Directives? / Do you have additional
  information to share with us?

### 3008 & Imaging Order Combined - BUILT
- If: `( A1 OR A2 )` where A1 = Service Requested `Is` 3008,
  A2 = Service Requested `Is` Imaging Order (only)
- Hide: Will an X-Ray be needed for this referral? / Does the patient use
  anticoagulant meds?

### Imaging Order only - BUILT Session 38
- If: Service Requested `Is` Imaging Order (only)
- Hide: Does the patient have allergies? / Is the patient self-responsible?

### Trigger question relabel - Session 38
The imaging trigger question now reads **"Will this referral require imaging
(X-ray or other)?"**. Label only. The link name `X_Ray_Needed` and its three
values (No / Yes / I'm Not Sure) are unchanged, so no rule, no mapping and no
Creator field was affected.

**The "3008 & Imaging Order Combined" rule must stay.** It hides the trigger
question for 3008 and Imaging Order (only), which leaves it blank for those
services. The General Information page rule below depends on that blank: it is
what stops the trigger question from ever being evaluated on a non-Patient-Visit
path. Removing the field rule would silently break the page rule.

--------------------------------------------------------------------------------
## 5. Page rules
--------------------------------------------------------------------------------

Both page rules below were BUILT in Session 38, 2026-08-31. They replace the
earlier General Information rule and the two specced-but-unbuilt entries.

### On page: Patient Medical Info - BUILT Session 38
- Rule 1: Service Requested `Is` Imaging Order (only) -> skip to
  **Imaging Order Details**
- Finally: skip to **General Information**

### On page: General Information - BUILT Session 38
- Rule 1: Service Requested `Is` Patient Visit AND trigger question
  `Is not` Yes -> skip to **Partner Lookup Details**
- Rule 2: Service Requested `Is` 3008 -> skip to **Partner Lookup Details**
- Finally: skip to **Imaging Order Details**

### Net effect
The existing **Imaging Order Details** page now serves two branches, and no
second imaging page was needed:

| Service | Trigger question | Sees Imaging Order Details |
|---|---|---|
| Imaging Order (only) | hidden, blank | yes, reached from Patient Medical Info |
| Patient Visit | Yes | yes, falls through General Information |
| Patient Visit | No | no |
| Patient Visit | I'm Not Sure | no |
| 3008 | hidden, blank | no |

`Is not` Yes is what makes No and I'm Not Sure behave identically. Both skip the
imaging page. If a future ruling needs I'm Not Sure to collect imaging detail,
that condition is the single place to change.

OPEN QUESTION, still undecided: does Imaging Order (only) also skip Additional
Contact Details?

--------------------------------------------------------------------------------
## 6. Partner Lookup Details page
--------------------------------------------------------------------------------

Fields:
- Partner POC Email + **Search** button (`.fldSuffixBtn.whookSearchBtn`)
- Referral Partner Lookup (grouped searchable dropdown, ~80 bare location
  names; mapped in the Creator integration to Partner_Location_Label). Replaces
  the former free-text Partner Branch/Location question and the Referral Partner
  Organization question, both now DELETED.
- Partner Clinical Team
- Referral POC First Name / Last Name / Title
- Referral POC Phone
- Lookup Status (read-only, receives FOUND / NOT_FOUND)
- Lookup Message (read-only Multi Line, receives the display text)
- Verification Code (captcha)

### The problem this page had
The Search button behaved identically whether the lookup found a contact or
not. A partner whose email was not on file saw nothing happen.

### The fix
The Creator custom API returns the message text itself. No rule required to
compose it; the field either has a message or it does not.

--------------------------------------------------------------------------------
## 7. Prefill webhook
--------------------------------------------------------------------------------

Configured at: form builder -> click the **Partner POC Email** field ->
Properties -> **Edit Prefill Configuration**. Three steps: Webhook Settings,
Test & Verify, Prefill Mapping.

| Setting | Value |
|---|---|
| Method | GET |
| URL | `https://www.zohoapis.com/creator/custom/sosmmc/Get_Partner_Referral_Contact` |
| Authorization | Connections |
| Connection | SOS Creator Connection (`sos_creator...`) |
| URL parameter | `pPocEmail` <- Partner POC Email |

Bound Creator function: `get_partner_referral_contact(string pPocEmail)`,
return type **map**, namespace default.

Response keys and their mappings:

| Key | Maps to |
|---|---|
| `/result/Lookup_Status` | Lookup Status |
| `/result/Lookup_Message` | Lookup Message |
| `/result/Partner_Organization` | Referral Partner Organization |
| `/result/Partner_Branch` | Referral Partner Lookup |
| `/result/Partner_POC_Team` | Partner Clinical Team |
| `/result/Partner_POC_First_Name` | Referral POC First Name |
| `/result/Partner_POC_Last_Name` | Referral POC Last Name |
| `/result/Partner_POC_Title` | Referral POC Title |
| `/result/Partner_POC_Phone` | Partner POC Phone |

Prefill Mapping only refreshes its available key list after re-running
step 2 Test & Verify. A new response key will not appear until you do. This
prefill mapping lives in the form Builder on the Partner POC Email field, NOT
on the Creator integration screen; the two are separate maps and are edited in
different places.

The function carries a **case-insensitive fallback scan**. Deluge criteria
matching on email fields is case-sensitive, so a partner whose stored email
differed only in case previously got a silent empty result. Same defect
class as the Partner Contact Upsert bug in context/28.

--------------------------------------------------------------------------------
## 8. Partner-facing copy
--------------------------------------------------------------------------------

FOUND (returned in Lookup_Message):
> Welcome back! We found your details and filled them in below. Update
> anything that has changed before you continue.

NOT_FOUND (returned in Lookup_Message):
> We couldn't find that email address. Double-check it for typos and search
> again. If you're new here, leave your email as entered, complete the
> remaining fields, and we'll save everything for next time.

New-user note:
> Looks like you're new here! Complete the fields below and we'll save them
> to speed up your next visit.

Closing note (last page):
> That's our new referral portal. It replaces the form you used before, and
> it only asks the questions that apply to the service you're requesting, so
> most referrals take less time to submit. Your contact details are saved
> after your first submission, so entering your email will fill them in from
> then on. If anything looks wrong or you have trouble, call us at
> (813) 513-1925.

--------------------------------------------------------------------------------
## 9. Email-change handling - SPECCED AND DROPPED
--------------------------------------------------------------------------------

Three designs were worked through and all were rejected. Recorded so they
are not re-proposed.

**Option A - per-contact token.** Add a Form_Token field to
Partner_Referral_Contacts, generate a random opaque token per contact, and
carry it in a personalised prefill link. Identity comes from the token, so
email becomes just another editable field.
REJECTED: replaces one shared referral URL with a personal link per contact
that must be distributed, must not be forwarded, and breaks if lost. Neil:
"no personal links." A sequential token (Sequence_Tracker style) is also
unusable here - an enumerable token lets any partner pull another partner's
contact record.

**Option B - "Has your email changed?" plus a Prior POC Email field.**
Specced in full including the revised upsert. Dropped.

**Option C - echo the searched email back from the API into a hidden field,
so the prior address is captured with no extra question.** Blocked: Zoho
Forms allows only ONE lookup field per form, so there is no second search
to run against the old address.

**DECISION: no email-change handling at all.** A partner whose email changed
searches with the new address, finds nothing, completes the fields, and
creates a duplicate row in Partner_Referral_Contacts. That is the entire
cost and it is acceptable. The referral itself still lands correctly in
Referrals_Main. Typos have the same cost and the same answer.

--------------------------------------------------------------------------------
## 10. Creator integration
--------------------------------------------------------------------------------

Native Zoho Forms -> Creator integration writing into `Referrals_Main`.

**HARD LIMITATION: an existing field map cannot be edited.** Any field
change means removing the integration and adding it back, re-selecting every
field by hand.

Mapping split as specced Session 29: 44 partner-entered fields mapped, 12
Creator-generated fields NOT mapped, 14 removed fields that must not be
re-selected.

**Session 38 count disagrees with that figure.** The live integration was read
back on 2026-08-31 and carries **38 rows**, not 44. The row-by-row map is in
`claude/SOS_ZohoForm_Config.md` section 8, which is a cchat-side document and is
NOT on the ccode machine, so the 38 rows are not reproduced here yet. Do not
treat the 44 above as the live state. Whoever has that document should paste
section 8 into this section; a placeholder is left below rather than a
reconstructed list, because a wrong field map on a referral intake is worse than
a missing one.

### 38-row live integration map - NOT YET CAPTURED IN THIS REPO
Source: `claude/SOS_ZohoForm_Config.md` section 8 (cchat side).
Needed here: all 38 form-field -> Creator-field rows, plus the confirmed-unmapped
list. Raised Session 38.

### Confirmed unmapped, found Session 38
No file upload field appears in the live integration. `General_Files_Upload`,
`Imaging_Orders_Upload` and `File_upload` have no row, so partner uploads are
not reaching Creator. Whether that is a defect depends on a ruling that has not
been made: see context/23, OPEN BLOCKING. If uploads are expected, the rebuild
must add them.

### Suspect mapping, found Session 38
The Creator Additional Information textarea is mapped to the form's
"Do you have additional information to share with us?" **Yes/No radio**, not to
a text field. If that is what the live map says, the textarea is storing the
literal string "Yes" and the partner's note is being discarded. Verify against a
live record before the rebuild.

### Imaging_Body_Site must be added
The rebuild is 38 existing rows **plus** `Imaging_Body_Site` <- "Body Part /
Affected Area". The Creator field already exists (see schema/Referrals_Main.md,
captured 2026-08-31); the integration row does not, so the field stays empty on
every submission until the rebuild happens.

Partner_Location_Label is now MAPPED, from the Referral Partner Lookup grouped
dropdown, so it moved out of the do-not-map list below (one field crossed over:
43 -> 44 mapped, 13 -> 12 not mapped). The master On Success workflow still
normalizes it and derives the other partner fields from it.

The stray "Prior POC Email <- Partner POC Email" integration row (left over
from the dropped Option B email-change design in section 9) was removed.

Do not map (Creator generates these): Partner_Link, Partner_Branch_Link,
Partner_Organization, Partner_Branch, Partner_ID, Partner_ID_Stamp,
Partner_POC_Name_Title, Referral_ID, Referral_ID_Stamp, Patient_Full_Name,
AC_Full_Name, Patient_Full_Address.

Gone - must not be re-selected: Requested_Priority, SOS_Prior_Service,
Patient_Responsibility, DM_First_Name, DM_Last_Name, DM_Full_Name,
Decision_Maker_Phone, Decision_Maker_Email,
Decision_Maker_Relationship_to_Patient, Imaging_Files_Upload,
Lab_Type_Orders, Lab_Order_Indication, Requested_Lab_Vendor,
Lab_Files_Upload.

--------------------------------------------------------------------------------
## 11. Styling and embedding
--------------------------------------------------------------------------------

**Cross-origin.** The form renders in an iframe served from
forms.zohopublic.com / referral.sosreferrals.com. No CSS or JS from the host
page can reach inside it. `.fldSuffixBtn.whookSearchBtn` cannot be styled
from WordPress or from a Creator portal page, and `!important` changes
nothing - the rule is never delivered to the form's document.

**Custom CSS is not available on the current Zoho Forms plan.** The only
lever for anything inside the form is Themes. Interior left/right padding is
the theme's page margin, not the embed.

**HTML/CSS export is not an option.** It would give full styling control but
does not support hidden fields, field rules, page rules, or captcha - i.e.
the entire branching structure plus the Verification Code field.

**Creator page builder strips `<script>`** from HTML snippet elements, so
the Creator-side embed must be a bare iframe.

### Live embed (WordPress, Beaver Builder HTML module)
- Custom domain `referral.sosreferrals.com`
- Auto-height retained (`?zf_rszfm=1` plus the postMessage listener) with
  `scrolling="no"` so there is no inner scrollbar
- 20px radius and box-shadow on a wrapper div with `overflow:hidden`;
  the iframe itself is 100% width
- UTM and `referrername` parameter logic retained
- FIXED: the previous version rendered TWO iframes, one hardcoded in the
  markup and one appended by the script

--------------------------------------------------------------------------------
## 12. Open issues
--------------------------------------------------------------------------------

| Item | Status |
|---|---|
| Lookup messages do not appear reliably on the live form. API response and mapping both verified correct. Suspect the field's Read Only / Hidden setting blocks the prefill write. | OPEN |
| Next diagnostic: log every call inside `get_partner_referral_contact` so a missing message with no log row (Search never fired) can be told apart from a log row with no message (write failed). Needs the Change_Log field link names. | OPEN |
| Imaging Order field rule | BUILT Session 38 |
| Patient Medical Info page rule | BUILT Session 38 |
| General Information page rule: Patient Visit -> skip to Partner Lookup Details | BUILT Session 38, as Patient Visit AND trigger question Is not Yes |
| Does Imaging Order skip Additional Contact Details? | UNDECIDED |
| Integration rebuild: 38 live rows + Imaging_Body_Site | NOT DONE - the new field does not reach Creator until it is |
| 38-row live map not captured in this repo (cchat-side doc) | OPEN |
| No file upload field mapped: General_Files_Upload, Imaging_Orders_Upload, File_upload | OPEN - ruling needed |
| Additional Information textarea mapped to the Yes/No radio | OPEN - verify against a live record |
| Creator page Patient_Referrals embeds the stale form PatientReferral | OPEN |
| Referral_Type choices on Referrals_Main do not match the form's Service list | OPEN |
