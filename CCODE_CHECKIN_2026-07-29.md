# SOS EMR — Claude Code Check-In Prompt
# Generated 2026-07-29 · Source of truth: SOS_Referrals_App_2026-07-29.ds

Paste everything below into Claude Code from the repo root.

---

You are working in the `sos-emr` repo. Read `CLAUDE.md` and `context/01_standing_rules.md`
first and follow them.

**Source of truth for this check-in:** `SOS_Referrals_App_2026-07-29.ds` in the repo root.
This is a fresh Creator export (29-Jul-2026 08:34). The repo's most recent prior export was
`SOS_Referrals_App_2026-07-17.ds` — twelve days stale. Everything below is drift that
accumulated in Creator and was never committed.

Extract the Deluge verbatim from the .ds. Do not rewrite, reformat, reorder, or "improve"
any of it. No comments added. The repo must mirror Creator exactly.

## 1. New standalone functions — create these files in `functions/`

None of these exist in the repo. All are live in Creator.

| File | Signature |
|---|---|
| `functions/create_invoice_from_selection.dg` | `string create_invoice_from_selection(list p_pvsIds)` |
| `functions/run_invoice_batch.dg` | `string run_invoice_batch(int p_batchId)` |
| `functions/create_books_customers.dg` | `string create_books_customers()` |
| `functions/diag_invoice_batch.dg` | `string diag_invoice_batch(int p_batchId)` |
| `functions/link_pvs_to_referral.dg` | `string link_pvs_to_referral()` |
| `functions/backfill_pvs_billing_branch.dg` | `string backfill_pvs_billing_branch()` |
| `functions/backfill_pvs_employee_initials.dg` | `string backfill_pvs_employee_initials()` |
| `functions/backfill_referral_branch.dg` | `string backfill_referral_branch()` |
| `functions/backfill_referral_branch_from_contact.dg` | `string backfill_referral_branch_from_contact()` |
| `functions/diag_referral_contact_match.dg` | `string diag_referral_contact_match()` |

## 2. Orphaned function files — do not delete, flag only

`functions/fn_resolveUserIdentity.dg` and `functions/get_partner_referral_contact.dg` exist
in the repo but are absent from the .ds. Either they were removed from Creator or never
deployed. Add a line for each to `context/04_open_contradictions.md` and leave the files
in place pending my decision.

## 3. New workflow files

Create these. Follow the existing `<Event>__<Field>__<Name>.dg` naming convention already
used in each form directory.

**`Encounter_PatientVisit/`**
- `OnUserInput__Referral_Link__Referral_Sets_Billing_Branch.dg`
- `OnUserInput__Complexity_Level__Complexity_Sets_Charge.dg`
- `OnUserInput__Billing_Branch__Branch_Sets_Charge.dg`
- `OnValidate__Billing_Branch_Required.dg`

**`Referrals_Main/`**
- `OnUserInput__Partner_Branch_Link__Branch_Sets_Partner.dg`
- `OnUserInput__Partner_POC_Email__Sender_Sets_Branch.dg`
- `OnSuccess__Branch_Sets_Partner_Link.dg` — note in the file header that this workflow is
  `status = inactive` in Creator

**`Invoice_Batch/`** (new directory)
- `OnLoad__Invoice_Batch_On_Load_Disable.dg`
- `OnSuccess__Invoice_Batch_On_Create.dg`

## 4. Modified workflow files — overwrite with the .ds versions

All four changed materially. Overwrite, do not merge.

- `Encounter_PatientVisit/OnLoad__Default_Hide_On_Load.dg` — Billing_Branch show/hide/enable
  logic added
- `Encounter_PatientVisit/OnUserInput__Has_Referral_ID__Show_Hide.dg` — Billing_Branch
  show/enable plus explicit null on the "No" branch
- `Encounter_PatientVisit/OnLoad__Invoice_Status_Lock.dg` — `disable Primary_Diagnosis;`
  removed (field deleted)
- `Encounter_PatientVisit/OnUserInput__Referral_Link__PreFill.dg` — now sets
  `input.Partner_Location_Label`

## 5. Schema files — regenerate from the .ds

Missing entirely: `schema/Invoices.md`, `schema/Invoice_Batch.md`, `schema/Imaging_Order.md`,
`schema/Schema_Snapshot.md`.

