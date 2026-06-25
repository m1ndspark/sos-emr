# Zoho Form reference — Referrals_Main

The public-facing referral form is a Zoho Form, NOT a Creator form. Respondents
never touch the Creator Referrals_Main form; the Zoho Form is mapped into it and
only stores data for backend processing. All conditional field logic (show/hide,
required, page skips) lives in Zoho Forms, not in Creator. Record it here so the
Creator side is not rebuilt to duplicate it. This is reference only, not Deluge.

Zoho Form name: "Patient Referral"
Maps to Creator form: Referrals_Main
Front-end formatting handled by Zoho Forms: phone (NOT SSN — SSN is formatted in
Creator, see _INDEX.md NOTE 7).

--------------------------------------------------------------------------------
RULE CATEGORIES PRESENT (Zoho Forms > Rules)
--------------------------------------------------------------------------------
- Field Rules           show/hide fields based on input   (captured below, partial)
- Choice-based Field Rules  show/hide choices in a field   (not reviewed yet)
- Form Rules            actions on form submission         (not reviewed yet)
- Page Rules            skip to pages based on input       (not reviewed yet)
- Deny Submissions      block submission based on input    (not reviewed yet)

--------------------------------------------------------------------------------
FIELD RULES
--------------------------------------------------------------------------------
Status: captured = full IF/THEN recorded; PENDING = name only, expand in Zoho to capture.

1. Patient Allergies            | captured
     IF   "Does the patient have allergies?" Is "Yes"
     THEN Show "List all allergies"

2. Patient Anticoagulants       | PENDING (expand to capture IF/THEN)
3. Patient Advanced Directives  | PENDING
4. 3008                         | PENDING (likely tied to the PACE 3008 assessment)
5. Patient Location - Home      | PENDING
6. Patient Location - Facility  | PENDING

--------------------------------------------------------------------------------
OPEN ITEMS
--------------------------------------------------------------------------------
- Expand field rules 2-6 and the other four rule categories to complete this note.
- Map each Zoho Form field to its Creator Referrals_Main field link name (labels
  here are Zoho Form labels, which may differ from Creator link names).
