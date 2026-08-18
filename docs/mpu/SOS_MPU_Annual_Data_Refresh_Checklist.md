SOS MPU - ANNUAL DATA REFRESH CHECKLIST
Everything the cost savings model depends on, where it comes from, and when
it changes. Hand this to any session and it can rebuild the model from
scratch.

Last verified: 2026-08-15, for CY2026 / FY2026 rates.

=====================================================================
THE SHORT VERSION
=====================================================================
Six files. Two calendars. About twenty minutes of downloading, once a year.

  NOVEMBER   - CMS publishes the OPPS final rule for the next calendar
               year. Pull items 1, 2 and 3 below.
  AUGUST     - CMS publishes the IPPS final rule for the next fiscal
               year. Pull items 4 and 5.
  ANYTIME    - Items 6 and 7 change on their own schedules.

Nothing else in the model has to be touched. Rates change once a year;
the method does not.

=====================================================================
1. OPPS ADDENDA - THE MOST IMPORTANT FILE
=====================================================================
WHAT     Addendum D1 (payment status indicator definitions) and
         Addendum J (the Comprehensive APC payment policy exclusions).
WHY      D1 tells you which procedures are J1 comprehensive APCs, which
         are T or Q1, and therefore how an episode gets paid. Addendum J
         is the definitive list of what does NOT get packaged. Together
         these two files decide the entire structure of the model. Get
         them first.
WHERE    cms.gov, search "CMS-####-FC hospital outpatient regulations
         notices". On the rule page, under Related Links, the entry
         named "20XX NFRM OPPS Addenda".
FILE     20XX_nfrm_addenda.MM.DD.YYYY.zip
CHANGES  Annually, effective January 1.
WATCH    The exclusion list grows. CY2026 added cell and gene therapies
         and non-opioid products. If a new exclusion touches anything we
         model, the packaging assumption changes.

=====================================================================
2. OPPS ADDENDUM B - FACILITY PAYMENT RATES
=====================================================================
WHAT     Payment rate, APC assignment and status indicator for every
         HCPCS code.
WHY      Supplies the outpatient facility payment for each procedure.
WHERE    Same rule page. Take the JULY WEB UPDATE, not the final-rule
         version - the July file supersedes it. For CY2026 the final
         rule said 49083 paid $937.33; the July update said $926.63.
FILE     20XX_july_web_addendum_b.MM.DD.YY.zip
CHANGES  Annually, then quarterly web updates. Use the most recent.
CODES WE NEED
         49083 paracentesis with imaging     - verify still J1
         32555 thoracentesis with imaging    - status T, NOT 32557
         51702 catheter insertion            - status Q1
         43762 G-tube/PEG replacement        - status T
         99285 / 99284 / 99283 ED visits     - status J2
WATCH    32557 is pleural DRAINAGE by indwelling catheter, a chest tube.
         It is not thoracentesis. We used it by mistake through July 2026.

=====================================================================
3. PHYSICIAN FEE SCHEDULE RELATIVE VALUE FILE
=====================================================================
WHAT     RVU components, PC/TC indicator, GPCIs, conversion factor.
WHY      Physician fees are the only line paid outside the facility
         payment. Computed, not looked up.
WHERE    cms.gov, search "PFS Relative Value Files". Take the release for
         the coming year, file named RVU__A or later revision.
FILE     rvu##ar_#.zip
INSIDE   PPRRVU####_Jan_nonQPP.csv   - RVUs and PC/TC indicator
         GPCI####.csv                - geographic indices by locality
         The conversion factor sits in the FACTOR column of PPRRVU.
CHANGES  Annually, with quarterly revisions.
CY2026   Conversion factor 33.4009 non-QP, 33.57 QP. Use non-QP.
         Rest of Florida is locality 99: work 1.000, PE 0.956, MP 1.503.
WATCH    PC/TC indicator 0 means modifier -26 does not apply. 49083 is
         indicator 0 - we got this wrong once.

=====================================================================
4. IPPS TABLE 5 - MS-DRG WEIGHTS
=====================================================================
WHAT     Every MS-DRG with its relative weight and geometric mean length
         of stay.
WHY      Prices the admitted pathway. Half the blended estimate.
WHERE    cms.gov "FY 20XX IPPS Final Rule Home Page", under FY 20XX Final
         Rule Tables, the entry "Table 5 (ZIP)".
FILE     cms####ftable5.zip
CHANGES  Annually, effective October 1.
DRGS WE USE
         393  other digestive system diagnoses with MCC   - paracentesis
                                                            and G-tube
         186  pleural effusion with MCC                   - thoracentesis
         695  kidney and urinary tract signs and symptoms with MCC
                                                          - catheter
WATCH    Always the WITH MCC tier. A hospice patient carries a major
         complication by definition of being on hospice.

=====================================================================
5. IPPS TABLES 1A-1E AND TABLE 3
=====================================================================
WHAT     1A-1E: national standardized amounts and the capital rate.
         Table 3: wage index by CBSA.
WHY      Converts a DRG weight into dollars, and adjusts both inpatient
         and outpatient payments for geography.
WHERE    Same IPPS final rule page. Two separate downloads:
         "Table 1A-1E (ZIP)" and
         "FY 20XX Tables 2, 3 and 4A and 4B (Wage Index Tables)(Final
         Rule) (ZIP)".
