# SOS Code Checkpoint - 2026-09-09 - Session 42

## 1. Scope

Provider record visibility: let providers sign in (portal or licensed) and see only
their own PVS entries. Plus a parked 3008 question and an Assignments prefill fix.

## 2. Parked

3008 PVS: "Was the 3008 Completed?" pre-selects Yes on entry. Not reproducible from
.ds v41. The field is radiobuttons with values {"No","Yes"} and no `initial value`,
no workflow on Encounter_PatientVisit assigns it, and the only `="Yes"` in the app is
inside `create_3008_pvs_july` (July backfill). Open question: brand-new Add form entry
vs. opening an existing July-imported record.

## 3. Research findings (Creator v6 limits)

- Report filters accept static values only. `Field == zoho.loginuserid` is not possible
  as a report filter.
- Permissions offer only "View" (records the user added) and "View all". No criteria
  option, for app users or portal users.
- `zoho.loginuserid` returns the PORTAL login email in a portal session, and the work
  email in a licensed session. Verified both ways with a temporary diagnostic workflow.
- `thisapp.portal.loginUserEmailid()` returns a list, `thisapp.portal.loginUserName()`
  returns text, `thisapp.portal.isUserInProfile()` returns boolean. All empty in a
  licensed session. None are callable from a report or permission filter.
- Creator's Users field can list Customers (portal users) and be designated record
  owner. Noted as an alternative, not built.
- Page variables (Variables tab plus the single page script) can be referenced in an
  embedded report's filter as `${variable_name}`. One script per page, read-only.
- Snippet syntax is `<%{ deluge %> html <% }%>` with `<%=var%>` interpolation. There is
  no `return` in a snippet.

## 4. Schema changes

| Form | Field | Type | Notes |
|---|---|---|---|
| Encounter_PatientVisit | Provider_Login_Email | Email | System Fields Section, personal data |
| Encounter_PatientVisit | Employee_Link | Lookup to Employees | display Employee_Name_Title |
| Referrals_Main | Employee_Link | Lookup to Employees | System Fields Group |

## 5. Workflow changes

| Form | Workflow | Event | Change |
|---|---|---|---|
| Encounter_PatientVisit | Provider_Identity_Stamp (was Provider_Login_Email_Stamp) | On Validate, Created or Edited | NEW. Resolves Employees by Employee_Email OR Employee_Portal_Email, stamps Provider_Login_Email and Employee_Link. Sources from the record's provider, not the creating session. |
| Assignments | Assignment_Referral_Emp | On Success, Created or Edited | NEW. Stamps Referrals_Main.Employee_Link from the assignment. Clears it when the assignment employee is cleared. |
| Assignments | Assignment_Pull_From_Refe1 | On User Input of Referral_Link | UPDATED. Now also pulls Referral_Date (MM/dd/yyyy), Referral_Partner (Partner / Branch), Referral_POC (Partner_POC_Name_Title). |
| Encounter_PatientVisit | Diag_Session_Identity | On Load, Created | Created then DELETED. Temporary login diagnostic. |

## 6. Functions added

| Function | Args | Purpose |
|---|---|---|
| backfill_provider_login_email | string pMode | Stamp Provider_Login_Email on all PVS. Map keys on work AND portal email. |
| backfill_pvs_employee_link | string pMode | Stamp Employee_Link on all PVS. |
| backfill_pvs_employee_email_alias | string pMode, string pOldEmail, string pNewEmail | Retire a stale Employee_Email on PVS records. |
| backfill_referral_employee_link | string pMode | Stamp Referrals_Main.Employee_Link from Assignments. |
| backfill_employee_name_title | string pMode | Rebuild Employee_Name_Title on Employees. |
| diag_pvs_login_email_gaps | none | List PVS Employee_Email values with no Employees match. |

## 7. Data corrections committed

- Ann Smith: 102 PVS records carried `ardentcarellc1@gmail.com` (her original address).
  Updated to `asmith@sosmmc.com`.
- Joshua Kolanko: duplicate Employees record resolved by Neil. The surviving row was
  missing Employee_Portal_Email, which was then set to
  `joshua.kolanko@sosreferrals.com`.
- One fully blank Employees row removed. Employees count 12 to 11.
- Provider_Login_Email: 286 of 286 PVS stamped, 0 unmatched.
- Employee_Link: 286 of 286 PVS stamped, 0 unmatched.
- Employee_Name_Title: 11 of 11 already correct, no backfill run.

## 8. In progress

Provider Dashboard filtered PVS report:
- Page variable `v_login_email` (Text) created on Provider_Dashboard.
- Page script set to `v_login_email = zoho.loginuserid;`.
- NEXT: add a Report element for PVS_Report with filter
  Provider Login Email is `${v_login_email}`, delete the snippet element, view live.

Design constraint carried forward: the provider portal profile must expose only the
page, never PVS_Report as its own component, or a provider can reach it unfiltered.

## 9. Blocked

- Referrals filtered report. `Referrals_Main` has no provider field of its own and
  Assignments holds zero rows with both a referral and an employee, so
  `backfill_referral_employee_link` PREVIEW returned 350 referrals, 0 matched. Neil is
  going to assign some visits. Revisit after.

## 10. Verification performed

| Check | Result |
|---|---|
| Diag_Session_Identity in portal | zoho.loginuserid = portal email, portal email matched, username neilheird3 |
| Diag_Session_Identity as admin | zoho.loginuserid = work email, both portal tasks empty |
| diag_pvs_login_email_gaps | 2 distinct unmatched values, 102 Ann, 35 Kayla |
| backfill_pvs_employee_email_alias PREVIEW then COMMIT | 102 matched, all initials AS |
| backfill_provider_login_email PREVIEW then COMMIT | 286 changed, 0 unmatched |
| backfill_pvs_employee_link PREVIEW then COMMIT | 286 changed, 0 unmatched |
| backfill_employee_name_title PREVIEW | 11 scanned, 0 changed |
| backfill_referral_employee_link PREVIEW | 350 referrals, 0 matched, no assignments |

## 11. Repo

- `SOS_Referrals_App_2026-09-09_v41.ds` added, `SOS_Referrals_App.ds` refreshed.
- Prior .ds in the repo was v34 (2026-09-03) while Deluge was synced to Session 41.

END
