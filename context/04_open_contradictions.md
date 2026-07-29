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

--------------------------------------------------------------------------------
4-E  ORPHANS AND SCHEMA CONVENTION FROM THE 2026-07-29 DRIFT SYNC
--------------------------------------------------------------------------------
Surfaced while syncing SOS_Referrals_App_2026-07-29.ds. Do not silently decide.

- functions/fn_resolveUserIdentity.dg is present in the repo but ABSENT from the
  .ds (0 references in the export). Either it was removed from Creator or never
  deployed. Standing rules still centralize identity resolution in this function
  (context/01). File left in place, not deleted, pending Neil's decision on
  whether it is still live.
- functions/get_partner_referral_contact.dg: the 7/29 check-in listed this as
  orphaned too, but it IS present in the .ds and synced as live. NOT orphaned.
  Correction recorded here so the check-in note is not acted on.
- Orphaned schema files (present in schema/, absent from the .ds forms):
  Encounter_RadiologyRequest.md (already tombstoned by the schema monitor on
  origin), X_Ray_Orders.md, X_Ray_Request_Form.md. Left in place, flagged.
  Tied to the still-open 4-A / 4-D radiology/lab question.
- Schema regeneration conflict: the 7/29 check-in asked to regenerate schema/
  from the .ds and to add schema/Schema_Snapshot.md. CLAUDE.md holds schema/ as
  auto-generated output from the live Meta API via run_schema_monitor, never
  hand-edited. Today's monitor run (7/29 06:01) already refreshed per-form schema
  and it reflects the 7/29 field changes (Partner_Location_Label,
  Hold_From_Invoicing, Invoice_Link added; Primary_Diagnosis and Multi_Line
  removed). Schema was therefore left to the monitor and NOT hand-written.
  Schema_Snapshot.md is not a monitor artifact and was not created. Confirm
  whether a combined snapshot is wanted and, if so, that the monitor should emit
  it rather than it being hand-maintained.
- Standing-rule note: context/01 still says show/hide are valid only in On User
  Input actions, but live workflows (e.g. Assignments OnLoad Show_Hide_Facility_
  Name_P) and context/05 / context/19 use show/hide/disable in On Load. Live
  behavior is On Load. context/01 is stale on this point.
- KNOWN DIVERGENCE, functions/run_schema_monitor.dg: the live 7/29 export added 5
  em dashes inside display-string literals (schema-monitor alert email HTML and
  the "REMOVED FROM CREATOR" tombstone text). context/08 and the pre-commit hook
  forbid em dashes anywhere, so the committed .dg has those 5 em dashes replaced
  with hyphens. This is display text only, no logic change, but the repo mirror
  now differs from live for that one file, and every ds_sync will re-flag it as
  DRIFT until the em dashes are removed in Creator and re-exported. Action for
  Neil: de-dash those strings in the live run_schema_monitor function, then
  re-export so repo and live match and the hook stops needing this patch.
