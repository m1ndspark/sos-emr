# SOS MPU - Hospital Savings Model, CY2026

**Two-pathway blended model. Adopted 2026-08-17 (Session 33).**

**This file is canonical.** The copy in the MPU Reporting folder is a working
copy. If the two disagree, this one wins. Reconciled against the working copy
2026-08-19 (Session 34): FY2026 DRG weights and GMLOS, the 32555 physician fee,
the admitted pathway component breakdown, the explicit IPPS formula, and the
IPPS outlier / DSH / IME exclusion note were merged in from it.

Supersedes the single-pathway model adopted 2026-08-15 (Session 32), and every
hospital cost figure in `SOS_MPU_Reporting_Instructions_v1.md` and in the
Decisions Log section 3.

---

## Why the model changed a second time

Session 32 fixed a real error - the April-July reports double-counted services
that are packaged into a Comprehensive APC. That fix stands and is documented
below. But the corrected model still priced every episode as a single
hospital-outpatient encounter, and clinical review with Neil broke that
assumption on two points:

1. **A paracentesis is almost never performed in the ER.** It happens in
   interventional radiology. The real decision is outpatient versus admit, not
   ER versus nothing.
2. **Patients need a tap for many reasons.** The DRG has to be ascites-generic,
   not cirrhosis-specific. That retired the DRG 432 (cirrhosis) assumption.

An episode does not have one price. It has two, and which one applies depends on
whether the patient goes home or gets admitted.

---

## The two pathways

Every procedure is now modeled **twice** and blended:

| | Pathway A | Pathway B |
|---|---|---|
| **Scenario** | Treated and discharged | Admitted |
| **Priced on** | OPPS facility payment for the encounter | MS-DRG for the whole stay (IPPS) |
| **Covers** | The outpatient/ER encounter, everything packaged into it, plus round-trip ambulance | The full inpatient admission |

The blend weight is **how often each actually happens in Florida**, taken from
2025 Medicare Part B claims by place of service. Admitted share drives Pathway B;
outpatient plus ER drives Pathway A.

```
Blended = Discharged x (outpatient% + ER%) + Admitted x (inpatient%)
```

---

## Florida place-of-service splits (PSPS 2025, carrier 09102)

| Procedure | CPT | Inpatient | Outpatient | ER |
|---|---|---|---|---|
| Paracentesis | 49083 | 32.8% | 61.9% | 5.3% |
| Thoracentesis | 32555 | 76.1% | 21.4% | 2.5% |
| Catheter | 51702 | 26.8% | 10.2% | 63.0% |
| G-Tube | 43762 | 6.7% | 3.9% | 89.4% |

The ER is 5% of paracentesis, not the base case.

**Use Florida, not national.** They diverge most on catheter management: 63% ER
in Florida against 36% nationally.

HOW TO REPRODUCE THE TABLE ABOVE. Read the complete
`Physician_Supplier_Procedure_Summary_2025.csv`, never a saved extract. Keep rows
where `CARRIER_NUM` is 09102 and `PSPS_ERROR_IND_CD` is 00. Sum
`PSPS_SUBMITTED_SERVICE_CNT` grouped by HCPCS and `PLACE_OF_SERVICE_CD`, using
POS 21 (inpatient hospital), 22 (outpatient hospital) and 23 (emergency room)
ONLY. Each share is that POS over the sum of those three.

Office (11), home (12) and SNF (31, 32) are EXCLUDED from the denominator, and
this is the step that gets lost. They are not the counterfactual: what SOS
prevents is a hospital encounter, not a routine office visit. Earlier wording
here listed POS 11 among the grouping codes, which does not reproduce the table -
including it collapses catheter management from 26.8% to 4.9%, because 12,793 of
its 16,100 Florida services are office based.

INTEGRITY CHECK, BEFORE THE NUMBERS ARE USED. Florida holds 2,176 rows across the
four CPTs. An extract with materially fewer rows is incomplete, whatever it is
named. Per CPT: 49083 495 rows | 32555 1,022 | 51702 361 | 43762 298. On
2026-08-22 both July partner reports were built from a 153-row file that was the
truncated head of this source, producing shares of 77.3, 32.3, 1.6 and 3.6
percent and overstating cost avoidance by $127,101.41 for Empath and $45,643.23
for AccentCare. If a build produces a paracentesis benchmark near $10,660, a
truncated extract has come back.

