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

### The live map, 38 rows
Read verbatim off the integration screen on 2026-08-31 (Session 38). This is the
authoritative record of what the live integration does. Anything in this file
that disagrees with it is wrong.

The Creator link-name column is not on that screen; it is resolved from
`schema/Referrals_Main.md` (captured 2026-08-31) so the map is usable from
Deluge. All 38 Creator field names matched a live schema display name exactly,
which is a check on the transcription as well as a convenience.

| # | Creator link name | Creator field | Zoho Forms question |
|---|---|---|---|
| 1 | `Referral_Source` | Referral Source | Referral Source |
| 2 | `Referral_Type` | Service | Service Requested |
| 3 | `Patient_First_Name` | Patient First Name | Patient First Name |
| 4 | `Patient_Last_Name` | Patient Last Name | Patient Last Name |
| 5 | `Patient_DOB` | Patient DOB | Patient DOB |
| 6 | `Patient_Gender` | Patient Gender | Biological Sex |
| 7 | `Patient_Hospice_ID` | Patient Hospice ID | Hospice ID |
| 8 | `Patient_Phone` | Patient Phone | Patient Phone |
| 9 | `Has_Additional_Contact` | Is there an additional contact? | Is there an additional/emergency contact for this patient? |
| 10 | `AC_First_Name` | AC First Name | AC First Name |
| 11 | `AC_Last_Name` | AC Last Name | AC Last Name |
| 12 | `AC_Phone` | AC Phone | AC Phone |
| 13 | `AC_Relationship_to_Patient` | AC Relationship to Patient | Relation to Patient |
| 14 | `Patient_Location` | Patient Location | Where is the patient currently located? |
| 15 | `Facility_Name` | Facility Name | Facility Name |
| 16 | `Facility_Phone` | Facility Phone | Facility Phone |
| 17 | `Facility_Room_Number` | Facility Room Number | Room # |
| 18 | `Patient_Address` | Patient Address | Patient Address |
| 19 | `Referral_Reason` | Reason for Referral | What is the reason for this referral? |
| 20 | `Partner_ICD_Codes` | Partner ICD Codes | ICD-10 Codes |
| 21 | `X_Ray_Needed` | Will an X-Ray be needed for this referral? | Will this referral require imaging (X-ray or other)? |
| 22 | `Patient_Has_Allergies` | Does this patient have allergies? | Does the patient have allergies? |
| 23 | `List_Patient_Allergies` | List Patient Allergies | List all allergies |
| 24 | `Patient_Has_Anticoagulants` | Does the patient take anticoagulants? | Does the patient use anticoagulant meds? |
| 25 | `List_Patient_Anticoagulants` | List Patient Anticoagulants | List anticoagulant meds |
| 26 | `Patient_Has_Advanced_Directives` | Does the patient have Advanced Directives? | Does the patient have Advanced Directives? |
| 27 | `Advanced_Directives_Details` | Advanced Directives Details | Advanced Directives Details |
| 28 | `Additional_Information` | Additional Information | Do you have additional information to share with us? |
| 29 | `Imaging_Type_Order` | Imaging Test(s) to be Ordered | List Imaging test(s) to be Ordered |
| 30 | `Imaging_Order_Indication` | Reason for Imaging Order(s) | Reason for Imaging Order(s) |
| 31 | `Partner_POC_First_Name` | Partner POC First Name | Referral POC First Name |
| 32 | `Partner_POC_Last_Name` | Partner POC Last Name | Referral POC Last Name |
| 33 | `Partner_POC_Title` | Partner POC Title | Referral POC Title |
| 34 | `Partner_POC_Team` | Partner POC Team | Partner Clinical Team |
| 35 | `Partner_POC_Phone` | Partner POC Phone | Partner POC Phone |
| 36 | `Partner_POC_Email` | Partner POC Email | Partner POC Email |
| 37 | `Partner_Location_Label` | Partner Location Label | Referral Partner Lookup |
| 38 | `Form_Token` | Form Token | Form Token |

### Row to ADD on the pending rebuild
`Imaging_Body_Site` <- "Body Part / Affected Area", inserted after row 30. The
Creator field already exists; the integration row does not, so the field stays
empty on every submission until the rebuild happens. The rebuild is therefore 39
rows, not 38.

### Confirmed NOT mapped, 21 fields
Verified against the same screen on 2026-08-31. This supersedes the old
"do not map" list, which was shorter and was written from the schema rather than
read off the integration.

