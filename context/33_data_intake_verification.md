# DATA INTAKE VERIFICATION PROTOCOL

Status: MANDATORY. Added 2026-09-10 (Session 43) after the August 2026 Cognito
import shipped a referral file with no Referral_ID column, which broke the
referral to PVS join for 191 records and was not detected until after import.

Scope: every external file intended to enter any SOS system. Cognito exports,
partner spreadsheets, Books extracts, vendor CSVs, anything. Applies whatever
the file type and whatever the destination, Creator or otherwise.

Governing principle: no report, invoice, metric or partner deliverable is ever
built from a data set that has not passed every gate below. Assembling correct
data comes first. Reporting comes last and only after the data is proven.

--------------------------------------------------------------------------------
## The rule
--------------------------------------------------------------------------------
Data is not "imported." Data is PROVEN. A file is not done when it loads without
an error message. It is done when a round trip diff shows zero loss and zero
drift against the source, and Neil has cleared every inference by name.

Never report progress as complete at any gate you have not actually executed.
Cite the gate number and the counts.

--------------------------------------------------------------------------------
## GATE 0 - Objective binding
--------------------------------------------------------------------------------
Before touching the file, write down in one line what this data is for. The
objective decides which fields are load bearing.

Name the downstream consumers. For the EMR that usually means the MPU report,
the invoice run, or the partner deliverable.

Identify every JOIN KEY the objective needs, on both sides of every join. Write
them down. This is the gate the August import failed.

--------------------------------------------------------------------------------
## GATE 1 - Destination schema enumeration
--------------------------------------------------------------------------------
Read the live schema from the current .ds export, not from memory and not from a
prior session's notes. Confirm the .ds timestamp is later than the last change
Neil made.

Enumerate every field on the destination form: link name, display name, type,
choice list, max length, and whether it is a lookup.

List the fields that exist in the destination and NOT in the file. For each,
state whether it is filled by import, by a workflow, by a backfill, or left
blank on purpose.

List the fields in the file and NOT in the destination. Each is either dropped
on purpose, with the reason stated, or the mapping is wrong.

--------------------------------------------------------------------------------
## GATE 2 - Join key proof
--------------------------------------------------------------------------------
Every key named in Gate 0 must appear as an explicit column in the import file.
Never rely on a value being minted, inherited or inferred on the destination
side.

If the destination mints its own ID on create, the source system's ID must be
carried into a dedicated field so the original is preserved and re-imports can
key on it. On Referrals_Main that field is Cognito_Referral_ID.

If two files will be joined after import, prove the key exists in BOTH files
before either is built. Print a sample of ten keys from each side and match them
by eye.

--------------------------------------------------------------------------------
## GATE 3 - Column mapping proof
--------------------------------------------------------------------------------
Map every column by hand. Creator auto-map silently mis-assigns columns.

Produce a mapping table: file column, destination link name, destination type,
transform applied. No column is left unmapped without a stated reason.

Never map into a lookup field. Import the text, then resolve it with the
resolver function.

Delete every column that is 100 percent empty. An empty column is one more
chance for the wizard to mis-map.

--------------------------------------------------------------------------------
## GATE 4 - Value normalization
--------------------------------------------------------------------------------
Dates: one format across the whole file, matched to the wizard setting. State
the format in the import instructions.

Text into fixed length fields: check every value against the field's max length.
Truncation is silent. Values that do not fit move to the field that fits, and
the move is reported.

Choice fields: every value in the file must exist in the destination choice list,
character for character. Print the distinct values and compare.

Lookup source text: every value must match the destination label exactly.
Partner_Location_Label carries the partner prefix, for example
"Empath - Tidewell".

Junk placeholders: NA, N/A, NONE, UNKNOWN, dash and blank are not data. Count
them, list them, and clear the disposition with Neil before import.

Phones, ZIPs, IDs: validate format. Report every value that fails.

