# SOS Code Checkpoint, 2026-09-17, Session 48

Mid-session checkpoint. Covers work since the Session 47 checkpoint
(context/handoff/SOS_Code_Checkpoint_2026-09-16_Session47.md).

--------------------------------------------------------------------------------
## 1. HIPAAtizer capability limits, verified empirically
--------------------------------------------------------------------------------

Items 1 through 6 were tested against the live PVS form embedded at
sosreferrals.com/new-referral-2 and against the HIPAAtizer renderer script
itself. Item 7 is admin console configuration read from vendor documentation.
Item 8 is read from the vendor's published API collection. The distinction
matters: a measurement rules something out, a published collection only shows
what the vendor chose to document.

1. The form always renders inside a cross-origin iframe on app.hipaatizer.com.
   The WordPress plugin does this, and the JavaScript embed does the same: the
   renderer writes an iframe and communicates by postMessage. No JavaScript on
   the host page can read or write any field inside the form.

2. The Hipaatizer constructor takes five arguments (workflowId,
   isStartMultiWorkflow, whiteLabelUrl, isAdvancedWorkflow, isFormPage). None
   of them accept field values.

3. postMessage traffic is limited to payment state and iframe height. There is
   no documented or observable channel for injecting field data.

4. The embed script passes parent page query parameters into the iframe as an
   initialValues payload at render time, alongside the hptz_* parent page
   variables. Tested with two parameters at once (utm_source and an invented
   name), both of which arrived, so it is not an allow-list of known keys. A
   parameter named after a field unique name prefills that field.

5. Prefill happens at render, not at submit. Passing ?input_4ec5=ZZTEST123
   visibly filled the Referral ID Lookup box on screen.

6. A radio group does not prefill. Passing the Has Referral ID radio its real
   stored value ("yes") did not select it; also tested "Yes", "Y", and "1".
   TESTED: one radio group, one text input. NOT TESTED: dropdown select,
   checkbox, multi-select, date, phone, currency, signature. Treat the general
   claim "choice fields do not prefill" as a working assumption until the form
   carrying those field types is published and tested.

7. Post-submission options are Display Success Page or Redirect, per vendor
   documentation. Redirect is a single static URL per form with no documented
   branching on an answer. Not independently tested.

8. The HIPAAtizer REST API appears read-only for this purpose. Their published
   Postman collection (github.com/HIPAAtizer/api-docs) contains 20 endpoints
   covering appointments, submissions, locations, services, and workers, with
   no create-submission, no draft, no prefill, and no field-write endpoint.
   Their documentation describes webhooks as outbound only, firing on
   submission, update, deletion, or draft save. This is absence from a
   published collection, not proof no such endpoint exists. Ask their support
   directly before treating it as final.

CONSEQUENCE: the in-form referral type-ahead is not buildable. Any lookup,
identity check, or PIN gate has to live on the page hosting the form, and the
only inbound channel to the form is parent-page URL parameters landing in text
inputs.

--------------------------------------------------------------------------------
## 2. Provider access architecture, decided
--------------------------------------------------------------------------------

Decision: keep HIPAAtizer. The only capability lost is the in-form lookup, and
that moves to a page that has to exist anyway.

Flow:

1. Each provider gets a personal PVS URL carrying a signed token. No login.
2. That page reads the token, resolves it through a Catalyst endpoint to one
   provider, and renders that provider's queue.
3. A 4-digit PIN gates the queue, so a forwarded link alone is not enough.
   The URL is a bearer credential without it.
4. The provider taps a referral.
5. The page re-renders the HIPAAtizer embed with the token and the patient
   confirmation values appended as query parameters, which prefill as text.
6. On submit the webhook posts to the Creator Custom API, which validates the
   token, re-reads the referral from Creator, rejects on mismatch or reuse,
   and writes the PVS.

Noted risk: patient confirmation values travel in the parent page URL and into
the iframe src.