FILE     cms####ftables1a1e.zip and cms####ftables234a4b_0.zip
CHANGES  Annually, effective October 1.
FY2026   Operating labor $4,456.72, nonlabor $2,295.89 (quality reporting
         and meaningful EHR user, wage index above 1). Capital $524.15.
         Florida wage index 1.0369 for EVERY CBSA, because the state
         rural floor overrides them all. Florida GAF 1.0251.
WATCH    Check whether Florida still has a uniform rural floor. If it
         ever splits, the model needs a per-county wage index instead of
         one number.

=====================================================================
6. AMBULANCE FEE SCHEDULE
=====================================================================
WHAT     Ground ambulance base rates and mileage by locality.
WHY      Transport is the ONLY line that sits outside comprehensive APC
         packaging, so it is added to every episode. Round trip.
WHERE    cms.gov, search "Ambulance Fee Schedule Public Use Files".
FILE     afs####_puf_ext.zip
CHANGES  Annually, effective January 1.
CY2026   Florida is MAC 09102, locality 99. Urban base rates:
         A0428 BLS non-emergency  281.31
         A0426 ALS1 non-emergency 337.57
         A0427 ALS1 emergency     534.49
         A0425 mileage            9.33 per statute mile urban
                                  9.42 rural

=====================================================================
7. HOSPICE PER DIEM RATES
=====================================================================
WHAT     Routine home care, continuous home care, inpatient respite and
         general inpatient rates by county.
WHY      Powers the "What This Means for [Partner]" paragraph. These are
         the partner's own revenue, and the only figures in the report
         that describe their economics rather than the hospital's.
WHERE    cms.gov hospice payment rates, or the annual hospice wage index
         final rule. County-level table for Florida.
FILE     sos_hospice_rates_fl_####.xlsx (as supplied)
CHANGES  Annually, effective October 1.
FY2026   Range across our counties: routine home care $189.04 to $220.42,
         general inpatient $991.73 to $1,149.01.
WATCH    Counties not individually listed fall to "All Other Counties".
         The Villages spans three counties; ruling is to use the highest,
         which is Lake.

=====================================================================
8. PLACE OF SERVICE MIX - THE BLEND WEIGHTS
=====================================================================
WHAT     How often each procedure happens inpatient, hospital outpatient,
         or in the emergency room.
WHY      Determines the weight between the discharged and admitted
         pathways. Without it the model is a guess.
WHERE    cms.gov, "Medicare Physician/Supplier Procedure Summary" (PSPS).
FILE     Physician_Supplier_Procedure_Summary_####.csv, roughly 840 MB.
         Do not upload it. Leave it in the MPU Reporting folder and it
         can be filtered in place to a few kilobytes.
FILTER   Keep rows where HCPCS is 49083, 32555, 51702 or 43762. Sum
         PSPS_SUBMITTED_SERVICE_CNT grouped by HCPCS and
         PLACE_OF_SERVICE_CD. Florida is CARRIER_NUM 09102.
POS      21 inpatient hospital | 22 outpatient hospital | 23 emergency
         room | 11 office
CHANGES  Annually, about a year in arrears.
2025 FLORIDA SPLITS
         Paracentesis   32.8% inpatient / 61.9% outpatient / 5.3% ER
         Thoracentesis  76.1% inpatient / 21.4% outpatient / 2.5% ER
         Catheter       26.8% inpatient / 10.2% outpatient / 63.0% ER
         G-Tube         6.7% inpatient / 3.9% outpatient / 89.4% ER
WATCH    Use Florida, not national. They diverge most on catheter
         management, 63% ER in Florida against 36% nationally.

=====================================================================
NOT A FILE, BUT REQUIRED
=====================================================================
PARTNER RATE CARDS
  Each partner's billing rate by acuity. From Neil, or from Partner_Rates
  in Creator. These change when a contract changes, not on a schedule.

ENCOUNTER ASSUMPTIONS
  Transport level, mileage, ED visit level, DRG severity tier. Currently
  ALS1 non-emergency round trip, 30 statute miles, Level 5, with MCC.
  These are business decisions, not data. Neil's ruling 2026-08-15 is to
  display the highest realistic figures with the methodology disclosed.

=====================================================================
ANNUAL REFRESH, IN ORDER
=====================================================================
1. Download the six file sets above.
2. Confirm status indicators in Addendum D1 have not changed for our
   codes, and read Addendum J for new exclusions.
3. Pull the new facility rates from Addendum B.
4. Recompute physician fees from the new RVU file and conversion factor.
5. Recompute the DRG dollar amounts from the new Table 5 weights and
   Table 1A standardized amounts.
6. Confirm the Florida wage index is still uniform.
7. Refresh the ambulance rates.
8. Refresh the hospice per diems.
9. Re-derive the place-of-service splits from the new PSPS file.
10. Recompute the four blended benchmarks and update prep_partner.py,
    the PATHNOTE block and the CPT narrative in build_docx_v2.js, and
    charts_v2.py PATH.
11. Rebuild one partner report and check the Disclaimers page still
    describes what the model actually does.

=====================================================================
ON API ACCESS
=====================================================================
An API key would not help, and none of these sources need one.

data.cms.gov is open, no authentication. The obstacle is not permission,
it is format: every file above is a ZIP or XLSX download, not a queryable
endpoint. This environment can fetch and read web pages but cannot
download and unpack archives, so the files have to arrive by upload or
be placed in a connected folder either way.

The realistic improvement is not an API. It is keeping the six ZIPs in
the MPU Reporting folder each year, where they can be read and filtered
in place without uploading anything.
