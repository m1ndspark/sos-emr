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
