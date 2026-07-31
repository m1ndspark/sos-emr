# Test fixtures - go-live import rehearsal (2026-07-31, Session 28)

Small throwaway ZZTEST sample files used to rehearse the go-live import sequence
end to end. See context/logs/SOS_Import_Rehearsal_2026-07-31.md for the run and
context/09_cognito_import_procedure.md (Section 5A) for the import findings.

| File | Cols | Purpose |
|---|---|---|
| DRYRUN_1_Referrals_ZZTEST.csv | 21 | Referrals dry-run import |
| DRYRUN_1_Referrals_ZZTEST_v2.csv | 21 | Same, branch value in the text field |
| DRYRUN_2_PVS_ZZTEST.csv | 20 | PVS dry-run import |
| COVERAGE_Referrals_ZZTEST.csv | every importable referral field | Field-coverage import |
| COVERAGE_PVS_ZZTEST.csv | every importable PVS field | Field-coverage import |

Both coverage files imported with ALL fields landing (address sub-fields
included) once the column mapping was set by hand.

NOTES
- DRYRUN_RUNBOOK.txt (the 9-step rehearsal runbook) was not found in ~/Downloads
  and is not yet committed. Pending from Neil.
- The two COVERAGE files originally carried two synthetic SSN-shaped placeholder
  values in Patient_SSN. Both were scrubbed to "REDACTED" in the committed copies
  to keep the repo clear of SSN-shaped data per the standing PHI rule. Field coverage is unaffected; on re-import the
  Patient_SSN On-User-Input formatter does not fire on the import path anyway.
- All rows are ZZTEST / ZZCOV synthetic records, deleted at go-live. No real PHI.
