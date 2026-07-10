# Chat Handoff - SOS EMR Code-Side Session, 2026-07-09

Purpose: I did this work in Claude Code (code side), which cannot share threads with the
claude.ai chat side. This file is a self-contained brief so chat can follow, review, and
continue everything. All code below is already committed and pushed to the repo `sos-emr`
on branch `main` (HEAD = faeb9a1). This document is the reasoning + the code; the repo is
the durable store.

====================================================================
0. PROJECT PRIMER (read first)
====================================================================
- SOS EMR is a Zoho Creator application. The language is Deluge only. Never propose a
  non-Deluge or non-Creator solution for app work.
- Medical + billing context. Data integrity and correctness are critical; errors have real
  clinical and billing consequences.
- The LIVE Creator app is the source of truth. The repo mirrors it so all code is visible
  in one place and tracked in git.
- Owner: Neil Heird (operational lead, SOS Mobile Medical Care).
- Working loop:
    1. A workflow is designed/finalized.
    2. Claude writes/edits the `.dg` file in the repo.
    3. Claude runs a pre-commit audit (QA gate), then commits + pushes. Neil does not run git.
    4. Neil copies the code out of the repo and pastes it into Creator.
    5. Neil tests in Creator and reports pass/fail.
    6. Claude updates the status row in `_INDEX.md`. History lives in git.

HARD RULES chat must honor to produce usable output:
- Deluge / Creator only. Confirm live Creator behavior when syntax is in question; Creator
  behavior beats generic Deluge docs.
- NO em dashes anywhere in SOS content (code, docs, commit messages). Use hyphens.
- Never guess a form name, field link name, data type, relationship, or section name.
  Confirm against the `schema/` mirror (authoritative, auto-generated from live Creator) or
  the context files, or ask. Recurring bug class: link name vs display label; e.g.
  Partner_Location_Code vs Partner_Loc_Code.
- Forms and workflows are ONE unit. Any field change must be evaluated against every known
  workflow at the same time. Never propose a field change without the matching workflow change.
- ID generation always lives in its own workflow, never inline in On User Input.
- `.dg` files are PURE Deluge, no comment headers, full function (so they round-trip back
  into Creator cleanly). One file per workflow. File path encodes form + trigger, e.g.
  `Encounter_PatientVisit/OnUserInput__Referral_Link__PreFill.dg`.
- Never commit PHI, secrets, tokens, or test records. (A pre-commit hook blocks em dashes
  and SSN-shaped values.)
- Never describe Creator UI navigation from memory; the UI changes. Ask for a screenshot.
- `disable`/`enable`/`show`/`hide` are ACTIONS that fire on an event, not persistent field
  properties. Whatever state you want must be re-asserted on every relevant event.

GLOSSARY:
- PVS = Patient Visit = the `Encounter_PatientVisit` form.
- Referrals_Main = the referral intake form (fed by a public Zoho Form, mapped into Creator;
  NOT typed by humans in Creator).
- Referrals_Master = passive aggregate hub (hub-and-spoke; spokes insert into it on create).
- POC = point of contact. DM = decision maker.
- schema monitor = a process that auto-generates the `schema/*.md` field mirror from live Creator.

ARCHITECTURE CONTEXT THAT THE DECISIONS REST ON:
- Referrals_Main is populated by the Zoho Form integration, so On-User-Input workflows do
  NOT fire on inbound referrals (nobody types in the Creator form). PVS is DIRECT ENTRY
  (a provider types in Creator), so On-User-Input is the right trigger there.
- Partner data model (resolved 2026-07-04): Empath Health = ONE Partner with its hospices
  (Suncoast Hillsborough, Hospice of Marion County, Tidewell, Suncoast Pinellas) as
  Locations/branches. AccentCare = parent with multiple Locations. Standalone "PACE" =
  InnoVage / PACE. (Trustbridge parent still open.)
- Unresolved open contradictions live in context/04 (items 4-A, 4-B, 4-D). Do NOT silently
  decide them; ask before touching those areas.

