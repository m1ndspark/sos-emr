# SOS Fax - Console and Bulk Send Design Spec

Scoped 2026-09-23 (Session 51). Nothing built. This is the requirements
record for the SECOND and THIRD ways to send faxes from the app,
alongside the per-row Fax PVS button delivered in Session 50.

Sections 1 to 8 cover option 2, the fax console. Section 9 covers
option 3, bulk send from `PVS_Report`.

> **Status 2026-09-23 (end of Session 51):** the console is BUILT server side
> (section 11 supersedes four decisions in sections 1 to 8), and the PVS-form
> fax path is BUILT (section 12, see 12.5 for how it actually shipped). Sections
> 1 to 10 are kept as the original scope record.

Read `SOS_PVS_Fax_System_Design.md` first. That covers the single-visit
path, the RingCentral plumbing, the poll and retry schedules, and the
Creator and Deluge findings this build relies on.

---

## 1. The problem

The Session 50 path faxes one visit at a time from `PVS_Report`. A staff
member with ten Tidewell notes to send has to fax ten times. They also
have no way to fax anything that is not a PVS note, and no way to write a
message on the cover.

## 2. What it is

A general outbound fax tool, modelled on the RingCentral app: pick a
recipient, attach whatever you want, write a message, send. It is not a
clinical-note workflow and it does not gate on whether a note has been
faxed before. Anything can be sent, any number of times.

## 3. Target shape

1. User opens the console and picks a recipient from `Fax_Address_Book`.
2. Destination name and fax number fill from the recipient record.
3. User ticks any number of PVS notes to include.
4. User attaches any number of files.
5. User types a custom cover message.
6. One cover sheet is generated listing every enclosed item.
7. Each selected note is rendered and converted into its OWN PDF.
8. The cover, every note PDF and every uploaded file post to RingCentral
   as separate multipart attachments in a single fax.
9. One `Fax_Log` row is written, carrying a manifest of everything sent.
10. Every PVS note included is stamped `Fax_Status = Sent`.
11. The existing poll and retry schedules handle it with no change.

## 4. Decisions taken

- **Recipients come from `Fax_Address_Book` in Creator.** Not RingCentral.
  The RC Address Book API exists but the app's live scopes are
  `ReadMessages`, `Faxes` and `ReadCallLog`, so reading contacts would need
  new scopes and a re-mint. An RC sync can be added later; nothing blocks
  on it.
- **The console can send anything**, including files with no PVS at all.
- **No gating on prior sends.** A note can go out as many times as the
  user wants.
- **Uploaded files are archived.** `Fax_Log` keeps the generated PDF plus
  a copy of every uploaded file that went with it, preserving the Session
  34 principle that the archive matches what was sent.
- **`Fax_Log` structure does NOT change beyond a manifest field.** No child
  form, no multi-select of PVS records. `PVS_Link` stays as it is and is
  simply empty for console faxes. The manifest field records the complete
  contents of the envelope, which is the send history.
- **Sending a note through the console stamps that PVS `Fax_Status = Sent`**,
  so the 4am digest does not keep reporting it as an unfaxed miss.
- **The console does NOT replace the per-row Fax PVS button.** Two paths,
  both supported.
- **Selection happens on the console, after the recipient is chosen**, so
  it is hard to fax a note to the wrong partner. No multi-select action on
  `PVS_Report`.
- **The cover carries a full manifest:** patient name, PVS ID and date of
  service for every note, plus every attached file name. The recipient is
  a records clerk filing each note against a chart, and a cover saying
  "10 enclosed" forces them to page through to find out what they got.
- **Access is portal users and admins.** A user can fax any file the app
  already lets them reach, a PVS note included, plus anything they upload.
  Reach follows the record permissions the app already enforces; this
  build adds no new permission model.
- **On demand sending only.** No Send later, no scheduling. Ruled out
  2026-09-23 despite the RC dialog offering it.
- **The form is modelled on the RingCentral New Fax dialog**, which Neil
  supplied as the reference: To, Fax from, Cover page, Notes, Attach, and
  a drop area for files. Ours substitutes the SOS cover template for RC's
  template picker, and adds the PVS note picker RC has no equivalent for.
- **The cover is always the SOS template.** The custom message always
  prints. The manifest section only appears when the fax carries PVS
  notes, so a non-clinical fax gets a clean cover with just the message.

## 5. How the batching actually works

CORRECTED 2026-09-23. An earlier draft merged every note into one
generated document. Neil's model is the right one: one fax, one cover,
one message, and each patient record as its OWN attachment.