Service Type becomes question 1 on the form, a Single Choice radio the provider
actually clicks (Patient Visit = visit, 3008 = 3008, Imaging Order = imaging),
CSS class radio-buttons2. It drives Display/Hide on the Clinical Note, Visit
Detail, Charges, Diversion, 3008, and Imaging Order rows. Type_of_Entry comes
from that field, and the Custom API rejects a submission that disagrees with
the referral's service.

--------------------------------------------------------------------------------
## 3. Assignment model, decided
--------------------------------------------------------------------------------

1. The provider queue is assignment-only. Every provider sees only what Josh
   assigned to them. Notifications go to Neil and Josh only; no provider knows
   a referral exists until Josh assigns it.
2. 3008 assessments are additionally private between providers. Kayla and Ann
   must never see each other's 3008s, in any state. Enforced in the Catalyst
   endpoint, not hidden in the page.
3. Because assignment now gates the whole PVS flow, an unassigned referral is
   invisible to every provider by design, so assignment reliability is load
   bearing.
4. New field on Referrals_Main: Assignment_Status. Dropdown. Values: Received
   (default), Patient Contacted, Visit Scheduled, Waiting on Equipment,
   Pending Results, Visit Completed. Stamped Received on referral add.
5. Assignments.Visit_Status is retired. One status field, one editing surface.
   Status is changed from the Referrals report with a button, not from the
   Assignments form. No cross-form writes and no sync workflow.
6. Reassignment and status changes log to the existing Change_Log form, which
   already carries Source_Form, Source_Record_ID, Source_Display_ID,
   Field_Changed, Old_Value, New_Value, and Changed_By. No new form needed.

--------------------------------------------------------------------------------
## 4. Partner confirmation notification
--------------------------------------------------------------------------------

New function build_referral_confirmation_html(int p_recId) written. It is a
trimmed sibling of build_referral_email_html, same styling, sent only to the
submitting Partner POC on referral submission. No CC, no internal copy.

Fields kept: Referral ID, Date Received (Referral_Date), Service Requested
(Referral_Type), Submitted By (Partner_POC_Name_Title), Patient Name
(Patient_Full_Name). Clinical Team (Partner_POC_Team) and Referral Status
(Assignment_Status) to be added once the field exists.

Everything else is dropped, including DOB, gender, location, address, facility
block, patient phone, hospice ID, additional contact, reason for referral,
allergies, anticoagulants, advanced directives, imaging block, attachments,
partner block, branch, POC phone and email. Patient name stays out of the
subject line; the subject carries the Referral ID only.

The send workflow is not built yet.

--------------------------------------------------------------------------------
## 5. Defects found and fixed
--------------------------------------------------------------------------------

### 5a. Reason for Referral required on hidden sections

PVS_Required_Fields (Encounter_PatientVisit, On Add or Edit, On Validate) had
Reason_for_Referral in the always-required block with no Type_of_Entry gate.
Reason_for_Referral lives in Referral_Details_Section, which
Entry_Type_Section_Visibi hides for 3008, Lab Order, Imaging Order, and Clinic
Hours. A 3008 therefore blocked on a field the provider could not see.

Fix applied: PVS_Required_Fields now stamps Reason_for_Referral with
"3008 Assessment" when Type_of_Entry is 3008 and the field is blank, before the
required check runs. Stamping in On Validate rather than On User Input means it
works regardless of how Type_of_Entry was set.

STILL OPEN: Lab Order, Imaging Order, and Clinic Hours hide the same section
and remain exposed to the same rule. ccode found a fifth exposed path in the
repo copy of OnUserInput__Type_of_Entry__Section_Visibility.dg: the trailing
else branch also hides Referral_Details_Section, so any unmatched Type_of_Entry
value hits it too. Neil has not yet said what should print for any of them.

### 5b. Referral_Sets_Billing_Bra hardening

The workflow read fields straight off a fetch result with no existence check,
so a dangling Referral_Link wrote blanks silently. Rewritten with an ID guard,
an alert on a missing referral, and Partner_Location_Label added to the copied
set.

