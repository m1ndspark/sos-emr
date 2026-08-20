# SOS MPU - Cost Savings Methodology

**What changed between the June and July reports, and why.**

Prepared for the walkthrough with Josh, 2026-08-20.

---

## The one-sentence version

We were adding up hospital charges line by line, the way a bill looks. Medicare
does not pay that way, so we rebuilt the model to pay the way Medicare actually
pays, one bundled amount per encounter, and then weighted it by how often the
procedure really ends in an admission.

---

## Change 1. Lines that used to stand alone are now inside one payment

June priced a hospital episode as a twelve-line stack. Each line had its own
dollar figure and they were summed.

Under CY2026 OPPS, a paracentesis and a thoracentesis are **J1** Comprehensive
APC procedures. When a J1 is on the claim, Medicare pays **one** amount that
covers the entire outpatient encounter. Every other service on that claim pays
zero. Not a discount, zero.

| Was a separate line | Now |
|---|---|
| ED visit facility fee | Packaged into the J1 comprehensive payment |
| Laboratory panels | Packaged |
| Imaging | Packaged |
| Ultrasound guidance | Packaged |
| Observation hours | Packaged |
| Albumin (P9047) | Packaged |
| Blood products | Packaged |
| Ascitic fluid cytology (88104 / 88108) | Packaged |
| Procedure facility fee | This **is** the comprehensive payment |
| Ambulance | **Still separate**, the only one |

So the honest answer to "where did that cost go?" is: it did not go away. It was
never a separate payment in the first place. It is inside the one number.

**When there is no J1 code.** Catheter management and G-tube management have no
J1 procedure. In those cases the ED visit itself becomes the comprehensive
payment, and it packages everything else on the claim. Same principle, different
anchor.

**Why ambulance survives.** CMS publishes fourteen categories excluded from C-APC
packaging. Ambulance is on that list. Nothing else in our stack is.

**The common pushback.** "Albumin is expensive, surely that pays on top." It does
not. Albumin is status K, non-pass-through, and status K is not one of the
fourteen exclusions. Two AI models told us otherwise; the CY2026 Addendum J
exclusion list says no.

---

## Change 2. We now price both ways the patient can go

June assumed a single hospital pathway. That was Josh's objection: a paracentesis
is almost never done in the ER. It happens in interventional radiology, and the
real fork is whether the patient goes home the same day or gets admitted.

Every procedure is now priced twice and blended.

| | Pathway A - treated and discharged | Pathway B - admitted |
|---|---|---|
| Facility | Comprehensive APC payment | MS-DRG for the entire inpatient stay |
| Transport | round-trip ambulance | round-trip ambulance |
| Professional | physician fees | ED physician fee + procedure physician fee |

```
BLENDED = A x (1 - admit%) + B x admit%
```

The admit% is not an assumption. It is how often that CPT actually resolved to an
inpatient stay in **Florida**, from the 2025 Part B claims file, carrier 09102.

| CPT | Procedure | Admitted |
|---|---|---|
| 49083 | paracentesis | 32.8% |
| 32555 | thoracentesis | 76.1% |
| 51702 | catheter | 26.8% |
| 43762 | G-tube | 6.7% |

Florida, not national, because they diverge. Catheter management is 63% ER in
Florida against 36% nationally.

### Worked example, paracentesis

```
Discharged      $2,176.12
Admitted       $13,150.74
Admit rate         32.8%

($2,176.12 x 0.672) + ($13,150.74 x 0.328)
= $1,462.35 + $4,313.44
= $5,775.80
```

---

## Change 3. We were using the wrong thoracentesis code

Every report from April through July used CPT **32557**.

32557 is pleural drainage by **indwelling catheter**, a chest tube. It is 98.6%
inpatient, which would have forced nearly every thoracentesis down the admitted
pathway.

The aspiration code, which is what we actually do, is **32555**.

This is a clean correction, not a judgment call.

---

## Change 4. The DRG is now ascites-generic

June used DRG 432, which is cirrhosis-specific.

Josh's point: patients need a tap for many reasons, not just cirrhosis. Pinning
the model to a cirrhosis DRG made it wrong for everyone else.

