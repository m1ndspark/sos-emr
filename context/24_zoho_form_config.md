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
| Builder form (current work) | `PatientReferralsHCO` |
| Public form perma | `_WhhCPE6GSg7iEZZyE6YGawxwZHr4Izij2oGuzkAGds` |
| Builder URL | forms.zoho.com/SOSReferralForm/form/PatientReferralsHCO/builder |
| Rules URL | forms.zoho.com/SOSReferralForm/form/PatientReferralsHCO/rules |
| Custom domain | referral.sosreferrals.com |
| Target Creator form | `Referrals_Main` |

**[NEEDS INPUT]** - `PatientReferral` and `PatientReferralsHCO` are two
different forms in the same org. Confirm which is live and whether one is
being retired.

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

### Imaging Order only - NOT BUILT
- If: Service Requested `Is` Imaging Order (only)
- Hide: Does the patient have allergies? / Is the patient self-responsible?

--------------------------------------------------------------------------------
## 5. Page rules
--------------------------------------------------------------------------------

### On page: General Information - BUILT
- Rule 1: Service Requested `Is` 3008 -> skip to **Partner Lookup Details**
- Finally: skip to **Imaging Order Details**

### On page: Patient Medical Info - NOT BUILT
- Rule 1: Service Requested `Is` Imaging Order (only) -> skip to
  **Imaging Order Details**
- Finally: skip to **General Information**

OPEN QUESTION: does Imaging Order (only) also skip Additional Contact
Details? Undecided.

--------------------------------------------------------------------------------
## 6. Partner Lookup Details page
--------------------------------------------------------------------------------

Fields:
- Partner POC Email + **Search** button (`.fldSuffixBtn.whookSearchBtn`)
- Referral Partner Organization
- Partner Branch/Location
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
| `/result/Partner_Branch` | Partner Branch/Location |
| `/result/Partner_POC_Team` | Partner Clinical Team |
| `/result/Partner_POC_First_Name` | Referral POC First Name |
| `/result/Partner_POC_Last_Name` | Referral POC Last Name |
| `/result/Partner_POC_Title` | Referral POC Title |
| `/result/Partner_POC_Phone` | Referral POC Phone |

Prefill Mapping only refreshes its available key list after re-running
step 2 Test & Verify. A new response key will not appear until you do.

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

Mapping split: 43 partner-entered fields mapped, 13 Creator-generated fields
NOT mapped, 14 removed fields that must not be re-selected.

Do not map (Creator generates these): Partner_Link, Partner_Branch_Link,
Partner_Organization, Partner_Branch, Partner_ID, Partner_ID_Stamp,
Partner_Location_Label, Partner_POC_Name_Title, Referral_ID,
Referral_ID_Stamp, Patient_Full_Name, AC_Full_Name, Patient_Full_Address.

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
| Imaging Order field rule | NOT BUILT |
| Patient Medical Info page rule | NOT BUILT |
| Does Imaging Order skip Additional Contact Details? | UNDECIDED |
| Integration rebuild, 43 fields | NOT DONE - blocks the remap |
