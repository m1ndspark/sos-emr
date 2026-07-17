# SOS EMR Launch Plan (LOCKED) to 8/3 Live Billing

Prepared: Friday, July 17, 2026 (Session 19). Hard launch: Monday, August 3, 2026.
Cadence: 12-hour days, every day. Test 1: Sun July 26. Test 2: Fri July 31.

--------------------------------------------------------------------------------
## Session 19 completed (7/17)
--------------------------------------------------------------------------------
- Refreshed the app export (SOS_Referrals_App.ds, 7/17) into the repo; archived the
  7/14 copy. Note: *.ds is gitignored (working input for ds_sync).
- Full build-vs-verify inventory from the .ds -> context/16_ds_inventory_punch_list.md.
- Canonical billing glossary signed off -> context/17_billing_glossary.md.
- Applied three label fixes live in Creator:
  Complexity_Level (+Telemedicine, Care Coordination, General Consultation, Cares 3008
  Assessment); Additional_Charges "Super STAT Fee" -> "Super STAT"; PVS_Charge_Type
  "After Hours Charge" -> "After Hours" and "Super STAT Fee" -> "Super STAT".
- Committed context/16 and context/17 to origin/main (cfaafd9).

--------------------------------------------------------------------------------
## Locked decisions
--------------------------------------------------------------------------------
1. All launch partners bill Per Branch. Branch is set on the record (imported for the
   backlog, selected by Josh at review for anything manual). Automatic territory
   resolver DEFERRED past 8/3.
2. First run bills July visits in August, always the prior month. Also incremental
   weekly billing where a partner allows, so multiple invoices per partner.
3. Backlog is approximately 250 July visits, imported from a Cognito export with your
   charge columns attached, one row per visit. No hand-keying.
4. One visit is one PVS is one row is one billable set of lines. A second visit is a
   new PVS and a new row.
5. Invoice flow: a finalized PVS creates a Draft billable entry, not a Books invoice.
   Josh reviews on a custom dashboard, checkbox-selects one or many for the same
   partner and branch, clicks Create Invoice (one line per visit), then Send to email
   the AP contact. Some dashboard fields are editable for manual amount overrides.
6. $3000 is an ALERT only on the selection total, never a block.
7. Fax is instant on a Send Fax button (SRFax). The PVS PDF stores on the record
   (Creator file field, BAA-covered). No WorkDrive for 8/3.
8. Charge amounts are entered manually on the PVS for 8/3. Rate-card auto-pricing is
   the first-week fast-follow.
9. Addendums are record-only for 8/3 and never touch an invoice.
10. Subscriptions run as native Zoho Books manual/recurring invoices, no Square.

Signed-off glossary decisions live in context/17_billing_glossary.md.

DEFERRED past 8/3: automatic territory resolver, Books-to-QuickBooks sync, WorkDrive,
new referral form as August intake (August is imported), Imaging_Orders and lab build,
AWS voice pipeline.

PARKED post-launch (fast-follow): rate-card auto-pricing; primary record-lookup view
(referral header plus all associated PVS, top-level, not billing-bound); reporting
data cards across referrals, PVS, and invoicing; supplemental-addendum billing; in-app
view of subscription records.

DESIGN PRINCIPLE: management screens are built around the business workflow, not
limited to default Creator report structure.

--------------------------------------------------------------------------------
## Owner split and data deadlines (gate build tasks)
--------------------------------------------------------------------------------
YOURS / JOSH:
- All partner data loaded and Active by Jul 21: partners, branches, Partner_Rates
  (acuity + premiums + services, current amounts), Partner_Billing_Contacts.
- Sample charge file (10 to 20 July visits with charge columns AND billing branch) by
  Jul 24, for Test 1.
- Full 250-visit charge file (Cognito export + charge columns + billing branch) by
  Jul 28, for the full import on Jul 29.
MINE: everything else.

--------------------------------------------------------------------------------
## Critical path
--------------------------------------------------------------------------------
Glossary lock (done) -> PVS billing readiness (Billing_Branch, finalize-lock) -> rate
card in Books -> July import to PVS -> invoice engine + approval dashboard ->
fax/email send -> Test 1 -> corrections -> full import -> Test 2 -> corrections ->
launch.

--------------------------------------------------------------------------------
## Daily task list
--------------------------------------------------------------------------------
### Fri Jul 17 (DONE)
Export .ds; inventory punch list; glossary signed off; three label fixes applied;
committed context/16 and context/17.

