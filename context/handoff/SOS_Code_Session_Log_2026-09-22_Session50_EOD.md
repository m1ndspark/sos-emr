# SOS Code Session Log, 2026-09-22, Session 50 (EOD)

Focus: PVS fax system built end to end and proven live; partner referral
confirmation email built and verified.

Patients are referenced by REF or PVS ID only.

## Headline
The PVS fax system went from "auth works, nothing has ever been
faxed" to a working loop: button, modal, send, poll, confirm,
retry, digest, log report. Eight real faxes sent tonight, seven
delivered and confirmed by RingCentral. A partner-facing referral
confirmation email was also built and verified.

--------------------------------------------------------------------------------
## 1. How the session opened
--------------------------------------------------------------------------------
Session 49 commit was on hold at ccode over a PHI scan hit: a
patient name in the INV-000099 double-billing row of
context/23_task_list.md. Neil confirmed it was a patient name.
ccode replaced it and committed.

  Commit 94f07d1b729e3463508542905772faa55c6fe8d0
  "Session 49: v51 export, August 3008 rebill closeout, Net 30
   fix, task list update"
  origin/main moved 2edd5c9 -> 94f07d1 on github.com:m1ndspark/sos-emr

Standing rule added and accepted by ccode: rows and prompts refer
to patients by REF or PVS ID only, never by name.

PHI scrub of context/34_august_backfill_open_items.md was
confirmed still outstanding (names in sections 2 and 3, and in
git history). NEIL RULING 2026-09-22: leave as is for now.

--------------------------------------------------------------------------------
## 2. Fax requirements settled before any code
--------------------------------------------------------------------------------
Reviewed v51 directly plus docs/fax/SOS_PVS_Fax_System_Design.md.
State found: all four functions existed, Fax_Log was correct,
Partner_PVS_Fax existed, PVS_Fax_Review existed with only an
On Load workflow. Nothing called send_pvs_fax. No schedule
existed. Nothing had ever been faxed.

Eight-item agenda was agreed and worked in order. Decisions:

1. Entry point: report button plus redirect on save, redirect only
   when the gate passes. LATER REVERSED, see section 7.
2. Destination authority: Partner_PVS_Fax only. Fax_Address_Book
   plays no part.
3. 3008 route: v1 is Patient Visit only. 3008 and Imaging Order
   are blocked with a gate message.
4. Attachments: field-qualified, everything inline. LATER DROPPED
   ENTIRELY, see section 3.
5. Poll: self re-arming schedule on Last_Polled_Time, no cron.
6. Retry and digest both ship in v1.
7. Validation: four block rules, plus warn-and-allow on a re-fax.
   The re-fax reason field was never built, see open items.
8. Reports: one Fax Log report with a saved Exceptions view.

--------------------------------------------------------------------------------
## 3. The flow changed mid-session
--------------------------------------------------------------------------------
Neil pushed back on the review-page-every-time design. New shape:

  - Fax PVS button on each PVS_Report row sends immediately.
  - One fax equals one document: our cover sheet plus the note.
    No attachments at all. Imaging reports are inbound, separate.
  - When there is no number on file or duplicate contacts, the
    review form opens as a MODAL to type a one-off number with a
    reason.

This dropped the attachment picker and the whole convertToPDF
merge question from v1.

--------------------------------------------------------------------------------
## 4. What the ZZ test button proved
--------------------------------------------------------------------------------
Rather than guess at Creator behavior, a throwaway report action
settled three unknowns at once:

  - alert is NOT available in a report action. Error: "'ALERT'
    task can be used only in on load, on validate and on change
    actions".
  - info IS visible to the user in a report action. It renders in
    a "log messages" dialog. This contradicts the assumption that
    info output is invisible.
  - openUrl with "popup window" DOES work from a report button and
    opens a Creator form as a true modal.

Also learned: the per-row control is a Button COLUMN on the
report, not the action item. The action item alone renders
nothing on the row.

--------------------------------------------------------------------------------
## 5. Defects found and fixed
--------------------------------------------------------------------------------
5.1 replaceAll three-argument form does not apply a regex.

  v_raw.replaceAll("[^0-9]","",true)  -> returns "+19418062117"
  v_raw.replaceAll("[^0-9]","")       -> returns "19418062117"

  The third argument switches to literal matching. This was in
  send_pvs_fax and in the PVS Fax Review On Load, so every fax
  would have posted a malformed E.164 like ++19418062117, and the
  modal showed "the PVS fax number on file is not 10 digits" for
  a number that was perfectly valid. Only those two places in the
  whole app used the broken form; the other seven three-argument
  calls replace literal strings and are correct.

