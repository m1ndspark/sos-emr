# Handoff log

Newest entry at the top. Written by ccode via the `/handoff` skill.
Read by cchat off the local mount.

## 2026-09-10 - Session 43 cleanup
Commits: (this commit only)
Status: DONE

1. functions/backfill_referral_upload_fields.dg deleted. Verified all four
   grounds before removing: absent from v43 (grep count 0), untracked (git
   ls-files returned nothing), still carrying its declaration line
   `string backfill_referral_upload_fields()`, and the superseding live
   backfill_referral_uploads.dg present in functions/. The working tree is now
   clean.
2. Provider_Identity_Stamp1 - nothing to do yet. No v44 export exists; the
   newest is SOS_Referrals_App_2026-09-10_v43.ds and the root copy still
   matches it. The workflow is STILL PRESENT in v43 (grep count 1), which is
   expected since Neil had not yet deleted it in Creator when v43 was taken.
   Will confirm absence when v44 lands.

Findings: the file in item 1 was untracked, so its deletion produces no diff
and this commit contains only LOG.md and NEXT.md. Nothing is lost - git never
held that file, so there is no history to recover it from if the ruling is ever
reversed. Its content was a 919-byte draft dated Sept 4.

Repo state after this handoff: ds_sync against v43 reports DRIFT 0, NEW 0,
MATCH 195. The remaining non-MATCH rows are unchanged and none are new:
EMPTY on Provider_Identity_Stamp1 (item 2 above) and log_change; AMBIGUOUS on
Diag_Session_Identity (deliberately fileless), Validate_Complexity_On_Fi
(pre-existing), and the two Partner_Rates workflows that token-score onto one
file (Partner_Rate_Stamp_Genera1 is byte-identical to the repo file and owns
it; Partner_Rate_Partner_Stam exports an empty body).

Noted, no action: context/01_standing_rules.md VERIFICATION BEFORE EXPLANATION
read and understood. Item 4 naming ccode as the deterministic check on
file-based claims is how this session has been operating; it will continue.

Awaiting Neil: none.

================================================================================
Session 43 follow-up (2026-09-10) - ccode
================================================================================
Took both corrections, recorded all three answers. No Deluge touched, so the
context/08 audit gate does not apply.

CORRECTION 1 TAKEN. context/01_standing_rules.md BACKFILL SIGNATURE now reads
snake_case:

    string backfill_<thing>(string p_mode, string p_scope)

Added a line saying the doc was the outlier and the code was never wrong, so
nobody "fixes" a working function back to camelCase. Also recorded that a more
specific second parameter is acceptable when the scope is one key type, since
backfill_pvs_referral_date(p_mode, p_pvsKey) already does this and would
otherwise read as a violation.

CORRECTION 2 TAKEN. context/09 section 5C moved from line 370 to sit
immediately before section 6. Verified as a pure move: sorted content before and
after is byte-identical, 417 lines both ways, nothing lost or reworded.

STILL OUT OF ORDER, NOT TOUCHED: 5A sits AFTER 5B in that file (5 at 212, 5B at
247, 5A at 313, 5C now at 341, 6 at 391). Your instruction was specific to 5C so
I left the 5A/5B inversion alone. If "reads in order" was the real goal, that
swap is still outstanding. Say the word and I will do it.

ANSWER 1 RECORDED. backfill_mint_missing_referral_ids is now DRIFT A in the
known-drift section of context/19, with the PREVIEW and COMMIT run figures and
the REF-1463 confirmation. That section was titled "behind live by one line" and
covered one item; it now covers two and is retitled. Explicitly noted that it
must NOT be extracted into functions/ until v45 exists, and that its absence
from MANIFEST.tsv is expected until then. Also recorded that this settles the
count: v44 holds four, the fifth postdates the export.

