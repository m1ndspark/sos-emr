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

NINE pages. Corrected Session 38 EOD, 2026-09-01.

| # | Page |
|---|---|
| 1 | Referral Details |
| 2 | Patient Details |
| 3 | Patient Details Cont'd |
| 4 | Patient Location |
| 5 | Patient Medical Info |
| 6 | General Information |
| 7 | Imaging Order Details |
| 8 | Referral Partner Lookup |
| 9 | Referral Partner Details |

**There is no Additional Contact page.** Earlier revisions of this file listed a
tenth page, "Additional Contact Details", sitting between Patient Details Cont'd
and Patient Location. It does not exist. The additional-contact questions are
**grids on Patient Details Cont'd**, revealed in place by field rule 2 in
section 4. Anything in this repo that treats Additional Contact as its own page -
a page count of ten, a page rule that targets it, an open question about whether
a service skips it - is wrong on that point and is corrected here.

Page 8 was also written in earlier revisions as "Partner Lookup Details". The
live page names are as tabled above.

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

All ELEVEN live field rules, in the order they appear on the Rules screen, as of
Session 38 EOD, 2026-09-01. This list is complete: a rule that is not below is
not on the form.

### 1. 3008 - ENABLED
- If: Service Requested `Is` 3008
- Show: 3008 Files Upload
- Hide: Patient DOB grid / Patient SSN grid / What is the reason for this
  referral? / ICD-10 grid / Does the patient have Advanced Directives? / Is the
  patient self-responsible? / Do you have additional information to share with us?

Wider than the "3008 Suppression" rule recorded earlier in Session 38, which had
only Advanced Directives and the additional-information question in its hide
list. The DOB and SSN grids, reason for referral, the ICD-10 grid and
self-responsible were added after that entry was written.

### 2. Additional Contact - ENABLED
- If: Is there an additional/emergency contact for this patient? `Is` Yes
- Show: the additional-contact grids on Patient Details Cont'd

This is the rule that makes Additional Contact a reveal-in-place block rather
than a page. See section 2.

### 3. Patient Location - ENABLED
- If: `( A1 OR A2 )` where A1 = Where is the patient currently located? `Is`
  Home, A2 = the same question `Is Empty`
- Hide: the facility grids

`Is Empty` is in the condition so the facility block stays hidden before the
question has been answered, not only after Home is picked.

### 4. Allergies - ENABLED
- If: Does the patient have allergies? `Is` Yes
- Show: List all allergies

### 5. Anticoagulants - ENABLED
- If: Does the patient use anticoagulant meds? `Is` Yes
- Show: List anticoagulant medications

### 6. Advanced Directives - ENABLED
- If: Does the patient have Advanced Directives? `Is` Yes
- Show: Advanced Directives Details

### 7. Additional Information - DISABLED, slated for deletion
Duplicate of rule 11: same trigger question, same intent. It is switched off, so
it is not live behaviour, and it should be deleted rather than left dormant. One
rule per target question is the constraint the whole ruleset is built on
(section 3), and a second rule aimed at the same targets is exactly what that
constraint exists to prevent. Left in place only so removing it is a deliberate
act rather than a side effect.

### 8. 3008 & Imaging Order Combined - ENABLED
- If: `( A1 OR A2 )` where A1 = Service Requested `Is` 3008,
  A2 = Service Requested `Is` Imaging Order (only)
- Hide: Will this referral require imaging (X-ray or other)? / Does the patient
  use anticoagulant meds?

### 9. Imaging Order - ENABLED
- If: Service Requested `Is` Imaging Order (only)
- Hide: Does the patient have allergies? / Is the patient self-responsible?

### 10. Partner Lookup - ENABLED
- If: `( A1 OR A2 )` where A1 = Lookup Status `Is Empty`,
  A2 = Partner POC Email `Is Empty`
- Hide: Email Lookup Alert

The alert is suppressed until a lookup has actually run against an entered
email, so an untouched page never shows it.

### 11. General Information - ENABLED
- If: Do you have additional information to share with us? `Is` Yes
- Show: the additional-details textarea / General Files Upload

