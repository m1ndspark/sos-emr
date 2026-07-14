# Object ID Conventions (EMR)

STALE NOTICE (June 26, 2026): the ID LAYOUT in this file is SUPERSEDED by
context/07_partner_billing_and_rates.md. The canonical layout is now the FUSED
token PREFIX-PARTNERBRANCH-SEQ (REF-ACCHIL-1001), not the v1.2 trailing-suffix
format below (REF-1001-VIT01). Also superseded: the no-referral path is now an M
suffix (PVS-ACCHIL-1001M), the MPR token is retired; partner+branch is FUSED (no
dash); Branch_Code is a descriptive 3-char code on the Location (HIL), not a
2-digit Partner_Branch_ID (01); several objects (Partner_Rates, Billing_Contacts,
Partner_Portal_Users) now use the native stamp only and have NO custom ID. The
charge-type codes and the deprecated-formats list below are still valid. Read
file 07 first for anything ID-related.

STALE NOTICE UPDATE (July 14, 2026): the June 26 notice above is itself now partly
stale for REF and PVS. Two corrections from the later work:
1. BRANCH IS DECOUPLED from REF/PVS identity (context/07 late-session reversal).
   REF and PVS carry NO partner+branch token. The fused REF-ACCHIL-1001 shown above
   applies to Partner (PAR-ACC-1001) and Location (LOC-ACCJAX-1001) ONLY, where the
   token is genuine identity. Billing branch is a separate Billing_Branch lookup.
2. LIVE-VERIFIED REF/PVS formats (ground truth = the built generators):
     REF = "REF-" + seq (clean sequence, base 1001, own REF tracker row, no PHI).
           Source: functions/mint_referral_id.dg. e.g. REF-1005, REF-1006.
     PVS = minted from PVS's OWN tracker row (does NOT inherit the parent REF seq).
           Referral path "PVS-" + seq + "-" + Employee_Initials; walk-in adds "-M".
           Plus PVS_Referral_ID = "PVS-" + Referral_ID on the referral path only
           (REF-1005 -> PVS-REF-1005). Source:
           Encounter_PatientVisit/OnSuccess__PVS_Stamp_Generator.dg (live 2026-07-14).
The "PVS STAMP PATHS" and "PVS and ADD derive seq from the parent REF" lines below
are SUPERSEDED by this; see contradiction 4-B (RESOLVED) and the .dg for the live
truth.

Source: SOS EMR Object ID Pattern Master Reference v1.2 (May 7, 2026). Layout now
superseded by file 07 (see notice above). The older T011 format is deprecated (see contradiction 4-B).

UNIVERSAL PATTERN
  [XXX]-[seq]-[suffix]
  XXX  = 3-letter object prefix
  seq  = object counter starting at 1001
  suffix = varies by object (see below)
  Date is NOT embedded. PVS and ADD derive seq from the parent REF, no own counter.

SUFFIX RULES
- Partner-linked: [Partner_Code][Partner_Branch_ID], e.g. VIT01, ACC03
- Patient initials: first initial + first 3 of last, e.g. JSMI for John Smith
- Employee initials: from Employee_Initials field. Duplicates JK, JK2, JK3
- Admin initials: from Zoho login at runtime. Applies to ADR only
- Charge type code: 4-char code. Applies to CHG only
- Private Pay: SP placeholder, e.g. REF-1001-JSMI-SP
- Branch_ID: 01 = primary partner, 02+ = locations, single-location = 01 always

OBJECT ID REFERENCE
  Referral              REF  REF-seq-[patient]-[partner+branch]   REF-1001-JSMI-VIT01
  Encounter / PVS       PVS  PVS-REF[seq]-[patient]-[employee]    PVS-REF1001-JSMI-JK
  Addendum              ADD  ADD-REF[seq]-[patient]-[emp##]       ADD-REF1001-JSMI-JK01
  Partner               PAR  PAR-seq-[partner+branch]             PAR-1001-VIT01
  Partner_Location      LOC  LOC-seq-[partner+branch]             LOC-1001-VIT02
  Employee              EMP  EMP-seq-[employee initials]          EMP-1001-JK
  Partner_Rates         RAT  RAT-seq-[partner+branch]             RAT-1001-VIT01
  Partner_Billing_Contacts PBC PBC-seq-[partner+branch]           PBC-1001-VIT01
  Partner_Portal_Users  PPU  PPU-seq-[partner+branch]             PPU-1001-VIT01
  Charge_Types          CHG  CHG-seq-[charge type code]           CHG-1001-LOWC
  Invoice               INV  INV-seq-[partner+branch]             INV-1001-VIT01
  Assignment            ASN  ASN-seq-[assigned provider]          ASN-1001-JK
  PVS_Admin_Review      ADR  ADR-seq-[admin initials]             ADR-1001-JK

PVS STAMP PATHS [SUPERSEDED -- see STALE NOTICE UPDATE above; live truth below]
  DEAD (May 8 log): Path A PVS-REF[seq]-[patient]-[emp]; Path B PVS-MPR[seq]-
    [patient]-[emp]. Patient token, REF/MPR infix, and the "stamp PVS_Referral_ID
    on the no-referral path" rule are all dead.
  LIVE (OnSuccess__PVS_Stamp_Generator.dg, verified 2026-07-14), own PVS tracker row:
    Referral (Has_Referral_ID = Yes): PVS-[seq]-[emp]   e.g. PVS-1001-JK
    Walk-in  (else):                  PVS-[seq]-[emp]-M  e.g. PVS-1002-JK-M
    PVS_Referral_ID (REFERRAL path only): "PVS-" + Referral_ID  e.g. PVS-REF-1005

CHARGE TYPE CODES (4-char)
  LOWC Low Complexity      MODC Moderate Complexity   HIGH High Complexity
  HAHO Hospital at Home    TELE Telemedicine          CCOR Care Coordination
  CONS General Consultation AFTH After Hours          STAT Super Stat
  3008 PACE 3008 Assessment

SEQUENCE TRACKER (per v1.2)
  Each object has its own counter starting at 1001. Locking required on REF only;
  PVS and ADD derive from REF; other objects are admin-only, no locking needed.
  NOTE: this conflicts with Standing Rules section 11 and T003, which call for a
  single global counter and locking on all generators. See contradiction 4-C.

DEPRECATED (DEAD, do not use)
  REF-MMDDYY-SEQ, ENC-[seq], E[seq]-[initials], R[seq]-[initials]-[code],
  P[seq]-[code], EM[seq]-[initials], BIL prefix (replaced by PBC).

NOTE: charge type codes and the locked partner RATE VALUES (Empath High 575 /
Moderate 373, AccentCare High 545 / Moderate 343, InnovAge 3008 175 flat) are
the authoritative numbers. Rate values and AR reconciliation belong to the SOS
Finance lane, not this repo. This repo builds the Charge_Types and Partner_Rates
forms and workflows; it does not own the numbers.
