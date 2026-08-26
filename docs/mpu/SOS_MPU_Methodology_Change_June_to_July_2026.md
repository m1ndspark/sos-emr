# SOS MPU - Cost Savings Methodology

**How the hospital benchmarks are built, and what changed along the way.**

Prepared for the walkthrough with Josh, 2026-08-20.
Amended 2026-08-21 after independent verification against CMS source files. Two
material corrections in that pass, both documented below.
Amended again 2026-08-21 after a line-by-line clinical read of all 21 Empath
evaluation notes. One paracentesis had been misclassified as an evaluation
because the note read "successfully removed" and only "fluid was removed" was on
the performed-phrase list. The list was extended and every month reclassified,
which moved six additional historical visits into the performed category. All
figures below are post-correction.

---

## The one-sentence version

We were adding up hospital charges line by line, the way a bill looks. Medicare
does not pay that way, so we rebuilt the model to pay the way Medicare actually
pays, one bundled amount per encounter where bundling applies, and then weighted
it by how often the procedure is billed to a patient who is already an inpatient.

---

## Change 1. Lines that used to stand alone are now inside one payment

June priced a hospital episode as a twelve-line stack. Each line had its own
dollar figure and they were summed. That is not how OPPS pays.

**Corrected 2026-08-21.** The original version of this document said all four
procedures anchor on a J1 comprehensive APC. That is only half right, and the
CY2026 Addendum B confirms it:

| CPT | Status indicator | Packages the claim? |
|---|---|---|
| 99285 ED visit Level 5 | J2 | Yes |
| 49083 paracentesis | **T** | **No** |
| 32555 thoracentesis | **T** | **No** |
| 32557 pleural drainage, indwelling | J1 | Yes, but this is not our code |
| 51702 catheter | Q1 | Conditionally packaged |
| 43762 G-tube | T | No |

So:

- **Catheter management and G-tube replacement** are priced on the Level 5 ED
  visit, which is J2 and does package every other covered Part B service on the
  claim. The packaging argument holds for these two.
- **Paracentesis and thoracentesis** are status T. Status T does not package the
  claim. Laboratory studies, imaging and observation billed alongside them would
  be paid separately, and we do not include them.

The practical effect is that our paracentesis and thoracentesis outpatient
figures are **lower than a real claim would be**, not higher. The savings are
conservative. The dollar figures were always right; the explanation was not.

**Why ambulance is always separate.** CMS excludes ambulance from C-APC packaging
along with status F, G, H, L and U services, mammography and preventive services.
Ambulance is the only line in our stack on that list.

**The common pushback.** "Albumin is expensive, surely that pays on top." Where
packaging applies, it does not. Albumin is status K, and status K is not on the
exclusion list.

---

## Change 2. We now price both ways the patient can be treated

June assumed a single hospital pathway. That assumption was wrong: a paracentesis
is almost never done in the ER. It happens in interventional radiology, and often
on a patient who is already admitted.

Every procedure is priced twice and blended.

| | Pathway A - hospital outpatient | Pathway B - inpatient |
|---|---|---|
| Facility | OPPS payment | MS-DRG for the entire stay |
| Transport | round-trip ambulance | round-trip ambulance |
| Professional | physician fees | ED physician fee + procedure physician fee |

```
BLENDED = A x (1 - inpatient share) + B x inpatient share
```

### The weighting, corrected 2026-08-21

The original table of shares did not reconcile to the source file. Pulled fresh
from the 2025 Physician/Supplier Procedure Summary, carrier 09102, Florida, the
inpatient place-of-service shares are:

| CPT | Procedure | Was | **Is** |
|---|---|---|---|
| 49083 | paracentesis | 32.8% | **77.3%** |
| 32555 | thoracentesis | 76.1% | **32.3%** |
| 51702 | catheter | 26.8% | **1.6%** |
| 43762 | G-tube | 6.7% | **3.6%** |

Paracentesis and thoracentesis were transposed. The old paracentesis figure of
32.8% is almost exactly thoracentesis's true 32.3%, and the old thoracentesis
figure of 76.1% is almost exactly paracentesis's true 77.3%. Catheter and G-tube
were simply wrong.

This is the single largest correction in the model, because paracentesis is our
highest-volume procedure by a wide margin.

**Two limits on this number, and they should be stated to any partner who asks.**
The PSPS file carries no hospice indicator, so these shares describe Florida
Medicare generally, not hospice patients. And place of service records that the
patient was an inpatient when the procedure was billed, which is not the same as
this encounter having caused an admission. We use it as the best available public
proxy and we say so.