### Trigger question relabel - Session 38
The imaging trigger question reads **"Will this referral require imaging (X-ray
or other)?"**. Label only. The link name `X_Ray_Needed` and its three values
(No / Yes / I'm Not Sure) are unchanged, so no rule, no mapping and no Creator
field was affected.

**Rule 8 must stay.** It hides the trigger question for 3008 and for Imaging
Order (only), which leaves it blank on those services. The General Information
page rule in section 5 depends on that blank: it is what stops the trigger
question from ever being evaluated on a non-Patient-Visit path. Removing the
field rule would silently break the page rule.

--------------------------------------------------------------------------------
## 5. Page rules
--------------------------------------------------------------------------------

Three page rules, as they stand at Session 38 EOD, 2026-09-01.

### On page: Patient Location
- Rule 1: Service Requested `Is` 3008 -> skip to **General Information**
- Finally: skip to **Patient Medical Info**

CHANGED this session. Rule 1 previously sent 3008 straight to **Referral Partner
Lookup**, which skipped General Information along with Patient Medical Info.
3008 now collects General Information and leaves that page by Rule 2 below.

### On page: Patient Medical Info
- Rule 1: Service Requested `Is` Imaging Order (only) -> skip to
  **Imaging Order Details**
- Finally: skip to **General Information**

### On page: General Information
- Rule 1: Service Requested `Is` Patient Visit AND "Will this referral require
  imaging (X-ray or other)?" `Is not` Yes -> skip to **Referral Partner Lookup**
- Rule 2: Service Requested `Is` 3008 -> skip to **Referral Partner Lookup**
- Finally: skip to **Imaging Order Details**

### Pathway matrix
Which pages each service actually sees, derived from the three rules above.

| # | Page | Patient Visit | 3008 | Imaging Order (only) |
|---|---|---|---|---|
| 1 | Referral Details | yes | yes | yes |
| 2 | Patient Details | yes | yes | yes |
| 3 | Patient Details Cont'd | yes | yes | yes |
| 4 | Patient Location | yes | yes | yes |
| 5 | Patient Medical Info | yes | **skipped** | yes |
| 6 | General Information | yes | yes | **skipped** |
| 7 | Imaging Order Details | only when the imaging question is Yes | no | yes |
| 8 | Referral Partner Lookup | yes | yes | yes |
| 9 | Referral Partner Details | yes | yes | yes |

Pages 1-4 and 8-9 are on all three paths: they sit before the branch point or
after every branch, which is what the forward-only skip-to limit in section 3
requires. Only two pages are ever skipped, one per service, and Imaging Order
Details is the single page whose inclusion depends on an answer rather than on
the service.

**Imaging Order Details serves two branches** and no second imaging page was
needed:

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

The old OPEN QUESTION here - "does Imaging Order (only) also skip Additional
Contact Details?" - is VOID. There is no Additional Contact page to skip; the
additional-contact grids live on Patient Details Cont'd, which every service
sees, and they are governed by field rule 2, not by a page rule.

--------------------------------------------------------------------------------
## 6. Referral Partner Lookup page (page 8)
--------------------------------------------------------------------------------

Naming: **Referral Partner Lookup** is both the name of page 8 and the name of
the grouped dropdown question that sits on it. Where it matters below, "the page"
and "the question" are said explicitly.

Fields:
- Partner POC Email + **Search** button (`.fldSuffixBtn.whookSearchBtn`)
- Referral Partner Lookup, the question (grouped searchable dropdown, ~80 bare
  location names). Replaces the former free-text Partner Branch/Location question
  and the Referral Partner Organization question, both now DELETED. It **should**
  be mapped in the Creator integration to `Partner_Location_Label`; after the
  Session 38 rebuilds it is mapped to `Partner_Organization` instead, which is
  OPEN BUG 1 in section 10.
- Partner Clinical Team
- Referral POC First Name / Last Name / Title
- Referral POC Phone
- Lookup Status (read-only, receives FOUND / NOT_FOUND). Paired with Partner POC
  Email in field rule 10, which hides the Email Lookup Alert until a lookup has
  run.
- Lookup Message (read-only Multi Line, receives the display text)
- Email Lookup Alert (hidden by field rule 10 until both Lookup Status and
  Partner POC Email are non-empty)
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

**HARD LIMITATION: an existing field map cannot be edited.** Any field change
means removing the integration and adding it back, re-selecting every field by
hand. That is why this section carries the map verbatim, and why a mis-selection
is a rebuild rather than a correction.

### The live map, 40 rows
State at Session 38 EOD, 2026-09-01. The map was **deleted and rebuilt twice**
this session; this is the result of the second rebuild and it supersedes the
38-row table filed earlier the same session (kept below as history). The two
added rows are `Patient_MBI` and `Imaging_Body_Site`.

Row numbers below are this file's ordering, kept aligned with the 38-row table so
the diff is readable. They are not a claim about the order of the rows on the
integration screen.

| # | Creator link name | Creator field | Zoho Forms question |
|---|---|---|---|
| 1 | `Referral_Source` | Referral Source | Referral Source |
| 2 | `Referral_Type` | Service | Service Requested |
| 3 | `Patient_First_Name` | Patient First Name | Patient First Name |
| 4 | `Patient_Last_Name` | Patient Last Name | Patient Last Name |
| 5 | `Patient_DOB` | Patient DOB | Patient DOB |
| 6 | `Patient_Gender` | Patient Gender | Biological Sex |
| 7 | `Patient_Hospice_ID` | Patient Hospice ID | Hospice ID |
| 7a | `Patient_MBI` * | Patient MBI | Patient MBI |
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
| 25 | `List_Patient_Anticoagulants` | List Patient Anticoagulants | **List all allergies** - WRONG, see OPEN BUG 2 |
| 26 | `Patient_Has_Advanced_Directives` | Does the patient have Advanced Directives? | Does the patient have Advanced Directives? |
| 27 | `Advanced_Directives_Details` | Advanced Directives Details | Advanced Directives Details |
| 28 | `Additional_Information` | Additional Information | Do you have additional information to share with us? |
| 29 | `Imaging_Type_Order` | Imaging Test(s) to be Ordered | List Imaging test(s) to be Ordered |
| 30 | `Imaging_Order_Indication` | Reason for Imaging Order(s) | Reason for Imaging Order(s) |
| 30a | `Imaging_Body_Site` | Body Part / Affected Area | Body Part / Affected Area |
| 31 | `Partner_POC_First_Name` | Partner POC First Name | Referral POC First Name |
| 32 | `Partner_POC_Last_Name` | Partner POC Last Name | Referral POC Last Name |
| 33 | `Partner_POC_Title` | Partner POC Title | Referral POC Title |
| 34 | `Partner_POC_Team` | Partner POC Team | Partner Clinical Team |
| 35 | `Partner_POC_Phone` | Partner POC Phone | Partner POC Phone |
| 36 | `Partner_POC_Email` | Partner POC Email | Partner POC Email |
| 37 | `Partner_Organization` | Partner Organization | **Referral Partner Lookup** - WRONG, see OPEN BUG 1 |
| 38 | `Form_Token` | Form Token | Form Token |

\* `Patient_MBI` is the expected link name but is NOT confirmed. The field does
not appear in `schema/Referrals_Main.md` as captured 2026-08-31 06:01, which is a
60-field snapshot taken before this field existed.

`diag_form_fields("Referrals_Main")` settles it: it dumps every field on the form
with its link name on demand (context/19). The next scheduled `run_schema_monitor`
run picks it up too, on the 06:00 daily schedule, and rewrites
`schema/Referrals_Main.md`. Either confirms it; the diagnostic just does not
require waiting for the schedule. Do not write Deluge against this link name
until one of them has.

`Imaging_Body_Site` is now MAPPED. The "row to ADD on the pending rebuild" note
that used to sit here is CLOSED: the rebuild happened, and the field was picked up
in it. The rebuild row count to hit is no longer 39.

--------------------------------------------------------------------------------
### OPEN BUG 1 - BLOCKING: Partner Organization mapped in place of Partner Location Label
--------------------------------------------------------------------------------

Row 37. The rebuild selected **Partner Organization** as the target for the
Referral Partner Lookup dropdown. **`Partner_Location_Label` is not mapped at
all** - it moved off the map and into the unmapped list below.

Why it breaks billing. The "Referrals Main On Create - Master" workflow
(Referrals_Main, Created / On Success - see context/19) resolves the billing
branch by reading `Partner_Location_Label` and matching it against Active
`Partner_Locations` by name. That field is now empty on every form-submitted
referral, so no location resolves, `Partner_Branch_Link` is left null, and the
referral lands with **no billing branch**. Everything downstream that keys off
the branch - rate lookup, invoice grouping - has nothing to key off.

Evidence: **REF-1064** shows Partner Organization = "Pasco", which is a location
name, not an organization, and Partner Branch/Location blank. The dropdown is
~80 bare location names (section 6), so writing it into the organization field
puts a location string in an org field and starves the resolver at the same time.

Fix, on the next rebuild: map **Partner Location Label** to the Referral Partner
Lookup question, and **drop Partner Organization from the map entirely**. Creator
derives Partner_Organization in the master workflow, from the resolved location.
It must not be fed from the form.

--------------------------------------------------------------------------------
### OPEN BUG 2 - BLOCKING: List Patient Anticoagulants mapped to the allergies question
--------------------------------------------------------------------------------

Row 25. `List_Patient_Anticoagulants` is mapped to the Forms question **"List all
allergies"** instead of **"List anticoagulant meds"**.

Effect: **the allergy text lands in the anticoagulants field.** The map runs
Forms question -> Creator field, so the answer to "List all allergies" is written
into `List_Patient_Anticoagulants`. Row 23 writes the same answer into
`List_Patient_Allergies`, so the allergy text is duplicated across both fields and
**the anticoagulant answer is not written anywhere**. On any referral submitted
since the rebuild, `List_Patient_Anticoagulants` holds allergies, and the
partner's anticoagulant answer is lost from Creator. It is still retrievable from
Zoho Forms > All Entries (section 11).

Clinically this is the dangerous one of the two bugs: a field labelled
anticoagulants that actually holds allergy text reads as a positive
anticoagulant history that was never entered.

Fix, on the next rebuild: point row 25 at **"List anticoagulant meds"**. Row 23
(`List_Patient_Allergies` <- "List all allergies") is correct and stays.

Both bugs are mis-selections made while re-picking 40 fields by hand, which is
the failure mode the HARD LIMITATION above guarantees. On the next rebuild, check
the map against this table row by row before saving.

--------------------------------------------------------------------------------
### SUPERSEDED: the 38-row map filed earlier in Session 38
--------------------------------------------------------------------------------

Read verbatim off the integration screen on 2026-08-31, before the map was
deleted and rebuilt twice. **This is history, not live state.** It is kept because
it is the only record of what the integration did between the Session 29 build
and the Session 38 rebuilds, and because the two bugs above are visible as a diff
against it: row 37 targeted `Partner_Location_Label` here and now targets
`Partner_Organization`; row 25 targeted "List anticoagulant meds" here and now
targets "List all allergies".

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

### Confirmed NOT mapped, 21 fields
Updated for the 40-row map. `Partner_Organization` left this list (it is now
row 37, wrongly - OPEN BUG 1) and `Partner_Location_Label` joined it (it should
not be here - same bug). The count is unchanged at 21 only because the two
swapped places.

| Creator link name | Creator field |
|---|---|
| `Patient_MI` | Patient MI |
| `Patient_SSN` | Patient SSN |
| `Patient_Full_Address` | Patient Full Address |
| `Prior_POC_Email` | Prior POC Email |
| `Email_Changed` | Has your email changed? |
| `General_Files_Upload` | General Files Upload |
| `Imaging_Orders_Upload` | Upload Imaging Orders |
| `File_Upload_3008` | 3008 File upload (in section `Details_Section_3008`; renamed from `File_upload` / "File upload" on 2026-09-01) |
| `Partner_Link` | Partner Lookup |
| `Partner_Branch_Link` | Partner Branch Lookup |
| `Partner_Location_Label` | Partner Location Label - SHOULD BE MAPPED, OPEN BUG 1 |
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

The three upload fields are unmapped for a platform reason, not an oversight.
Section 11 has the cause and the two ways out.

### Reconciliation
40 mapped + 21 unmapped = **61**, which is the 60 fields in
`schema/Referrals_Main.md` as captured 2026-08-31 plus `Patient_MBI`, added after
that capture. Every field on the form is accounted for.

**The Session 29 figure of 44 mapped / 12 not mapped / 14 removed is RETIRED.**
It was a spec written from the Creator schema and was never verified against the
integration screen. It is not a target for any rebuild and should not be used to
check a rebuild's row count; the number to hit is 40. The Session 29 split is left
out of this section deliberately rather than corrected in place, because two
counts sitting side by side is how it got mistaken for live state in the first
place. The Session 38 figure of 39 is likewise dead: it assumed the 38-row map
plus `Imaging_Body_Site`, and the rebuild landed on 40.

### OPEN: Additional Information is mapped to a Yes/No radio
Row 28, unchanged through both rebuilds. The Creator `Additional_Information`
textarea is mapped to the form's "Do you have additional information to share
with us?" question, which is a Yes/No radio, not a text field. It is therefore
likely storing the literal string "Yes" rather than the partner's note. The real
note text is the field revealed by field rule 11 (section 4), which is a separate
question.

Owner Neil. Open. Not blocking. Needs verification against live records: pull a
referral where the partner answered Yes and check what the textarea actually
holds. If confirmed, the correct source question has to be picked up on the next
rebuild.

The stray "Prior POC Email <- Partner POC Email" integration row (left over from
the dropped Option B email-change design in section 9) was removed and has not
come back in either rebuild.

Gone - must not be re-selected: Requested_Priority, SOS_Prior_Service,
Patient_Responsibility, DM_First_Name, DM_Last_Name, DM_Full_Name,
Decision_Maker_Phone, Decision_Maker_Email,
Decision_Maker_Relationship_to_Patient, Imaging_Files_Upload,
Lab_Type_Orders, Lab_Order_Indication, Requested_Lab_Vendor,
Lab_Files_Upload.

--------------------------------------------------------------------------------
## 11. File uploads do not reach Creator - BLOCKED on a platform limit
--------------------------------------------------------------------------------

None of `General_Files_Upload`, `Imaging_Orders_Upload` or `File_Upload_3008`
appear in the integration's **Creator field dropdown**. They cannot be mapped.
This is not an oversight in the rebuild and it is not fixed by rebuilding again:
the fields are not offered for selection.

`File_Upload_3008` is CONFIRMED, read off the Creator field properties panel:
Field name **"3008 File upload"**, Field link name **`File_Upload_3008`**, inside
section **`Details_Section_3008`**. It was renamed on **2026-09-01**. The
`File_upload` / "File upload" naming in `schema/Referrals_Main.md` as captured
2026-08-31 predates that rename and is stale; the next schema monitor run
replaces it.

### Cause
Creator file fields carry an **Upload Mode** of Single or Multiple. The **Max
file limit** control only exists in Multiple mode, so setting the limit to 1 does
not make a field single-upload - it leaves the field in multi-upload mode with a
limit of one. All three fields are in Multiple mode.

The Forms integration is written against **single-attachment** Creator fields.
Zoho's own documentation states that where a form question carries more than one
file, "only one will be pushed, as Zoho Creator allows only one attachment per
field." A multi-upload field is therefore not a valid target and is filtered out
of the dropdown.

Supporting observation: the Creator meta API reports these three fields as
**Type 46**. Zoho documents File Upload as type **19** and does not document 46
anywhere. File Upload is also **not in Creator's list of convertible field
types**, so a field that is locked into the wrong mode has to be **replaced**,
not converted.

### Next test
Set one of the three fields to **Single Upload** - or, if the mode cannot be
changed on an existing field, add a **new** field explicitly created as Single -
then reopen the integration and recheck whether it now appears in the Creator
field dropdown. That single check decides between the direct fix and the fallback
below.

### Fallback if Single Upload does not unlock the dropdown
Route the files through WorkDrive and pull them into Creator with Deluge:

1. Zoho Forms > **Manage Form Attachments** > store to **Zoho WorkDrive**.
2. Map each upload question to a Creator **Multi Line** field, which receives the
   file URLs rather than the files.
3. An **On Success** Deluge routine fetches each URL with
   `getUrl().toFile()` and writes the result into the real upload field.

Cost: one API call per file. It is the only path that puts the actual file in
Creator if the field type stays unmappable.

### Interim state - retrieval gap, not data loss
Nothing submitted is being lost:
- attachments arrive on the **Zoho Forms notification email**, and
- all entries and their files are retained in **Zoho Forms > All Entries**.

So the files exist and can be retrieved by hand. What is broken is automation
that reads the file off the Creator record.

**It blocks the SendGrid imaging-order email**, which attaches the order document
from the Creator record. With no file on the record there is nothing to attach,
so that email cannot go out on its own. Treat this as blocking for the imaging
order path, and as a manual-retrieval nuisance everywhere else.

Owner Neil. Open.

--------------------------------------------------------------------------------
## 12. Styling and embedding
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
## 13. Open issues
--------------------------------------------------------------------------------

| Item | Status |
|---|---|
| **Integration: Partner Organization mapped to Referral Partner Lookup, Partner Location Label not mapped.** Starves the master workflow's branch resolver; referrals land with no billing branch. Evidence REF-1064. Section 10, OPEN BUG 1. | OPEN - BLOCKING |
| **Integration: List Patient Anticoagulants mapped to "List all allergies".** Allergy text lands in the anticoagulants field and the anticoagulant answer never reaches Creator. Section 10, OPEN BUG 2. | OPEN - BLOCKING |
| **File uploads cannot be mapped at all** - the three upload fields are not in the integration's Creator field dropdown, because they are multi-upload (Type 46) and the integration only accepts single-attachment fields. Section 11. | OPEN - BLOCKING the SendGrid imaging-order email |
| Next test on the uploads: set one field to Single Upload, or add a new field created as Single, then recheck the dropdown. Section 11. | OPEN |
| `Patient_MBI` link name unconfirmed - the field postdates the 2026-08-31 schema capture. `diag_form_fields("Referrals_Main")` settles it on demand; the next scheduled schema monitor run also picks it up. | OPEN |
| Integration rebuild to correct both bugs above. A field map cannot be edited, so this is another full delete and re-add, 40 rows re-selected by hand. | OPEN |
| Lookup messages do not appear reliably on the live form. API response and mapping both verified correct. Suspect the field's Read Only / Hidden setting blocks the prefill write. | OPEN |
| Next diagnostic: log every call inside `get_partner_referral_contact` so a missing message with no log row (Search never fired) can be told apart from a log row with no message (write failed). Needs the Change_Log field link names. | OPEN |
| Additional Information textarea mapped to the Yes/No radio. Row 28, survived both rebuilds. Verify against a live record. | OPEN - not blocking |
| Creator page `Patient_Referrals` embeds the stale form `PatientReferral` | OPEN |
| `Referral_Type` choices on Referrals_Main do not match the form's Service list | OPEN |
| Field rule 7 "Additional Information" is a disabled duplicate of rule 11. Delete it. | OPEN - tidiness |
| Page count is nine, not ten; there is no Additional Contact page | CORRECTED Session 38 EOD, section 2 |
| All 11 field rules recorded | DONE Session 38 EOD, section 4 |
| All 3 page rules recorded, plus the pathway matrix | DONE Session 38 EOD, section 5 |
| Patient Location page rule: 3008 now goes to General Information, not Referral Partner Lookup | CHANGED Session 38, section 5 |
| Imaging Order field rule | BUILT Session 38 |
| Patient Medical Info page rule | BUILT Session 38 |
| General Information page rule: Patient Visit -> skip to Referral Partner Lookup | BUILT Session 38, as Patient Visit AND trigger question Is not Yes |
| Does Imaging Order skip Additional Contact Details? | VOID - no such page, section 5 |
| `Imaging_Body_Site` reaches Creator | CLOSED Session 38 EOD - mapped in the 40-row rebuild |
| 38-row live map not captured in this repo | CLOSED Session 38 - filed in section 10, now SUPERSEDED by the 40-row map |
| Session 29 count of 44 mapped; Session 38 rebuild target of 39 rows | BOTH RETIRED - the live count is 40 |
