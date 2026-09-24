# SOS Provider Portal and PVS Validation Model

Design agreed 2026-09-24 (Session 53). NOTHING BUILT. Source: Session 53 log,
PART 8.

## 1. Structure

**Provider Dashboard**, three boxes:

| Box | Source | Opens |
|---|---|---|
| My Info | Employees record | - |
| My Assignments | Referrals_Main, filtered to the provider | Assignments page |
| My PVS Notes | Encounter_PatientVisit, filtered to the provider | PVS page |

**Assignments page.** A filtered referrals table. Basic fields visible, full
record on edit, and an action-item column on every row: Update Visit Status,
patient not yet Called, and so on.

**PVS page.** Completed notes, plus assigned patients with no note yet. Those
rows get a Start PVS button that is either live or DISABLED WITH THE REASON
SHOWING. Never a greyed row that says nothing.

## 2. The pattern

Both pages are one pattern: a table where every row carries its next action.

## 3. PVS_Status (new field)

On Encounter_PatientVisit.

| Value | Stored? | Meaning |
|---|---|---|
| Not Started | NO, computed | assigned referral with no PVS row |
| In Progress | yes | PVS exists, fails the completeness check |
| Completed | yes | PVS passes the completeness check |

- Not Started is deliberately NOT stored. Pre-creating PVS records would
  produce exactly the empty notes the app already has 23 of.
- Set automatically on save. The provider never touches it.
- Failing the check leaves In Progress and generates action items.
- NEIL RULING: `Assignment_Status` on Referrals_Main does NOT gate the PVS.
  Gating on a field a human must remember to update is how the feature dies.

## 4. The validation model

JOSH'S RULING (2026-09-23), now a principle: nothing blocks a PVS save, not
even inaccurate data.

Correctness moves from a wall at submit to an action item on a list. An
incomplete PVS becomes a task, not a blocked save.

### Two kinds of required

| Kind | Meaning | Where it belongs |
|---|---|---|
| Required to EXIST | needed on the record to bill and fax | checked, routed to whoever owns it |
| Required as PROVIDER INPUT | the provider must supply it | the PVS form |

- Only provider input belongs on the PVS form.
- Inherited referral data is already validated at the referral and must not
  be re-demanded.
- A field the provider CANNOT EDIT must never block them. It routes to the
  admin action list.

### Mechanism

- An On Load workflow computes what is missing, including hidden fields, and
  writes it to a read-only panel at the top of the form before the provider
  types. Proven mechanism: this is how Print_Preview works.
- Native field Mandatory is RULED OUT. It blocks the save and fires before
  workflows, which would break the 3008 Reason default and the Patient_DOB1
  parse.
- PVS Required Fields is KEPT but repurposed: stop validating, start
  computing PVS_Status and the missing-items panel.

### How we got here (Neil's diagnosis, the design principle going forward)

Required fields were set on the referral, then the same fields were pulled into
the PVS as a visit guide, then set required there too, and hidden from the
provider. The PVS became a wall demanding data the provider could not supply.

## 5. Data ownership rule

The PVS owns workflows ONLY for data originating on it:

- visit status and date
- note type and body
- ICD, procedures
- complexity and charges
- diversion
- 3008 and imaging fields

Patient data is maintained on Referrals_Main. Provider data on Employees. The
PVS originates neither.

### Freeze at creation

Inherited values are written ONCE AT CREATION AND FROZEN. A signed note is a
point-in-time record; a patient moving next month must not alter last month's
note.

This contradicts `backfill_pvs_from_referral` and `relink_pvs_to_referral`,
which resync. Their fate is undecided.

### Found while mapping ownership

- Build Patient Full Address exists on BOTH Encounter_PatientVisit and
  Referrals_Main, both on user input of `Patient_Address`. The PVS copy is
  redundant; a provider does not type an address there. To be deleted.
- Concatenation sprawl, same disease as the partner fields:
  - `Employee_Name_Title` / `Employee_Full_Name` - 7 writers
  - `Patient_Full_Address` - 5 writers

## 6. Open questions (decide before building)

1. Do `Type_of_Procedures` and `Provider_ICD10_Codes_Link` count toward
   Completed, or are they advisory? This blocks the completeness set, which
   blocks PVS_Status.
2. What happens when a provider starts a SECOND note for the same patient?
   Unaddressed in the app today.

## 7. Related

- Portal access ruling (one link, one login): `context/23_task_list.md`,
  "Build the provider portal" row.
- Platform decision, which the portal feeds into:
  `Claude outputs/SOS_EMR_v2_Platform_Case_2026-09-24.md`.
