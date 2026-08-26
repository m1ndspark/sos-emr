# SOS Monthly Partner Utilization Report (MPU): Complete Build Specification

Version 1.2
Written 2026-08-21 from the Empath July 2026 rebuild (Session 37).
Revised 2026-08-21 after independent verification against CMS source files: section 8 rebuilt on corrected inpatient shares, packaging rules corrected, AccentCare added.
Revised again 2026-08-21 after a line-by-line clinical read of all 21 Empath evaluation notes: one misclassification found, perf marker list extended, all baselines restated.
Owner: Neil Heird, SOS Mobile Medical Care.

This document is the single source of truth for building an MPU report. It is written so that a model given this file plus the month's Cognito exports can reproduce the output exactly, with no questions asked. Read it start to finish before touching data.

Repo rule: no em dashes anywhere in this repo. Use commas, colons, or en dashes. A pre-commit hook enforces this.

---

## 0. What the MPU is

A monthly PDF sent to each contracted hospice partner. It reports what SOS did for them that month, proves those visits prevented outside care, and prices the hospital cost that was avoided. It is a retention and growth document, not an invoice or a clinical record.

Partners are hospice organizations. Each partner has branches (regional operating units). Empath is the largest with seven; AccentCare has six. Each branch gets its own detail page because branch leadership reads only its own page.

One report per partner per month. Never combine partners.

---

## 1. Working style: how Neil operates

These are not preferences to be polite about. Violating them wastes his time.

- **Three sentences maximum** in any reply. Exempt: code itself, session logs, ccode prompts, and a review he explicitly asked for (in a review, every finding is one sentence, no lead-in, no closing summary).
- **One item at a time.** Never stack deliverables or ask two questions in one reply.
- **Never explain a question before asking it.** Ask it.
- **Never justify a decision he already approved.** Once he says go, the next thing produced is the deliverable or a blocking question.
- **Never guess.** If a mapping, a name, or a rule is unclear, stop and ask. He would rather answer one question than unwind a wrong build.
- **Read the files before answering.** He will notice if you inferred instead of checked.
- **Do not speculate about causes.** When something is wrong and the reason is not in front of you, say you do not know. During this build I guessed at why four figures were wrong and the guess was wrong.
- If he says "too long," re-answer in one sentence. Do not apologize.
- He drifts to side questions mid-build. Note the parked question, answer briefly, return to the blocking task. You are the project manager.
- **Flag what you changed and why, in one line.** He wants to know when you deviated, especially on layout or classification.
- **Keep repo docs current as you go.** He expects the spec and the methodology doc updated in the same session the numbers change, not at the end.

Cadence that worked: compute, show him the number, stop. He confirms or rules. Then build. QC gates are listed in section 9.

---

## 2. Inputs

Two Cognito exports per month, both XLSX.

| File | Typical name | Rows (July 2026) | Role |
|---|---|---|---|
| Patient Visit Summary | `PatientVisitSummary2__NN_.xlsx` | 202 all partners | Authority for completed visits |
| Patient Referral | `PatientReferral__NN_.xlsx` | 280 all partners | Address, submit time, referrer, hospice ID |

Key columns in the PVS export (77 columns total):
`Referral ID`, `Completion Date`, `Referral Date`, `Patient Name`, `Patient_Hospice_ID`, `Referral Source`, `Acuity Level`, `Type of Procedure`, `Clinical Note`, `Did this visit prevent a trip to the Emergency Department?`

Key columns in the referral export (59 columns total):
`Referral ID`, `Date Submitted`, `Organization/Affiliate Name`, `First Name`, `Last Name`, `Title`, `Hospice ID`, `Address`, `Address.1`, `Current Patient Location`, `Facility Name`

### Referral ID normalization

Cognito writes referral IDs with thousands separators in some rows (`REF-072226-1,403`) and without in others. **Always normalize before joining:**

```python
N = lambda s: re.sub(r'[^0-9A-Za-z-]', '', str(s))
```

Every join in the pipeline uses the normalized ID. Skipping this silently drops rows.

### Prior month carry-in

Visits completed on the 1st or 2nd of the month often have referrals submitted in the last days of the prior month, so those referral rows are absent from the month's referral export. Ask Neil for a supplemental referral export covering the last week of the prior month, then union only the specific IDs needed. For July 2026 that was five IDs for Empath and one for AccentCare.

Do not union the whole supplement. Pull only the needed IDs.

### Referral counts on the chart are month-bounded

The time-of-day chart counts referrals **submitted in the report month**, not referrals that produced a counted visit. Empath July: 127. AccentCare July: 52. Carry-in referrals are used for addresses and response time but are not counted toward that total.

---

## 3. Partner attribution

`Referral Source` on the PVS row is free text and inconsistently spelled. Map with a keyword function, not exact match.