We never merge PDFs. RingCentral accepts several multipart attachments in
a single fax and stitches them into one transmission, so:

- the cover is one PDF,
- each PVS note is rendered and converted into its own PDF,
- each uploaded file rides as its own part.

Ten notes means eleven parts and ten `convertToPDF` calls rather than one.
Slower than merging, and worth watching against Creator statement limits
on a large batch, but it keeps each note a separate document in the
archive and gives a natural per-note page count.

The unresolved `convertToPDF` options Collection problem does NOT block
this build. It only costs the running footer, same as the current path.

## 6. Work required

- New form for the console itself, stateless, following the
  `PVS_Fax_Review` pattern.
- `Fax_Log`: a manifest field, and a file field for archived uploads
  separate from `Fax_PDF`.
- `Fax_Address_Book` is empty and needs seeding before the console is
  usable. It exists with Recipient Name, Recipient Category, Recipient
  Fax, Recipient Notes and Recipient Status, and nothing in the app reads
  it today.
- A cover builder that takes a manifest, separate from the note renderer.
- A per-note renderer. `build_pvs_fax_html` already produces cover plus
  note in one document, so it needs splitting so the note can be built and
  converted on its own.
- A send function that assembles an arbitrary number of multipart parts,
  which `send_pvs_fax` already does for `pAttachFiles` but only alongside
  a single generated PDF.

## 7. Still open

Nothing. Scoped and closed 2026-09-23.

## 8. Dependencies

- Nothing depends on the RingCentral scope change.
- Nothing depends on the `convertToPDF` options fix.
- It does depend on `Fax_Address_Book` being populated.


---

# 9. Option 3 - bulk fax from PVS_Report

A multi-record action on `PVS_Report`. Tick rows, click Fax Selected, and
the selection goes out as faxes grouped by recipient. It does not replace
either of the other two paths.

## 9.1 Target shape

1. User ticks any number of rows on `PVS_Report`.
2. User clicks the multi-record Fax Selected action.
3. The selection is grouped by billing branch.
4. Rows that cannot be faxed are separated out: no billing branch, no
   `Partner_PVS_Fax` on file for that branch, duplicate active billing
   contacts, and anything whose `Type_of_Entry` is not Patient Visit.
5. A confirmation screen shows the full plan: each recipient, their fax
   number, how many notes that fax will carry, and every held-back row
   with the reason.
6. User types one cover message, which prints on every fax in the batch.
7. User confirms; nothing sends before that.
8. One fax per recipient. Each fax carries one cover, then that
   recipient's notes as separate attachments, one PDF per note.
9. One `Fax_Log` row per fax, each with its manifest.
10. Every note sent is stamped `Fax_Status = Sent`.

## 9.2 Decisions taken

- **Group and send one fax per recipient.** Twenty rows across five
  partners produces five faxes, not twenty.
- **A confirmation screen, not Creator's built-in prompt.** The native
  confirm cannot name the partners or the counts, so it would be a blind
  yes. This action can fire five faxes from one click and the user needs
  to see the plan first.
- **One cover message for the whole batch**, typed on the confirmation
  screen.
- **3008 and Imaging Order rows are held back and reported**, following
  the v1 Patient Visit gate. Faxing those is still phase 2.
- **Does not replace the per-row button or the console.** Three paths.

## 9.3 Still open

- Whether the confirmation screen is a stateless form opened as a modal,
  the same pattern as `PVS_Fax_Review`, or a page. The modal pattern is
  proven and is the assumption unless changed.
- How the selection is carried from the report into the confirmation
  screen. Creator multi-record actions expose the selected set to the
  action's Deluge, but passing it to a form needs a mechanism that has
  not been tested.

---

# 10. Split view preview

Scoped 2026-09-23. Applies to all three paths, but lands first on the
existing `PVS_Fax_Review` modal.

## 10.1 The ask

Neil asked for a split view: fax details on the left, a preview of the PVS
PDF on the right.

## 10.2 Why not an actual PDF preview

The PDF does not exist until Fax Now runs. A real preview pane means
calling `zoho.file.convertToPDF` on form load, so every open pays a
conversion for a document most users send without reading. Rejected on
cost, not capability.

## 10.3 What to build instead

A read-only rich text field showing the cover and note rendered as styled
HTML, laid out beside the fax fields.

