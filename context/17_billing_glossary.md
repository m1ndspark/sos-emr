# SOS EMR Canonical Billing Glossary

Prepared: Friday, July 17, 2026 (Session 19). Signed off.
Anchor: Partner_Rates is the rate card and the source of truth for every billable
term. Everything from the PVS through the invoice uses these terms exactly.

--------------------------------------------------------------------------------
## 1. Canonical taxonomy (from Partner_Rates)
--------------------------------------------------------------------------------
A rate row is Rate_Category + Rate_Type + Rate_Amount, effective-dated, with a
Current flag and Active status, keyed to Partner and Location.

Rate_Category: Acuity Level, Premium, Service, Other.
Rate_Type (canonical spelling in quotes), grouped by the category it belongs to:

  Acuity Level (one per visit):
    "High Complexity", "Moderate Complexity", "Low Complexity", "Hospital at Home",
    "Telemedicine", "Care Coordination", "General Consultation",
    "Cares 3008 Assessment"
  Premium (zero or more per visit, add-ons):
    "After Hours", "Super STAT"
  Service:
    reserved. No Rate_Type values today. Use for future service-based rates.
  Other:
    catch-all. Priced manually, no rate row required.

Billing state, NOT an acuity: "No Charge" means a completed visit that bills $0. It
is a state of the acuity field, not a rate type. It has no Partner_Rates row.

Manual charges, NOT rate types: "Equipment Charge" and "Other" are entered by hand on
the PVS and have no rate row.

--------------------------------------------------------------------------------
## 2. PVS to canonical mapping
--------------------------------------------------------------------------------
Acuity: PVS field Complexity_Level (single-select), one per visit.
  Canonical: the eight Acuity Level types above, plus No Charge.
  Applied: the four missing types (Telemedicine, Care Coordination,
           General Consultation, Cares 3008 Assessment) added in Creator so every
           acuity the rate card prices can be selected.

Add-ons: PVS field Additional_Charges (multi-select checkboxes), the next field,
  where the provider adds items if warranted.
  Canonical: "After Hours", "Super STAT" (Premiums), plus Equipment Charge and Other
             (manual).
  Applied: label "Super STAT Fee" changed to "Super STAT" to match the rate card.

Charge amount fields (storage, link names unchanged): Complexity_Charge,
  After_Hours_Fee, Super_Stat_Fee, Equipment_Charge_Amount, Equipment_Charge_Details,
  Other_Charges_Amount. For launch these dollar amounts are entered manually. No
  rate-card auto-lookup.

Addendum (record only, does NOT bill): Encounters_PVSAddendum field PVS_Charge_Type
  (display "PVS Charge Type"). This is an addendum correction/supplemental charge-type,
  not a second primary acuity. Do not wire the invoice to it. Applied: "After Hours
  Charge" changed to "After Hours" and "Super STAT Fee" to "Super STAT" for label
  consistency only. The addendum's own Equipment_Charge_Amount is also record-only.

--------------------------------------------------------------------------------
## 3. Invoice line naming (PVS to Books)
--------------------------------------------------------------------------------
Each finalized PVS is one visit and contributes lines built from its flat charge
fields, described in canonical terms:
  Acuity line:    the Complexity_Level value (e.g. "High Complexity"), amount from
                  Complexity_Charge. "No Charge" is omitted from the invoice, kept on
                  the PVS.
  Premium lines:  "After Hours" (After_Hours_Fee), "Super STAT" (Super_Stat_Fee),
                  each only if selected in Additional_Charges and amount > 0.
  Equipment line: "Equipment Charge" with Equipment_Charge_Details as the note,
                  amount from Equipment_Charge_Amount.
  Other line:     "Other" from Other_Charges_Amount.

One visit is one PVS is one row. A second visit is another PVS and another row.

--------------------------------------------------------------------------------
## 4. Label normalizations applied (pre-launch, no live billing data depends on them)
--------------------------------------------------------------------------------
- PVS Complexity_Level: added Telemedicine, Care Coordination, General Consultation,
  Cares 3008 Assessment.
- PVS Additional_Charges: "Super STAT Fee" becomes "Super STAT".
- Addendum PVS_Charge_Type: "After Hours Charge" becomes "After Hours"; "Super STAT
  Fee" becomes "Super STAT".
- Option values kept identical in spelling and case to Partner_Rates Rate_Type.
- Field link names are NOT changed. Only picklist option values and display labels.
- Verified no Deluge workflow logic keys on the old strings.

--------------------------------------------------------------------------------
## 5. Signed-off decisions
--------------------------------------------------------------------------------
1. Add the four missing acuity types to PVS Complexity_Level. YES. Applied in Creator.
2. Rate_Type to Rate_Category pairing in Section 1 (Acuity vs Premium). CONFIRMED.
3. A "No Charge" visit is omitted from the invoice, kept on the PVS. CONFIRMED.
4. For launch the invoice reads PVS charge fields only. Corrections are made on the
   approval dashboard via editable overrides. Every addendum (correction or
   supplemental) is record-only for 8/3. CONFIRMED.
5. Charge amounts are entered manually on the PVS for 8/3. Rate-card auto-pricing is
   the first-week fast-follow. CONFIRMED.
6. Label normalizations applied in Creator (the three fields in Section 4). DONE.

--------------------------------------------------------------------------------
## 6. Post-launch list (parked)
--------------------------------------------------------------------------------
- Rate-card auto-pricing: the PVS looks up the Active Partner_Rates amount by partner,
  branch, and type as of date of service, filling the dollar fields instead of manual
  entry. First-week fast-follow.
- Supplemental-addendum billing, only if a follow-up is ever billed as an addendum
  instead of a new PVS. Not needed while one visit is one PVS is one row.
- Primary record-lookup view: a top-level screen showing a referral header plus all
  associated PVS entries, for investigation and oversight, not billing-bound.
- Reporting data cards across referrals, PVS, and invoicing.

--------------------------------------------------------------------------------
END
--------------------------------------------------------------------------------