5.2 get_rc_token was the OLD version, not the one the repo
    documents. It cached tokens for a hardcoded 115 minutes and
    had no safety margin, while RingCentral issues 3600-second
    tokens. For roughly 55 minutes of every cycle it served a
    dead token. Symptom was TokenInvalid / OAU-213 "Token not
    found" on a send. Now reads expires_in off the response and
    requires more than five minutes of life left.

5.3 left(250) throws when the string is shorter than 250. This
    swallowed the real RingCentral error behind a second failure.
    Guarded in send_pvs_fax and poll_fax_status.

5.4 Original_Fax_Link is a self-lookup; passing 0 kills the
    insert. Sent_By is an Employees lookup being handed a login
    email. Both now set after the insert, only when they resolve.

5.5 invokeurl THROWS on a 503 rather than returning a body, which
    aborted send_pvs_fax and left the Fax_Log row stranded at
    Building. Both POSTs are now wrapped in try/catch. Deluge
    try/catch IS supported in custom functions.

5.6 for each cannot iterate a variable holding a fetched record
    set in a standalone function. The query has to sit inline in
    the loop. Cost one round trip on diag_pvs_fax_number.

5.7 zoho.file.convertToPDF options argument. Collection() plus
    two-argument insert produced a LIST. A Map was rejected as
    the wrong type. A key-value literal was also rejected. The
    options argument was dropped entirely to get a send tonight,
    which means the running footer (patient, DOB, PVS ID, fax ID,
    page x of y) is currently missing from every page. Zoho's doc
    says lowercase collection() plus insert, which is what failed.
    PARKED at Neil's instruction.

--------------------------------------------------------------------------------
## 6. What was built
--------------------------------------------------------------------------------
Functions changed or created:
  send_pvs_fax          regex fix, lookup guards, Map->no options,
                        TokenInvalid retry, try/catch on both POSTs
  get_rc_token          expires_in plus five minute margin
  poll_fax_status       try/catch, guarded truncation, error count
  retry_failed_faxes    NEW. Retry Pending rows, three attempt cap,
                        spawns a new fax linked to the original,
                        retires the old row to Failed
  send_fax_digest       NEW. Five sections, ZeptoMail, floor at
                        22-Sep-2026 so pre-fax history is excluded
  send_referral_confirmation  NEW. Partner-facing, Partner_POC_Email
                        only, wraps the existing
                        build_referral_confirmation_html
  process_new_referral  calls send_referral_confirmation in the
                        success branch only
  build_pvs_fax_html    cover FROM block rewritten
  diag_pvs_fax_number, diag_fax_error, diag_rc_token, diag_fax_pdf_image,
                        diag_collection_shape   all diagnostic

Workflows on PVS_Fax_Review (stateless form, so the only events
available are Field rules, On Load, On User Input, Click of a
button):
  PVS Fax Review On Load          rewritten several times
  PVS Fax Review Override Unlock  On User Input of Override_Unlock
  PVS Fax Review Fax Now          Click of a button, does the gate
                                  checks, calls send_pvs_fax,
                                  alerts, closes the modal

Form changes Neil made:
  PVS_Fax_Review: added Patient_Name and Referral_ID, both
    prefilled and disabled. PVS_Link and Patient_Display hidden.
    Note_Preview relabeled Cover Remarks, now editable rich text
    that feeds the cover. Cover_Remarks hidden.
  PVS_Report: Button column added, labeled Fax PVS.

Schedules created:
  Fax Poll Re-arm     Fax_Log, Last_Polled_Time + 3 minutes,
                      condition Fax Status is Queued
  Fax Retry Sweep     Fax_Log, Last_Polled_Time + 15 minutes,
                      condition Fax Status is Retry Pending
  Fax Digest Daily 4am   daily at 04:00

Report created:
  Fax Log, sorted by Submitted Time descending

Cover sheet FROM block now reads:
  SOS Mobile Medical Care
  8270 Woodland Center Blvd, Tampa, FL 33614
  Phone (813) 513-1925    Fax (813) 626-3312
