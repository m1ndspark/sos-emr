# SOS Code - Session Log - 2026-08-17 (Session 33) - EOD

Covers Saturday 2026-08-15 through Monday 2026-08-17. Two tracks: the MPU
savings model was rebuilt a second time after Josh's clinical review, and the
referral notification emails were redesigned for SendGrid.

---

## Part 1 - MPU savings model, second rebuild

### Why it changed again

Session 32 corrected the comprehensive-APC packaging error. Neil then took that
to Josh, who raised two things that broke the corrected model:

1. A paracentesis is almost never performed in the ER. It happens in
   interventional radiology, and the real decision is outpatient versus admit.
2. Patients need a tap for many reasons, so the DRG should be ascites-generic,
   not cirrhosis-specific.

### What we built instead

Every procedure is now modeled **twice** and blended:

- **Pathway A** - treated and discharged, priced on the comprehensive APC.
- **Pathway B** - admitted, priced on the MS-DRG for the whole stay.

The blend weight is how often each actually happens in **Florida**, taken from
2025 Medicare Part B claims by place of service.

### Florida place-of-service splits (carrier 09102)

| Procedure | CPT | Inpatient | Outpatient | ER |
|---|---|---|---|---|
| Paracentesis | 49083 | 32.8% | 61.9% | 5.3% |
| Thoracentesis | 32555 | 76.1% | 21.4% | 2.5% |
| Catheter | 51702 | 26.8% | 10.2% | 63.0% |
| G-Tube | 43762 | 6.7% | 3.9% | 89.4% |

Josh was right - the ER is 5% of paracentesis, not the base case. Florida differs
from national most on catheter: 63% ER here vs 36% nationally. **Use Florida.**

### Wrong CPT found and fixed

We had been using **32557** for thoracentesis. That is pleural *drainage* by
indwelling catheter - a chest tube - and it is 98.6% inpatient. The aspiration
code is **32555**. This was wrong in every report since April.

### MS-DRGs adopted

| DRG | Description | Applies to |
|---|---|---|
| 393 | Other digestive system diagnoses with MCC | Paracentesis, G-tube |
| 186 | Pleural effusion with MCC | Thoracentesis |
| 695 | Kidney and urinary tract signs and symptoms with MCC | Catheter |

Always the **with MCC** tier. Ascites is a symptom, so it groups to 393-395, not
the cirrhosis family - that was Josh's correction to DRG 432.

### Blended benchmarks now in the reports

| Procedure | Discharged | Admitted | FL admit % | Blended |
|---|---|---|---|---|
| Paracentesis | 2,176.12 | 13,150.74 | 32.8% | 5,775.80 |
| Thoracentesis | 1,852.39 | 12,848.13 | 76.1% | 10,220.14 |
| Catheter | 1,779.11 | 9,683.52 | 26.8% | 3,897.49 |
| G-Tube | 1,792.10 | 13,091.97 | 6.7% | 2,549.19 |

### July savings, restated again

| Partner | Restated July 2026 |
|---|---|
| Empath | 237,682.63 |
| AccentCare | 77,884.92 |
| Chapters | 5,230.80 |
| VITAS | 3,574.49 |

These supersede **both** the original April-July figures and the Session 32
corrections. Only these are valid for month-over-month.

### New data sources added

- **IPPS Table 5** - MS-DRG relative weights and length of stay.
- **IPPS Tables 1A-1E** - national standardized amounts, capital rate.
- **PSPS claims file** - place-of-service mix, 840 MB, filter in place.
- **FL hospice per diems** - routine home care and general inpatient by county.

### Hospice per diem paragraph - new section

Every clinical report now carries "What This Means for [Partner]" under the
aggregate savings table. It states the published FY2026 routine home care and
general inpatient rates for the counties that partner's visits actually resolved
to, and makes the point that a day at home stays on the lower rate. It
deliberately makes **no** claim about what the partner pays its contracted
hospitals, because we cannot know that.

Neil's ruling: keep hospital cost as the primary table, add this as one
paragraph, not a second table. Villages spans three counties - use the highest,
which is Lake.

### Presentation changes

- All per-procedure CPT line-item tables **removed**. Neil: "people aren't likely
  checking the per line breakdowns." Replaced by three narrative paragraphs plus
  one range chart. Six or seven pages became about two.
- New chart: Estimated Hospital Cost per Episode. Dot at the discharged figure,
  dot at the admitted figure, diamond at the blend.
- Tables carry the blended figure only.
- Exec summary no longer says "Based on 2026 Medicare reference rates" - it names
  the blend method.
- Coverage line flipped to lead with what **is** covered rather than what falls
  outside.
- Branch charts adopted at the 15-visit threshold; below that, tables.
- Services Performed gets its own page when a partner has more than 8 service
  types, which fixed a near-blank page on Empath.
- Visit Complexity moved up to share page 3 with Time of Day.
- "Shown in clinical order" caption appears once, not four times.
- Three new disclaimers: Pathway Weighting, Nature of These Estimates, and an
  expanded How Medicare Pays covering the three-day payment window.

**July page counts:** Empath 23, AccentCare 17, Chapters 12, InnoVage 12,
VITAS 11.

---

## Part 2 - Referral notification emails

### Goal

Replace the Cognito notification with a sectioned, mobile-responsive email sent
from Creator through SendGrid.

### Decision: SendGrid dynamic template