---

## CPT correction: 32557 was wrong, use 32555

We had been using **32557** for thoracentesis. That code is pleural **drainage by
indwelling catheter** - a chest tube - and it is 98.6% inpatient. It is not a
thoracentesis.

The aspiration code, thoracentesis with imaging guidance, is **32555**.

**32557 was wrong in every report issued from April through July 2026.** The
correction is why the thoracentesis discharged figure moved from 2,911.43 to
1,852.39; the other three procedures' discharged figures are unchanged from
Session 32.

---

## MS-DRGs adopted (Pathway B)

Weights and GMLOS are FY2026 IPPS Table 5.

| DRG | Description | Weight | GMLOS | Applies to |
|---|---|---|---|---|
| 393 | Other digestive system diagnoses **with MCC** | 1.5993 | 4.2 | Paracentesis, G-tube |
| 186 | Pleural effusion **with MCC** | 1.5585 | 4.2 | Thoracentesis |
| 695 | Kidney and urinary tract signs and symptoms **with MCC** | 1.1438 | 3.6 | Catheter |

**Always the with-MCC tier.** A hospice patient carries a major complication by
definition of being on hospice.

Ascites is a symptom, so it groups to the 393-395 family, not the cirrhosis
family. That corrected the earlier DRG 432 assumption.

---

## Locked CY2026 / FY2026 benchmarks

| Procedure | Discharged (Pathway A) | Admitted (Pathway B) | FL admit % | **Blended** |
|---|---|---|---|---|
| Paracentesis | 1,997.66 | 13,150.74 | 32.8% | **5,655.87** |
| Thoracentesis | 1,707.11 | 12,848.13 | 76.1% | **10,185.43** |
| Catheter Management | 1,779.11 | 9,683.52 | 26.8% | **3,897.49** |
| G-Tube / PEG | 1,792.10 | 13,091.97 | 6.7% | **2,549.19** |

**Discharged pathway corrected 2026-08-26 (status T).** Through 2026-08-25 every
procedure's discharged pathway was priced on the Level 5 ED facility payment plus
the 99285 ED physician fee. That is right for catheter and G-tube and wrong for
paracentesis and thoracentesis. Both are status T, separately payable on their own
APC, and the PSPS place-of-service split says that is where they happen when the
patient is not admitted:

| Procedure | Outpatient | ER | Discharged encounter modeled |
|---|---|---|---|
| Paracentesis 49083 | 9,165 (92.1%) | 781 (7.9%) | Outpatient, APC 5301, no ED visit |
| Thoracentesis 32555 | 4,070 (89.4%) | 483 (10.6%) | Outpatient, APC 5181, no ED visit |
| Catheter 51702 | 300 (14.0%) | 1,847 (86.0%) | ED, APC 5025 J2, procedure packages |
| G-Tube 43762 | 103 (4.2%) | 2,360 (95.8%) | ED, APC 5025 J2, procedure packages |

Where the encounter is an ED visit, 99285 is J2 and everything else on the claim
packages into it, so the procedure's own APC is not paid and the ED physician fee
applies. Where it is an outpatient encounter, the status T procedure is paid on
its own APC and there is no ED visit and no ED physician fee. Physician
professional fees are never packaged by OPPS and are always payable.

This also closes the hybrid noted on 2026-08-25, where paracentesis was priced on
APC 5301 while still carrying the ED physician fee. Empath July moves from
230,633.65 to 226,761.13.

The **blended** column is the figure that appears in partner reports. Each row
reconciles to the blend formula within a penny.

### Discharged pathway components (Pathway A)

```
A0426 ALS1 non-emergency round trip     675.14
A0425 30 statute miles round trip       279.90
APC 5301 paracentesis facility          947.15
APC 5025 ED Level 5 facility            621.90   (primary for thoracentesis,
                                                  catheter, G-tube)
99285 ED physician                      178.46
49083 physician                          95.47
32555 physician                          96.99
51702 physician                          23.71
43762 physician                          36.70
```

Everything else on the claim packages at 0.00.