A third limit is internal: CMS suppressed 98 of the 153 Florida rows for small
cell size, so these shares are computed on the reported rows only. Suppression
hits small cells, so the bulk of volume is captured, but the shares are not exact.

### Worked example, paracentesis

```
Outpatient      $2,176.12
Inpatient      $13,150.74
Inpatient share    77.3%

($2,176.12 x 0.227) + ($13,150.74 x 0.773)
= $493.98 + $10,165.52
= $10,659.50
```

---

## Change 3. We were using the wrong thoracentesis code

Every report from April through July used CPT **32557**, which is pleural drainage
by indwelling catheter, a chest tube. The aspiration code, which is what we
actually do, is **32555**. Verified against AMA coding references: 32554 and
32555 are aspiration where the needle or catheter comes out at the end of the
procedure; 32556 and 32557 leave a catheter in for continuing drainage.

A residual error from this correction was found on 2026-08-21. The inpatient
pathway had been updated to the 32555 physician fee of $96.99 but the outpatient
pathway had not, leaving it $33.18 low. Corrected: thoracentesis outpatient is
**$1,885.57**.

---

## Change 4. The DRG is ascites-generic

June used DRG 432, which is cirrhosis-specific. Patients need a tap for many
reasons, so pinning the model to a cirrhosis DRG made it wrong for everyone else.

| DRG | Description | Applies to | FY2026 weight |
|---|---|---|---|
| 393 | Other digestive system diagnoses with MCC | paracentesis, G-tube | 1.5993 |
| 186 | Pleural effusion with MCC | thoracentesis | 1.5585 |
| 695 | Kidney and urinary tract signs with MCC | catheter | 1.1438 |

Always the with-MCC tier. A patient on hospice carries a major complication by
definition of being on hospice.

---

## Change 5. SOS's own rate is the partner's contract rate

June used a flat internal rate table. July uses the actual contracted rate for
that partner at that visit's acuity, because that is the number the partner
recognizes on its own invoice.

Rates come from the Partner Rates report in Creator. Filter to Rate Category
`Acuity Level` **plus** the `Telemedicine` rate, which sits under Rate Category
`Service`. Filtering on Acuity Level alone silently drops Telemedicine.

Savings is hospital benchmark minus what the partner actually paid SOS.

---

## Change 6. Encounter assumptions are stated

- ALS1 non-emergency ambulance, round trip, 30 statute miles: $955.04
- ED Level 5
- With MCC on the inpatient pathway
- Florida wage index 1.0369, which the state rural floor applies to every Florida
  CBSA, so there is no geographic variation to model
- OPPS labor-related share 60 percent
- Capital adjusted by the capital GAF

---

## Change 7. No per-CPT line items in the report

The twelve-line tables are gone. They implied the lines pay separately, which is
the error we corrected. Replaced by narrative and one range chart per procedure:
a hollow dot at the outpatient figure, a filled dot at the inpatient figure, a
green diamond at the blend.

---

## Where the numbers landed

### Blended benchmark per episode, current as of 2026-08-21

| Procedure | Outpatient | Inpatient | FL inpatient share | Blended |
|---|---|---|---|---|
| Paracentesis | 2,176.12 | 13,150.74 | 77.3% | **10,659.50** |
| Thoracentesis | 1,885.57 | 12,848.13 | 32.3% | **5,426.48** |
| Catheter | 1,779.11 | 9,683.52 | 1.6% | **1,905.58** |
| G-Tube / PEG | 1,792.10 | 13,091.97 | 3.6% | **2,198.90** |

### Savings history for these figures

| Partner | Session 33 | 2026-08-21 rebuild | **Current, corrected** |
|---|---|---|---|
| Empath, July | 237,682.63 | 225,762.85 | **357,735.06** |
| AccentCare, July | 77,884.92 | 76,401.61 | **127,275.64** |

Only the final column is valid. The middle column corrected visit classification
and contracted rates; the final column corrects the inpatient shares and the
performed-phrase list.

### Year to date, both partners restated on the current model

| Month | Empath | AccentCare |
|---|---|---|
| April 2026 | 200,831.96 | 20,278.62 |
| May 2026 | 227,126.16 | 51,429.16 |
| June 2026 | 247,494.94 | 77,394.82 |
| July 2026 | 357,735.06 | 127,275.64 |
| **YTD** | **1,033,188.12** | **276,378.24** |

---

## June restatement status

**Corrected 2026-08-21.** An earlier version said June was never restated and no
June-to-July comparison was possible. That is no longer true. April, May and June
have been rebuilt on the current model for both partners and appear on the Year
to Date page of each July report.

Two adjustments make the historical months comparable, both documented in the
build spec:

