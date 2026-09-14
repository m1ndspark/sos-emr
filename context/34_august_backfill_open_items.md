# August 2026 PVS and Referral Backfill, open items

Raised 2026-09-14 (Session 46) while reconciling the August Cognito exports
against Creator. Nothing here is written yet. Source file:
SOS_August_Partner_Source_Backfill_2026-09-14.xlsx.

--------------------------------------------------------------------------------
## 1. Partner source text is free text in Cognito and will not auto-resolve
--------------------------------------------------------------------------------
61 distinct Referral Source values across 164 August rows, 6 more blank.
The field had no validation, so the same branch appears as "Tidewell",
"Tidewell Hospice", "TIDEWELL", "Tidwell", "Tidewell/Empath" and
"Tidewell Hospice Venice".

Resolution against the 22 approved location labels:
  78 rows resolve to an exact approved label
  86 rows give the organization only, with no branch stated
   6 rows are blank in Cognito

The 86 break down as: Empath with no branch, AccentCare with no branch, and one
VITAS. "AccentCare Tampa" is not a branch label. Suncoast never says HIL or PIN
unless the raw text spells it out, so every bare "Suncoast" is undecided.

Two raw values are facilities rather than partners and were resolved on that
basis: "North Pinellas Care Center" and "Suncoast Hospice Mid-Pinellas Care
Center" both point at Empath - Suncoast - PIN.

NEXT: Neil assigns a branch to the 86 organization-only rows, or rules that
organization alone is enough for MPU and the branch stays blank on those.

--------------------------------------------------------------------------------
## 2. Two partner assignments made this session are wrong
--------------------------------------------------------------------------------
Both were assigned to the Direct placeholder partner before the clinical notes
were read.

REF-1357, Ricilia Dorlizier, 08/11. The note is a completed paracentesis
performed by Ann Smith APRN and Cognito marks it Partner Referral. This is
billable partner work, not a direct inquiry. The referring organization is not
recorded anywhere in Cognito.

REF-1237, Norma Zotolor, 08/21. The note names the partner: "Patient was with
Gentiva Hospice and they placed the order however the patient went to the
hospital." Gentiva is not among the 22 approved locations and has no Partners
record.

The other four Direct assignments are confirmed correct by their notes:
Oliver Wittig "Patient contacted the wrong provider", Liam Wittig "wrong
company", Zenia Krase "Private patient and request The patients family
cancelled", Elisabeta Bega "unable to reach the patient".

--------------------------------------------------------------------------------
## 3. Billing items with no current mechanism
--------------------------------------------------------------------------------
Bennie Benjamin, 08/11, AccentCare, REF-080626-1557. Recorded as Low
Complexity. The note reads: "Visit/procedure not cancelled by staff. Phone call
to Mayra Marrero, left voicemail. She called back stating procedure was no
longer needed due to having another physician out there. Bill for travel. 3hr
each way." The provider drove 1.5 hours each way and saw no patient. Neil's
position is that SOS does not absorb this and the provider expects to be paid.
There is no travel charge field and no travel rate in the Partner Rates table.

Ronaldo Martinez, 08/22, Empath, REF-082226-1694. The note reads "False
Patient". Currently No Charge. It should be excluded from referral and visit
counts entirely, not merely left unbilled.

--------------------------------------------------------------------------------
## 4. Records that cannot be completed from any source
--------------------------------------------------------------------------------
Three PVS carry no employee link, and their PVS IDs end in a bare dash as a
result. Cognito records no provider on any of them and only one names a
provider inside the note.
  PVS-1413- Joseph Wasser 08/14, note reads "Provider: Ann Marie Smith, APRN"
  PVS-1382- Cherlyn Gould 08/20, no provider anywhere
  PVS-1332- Abraham Jacobs 08/28, no provider and no acuity anywhere

Type of Procedure(s) is blank on 148 of 168 August PVS rows. Cognito carries a
Type of Procedure value on only 15 rows in the whole month, and none of them
align with a Creator blank. The procedure is described in the clinical note
text but extracting it is interpretation, not data.

--------------------------------------------------------------------------------
## 5. What Cognito can actually fill
--------------------------------------------------------------------------------
Measured against every Cognito column, not a sample. Where Creator is blank,
Cognito is blank too for POC team, referred by, partner, provider, procedure
type and facility name. The only genuine imports are 2 patient hospice IDs.

Patient Full Address (blank on all 168) and Employee Full Name (blank on 163)
are better derived inside Creator from fields it already holds than imported.
backfill_pvs_repair does both.

--------------------------------------------------------------------------------
## 6. Duplicates and test rows confirmed by note text
--------------------------------------------------------------------------------
Linda Franco 08/31 is one cancellation entered twice, notes "deceased" and
"patient passed away".

Patricia Eckhardt has two Cognito rows on one referral, a Madison Smith
preliminary and a Joshua Kolanko final. Creator holds only the final, which is
correct. The visit was a supervised blood draw.

TEST TEST 08/21, PVS-1367-JK, note "Test Referral". Delete.

PVS-1307-JK-M 08/31 has no patient name, no service and no referral link. It
does not correspond to any Cognito row.

--------------------------------------------------------------------------------
## 7. Method note
--------------------------------------------------------------------------------
The first pass over the Cognito PVS export counted populated columns and
concluded the file had nothing to contribute. That was wrong. The partner,
referring contact, clinical team and provider identity are carried in free text
and inside the clinical notes, and reading them produced every finding in
sections 2, 3 and 6. Column counts are not a substitute for reading the file.

END
