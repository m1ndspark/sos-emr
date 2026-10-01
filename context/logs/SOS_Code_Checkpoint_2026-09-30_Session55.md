SOS Code - CHECKPOINT - 2026-09-30 (Session 55)

Work since the Session 54 checkpoint (09-25). Spans 09-29 evening and 09-30.

===============================================================
PART 1 - PVS FAX REVIEW: OVERRIDE SPINNER
===============================================================
Cause: On User Input workflows "PVS Fax Review Format Override Fax" and
"...Format Override Fax Confirm" set their own field on every run, which
re-fired the same handler (endless loop, spinner never stops).
Fix: write back only when the formatted value differs from what is in the
field (same guard already used by Fax_Override_Number on the PVS). Both
pasted and tested by Neil.

===============================================================
PART 2 - FAX DESTINATION BLANK (PVS-1797-JK)
===============================================================
- Billing_Branch was empty. REF-1603 had no Partner_Branch_Link; its
  Partner_Organization held the location NAME ("Suncoast - HIL") and the
  POC contact had no location link, so resolve_branch_id returned "".
- resolve_branch_id updated: after the label checks, match org text to an
  Active Partner_Location_Name, only when exactly one matches.
- POC contact linked to LOC-EMPHIL-1014. REF-1603 and the PVS re-saved;
  fax now resolves.
- Same gap: REF-1593/1596/1599/1611/1612 and PVS-1792-AS / PVS-1795-JK
  re-saved. diag_fax_readiness(30): 0 missing branch, 0 missing link.
- New diag: diag_ref_branch_candidates(string p_refId).

===============================================================
PART 3 - PVS DELIVERY BY EMAIL (INNOVAGE)
===============================================================
- InnoVage gets completed 3008s by email, not fax.
- New field Partner_Billing_Contacts.Partner_PVS_Delivery (radio Fax /
  Email, initial value Fax). InnoVage Orlando/Tampa contacts = Email.
  (A Partners-form field was proposed first and rejected - delivery lives
  with the contact data.)
- New function is_pvs_email_branch(int pBranchId) -> bool.
- Updated to skip email branches: send_fax_digest (unfaxed list only;
  Preliminary list unchanged), diag_fax_readiness (new key
  excluded_email_delivery), diag_missing_pvs_fax (new list email_delivery).
- New diag: diag_pvs_email_branches().
- CREATOR QUIRK HIT AGAIN: if(!a && (b || c)) saved as if(!a && b || c).
  Re-pasted with nested ifs and verified live. Never use parenthesized ||
  sub-groups in Deluge conditions.

===============================================================
PART 4 - PVS FAX COVERAGE
===============================================================
diag_missing_pvs_fax: 19 of 24 locations OK, 2 email delivery. Chapters
Good Shepherd / HPH Hospice / LifePath contacts added.
Still no billing contact: AccentCare - Pasco, Cornerstone - Main,
Direct - Individual (Neil, not blocking).

===============================================================
PART 5 - ZOHO FORMS REFERRALS DROPPED BEFORE CREATOR
===============================================================
Zoho Forms > Patient Referral > All Entries > "Integration - Failed
Entries" held 17 entries (09/02 onward, plus 4 January tests).
- "Invalid column value for Referral_Type": form sent "Imaging Order",
  Creator expects "Imaging Order (only)". Neil renamed the Forms choice
  and reset the Creator connection. RESOLVED.
- "'Facility_Room_Number' has exceeded the maximum character length":
  maxchar 8 on Referrals_Main and Assignments. Neil removed both limits.
  (Referrals_Main2 had no limit; not in use yet.)
- Of 12 real referrals: 6 had been re-entered by hand, 1 (09/29) re-entered
  today, 5 set aside by Neil's call.
- diag_unnotified_referrals: REF-1500 and REF-1579 never ran On Create.

===============================================================
PART 6 - REPO
===============================================================
- v56 .ds saved (versioned + canonical). ds_sync --apply pulled 11
  live-only diag functions and the PVS System Fields Stamp drift.
  Commit 0469185 (not pushed).
- Repo send_fax_digest.dg is ahead of v56 (nested-if fix pasted after).
- context/23_task_list.md updated this checkpoint.
- Session also left a stale .git/index.lock (removed with Neil's delete
  approval). Use git --no-optional-locks for status in the mounted repo.

===============================================================
OPEN (next)
===============================================================
- 3 locations without billing contact (Neil).
- REF-1500 / REF-1579 notification + assignment (decide).
- 5 set-aside referrals (Neil's call).
- Next .ds export to confirm send_fax_digest MATCH.