THIS SESSION'S COMMITS (all pushed to main):
  faeb9a1 feat(phone): app-wide phone/fax format standard +1 (AAA) MMM-LLLL
  8de7bbb fix(pvs): hide Patient_Full_Name by default on load
  e7f3b5b feat(pvs): conditional referral lock with Edit_Needed override
  523aa1d fix(pvs): repair Referral_Link pre-fill pull + expand pulled fields
  9faaf25 / fdb5fb1 docs(context/11): PVS walkthrough + billing flow + charge-model correction
  98b58c5 docs: Session 10 referral flow + schema monitor reconciliation
  (plus schema-monitor auto-syncs of Encounter_PatientVisit)

====================================================================
A. PVS REFERRAL PRE-FILL + CONDITIONAL LOCK  (form: Encounter_PatientVisit)
====================================================================

GOAL: When a provider links a referral on a PVS record, auto-pull the patient/partner data
from Referrals_Main and lock those fields; still allow manual entry when there is no
referral; provide a manual override to edit locked fields.

DECISIONS:
1. LOCK TRIGGER = "Option B": fields lock ONLY when an actual referral is selected and
   matched (Referral_Link), NOT the moment "Do you have a Referral ID?" (Has_Referral_ID) is
   answered Yes. A disabled field therefore always means "came from a referral." This
   required REMOVING the field-disabling from the Has_Referral_ID = Yes branch (it used to
   lock on Yes = Option A).
2. WIPE ON DESELECT: clearing Referral_Link or switching Has_Referral_ID to No wipes all
   pulled values and re-enables the fields for manual entry.
3. NAME FIELDS: patient name = 3 split fields (Patient_First_Name / Patient_MI /
   Patient_Last_Name) plus a convenience concatenation Patient_Full_Name. RULE:
   Patient_Full_Name is visible ONLY when a referral is linked (locked display). Otherwise
   it is hidden and the 3 split fields are shown - including when unlocked for editing:
     - Referral linked + locked   -> show Full_Name, hide split fields
     - Editing (Edit_Needed = Yes) -> hide Full_Name, show + enable split fields
     - No referral / default load  -> hide Full_Name, show split fields
4. POST-SUBMIT LOCK is a SEPARATE, not-yet-built feature: "once a PVS is saved, most of the
   record cannot be edited; only specific fields are editable after initial submit." We
   deferred it. The referral lock only governs the live entry session.

MANUAL OVERRIDE - new field `Edit_Needed` (Radio, choices No / Yes), link name confirmed:
   ONE radio (not per-section). Edit_Needed = Yes unlocks ALL referral-prepopulated fields
   EXCEPT the System Fields section, and swaps Full_Name for the split name fields.
   Edit_Needed = No re-locks. Shown only when a referral is linked.

FIELD GROUPS:
   - Prepopulated set (locked on match; toggled by Edit_Needed): Patient_Full_Name,
     Patient_DOB, Patient_Gender, Patient_Address, Patient_Phone, Patient_Email,
     Patient_Hospice_ID, Patient_SSN, Facility_Name, Facility_Phone, Facility_Room_Number,
     Partner_Organization, Partner_Branch, Partner_POC_Phone, Partner_POC_Email,
     Partner_POC_Team, Partner_POC_Name_Title (+ the 3 split name fields via the swap).
   - System set (ALWAYS locked, never toggled by Edit_Needed): Referral_ID, Referral_ID_Stamp,
     Partner_ID, Partner_ID_Stamp, PVS_ID, Invoice_Status. These live in System_Fields_Section.

SECTION NAMES (confirmed live): System_Fields_Section (backend; hidden once a referral is
linked), Referral_Partner_Section (shown only when a referral is linked).

STALE PLACEHOLDER: the repo had OnUserInput__Type_of_Entry__Section_Visibility.dg, but that
workflow DOES NOT exist live (Neil confirmed). Left in place; flagged for a cleanup pass.

--------------------------------------------------------------------
FULL DELUGE - the 4 PVS workflows (final, as committed)
--------------------------------------------------------------------