The trick is that `build_pvs_fax_html` already produces exactly this HTML.
On Load calls it with a placeholder fax ID and drops the result straight
into the preview field. The preview is therefore literally the document
that will be sent, not a reconstruction of it, and it costs one function
call rather than a conversion.

## 10.4 Shape

1. Add a rich text field, `Print_Preview`, to `PVS_Fax_Review`.
2. Lay the form out in two columns: existing fields left, preview right.
3. On Load calls `build_pvs_fax_html` with fax ID "PREVIEW" and writes the
   result to `Print_Preview`.
4. `Print_Preview` is disabled.
5. The preview refreshes on user input of the cover remarks field, so what
   the provider types shows up where it will print.

## 10.5 Open

- **Form width.** Neil wants the modal wider and mobile responsive,
  something like 75vw. Creator controls the sizing of a popup-opened form,
  and whether the form's layout settings expose a width for that case has
  NOT been checked. Verify before promising it.
- **Responsive behaviour: two columns collapse to one at 768px.** Decided
  2026-09-23. Mechanism not settled: Creator's form builder carries
  separate desktop, tablet and phone layouts, so this may be configured
  per device rather than written as a CSS breakpoint, in which case the
  boundary is whatever Creator's tablet cutoff is rather than 768 exactly.
  Check the builder before assuming a breakpoint is needed.
- Two-column layout on a stateless form opened as a popup is assumed to
  work from the field row and column properties, but has not been tested
  at this width.
- Whether the preview is worth the On Load cost on mobile, where a
  side-by-side layout collapses anyway.

---

# 11. Build status, updated 2026-09-23 (Session 51)

Option 2, the console, is BUILT on the server side and proven end to end.
No UI yet. Four decisions in sections 1 to 8 changed during the build.

## 11.1 Changed from the original scope

- **Recipients come from `Partner_Billing_Contacts`, not `Fax_Address_Book`.**
  Section 4 said the address book. It is still empty and nothing reads it.
  The billing contacts already carry live `Partner_PVS_Fax` numbers and drive
  the per-row Fax PVS button, so the console reuses them and the seeding
  dependency in section 8 is retired.
- **`Fax_Attachments` is a related child form, not a subform.** Section 6 said
  a file field on `Fax_Log`. Zoho documents subform row inserts only in form
  context (`input.<subform>.insert`), and this build writes from a standalone
  custom function, so `insert into` on a child form is used instead.
- **Ten notes per fax, hard cap.** Not in the original scope. Neil's reason is
  the receiving machine, not the API: more than ten overflows it or ties it up
  while it prints. RingCentral's own ceiling is 200 pages and 50 MB.
- **Local file uploads deferred to phase 2.** Section 3 step 4 and section 4
  both assume uploads. They are not in v1. See 11.3.

## 11.2 What was built

Five functions, all Deluge, default namespace, Map return:

1. `api_fax_recipients()`
2. `api_fax_pvs_search(p_branchId, p_query, p_unsentOnly)`
3. `api_fax_begin()`
4. `build_console_docs(pFaxID, pToName, pToPartner, pToFax, pToAttn, pRemarks, pPvsIds, pUploadNames)`
5. `api_fax_send_console(pLogId, pContactId, pPvsIds, pRemarks)`

Plus the `Fax_Attachments` form, the `Fax_Attachments_Report`, and a Canvas
custom layout on the Fax Log detail view carrying the attachments as a
related block.

The flow is draft-first: opening the console mints a Building `Fax_Log` row,
work attaches to it, and Send assembles and posts. The Fax ID is minted at
send, not at begin, so an abandoned draft leaves no gap in the FAX sequence.

## 11.3 Why uploads are not in v1

Deluge `getFileContent()` states it works only on files fetched with
`invokeUrl`, not on files fetched from Creator fields, and the `.content`
attribute returns text only, not a file object. There is therefore no
documented route from a stored Creator file field into an `invokeurl`
multipart part.

The candidate is the Creator v2.1 download endpoint
(`/creator/v2.1/data/<owner>/<app>/report/<report>/<id>/<field>/download`)
called with a `ZohoCreator.report.READ` connection, feeding the response
straight into `files:`. Documented endpoint, untested chain.

`build_console_docs` already takes `pUploadNames` and prints them on the
cover manifest, so adding uploads needs no rework of the cover or the send
function beyond the parts list.

## 11.4 Option 3 unchanged

Section 9, bulk send from `PVS_Report`, is still unbuilt and unchanged.

---

# 12. Fax from the PVS form - preview then send

