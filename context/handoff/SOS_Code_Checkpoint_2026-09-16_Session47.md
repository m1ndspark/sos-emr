# SOS Code - Checkpoint - 2026-09-16 - Session 47

## Scope of this session
Front end replacement for the Creator PVS and referral forms, and the field
design for a rebuilt referral form. No Deluge written yet. No workflows built.

--------------------------------------------------------------------------------
## 1. Decision: form builder
--------------------------------------------------------------------------------
HIPAAtizer, Simple Compliance Gold Plus, 39/mo annual or 45/mo monthly.
10 published forms, 10 team members, 1000 submissions/mo, 5GB.
API and webhooks included. BAA listed on the Gold tier, needs confirming on
Gold Plus before purchase. Currently on a free trial, 29 days remaining.

Evaluated and rejected: Jotform Gold (129/mo monthly, webhooks allowed on HIPAA
accounts but no Zoho Flow connector), Cognito Forms Enterprise (129/mo annual,
dated design), 123FormBuilder (HIPAA is Enterprise at 225/mo), Formstack
(Enterprise, sales only), FormAssembly (about 20k/yr), Formsort (sales only),
Zoho Forms Premium (110/mo, no custom CSS, no On Load, no session awareness),
Google Forms (covered by the Workspace BAA, no styling control at all).

HIPAAtizer capability notes, confirmed from their docs:
  Custom CSS editor, visual theme editor, Style Grabber
  Script embed renders into the page DOM, iframe embed also available
  Webhooks with a custom JSON body and an HMAC HIPAA-Signature header
  REST API authenticated by X-Api-Key with server IP whitelisting
  API covers submissions, appointments, locations, services, workers
  API does NOT create or edit form definitions
  Conditional logic: only Dropdown, Single Choice, Multiple Choice and Checkbox
    can trigger; only Display and Hide actions; equals, does not equal,
    contains, does not contain; AND or OR within one row; no nesting;
    no conditional required and no set value
  Logic attaches to a row, not a field

--------------------------------------------------------------------------------
## 2. Architecture decided
--------------------------------------------------------------------------------
Provider opens the visit list in Creator, authenticated, and sees the patient
block there. A button opens the HIPAAtizer PVS carrying only a signed token.
The form collects provider input only. On submit HIPAAtizer fires its webhook
into a Creator Custom API, which resolves the referral, merges patient and
partner data server side, and writes the record so OnValidate and every On
Success workflow fire normally.

Security requirements established:
  Signed, single use, short expiry token carrying referral plus provider
  Provider identity comes from inside the token, never a form field
  The Custom API rejects expired, reused or unsigned tokens
  A second identifier on the form, Referral ID plus patient last name, so a
    mistyped ID fails at the door instead of landing on another chart
  No PHI in any URL query string

Known fragile joint, accepted as a bridge to the v2 platform rebuild: the
referral type ahead depends on JavaScript reaching HIPAAtizer's rendered DOM.
Mitigations agreed: all validation server side, and the front end fails loudly
rather than silently.

--------------------------------------------------------------------------------
## 3. PVS form - BUILT
--------------------------------------------------------------------------------
Form exists in HIPAAtizer, named PVS Entry, id 01a0a72d-4b46-7266-9b18-e5244b99dc09.
Embedded at sosreferrals.com/new-referral-2 via WordPress shortcode.
Whole form now fits one screen, which was the original complaint from Josh.

Provider visible set, 34 fields across 9 sections. Everything else is hidden
and merged server side. Build sheet delivered as
SOS_PVS_HIPAAtizer_Build_Sheet_2026-09-15.xlsx.

Field rulings made this session:
  Visit Status hidden, Complexity Level "Visit Cancelled" owns cancellation
  Type of Entry derived from the referral Service, never shown
  Patient first, MI, last hidden; Patient Full Name shown read only
  Patient_DOB1 dropped; the date field only
  Patient SSN shown on 3008 only
  Patient Location, Patient Address and all Facility fields hidden
  Goals of Care, Reason for Referral, Partner ICD Codes, Allergies hidden
  Advanced Directives hidden when the referral value is blank
  Additional Information kept, blank when the referral has no value
  Anticoagulants kept, optional, no procedure gating
  Employee Initials and Employee Email hidden, prefilled from the token
  Visit Completion Date visible to the provider
  Equipment Charge Amount and Equipment Charge Details both visible
  Every other dollar field hidden, no prices on option labels
  Other Charges Amount and Details hidden
  Invoice Connection and Hold From Invoicing removed from the form
  Lab Orders section deleted
  Has Referral ID gate kept
  All file uploads consolidated into one area

CSS is complete and live. Figtree body, Libre Franklin headings, both imported
from Google Fonts. Navy pills, 40px circular radio buttons at 15px bold,
44px on mobile, green 02cd3b selected state, green checkboxes, green submit
turning red on hover, green focus glow on inputs and the Ant Select dropdown.

CSS lessons worth keeping:
  HIPAAtizer renders Ant Design, so every selector targets Ant internals
  The Ant radio label text sits two spans deep
  span.ant-radio-button is absolutely positioned over the whole label and
    paints its own background, which is what caused navy bleeding around green
  Ant hard sets height 32px and line-height 30px on radio wrappers
  The radio group is a CSS grid with inline grid-template-columns
  Ant Select is div.ant-select-selector, not .ant-input, and HIPAAtizer's own
    focus rule outranks anything without matching specificity

