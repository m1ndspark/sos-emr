# SOS EMR - HANDOFF

Purpose: the smallest current-state file. Open flags + verified names only.
Full detail in _INDEX.md and context/. Update at each "document everywhere" / EOD.
Last updated: 2026-07-22.

--------------------------------------------------------------------------------
BIG NEWS THIS SESSION: full app export exists
--------------------------------------------------------------------------------
Settings > Application IDE > Export produces a .ds file = the ENTIRE app definition
(forms, fields, AND every workflow/function Deluge), definition-only (no record data,
no PHI - verified). This is authoritative LIVE truth and ends the paste-from-live relay.
- IMPORT of a .ds CREATES A NEW APP (clone); it does NOT patch the live app in place.
  So .ds is a MIRROR + dev-clone tool, not a production deploy button. Authoring new
  code is still applied by hand in Creator.
- tools/ds_sync.py reconciles a .ds against the repo .dg files: dry-run report
  (MATCH/DRIFT/NEW/EMPTY/AMBIGUOUS), --apply writes DRIFT+NEW only. Never writes EMPTY
  or AMBIGUOUS (incl. target collisions), so a mis-map can't clobber. Compare is
  whitespace-insensitive (Deluge nesting is braces, not indent).
- DRIFT DIRECTION IS NOT ALWAYS live->repo. Decide per item: most old generators are
  repo-stale (pull live), but recently-edited ones can be repo-AHEAD (push to live).

--------------------------------------------------------------------------------
OPEN FLAGS (next up)
--------------------------------------------------------------------------------
- Referral_Link Pre-Fill: repo has `hide System_Fields_Section;` in the if(v_Found)
  block; LIVE does not (repo-ahead). Decide: add the line live (plain hide, safe) OR
  drop it from repo to match. Likely harmless either way (Default_Hide_On_Load hides
  that section on load), but repo+live should agree.
- Legacy workflow "Patient_Fields_Editability_Toggle" (PVS, On User Input Has_Referral_ID)
  is still LIVE + ENABLED. It un-hides PVS_Referral_ID + double-handles patient locking.
  DELETE it live -> also clears one ds_sync AMBIGUOUS collision.
- Stray "Partner_Rate_Stamp" workflow sits on the PARTNERS form (belongs on Partner_Rates).
  Investigate why; likely misplaced/leftover.
- FLAG 3 RESOLVED 2026-07-22. Build Patient Full Address was missing the `input.` prefix
  on its final write (`Patient_Full_Address = v_addr.trim();`) and on all five
  trim-checks (the null half of each condition had it, the trim half did not), so
  Patient_Full_Address never populated. Fixed live and verified by Neil on BOTH
  Encounter_PatientVisit and the Referrals_Main sibling
  (OnUserInput__Patient_Address__Build_Full_Address.dg). Both repo copies now carry the
  corrected body. CARRY: the fix post-dates the July 22 .ds export, so ds_sync shows
  both as DRIFT (repo AHEAD, do NOT --apply over them) until a fresh .ds is pulled.
- Employee Term Date visibility: TRIGGER DISAGREEMENT. Repo file is named
  OnLoadAndOnInput__Employee_Term_Date_Visibility.dg, but the July 22 live .ds reports the
  workflow as On User Input only. Do not assume the repo file matches live. Reconcile
  against Creator and rename or re-mirror accordingly.
- Drift reconciliation (ds_sync), July 22 export: MATCH 23, DRIFT 45, NEW 12,
  AMBIGUOUS 5, EMPTY 1. DRIFT is not yet pulled; confirm direction per item before
  --apply, since some repo files are repo-AHEAD rather than repo-stale. Of the 12 NEW,
  3 were duplicates of existing repo files under non-conforming names and were dropped
  (existing files kept): ShowHide_Facility_block.dg,
  OnUserInput__Assignment_Pull_From_Referral.dg,
  OnLoadAndOnInput__Employee_Term_Date_Visibility.dg. Those three repo names still do not
  match the OnEvent__Field__Name.dg convention; renaming them is a separate cleanup.
- ds_sync AMBIGUOUS, 1 of the 5 is a different failure than the rest:
  Employees "OnSuccess Portal_Access_By_Status" resolved to NO repo file at all, rather
  than colliding with one. The other 4 are the usual 25-char name-truncation collisions.
- Phone/fax standard (AAA-MMM-LLLL) rollout to remaining 6 forms (carry).
- Annual ICD-10 refresh function (early Oct; designed, not built).
- Retire empty Encounter_RadiologyRequest; delete DEBUG-joshua.kolanko test PVS record.
- Optional: chip-style HTML display of partner + provider ICD codes.

--------------------------------------------------------------------------------
VERIFIED NAMES / FACTS (live-confirmed)
--------------------------------------------------------------------------------
PVS ID (Encounter_PatientVisit, "PVS ID Stamp Generator", On Success):
  referral = PVS-<seq>-<init> (PVS-1003-JK); walk-in = PVS-<seq>-<init>-M (PVS-1002-JK-M).
  PVS_Referral_ID = PVS-<Referral_ID> (referral path only; blank on walk-in).
  ID logic is NESTED ifs (outer Has_Referral_ID=="Yes" && Referral_ID present; inner
  PVS_Referral_ID null/empty). CREATOR QUIRK: if(A && B && (C||D)) with a parenthesized
  ||-subgroup SILENTLY REVERTS ON SAVE - never use it; split into nested ifs. Always
  reopen a saved workflow to confirm it persisted, and test the EDIT/re-submit path.
  Mints from shared "PVS" Sequence_Tracker row. No-duplicate on PVS_ID = ON.

Partner_Referral_Contacts (soft partner identity, email-keyed, no PHI):
  Partner_POC_Email (No-dup, key), Partner_POC_First_Name/Last_Name/Title/Phone/Team,
  Partner_Organization, Partner_Branch. NOTE: keep passive-store fields Single Line - a
  non-choice value into a DROPDOWN field aborts the WHOLE upsert (all-or-nothing).

Return-visit prefill (live): Zoho Forms Dynamic-Prefill-Webhook (Email field) -> Creator
  Custom API "Get Partner Referral Contact" (GET, OAuth2, Admin-only, Argument Type
  Key-and-Value param pPocEmail, Response STANDARD) -> functions/get_partner_referral_contact.dg.
  Endpoint www.zohoapis.com/creator/custom/sosmmc/Get_Partner_Referral_Contact.
  Connection sos_creator_connection (customapi.EXECUTE + report.READ). Custom API STANDARD
  response WRAPS the Map under "result" -> Forms mapping paths are /result/<Field>.

Partner ICD on PVS (live): Partner_ICD_Codes (Single Line) pulled from
  Referrals_Main.Partner_ICD_Codes on referral match in Referral Link Pre-Fill, locked.
  Provider side: Provider_ICD10_Codes_Link (Multi Select lookup -> ICD10_Codes),
  Provider_ICD_Print roll-up. ICD10_Codes = 74,879 CMS FY2027 rows.

log_change: live body is genuinely EMPTY (Creator logs errors only, not every change).

Repo: /Users/neilheird/Claude/GitHub/sos-emr  (remote m1ndspark/sos-emr, branch main)