### OnLoad__Default_Hide_On_Load.dg   (trigger: On Load)
```
hide Referral_Link;
hide Referral_ID;
hide PVS_Referral_ID;
hide Final_Clinical_Note_Section;
hide Type_of_Procedure_Section;
hide Visit_Cost_Drivers_Section;
hide Charges_Section;
hide Cares_3008_Completion_Section;
hide Imaging_Order_Section;
hide Lab_Order_Section;
hide Diversion_Tracking_Section;
hide Files_Upload_Section;
hide Type_of_Diversion;
hide Referral_Partner_Section;
hide Edit_Needed;
hide Patient_Full_Name;
show Patient_First_Name;
show Patient_MI;
show Patient_Last_Name;
hide Partner_POC_First_Name;
hide Partner_POC_Last_Name;
hide Partner_POC_Title;
hide Equipment_Charge_Amount;
hide Equipment_Charge_Details;
hide Other_Charges_Amount;
hide Other_Charges_Details;
disable Patient_First_Name;
disable Patient_MI;
disable Patient_Last_Name;
disable Patient_DOB;
disable Patient_Gender;
disable Patient_Address;
disable Employee_First_Name;
disable Employee_Last_Name;
disable Employee_Initials;
disable Employee_Title;
disable PVS_ID;
disable Referral_ID;
disable Referral_ID_Stamp;
disable Partner_ID;
disable Partner_ID_Stamp;
disable Invoice_Status;
```

### OnUserInput__Has_Referral_ID__Show_Hide.dg   (trigger: On User Input, field Has_Referral_ID)
```
if(input.Has_Referral_ID == "Yes")
{
	show Referral_Link;
	show Referral_ID;
	hide PVS_Referral_ID;
}
else if(input.Has_Referral_ID == "No")
{
	input.Referral_Link = null;
	input.Patient_Full_Name = null;
	input.Patient_First_Name = null;
	input.Patient_MI = null;
	input.Patient_Last_Name = null;
	input.Patient_DOB = null;
	input.Patient_Gender = null;
	input.Patient_Address = null;
	input.Patient_Hospice_ID = null;
	input.Patient_SSN = null;
	input.Patient_Phone = null;
	input.Patient_Email = null;
	input.Patient_Location = null;
	input.Facility_Name = null;
	input.Facility_Phone = null;
	input.Facility_Room_Number = null;
	input.Referral_ID = null;
	input.Referral_ID_Stamp = null;
	input.Partner_ID = null;
	input.Partner_ID_Stamp = null;
	input.Partner_Organization = null;
	input.Partner_Branch = null;
	input.Partner_POC_Team = null;
	input.Partner_POC_First_Name = null;
	input.Partner_POC_Last_Name = null;
	input.Partner_POC_Title = null;
	input.Partner_POC_Phone = null;
	input.Partner_POC_Email = null;
	input.Partner_POC_Name_Title = null;
	input.Edit_Needed = null;
	show PVS_Referral_ID;
	hide Referral_Link;
	hide Referral_ID;
	hide Referral_Partner_Section;
	hide Edit_Needed;
	show Patient_First_Name;
	show Patient_MI;
	show Patient_Last_Name;
	hide Patient_Full_Name;
	enable Patient_First_Name;
	enable Patient_MI;
	enable Patient_Last_Name;
	enable Patient_DOB;
	enable Patient_Gender;
	enable Patient_Address;
	enable Patient_Phone;
	enable Patient_Email;
	enable Patient_Hospice_ID;
	enable Patient_SSN;
	enable Facility_Name;
	enable Facility_Phone;
	enable Facility_Room_Number;
}
else
{
	hide Referral_Link;
	hide Referral_ID;
	hide PVS_Referral_ID;
	hide Referral_Partner_Section;
	hide Edit_Needed;
}
```

