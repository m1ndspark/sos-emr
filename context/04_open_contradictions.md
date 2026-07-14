# Open Contradictions (resolve during extraction, do not silently decide)

Items conflict between documents of different vintages. Each must be confirmed
against the live Creator app before any code touches that area. Do not pick a
side silently. The live app is ground truth.

NOTE (June 25, 2026): the app is being REBUILT in a new Creator instance. ID,
stamp, sequencing, and billing design are now decided fresh in
context/07_partner_billing_and_rates.md, not extracted. See that file.

--------------------------------------------------------------------------------
4-A  FORM NAME: Encounter_PatientVisit vs Encounters_Main
--------------------------------------------------------------------------------
- May 8 session log and the June module use Encounter_PatientVisit (PVS), with
  separate Encounter_RadiologyRequest and Encounter_LabRequest forms.
- The April 30 task master is built around a single consolidated Encounters_Main
  that absorbs X-Ray via an Imaging_Order_Section, and shows Encounter_Radiology
  Request as CLOSED April 25 (folded in).
- Action: confirm the live form name and whether radiology/lab are separate forms
  or sections. Rename repo folders to match what is live.

--------------------------------------------------------------------------------
4-B  OBJECT ID FORMAT: v1.2 vs T011  [RESOLVED]
--------------------------------------------------------------------------------
- RESOLVED July 14, 2026: BOTH candidates are dead. Neither the May 7 v1.2 suffix
  format (REF-1001-JSMI-VIT01, PVS-REF1001-JSMI-JK) nor the older T011 format
  (single global counter from 1313, date embedded, REF-MMDDYY-1001-VIT) is live.
  The app was rebuilt after both; ID design is now set fresh in
  context/07_partner_billing_and_rates.md and realized by the live generators.
- LIVE-VERIFIED formats (ground truth = the built generators, not either doc):
    REF: "REF-" + seq, clean sequence from the REF Sequence_Tracker row, base 1001.
         No branch token, no PHI. Source: functions/mint_referral_id.dg (wired into
         Referrals_Main On Success). Examples: REF-1001, REF-1005, REF-1006.
    PVS: minted from PVS's OWN Sequence_Tracker row (it does NOT inherit the parent
         REF's sequence). Referral path = "PVS-" + seq + "-" + Employee_Initials;
         walk-in path = same + "-M". Plus PVS_Referral_ID = "PVS-" + Referral_ID on
         the referral path only (e.g. REF-1005 -> PVS-REF-1005). Source:
         Encounter_PatientVisit/OnSuccess__PVS_Stamp_Generator.dg. Deployed + tested
         live 2026-07-14; PVS row observed incrementing 1001, 1002, 1003.
- Branch is DECOUPLED from ID identity (context/07 late-session reversal): REF/PVS
  carry no partner+branch token; billing branch is a separate Billing_Branch lookup.
  The descriptive PARTNERBRANCH token survives only where it is genuine identity:
  Partner (PAR-ACC-1001) and Location (LOC-ACCJAX-1001).
- NOTE (divergence from context/07's "PVS ID PATHS (LOCKED)"): 07 planned the
  referral-linked PVS to INHERIT the parent REF's PARTNERBRANCH-SEQ. The live build
  instead mints an independent PVS sequence and carries the REF link in the separate
  PVS_Referral_ID field. Live wins (it is the running app); 07's PVS section is
  annotated build-realized to match. See context/03 and context/07 for detail.

--------------------------------------------------------------------------------
4-C  SEQUENCE_TRACKER: per-object counters vs single global counter  [RESOLVED]
--------------------------------------------------------------------------------
- RESOLVED June 25, 2026: per-object counters. The live tracker shows one row
  per object, each with its own Object_Sequence at 1001. The single-global-counter
  model (Standing Rules section 11 / T003) is dead.
- See context/07_partner_billing_and_rates.md for the full sequencing redesign
  (sequenced vs inheriting objects, PVS inherits, MPR path, starting numbers).

--------------------------------------------------------------------------------
4-D  RADIOLOGY / LAB HANDLING
--------------------------------------------------------------------------------
- Task master: Encounter_RadiologyRequest CLOSED April 25, X-Ray handled inside
  Encounters_Main via Imaging_Order_Section.
- June module: Encounter_RadiologyRequest and Encounter_LabRequest still listed
  as locked forms, with a verify-flag.
- Tied to open Josh clarifications (separate referral vs under-visit referral for
  X-Ray, billing when ordered during a visit, ordering without seeing patient).
- Action: confirm current truth before building anything radiology or lab related.