ANSWER 2 RECORDED. Branch_Sets_Partner_Link verdict kept, evidence replaced.
Both places in context/19 updated: the inventory line now reads DISABLED with
"UI confirmed by Neil 2026-09-10", and the status-flag section records the
re-check as RESOLVED rather than pending. Added the REF-1458 corroboration
(PartnerLink=- and PartnerID= empty until backfill_referral_partner_fields ran),
since a disabled workflow predicts exactly that failure and is better evidence
than any flag in the export. Added the general lesson: when export and UI
disagree, treat the export's evidence as worthless and re-derive the answer
rather than assuming its verdict is wrong. Here the verdict held. It may not
next time.

ANSWER 3 RECORDED. The August adjudication is in context/32 under the
Performed vs Eval gap, as a table: 30 performed rows all High Complexity, 13
evaluated-not-performed all Moderate or Low, zero exceptions, adjudicated across
all 164 notes.

I recorded it as strong evidence, not as settled, and wrote the caveat in
plainly: it is one month, adjudicated by hand rather than enforced by the form,
and nothing stops a provider from coding a performed procedure as Moderate. It
is an observed correlation, not a constraint. If the metric ever becomes
load-bearing for billing or partner reporting it needs a second month that
holds, or an On Validate rule that makes the correlation real. Flagged that
Neil's ruling is pending and that no second procedure list gets built before it.

CONFIRMED UNCHANGED: both context/19 notes from the prior entry stand as
written. Nothing hand-written into Referral_Link_Pre_Fill.

Repo state: ds_sync against v44 reports MATCH=199, DRIFT=0, NEW=0. The four
non-MATCH rows (Diag_Session_Identity, Validate_Complexity_On_Fi, the two
Partner_Rates collisions) and EMPTY log_change are unchanged and all pre-exist
in v43. context/23_task_list.md still untouched by me.

Awaiting Neil: the Performed vs Eval ruling. Awaiting you: whether to swap
5A and 5B.

================================================================================
Session 43 follow-up 2 (2026-09-10) - ccode
================================================================================
5A/5B SWAP DONE. context/09 now reads 5, 5A, 5B, 5C, 6, 7 in order:

    5 @212   5A @247   5B @275   5C @341   6 @391   7 @401

Same verification as the 5C move: sorted content byte-identical before and
after, 417 lines both ways, diffstat 28/28 which matches the 5A block length
exactly. Pure move, nothing reworded.

Checked cross-references, none broke. All three are by section name rather than
by direction: line 15 points to 5B(a), the checklist points to 5A-a and 5A-c.
The only "above" inside the moved blocks is "Section 0-A above", and 0-A is
still above. The other two directional-looking words ("earlier conclusion",
"previously dropped") are chronological, not positional.

PROPOSED SHAPE RECORDED. context/32 now carries both branches of Neil's ruling
under the Performed vs Eval gap, so nothing is owed when it lands:

  REQUIRED   -> On Validate rule on Encounter_PatientVisit making the
                Complexity_Level correlation real. Not a second procedure list.
  DESCRIPTIVE-> leave it derived, close the question, no build.

I added two implementation warnings to the REQUIRED branch, because "write an On
Validate rule" hides both of them:

1. It fires on rows that predate it. Anything already in the system that
   violates the correlation will block on edit until corrected, or the rule has
   to be scoped to new records only. August had zero exceptions, but August is
   not the whole table.
2. Complexity_Level carries TEN choices, not two. Verified against v44: High,
   Moderate, Low, Hospital at Home, Telemedicine, Care Coordination, General
   Consultation, No Charge, Cares 3008 Assessment, Visit Cancelled. The rule has
   to state which ones count as performed. Assuming High is the only one is
   wrong on its face, since a performed procedure on a Telemedicine or Care
   Coordination row is not excluded by anything in the data.

Also stated plainly in the doc that the second procedure list is off the table
either way: it was the original spec's answer and it is the wrong one.

Your reframing of answer 3 is on record in the doc as written, not as
"Complexity_Level already carries it".