1. The `Visit Cancelled` acuity value did not exist in Cognito before July.
   Cancellations in April, May and June are detected from clinical note text.
2. May recorded imaging coordination visits as `No Charge` rather than
   `Telemedicine`. Those rows are reclassified, since billing status is not an
   acuity. Eleven May rows and two June rows moved for Empath.

What you cannot do is compare a restated month to the report originally issued
for that month. Those used the old method.

---

## Independent verification log

Checked 2026-08-21 against CMS source files rather than accepted from this
document.

**Verified to the cent.**

- FY2026 IPPS Table 5 weights: DRG 393 at 1.5993, DRG 186 at 1.5585, DRG 695 at
  1.1438.
- FY2026 IPPS Table 1A: labor-related $4,456.72, nonlabor-related $2,295.89.
  Capital standard federal rate $524.15.
- All four inpatient figures rebuild from those values at wage index 1.0369 with
  the capital GAF, to within two cents.
- CY2026 OPPS Addendum B, January and July releases identical for our codes:
  49083 at $926.63, 32555 at $640.89, 99285 at $608.43. Wage-adjusted at
  0.6 x 1.0369 + 0.4, these reproduce the outpatient figures for paracentesis,
  catheter and G-tube exactly.
- CY2026 PFS relative value file: every physician fee reproduces exactly at the
  $33.4009 conversion factor and the Rest of Florida GPCIs of 1.000, 0.956 and
  1.503. 99285 $178.46, 49083 $95.47, 32555 $96.99, 32557 $134.07, 51702 $23.71,
  43762 $36.70.
- CPT 32555 versus 32557 definitions, confirmed against AMA-derived references.
- J1 and J2 packaging rules and the ambulance exclusion, confirmed against the
  CY2026 OPPS final rule.
- Blend arithmetic, verified programmatically.

**Found wrong and corrected.**

- The four inpatient shares. Paracentesis and thoracentesis transposed; catheter
  and G-tube materially off.
- Thoracentesis outpatient figure, $33.18 low.
- The J1 packaging claim for paracentesis and thoracentesis.
- One performed paracentesis classified as an evaluation, and the phrase list
  that caused it.

**Still unverified.**

- CY2026 Ambulance Fee Schedule, MAC 09102: the $955.04 transport figure. Every
  other input has been traced to source; this one has not.

---

## Answers to the questions Josh will ask

**"Why did paracentesis nearly double?"**
Because the inpatient share was wrong. It was carrying thoracentesis's 32.8%
when the Florida file says 77.3%. An inpatient stay costs six times what the
outpatient encounter does, so the weighting drives almost everything.

**"How did that happen?"**
The two procedures were transposed somewhere between the source file and the
model. It was caught by pulling the file and rebuilding the shares from scratch.

**"Why did the paracentesis count change from 31 to 32?"**
A performed paracentesis was reading as an evaluation. The note said six liters
"was successfully removed" and our phrase list only had "fluid was removed." All
21 Empath evaluation notes were then read in full, one at a time. That one was the
only error; the other twenty were correct. The phrase list was extended and every
month reclassified, which moved six more historical visits into the performed
category, mostly at AccentCare.

**"Do evaluations mean the patient refused?"**
Almost never. Of 21 Empath evaluations in July, the reason was clinical in
nineteen: no drainable fluid on ultrasound, blood pressure too low to tap safely,
anticoagulation, or a tunneled drain already scheduled for the next day. Two were
patient preference. An evaluation is a provider correctly deciding not to do a
procedure, and it still counts as a visit and a diversion.

**"Are we inflating this?"**
No. These are Medicare rates. A hospital bills a hospice under private contract,
and a non-contracted facility bills chargemaster, both well above Medicare. We do
not model outlier payments, DSH or IME. And because paracentesis and thoracentesis
do not package, the services billed alongside them are missing from our figure
entirely. It is a floor.

**"Can we compare this to June?"**
Yes. April through June are restated on the current model. You cannot compare to
the reports originally issued for those months.

**"Why isn't every visit in the savings number?"**
Nine service lines have no published hospital benchmark: Imaging / X-Ray,
Consultation/Evaluation, Wound/Fracture Care, Pleural Catheter/Chest Tube,
Tracheostomy Management, IV Access/Infusion, Lab Draw, Foot Care,
Ultrasound/Evaluation. 66 of Empath's 118 July visits and 29 of AccentCare's 49
fall outside the model. Actual avoidance is higher than what we show.

**"What does the inpatient share actually measure?"**
That the patient was already an inpatient when the procedure was billed. It is a
proxy for how these procedures get delivered, not proof that a given visit would
have caused an admission. Say it that way if a partner asks.
