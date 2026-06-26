# CLAUDE.md - SOS EMR Code Repository

This file briefs Claude Code at the start of every session in this repo. Read it
first, then read `_INDEX.md` for current code status, then the files in `context/`.

--------------------------------------------------------------------------------
WHAT THIS REPO IS
--------------------------------------------------------------------------------
This repository is the canonical mirror of the Deluge code in the SOS EMR app,
built in Zoho Creator. The live Creator app is the source of truth. This repo
mirrors it so all related code is visible in one place and revisions are tracked
in git instead of by hand.

Owner: Neil Heird (operational lead, SOS Mobile Medical Care). Neil's only manual
step in the loop is pasting verified code into Creator. Claude holds the code and
its history here.

The working loop:
1. A workflow is designed or finalized.
2. Claude writes or edits the `.dg` file here and commits with a clear message.
3. Neil copies the function out of the repo and pastes it into Creator.
4. Neil tests in Creator and reports pass or fail.
5. Claude updates the status row in `_INDEX.md`. History lives in git.

--------------------------------------------------------------------------------
HARD RULES (NON-NEGOTIABLE)
--------------------------------------------------------------------------------
- Platform is Zoho Creator. Language is Deluge only. Never propose a non-Deluge
  or non-Creator solution for app work. Confirm the live Creator build when
  syntax behavior is in question; Creator behavior wins over generic Deluge docs.
- This is a MEDICAL-CONTEXT application. Data integrity and correctness are
  critical. Errors have real clinical and billing consequences.
- Never guess. If a form name, field link name, data type, relationship, or
  logic intent is unclear, stop and ask before writing code.
- Never describe Creator UI navigation from memory. Creator's UI changes often.
  Ask Neil for a screenshot or doc link if a UI path is needed.
- Never rename or change a field or form name without explicit approval.
- Confirm before refactoring large blocks or restructuring logic.
- No em dashes in any SOS content.

--------------------------------------------------------------------------------
CODE DELIVERY RULES
--------------------------------------------------------------------------------
- Full function only. Never partial snippets or diffs unless Neil asks.
- No comments in delivered Deluge unless Neil asks.
- Provide a plain-language logic map before generating or changing code.
- Forms and workflows are one unit. Any field change must be evaluated against
  every known workflow at the same time. Never propose a field change without the
  matching workflow change.
- ID generation always lives in its own workflow, never inline in On User Input.
- Confirm the exact field link name before referencing it. Display labels and
  link names often differ.

--------------------------------------------------------------------------------
REPO CONVENTIONS
--------------------------------------------------------------------------------
- `.dg` files hold pure Deluge only, no comment headers, so they round-trip
  cleanly back into Creator. All status and metadata live in `_INDEX.md`.
- One file per workflow. Path encodes form and trigger, e.g.
  `Encounter_PatientVisit/OnUserInput__Has_Referral_ID__Show_Hide.dg`.
- Standalone functions live in `functions/`.
- Non-Deluge logic (condition-expression show/hide) is recorded as a short note
  in the form's folder, since it will not copy out as code.

--------------------------------------------------------------------------------
SECRETS AND PHI (CRITICAL)
--------------------------------------------------------------------------------
- Never commit API keys, tokens, connection secrets, test records, or any PHI.
- Secrets live in Zoho Connections (runtime) and a password manager (human
  logins), never in code or in this repo.
- The Deluge here references field link names, not patient data, so the repo
  stays PHI-clean as long as data is kept out.

--------------------------------------------------------------------------------
START HERE EACH SESSION
--------------------------------------------------------------------------------
1. Read `_INDEX.md` for the extraction checklist and per-workflow status.
2. Read `context/04_open_contradictions.md`. Three items remain unresolved (4-A,
   4-B, 4-D; 4-C resolved June 25) and must not be silently decided. They affect
   any code that touches those areas.
3. The repo is being seeded by manual extraction from Creator. Many `.dg` files
   are still placeholders marked PENDING. Do not treat a placeholder as live code.

--------------------------------------------------------------------------------
CONTEXT FILES
--------------------------------------------------------------------------------
- `context/01_standing_rules.md`   full standing rules
- `context/02_form_architecture.md` forms, PVS, fields
- `context/03_id_conventions.md`   object ID patterns and charge codes
- `context/04_open_contradictions.md` the remaining unresolved items (4-A, 4-B, 4-D)
- `context/05_deluge_learnings.md` confirmed works and does-not-work
- `context/06_field_link_names.md` Creator field link names per form (confirm before referencing)
- `context/07_partner_billing_and_rates.md` rate model, partner billing hierarchy, ID format, sequencing redesign, collision safety (June 25, 2026 design)

--------------------------------------------------------------------------------
REFERENCE / DOCUMENTATION URLS
--------------------------------------------------------------------------------
- https://help.zoho.com/portal/en/kb/creator/developer-guide
    Library of articles for the Zoho Creator developer guide.
- https://help.zoho.com/portal/en/kb/creator
    Zoho Creator knowledge base (general help articles).
- https://www.zoho.com/books/api/v3/oauth/#overview
    Zoho Books API v3, OAuth overview.
- https://www.zoho.com/developer/rest-api.html
    Zoho developer REST API reference.
- https://www.zoho.com/creator/help/api/v2.1/
    Zoho Creator API v2.1 help.