### OnUserInput__Referral_Link__PreFill.dg   (trigger: On User Input, field Referral_Link)
```
if(input.Referral_Link != null)
{
	v_Referral = Referrals_Main[ID == input.Referral_Link];
	v_Found = false;
	for each  v_Rec in v_Referral
	{
		input.Patient_Full_Name = v_Rec.Patient_Full_Name;
		input.Patient_First_Name = v_Rec.Patient_First_Name;
		input.Patient_MI = v_Rec.Patient_MI;
		input.Patient_Last_Name = v_Rec.Patient_Last_Name;
		input.Patient_DOB = v_Rec.Patient_DOB;
		input.Patient_Gender = v_Rec.Patient_Gender;
		input.Patient_Address = v_Rec.Patient_Address;
		input.Patient_Hospice_ID = v_Rec.Patient_Hospice_ID;
		input.Patient_SSN = v_Rec.Patient_SSN;
		input.Patient_Phone = v_Rec.Patient_Phone;
		input.Patient_Email = v_Rec.Patient_Email;
		input.Patient_Location = v_Rec.Patient_Location;
		input.Facility_Name = v_Rec.Facility_Name;
		input.Facility_Phone = v_Rec.Facility_Phone;
		input.Facility_Room_Number = v_Rec.Facility_Room_Number;
		input.Referral_ID = v_Rec.Referral_ID;
		input.Referral_ID_Stamp = v_Rec.Referral_ID_Stamp;
		input.Partner_ID = v_Rec.Partner_ID;
		input.Partner_ID_Stamp = v_Rec.Partner_ID_Stamp;
		input.Partner_Organization = v_Rec.Partner_Organization;
		input.Partner_Branch = v_Rec.Partner_Branch;
		input.Partner_POC_Team = v_Rec.Partner_POC_Team;
		input.Partner_POC_First_Name = v_Rec.Partner_POC_First_Name;
		input.Partner_POC_Last_Name = v_Rec.Partner_POC_Last_Name;
		input.Partner_POC_Title = v_Rec.Partner_POC_Title;
		input.Partner_POC_Phone = v_Rec.Partner_POC_Phone;
		input.Partner_POC_Email = v_Rec.Partner_POC_Email;
		input.Partner_POC_Name_Title = v_Rec.Partner_POC_First_Name + " " + v_Rec.Partner_POC_Last_Name + ", " + v_Rec.Partner_POC_Title;
		v_Found = true;
		break;
	}
	if(v_Found)
	{
		input.Edit_Needed = "No";
		show Edit_Needed;
		show Referral_Partner_Section;
		hide System_Fields_Section;
		show Patient_Full_Name;
		hide Patient_First_Name;
		hide Patient_MI;
		hide Patient_Last_Name;
		disable Patient_Full_Name;
		disable Patient_DOB;
		disable Patient_Gender;
		disable Patient_Address;
		disable Patient_Phone;
		disable Patient_Email;
		disable Patient_Hospice_ID;
		disable Patient_SSN;
		disable Facility_Name;
		disable Facility_Phone;
		disable Facility_Room_Number;
		disable Partner_Organization;
		disable Partner_Branch;
		disable Partner_POC_Phone;
		disable Partner_POC_Email;
		disable Partner_POC_Team;
		disable Partner_POC_Name_Title;
	}
}
else
{
	input.Patient_Full_Name = null;
	input.Patient_First_Name = null;
	input.Patient_MI = null;
	input.Patient_Last_Name = null;
	input.Patient_DOB = null;
	input.Patient_Gender = null;
	input.Patient_Address = null;
	input.Patient_Hospice_ID = null;
	input.Patient_SSN = null;
	input.Patient_Phone = null;
	input.Patient_Email = null;
	input.Patient_Location = null;
	input.Facility_Name = null;
	input.Facility_Phone = null;
	input.Facility_Room_Number = null;
	input.Referral_ID = null;
	input.Referral_ID_Stamp = null;
	input.Partner_ID = null;
	input.Partner_ID_Stamp = null;
	input.Partner_Organization = null;
	input.Partner_Branch = null;
	input.Partner_POC_Team = null;
	input.Partner_POC_First_Name = null;
	input.Partner_POC_Last_Name = null;
	input.Partner_POC_Title = null;
	input.Partner_POC_Phone = null;
	input.Partner_POC_Email = null;
	input.Partner_POC_Name_Title = null;
	input.Edit_Needed = null;
	hide Edit_Needed;
	hide Referral_Partner_Section;
	show Patient_First_Name;
	show Patient_MI;
	show Patient_Last_Name;
	hide Patient_Full_Name;
	enable Patient_First_Name;
	enable Patient_MI;
	enable Patient_Last_Name;
	enable Patient_DOB;
	enable Patient_Gender;
	enable Patient_Address;
	enable Patient_Phone;
	enable Patient_Email;
	enable Patient_Hospice_ID;
	enable Patient_SSN;
	enable Facility_Name;
	enable Facility_Phone;
	enable Facility_Room_Number;
}
```