Other adjusted APCs if needed: 5024 ED Level 4 435.74, 5371 G-tube facility
260.91, 5734 catheter facility 138.94. ED physician at other levels: 99283 72.42,
99284 123.46.

### Admitted pathway components (Pathway B)

```
DRG amount   393    11,921.77
             186    11,617.64
             695     8,526.31
plus         round-trip transport      955.04
             99285 ED physician        178.46
             procedure physician fee   (per the discharged list above)
```

---

## Why the Session 32 packaging correction still stands, and what was wrong about it

**Corrected 2026-08-25 against the CY2026 July Web Addendum B.** This section
previously stated that paracentesis (49083) carries status indicator J1 as the
primary procedure of a Comprehensive APC. That is false. Verified status
indicators and national unadjusted rates, CY2026 July Addendum B:

| CPT | SI | APC | National rate | Florida adjusted |
|---|---|---|---|---|
| 49083 paracentesis | **T** | 5301 | $926.63 | $947.15 |
| 32555 thoracentesis | **T** | 5181 | $640.89 | $655.08 |
| 43762 G-tube replacement | **T** | 5371 | $255.26 | $260.91 |
| 51702 catheter | **Q1** | 5734 | $135.93 | $138.94 |
| 99285 ED visit Level 5 | **J2** | 5025 | $608.43 | $621.90 |
| 32557 pleural catheter | J1 | 5182 | $1,608.25 | n/a, not our code |

**J1 belonged to 32557, the code we abandoned.** The Comprehensive APC reasoning
was written while 32557 was still in use, and it was correct about 32557. When
Session 33 replaced it with 32555, the packaging rationale was never revisited.
No procedure in our set is J1, and no Comprehensive APC is in play.

**The double count was still real, but for a different reason.** The packaging
that collapses the April-July twelve-line stack is the **J2** ED visit, not a J1
procedure. Addendum D1 defines J2 as a comprehensive payment where no J1 appears
on the claim, packaging every other service reported on it. So where the modeled
encounter runs through the emergency department, the ED visit is the single
payment and the labs, imaging, observation and the procedure package into it.
The Session 32 correction stands. Its stated basis did not.

**Two consequences for the discharged pathway, both open, both move dollars.**
Neither is changed here, because changing them changes every published figure.

1. Status T is *separately payable*, subject to the multiple-procedure
   reduction. It is not packaged the way J1 packages. Where the modeled encounter
   does NOT include an ED visit, the T procedure pays on its own APC and other
   services on the claim pay on their own indicators.
2. The discharged stack is a hybrid: it uses the procedure's own APC as the
   facility payment while also charging the 99285 ED **physician** fee of
   $178.46, without the ED facility payment. That is inconsistent with Session
   33's own finding that a paracentesis happens in interventional radiology
   rather than the ER. Either the encounter includes the ED, in which case the
   J2 facility payment applies and the procedure packages, or it does not, in
   which case the ED physician fee should not be there.

`SOS_MPU_Report_Build_Spec_v1.md` section 8.2 and the disclaimer text in the
issued partner reports both already state T correctly. This file was the outlier.

### The fourteen C-APC exclusions (CY2026 Addendum J)

Ambulance services | Brachytherapy | Diagnostic and mammography screenings |
PT/SLP/OT on a separate recurring facility claim | Pass-through drugs,
biologicals and devices | Preventive services under 42 CFR 410.2 |
Self-administered drugs | Status F services | Status L services | Certain Part B
inpatient ancillary services | New Technology APC services | HCPCS C9399 drugs |
Non-opioid products under CAA 2023 section 4135 (H1 and K1) | Cell and gene
therapies.

### Consequences

- **Ambulance is the only line in our stacks outside the packaging.**
- Status K non-pass-through drugs are **not** excluded, so albumin (P9047)
  packages. Two AI models said it pays on top. It does not.
- Status R blood products are **not** excluded either. Same conclusion.
- J2 (ED visit) would package into a J1 on the same claim, per Addendum D1
  verbatim: "Packaged APC payment if billed on the same claim as a HCPCS code
  assigned status indicator J1." **No code in our set is J1, so this clause
  never fires for us.** It is retained only because it applied to 32557.
- Since no J1 exists for any of our four procedures, the ED visit is always the
  comprehensive payment where an ED visit is part of the encounter, per Addendum
  D1 J2 clause (1), and it packages everything else on that claim.

