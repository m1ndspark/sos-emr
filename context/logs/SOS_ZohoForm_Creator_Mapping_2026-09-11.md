# Zoho Forms to Zoho Creator Integration Mapping

Form: Patient Referral (forms.zoho.com/SOSReferralForm/form/PatientReferralsHCO)
Creator app: sos-referrals-app, form Referrals_Main
Captured: 2026-09-11, from the Field Mapping screen immediately before the
integration was removed and rebuilt.

Left column is the Creator field. Right column is the Zoho Forms question as
the mapping screen displayed it. Truncated labels are marked with an ellipsis
exactly as shown. The mapping screen reads Creator field on the left, Zoho
Forms question on the right.

| # | Creator field | Zoho Forms question |
|---|---|---|
| 1 | Referral Source | Referral Source |
| 2 | Service | Service Requested |
| 3 | Patient First Name | Patient First Name |
| 4 | Patient Last Name | Patient Last Name |
| 5 | Patient DOB | Patient DOB |
| 6 | Patient Gender | Biological Sex |
| 7 | Patient Hospice ID | Hospice ID |
| 8 | Patient MBI | Patient MBI |
| 9 | Patient SSN | Patient SSN |
| 10 | Patient Phone | Patient Phone |
| 11 | Is there an additional contact? | Is there an additiona... |
| 12 | AC First Name | AC First Name |
| 13 | AC Last Name | AC Last Name |
| 14 | AC Phone | AC Phone |
| 15 | AC Relationship to Patient | Relation to Patient |
| 16 | Patient Location | Where is the patient... |
| 17 | Facility Name | Facility Name |
| 18 | Facility Phone | Facility Phone |
| 19 | Facility Room Number | Facility Room # |
| 20 | Patient Address | Patient Address |
| 21 | Reason for Referral | What is the reason f... |
| 22 | Partner ICD Codes | ICD-10 Codes |
| 23 | Will an X-Ray be needed for this r... | Will this referral requ... |
| 24 | Does the patient take anticoagula... | Does the patient us... |
| 25 | List Patient Anticoagulants | List anticoagulant m... |
| 26 | Does the patient have Advanced ... | Does the patient hav... |
| 27 | Advanced Directives Details | Advanced Directives... |
| 28 | Additional Information | Provide any addition... |
| 29 | Imaging Test(s) to be Ordered | List Imaging test(s) t... |
| 30 | Body Part / Affected Area | Body Part / Affected... |
| 31 | Reason for Imaging Order(s) | Reason for Imaging ... |
| 32 | Partner POC First Name | Referral POC First N... |
| 33 | Partner POC Last Name | Referral POC Last N... |
| 34 | Partner POC Title | Referral POC Title |
| 35 | Partner POC Team | Partner Clinical Team |
| 36 | Partner POC Phone | Partner POC Phone |
| 37 | Partner POC Email | Partner POC Email |
| 38 | 3008 File URLs | 3008 Files Upload - ... |
| 39 | General Files URLs | General Files Upload... |
| 40 | Imaging Orders URLs | Upload Imaging Ord... |
| 41 | Partner Location Label | Referral Partner Loo... |
| 42 | Form Token | Form Token |

Total mappings: 42.

## Load bearing mappings, do not lose these

- Rows 38, 39 and 40 are the WorkDrive URL fields that feed file intake. They
  must map to the Creator Multi Line fields Files_3008_URLs,
  General_Files_URLs and Imaging_Orders_URLs, never to a Creator file upload
  field. Creator file fields in Multiple Upload mode are not offered for
  mapping at all.
- Row 42 Form Token populates Referrals_Main.Form_Token. Every downstream
  check for form origin depends on it, including the rule that Referral Date
  is only ever derived for form created records.
- Row 41 carries the partner location. It must land in the TEXT field
  Partner_Location_Label so process_new_referral can resolve organization,
  branch, Partner_ID and billing branch from it.

## Row 41 resolved

Creator "Partner Location Label" now maps to the Zoho Forms question labeled
"Branch/Location", the flat 22 option Dropdown that replaced the old group
list. Confirmed present on the rebuilt integration before Integrate was
clicked.

The old pre-rebuild capture showed this row pointing at a question displayed
as "Referral Partner Loo...". That question is gone.

## Rebuild sequence

1. Screenshot every mapping before removing the integration. Done.
2. Delete the old Partner Locations field and add a Dropdown with the 22
   approved labels. Done.
3. Remove the integration and rebuild it from this table. Done, 42 rows.
4. Confirm rows 38 to 42 explicitly. Done.
5. Submit one test referral through the live form. Done.
6. Run sos_referral_health with REPORT, ALL, 5. Done.

## Rebuild result, 2026-09-11

REF-1468, TEST TEST, AccentCare / Miami. Partner and branch resolved from
Partner_Location_Label, POC email captured, DOB captured, assignment created,
Referral_ID minted in the REF-NNNN format. The only health flag returned was
TESTREC, which is expected for a test row. The integration is confirmed
working end to end.

Rows removed from the mapping deliberately and left unmapped in Creator:
Patient DOB (system), Data Issues, Referral ID, Referral Date, Referral Date
(Don't Use), Partner Organization, Partner Branch/Location.

## Approved 22 location labels as of 2026-09-11

AccentCare - Broward
AccentCare - Hernando
AccentCare - Hillsborough
AccentCare - Miami
AccentCare - Pasco
AccentCare - Pinellas
Chapters - Good Shepherd
Chapters - HPH Hospice
Chapters - LifePath
Cornerstone - Main
Empath - Marion
Empath - Polk
Empath - Suncoast - HIL
Empath - Suncoast - PIN
Empath - Tidewell
Empath - Trustbridge
InnoVage - Orlando
InnoVage - Tampa
VITAS - Citrus
VITAS - Lee/Glades
VITAS - Sumter
VITAS - Villages

END