### OnUserInput__Edit_Needed__Unlock.dg   (trigger: On User Input, field Edit_Needed)
```
if(input.Edit_Needed == "Yes")
{
	hide Patient_Full_Name;
	show Patient_First_Name;
	show Patient_MI;
	show Patient_Last_Name;
	enable Patient_First_Name;
	enable Patient_MI;
	enable Patient_Last_Name;
	enable Patient_DOB;
	enable Patient_Gender;
	enable Patient_Address;
	enable Patient_Phone;
	enable Patient_Email;
	enable Patient_Hospice_ID;
	enable Patient_SSN;
	enable Facility_Name;
	enable Facility_Phone;
	enable Facility_Room_Number;
	enable Partner_Organization;
	enable Partner_Branch;
	enable Partner_POC_Phone;
	enable Partner_POC_Email;
	enable Partner_POC_Team;
	enable Partner_POC_Name_Title;
}
else
{
	show Patient_Full_Name;
	hide Patient_First_Name;
	hide Patient_MI;
	hide Patient_Last_Name;
	disable Patient_Full_Name;
	disable Patient_DOB;
	disable Patient_Gender;
	disable Patient_Address;
	disable Patient_Phone;
	disable Patient_Email;
	disable Patient_Hospice_ID;
	disable Patient_SSN;
	disable Facility_Name;
	disable Facility_Phone;
	disable Facility_Room_Number;
	disable Partner_Organization;
	disable Partner_Branch;
	disable Partner_POC_Phone;
	disable Partner_POC_Email;
	disable Partner_POC_Team;
	disable Partner_POC_Name_Title;
}
```

====================================================================
B. APP-WIDE PHONE / FAX FORMAT STANDARD
====================================================================

*** SUPERSEDED 2026-07-10 (chat session). The mask changed from +1 (AAA) MMM-LLLL
to AAA-MMM-LLLL, and the formatter now uses strip/reject behavior with a re-entry
guard plus a paired On-Validate and a field tooltip. The ORIGINAL +1 (AAA) spec is
kept below under "SUPERSEDED ORIGINAL" for history. Use the NEW STANDARD for all
rollout. Reference implementation proven live: Partner_Billing_Contacts (phone + fax). ***

--------------------------------------------------------------------
NEW STANDARD (2026-07-10) - proven live on Partner_Billing_Contacts
--------------------------------------------------------------------
MASK: AAA-MMM-LLLL   e.g.  813-555-1234   (no +1, no parentheses)

THREE LAYERS per phone/fax field (all three required):
  1. FIELD TOOLTIP (Creator field property, not code, not in schema mirror):
     "Enter exactly 10 digits. Exclude dashes and parentheses."
  2. ON-USER-INPUT FORMATTER (one .dg per field): strips non-digits; formats ONLY
     on exactly 10 digits; collapses to raw digits on any invalid length (so a
     wrong-length entry visibly reads as unformatted, not a stale-dashed mask);
     re-entry guard prevents an infinite format loop.
  3. ON-VALIDATE (form-level, one workflow per form): blocks submit with a
     per-field alert if a filled phone/fax is not exactly 10 digits.

BEHAVIOR DECISIONS:
  - REJECT, not trim: a non-10-digit entry is NOT silently trimmed to 10 (that
    could hide a typo on a billing contact). It stays unformatted and On-Validate
    blocks the save.
  - Phone/fax are OPTIONAL: validated only if filled (!= null && != "").
  - Do NOT set field max-characters as the cap: the formatted value (12 chars) is
    longer than 10 raw digits, so a low max-char fires Creator's generic "Invalid
    entries found" popup BEFORE the custom On-Validate alert. Leave max-char
    generous/unset; the formatter + On-Validate do the enforcement.