Requested by Josh via Neil, 2026-09-23. Scoped mid-session, then **BUILT the
same session in a different shape**. 12.1 to 12.4 are the scope as written;
**12.5 is authoritative** where they disagree. The two form buttons in 12.2
were not possible: a stateful form cannot run Deluge from a button.

## 12.1 The ask

Josh asked whether a PVS could fax on submit. Auto-fax on save was rejected:
an On Success workflow cannot raise an alert, so a provider whose branch has
no fax number on file would get no on-screen warning and the failure would
surface only on the Fax Log and the 4am digest. This matters more than usual
right now because every required-field guard on the PVS form was removed the
same day, so nothing validates a note before it saves.

NEIL RULING 2026-09-23: a button on the PVS form, with a preview of the note
before it goes.

## 12.2 Shape

1. New field `Print_Preview` on `Encounter_PatientVisit`, rich text, disabled.
2. New `Preview Note` button.
3. New `Fax PVS` button.
4. Provider fills the note and saves.
5. Preview Note calls `build_pvs_fax_html` with the record ID and the literal
   fax ID `PREVIEW`, and writes the returned HTML into `Print_Preview`.
6. Provider reads exactly what the hospice will receive and can go back and
   correct anything before sending.
7. Fax PVS resolves the billing branch to one active `Partner_Billing_Contacts`
   row carrying a `Partner_PVS_Fax`, calls the existing send path, and alerts
   SUCCESS with patient, referral, partner, number and fax ID, or FAILURE.

## 12.3 Why no renderer refactor

The preview runs AFTER the save, so `build_pvs_fax_html` is reused exactly as
it stands. It takes a PVS record ID and reads the saved record, which is why a
genuinely pre-save preview would have needed the renderer split to accept
on-screen values instead. NEIL RULING 2026-09-23: after save is fine, so the
split is not needed and the template stays single-sourced.

## 12.4 Open

- Whether the two form buttons replace the Fax PVS button column on
  `PVS_Report` or sit alongside it. Assumption is alongside, same as the
  console did not replace the per-row button.
- Gate behaviour on a note that is Preliminary, not a Patient Visit, or already
  Sent. The modal already has this logic in `PVS_Fax_Review` On Load and it
  should be reused rather than rewritten.

## 12.5 As built, 2026-09-23 (supersedes 12.2 to 12.4)

Source: `docs/fax/SOS_Code_Checkpoint_2026-09-23_Session51.md`, PART 2.

NEIL RULING 2026-09-23: a tickbox during entry, preview, submit, then fax. No
buttons. "Click of a button" is a stateless-form-only event, so the path runs
on decision boxes and on user input events.

Flow: the provider ticks `Fax_This_Note` while filling the PVS. That renders the
note into `Print_Preview` and runs the full gate immediately, so a failure
alerts on screen at tick time. Submit then sends through `send_pvs_fax`. An
override to a manually entered number is supported with a required reason.

The preview is therefore BEFORE save, not after, which is the opposite of 12.3.
That needed the renderer split 12.3 avoided: `build_pvs_note_html` takes a value
map rather than a record ID, so one template serves the on-screen preview and
the saved-record path.

New fields on `Encounter_PatientVisit`, in a Fax Preview Section:
`Print_Preview` (rich text), `Fax_This_Note`, `Fax_Override_Unlock`,
`Fax_Override_Number`, `Fax_Override_Reason`.

New functions:
- `build_pvs_note_html(map pVals)` - the note template, fed by a value map.
- `resolve_pvs_fax_target(int pPvsID)` - single source of the destination and
  the gate. `PVS Fax Review On Load` now takes its gate from it, which answers
  the 12.4 question about reusing the modal's gate logic.
- `fmt_referral_source(string pOrg, string pBranch)` - returns the longer label
  when one contains the other. Wired into the PVS form preview only (open).

New workflows on `Encounter_PatientVisit`:
- `Fax This Note Preview And Gate`, on user input of `Fax_This_Note`
- `Fax Override Number Format`, on user input of `Fax_Override_Number`
- `Fax This Note On Submit`, on success

`build_pvs_fax_html` now loads the logo from a public HTTPS URL on
sosreferrals.com instead of 20 KB of base64.

Live test: a real PVS was faxed to a real partner from the PVS edit page, and
the override path was tested separately with a manually entered number.

The per-row Fax PVS button on `PVS_Report` is unchanged.

None of these objects are in the repo `.ds`. v52 (2026-09-23 13:12) predates
them; see the task list drift row.
