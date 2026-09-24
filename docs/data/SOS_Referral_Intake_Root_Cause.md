# SOS Referral Intake Defect - Root Cause

Established 2026-09-24 (Session 53) by reading the v53 export, not by
inference. Source: Session 53 log, PARTS 3 and 4. Architecture and the agreed
fix: `docs/data/SOS_Referral_Partner_Field_Convention.md`, Part 2.

## Symptom

`referrals_missing_branch_link` went from 1 to 4 overnight. REF-1556, REF-1557
and REF-1558 were all new. (REF-1500 is the fourth, unchanged since Session
52.)

## The chain

1. `process_new_referral` DOES resolve the branch, but the whole resolution
   block is wrapped in `if(v_SubmittedLabel != "")`, where `v_SubmittedLabel`
   reads `Partner_Location_Label`.
2. On all three referrals that field was empty, so the block never ran.
3. The branch label arrived in `Partner_Organization` instead:
   "VITAS - Citrus", "AccentCare - Hillsborough", "Suncoast - HIL".
4. Sender Sets Branch, which would have caught it, fires only on user input of
   `Partner_POC_Email`. It never fires on an API or form submission.

## Why the label lands in the wrong field

The Zoho Form has two dropdowns on Referral Partner Details:

| Question | Required | Source |
|---|---|---|
| Partner Organization | yes | Large List "Partner Locations" |
| Referral POC Branch Lookup | no | same Large List |

The list is NESTED: partner as parent, locations as children. Users pick a
location under the parent in the required org box and never reach the
optional branch question.

### Global Choices constraint (verified)

Zoho Forms choice-based field rules do NOT support Global Choices, so a saved
list cannot drive a dependency. The nesting is not a dependency; it is one long
list.

## Second source: NAME vs LABEL

`get_partner_referral_contact`, the email lookup the form calls, returned
`Partner_Branch` from `Partner_Locations.Partner_Location_NAME`
("Suncoast - HIL"), while the dropdown offers `Partner_Location_LABEL`
("Empath - Suncoast - HIL"). Two different strings for the same branch. That is
exactly REF-1558.

FIXED 2026-09-24: `get_partner_referral_contact` now returns
`Partner_Location_Label`. Both paths speak one string, so matching is an exact
label lookup with no splitting.

## Ruling

NEIL RULING: one flat branch dropdown. Drop the separate org question. Creator
derives the organization from the location record, so `Partner_Organization`
is still written for report filtering, from the master record, not from parsing
text.

## Zoho Form list vs Partner_Locations - RECONCILED

Every group in the saved list walked against the 24 Partner_Locations records.

| Finding | Locations | Status |
|---|---|---|
| Missing from the form, live Creator record | InnoVage - Orlando, VITAS - Villages | ADDED by Neil 2026-09-24 |
| On the form, disabled, no Creator record | Chapters - Okeechobee, Chapters - Marathon, Chapters - Alachua | harmless while disabled; breaks referrals the day one is enabled |
| On the form, disabled, misnamed | "Empath - Main" | should be "Empath - Main Hospice" |
| In Creator, correctly absent from a partner form | Direct - Individual (internal), Cornerstone - Main (not a branch, per Neil) | correct |

Everything else matches character for character. Reconciliation complete.

Correction to Session 52: AccentCare - Broward IS on the form. It was below the
fold.

## Permanent cost

Zoho Forms has no way to populate a dropdown from Creator. Any list on the form
is a hand-maintained copy of Partner_Locations and must be re-reconciled
whenever a location is added, renamed or retired.