```python
def partner(s):
    t = str(s).lower()
    if 'accent' in t: return 'AccentCare'
    if 'vitas' in t: return 'VITAS'
    if 'innovage' in t or 'total community' in t: return 'InnoVage'
    for k in ['empath','suncoast','tidewell','tisewell','tiewell','tridewell','tidwell',
              'trustbridge','trustridge','marion','twh','mpcc','spcc']:
        if k in t: return 'Empath'
    return 'Unresolved'
```

Real misspellings observed: `Tisewell`, `Tiewell`, `Tridewell`, `Tidwell`, `Suncost`, `Emapth`, `Trustridge`, `Accent Care`, `ACcentCare`.

### The Unresolved bucket is not optional

Any row landing in `Unresolved` must be resolved by hand before the report ships. July had six. Resolution order:

1. Read the row's referral record for `Organization/Affiliate Name`, referrer name, and address.
2. Check the Hospice ID format. Empath uses either a six digit ID (`481309`) or an eight digit ID ending `02` (`39469502`). Tidewell prefixes with `T`. Marion prefixes with `M` or `MM`.
3. Check the address ZIP against the branch map (section 5).
4. If still ambiguous, ask Neil. Do not assign on geography alone.

**Confirmed rulings from July 2026, apply these permanently:**

| Source label | Belongs to |
|---|---|
| `Hernando Pasco Hospice` | Chapters, not Empath |
| `Life Path Hospice` | Chapters, not Empath |
| `Good Shepherd Hospice` | Chapters, not Empath |
| `Suncost St Joseph Care Center` | Empath, Suncoast Hillsborough |
| blank source, Empath ID format, Pinellas ZIP | Empath, Suncoast Pinellas |
| bare `Hospice`, Empath ID format, Pinellas ZIP | Empath, Suncoast Pinellas |

Chapters Health System operates HPH Hospice, LifePath Hospice, and Good Shepherd Hospice. Those are a separate partner and must be excluded from Empath.

---

## 4. Record classification

Every PVS row for the partner gets exactly one status: `Counted`, `Cancelled`, or `Duplicate`. Only `Counted` rows appear anywhere in the report.

### 4.1 Cancelled

A visit is cancelled when care was never rendered. Neil's rule, verbatim:

> We assume that 100% of our visits will be a diversion. Non-diversions happen when the patient leaves home for care and/or the patient (or family) cancel the visit prior to receiving care. If Josh arrives and is told no, then the visit is cancelled. Cancelled visits cannot divert.

Detection:
- **July 2026 forward:** `Acuity Level == 'Visit Cancelled'`.
- **April, May, June 2026:** the value does not exist. Detect from `Clinical Note` text:

```python
CANC = re.compile(r'visit\s*cancell?e[dre]|cancelled per|cancelled for x|x ray cancelled|visit\.\s*cancel', re.I)
```

Observed variants: `Visit Cancelled`, `Visit cancelled`, `Visit cancellee`, `VISIT CANCELLED PER EMPATH`, `x ray cancelled per hospice`, `Visit. Canceled`, `Visit Cancelled per Hospice`.

- **A patient who left for care before SOS arrived is cancelled**, not a non-diverting visit.

### 4.2 Attempted visit

A visit where SOS arrived but no care was rendered and the patient did not leave home is **counted**, service type `Attempted Visit`, and **cannot divert**. July example: John Masters, property inaccessible, Hospice of Marion County.

### 4.3 Duplicate

Fold when the same encounter was submitted twice. Rules in order:

1. Same normalized Referral ID, same `Completion Date`, same `Acuity Level`: fold, keep the first.
2. Same Referral ID with rows on different dates: **these are separate genuine visits**, do not fold. July example: Alejandro Cruz REF-070826-1287 had two rows on 07-08 (fold one) and a separate row on 07-14 (keep, and it is a performed paracentesis).
3. Blank or empty rows paired with a substantive row on the same referral and date: fold the empty one.
4. When two rows on one referral differ and only one is truth, ask Neil. July example: Juana Enrique REF-072226-1403, where Neil ruled the Moderate row is truth and the Visit Cancelled row is the duplicate.

**There is no imaging fold.** Standalone imaging-only rows paired with a clinical visit do not exist in the data. Do not build for it.

### 4.4 Reconciliation must be reported

The exec summary carries a Records Reconciliation line stating total records submitted, cancelled, duplicates, and the counted remainder. Empath July 2026: 134 submitted, 10 cancelled, 6 duplicates, 118 counted. AccentCare July 2026: 54 submitted, 1 cancelled, 4 duplicates, 49 counted.

---

## 5. Branch assignment

Branch comes from the patient's ZIP, resolved to a county, then mapped. ZIP is primary; the source label is a fallback only when no referral row exists.

Neil pushed back on this and the answer stands: the source label is free text and often wrong about location. Two July rows prove it, an "Empath Hospice" label on a Hardee County patient and a "Tidewell Hospice" label on a Lee County patient.

### ZIP extraction

