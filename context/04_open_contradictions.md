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
4-B  OBJECT ID FORMAT: v1.2 vs T011
--------------------------------------------------------------------------------
- Authoritative: May 7 v1.2 reference. Per-object counters from 1001, no date
  embedded, e.g. REF-1001-JSMI-VIT01, PVS-REF1001-JSMI-JK.
- Deprecated: the older T011 format (single global counter from 1313, date
  embedded, e.g. REF-MMDDYY-1001-VIT, E1002-JK). The April task master still shows
  T011 as confirmed; that task description is stale.
- Action: confirm live stamp generators emit the v1.2 format.

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
