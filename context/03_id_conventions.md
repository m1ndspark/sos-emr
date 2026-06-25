# Object ID Conventions (EMR)

Source: SOS EMR Object ID Pattern Master Reference v1.2 (May 7, 2026). This is
the authoritative format. The older T011 format is deprecated (see contradiction 4-B).

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

PVS STAMP PATHS (two, from May 8 log)
  Path A (Has_Referral_ID = Yes): PVS-REF[seq]-[patient]-[emp]
  Path B (Has_Referral_ID = No):  PVS-MPR[seq]-[patient]-[emp], also stamps
                                  PVS_Referral_ID with the same value

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
