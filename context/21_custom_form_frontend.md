# Custom HTML Form Front End (post-launch architecture note)

Written: Tuesday, July 21, 2026 (Session 20)
Status: DECIDED IN PRINCIPLE, NOT SCHEDULED. Post-8/3. Nothing here is built.
Context: Neil dislikes native Creator forms; Zoho Forms is better but constrained on
layout, field formatting, and conditional logic. He has 15+ years of Gravity Forms
experience and wants that level of design control.

--------------------------------------------------------------------------------
## The constraint that decides everything
--------------------------------------------------------------------------------
HIPAA covers TRANSMISSION and ACCESS, not only storage. "The data is not saved" is
not the compliance line. Any component the PHI payload passes through is in scope and
needs a BAA, including a web server that merely parses and forwards it.

Current posture: PHI lives in Zoho One (BAA) and AWS (BAA). WordPress and Cloudways
are NOT in the PHI path today, and that is worth preserving. WordPress is a large,
plugin-extensible attack surface maintained by a two-admin operation.

--------------------------------------------------------------------------------
## Options evaluated
--------------------------------------------------------------------------------
1. Gravity Forms + a companion plugin that overrides GF's entry storage.
   Mechanically easy (about 150 lines). Pattern proven by the Code Monkeys HIPAA
   Forms plugin (reviewed 7/21): it removes the GF submit button via
   gform_submit_button_<id> returning false, forces native validation to fail as a
   fallback, and handles submit through its own AJAX action, so NO WP entry row is
   ever created. Cleaner than the common delete-after-write approach.
   REJECTED for PHI: the payload still lands on Cloudways and is parsed by PHP, so
   WordPress is in the PHI path and needs a Cloudways BAA plus HIPAA-grade hardening.

2. The Code Monkeys HIPAA Forms plugin itself (v3.3.0, reviewed from the zip).
   REJECTED. It is a storage SaaS, not a pass-through. includes/class-cm-hipaa.php
   hardcodes CURL_URL = https://www.hipaaforms.online/hipaa-api. Submissions encrypt
   and go to Code Monkeys LLC servers; you view them through their API inside WP
   admin, and per their own documentation the only way data leaves is a generated
   encrypted PDF. There is no path into Creator. It would mean a third BAA vendor, a
   subscription dependency, referrals living outside the EMR, and manual PDF as the
   bridge.

3. Contact Form 7 with no Flamingo plugin.
   CF7 stores nothing by design (it builds an email and discards the payload;
   Flamingo is what adds persistence). Wire wpcf7_before_send_mail to POST to Creator
   and wpcf7_skip_mail to suppress the email. REJECTED on two counts: WordPress is
   still in the PHI path, and CF7 is markup and shortcodes with addon-dependent
   conditional logic, which is LESS capable than Zoho Forms. It trades away the exact
   thing the exercise was meant to gain.

4. Custom HTML form front end. SELECTED as the target.

--------------------------------------------------------------------------------
## Target architecture
--------------------------------------------------------------------------------
Hand-built HTML, CSS, and JS form, served as a static page. It does NOT need to live
on WordPress: Cloudflare Pages or S3 both work, which removes PHP, the plugin
surface, and Cloudways from the path entirely.

Flow:
  browser (static HTML form)
    -> AWS API Gateway + Lambda        [BAA covered, already in the stack]
    -> Zoho Creator Custom API         [BAA covered]
    -> Creator form record

Why the Lambda hop is REQUIRED and not optional: Creator Custom APIs authenticate
with OAuth, and a client secret cannot live in browser JavaScript.
[CORRECTED Session 38, 2026-08-31: Custom APIs also support PublicKey auth, so a
browser can post directly and this paragraph overstates the case. See the
Session 38 section at the end of this file.] Lambda is the
credential holder. It also does the server-side validation, since there is no longer
a form engine doing it.

Reuses the existing AWS footprint built for the voice documentation pipeline
(Transcribe Medical, Bedrock, Lambda), so this is not a new vendor or a new BAA.

--------------------------------------------------------------------------------
## What this costs
--------------------------------------------------------------------------------
- Every form becomes a code artifact in the repo. No drag-and-drop, no non-developer
  edits, no form-builder admin.
- Validation and conditional logic get written in JS (client) and re-validated in
  Lambda (server). Client-side conditional logic is straightforward; the duplication
  is the real tax.
- No built-in notifications, confirmations, or entry views. Those become Creator-side
  or Lambda-side concerns.
Mitigation: Claude generates the HTML and the Lambda handler, so the authoring cost
is lower than it looks. But forms move into the repo and the deploy process, out of a
plugin admin panel.