---

## Computation rules

**FACILITY (Pathway A):** Addendum B national unadjusted rate x
`[(0.60 x wage index) + 0.40]`. Labor-related share is 60% for CY2026, confirmed
in the CMS-1834-FC final rule summary.

**WAGE INDEX:** 1.0369 for **every** Florida CBSA. Florida's rural floor lifts
them all to the same value - Orlando's pre-floor is 0.9568, Tampa's 0.8776,
Pensacola's 0.7784, and all are overridden. There is **no** geographic variation
to model in Florida. Factor = 1.02214.

**PHYSICIAN:** `(Work RVU x 1.000) + (Facility PE RVU x 0.956) + (MP RVU x 1.503)`,
times 33.4009. Those GPCIs are Rest of Florida, locality 99. 49083 has PC/TC
indicator 0 - modifier -26 does **not** apply to it.

**AMBULANCE:** MAC 09102 locality 99 urban base. A0428 BLS non-emergency 281.31 |
A0426 ALS1 non-emergency 337.57 | A0427 ALS1 emergency 534.49 | A0425 mileage
9.33 per statute mile urban, 9.42 rural. Round trip is modeled - the hospice pays
for the ride home.

**INPATIENT (Pathway B):**

```
DRG weight x [(operating labor 4,456.72 x wage index) + operating nonlabor 2,295.89]
  + (capital 524.15 x GAF x DRG weight)
```

Those are the FY2026 standardized amounts (IPPS Tables 1A-1E), at the
quality-reporting and meaningful-EHR-user rates, wage index above 1. Florida GAF
1.0251. Weights and GMLOS come from IPPS Table 5 and are listed in the MS-DRG
section above.

**ENCOUNTER ASSUMPTIONS:** ALS1 non-emergency round trip, 30 statute miles,
ED Level 5, with-MCC DRG tier. These are business decisions, not data. Neil's
ruling 2026-08-15 is to display the highest realistic figures with the
methodology disclosed.

---

## Source files - re-download each year

See `SOS_MPU_Annual_Data_Refresh_Checklist.md` for the full eight-source list,
cadence and traps. In brief:

| # | Source | File | Cadence |
|---|---|---|---|
| 1 | OPPS Addenda D1 + J | `20XX_nfrm_addenda.MM.DD.YYYY.zip` | Annual, Jan 1 |
| 2 | OPPS Addendum B (July web update) | `20XX_july_web_addendum_b.*.zip` | Annual + quarterly |
| 3 | PFS relative value file | `rvu##ar_#.zip` | Annual + quarterly |
| 4 | IPPS Table 5 (MS-DRG weights) | `cms####ftable5.zip` | Annual, Oct 1 |
| 5 | IPPS Tables 1A-1E and Table 3 | `cms####ftables1a1e.zip`, `cms####ftables234a4b_0.zip` | Annual, Oct 1 |
| 6 | Ambulance fee schedule | `afs####_puf_ext.zip` | Annual, Jan 1 |
| 7 | FL hospice per diems | `sos_hospice_rates_fl_####.xlsx` | Annual, Oct 1 |
| 8 | PSPS claims file (blend weights) | `Physician_Supplier_Procedure_Summary_####.csv` (~840 MB) | Annual, ~1 year in arrears |

Items 4, 5, 7 and 8 are new since Session 32. Addendum B took the July web
update, which supersedes the final-rule figure (49083 is 926.63, not the 937.33
an AI model quoted). Conversion factor 33.4009 non-QP, 33.57 QP.

The working copies live in the ephemeral session container, not in this repo.
Re-download every cycle. The PSPS file stays in the MPU Reporting folder and is
filtered in place - do not upload it.

---

## Presentation

- **All per-procedure CPT line-item tables are removed.** Neil: "people aren't
  likely checking the per line breakdowns." Replaced by three narrative
  paragraphs plus one range chart. Six or seven pages became about two.
- **New chart, Estimated Hospital Cost per Episode:** dot at the discharged
  figure, dot at the admitted figure, diamond at the blend.
- Tables carry the **blended figure only**.
- Exec summary no longer says "Based on 2026 Medicare reference rates" - it names
  the blend method.