--------------------------------------------------------------------------------
## GATE 5 - Inference review
--------------------------------------------------------------------------------
Anything not present verbatim in the source is an inference. Name splitting,
branch resolution by ZIP, county lookups, partner matching, anything derived.

Every inference is presented to Neil individually with the source text beside
the proposed value. He confirms each one. Nothing derived is written on my
judgment alone.

Ambiguous cases are flagged, not guessed. A flagged row is better than a wrong
row.

--------------------------------------------------------------------------------
## GATE 6 - Pre-import validation
--------------------------------------------------------------------------------
Row count matches the source. State it.

Blank count per column, with each non-zero count explained as either blank in the
source or a defect.

Duplicate detection on the natural key. Duplicates are either legitimate repeats,
confirmed as such, or resolved to a canonical row.

Import file carries no styling. Plain header row, plain data rows.

Blockers cleared: form CAPTCHA disabled, "Execute form workflows" unchecked if
On Validate gates would reject rows, wizard date format set.

--------------------------------------------------------------------------------
## GATE 7 - Import execution
--------------------------------------------------------------------------------
Watch the created count. "Skip corresponding row" silently drops whole rows.
Created count must equal row count. Any gap is investigated before proceeding.

Record the destination ID range the import produced. A contiguous block is the
cheapest possible recovery key if a join later fails.

--------------------------------------------------------------------------------
## GATE 8 - Round trip diff
--------------------------------------------------------------------------------
This gate is not optional and it is the one that would have caught August.

Export the imported records back out of the destination.

Diff every mapped field, row by row, against the source file. Report three
counts per field: lost (populated in source, blank in destination), blank in
both, and matching.

Any non-zero lost count is a defect. Fix it and repeat the gate.

Confirm every join key resolves. Run the linking function in preview and confirm
the match count equals the expected count.

--------------------------------------------------------------------------------
## GATE 9 - Resolution chain
--------------------------------------------------------------------------------
Imports never fire On User Input workflows, so every value those workflows would
have set must be filled by an explicit backfill, in dependency order.

Run each in preview, read the output, then commit. Never commit a bulk write
without reading its preview.

Re-run any backfill whose source was still empty the first time it ran. A
backfill that ran before its input existed did nothing and reported success.

Order for Creator referrals and PVS:
1. resolve_referral_branch_from_text
2. backfill_referral_partner_fields
3. resync_location_labels
4. link_pvs_to_referral, or the Cognito ID variant
5. backfill_pvs_from_referral
6. backfill_pvs_ids
7. backfill_pvs_referral_id_from_link
8. backfill_pvs_referral_date
9. backfill_pvs_billing_branch
10. backfill_pvs_complexity_charge
11. backfill_pvs_premium_fees
12. backfill_provider_login_email
13. backfill_pvs_employee_link
14. backfill_pvs_from_referral again, to pick up values that were blank on the
    first pass
15. resync_location_labels again, for the same reason

--------------------------------------------------------------------------------
## GATE 10 - Release for reporting
--------------------------------------------------------------------------------
Spot check at least five records end to end against their source documents.

Every residual is listed by name with its reason. No residual is left
undescribed.

State explicitly that the data set is released for reporting, and name the
gates that were run. Only then is a report built from it.

--------------------------------------------------------------------------------
## Failure log
--------------------------------------------------------------------------------
August 2026 Cognito referral import, 306 rows:

- Gate 0 failed. Referral_ID was never named as a join key, so the import file
  was built without it and mint_referral_id assigned unrelated numbers.
- Gate 2 failed. The PVS file carried pre-assigned REF IDs that matched nothing
  in Referrals_Main.
- Gate 8 was never run. The break surfaced only when a backfill reported 194
  unlinked rows, days later.
- Recovery was possible only because the minted IDs formed a contiguous block,
  REF-1138 through REF-1443, aligned to import file row order. That was luck,
  not design.
- Referral_Date did not map and every row landed on the import date.
- Partner_Branch text landed in the lookup instead, leaving the text field blank
  and Partner_Link unresolved on all 306.

END
