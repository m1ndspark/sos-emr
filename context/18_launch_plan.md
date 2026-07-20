# SOS EMR Launch Plan (LOCKED) to 8/3 Live Billing

Prepared: Saturday, July 18, 2026 (Session 19). Hard launch: Monday, August 3, 2026.
Cadence: 12-hour days, every day. Test 1: Sun July 26. Test 2: Fri July 31.

--------------------------------------------------------------------------------
## Session 19 completed (7/18)
--------------------------------------------------------------------------------
- Launch plan built and locked to 8/3.
- Refreshed the app export: SOS_Referrals_App.ds (exported 7/17, 287 KB) placed in the
  repo; prior copy archived as SOS_Referrals_App_2026-07-14.ds. Note: *.ds is
  gitignored (working input for ds_sync).
- Full build-vs-verify inventory from the .ds -> context/16_ds_inventory_punch_list.md.
- Canonical billing glossary signed off -> context/17_billing_glossary.md.
- Applied three label fixes live in Creator:
  Complexity_Level (+Telemedicine, Care Coordination, General Consultation, Cares 3008
  Assessment); Additional_Charges "Super STAT Fee" -> "Super STAT"; PVS_Charge_Type
  "After Hours Charge" -> "After Hours" and "Super STAT Fee" -> "Super STAT".
- Committed context/16 and context/17 to origin/main (cfaafd9).

Note on the calendar: planning day landed on 7/18, so the build runs 7/19 onward. The
schedule below is compressed to still hold Test 1 (7/26), Test 2 (7/31), and launch
(8/3).

--------------------------------------------------------------------------------
## Locked decisions
--------------------------------------------------------------------------------
1. All launch partners bill Per Branch. Billing_Branch is a record field on the PVS,
   NOT provider-facing. It is set from the import column for the backlog and
   selected or confirmed by Josh on the approval dashboard. The automatic territory
   resolver is DEFERRED (fast-follow).
2. First run bills July visits in August, always the prior month. Also incremental
   weekly billing where a partner allows, so multiple invoices per partner.
3. Backlog is approximately 250 July visits, imported from a Cognito export with your
   charge columns attached, one row per visit. No hand-keying.
4. One visit is one PVS is one row is one billable set of lines. A second visit is a
   new PVS and a new row.
5. Invoice flow: a finalized PVS creates a Draft billable entry, not a Books invoice.
   Josh reviews on a custom dashboard, checkbox-selects one or many for the same
   partner and branch, clicks Create Invoice (one line per visit), then Send to email
   the AP contact. Some dashboard fields are editable for manual amount overrides and
   for the branch select or confirm.
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

PARKED post-launch (fast-follow):
- Automatic territory resolver: pre-fills the hidden Billing_Branch from the patient
  address, still overridable at approval. Real scope is two parts: an address-to-county
  map (zip/city table) AND county-to-branch per partner, which is business logic you
  and Josh define per partner since each carves territory differently. A manual
  fallback stays regardless (home vs facility addresses, missing data).
- Rate-card auto-pricing: the PVS looks up the Active Partner_Rates amount by partner,
  branch, and type as of date of service, filling the dollar fields instead of manual
  entry.
- Primary record-lookup view: a top-level screen showing a referral header plus all
  associated PVS entries, for investigation and oversight, not billing-bound.
- Reporting data cards across referrals, PVS, and invoicing.
- Supplemental-addendum billing; in-app view of subscription records.

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
Glossary lock (done) -> PVS billing readiness (Billing_Branch record field,
finalize-lock) -> rate card in Books -> July import to PVS -> invoice engine +
approval dashboard -> fax/email send -> Test 1 -> corrections -> full import ->
Test 2 -> corrections -> launch.

--------------------------------------------------------------------------------
## Daily task list (re-based from 7/18)
--------------------------------------------------------------------------------
### Sat Jul 18 (DONE)
Plan locked; .ds inventory; glossary signed off; three label fixes applied; committed
context/16 and context/17.

### Sun Jul 19 - PVS billing readiness + cleanups
1. Add Billing_Branch to the PVS as a hidden record field (not provider-facing).
2. Finalize action: set Invoice_Status to a billable Draft state and lock the PVS.
3. Delete the legacy Patient Fields Editability Toggle (double-handles Has_Referral_ID).
4. Remove the stray Partner Rate Stamp Generator on the Partners form.

### Mon Jul 20 - Referrals close-out + import design
1. DM_Full_Name generator + backfill on Referrals_Main.
2. Design the July import mapping: Cognito export + charge columns + billing branch to
   PVS records, one row per visit, carrying the referral data the dashboard needs.
3. Import template and transforms; backfill plan (import does not fire workflows);
   reconcile confirmed ds_sync DRIFT files.

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
2. Write invoice number back; mark invoiced. Premium line rule: bill only when the box
   is checked and the amount is greater than zero.
3. Unit test with sample PVS data.

### Fri Jul 24 - approval dashboard (1)
1. Custom Creator page: table of finalized PVS billable entries with pertinent referral
   data.
2. Editable override fields for manual amount adjustments and the branch select or
   confirm, change recorded.
3. Checkbox multi-select scoped to the same partner and branch.
(Sample charge file due today.)

### Sat Jul 25 - approval dashboard (2) + email
1. Running-total $3000 alert (alert only).
2. Create Invoice button: assemble, push to Books, mark invoiced, write back number.
3. Send button: Books emails the AP contact, From SOS.
4. Internal dry run of the full chain before Test 1.

### Sun Jul 26 - TEST 1
End to end on the sample import: import to finalized PVS to dashboard to select to $3k
alert to create invoice to email. Log every defect.

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
- Compression removed the slack from one form-readiness day. If Jul 19 to 20 slips,
  Books setup on Jul 21 slips with it.
- July import to PVS is a new path. Jul 20 design de-risks it; Test 1 exercises it on a
  sample before the full 250.
- Rate-card completeness is a data task by Jul 21. If late, Books setup and pricing
  stall.
- The committed 7/17 .ds predates the three label fixes; the next export captures them.

--------------------------------------------------------------------------------
END
--------------------------------------------------------------------------------