Separately noted: both Referral_Sets_Billing_Bra and Sender_Sets_Branch are On
User Input, so neither fires on an API write. The Custom API has to set
Billing_Branch itself.

### 5c. PVS records never linked to their referral

relink_pvs_to_referral(p_mode) written and run. It finds
Encounter_PatientVisit rows where Referral_Link is null but the Referral_ID
text is populated, matches Referrals_Main by that ID, and fills only blank
fields. Nothing existing is overwritten. Patient_Address is deliberately not
touched.

Result: 7 candidates, 5 matched and committed, 2 unmatched.

Committed: PVS-1308-NH (link only), PVS-1490-JK, PVS-1502-JK, PVS-1503-JK,
PVS-1506-JK (link plus reason, patient name, billing branch, partner branch,
partner organization).

Unmatched and still open: PVS-1227-JK points at REF-1045 and PVS-1367-JK points
at REF-1247. Neither referral exists in Referrals_Main.

--------------------------------------------------------------------------------
## 6. Data verification run
--------------------------------------------------------------------------------

1. DOB pipeline documented: the Zoho Form captures DOB as a TEXT field with a
   dd/dd/dddd mask because a date-to-date mapping failed on field type
   mismatch. It maps to Patient_DOB1, and a workflow parses that into
   Patient_DOB. Patient_DOB is the field that counts. A blank Patient_DOB1 is
   not a gap; a populated Patient_DOB1 with an empty Patient_DOB means the
   parse failed.

2. New function resync_patient_dob(p_mode) written: re-derives Patient_DOB from
   Patient_DOB1 on every record carrying DOB text, regardless of whether a date
   already exists. This exists because the parse workflow is On User Input and
   only fires when a record is opened and saved in the UI.
   PREVIEW result: 704 records, 419 with DOB text, 0 changed, 418 unchanged,
   1 unparseable (REF-1111, since corrected).

3. Future-dated DOBs: 104 records carry a Patient DOB between 2028 and 2045.
   All 104 are Cognito-style referral IDs and all 104 are July 2026 referrals.
   Verified against the Cognito export: for every row that appears in both,
   month and day match exactly and only the century differs, 19xx in the
   source against 20xx in Creator.
   The August conversion files in this repo are clean (306 rows, zero future
   DOBs), so the flip came from an earlier load.
   Neil's call: out of scope, July referrals do not matter. CLOSED.

4. Duplicate Referral IDs: diag_duplicate_referral_ids returned 706 referrals,
   705 distinct IDs, zero held by more than one record. The old four-day
   mapping defect is fully repaired.

5. One referral had a blank Referral_ID (record 4904890000000584020, service
   3008, InnovAge POC). Its Form_Token was 0005326081, a raw number rather
   than a REF value, so backfill_referral_id_from_token would have written
   garbage. Minted with mint_referral_id instead. CLOSED.

6. 3008 Reason for Referral audit: 76 3008 entries, zero with a blank reason.
   All inherit a real reason from the referral, mostly PACE enrollment
   language. The four blank-reason PVS records were all Patient Visit type and
   are covered in 5c.

--------------------------------------------------------------------------------
## 7. Platform exploration, reference only
--------------------------------------------------------------------------------

Neil scoped what a rebuild outside Zoho would look like, for a conversation
with a prospective developer. Captured here because it will come back.

BAA availability, verified at source:
- AWS: self-serve BAA accepted in AWS Artifact, no extra cost, covers the
  HIPAA-eligible service list.
- Azure: BAA included in Microsoft Product Terms.
- Google Cloud: BAA executed through an account manager, and it is SEPARATE
  from the Google Workspace BAA. The existing SOS Workspace BAA covers
  Workspace and Cloud Identity only, not GCP.