If `Current Patient Location` contains "facility", prefer `Address.1` (facility address), else `Address`. Take the **last** five digit run in the string. Fall back to the PVS row's `Facility Address` then `Patient Address` when the referral row is missing.

Use the `zipcodes` Python package (offline, no network) for ZIP to county.

```python
pip install zipcodes --break-system-packages
zipcodes.matching('33616')[0]['county']  # 'Hillsborough County'
```

### Empath branch map (locked)

| County | Branch |
|---|---|
| Sarasota, Manatee, Charlotte, DeSoto | Tidewell |
| Palm Beach, Broward | Trustbridge |
| Marion | Hospice of Marion County |
| Pinellas | Suncoast Pinellas |
| Hillsborough | Suncoast Hillsborough |
| Polk | Polk |
| **any other county** | **Empath Main/Primary** |

`Empath Main/Primary` is the catchall, confirmed by Neil. July sent Hardee and Lee counties there.

### AccentCare branch map (locked)

AccentCare branches are county names, so the map is direct: Hillsborough, Pinellas, Pasco, Hernando, Broward, and Miami, where Miami takes Miami-Dade County. There is no catchall; a county outside these six is a blocking question for Neil.

Other partners need their own map. **Do not build a partner report without asking Neil for the branch map and the contracted rates.**

---

## 6. Service type derivation

`Type of Procedure` in Cognito is populated on only about 20% of rows. The remainder must be derived from `Clinical Note` text.

**This is a one-time method for Cognito months.** August 2026 forward comes from Creator where `Type_of_Procedures` is a real multi-select, so no note inference is needed. Say so in the session log, but do NOT put a disclaimer about note derivation in the report; Neil ruled it omitted.

Note text is HTML. Strip tags, unescape entities, collapse whitespace, lowercase before matching.

### Classifier, in strict order

```
1. Attempted Visit          explicit override list (arrival, no care rendered)
2. Imaging / X-Ray          'coordination of diagnostic imaging' | 'mobile radiology' | 'xr mobile'
3. Paracentesis (priority)  if ('paracentesis'|'ascit') and 'thoracentesis' not in Type of Procedure:
                              if note has 'procedure note: paracentesis' or 'paracentesis procedure note':
                                Performed if perf and not defer, else Eval (Not Performed)
4. Thoracentesis            'thoracentesis' | 'pleural fluid'
                              -> Pleural Catheter/Chest Tube if 'pleurx'|'chest tube'|'indwelling pleural'
                              -> Performed if perf and not defer, else Eval (Not Performed)
5. Pleural Catheter/Chest Tube   'pleurx' | 'chest tube' | 'indwelling pleural'
6. Paracentesis (general)   'paracentesis' | 'ascites' | 'ascitic'
7. Tracheostomy Management  'tracheostomy' | 'trach '
8. G-Tube/PEG Management    'g-tube','gtube','peg tube','gastrostomy','g-button','peg ','nasogastric','feeding tube'
9. Catheter Management      'foley','urinary catheter','suprapubic','nephrostomy','catheter exchange',
                            'catheter replacement','urinary retention','indwelling catheter','condom cath'
10. IV Access/Infusion      'picc','midline','iv access','infusion','venipuncture','iv line'
11. Wound/Fracture Care     'wound','fracture','splint','lesion','ulcer','dressing change','laceration','bursa','bursitis'
12. Consultation/Evaluation fallback
```

Step 3 exists because a paracentesis note that mentions pleural anatomy elsewhere was being caught by the thoracentesis branch. Do not reorder.

`perf` markers: `was successfully performed`, `successfully performed`, `fluid was removed`, `fluid were removed`, `was performed without complication`, `procedure was performed`, `catheter was removed intact`, `successfully removed`, `fluid was successfully drained`, `was drained without complication`, `procedure was completed without complication`.

**The perf list is the single highest-risk element in the pipeline.** A missed phrase silently demotes a performed procedure to an evaluation and costs roughly $10,100. On 2026-08-21 a note reading "6 liters of clear yellow ascitic fluid was successfully removed" was classified as an evaluation because only "fluid was removed" was on the list. When adding a partner or a month, read every note classified as `Eval (Not Performed)` in full before trusting the totals.

`defer` markers: `elected to defer`, `declined the procedure`, `deferred`, `not medically indicated`, `no indication for`, `does not meet criteria`, `aspiration is not`, `not performed`, `qualifies for palliative paracentesis`.

### Why the Performed / Eval split exists

SOS goes to the home, assesses with point-of-care ultrasound, and sometimes correctly decides not to tap. That is still a visit and still a diversion, but no procedure happened, so it cannot carry a procedure benchmark.

A full clinical read of all 21 Empath July evaluations on 2026-08-21 found the deferrals are overwhelmingly **provider** decisions, not patient refusal: insufficient or absent drainable fluid on ultrasound, hypotension, anticoagulation, or a scheduled tunneled drain the following day. Only two of 21 were patient preference. Do not assume an evaluation means the patient declined.

### Clinical review gate