### Sat Jul 18 - PVS billing readiness (1) + cleanups
1. Add Billing_Branch lookup on the PVS (to that partner's locations).
2. DM_Full_Name generator + backfill on Referrals_Main.
3. Delete the legacy Patient Fields Editability Toggle (double-handles Has_Referral_ID).
4. Remove the stray Partner Rate Stamp Generator on the Partners form.

### Sun Jul 19 - PVS billing readiness (2)
1. Finalize action: set Invoice_Status to a billable Draft state and lock the PVS.
2. Confirm charge fields and every invoice-source field present and correct.
3. Reconcile confirmed ds_sync DRIFT files (separate track).

### Mon Jul 20 - July import path
1. Design the import mapping: Cognito export + charge columns + billing branch to PVS
   records, one row per visit, carrying the referral data the dashboard needs.
2. Build the import template and transforms; settle referral-record handling.
3. Backfill plan (import does not fire workflows): IDs, Billing_Branch.

### Tue Jul 21 - Books setup
1. Partners and branches as Books customers.
2. Rate-card items in Books priced from Partner_Rates; template, numbering, terms.
3. Map Partner_Billing_Contacts to the Books customer AP email.
(Depends on partner data loaded and Active today.)

### Wed Jul 22 - invoice engine (1)
1. Deluge: assemble line items from a finalized PVS (flat charge fields).
2. Create a Books invoice via integration task (one line per visit).

### Thu Jul 23 - invoice engine (2)
1. Consolidation: multiple selected PVS for the same partner and branch into one
   invoice.
2. Write invoice number back; mark invoiced. Premium line rule: bill only when the
   box is checked and the amount is greater than zero.
3. Unit test with sample PVS data.

### Fri Jul 24 - approval dashboard (1)
1. Custom Creator page: table of finalized PVS billable entries with pertinent
   referral data.
2. Editable override fields for manual amount adjustments, change recorded.
3. Checkbox multi-select scoped to the same partner and branch.
(Sample charge file due today.)

### Sat Jul 25 - approval dashboard (2) + email
1. Running-total $3000 alert (alert only).
2. Create Invoice button: assemble, push to Books, mark invoiced, write back number.
3. Send button: Books emails the AP contact, From SOS.
4. Internal dry run of the full chain before Test 1.

### Sun Jul 26 - TEST 1
End to end on the sample import: import to finalized PVS to dashboard to select to
$3k alert to create invoice to email. Log every defect.

### Mon Jul 27 - corrections
Fix Test 1 defects, highest impact first.

### Tue Jul 28 - PVS fax/email send
1. PVS PDF generate and store on the record (Creator file field, no WorkDrive).
2. Send Fax button: instant SRFax to Fax_Address_Book or a manual number.
3. Email path to the referral contact (SendGrid); send log and re-send.
(Full 250-visit charge file due today.)

### Wed Jul 29 - oversight dashboard + full import
1. Internal dashboard: referrals, PVS status, invoicing by partner, branch, cycle.
2. Run the full July backlog import (about 250 visits) into finalized PVS records.
3. Spot-check imported records: charges, branch, patient data, referral linkage.

### Thu Jul 30 - full-data validation + polish
1. Price-check a sample of the 250 against expected amounts.
2. Close remaining Test 1 corrections; verify fax and email on real records.
3. Pre-Test-2 readiness pass.

### Fri Jul 31 - TEST 2
Full rehearsal on the real 250-visit data, all paths. Log defects.

### Sat Aug 1 - final corrections
Fix Test 2 defects.

### Sun Aug 2 - go/no-go + data readiness
1. Final data verification: partners, branches, rates, billing contacts Active.
2. Backups; rollback plan; confirm SRFax and SendGrid live.
3. Go/no-go checklist sign-off.

### Mon Aug 3 - LAUNCH
1. Generate and send the first live invoices (per partner and branch).
2. Verify emails delivered and fax sends.
3. Monitor; hotfix standby.

--------------------------------------------------------------------------------
## Risks
--------------------------------------------------------------------------------
- Invoice engine + approval dashboard (Jul 22 to 25) is the core build. Scheduled
  first after the forms for recovery room.
- July import to PVS is a new path. Jul 20 design de-risks it; Test 1 exercises it on
  a sample before the full 250.
- Rate-card completeness is a data task by Jul 21. If late, Books setup and pricing
  stall.
- The committed 7/17 .ds predates today's three label fixes; the next export captures
  them.

--------------------------------------------------------------------------------
END
--------------------------------------------------------------------------------