Platforms with a database and backend GUI plus a BAA path: Supabase, Xano
(BAA after registering the HIPAA add-on), Aptible, Caspio HIPAA Edition, Knack,
Backendless, Firebase under the Google Cloud BAA, Nhost, Appwrite Cloud,
Directus Cloud, Budibase, Retool. Medplum is the healthcare-native option: open
source FHIR backend, admin GUI, signs a BAA.

No pricing or plan tier in this section is confirmed. Every one needs
verification with the vendor before it is quoted to anyone.

On self-managing HIPAA compliance: setup is one time, roughly 40 to 80 hours,
but passing an audit depends on the recurring evidence trail, which does not
automate. AWS Config, CloudTrail, GuardDuty, Security Hub, and Audit Manager
generate the technical evidence. The risk analysis, policies, training records,
access reviews, and proof of acting on findings stay manual.

--------------------------------------------------------------------------------
## 8. Repo and tooling note
--------------------------------------------------------------------------------

The local sos-emr repo is now directly readable and writable from the chat
session at /Users/neilheird/Claude/GitHub/sos-emr. Push is not possible from that
shell: the remote is SSH (git@github.com:m1ndspark/sos-emr.git) and it has no
key, so git ls-remote fails on host key verification. ccode's environment
pushes normally; this limit is specific to the chat session's shell.

Division of labor going forward: chat writes and edits repo files directly,
ccode runs the sos-precommit-audit subagent and performs the commit and push.

.ds v49 was provided in chat on 2026-09-17 and has NOT yet been written into
the repo. The repo is still at v47. v49 carries 37 forms, 86 workflows, and
140 functions.

--------------------------------------------------------------------------------
## 9. Open contradictions raised by the Session 48 audit
--------------------------------------------------------------------------------

Raised by ccode against this checkpoint. Item 2 is resolved; the rest are not.

1. Retiring Assignments.Visit_Status silently drops three values. The live
   field carries nine choices; the proposed Assignment_Status carries six.
   Ordered, Report Sent, and Pending Info have no home in the new list.
2. Record counts disagree within this document. Section 6.2 reports 704 and
   section 6.4 reports 706. Both count the same form: resync_patient_dob loops
   Referrals_Main[ID != 0] and so does diag_duplicate_referral_ids. The
   two-record gap is the order the functions were run, with referrals created
   during the session in between, including the minted blank-ID record.
   Section 6.2's wording implies PVS records and is wrong.
3. Assignment_Status target form is ambiguous. Section 3.4 puts it on
   Referrals_Main while Referrals_Main2 is mid-build as its replacement.
4. Type coverage gap. Type_of_Entry carries five values and the new Service
   Type radio carries three, so Lab Order and Clinic Hours cannot come through
   the HIPAAtizer form at all.
5. The webhook payload capture and body rewrite are not recorded in any
   checkpoint. The Session 47 checkpoint records the INSTRUCTION to capture a
   payload and lists it as blocking; the capture and the rewrite were executed
   after that checkpoint was written and before this one, and neither document
   records the completion. Session 47 is the pointer for the plan, not for the
   result: context/handoff/SOS_Code_Checkpoint_2026-09-16_Session47.md.
6. Pre-existing and separate from this change set: context/34_august_backfill
   _open_items.md carries patient names, committed 2026-09-14, after the no-PHI
   rule was added. Needs its own scrub.
7. HIPAAtizer PVS webhook destination. A webhook.site placeholder was set in
   Session 47 to capture the payload, using junk data only. webhook.site is a
   public inspection endpoint readable by anyone holding the URL and carries no
   BAA, so a real submission against it would have been an exposure. Neil
   checked the HIPAAtizer console on 2026-09-17: the destination field is now
   BLANK. No PHI can leave the form. Consequence of blank: the form is live at
   sosreferrals.com/new-referral-2 and a provider submission would be stored in
   HIPAAtizer and reach Creator not at all. The destination must be set to the
   live Creator Custom API URL before go-live, and must never be set back to a
   public inspection endpoint once real data can reach the form.

END