FORMATTER TEMPLATE (substitute the field link name for FIELD):
```
v_Raw = input.FIELD.toString();
v_Digits = v_Raw.replaceAll("[^0-9]","");
if(v_Digits.length() != 10)
{
	if(v_Raw != v_Digits)
	{
		input.FIELD = v_Digits;
	}
	return;
}
v_Formatted = v_Digits.subString(0,3) + "-" + v_Digits.subString(3,6) + "-" + v_Digits.subString(6,10);
if(v_Raw == v_Formatted)
{
	return;
}
input.FIELD = v_Formatted;
```

ON-VALIDATE SNIPPET (add one block per phone/fax field on the form; combine with
any existing On-Validate logic - a form has ONE On-Validate workflow):
```
if(input.FIELD != null && input.FIELD != "")
{
	v_digits = input.FIELD.replaceAll("[^0-9]","");
	if(v_digits.length() != 10)
	{
		alert "Phone number must be exactly 10 digits (numbers only).";
		cancel submit;
	}
}
```
(Use "Fax number..." wording for fax fields.)

ROLLOUT STATUS:
  - DONE + tested live: Partner_Billing_Contacts (Partner_Billing_POC_Phone,
    Partner_Billing_POC_Fax). Fax field renamed from Partner_Billing_POC_Phone1
    to Partner_Billing_POC_Fax; old formatter file retired.
  - TODO (update to new mask + add On-Validate + tooltip): Referrals_Main
    (Patient_Phone, Decision_Maker_Phone, Facility_Phone, Partner_POC_Phone) -
    NOTE these are Zoho-Form-fed so On-User-Input does NOT fire inbound (see C-1);
    Encounter_PatientVisit (Patient_Phone, Facility_Phone, Partner_POC_Phone);
    Assignments (Patient_Phone, Facility_Phone); Employees (Employee_Phone);
    Partners (Partner_Phone); X_Ray_Orders (Patient_Phone, X_Ray_Results_Fax).
  - Roll out ONE FORM AT A TIME; Neil tests each before the next.

--------------------------------------------------------------------
SUPERSEDED ORIGINAL (2026-07-09) - kept for history, do NOT use
--------------------------------------------------------------------
DECISION: every phone AND fax field, on EVERY form, uses one viewing mask:
   +1 (AAA) MMM-LLLL      e.g.  +1 (813) 555-1234
(Preferred. Acceptable fallback was X-XXX-XXX-XXXX; we chose the +1 (AAA) form.)

WHY A FORMATTER: Creator has no input mask, and the native Phone field type (type 27)
renders as +1XXXXXXXXXX (E.164), which is not wanted. So each phone field is a Single Line
text field with an On-User-Input formatter that normalizes typed input.

FIELD-TYPE CONVERSION (Neil, Creator side): native Phone fields must be DELETED and rebuilt
as Single Line text fields WITH THE IDENTICAL LINK NAME, then the formatter pasted. Same
link name is critical - the PVS pre-fill/lock and every other reference key off these names.
Referrals_Main phone fields were already Single Line; only their mask changed. Converting
PVS phones to Single Line also removes a pre-fill type-coercion risk.

FORMATTER LOGIC (shared template; substitute the field link name):
```
v_Raw = input.FIELD.toString();
if(v_Raw.startsWith("+1 ("))
{
	return;
}
v_Digits = v_Raw.replaceAll("[^0-9]","");
if(v_Digits.length() < 10)
{
	return;
}
v_Digits = v_Digits.subString(v_Digits.length() - 10,v_Digits.length());
v_Area = v_Digits.subString(0,3);
v_Mid = v_Digits.subString(3,6);
v_Last = v_Digits.subString(6,10);
input.FIELD = "+1 (" + v_Area + ") " + v_Mid + "-" + v_Last;
```

