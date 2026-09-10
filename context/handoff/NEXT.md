# Handoff - 2026-09-10 - Session 43 cleanup

Two small items, then a note.

1. Delete `functions/backfill_referral_upload_fields.dg`. Neil ruled on it: it
   is a Sept 4 draft that never went live, absent from v43, superseded by the
   live `backfill_referral_uploads` already captured in the sweep. It still
   carries its declaration line. Remove it and commit.

2. Confirm `Provider_Identity_Stamp1` is gone from the next .ds export. It is a
   live workflow on `Referrals_Main`, On Validate, Created or Edited, with an
   EMPTY body, created by accident during Session 42 when cchat had Neil open
   the PVS workflow from the Referrals_Main list. Neil is deleting it in
   Creator. Nothing for you to do now beyond checking it is absent when v44
   lands, and flagging it if it is still there.

Note, no action: `context/01_standing_rules.md` gained a new section,
VERIFICATION BEFORE EXPLANATION, in commit 3902283. It records why cchat
twice explained away contradicting evidence instead of checking, and sets the
rule that a contradiction triggers a query before an explanation. Item 4 of
that section names ccode as the deterministic check on anything file based.
That is now written policy, not a courtesy. Keep reporting what you find even
when it contradicts what cchat asserted.