Before the derived types drive the savings model, produce a plain text review file listing every counted row with its derived type, the source field value, and a 260 character note excerpt. Neil or Josh Kolanko (APRN, co-admin) signs off. For the four benchmark-bearing service types, read the full note, not the excerpt.

---

## 7. Diversion

A diversion is recorded when SOS provided **any** service in the patient's home, education only included.

**Do not use the Cognito field** `Did this visit prevent a trip to the Emergency Department?`. It is unreliably answered by providers (77 Yes of 117 for Empath July, including performed paracenteses and PICC removals that obviously diverted) and its wording covers only the ED while the SOS definition covers any outside care setting.

Rule: `diversion = True` for every counted row, except `Attempted Visit` rows.

Cancelled rows are excluded from the counted set entirely and therefore cannot divert.

Empath July 2026: 118 counted, 117 diversions, 99.2%. AccentCare July 2026: 49 counted, 49 diversions, 100%.

---

## 8. Savings model

### 8.1 Two pathway blend

An episode does not have one price. Each procedure is priced twice, then blended by the share of Florida cases billed with an **inpatient place of service**, from the 2025 PSPS file, carrier 09102.

| Procedure | Discharged | Admitted | FL inpatient share | **Blended benchmark** |
|---|---|---|---|---|
| Paracentesis | $1,997.66 | $13,150.74 | 32.8% | **$5,655.87** |
| Thoracentesis | $1,707.11 | $12,848.13 | 76.1% | **$10,185.43** |
| Catheter Management | $1,779.11 | $9,683.52 | 26.8% | **$3,897.49** |
| G-Tube/PEG Management | $1,792.10 | $13,091.97 | 6.7% | **$2,549.19** |

**Discharged pathway corrected 2026-08-26.** Paracentesis and thoracentesis are OPPS status T, separately payable on their own APC, and the PSPS split says the discharged encounter is outpatient (92.1% and 89.4% of non-admitted cases), not the ED. They are priced on APC 5301 and APC 5181 with no ED visit and no 99285 physician fee. Catheter and G-tube are 86.0% and 95.8% ER, so they stay on the 99285 J2 comprehensive payment with the procedure packaged into it. Physician professional fees are never packaged and are always payable. The prior figures priced all four on the ED pathway.

Blend check: `share*admitted + (1-share)*discharged` reproduces the benchmark to the cent. Verify this on every build.

Each discharged figure also reconciles from its components: round-trip transport $955.04, the facility payment (APC 5301 $947.15 for paracentesis, ED Level 5 APC 5025 $621.90 for the other three), the ED physician fee $178.46, and the procedure physician fee. Thoracentesis is $1,852.39, not $1,885.57; the latter appeared in this spec through 2026-08-22 and reconciles to no component stack.

Only these four service types qualify. `Paracentesis Performed` and `Thoracentesis Performed` qualify; the `Eval (Not Performed)` variants do not.

### 8.1.1 How the shares are computed

Source is `Physician_Supplier_Procedure_Summary_2025.csv`, the complete CMS file, not a saved extract.

- `CARRIER_NUM` = 09102
- `PSPS_ERROR_IND_CD` = 00
- `PLACE_OF_SERVICE_CD` in 21, 22, 23 ONLY
- share = `PSPS_SUBMITTED_SERVICE_CNT` at POS 21, over the sum across 21, 22 and 23

Office (11), home (12) and SNF (31, 32) are excluded from the denominator. They are not the counterfactual. What SOS prevents is a hospital encounter, not a routine office visit. Including POS 11 collapses catheter management from 26.8% to 4.9%, because 12,793 of its 16,100 Florida services are office based.

**Integrity check, run before using any extract.** Florida holds 2,176 rows across the four CPTs. An extract with materially fewer rows is incomplete, whatever it is named.

| CPT | FL rows | POS 21 | POS 22 | POS 23 |
|---|---|---|---|---|
| 49083 | 495 | 4,852 | 9,165 | 781 |
| 32555 | 1,022 | 14,481 | 4,070 | 483 |
| 51702 | 361 | 785 | 300 | 1,847 |
| 43762 | 298 | 177 | 103 | 2,360 |

**Regression, 2026-08-22.** Both July partner reports were built on shares of 77.3, 32.3, 1.6 and 3.6 percent, read from `4claude.xlsx`, which held only the first 153 of the 2,176 Florida rows. It was a truncated prefix, not a filtered set, and because PSPS is ordered by HCPCS and modifier a prefix destroys the place-of-service mix. A note in this spec dated 2026-08-21 recorded those shares as a correction, described the values now in the table above as transposed, and instructed that they never be reintroduced. That note was wrong and is withdrawn. It also read the 153-row truncation as the whole of Florida and attributed the missing rows to CMS cell suppression. Cost avoidance was overstated by $127,101.41 for Empath and $45,643.23 for AccentCare. **If a build produces a paracentesis benchmark near $10,660, a truncated extract has come back.**

