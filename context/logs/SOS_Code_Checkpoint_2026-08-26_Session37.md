# SOS Code Checkpoint | 2026-08-26 | Session 37

Covers work since the Session 36 checkpoint (2026-08-20). Scope this session was
MPU reporting only. No Creator or Deluge work was done.

---

## 1. Empath July 2026 report finished and sent

- Layout: every page top-aligned, uniform 22px object spacing, footers pinned by a
  single flex spacer. Removed `justify-content: space-between` and all stretch
  (`flex: 1`) from content blocks, which had been distributing whitespace unevenly.
- Records reconciliation paragraph corrected. It read 134 submitted / 10 cancelled /
  6 duplicate. The normalized workbook says 137 submitted / 10 cancelled /
  7 duplicate / 1 folded / 1 excluded. Every other figure in the report was correct.
- All estimate figures rounded to whole dollars. CMS source-rate citations on page 5
  (hospice per diems $202.26, $227.61, $1,058.00, $1,185.05) keep cents by Neil's ruling.
- Cover spine narrowed from 88px to 56px to match interior pages.
- Final figures unchanged: 118 visits, 54 qualifying, $233,810, $4,330 average,
  $2,805,722 annualized, YTD $860,813 across 187 of 472.
- Neil sent this report to Andrea Garr on the night of 2026-08-25.

## 2. AccentCare rebuilt from the normalized workbook

Previously on classifier-derived numbers. Rebuilt on the verified Empath master.
Counted visits 49 to 51. Qualifying 20 to 19. Savings $80,313.18 to $76,566.
Branches 6 including Broward, down to 5 with Hernando at zero qualifying.
Recurring patients 4 / 12 visits, up to 6 / 16 visits. 16 pages.
Branch savings: Pinellas $43,743, Hillsborough $23,299, Miami-Dade $5,111,
Pasco $4,412, Hernando $0.

## 3. InnoVage, new report type built

3008 evaluations carry no savings model, so the hospice template does not fit.
Built a separate 10-page report from two sources joined on referral ID: the
normalized workbook for referrals, 3008_july_map.csv for completions.

83 referrals, 76 evals completed, 91.6%, Orlando 50/46, Tampa 33/30, 7 open.
All 76 completions closed within one business day, 58 same day.

Three defects found against the prior July docx:

1. Its pending list showed REF-072926-1467 (Veronica Adejola) as pending. That one
   completed 07/29. The actually-open referral is her earlier REF-072126-1401,
   which the docx omitted.
2. It counted completions by the completion log's site (48/28) against referrals by
   routing (50/33). This report counts both by routing so they share one denominator.
   Four records disagree between the two.
3. 22 InnoVage dates of birth are stored in the wrong century, 2030 to 2045, from
   two-digit year entry. Displayed corrected; records untouched.

## 4. VITAS and Chapters, third report type built

Both are very low volume, so a 3-page format: cover, one summary page carrying
every visit on one line, disclaimers. No charts.

- VITAS: 6 counted from 8 submitted, 100% diversion, 1 qualifying at $3,554.
  Lake priced at Sumter's rates per Neil's ruling. Note this is 6, not the 5 Neil
  expected.
- Chapters: 3 counted, 100% diversion, 1 qualifying at $5,111. Rates found in
  Partner Rates Report (13).xlsx: High 545, Moderate 323, Low 150, uniform across
  HPH Hospice, LifePath and Good Shepherd. No Telemedicine rate exists for Chapters.