Provider name removed. The (561) 560-8302 x101 extension is gone
from both the FROM block and the confidentiality notice.

Alert wording agreed:
  SUCCESS: [patient] ([REF ID]) Faxing to [destination] at
  [number]. Fax ID [FAX-...].
  FAILURE: FAX NOT SENT. Fax ID [FAX-...]. Check the fax log for
  details.

--------------------------------------------------------------------------------
## 7. Decisions and rulings
--------------------------------------------------------------------------------
- Fax cover FROM block is company only, no provider name.
- Note Preview shows "Clinical note(s) for:" plus patient name and
  MRN (Patient_Hospice_ID from the referral). No note excerpt.
  This same field is the editable cover remarks.
- Override does NOT unlock the rest of the record. The form is
  stateless, so edits there would change what is faxed while the
  PVS still said something else.
- REDIRECT ON PVS SAVE IS SKIPPED. openUrl is terminal and would
  kill whatever On Success jobs had not yet run, including the
  draft invoice. Neil: "so lets not create a new problem."
- No Partner_Confirmed_Time stamp field. Neil declined it. Known
  consequence: a re-run of process_new_referral emails the partner
  again.
- Digest floor is 22-Sep-2026, hardcoded.
- Digest uses ZeptoMail for consistency with the other
  notifications.
- Token safety: expiry math alone cannot prevent a revoked token,
  so send_pvs_fax now clears the cache and retries once on
  TokenInvalid. This is NOT the same as retry_failed_faxes and
  does not consume an attempt.

--------------------------------------------------------------------------------
## 8. Live results
--------------------------------------------------------------------------------
Eight faxes, FAX-092226-1001 through 1008, all to the test line
813-336-2236 except 1003 which went to 813-626-3312.

  1001  Sent    3 pages
  1002  Sent    3 pages
  1003  Sent    3 pages
  1004  Failed  RingCentral 503 Service Temporary Unavailable
  1005  Sent    4 pages
  1006  Sent    4 pages
  1007  Sent    4 pages
  1008  Sent    3 pages, resolved by the schedule with no manual
                poll, which proved the re-arm works

Digest after the floor was added: missed 0, prelim 0, failures 0,
overrides 8.

Partner confirmation verified: REF-1509 sent live to a real
Empath contact (benign "referral received" message), then REF-1545
confirmed arriving at Neil's own address through the form path.

--------------------------------------------------------------------------------
## 9. Open items
--------------------------------------------------------------------------------
BLOCKING NOTHING, BUT OUTSTANDING
- convertToPDF options Collection syntax unsolved. Running footer
  missing from every faxed page. PARKED.
- Fax Exceptions saved filter view not created. The Fax Log report
  exists; the filtered view does not.
- Re-fax reason: the warn-and-allow ruling has nowhere to store a
  reason. No Resend_Reason field was added, and On Validate does
  not currently block or warn on an already-Sent PVS.
- Partner_PVS_Fax is blank on all four InnoVage rows, and InnoVage
  has duplicate Orlando and Tampa rows.
- Digest fires in the app timezone, so it will shift with daylight
  saving rather than staying fixed at 4:00 am Eastern as the
  Session 34 ruling states.
- build_referral_confirmation_html uses the &mdash; entity as its
  blank placeholder, same class as the fax em dash defect.
- Zoho Form is not passing Partner_Branch_Submitted. Seen on
  REF-1508 and again on REF-1545. Form-side, not Creator.
- No partner confirmation stamp, so re-running
  process_new_referral re-emails the partner.
- context/34_august_backfill_open_items.md still holds patient
  names, in the working file and in git history.

PHASE 2, NOT STARTED
- 3008 fax route. Nothing reads Type_of_Entry into a fax path and
  the 3008 document variant is still tabled pending the PDF Filler
  review.
- Imaging order faxing to vendors. Blocked in v1 with the same
  gate message as 3008.

--------------------------------------------------------------------------------
## 10. Next session
--------------------------------------------------------------------------------
1. Fresh .ds export and commit. The repo is now well behind the
   live app: five functions changed, three created, three
   workflows, three schedules, one report, two new form fields.
2. Solve the convertToPDF options Collection and restore the
   running footer.
3. Populate Partner_PVS_Fax for InnoVage and fix the duplicate
   branch rows.
4. Decide the re-fax path, which needs a field.
5. Build the Fax Exceptions view.
6. Scope the 3008 fax route.
