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
with OAuth, and a client secret cannot live in browser JavaScript. Lambda is the
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
END
--------------------------------------------------------------------------------