--------------------------------------------------------------------------------
## Decision for launch (through 8/3)
--------------------------------------------------------------------------------
- Referrals: STAY on Zoho Forms. It is BAA covered, maps natively into
  Referrals_Main with no custom API, and the return-visit prefill webhook already
  works against Partner_Referral_Contacts. Do not disturb it before launch.
- PVS and other internal forms: stay native Creator. If layout becomes intolerable
  before the custom stack exists, a Creator CUSTOM PAGE (own HTML and CSS, calling
  Deluge) is the in-BAA escape hatch from the native form renderer.
- Gravity Forms IS fine to use NOW for anything with NO PHI: vendor and imaging
  partner intake, partner information requests, employee applications, contact and
  marketing forms. No BAA question, and it uses skills Neil already has.

--------------------------------------------------------------------------------
## Post-launch build order, when it is picked up
--------------------------------------------------------------------------------
1. Stand up one Lambda + API Gateway endpoint that accepts a JSON payload and writes
   to one Creator form via Custom API. Prove the chain end to end on a non-PHI form.
2. Build the first real form as static HTML against that endpoint. Establish the
   house pattern: markup structure, CSS system, JS validation, conditional logic,
   error and success handling.
3. Decide hosting (Cloudflare Pages is the likely fit, given Cloudflare is already in
   the stack) and how the form pages get deployed from the repo.
4. Port forms one at a time, highest-friction first. Referrals last, since Zoho Forms
   works and the prefill webhook would need rebuilding.

Open questions for that phase: file uploads (Creator file fields vs S3 presign), spam
and bot protection without a form engine, and whether Lambda or Creator owns
duplicate detection.

--------------------------------------------------------------------------------
## Session 38 re-investigation, 2026-08-31: SET ASIDE AGAIN
--------------------------------------------------------------------------------
Picked the hand-built form back up while working the Zoho Forms imaging branch,
and closed it again the same session. Three findings, recorded so the next person
does not spend the time twice.

**1. A browser CAN post to Creator directly. The Lambda hop is not strictly
required after all.** Creator Custom APIs support **PublicKey** authentication,
which is designed for exactly this: an unauthenticated client calling a published
endpoint without OAuth and without a client secret in JavaScript. This corrects
the "Why the Lambda hop is REQUIRED and not optional" paragraph above, which was
written assuming OAuth was the only option.

That removes the credential argument for Lambda. It does NOT remove Lambda from
the design on its own, since server-side validation still has to live somewhere,
but the chain browser -> Creator Custom API is now technically open.

**2. Record creation must go through REST API v2.1 with workflows triggered.**
A Custom API that creates the record with a Deluge `insert into` **skips both
On Validate and On Success**, and there is no override or parameter that turns
them back on. For Referrals_Main that would bypass the master On Success
workflow, which is what derives every partner field from Partner_Location_Label
and mints the Referral ID. A record created that way arrives unstamped and
unlinked.

So the Custom API cannot be a thin Deluge wrapper. It has to call REST API v2.1
with workflow triggering switched on, or the whole downstream chain silently does
not run. This is the same class of finding as context/09 section 5 (imports fire
On Success only when "Execute form workflows" is checked, and On User Input never
fires at all).

**3. A PHP proxy is permanently off the table.** No hosting BAA exists and none
is being pursued, so Cloudways and WordPress cannot be in the PHI path. This is
not a "not yet", it is a closed door, and it retires options 1 and 3 in the list
above for good rather than leaving them as rejected-for-now.

**Status unchanged: DECIDED IN PRINCIPLE, NOT SCHEDULED, nothing built.**
Referrals stay on Zoho Forms. The Session 38 imaging work was done in Zoho Forms
for that reason.

--------------------------------------------------------------------------------
## Session 38 note: form link names are immutable
--------------------------------------------------------------------------------
Relevant here because it is a standing Zoho Forms constraint, not a one-off.

A Zoho Forms link name is fixed at creation. Only the title and the nickname can
be changed afterwards. The live referral form's link name is
`PatientReferralsHCO` and it presents as "Patient Referral"; the two cannot be
brought into line.

Getting a cleaner URL would mean duplicating the form, which mints a new perma
and forces the Forms -> Creator integration to be removed and rebuilt field by
field. REJECTED Session 38. Full detail in context/24 section 1.

This is one more entry in the column of things a hand-built form would not have,
alongside layout and conditional-logic control. It is not on its own a reason to
build one.

--------------------------------------------------------------------------------
END
--------------------------------------------------------------------------------