Repo state: no Deluge touched, context/08 gate does not apply. ds_sync against
v44 unchanged at MATCH=199, DRIFT=0, NEW=0. context/23_task_list.md still
untouched by me. Both DO NOTs still stand: no extraction of
backfill_mint_missing_referral_ids until v45, no hand-written Referral_Date
lines in Referral_Link_Pre_Fill.

Awaiting Neil: the Performed vs Eval ruling, now fully scoped both ways.
Awaiting you: nothing.

================================================================================
Session 45 (2026-09-11) - ccode
================================================================================
Docs updated: context/01 (DATA PROVENANCE, scope reversal, PVS repair guard),
context/05 (9 Session 45 learnings), context/23 (8 DONE, 15 OPEN), context/24
(41-row rebuild, Partner Locations Dropdown). No Deluge touched, context/08 gate
does not apply.

TWO ITEMS COULD NOT BE DONE. Neither file exists anywhere in the repo, tracked
or untracked, and nothing was pasted:
  - SOS_Code_Checkpoint_2026-09-11_Session45.md  (item 1)
  - SOS_ZohoForm_Creator_Mapping_2026-09-11.md   (item 6)
I did not invent either one. context/logs/ is unchanged and still ends at
Session 42. Both are waiting on Neil to drop the files.

ONE CONTRADICTION, RESOLVED IN FAVOUR OF THE NEW RULE. context/01 previously
said p_scope blank "means ALL". The new rule says blank returns SKIP-NOSCOPE.
These are exact opposites. I applied the new rule and recorded the reversal in
place rather than leaving the doc arguing with itself, because a blank scope is
almost always a forgotten argument and the old default turned that into a silent
full-table write. If the old behaviour was deliberate, say so and I will revert.

V45 IS UNSYNCED AND I DID NOT SYNC IT. ds_sync against v45 reports DRIFT=4,
NEW=2:
  DRIFT  Encounter_PatientVisit/OnLoad__Default_Hide_On_Load.dg
  DRIFT  Encounter_PatientVisit/OnUserInput__Edit_Needed__Unlock.dg
  DRIFT  Encounter_PatientVisit/OnUserInput__Referral_Link__PreFill.dg
  DRIFT  Encounter_PatientVisit/OnValidate__PVS_Required_Fields.dg
  NEW    functions/backfill_mint_missing_referral_ids.dg
  NEW    functions/diag_unnotified_referrals.dg
Referral_Link_Pre_Fill is the Session 43 known drift finally landing, and
backfill_mint_missing_referral_ids is DRIFT A from the same entry. Both are now
extractable. I left them alone because this writes Deluge and therefore trips
the context/08 gate, and the commit message Neil specified covers docs only.
Say the word and it is one gated commit.

THE REPO HAS NO ARTIFACT FOR ANY OF TODAY'S CODE. process_new_referral,
sos_referral_health, sweep_unnotified_referrals, the imaging notifications and
the mint_referral_id rewrite are all absent from v45 AND from the repo. Verified:
functions/mint_referral_id.dg still holds the old bare-assignment body, and the
On Create master is still 415 lines with no call to process_new_referral. I
marked the tasks DONE as instructed but wrote the missing-artifact note into
each row, because "DONE" with nothing committed is exactly what the standing
rule in context/01 exists to prevent. A fresh .ds is filed as BLOCKING Y.

Everything else verified against v45 before writing: Assignments.Patient_DOB is
text maxchar 11; Referrals_Main.Patient_DOB is date "Patient DOB (system)" and
Patient_DOB1 is text maxchar 11 "Patient DOB"; Invoice_Status is {Draft,Final}
and Hold_From_Invoicing is {No,Yes}; the three URL fields are textarea and the
three upload fields are upload file; all four other mint_* functions carry the
same bare-assignment pattern as mint_referral_id. containsKey appears in zero
repo files.

Awaiting Neil: the two dropped files, and a call on the v45 sync.
