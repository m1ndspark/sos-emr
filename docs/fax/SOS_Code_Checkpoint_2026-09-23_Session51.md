# SOS Code - CHECKPOINT 2026-09-23 (Session 51)

Fax console server side built and proven end to end. No UI yet.

## Built and verified

- New form `Fax_Attachments`: `Fax_Log` (lookup to Fax_Log), `Attachment_Type`
  (PVS Note / Upload), `Attachment_Name`, `Attachment_File`, `Source_PVS_Link`
  (lookup to Encounter_PatientVisit), `Sequence_Number`.
- New functions, all Deluge, default namespace, return Map:
  - `api_fax_recipients()` - active Partner_Billing_Contacts carrying a
    Partner_PVS_Fax. Returns 16.
  - `api_fax_pvs_search(p_branchId, p_query, p_unsentOnly)` - Patient Visit
    notes, Final or Addendum, optional unfaxed filter, capped at 200.
  - `api_fax_begin()` - creates a Building draft Fax_Log row, returns log_id.
  - `build_console_docs(...)` - cover HTML with numbered enclosure manifest,
    plus one complete HTML document per selected note.
  - `api_fax_send_console(pLogId, pContactId, pPvsIds, pRemarks)` - mints the
    Fax ID, converts cover and every note to its own PDF, writes a
    Fax_Attachments row per note, posts one multipart fax, stamps each PVS.
- `Fax_Attachments_Report` list report.
- Canvas custom layout on the Fax Log detail view carrying a related block for
  Fax Attachments, so every note faxed is downloadable from the fax record.

## Live test

FAX-092326-1009 to Empath - Tidewell, two Patient Visit notes, Page Count 5
returned by RingCentral, two Fax_Attachments rows written, both PDFs
downloadable from the fax record. Cover carried the custom message and the
numbered enclosure list.

## PVS required-field guards removed

All four On Validate guards on `Encounter_PatientVisit` are out, per Neil.

- `PVS Required Fields` rewritten: alert and cancel submit stripped, the 3008
  Reason default and the Patient_DOB1 text parse kept.
- `Billing Branch Required`, `Complexity Charge Required` and
  `Validate Complexity On Final` disabled, not deleted.

Verified against v52: no field on Encounter_PatientVisit carries a native
mandatory flag, so every required check on that form was Deluge.

## Decisions taken

- Console recipients come from `Partner_Billing_Contacts`, not
  `Fax_Address_Book`. Address book stays empty and unused.
- `Fax_Attachments` is a related child form, not a subform. Zoho documents
  subform inserts only in form context; `insert into` is the proven pattern.
- Cap of 10 notes per fax. Neil's reason: more than that overflows or ties up
  the recipient machine while it prints.
- Local file uploads deferred to phase 2. Notes-only v1.
- Fax ID minting now verifies uniqueness and re-mints, up to five attempts.
- Portal UI will be a Creator Widget. Node and the zet CLI run in Claude's
  cloud workspace; Neil never installs Node.
- InnoVage needs no fax path at all. Completed 3008 PDFs go back by email via
  PDF Filler. The blank Partner_PVS_Fax on those rows is by design.

## Findings

- RingCentral fax limits: 50 MB combined, 200 pages, and filenames must not
  contain ampersands or other special characters. Filenames are sanitised.
- Deluge `getFileContent()` explicitly does not work on files fetched from
  Creator fields, and the `.content` attribute returns text only. There is no
  documented route from a Creator file field into an invokeurl multipart part.
  The Creator v2.1 download endpoint plus a ZohoCreator.report.READ connection
  is the untested candidate.
- Microservices and Custom APIs are active on this plan.
- A widget calls Deluge through `ZOHO.CREATOR.DATA.invokeCustomApi()`, which
  requires the function to be exposed as a Custom API.
- Related Blocks appear only in the Canvas layout editor, not the plain report
  field list.
- One branch alone had 100 unfaxed Final notes at the time of this checkpoint.

## Open

- Expose the three api_ functions as Custom APIs, then build and pack the
  widget.
- `Sent_By` resolved to the wrong employee on a fax Neil sent. Either the
  Creator login in use or an Employee_Email value is wrong. Audit trail issue.
