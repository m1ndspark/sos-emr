SOS MPU - Build Procedure and Source of Truth
Written 2026-08-26 after a session in which the wrong source was used three
separate times. Read this BEFORE touching an MPU report, a savings figure, or a
model document. It exists to stop the specific failures listed in section 6.

=====================================================================
1. SOURCE OF TRUTH, IN ORDER
=====================================================================
When two artifacts disagree, the one higher on this list wins. Do not average
them, do not pick the newer one by default, and do not re-derive a number that
one of these already carries.

  1. [MONTH][YEAR]_MPU_Normalized_Data.xlsx, Master tab.
     The joined referral + PVS dataset. Carries Partner, Branch, Visit Type,
     Acuity, Diversion, Row Status, Flag / Duplicate Note, Hospice ID, Provider,
     After Hours, SuperStat, Equipment. THIS IS THE ADJUDICATED DATASET.
     Filter Row Status == "Counted" for anything that appears in a report.
     Row Status values: Counted, Cancelled, Duplicate, Excluded, Folded.
     Per-branch tabs carry the same rows filtered to that branch, and are the
     source for Patient Visit Detail tables.
     ITS SAVINGS MODEL TAB IS NOT A SOURCE. It is frozen at whatever model was
     current when the workbook was built and goes stale immediately.

  2. sos-emr/docs/mpu/SOS_MPU_Savings_Model_CY2026.md
     Every hospital benchmark, pathway component, admit share, and computation
     rule. Canonical over the MPU Reporting working copy and over the project
     copy. If they differ, the repo wins and the other two get resynced.

  3. sos-emr/docs/mpu/SOS_MPU_Report_Build_Spec_v1.md
     Layout, section order, reconciliation counts, partner rate table.

  4. claude/SOS_MPU_Reporting_Decisions_Log.md
     Neil's rulings. Beats the v1 instructions on any conflict.

  5. Raw exports (PatientVisitSummary2, PatientReferral, monthly PVS files).
     LAST RESORT ONLY. Use these to derive a Visit Type only when no normalized
     workbook exists for that month. Say so explicitly in the output when you do.

=====================================================================
2. PRE-FLIGHT, EVERY TIME, BEFORE ANY EDIT
=====================================================================
Answer all six in writing before the first change. If any answer is "I think"
or "probably", stop and check.

  1. What is the source of truth for this number? Name the file and the tab.
  2. Have I opened it this session, or am I recalling it?
  3. Does a normalized workbook exist for this month? Run:
       ls ~/Claude/MPU\ Reporting/*Normalized_Data.xlsx
  4. Which artifact am I editing, and is it the one the build actually reads?
  5. What else carries this same number and will now disagree with it?
  6. What does the change do to the total, and does the total still foot?

=====================================================================
3. NEVER ASSERT A FILE IS MISSING
=====================================================================
Before saying "I do not have that file" or "you need to send me X":
  1. ls the Downloads folder filtered on a keyword from the file's purpose.
  2. grep the model doc and the build spec for the file name. Both name their
     own source files, including the annual refresh list.
  3. Only then say it is missing, and name where you looked.
Three separate times on 2026-08-26 a file was declared missing while sitting in
Downloads, and in one case while named in our own spec.

=====================================================================
4. VALIDATING AN EXTRACT BEFORE USING IT
=====================================================================
An extract someone hands you is not a source. Check it against the full file.
  - Row count. Florida PSPS holds 2,176 rows across the four CPTs. A 153-row
    file is a truncation, not a filter.
  - Reproduce one known value from the extract and confirm it matches the
    canonical document. If it does not, the extract is wrong, not the document.
  - For a prefix-ordered file, a truncation looks like a valid sample and is
    not one. Check min and max of a sort key, not just the count.

=====================================================================
5. AFTER ANY REPORT EDIT
=====================================================================
  1. Render the whole document and LOOK AT EVERY PAGE. Not the pages you
     changed. Every page. Removing a block can unbalance tags and collapse a
     layout three pages away.
  2. Confirm div balance on any page where markup was removed:
       opens = len(re.findall(r'<div\b', page)); closes = page.count('</div>')
     Never strip an element with a non-greedy regex ending in nested closers.
     Walk the tags and balance them.
  3. Re-derive every chart's geometry from its new values. Replacing a label
     does not move a marker. A chart whose axis maximum is below its own
     largest value is a defect, not a rounding issue.
  4. Foot the totals: branch savings must sum to the report total; monthly
     rows must sum to the YTD row.
  5. Check for stale counts in narrative sentences and disclaimers, which do
     not move when a table cell does.

=====================================================================
6. WHAT WENT WRONG ON 2026-08-26, SO IT DOES NOT REPEAT
=====================================================================
  - Built two partner reports off raw PVS exports and a regex classifier while
    July2026_MPU_Normalized_Data.xlsx sat unopened in the same folder. Its
    Master tab already carried adjudicated Visit Type, Branch and Acuity.
  - Reversed a correct finding because a 153-row truncated extract contradicted
    it, without checking the extract against the 841 MB source.
  - Said the hospice per diem file did not exist. It was in Downloads and named
    in our own model doc's source list.
  - Stripped a block with a non-greedy regex, collapsing eight page layouts, and
    delivered the file without looking at those pages.
  - Told Neil to review output whose numbers were mine to verify.

=====================================================================
7. WHEN SOURCES GENUINELY CONFLICT
=====================================================================
Do not pick one. Report both, quantify the difference in dollars and visits,
name which rows differ, and ask. A conflict between the normalized workbook and
a later ruling is a real question about which adjudication stands, not a
tie-break for you to make.


=====================================================================
8. HTML EDITING FAILURE MODES, 2026-08-26
=====================================================================
Five ways a report was broken this session by editing HTML with string
operations. All five are cheap to prevent and expensive to find later.

  8.1 NEVER REPLACE A BALANCED BLOCK WITH HAND-COMPUTED STRING OFFSETS.
      Two page layouts collapsed because find('</div></div>') matched the
      wrong closer. That string occurs many times in a report and nothing
      about it identifies the block you meant. Walk the tags and count depth
      until the matching closer is found. If a balanced walk feels like too
      much work for the edit, the edit is still not allowed to guess.

  8.2 ASSERT ON EVERY ANCHOR STRING.
      A missing anchor returned -1, which is a valid index in Python, so the
      replace silently appended a duplicate table body instead of replacing
      one. The report shipped with eight year-to-date rows where four
      belonged, and nothing raised. Every anchor gets an assert that it
      exists, and every replace asserts the expected number of occurrences
      before it runs. An edit that cannot find its anchor must stop, not
      continue with -1.

  8.3 RENDER EVERY PAGE AND CHECK DIV BALANCE AFTER ANY EDIT.
      Both, not either. Balance alone is not sufficient: two offsetting
      errors cancel and the count comes back clean while the layout is
      wrong. Render the pages and look at them.

  8.4 WHOLE DOLLARS FOR EVERY MODELED FIGURE.
      Savings, rates, benchmarks, transport, totals. No cents. The one
      exception is a CMS source-rate citation, which keeps its cents because
      it is quoting a published figure rather than presenting a model output.

  8.5 TABLE CELLS WITH NO APPLICABLE VALUE READ N/A.
      Not an en dash, not a blank, not a hyphen. A true zero stays 0, because
      zero and not-applicable are different facts and a reader cannot tell
      them apart once both render as punctuation. Chapters having no
      Telemedicine rate is N/A. A branch with no qualifying visits is 0.