| DRG | Description | Applies to |
|---|---|---|
| 393 | Other digestive system diagnoses with MCC | paracentesis, G-tube |
| 186 | Pleural effusion with MCC | thoracentesis |
| 695 | Kidney and urinary tract signs with MCC | catheter |

Always the **with MCC** tier. A patient on hospice carries a major complication
by definition of being on hospice.

---

## Change 5. SOS's own rate is now the partner's contract rate

June used a flat internal rate table for what SOS charges.

July uses the actual contracted rate for that partner at that visit's acuity,
because that is the number the partner recognizes on its own invoice. Empath High
is 575, AccentCare High is 545, and so on.

Savings is hospital benchmark minus what the partner actually paid SOS.

---

## Change 6. Encounter assumptions are now stated

June did not disclose them. July does, and they are set to the highest realistic
scenario with the methodology disclosed:

- ALS1 non-emergency ambulance, round trip
- 30 statute miles
- ED Level 5
- With MCC
- Florida wage index 1.0369

One note on the wage index: it is 1.0369 for **every** Florida CBSA. The state
rural floor lifts them all to the same value. Orlando's raw index is 0.9568,
Tampa's 0.8776, so there is no geographic variation to model in Florida.

---

## Change 7. The report no longer shows per-CPT line items

The twelve-line tables are gone. They implied the lines pay separately, which is
exactly the error we corrected.

Replaced by three narrative paragraphs and one range chart per procedure: a dot
at the discharged figure, a dot at the admitted figure, a diamond at the blend.

---

## Where the numbers landed

### Blended benchmark per episode

| Procedure | Discharged | Admitted | FL admit % | Blended |
|---|---|---|---|---|
| Paracentesis | 2,176.12 | 13,150.74 | 32.8% | **5,775.80** |
| Thoracentesis | 1,852.39 | 12,848.13 | 76.1% | **10,220.14** |
| Catheter | 1,779.11 | 9,683.52 | 26.8% | **3,897.49** |
| G-Tube / PEG | 1,792.10 | 13,091.97 | 6.7% | **2,549.19** |

### July total savings by partner

| Partner | June method | Interim fix | CURRENT (valid) |
|---|---|---|---|
| Empath | 158,426.86 | 81,588.50 | **237,682.63** |
| AccentCare | 55,496.33 | 29,509.14 | **77,884.92** |
| Chapters | - | 1,631.12 | **5,230.80** |
| VITAS | 1,505.07 | 1,456.11 | **3,574.49** |

Only the CURRENT column is valid. The interim column was the packaging fix before
the pathway fix; it is on the page only so nobody is surprised by a number they
saw in passing.

---

## Answers to the questions Josh will ask

**"The number went UP. Didn't you say we were overstating it?"**
Both are true. Removing the double count pushed it down. Adding the admitted
pathway pushed it further up, because an admission costs far more than an
outpatient visit and thoracentesis admits 76% of the time. Net, it went up.

**"Why is thoracentesis so much higher than paracentesis?"**
Almost entirely the admit rate. 76.1% versus 32.8%. Discharged, the two are
within a few hundred dollars of each other.

**"Are we inflating this?"**
The opposite. These are Medicare rates. A hospital bills a hospice under private
contract, and a non-contracted facility bills chargemaster, both well above
Medicare. We do not model outlier payments, DSH or IME either, and all three
would raise the admitted pathway. The figure is a floor.

**"Can we compare this to June?"**
No. June was never restated on this model. A June-to-July comparison is
method-over-method, not month-over-month. The first clean comparison is July to
August.

**"Why isn't every visit in the savings number?"**
Nine service lines have no hospital benchmark at all: Imaging / X-Ray,
Consultation/Evaluation, Wound/Fracture Care, Pleural Catheter/Chest Tube,
Tracheostomy Management, IV Access/Infusion, Lab Draw, Foot Care,
Ultrasound/Evaluation. 64 of Empath's 118 July visits fall outside the model.
Actual avoidance is higher than what we show.

**"Where did the ER visit charge go?"**
Into the comprehensive payment, when there is a J1 procedure on the claim. Where
there is no J1, the ER visit IS the comprehensive payment.