15 FORMATTERS WRITTEN (file per field: OnUserInput__<Field>__Format.dg in each form folder):
   Referrals_Main:           Patient_Phone, Decision_Maker_Phone, Facility_Phone, Partner_POC_Phone  (mask updated; trigger unchanged)
   Encounter_PatientVisit:   Patient_Phone, Facility_Phone, Partner_POC_Phone
   Assignments:              Patient_Phone, Facility_Phone
   Employees:                Employee_Phone
   Partners:                 Partner_Phone
   Partner_Billing_Contacts: Partner_Billing_POC_Phone, Partner_Billing_POC_Phone1 (Fax)
   X_Ray_Orders:             Patient_Phone, X_Ray_Results_Fax

====================================================================
C. OPEN ITEMS / VERIFY-LIVE  (decisions still needed or things to confirm in Creator)
====================================================================
1. ZOHO FORM PHONE OUTPUT: On-User-Input formatters do NOT fire on the Zoho Form
   integration path, so inbound Referrals phones rely on the Zoho Form ALREADY outputting
   +1 (AAA) MMM-LLLL. Confirm what the Zoho Form actually outputs. If it differs, we need an
   On-Create/Edit normalizer (or a Zoho Form change) so inbound is standardized.
2. PATIENT_FULL_NAME RECONCILIATION: there is NO PVS workflow that rebuilds Patient_Full_Name
   from the split names. If a provider unlocks (Edit_Needed = Yes) and edits the split names,
   the stored Full_Name can go stale. DECISION NEEDED: add a concatenator or not.
3. PROGRAMMATIC PHONE PATHS: any form where a phone value is created by a workflow insert or
   import (not typed, not copied from an already-formatted source) bypasses the On-User-Input
   formatter. Confirm per form.
4. POST-SUBMIT LOCK regime for PVS (most fields read-only after save; only specific fields
   editable) is a separate, not-yet-designed feature.
5. PHONE TYPE COERCION on the PVS pre-fill is resolved once PVS phone fields become Single Line.
6. SSN CONTEXT (background): SSN is formatted entirely by the Zoho Form (passes XXX-XX-XXXX);
   Creator's SSN On-User-Input formatter is inert on the integration path.
7. context/04 open contradictions 4-A, 4-B, 4-D remain unresolved; do not silently decide.

====================================================================
D. CREATOR-SIDE CHECKLIST FOR NEIL (to go live)
====================================================================
1. Create the `Edit_Needed` Radio field (No / Yes) at the top of the PVS referral-populated area.
2. Paste the 4 PVS workflows in this order: OnLoad__Default_Hide_On_Load ->
   OnUserInput__Has_Referral_ID__Show_Hide -> OnUserInput__Referral_Link__PreFill ->
   OnUserInput__Edit_Needed__Unlock.
3. For every native Phone/Fax field on every form: delete it, rebuild as Single Line with the
   SAME link name, paste the matching formatter. Referrals: just repaste the 4 updated ones.
4. Test, then report pass/fail so the code-side _INDEX verified flags get updated.

====================================================================
E. FIELD LINK NAMES (from the schema mirror; authoritative)
====================================================================