**What the share measures.** Place of service records that the patient was an inpatient when the procedure was billed. It is not proof the encounter caused an admission, and PSPS carries no hospice indicator. CMS suppresses some low-volume cells, so the shares rest on reported rows only. State all three limits in the disclaimers.

### 8.2 Packaging, and why only two procedures package

Status indicators from CY2026 OPPS Addendum B, identical in the January and July releases:

| CPT | SI | Packages the claim? |
|---|---|---|
| 99285 ED visit Level 5 | J2 | Yes |
| 49083 paracentesis | T | No |
| 32555 thoracentesis | T | No |
| 51702 catheter | Q1 | Conditionally |
| 43762 G-tube | T | No |

Catheter and G-tube anchor on the J2 emergency visit, which packages everything else on the claim. Paracentesis and thoracentesis are status T and do not package, so labs, imaging and observation billed alongside them are absent from our figure. That makes those two benchmarks conservative. Do not describe them as comprehensive APC procedures.

### 8.3 SOS rates

Pull from the Partner Rates report, filtering Rate Category `Acuity Level` **plus** the `Telemedicine` rate, which sits under Rate Category `Service`. Filtering on Acuity Level alone silently drops Telemedicine.

| Acuity | Empath | AccentCare |
|---|---|---|
| High Complexity | $575.00 | $545.00 |
| Moderate Complexity | **$373.00** | $343.00 |
| Low Complexity | $170.00 | $150.00 |
| Telemedicine | $65.00 | $55.00 |
| No Charge | $0.00 | $0.00 |

**Corrected 2026-08-25.** Through 2026-08-22 the Empath column read $343.00 Moderate, $150.00 Low and $55.00 Telemedicine. Those are AccentCare's rates; every Empath acuity except High had been filled from the wrong partner. Decisions Log section 3 has Empath at High 575, Moderate 373, Low 170, Telemedicine 65. Neil ruled Moderate $373.00 on 2026-08-25. Moderate is the only one of the three that reaches a savings figure: it overstated Empath July by $330.00 across 11 qualifying visits, 6 catheter and 5 G-tube. Low and Telemedicine touch no qualifying visit in July.

**Confirmed 2026-08-26 by Neil.** Empath Low is $170.00 and Telemedicine is $65.00. The prior claim in this spec that $65.00 was a data entry error corrected to $55.00 is withdrawn.

**Rule.** Every rate is per partner. Never carry a value across the columns of this table.

Savings per qualifying visit = benchmark for its service minus the SOS rate for its acuity. Sum by procedure and by branch.

### 8.4 Transport figure

Round trip ALS1 non-emergency ground transport plus 30 statute miles, CY2026 Florida ambulance fee schedule: **$955.04 per episode**. Used inside both pathways, and in the "Where the Model Does Not Yet Reach" callout multiplied by the count of non-qualifying counted visits.

This is the one input never traced to a CMS source file. Everything else has been.

### 8.5 Regression baselines

**VOID as of 2026-08-25. Do not regression-test against the figures below.** They were produced from the truncated 153-row PSPS extract described in 8.1 and from the wrong Empath Moderate rate. Empath's true July total is approximately $230,633.65 against the $357,735.06 shown, AccentCare's approximately $81,632.41 against $127,275.64. Replace this whole section with fresh baselines taken from the corrected rebuild, and only then restore it as a regression gate.

Retained below only as the fingerprint of the defective build.

Empath July 2026:

```
Paracentesis           32 visits   hospital $341,104.00   SOS $18,400.00   savings $322,704.00
Thoracentesis           1 visit    hospital   $5,426.48   SOS    $575.00   savings   $4,851.48
Catheter Management    11 visits   hospital  $20,961.38   SOS  $4,933.00   savings  $16,028.38
G-Tube/PEG Management   8 visits   hospital  $17,591.20   SOS  $3,440.00   savings  $14,151.20
TOTAL                  52 visits   hospital $385,083.06   SOS $27,348.00   savings $357,735.06
average per qualifying visit $6,879.52
annualized $4,292,820.72
outside the model 66 of 118, transport-only floor $63,032.64
```

Branch savings: Suncoast Pinellas $152,769.02, Tidewell $91,436.44, Hospice of Marion County $45,673.70, Suncoast Hillsborough $37,602.40, Trustbridge $20,169.00, Polk $10,084.50, Empath Main/Primary $0.

AccentCare July 2026:

```
Paracentesis           11 visits   hospital $117,254.50   SOS  $5,995.00   savings $111,259.50
Catheter Management     3 visits   hospital   $5,716.74   SOS    $836.00   savings   $4,880.74
G-Tube/PEG Management   6 visits   hospital  $13,193.40   SOS  $2,058.00   savings  $11,135.40
TOTAL                  20 visits   hospital $136,164.64   SOS  $8,889.00   savings $127,275.64
average per qualifying visit $6,363.78
outside the model 29 of 49
```