| Creator link name | Creator field |
|---|---|
| `Patient_MI` | Patient MI |
| `Patient_SSN` | Patient SSN |
| `Patient_Full_Address` | Patient Full Address |
| `Prior_POC_Email` | Prior POC Email |
| `Email_Changed` | Has your email changed? |
| `General_Files_Upload` | General Files Upload |
| `Imaging_Orders_Upload` | Upload Imaging Orders |
| `File_upload` | File upload |
| `Partner_Link` | Partner Lookup |
| `Partner_Branch_Link` | Partner Branch Lookup |
| `Partner_Organization` | Partner Organization |
| `Partner_Branch` | Partner Branch/Location |
| `Referral_ID` | Referral ID |
| `Referral_Date` | Referral Date |
| `Referral_ID_Stamp` | Referral ID Stamp |
| `Patient_Full_Name` | Patient Full Name |
| `AC_Full_Name` | AC Full Name |
| `Partner_POC_Name_Title` | Partner POC Name & Title |
| `Partner_ID` | Partner ID |
| `Partner_ID_Stamp` | Partner ID Stamp |
| `Referral_Added_Time` | Referral Added Time |

### Reconciliation, and the retired 44
38 mapped + 21 unmapped + `Imaging_Body_Site` = **60**, which is exactly the
field count in `schema/Referrals_Main.md` as captured 2026-08-31. Every field on
the form is accounted for, and the only one in neither list is the new one
awaiting the rebuild.

**The Session 29 figure of 44 mapped / 12 not mapped / 14 removed is RETIRED.**
It was a spec written from the Creator schema and was never verified against the
integration screen. It is not a target for the rebuild and should not be used to
check the rebuild's row count; the number to hit is 39. The Session 29 split is
left out of this section deliberately rather than corrected in place, because
two counts sitting side by side is how it got mistaken for live state in the
first place.

### OPEN: no file upload field is mapped
`General_Files_Upload`, `Imaging_Orders_Upload` and `File_upload` all appear in
the unmapped list above, confirmed against the live screen. Partner uploads are
not reaching Creator at all.

Owner Neil. Open. **Blocking if uploads are expected in Creator** - that ruling
has not been made. If they are expected this is a live data-loss defect, not a
gap, and every referral submitted with an attachment since the integration was
built has lost it. The rebuild must add them.

### OPEN: Additional Information is mapped to a Yes/No radio
Row 28 above. The Creator `Additional_Information` textarea is mapped to the
form's "Do you have additional information to share with us?" question, which is
a Yes/No radio, not a text field. It is therefore likely storing the literal
string "Yes" rather than the partner's note.

Owner Neil. Open. Not blocking. Needs verification against live records: pull a
referral where the partner answered Yes and check what the textarea actually
holds. If confirmed, the real note field has to be identified before the rebuild,
since the rebuild is the only chance to correct the mapping.

Partner_Location_Label is MAPPED, from the Referral Partner Lookup grouped
dropdown; it is row 37 of the live map above. The master On Success workflow
still normalizes it and derives the other partner fields from it.
(This paragraph previously carried a "43 -> 44 mapped, 13 -> 12 not mapped"
count from the Session 29 spec. Removed with the rest of that count.)

The stray "Prior POC Email <- Partner POC Email" integration row (left over
from the dropped Option B email-change design in section 9) was removed.

Do not map (Creator generates these): superseded by the verified 21-row
"Confirmed NOT mapped" table above, which was read off the integration screen.
The old 12-name list here was written from the schema and was missing
Patient_MI, Patient_SSN, Prior_POC_Email, Email_Changed, the three upload
fields, Referral_Date and Referral_Added_Time.

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
| Integration rebuild: 39 rows (38 live + Imaging_Body_Site) | NOT DONE - the new field does not reach Creator until it is |
| 38-row live map not captured in this repo | CLOSED Session 38 - filed verbatim in section 10 |
| No file upload field mapped: General_Files_Upload, Imaging_Orders_Upload, File_upload | OPEN - ruling needed, blocking if uploads are expected. Confirmed against the live screen |
| Additional Information textarea mapped to the Yes/No radio | OPEN - confirmed in the live map, row 28. Verify against a live record |
| Session 29 count of 44 mapped | RETIRED Session 38 - never verified against the integration screen, superseded by the 38-row map |
| Creator page Patient_Referrals embeds the stale form PatientReferral | OPEN |
| Referral_Type choices on Referrals_Main do not match the form's Service list | OPEN |