- `retry_failed_faxes` marks any row without a `PVS_Link` as Permanent Fail, so
  a failed console fax never retries.
- The Fax Attachments related block exposes an add-record control. The setting
  that disables it was not found in Report Customization; it sits on the block
  inside Canvas.
- How required PVS fields get marked visually now that nothing enforces them.
- `&mdash;` entity still present in four email template functions.

---

# PART 2 - after the checkpoint (same session, 2026-09-23)

The checkpoint above was written mid-session. Everything below happened
after it. See the EOD log for the full narrative.

## Fax from the PVS form - BUILT and working

Josh asked whether a PVS could fax on submit. Auto-fax on save was
rejected because On Success cannot raise an alert. NEIL RULING: a
tickbox during entry, preview, submit, then fax.

Creator does not allow a Deluge button on a stateful form, so the whole
path runs on decision boxes and on-user-input events.

New fields on `Encounter_PatientVisit`, in a Fax Preview Section:
`Print_Preview` (rich text), `Fax_This_Note`, `Fax_Override_Unlock`,
`Fax_Override_Number`, `Fax_Override_Reason`.

New functions:
- `build_pvs_note_html(map pVals)` - the note template fed by a value
  map rather than a record, so one template serves both the on-screen
  preview and the saved-record path.
- `resolve_pvs_fax_target(int pPvsID)` - single source of the
  destination and the gate.
- `fmt_referral_source(string pOrg, string pBranch)` - returns the
  longer label when one contains the other.

New workflows on `Encounter_PatientVisit`:
- `Fax This Note Preview And Gate` (on user input of `Fax_This_Note`)
- `Fax Override Number Format` (on user input of `Fax_Override_Number`)
- `Fax This Note On Submit` (on success)

`PVS Fax Review On Load` now pulls its gate from
`resolve_pvs_fax_target`. `build_pvs_fax_html` now loads the logo from
https://sosreferrals.com/... instead of 20 KB of base64.

Live test: a real PVS was faxed to a real partner from the PVS edit
page, and the override path was tested separately with a manually
entered number.

## Creator learnings from this half

- An on-user-input workflow that writes back to its own trigger field
  loops forever and hangs the form with NO error. `Fax Override Number
  Format` did this. Compare and only assign when the value changes.
- "Click of a button" is a STATELESS-FORM-ONLY event. A stateful form
  cannot run Deluge from a button.
- `alert` works in on load, on validate and on user input. NOT in on
  success. Anything needing an on-screen result must be checked at tick
  time, not at send time.
- A complete HTML document, style block included, survives being
  written into a Creator rich text field and renders styled.
- A logo loads fine from a public HTTPS URL inside `convertToPDF`.

## Data finding

`Referral_Sets_Billing_Branch` fires ONLY on user input of
`Referral_Link`. A PVS that gets its referral any other way never
receives a `Billing_Branch`. It copies `Partner_Branch_Link` straight
from the referral, so a referral missing that link yields a null branch
silently. The only thing that caught a null branch was `Billing Branch
Required`, disabled today, and even that only fired when
`Has_Referral_ID` was "No". No backstop at any link in the chain.

The same workflow copies `Partner_Organization` and `Partner_Branch` as
separate strings, which is the doubled Referral Source on the cover.
The Zoho intake form populates those two inconsistently between
submissions, which is the upstream cause.

## Sent_By - RESOLVED

Not a defect. Neil is signed into Creator under Josh's profile.
App-wide consequence: every `Added_User`, `Modified_User` and `Sent_By`
stamped during such a session attributes to Josh.

## Added to open

- `diag_fax_readiness(int p_days)` was written and handed over but
  never run. Read-only. Reports unfaxed Final and Addendum notes
  grouped by why they cannot fax, plus referrals missing
  `Partner_Branch_Link`.
- `fmt_referral_source` is only wired into the PVS form preview.
  `build_pvs_fax_html` and `build_console_docs` still build the source
  line the old way, so faxes still carry the doubled label.
- `Partner_POC_Name_Title` contains an email address on at least one
  referral and prints on the fax.