Branch savings: Pinellas $76,075.88, Hillsborough $37,373.46, Miami $10,114.50, Pasco $3,711.80, Hernando $0, Broward no volume.

### 8.6 Year to date

Both partners restated on the current model:

| Month | Empath visits | Empath qual | Empath savings | AccentCare visits | AccentCare qual | AccentCare savings |
|---|---|---|---|---|---|---|
| April 2026 | 89 | 36 | $200,831.96 | 23 | 7 | $20,278.62 |
| May 2026 | 117 | 41 | $227,126.16 | 31 | 12 | $51,429.16 |
| June 2026 | 133 | 47 | $247,494.94 | 44 | 11 | $77,394.82 |
| July 2026 | 118 | 52 | $357,735.06 | 49 | 20 | $127,275.64 |
| **YTD** | **457** | **176** | **$1,033,188.12** | **147** | **50** | **$276,378.24** |

Historical month quirks, already handled:
- No `Visit Cancelled` acuity value exists before July. Use the note regex.
- May recorded imaging coordination visits as `No Charge` rather than `Telemedicine`. Reclassify them; billing status is not an acuity. Eleven May rows and two June rows moved for Empath.
- April has no imaging coordination visits at all. Do not reclassify April.

Any chart or table showing April through June must carry the methodology note.

### 8.7 Verification status of every input

Traced to a CMS source file and reproducing to the cent: FY2026 IPPS Table 5 weights (393 at 1.5993, 186 at 1.5585, 695 at 1.1438), Table 1A amounts ($4,456.72 labor, $2,295.89 nonlabor), capital rate $524.15, wage index 1.0369 with the capital GAF, CY2026 OPPS Addendum B rates ($926.63, $640.89, $608.43), all PFS physician fees at conversion factor $33.4009 with Rest of Florida GPCIs 1.000 / 0.956 / 1.503, and the four inpatient shares from PSPS.

Not traced: the $955.04 ambulance figure.

Full detail lives in `SOS_MPU_Methodology_Change_June_to_July_2026.md`.

---

## 9. QC gates

Stop and show Neil the number at each gate. Do not proceed past a gate on your own.

1. **Files load.** Row counts, date ranges, column count parity, duplicate ID count, join coverage.
2. **Partner split.** Counts per partner, and the full contents of the Unresolved bucket with source label, county, and patient name.
3. **Branch resolution.** Every counted row has a branch. Any row without one is a blocking failure.
4. **Classification.** Counted, Cancelled, Duplicate totals, and the acuity mix.
5. **Service mix.** Present the derived distribution and the review file. Read every `Eval (Not Performed)` note in full.
6. **Savings.** Per procedure table, total, average, annualized, and the excluded count. Run the blend check from 8.1.
7. **Render.** Zero overflow (see section 12), correct page count, continuous spine numbering.

---

## 10. Report structure

Empath July 2026 runs 19 pages, AccentCare 16. The difference is branch count: seven against five, with AccentCare's Broward carrying no volume.

| Page | Spine | Content |
|---|---|---|
| 1 | 01 | Cover |
| 2 | 02 | Section 01, Executive Summary |
| 3 | 03 | Section 02, Volume, Services, and Delivery |
| 4 | 04 | Section 03, Estimated Cost Savings |
| 5 | 05 | Section 03 continued, Aggregate Monthly Savings |
| 6 | 06 | Section 04, Savings by Branch + Section 05, Utilization Upside |
| 7 | 07 | Section 06, Year to Date Cost Savings |
| 8 | 08 | Section 07, Recurring Patients |
| 9 | 09 | Section 08, Top Referring Staff |
| 10+ | 10+ | Branch detail, one page per branch in descending visit order, plus continuation pages |
| last | N | Reference, Disclaimers |

### Cover
Logo top left, "Confidential" top right, month eyebrow, "Monthly Partner Utilization" at 60px in two lines, four color swatches, then Prepared for / Prepared by / Issued rows at 15px with 10px labels, then the PHI notice. Spine reads 01, width 56px like every other page.

### Section 01, Executive Summary
Four KPI tiles, centered: Total Visits, Prevented a Diversion, Diversion Avoidance, and Estimated Cost Avoided. The fourth is navy background with green figure. Then the savings callout in the green treatment. Then four two-column blocks: Overview, Service Highlights, Visit Complexity, Referral Patterns. **Records Reconciliation callout sits at the bottom of the page, directly above the footer rule.**

Acuity in the Visit Complexity sentence must be ordered **by count**, not by display order.

### Section 02
Left column: Services Performed as a labeled bar list, top three circled (section 11). Right column: Referral Volume by Time of Day (ten two-hour buckets) and Visit Complexity stacked bar with all five levels listed. Full width at the bottom: Branch Breakdown column chart on the seven step navy ramp.

Response Time was removed from this page and everywhere else at Josh's request, 2026-08-21.