Neil already built the template in SendGrid. Chosen because SendGrid templates
run Handlebars, so `{{#if Facility_Name}}...{{/if}}` handles show/hide inside the
template with no Deluge branching. Creator posts the data as JSON.

### Files built

All in `/Users/neilheird/Claude/MPU Reporting`:

- `referral_notification_email.html` - Patient Visit
- `referral_imaging_order_email.html` - Imaging Order

Both are email-safe: nested tables, every style inline, Arial, 600px max width,
media query for mobile stacking. **Do not** use the earlier
`two_column_table.html` pattern in email - `display:block` and CSS borders break
in Outlook.

### Sections - Patient Visit

| Section | Fields |
|---|---|
| Referral Info | Referral ID, Referral Date, Service Request Type, Referral Source |
| Patient Info | Name, DOB, Current Location, then address **or** facility block, Gender, Phone, additional contact block, Hospice ID |
| Medical Info | Reason for Referral, Goal for Care, Allergies, Anticoagulants, Advanced Directives |
| Partner Info | Referral Partner, Billing Branch, Referred By, Phone, Email, Clinical Team, Patient Program |

### Sections - Imaging Order

Same, except Medical Info is replaced by **Imaging Order Details**: Imaging Type,
Indication, Order Document. No Medical Info section.

### Neil's rulings

- Referral Source displays partner **and** billing branch together, e.g.
  "Empath Suncoast - HIL" or "AccentCare - PIN".
- Removed from Patient Info: Coordinate Visit With, MBI.
- Allergies, anticoagulants and advanced directives display the LIST / DETAIL
  fields, not the Yes/No parent answer.
- Blank fields should render "NA" - handled in Deluge before the merge, not in
  HTML. Recommended exception: allergies and anticoagulants should read
  "None reported", because NA is ambiguous in a clinical field.
- Imaging order document is **attached** to the email, not linked. A Creator file
  URL requires a login and field staff should only log in when creating a PVS.
  The row prints "Attached to this email".
- Recipients: Josh, Neil, and field staff.

### Field names confirmed from SOS_Referrals_App v24

```
Referral_ID | Referral_Date | Referral_Type | Partner_Organization |
Partner_Branch | Patient_Full_Name | Patient_DOB | Patient_Gender |
Patient_Phone | Patient_Location | Patient_Full_Address | Facility_Name |
Facility_Room_Number | Facility_Phone | AC_Full_Name | AC_Phone |
AC_Relationship_to_Patient | Has_Additional_Contact |
Patient_Hospice_ID | Referral_Reason | List_Patient_Allergies |
List_Patient_Anticoagulants | Advanced_Directives_Details |
Partner_POC_Name_Title | Partner_POC_Phone | Partner_POC_Email |
Partner_POC_Team | Imaging_Type_Order | Imaging_Order_Indication |
Imaging_Orders_Upload
```

### Three findings from v24

1. There is **no** Goal for Care field on `Referrals_Main`. `Goals_of_Care` lives
   on `Encounter_PatientVisit`. The Medical Info row Neil specified has no source
   on a referral - either drop it or add the field.
2. `Referral_Type` has **four** values, not three: Patient Visit, 3008,
   X-Ray Order (only), Lab Draw (only). Lab Draw still needs a template decision.
3. `send_via_sendgrid` **already exists** and works. It posts to
   `api.sendgrid.com/v3/mail/send` over connection `sendgrid_connection`, from
   notifications@sosreferrals.com. Nothing to set up - the new function just posts
   a template ID and a data map instead of raw HTML.

---

## Part 3 - Blocking / open

### Blocking - needed before the SendGrid function can be written

- SendGrid Dynamic Template ID.
- Ruling on Goal for Care: drop it, or add the field to `Referrals_Main`.
- Confirm a signed BAA covers PHI through SendGrid. These emails carry name, DOB,
  address and diagnosis.

### Not blocking

- 3008 notification template not started. Needs its field list.
- Lab Draw (only) template not started.
- Facility and additional-contact fields exist on the form; the email blocks for
  them are built but commented out pending wiring.
- `backfill_referral_added_time` still not run in Creator. Carried from
  Session 31.
- Nine service lines still have no hospital benchmark. 64 of Empath's 118 July
  visits sit outside the savings model.
- Imaging / X-Ray benchmark still blocked - SOS does not perform the study, the
  vendor bills hospice directly, and we do not have the vendor's rate.
- Clinical Team is free text on the form; a partner typed a phone number into it
  on REF-081626-1638. A picklist would fix it at the source.
- Data quality items unchanged from Session 32: 20xx-century DOBs, the
  byte-identical clinical note on PVS-1112-JK, name-particle imports, duplicate
  patients.

---

## Part 4 - Cold thread orientation

### Read in this order

1. `docs/mpu/SOS_MPU_Savings_Model_CY2026.md` - the two-pathway blended model.
2. `docs/mpu/SOS_MPU_Annual_Data_Refresh_Checklist.md` - all eight data sources,
   when each changes, and the traps.
3. `SOS_MPU_Reporting_Decisions_Log.md` - every ruling Neil has made. Not yet in
   this repo; held in the MPU Reporting folder.

### Build pipeline

All in `/root/mpu` on the session container:

```
build_base.py -> classify.py -> master.py -> insights.py
prep_partner.py <Partner> <Display>
charts_v2.py
node build_docx_v2.js <output.docx>
```

InnoVage is separate: `charts_innovage_v2.py` + `chart.py` + `build_innovage.js`.

The container is ephemeral. Re-download the CMS files each cycle.
