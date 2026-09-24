# SOS Referral Partner Field Convention

How the partner is recorded on `Referrals_Main`. Established 2026-09-23
(Session 52) from the correctly shaped rows of the September referral export.

## The four columns

Every referral carries the partner in four columns. Example, the Tidewell
branch of Empath:

| Export column | Value |
|---|---|
| Partner Organization | `Empath` |
| Partner Branch/Location | `Tidewell` |
| Partner Branch | `Empath - Tidewell` (the full label) |
| Partner Lookup | `Empath` |

Partner Branch holds the full label. Partner Organization and Partner Lookup
hold the organization. Partner Branch/Location holds the branch part.

## Deriving the four from the full label

Split the full label on the FIRST `" - "` only:

- left of it: Partner Organization and Partner Lookup
- right of it: Partner Branch/Location
- the whole label: Partner Branch

Splitting on the first separator, not every separator, is what keeps
multi-part branch names intact:

| Full label | Organization | Branch/Location |
|---|---|---|
| `Empath - Suncoast - HIL` | `Empath` | `Suncoast - HIL` |
| `Empath - Suncoast - PIN` | `Empath` | `Suncoast - PIN` |

This reproduces the clean September rows exactly.

## Normalisation rule

A value beginning `Suncoast - ` is an Empath branch written without its
organization. Prefix it with `Empath - ` before splitting:
`Suncoast - PIN` becomes `Empath - Suncoast - PIN`.

## Canonical labels

Twelve canonical full labels, derived from the clean September rows:

- `AccentCare - Hillsborough`
- `AccentCare - Miami`
- `AccentCare - Pasco`
- `AccentCare - Pinellas`
- `Empath - Marion`
- `Empath - Polk`
- `Empath - Suncoast - HIL`
- `Empath - Suncoast - PIN`
- `Empath - Tidewell`
- `Empath - Trustbridge`
- `InnoVage - Orlando`
- `InnoVage - Tampa`

**`AccentCare - Broward` is a valid thirteenth label.** It exists in
`Partner_Locations` as an active location (code BRO) but was absent from
September traffic apart from REF-1545, which resolved to it.

## September 2026 correction

- Export: 107 rows, 47 columns. 60 correctly shaped. 47 had the full label in
  Partner Organization, with Partner Branch and Partner Lookup empty.
- 46 of the 47 resolved with the rules above. REF-1500 was blank on all four
  columns and could not be resolved (open).
- `Referrals_Partner_Fix_Sept2026.xlsx`, 46 rows, Referral ID plus the four
  partner columns, headers matching the export exactly. **The import of the 46
  corrected rows succeeded on the first try.**

---

# Part 2 - Partner data architecture (Session 53, 2026-09-24)

Measured from v53. Source: Session 53 log, PART 5. Intake root cause:
`docs/data/SOS_Referral_Intake_Root_Cause.md`.

Note: the split-on-first-separator rules above were written for the September
bulk correction. Going forward, matching is an exact lookup on
`Partner_Location_Label`, with no splitting (see the intake root cause doc).

## The four-level copy chain

Partner and branch data is duplicated across five fields per form, with
**seventeen distinct writers on `Partner_Branch` alone**.

| Level | Form | What it holds |
|---|---|---|
| 1 | `Partner_Locations` | the only real record; its ID is the key |
| 2 | `Partner_Referral_Contacts` | copies it |
| 3 | `Referrals_Main` | copies it again: `Partner_Branch_Link` plus `Partner_Organization`, `Partner_Branch`, `Partner_Location_Label`, `Partner_Branch_Submitted`, `Partner_ID` |
| 4 | `Encounter_PatientVisit` | copies it a third time: `Billing_Branch` plus three text fields |

## The three defects

1. The Zoho Form writes the branch label to `Partner_Organization`.
2. Resolution lives in on-user-input events, which never fire on an API
   submission.
3. Nothing validates that a text copy still agrees with its link, so they
   drift silently.

## Ruling

NEIL RULING: **link is truth, text is display.** One resolver writes every text
field; nothing else touches them. All 17 writers collapse to one.

Rejected:
- Dropping the text fields entirely. Touches every report, fax template and
  email.
- A drift validator alone. Fixes nothing structural.

## Nine-step plan - AGREED, NOT YET BUILT

Current versions from cchat, 2026-09-24. Steps 2 and 9 changed late in the
session, after the point the session log summarises.

1. **New function `partner_branch_values(int pLocationId)`, returns Map.**
   Given a Partner_Locations ID it returns the canonical
   `Partner_Organization`, `Partner_Branch`, `Partner_Location_Label`,
   `Partner_Link` and `Partner_ID`. The only place that text is ever composed.
2. **New function `resolve_branch_id(string pLabelText, string pOrgText,
   string pContactEmail, int pCurrentLink)`, returns the location ID.** Tries in
   order: the existing link, the contact's `Partner_Locations_Link`, an EXACT
   match on `Partner_Location_Label`, then the same exact match against
   `pOrgText`.
   SUPERSEDED: the original plan split the label on the first `" - "`. No
   longer needed, because `get_partner_referral_contact` now returns
   `Partner_Location_Label` and both the dropdown and the email lookup speak one
   string. **Do not implement splitting.**
3. **New On Validate on `Referrals_Main`.** If `Partner_Branch_Link` is empty,
   resolve it via `resolve_branch_id`. Then ALWAYS rewrite the four text fields
   from `partner_branch_values`, whether or not the link changed.
4. **Extend PVS Sets Billing Branch On Save** (Encounter_PatientVisit, Created
   or Edited, On Validate) to do the same for `Billing_Branch` on every save,
   not only when it is blank.
5. **Strip the text-field writes out of five workflows** so they set the LINK
   and nothing else: Sender Sets Branch, Referral Link Pre-Fill, Referral Sets
   Billing Branch, Branch Sets Partner, Has Referral_ID Show_Hide.
6. **Strip the text writes out of `process_new_referral` and DELETE its
   `if(v_SubmittedLabel != "")` gate.** It sets the link; the On Validate from
   step 3 does the rest. This is the root cause in
   `docs/data/SOS_Referral_Intake_Root_Cause.md`.
7. **One-time backfill** across Referrals_Main and Encounter_PatientVisit so
   existing records match the new resolver.
8. **Retire the drift-repair backfills** once steps 3 to 7 make drift
   impossible. Candidates: `backfill_referral_branch`,
   `backfill_referral_partner_fields`, `backfill_referral_branch_from_contact`,
   `resolve_referral_branch_from_text`. `backfill_pvs_from_referral` and
   `relink_pvs_to_referral` are a SEPARATE open question (they conflict with
   freeze-at-creation).
9. **Zoho Form. PARTLY DONE.** InnoVage - Orlando and VITAS - Villages added
   2026-09-24; the list now reconciles. STILL OPEN: rename the Partner
   Organization field to a branch label and remap it so the value lands in a
   branch field rather than `Partner_Organization`; add a conditional Set
   Fields as Mandatory rule making Facility Room # required when patient
   location is Facility.

### Sequencing

Steps 1 to 4 are additive and safe. Steps 5 and 6 change live intake and go
LAST, together, after 1 to 4 are proven on a test referral.