--------------------------------------------------------------------------------
## 4. Referrals_Main2 - FIELD DESIGN COMPLETE, BUILD IN PROGRESS
--------------------------------------------------------------------------------
New Creator form. Neil started building it in the Creator builder this session.
Design sheet delivered as SOS_Referrals_Main2_Field_Design_2026-09-16.xlsx with
a second tab listing every dropped field and why.

52 fields, down from 69 on Referrals_Main. 12 written by the system. Zero
fields require manual input or modification after a referral is submitted.

Eight sections: Submission Routing, Referring Partner, Patient Identity,
Patient Location, Clinical Context, Imaging Order, Attachments, System and
Identifiers.

Structural decisions:
  Two IDs only. Referral_ID is the single minted identifier. Submission_Token
    is an idempotency key so a webhook retry cannot double create.
  All stamp fields dropped. One mint function keyed to record creation.
  One Lookup replaces the Partner and Branch pair: Partner_Branch_Link points
    at Partner_Locations, displays Partner_Location_Label, filtered to
    Partner_Loc Status equals Active, alphabetical, search enabled.
  Partner_Link, Partner_Organization and Partner_Branch are written by an
    On Success workflow from the selected location. Nobody types them.
  No concatenation fields. Full name, full address and POC name with title are
    built at output, not stored.
  One DOB field. One attachment upload field. One attachment URL field.
  Employee_Link removed from this form. Assignment lives on Assignments.
  Row_Status and Duplicate_Of_Referral_ID added, both written automatically by
    a duplicate check on create, never typed.

Dropped from v1: Patient_DOB1, Patient_Full_Address, Patient_Full_Name,
AC_Full_Name, Partner_POC_Name_Title, Referral_Date1, Referral_ID_Stamp,
Partner_ID_Stamp, Partner_ID, Partner_Location_Label, Partner_Branch_Submitted,
Cognito_Referral_ID, Referral_Added_Time, Files_3008_URLs, General_Files_URLs,
Imaging_Orders_URLs, File_Upload_3008, Imaging_Orders_Upload,
General_Files_Upload, Form_Token, Employee_Link.

Automatic duplicate detection is now a launch requirement, since nothing else
catches what was hand flagged all through August.

--------------------------------------------------------------------------------
## 5. Partner email lookup - DESIGNED, NOT BUILT
--------------------------------------------------------------------------------
For the public referral form. Partner types their email, leaves the field, and
sees their name and branch confirmed before submitting.

Eleven states, each with its own message, no state without an explanation:
idle, invalid format, checking, recognized, recognized with branch missing,
not on file, offline, timed out, server error, rate limited, not initialized.
Green for recognized, amber for the three partial states, red for the five
failure states. Every failure message says what went wrong and that the
referral still works.

Partner_POC_Email is declared unique on Partner_Referral_Contacts, so a
multiple match state cannot occur.

Function designed but not written:
  api_partner_contact_lookup, New, Deluge, default namespace,
  returns String JSON, takes string p_email
  Returns first name, last name, title, team, organization and branch label
  Never returns phone, Partner_ID, Partner_Link or any record ID
  Wrapped so any failure returns status error rather than a stack trace

Open judgement recorded: a per branch form link would delete this whole feature,
since the branch would be baked into the URL and the lookup would have nothing
left to resolve. Not chosen. Neil wants the visual confirmation.

--------------------------------------------------------------------------------
## 6. Open items
--------------------------------------------------------------------------------
BLOCKING for the PVS launch:
  Sample HIPAAtizer webhook payload needed. Point the PVS webhook at
    webhook.site, submit once with junk data, and send the JSON. The Creator
    Custom API cannot be written against guessed field names.

Needed before purchase:
  Confirm the BAA is included on Simple Compliance Gold Plus, not just Gold.

Needed before the referral form is finalized:
  Confirm whether Referral_Source carries two values or three. v47 shows
    Contracted Partner and SOS Internal. The MPU rule written on 09-14 says
    Direct/Individual was added.

Carried from Session 46, still open:
  Push commits d8bd786, 1476c79, 629554a, 55aea38
  The August PVS import itself
  backfill_pvs_repair PREVIEW has never been run
  REF-1357 and REF-1237 partner assignments are wrong
  Bennie Benjamin travel charge has no field and no rate
  Ronaldo Martinez False Patient should leave the counts
  86 August referrals have an organization but no branch
  25 fields missing from the PVS report including Clinical Note and all charges
  backfill_mint_missing_referral_ids still needs the SKIP-NOSCOPE retrofit
  The four other mint functions still carry the bare assignment defect
  PVS-1227-JK is Draft and unheld since the INV-000028 void
  15 August PVS rows carry something other than a real hospice ID

--------------------------------------------------------------------------------
## 7. Next session
--------------------------------------------------------------------------------
Complete the PVS integration and take it live. Order of work:
  1. Read the sample webhook payload
  2. Write the Creator Custom API receiver
  3. Write the token mint function on the Creator side
  4. Build the provider launch button on the Creator visit list
  5. Test end to end against a throwaway referral
  6. Go live

END
