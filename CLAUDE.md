# CLAUDE.md - SOS EMR Code Repository

This file briefs Claude Code at the start of every session in this repo. Read it
first, then read `MANIFEST.tsv` to locate code, then the files in `context/`.
Open `_INDEX.md` only for one item's deep history, never wholesale.

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
2. Claude writes or edits the `.dg` file here.
3. Claude runs the pre-commit audit (`context/08_code_review_checklist.md`)
   before staging, then commits and pushes. Neil does not run git himself.
4. Neil copies the function out of the repo and pastes it into Creator.
5. Neil tests in Creator and reports pass or fail.
6. Claude updates the status row in `_INDEX.md`. History lives in git.

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
  link names often differ. `schema/<Form>.md` is the authoritative source for
  field lists and is checked first; `context/06` is supplementary. On conflict,
  schema/ wins.
- Open the `.dg` for ground truth before any edit. The manifest relationship
  columns (calls, writes, reads, fetches) are regex-derived navigation aids, not
  an authoritative logic model. Never write code off the manifest columns alone.
- Treat any `.dg` as possibly stale versus live until confirmed. Ask for a fresh
  read of the `.dg` before editing it.

--------------------------------------------------------------------------------
PRE-COMMIT AUDIT (QA GATE)
--------------------------------------------------------------------------------
- Before any Deluge or workflow change is committed, run the checklist in
  `context/08_code_review_checklist.md` and present the result. This runs
  automatically whenever Neil asks to commit or push. Nothing is staged while a
  FLAG is open. VERIFY LIVE items (assumptions only Neil can confirm in the live
  Creator app) are listed but do not block the commit.
- Neil handles no git himself. Claude does review, stage, commit, and push.
  Neil can override per change with "just commit, skip the audit".
- The audit gates Deluge changes only. A change that touches no Deluge is exempt,
  for example context files, `_INDEX.md`, `MANIFEST.tsv`, `schema/`, and
  `tools/`.

--------------------------------------------------------------------------------
REPO CONVENTIONS
--------------------------------------------------------------------------------
- `.dg` files hold pure Deluge only, no comment headers, so they round-trip
  cleanly back into Creator. Status and per-workflow history live in
  `_INDEX.md`; generated navigation metadata lives in `MANIFEST.tsv`.
- One file per workflow. Path encodes form and trigger, e.g.
  `Encounter_PatientVisit/OnUserInput__Has_Referral_ID__Show_Hide.dg`.
- Standalone functions live in `functions/`.
- Non-Deluge logic (condition-expression show/hide) is recorded as a short note
  in the form's folder, since it will not copy out as code.
- `schema/` is generated output from the live Creator Meta API, not hand
  maintained. It is written by the Deluge function `run_schema_monitor` on a
  daily 06:00 schedule.
- `MANIFEST.tsv` is generated output, never hand-edited. Regenerate with:
  `python3 tools/ds_sync.py --ds SOS_Referrals_App.ds --repo . --manifest`.
  The `.ds` is a local Zoho Creator export from Settings > Application IDE >
  Export; it is deliberately not a repo artifact (`.gitignore` excludes
  `*.ds`), and Neil supplies it when the manifest needs regenerating. The hash
  is computed from the `.ds` (live Creator truth), so a hash that does not
  match a `.dg` usually means the repo has drifted from live, NOT that the
  manifest is stale.

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
1. Read `MANIFEST.tsv` first. It is the navigation index: one row per workflow or
   standalone function, with columns file, name, form, trigger, field, calls,
   writes, reads, fetches, integrations, hash. Use it to locate the ONE `.dg`
   that matters. Do not read `_INDEX.md` wholesale; open it only for one item's
   deep history, reading just that item's block.
2. Read `context/04_open_contradictions.md`. Three items remain unresolved (4-A,
   4-B, 4-D; 4-C resolved June 25) and must not be silently decided. They affect
   any code that touches those areas.
3. The repo is being seeded by manual extraction from Creator. Many `.dg` files
   are still placeholders marked PENDING. Do not treat a placeholder as live code.

--------------------------------------------------------------------------------
CONTEXT FILES
--------------------------------------------------------------------------------
- `schema/` per-form field mirror (link name, type, mandatory, unique, choices,
  subfields), auto-generated so never hand-edited. Authoritative for field
  lists; checked before `context/06`. On conflict, schema/ wins.
- `context/01_standing_rules.md`   full standing rules
- `context/02_form_architecture.md` forms, PVS, fields
- `context/03_id_conventions.md`   object ID patterns and charge codes
- `context/04_open_contradictions.md` the remaining unresolved items (4-A, 4-B, 4-D)
- `context/05_deluge_learnings.md` confirmed works and does-not-work
- `context/06_field_link_names.md` Creator field link names per form (confirm before referencing)
- `context/07_partner_billing_and_rates.md` rate model, partner billing hierarchy, ID format, sequencing redesign, collision safety (June 25, 2026 design)
- `context/08_code_review_checklist.md` pre-commit QA gate: what Claude audits before any code is committed

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