--- Encounter_PatientVisit (PVS), 65 fields ---
Has_Referral_ID (Radio: No,Yes), Referral_Link (Lookup), PVS_Referral_ID, Type_of_Entry
(Dropdown: Patient Visit,3008,Lab Order,X-Ray Order,Clinic Hours), Patient_Full_Name,
Patient_First_Name, Patient_MI, Patient_Last_Name, Patient_DOB (Date), Patient_Gender
(Dropdown: Female,Male), Patient_Hospice_ID, Patient_SSN, Patient_Phone (Phone->converting to
Single Line), Patient_Email (Email), Patient_Location (Radio: Home,Facility), Facility_Name,
Facility_Phone (Phone->Single Line), Facility_Room_Number, Patient_Address (Address),
Clinical_Note_Type (Dropdown: Final,Addendum), Final_Clinical_Note, Final_Note_File_Upload,
ICD_10_Search, ICD_10_Codes, Type_of_Procedure (Checkbox), Complexity_Level (Radio: High
Complexity,Moderate Complexity,Low Complexity,Hospital at Home,No Charge), Additional_Charges
(Checkbox: After Hours,Super STAT Fee,Equipment Charge,Other), After_Hours_Fee (Currency),
Super_Stat_Fee (Currency), Equipment_Charge_Amount (Currency), Equipment_Charge_Details,
Other_Charges_Amount (Currency), Other_Charges_Details, PVS_File_Upload, Diversion_Tracking
(Radio: No,Yes), Type_of_Diversion (Dropdown), Partner_Organization, Partner_Branch,
Partner_POC_Name_Title, Partner_POC_Team, Partner_POC_First_Name, Partner_POC_Last_Name,
Partner_POC_Title (Dropdown: MD,DO,APRN,PA,Team Leader,RN,MSW,Care Manager,Admin),
Partner_POC_Phone (Phone->Single Line), Partner_POC_Email (Email), Was_3008_Completed (Radio:
No,Yes), Notes_3008, Cares_3008_Completion_Date (Date), Imaging_Type_Order,
Imaging_Order_Indication, Imaging_Order_Date (Date), Lab_Type_Orders, Lab_Order_Indication,
Lab_Order_Date (Date), Employee_First_Name, Employee_Last_Name, Employee_Title (Dropdown:
MD,DO,APRN,PA,RN,Paramedic), Employee_Initials, Visit_Completion_Date (Date), PVS_ID,
Referral_ID, Referral_ID_Stamp, Partner_ID, Partner_ID_Stamp, Invoice_Status (Radio: Draft,Final).
Sections referenced by the lock: System_Fields_Section, Referral_Partner_Section (+ the new
Edit_Needed field).

--- Referrals_Main (source of the pre-fill), 56 fields ---
Referral_Source (Radio: Contracted Parnter[sic],SOS Internal), Referral_Type (label "Service";
Radio: Patient Visit,3008,X-Ray Order (only),Lab Draw (only)), Requested_Priority (Radio:
Routine,Priority), SOS_Prior_Service (Radio: No,Yes), Patient_First_Name, Patient_MI,
Patient_Last_Name, Patient_DOB (Date), Patient_Gender (Radio: Female,Male), Patient_Hospice_ID,
Patient_SSN, Patient_Phone (Single Line), Patient_Email (Email), Patient_Responsibility (Radio:
No,Yes), DM_First_Name, DM_Last_Name, Decision_Maker_Phone (Single Line), Decision_Maker_Email
(Email), Decision_Maker_Relationship_to_Patient (Dropdown: Advocate,Family/Friend,Legal
Representative), Patient_Location (Radio: Home,Facility), Facility_Name, Facility_Phone (Single
Line), Facility_Room_Number, Patient_Address (Address), Referral_Reason, Goals_of_Care,
X_Ray_Needed (Radio: No,Yes,I'm Not Sure), Patient_Has_Allergies, List_Patient_Allergies,
Patient_Has_Anticoagulants, List_Patient_Anticoagulants, Patient_Has_Advanced_Directives
(Radio: No,Yes), Advanced_Directives_Details (Multi Line), Additional_Information,
General_Files_Upload, Reason_for_X_Ray_Request, Upload_X_Ray_Request_Files,
Reason_for_Lab_Request, Requested_Lab_Vendor, Upload_Lab_Request_Files, Partner_Link (Lookup to
Partners), Partner_Organization, Partner_Branch, Partner_POC_First_Name, Partner_POC_Last_Name,
Partner_POC_Title (Dropdown, same choices as PVS), Partner_POC_Team, Partner_POC_Phone (Single
Line), Partner_POC_Email (Email), Referral_ID (unique), Referral_Date (Date), Referral_ID_Stamp,
Patient_Full_Name, Partner_POC_Name_Title, Partner_ID, Partner_ID_Stamp.

NOTE on the pre-fill: PVS pulls from Referrals_Main[ID == input.Referral_Link] and copies the
matching fields. Partner_POC_Name_Title is COMPUTED in the pre-fill as
First + " " + Last + ", " + Title (Referrals also stores its own copy). The PVS pre-fill hides
the Referrals split-name convention and shows Patient_Full_Name when locked.
```
