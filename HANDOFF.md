# SOS EMR - HANDOFF

Purpose: the smallest current-state file. Open flags + verified names only.
Full detail lives in _INDEX.md and context/. Update at each "document everywhere" / EOD.
Last updated: 2026-07-14 (Session 16).

--------------------------------------------------------------------------------
OPEN FLAGS (load-bearing / next up)
--------------------------------------------------------------------------------
- Partner ICD field on the PVS: pull/lock from Referrals_Main on referral match.
  Drafted Session 15, "didn't work" on test. NEXT.
- Prefill email match is exact (Creator ==). Lowercase-normalize on upsert (write)
  AND get_partner_referral_contact (read) IF live emails prove inconsistent. Not done yet.
- Extract "Entry Type Section Visibility" live code -> its .dg; fix stale _INDEX row.
- Phone/fax standard (AAA-MMM-LLLL) rollout to remaining 6 forms.
- Annual ICD-10 refresh function (early October; delta upsert; designed, not built).
- Cleanup: delete 2 disabled legacy PVS workflows (Referral Fields Default Hide,
  Patient Fields Editability Toggle); retire empty Encounter_RadiologyRequest.

--------------------------------------------------------------------------------
VERIFIED NAMES / FACTS (recent, live-confirmed)
--------------------------------------------------------------------------------
PVS ID (Encounter_PatientVisit, PVS ID Stamp Generator, On Success):
  referral  = PVS-<seq>-<init>        (e.g. PVS-1003-JK)
  walk-in   = PVS-<seq>-<init>-M      (e.g. PVS-1002-JK-M)
  PVS_Referral_ID = PVS-REF-<Referral_ID>  (referral path only; blank on walk-in)
  Mints from shared "PVS" Sequence_Tracker row. No-duplicate on PVS_ID = ON. No patient initials (PHI).

Partner_Referral_Contacts (soft partner identity, keyed on email; no PHI):
  Partner_POC_Email (No-duplicate ON, the key), Partner_POC_First_Name,
  Partner_POC_Last_Name, Partner_POC_Title, Partner_POC_Phone, Partner_POC_Team,
  Partner_Organization, Partner_Branch.

Return-visit prefill (verified live):
  Zoho Forms Dynamic-Prefill-Webhook -> Creator Custom API "Get Partner Referral Contact"
  (GET, OAuth2, Admin-only, Argument Type Key-and-Value, param pPocEmail, Response Standard)
  -> functions/get_partner_referral_contact.dg.
  Endpoint: www.zohoapis.com/creator/custom/sosmmc/Get_Partner_Referral_Contact
  Connection: sos_creator_connection (customapi.EXECUTE + report.READ).
  RESPONSE WRAPS the Map under "result" -> Forms mapping paths are /result/<Field>.

ICD-10 (PVS provider side, verified live):
  Reference form ICD10_Codes (74,879 CMS FY2027 rows). Key fields: ICD_Code (No-dup),
  ICD_Description, ICD_Display (lookup display), Status, Source_FY.
  PVS: Provider_ICD10_Codes_Link (Lookup, Multi Select) -> Provider_ICD_Print (code-only roll-up).
  Partner ICD side: Partner_ICD_Codes free-text on Referrals_Main (pull to PVS still open).

Repo: /Users/neilheird/Claude/GitHub/sos-emr  (remote m1ndspark/sos-emr, branch main)
