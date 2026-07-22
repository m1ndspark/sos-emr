# SOS EMR Catch-Up Plan: Wed 7/22 to Fri 7/24

Written: Tuesday, July 21, 2026 (end of Session 20)
Purpose: absorb the backlog carried out of 7/20 and 7/21 without moving Test 1.
Parent plan: context/18_launch_plan.md (LOCKED to 8/3). This file supersedes the
daily task lists for 7/22 through 7/24 only. Everything from Sat 7/25 onward is
unchanged.

--------------------------------------------------------------------------------
## Where the slip came from
--------------------------------------------------------------------------------
7/17, 7/18, 7/19 completed on plan. Session 20 (7/20 to 7/21) went deep on PVS form
hardening: provider signature, facility conditional, entry-type visibility for all
types, the imaging restructure, walk-in gating, Patient_Display_Name, the
referral-detail pull and lock, and the finalize-lock. That work was necessary and is
now live, but most of it was not on the explicit critical-path list, so two scheduled
items did not start:

- Finalize-lock (7/20) - now BUILT at the end of Session 20.
- July import path (7/21) - NOT started. This is the real gap.

Also outstanding and small: two backfills, two workflow cleanups, and one open
question.

--------------------------------------------------------------------------------
## Wed 7/22 - clear the backlog, then the July import path
--------------------------------------------------------------------------------
Morning, roughly one hour total. These are all small and unblock nothing else, so
they go first to get them off the list.

1. Backfill DM_Full_Name on existing Referrals_Main rows (generator is live; only
   new and edited records populate today).
2. Backfill Patient_Full_Address on existing Referrals_Main rows (same situation).
3. Delete the DISABLED legacy PVS workflow "Patient Fields Editability Toggle".
   This also clears a long-standing ds_sync AMBIGUOUS collision on the PVS
   Has_Referral_ID event.
4. Confirm live and remove the stray "Partner Rate Stamp Generator" bound to the
   Partners form (the correct one lives on Partner_Rates).
5. Answer the Referral_Partner_Section question Neil flagged during Session 20 and
   never raised.

Rest of the day, the actual 7/21 work:

6. Design the import mapping: Cognito export plus charge columns plus billing branch
   into PVS records, one row per visit, carrying the referral data the approval
   dashboard needs.
7. Build the import template and the transforms; settle referral-record handling
   (link to an existing referral vs standalone visit rows).
8. Write the backfill plan. Imports do NOT fire workflows, so PVS_ID, Billing_Branch,
   Employee_Full_Name and Employee_Name_Title, Patient_Display_Name, and pricing all
   need an explicit backfill or import-column strategy.

--------------------------------------------------------------------------------
## Thu 7/23 - Books setup plus the invoice engine
--------------------------------------------------------------------------------
This is the heaviest day. It merges what the parent plan had as two separate days
(7/22 Books setup and 7/23 invoice engine).

1. Create all launch partners and branches as Zoho Books customers.
2. Create rate-card items in Books priced from Partner_Rates. Confirm invoice
   template, numbering, and terms.
3. Map Partner_Billing_Contacts to the Books customer AP email.
4. Deluge: assemble priced line items from a finalized PVS.
5. Create a Books invoice via integration task, one line per visit.

--------------------------------------------------------------------------------
## Fri 7/24 - consolidation plus approval dashboard (1)
--------------------------------------------------------------------------------
1. Consolidation: multiple selected PVS records for the same partner and branch into
   a single invoice.
2. Custom Creator page: table of finalized PVS billable entries showing PVS plus the
   pertinent referral data.
3. Editable override fields for manual amount adjustments, with the change recorded.
4. Checkbox multi-select scoped to the same partner and branch.

DUE FROM NEIL TODAY: the sample charge file, 10 to 20 July visits with charge columns
AND the billing branch. Test 1 on Sunday runs against this file.

--------------------------------------------------------------------------------
## Unchanged from the parent plan
--------------------------------------------------------------------------------
- Sat 7/25: approval dashboard (2). Running-total $3000 alert (alert only), Create
  Invoice button (assemble, push to Books, mark invoiced, write the invoice number
  back), Send button, and an internal dry run of the full chain on the sample file.
- Sun 7/26: TEST 1, end to end on the sample import.
- Mon 7/27 onward: unchanged. Test 2 Fri 7/31. Launch Mon 8/3.

If Wed through Fri land as written, the schedule is fully recovered by Friday night.

--------------------------------------------------------------------------------
## Risks in this compression
--------------------------------------------------------------------------------
1. Thursday is the pinch point. Books setup and the invoice engine were separate days
   in the parent plan. If Books setup runs long (customer creation, rate-card items,
   or the AP email mapping), consolidation slides to Friday and the dashboard build
   compresses.
2. The import path is still a new path with no rehearsal. Wednesday's design work is
   the de-risk; Test 1 exercises it on a sample before the full 250 on 7/29.
3. The sample charge file is a hard dependency for Test 1. If it slips past Friday,
   Sunday's test has nothing to run against.
4. Rate-card completeness in Partner_Rates gates Thursday's Books item creation. It
   was due 7/21 in the parent plan; confirm it is loaded and Active before Thursday.

--------------------------------------------------------------------------------
## Deferred, explicitly not in this window
--------------------------------------------------------------------------------
Territory resolver, rate-card auto-pricing, QuickBooks sync, WorkDrive, the 3008
assessment field group on Referrals_Main, the 3008 inbox, in-app 3008 PDF generation
(replacing pdfFiller), the primary record-lookup view, richer reporting, and the
subscription in-app view. All post-launch.

--------------------------------------------------------------------------------
END
--------------------------------------------------------------------------------