### Section 03
Four procedure tiles, each with visit count chip, savings figure, and a two segment bar. Then the total band. Then the "Where the Model Does Not Yet Reach" callout.

### Section 03 continued
Order is: green intro explaining the blend, "Estimated Hospital Cost per Episode" dot plot, the aggregate table, then the annualized band at the bottom. Hollow circle for outpatient, filled circle for inpatient, green diamond for the blend, with the inpatient share printed under each label. The legend diamond glyph is green. **Axis auto-scales**: `ceil(max_inpatient * 1.05 / 1000) * 1000`. Never cap a marker at the axis edge.

### Section 04 and 05
Branch savings column chart, then the Utilization Upside table at 1.0x, 1.25x, 1.5x, and 2.0x. Both headings at 30px.

### Section 06, Year to Date
Line chart, not bars. Gridlines auto-scaled by picking the first step from 10k, 25k, 50k, 100k, 250k where `max/step <= 5`. Hollow dots for prior months, filled dot for the current month, value labels above each point. Then the total band, the month table, and the **methodology note**.

### Section 07, Recurring Patients
Patients seen more than once in the month. Four KPI tiles: recurring patient count, their visit count with percent of volume, diversion percent, and estimated cost avoided. Then a table: Hospice ID, Branch, Service, Visits, Off-Hours or Weekend, Diversions, Est. Savings. Then the off-hours callout, which uses the purple bar, not green.

Costly window: referral submitted before 08:00 or at or after 17:00, **or** visit completed on a weekend. Report diversion separately for that subset.

### Section 08, Top Referring Staff
Partner wide top ten by completed visits. Columns: rank, name, title, primary branch (with `+N` when they referred across multiple), a volume bar, and their two most referred services.

Do not build a per-branch referrer listing. It was tried and rejected as too long.

Name normalization: the source has no staff ID, so merge only obvious variants of one person and say which merges you applied.

### Branch detail pages
Navy header band with branch name and three figures. Then the intro paragraph in the gray callout, not green. Then Services Performed with the top row circled, and on the right Visit Complexity with all five levels in fixed order High, Moderate, Telemedicine, Low, No Charge, zeros shown muted. Then the diversion callout. Then Patient Visit Detail.

The intro paragraph is generated and must degrade gracefully for single-visit and single-service branches, and must order acuity by count.

### Disclaimers
Two column reference page. The Scope of Savings Model entry must state the split explicitly. The Pathway Weighting entry must disclose all three limits from 8.1. The Comprehensive APC entry must state that only catheter and G-tube package.

---

## 11. Design system

Letter portrait, 816 x 1056 px at 96 dpi. Page container is `.page` with `overflow: hidden`.

### Palette
| Token | Hex | Use |
|---|---|---|
| Navy darkest | `#0b0b5b` | Headings, primary bars, table headers |
| Navy spine | `#0d155c` | Spine rail, branch header band |
| Mid purple | `#5b5b9a` | Secondary bars, labels, callout rules |
| Light purple | `#a5a5c8` | Tertiary bars, footer text, spine text |
| Pale | `#c4c4dd` | Low Complexity swatch |
| Very pale | `#e0e0ef`, `#eeeef5`, `#f2f2f7`, `#f7f7fb` | Ramp tail, tracks, gray callouts |
| Green | `#02cd3b` | Savings figures, hand drawn circles, green callout rule |
| Green fill | `#effcee` | Section intro callout background |
| Red | `#ff0000` | No Charge swatch, Not Provided text |
| Body text | `#000000` | All body copy, table cells, legends |
| Caption | `#5b5b9a` | Small annotation lines under charts |

Seven step branch ramp: `#0b0b5b`, `#383a80`, `#5b5b9a`, `#8181b2`, `#a5a5c8`, `#c4c4dd`, `#e0e0ef`.

**No Charge is red, not green**, including muted zero rows.

### Type
Headings: Libre Franklin, weights 600, 700, 800. Body: Figtree, weights 400, 500, 600, 700. Both embedded as base64 `@font-face` rules; there is no network font link. Anything at weight 400 to 600 is body and uses Figtree.

Page title 30px/700. Cover title 60px/700. Section eyebrow 12px/800, 0.2em tracking, uppercase, `#5b5b9a`. Block headings 12px/700 uppercase navy with a 2px navy bottom rule. Body 11 to 13px/400 at 1.6 line height. Section intro callouts 12px, uniform across all sections.

### Spine
Fixed 56px rail on every page including the cover. The SOS circle favicon sits at the vertical position of the section title, the vertical uppercase label fills the middle, and the two digit page number sits at the footer line. Rail padding is `58px 0 35px 0`.

### Footer
`SOS Mobile Medical Care, Monthly Partner Utilization - Confidential` on the left, `{Partner or Branch} | {Month}` on the right, above a 1px `#a5a5c8` rule, with `margin-top: auto` so it pins to the bottom. Savings pages append ` · Modeled estimates; see Disclaimers`.