Stale, must be regenerated: `schema/Encounter_PatientVisit.md`, `schema/Referrals_Main.md`,
`schema/Partner_Referral_Contacts.md`, `schema/Partner_Rates.md`, `schema/Partner_Locations.md`.

Orphaned — present in the repo, absent from the .ds. Flag in
`context/04_open_contradictions.md`, do not delete:
`schema/Encounter_RadiologyRequest.md`, `schema/X_Ray_Orders.md`, `schema/X_Ray_Request_Form.md`.

## 6. Field-level changes to reflect in schema and context docs

**Encounter_PatientVisit**
- DELETED `Primary_Diagnosis` (textarea) — superseded by the ICD-10 lookup
- DELETED `Multi_Line` (stray field, created accidentally)
- ADDED `Partner_Location_Label` (text) — was briefly named `Partner_Branch1`
- ADDED `Hold_From_Invoicing` (radio No/Yes)
- ADDED `Invoice_Link` (lookup → Invoices, label "Invoice Connection")
- MOVED `Billing_Branch` from Referral_Partner_Section to Provider_Signature_Section, below
  `Hold_From_Invoicing`
- RELABELED `Partner_ICD_Codes` → "Partner ICD 10 Codes"

**Referrals_Main**
- ADDED `Partner_Location_Label` (text)

**Partner_Referral_Contacts**
- ADDED `Partner_Locations_Link` (lookup → Partner_Locations, filtered by
  `Partner_Link.ID == input.Partner_Link`)

**Partner_Rates**
- `Partner_Location_Link` display format changed `Partner_Location_Name` →
  `Partner_Location_Label`

**Partner_Locations**
- `Partner_Link` display format bug fixed — was
  `[Partner_Display_Name + " - " + Partner_Display_Name]` (same field twice)

**Invoice_Batch** — entire form is new. Fields: `Partner_Link`, `Partner_Location_Link`,
`Date_From`, `Date_To`, `Batch_Status`, `Result_Message`, `Invoice_Link`.

## 7. Context docs to update

- `context/19_live_workflow_inventory.md` — add every workflow and function from sections 1
  and 3 above
- `context/17_billing_glossary.md` — record that `Complexity_Level` "No Charge" has no
  corresponding `Partner_Rates.Rate_Type` value, and that the rate lookup filters on
  `Current_Rate == "Yes"` only, not `Partner_Rate_Status`
- `context/05_deluge_learnings.md` — append these Creator v6 findings:
  - Report custom actions execute once per selected record, so they cannot pass a whole
    multi-select to one function. This is why `Invoice_Batch` exists as a staging form.
  - There is no read-only field property. Use `disable Field;` in an On Load workflow.
  - There is no conditional-mandatory property. Use an On Validate workflow with `alert` then
    `cancel submit;`. `cancel submit` takes no message argument.
  - Lookup display formats cannot traverse two hops. A second-hop value must be denormalized
    into a text field on the intermediate form.
  - Setting a field via Deluge does not fire that field's On User Input workflow.
  - Creator's mobile offline mode blocks any form carrying before-submit workflows (on load,
    on user input, field rules). Encounter_PatientVisit and Referrals_Main can therefore
    never be offline-capable.
- `context/18_launch_plan.md` — supersede with the current launch list; hard date Mon
  2026-08-03

## 8. Versioning change — do this and note it in README.md

`run_schema_monitor` emits field tables only. It does not version workflows or functions, so
every piece of Deluge written in the last two weeks existed nowhere but the Creator instance.

Going forward the .ds export is the versioned artifact. Commit
`SOS_Referrals_App_YYYY-MM-DD.ds` on every export, keep `SOS_Referrals_App.ds` as a copy of
the newest, and confirm `.gitignore` is not excluding `*.ds`.

## 9. Commit

One commit. Message:

```
Sync Creator drift 2026-07-17 → 2026-07-29

Invoice engine (create_invoice_from_selection, run_invoice_batch,
create_books_customers), rate lookup, Billing_Branch manual path,
referral branch resolver, and supporting backfills. Adds .ds as the
versioned source of truth for Deluge.
```

Run the pre-commit hook. If `.githooks/sos-checks.sh` fails, report the failure and stop —
do not bypass it.

## 10. Report back

Print a diff summary: files added, files modified, files flagged. List anything in the .ds
you could not place, and anything in the repo you could not match to the .ds.