Chapters carries an alert-styled box (red bar, #fce0e0) on page 2 because its two
excluded visits are deferred evaluations, not unbenchmarked service types. The
generic wording claimed they carry no published benchmark, which is false for
paracentesis. The template picks the alert version only when every excluded visit
is a deferred evaluation, so it stays correct as volumes change.

Both excluded Chapters visits were re-reviewed against their clinical notes and are
correctly classified: Glema Smith, bedside ultrasound found no ascites; Mercedes
Fangul, trace non-drainable ascites, did not meet criteria for palliative
paracentesis.

## 5. Cross-cutting changes applied to all five reports

- Whole dollars everywhere except CMS source-rate citations.
- 24 placeholder table cells now read N/A instead of an en dash.
- Cover spine 56px.
- True zeros left as zero, not N/A: InnoVage's Saturday heatmap total and
  AccentCare's greyed 0 / 0% branch acuity rows.

## 6. Folder reorganization

MPU Reporting/ now holds one folder per partner. Each carries the _FINAL files at
the top and everything superseded in Archive/ renamed _DRAFT_<date>. VITAS and
Chapters previously had only an Archive; both now have a FINAL. Working files moved
to _Working/. Everything else left at the root.

## 7. Multi-tab monthly workbook

SOS_MPU_Monthly_Normalized_AprJul2026.xlsx, seven tabs: YTD Summary, April, May,
June, July, All Months, Sources & Caveats. 834 rows on one 24-column schema.

Three findings recorded on the Sources tab:

- Counted visits do not match the April to June figures printed in the issued
  reports. This workbook: Empath 89/115/126, AccentCare 22/32/42.
- April and May carry no cancelled or duplicate rows because the Clean Visits tabs
  were adjudicated upstream, so Submitted equals Counted for those months.
- June carries no service classification at all. Visit Type holds only
  patient visit, Xray order (only), 3008 or Cancelled.

## 8. Templates, and the PHI problem this created

REVISED at end of session. The earlier plan was to keep the finished Empath and
InnoVage reports in docs/mpu/templates/ as masters. That was wrong: a finished
report carries patient names, hospice IDs and dates of service, and this repo is
documented as holding field link names rather than patient data.

Measured before removal:
- MPU_Master_Hospice_Savings.html: 8 patient tables, 9 hospice ID columns,
  118 date-of-service strings.
- MPU_Master_3008_Evaluations.html: 5 patient tables, 170 date-of-service strings.
- MPU_Partner_Report_Master_2026-08-26_superseded.html: same as the first.

All three were untracked and have been MOVED OUT of the repo to
MPU Reporting/_Working/repo_phi_pulled_2026-08-26/. Nothing was deleted.

The generators DO belong in the repo. They hold structure and CSS only, no patient
data; their two "Patient Name" matches are column headers.
- templates/generators/gen_hospice_savings.py
- templates/generators/gen_3008_evaluations.py

STILL OUTSTANDING: five earlier commits carry the same file with the same PHI.
fbbb2c4, ba011ac, 0be76d4, e3bcc65, b46f474, all local and unpushed. History must
be rewritten before any push. See section 11.

## 9. Rate conflict, closed

Partner Rates Report (13).xlsx (21 Aug) shows Empath Moderate 343, Low 150,
Telemedicine 55, and Polk High 545, against the build spec's 575 / 373 / 170 / 65.
Neil ruled his own confirmations govern; the export is stale. Empath as shipped is
correct. Do not reopen this.

## 10. Working-practice change

Neil: stop writing every iteration to his folders. Iterate in chat, write to disk
only once a version is approved.

## 11. PHI in git history, DECISION PENDING

Five unpushed commits carry docs/mpu/templates/MPU_Partner_Report_Master.html,
which is the full Empath July report including every patient row.

main is 10 ahead of origin/main and 2 behind. A push sends all ten.

NOTHING MAY BE PUSHED until the history is rewritten.

The schema monitor is NOT the risk. Reviewed 2026-08-26: run_schema_monitor uses the
GitHub Contents API (PUT /repos/{owner}/{repo}/contents/{path}, connection
sos_github_sync), not git. It commits one file at a time straight to origin/main and
has no access to the local clone, so it cannot carry the local commits anywhere. That
is also why local main is 2 behind: the two schema commits arrived by API.

The only thing that can send the PHI is a deliberate git push from the local clone,
by Neil or by ccode.

Options, for Neil to choose:
(a) git filter-repo --invert-paths on that one path, then force the local branch.
(b) Soft reset to 267d57d, re-apply only the clean changes as one commit, then pull
    the two schema commits.
Either way the generators and the e554cba spec work are kept; only the HTML is
purged.

---

## 12. InnoVage open-referral dispositions, IN PROGRESS 2026-08-26

Neil is classifying all 83 July referrals, not only the 76 that completed in July.
"Open" in the current build is an inference, not a recorded status: it is the set
difference between the 83 referrals in the workbook Master and the 76 referral IDs
in 3008_july_map.csv. Nothing in any file marks a referral open.

Dispositions supplied so far:

| Referral | Patient | Disposition |
|---|---|---|
| REF-072126-1401 (07/21) | Veronica Adejola | DUPLICATE. She has two July referrals; REF-072926-1467 (07/29) completed and was counted. Remove 1401. |
| REF-072326-1419 (07/23) | Michael Lahee | DUPLICATE. Billed on the original June referral. |
| REF-072926-1483 (07/29) | Eliette Patterson | COMPLETED 07/31 and billed in July. She was never open. |
| REF-072326-1422 (07/23) | Mattie Richards | OPEN. Awaiting additional information from InnoVage. Request date not yet supplied. |
| REF-072926-1484 (07/29) | Aurea Aviles | OPEN. Same partner-side delay; information not provided until after 07/31. Request date not yet supplied. |
| REF-073126-1497 (07/31) | Myrtelina Rivera | COMPLETED 08/03. Referred 07/31, evaluated in the next reporting period. |
| REF-073126-1498 (07/31) | Donna Buckley | COMPLETED 08/03. Referred 07/31, evaluated in the next reporting period. |

Restated July totals once applied:

- Referrals received 83, duplicates removed 2, adjusted base 81
- Evals completed 77, up from 76
- Open at cutoff 4, down from 7
- Completion rate 95.1%, up from 91.6%

FLAG: Eliette Patterson completed 07/31 and was billed in July but does NOT appear
in 3008_july_map.csv. The completion log is therefore missing at least one July
completion, and should not be treated as authoritative on its own.

All seven are now classified. Final July disposition of the 83 referrals:

- 2 duplicates, removed from the denominator: Adejola 1401, Lahee 1419
- 77 evals completed within July, including Patterson on 07/31
- 2 completed 08/03, carried into the August period: Rivera, Buckley
- 2 still open at 08/26, both awaiting information from InnoVage: Richards, Aviles

Adjusted base 81. Completed in July 77, 95.1%. Carried into August 2. Open 2.

BLOCKED pending Neil: the dates SOS requested additional information from InnoVage
for Richards and Aviles. Everything else needed for the rebuild is in hand.