- Coverage line leads with what **is** covered rather than what falls outside.
- Branch charts at the 15-visit threshold; below that, tables.
- Services Performed gets its own page when a partner has more than 8 service
  types.
- Visit Complexity shares page 3 with Time of Day.
- "Shown in clinical order" caption appears once, not four times.

### Hospice per diem paragraph

Every clinical report carries **"What This Means for [Partner]"** under the
aggregate savings table. It states the published FY2026 routine home care and
general inpatient rates for the counties that partner's visits actually resolved
to, and makes the point that a day at home stays on the lower rate. It
deliberately makes **no** claim about what the partner pays its contracted
hospitals, because we cannot know that.

Neil's ruling: keep hospital cost as the primary table, add this as one
paragraph, not a second table. Villages spans three counties - use the highest,
which is Lake. FY2026 range across our counties: routine home care $189.04 to
$220.42, general inpatient $991.73 to $1,149.01.

### Disclaimers

- **Pathway Weighting** - explains the two pathways and the Florida blend.
- **Nature of These Estimates** - these are modeled reference figures, not bills.
- **How Medicare Pays** - expanded to cover the three-day payment window.
- **Rate Sources** - names each source file.
- **Comprehensive APC Packaging** - explains why bundled services do not appear
  as separate lines.
- **Financial Responsibility** - the central point: for a patient on the Medicare
  hospice benefit, care related to the terminal diagnosis is the **hospice's**
  financial responsibility. Hospitals bill hospices under private contract, and
  non-contracted facilities bill chargemaster rates far above Medicare. These
  figures are therefore a conservative **floor** on avoided cost, never a
  ceiling. That is the whole point of the report.

---

## July 2026 restated totals

| Partner | Restated (Session 33) | Session 32 figure | Original April-July figure |
|---|---|---|---|
| Empath | **237,682.63** | 81,588.50 | 158,426.86 |
| AccentCare | **77,884.92** | 29,509.14 | 55,496.33 |
| Chapters | **5,230.80** | 1,631.12 | n/a (new report) |
| VITAS | **3,574.49** | 1,456.11 | 1,505.07 |

These supersede **both** the original April-July figures and the Session 32
corrections. **Only these are valid for month-over-month comparison.**

July page counts: Empath 23, AccentCare 17, Chapters 12, InnoVage 12, VITAS 11.

---

## Open

- **Nine service lines still have no hospital benchmark:** Imaging / X-Ray,
  Consultation/Evaluation, Wound/Fracture Care, Pleural Catheter/Chest Tube,
  Tracheostomy Management, IV Access/Infusion, Lab Draw, Foot Care,
  Ultrasound/Evaluation. **64 of Empath's 118 July visits sit outside the model**
  for want of benchmarks.
- **Imaging / X-Ray** cannot be benchmarked yet: SOS does not perform the study,
  it is outsourced, and the vendor bills the hospice directly. Any benchmark must
  account for the vendor charge, which Neil does not have to hand.
- Outlier payments (42 CFR 419.43(d), capped at 3.0% of program payments) are not
  modeled.
- IPPS cost outlier payments and DSH / IME add-ons are not modeled either. Both
  would raise the admitted pathway, so the blend stays conservative.
- Whether to notify partners that July reports were reissued under corrected
  methodology, and in what words, is Neil's call and still open.
- **The July reports as issued 2026-08-22 are wrong and must be rebuilt.** Both
  were built on the truncated 153-row extract. Empath shows 357,735.06 and
  AccentCare 127,275.64; recomputed on this model, using each report's own visit
  and acuity counts, they are 230,633.65 and 81,632.41.
- **Those recomputed figures do not match the Session 33 restatement above**
  (237,682.63 and 77,884.92). Three known causes, to resolve at rebuild: the
  Empath report prices Moderate Complexity at 343, which is AccentCare's rate and
  should be 373; AccentCare counted visits are 49 in the build spec against 51 in
  the Decisions Log; and the reports carry one thoracentesis where the Session 33
  basis may differ. Reconcile before any figure is reissued.
- **`SOS_MPU_Report_Build_Spec_v1.md` is untracked in git.** It drifted from this
  file undetected and is what a rebuild actually reads. Commit it.
