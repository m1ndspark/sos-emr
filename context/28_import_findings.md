# Import Findings - reusable lessons (2026-08-05, Session 28 checkpoint)

Captured from the July/June referral and July PVS imports. These are general
rules, not one-off notes; apply them to every future import and to any Deluge
that touches a lookup or a unique email field.

--------------------------------------------------------------------------------
## 1. Creator imports do not fire On User Input workflows
--------------------------------------------------------------------------------
A CSV/API import does NOT run On User Input workflows (it can run On Success
workflows when "Execute form workflows" is checked; see
09_cognito_import_procedure.md section 5). On the PVS, "Referral Link Pre-Fill"
is an On User Input workflow, so setting `Referral_Link` programmatically (or by
import) never fires it and the referral-derived fields stay blank.

RULE: any programmatic or imported `Referral_Link` assignment on
Encounter_PatientVisit must be followed by `backfill_pvs_from_referral`, which
pulls the referral-derived fields the On-User-Input pre-fill would have set.

--------------------------------------------------------------------------------
## 2. Deluge criteria matching on email fields is case-sensitive
--------------------------------------------------------------------------------
A Deluge fetch like `Form[Email_Field == v_email]` matches case-SENSITIVELY.
Against a field with a UNIQUE constraint this silently misses an existing record
whose stored email differs only in case, so the code proceeds to insert and then
violates the unique constraint (this was the Partner Contact Upsert defect).

RULE: any lookup against a unique email field must do a lowercase fallback scan
before it inserts - e.g. iterate and compare `record.Email.toLowerCase() ==
v_email.toLowerCase()` - and update the found record instead of inserting.

--------------------------------------------------------------------------------
## 3. Import wizard mis-maps Partner_Organization to the Partner_Link lookup
--------------------------------------------------------------------------------
On Referrals_Main the import wizard auto-assigns the `Partner_Organization`
column onto the `Partner_Link` LOOKUP. A lookup only accepts an existing record
value, so this corrupts the mapping. EVERY column must be mapped by hand before
running the import (this is the same class of auto-map defect logged in
09_cognito_import_procedure.md section 5A-a). Never trust the wizard defaults;
confirm each target field one by one.