### Page rhythm
Content columns are `display: flex; flex-direction: column; gap: 22px` with no `justify-content: space-between`. Space-between stretches leftover room into arbitrary gaps and makes every page space differently.

### Hand drawn circles
Green SVG ellipses with deliberate asymmetry and an overshoot tail. Used on the top three services in Section 02 and the top service on each branch page.

Group circle (three rows), viewBox `0 0 400 60`, `preserveAspectRatio="none"`, `vector-effect="non-scaling-stroke"`, stroke `#02cd3b` at 2px, opacity 0.9:
```
M 397 24 C 399 46 331 59 199 59 C 70 59 3 47 3 30 C 3 13 70 2 199 2
C 328 2 397 10 396 25 C 395 45 380 56 348 59
```
Wrapper: `position: relative; margin: 5px 0 15px 0;` and the SVG inset `left/right -12px, top -11px, bottom -14px`.

Single row circle, viewBox `0 0 400 44`:
```
M 397 19 C 399 33 331 42 199 42 C 70 42 3 34 3 22 C 3 10 70 2 199 2
C 328 2 397 8 396 20 C 395 33 380 40 348 42
```
Wrapper `padding-top: 3px`, SVG `left -10px, top -12px, width calc(100% + 20px), height 45px`.

The bottom right arc is the part that clips text. If a value column is being crossed, lower that segment and the tail rather than shrinking the whole ellipse.

### Prohibited characters
**No em dashes anywhere.** Not in prose, not in the HTML title tag, not as a table placeholder. Use commas for prose and `&#8211;` (en dash) for empty value cells.

---

## 12. Build and render

Pure HTML with inline styles, one file, no external assets. The SOS logo, the spine favicon, and both font families are embedded as base64.

```css
.page { width: 816px; height: 1056px; overflow: hidden; background: #fff;
        margin: 24px auto; box-shadow: 0 2px 16px rgba(11,11,91,0.14); position: relative; }
@media print {
  body { background: none; }
  .page { margin: 0; box-shadow: none; page-break-after: always; }
  @page { size: letter; margin: 0; }
}
```

PDF via headless Chromium (Playwright), `format='Letter'`, `print_background=True`, zero margins, `prefer_css_page_size=True`, after a 4 second wait.

### Overflow check, mandatory before shipping

```python
bad = page.evaluate("""() => {
  const out=[];
  document.querySelectorAll('.page').forEach((pe,i)=>{
    const pb=pe.getBoundingClientRect().bottom;
    pe.querySelectorAll('table,div').forEach(el=>{
      const r=el.getBoundingClientRect();
      if(r.bottom>pb+1 && r.height>0) out.push([i, Math.round(r.bottom-pb), el.tagName]);
    });
  });
  return out.slice(0,20);
}""")
```

Must return empty. `.page` has `overflow: hidden`, so an overflow silently truncates rather than erroring.

Also grep the rendered PDF text for superseded figures before shipping. After the 2026-08-21 corrections, the strings `5,775`, `10,220`, `3,897`, `2,549`, `32.8%`, `76.1%`, `26.8%`, `347,650` and `117,161` should not appear except where a branch acuity percentage legitimately reads 6.7%.

### Branch page row budget

First branch page: `max(16, 38 - 2*len(services)) - 6` patient rows, the 6 accounting for the intro callout. Continuation pages take 38 rows. Recheck overflow after any change; adding a block always costs rows.

---

## 13. Data defects to expect

- **Missing hospice IDs.** July had 24 counted Empath rows with a blank or placeholder ID. Backfill from the referral record first, then from the same patient's other visits in the month. Anything still empty gets escalated to Neil, then rendered as `Not Provided` in `#ff0000` if he cannot supply it. Neil's standard: every record in the MPU must be 100% complete.
- **Placeholder IDs.** `Hospice`, `Unknown`, `EMPATH`, `TIDEWELL HOSPICE`, `N/A` are not IDs. Treat as blank.
- **Name spelling drift across files.** `McHugh` in one file and `McHigh` in another. **Key on Hospice ID, never on name.** This caused a wrong finding during the July build.
- **Impossible dates.** July had a referral dated 08-03 for a visit completed 07-31.
- **Referral rows absent for real visits.** Recover them rather than dropping them at the join.
- **Blank `Referral Source`.** Resolve from the referral record and the hospice ID format.

---

## 14. Start of a new partner report

1. Confirm the branch map (counties to branch names, plus the catchall, or that there is none).
2. Confirm contracted rates by acuity, including Telemedicine from the Service category.
3. Confirm which partner-name spellings map to this partner and which similar-sounding organizations do not.
4. Then run the pipeline unchanged.

Everything else in this document is partner independent.

---

## 15. Session close

Write the session log to Apple Notes, folder `SOS Code`, named `[Project Name] - SOS Session Log - [Month DD, YYYY] (Session N)`, plain text, and produce a downloadable copy. Update `context/23_task_list.md` and issue the ccode prompt so the repo stays in sync.
