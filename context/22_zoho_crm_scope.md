# Zoho CRM: Scope and Data Ownership (tabled)

Written: Wednesday, July 22, 2026 (Session 21)
Status: TABLED. Nothing built. No CRM work before 8/3.
Raised because Neil added Zoho CRM to the plan and wants to use it eventually for
partners, billing contacts, employees, and a prospecting list for nurture campaigns.

--------------------------------------------------------------------------------
## Why this needs a decision before any setup
--------------------------------------------------------------------------------
Partners, Partner_Locations, Partner_Billing_Contacts, and Employees are load-bearing
for billing TODAY:
- Partner_Rates keys off Partner_Locations (rates are location-level).
- The Books setup maps Partner_Billing_Contacts to the customer AP email.
- The PVS and Imaging_Orders provider resolvers match Employees on
  Employee_Email == zoho.loginuserid, and Employees carries Provider_NPI and the
  clinical-note signature identity.

Two systems holding the same records means drift, and drift in this data means wrong
invoices or a provider who cannot sign a note.

--------------------------------------------------------------------------------
## The split (decided in principle)
--------------------------------------------------------------------------------
CRM OWNS what Creator does not have:
- Prospects (hospices, PACE orgs, employer groups not yet contracted)
- Deal stages and pipeline
- Outreach history, nurture campaigns, email sequences
This is genuinely new. There is no Creator equivalent and no conflict. A prospect is
not a Partner yet.

CREATOR STAYS system of record for anything the EMR or billing reads:
- Partners, Partner_Locations, Partner_Rates, Partner_Billing_Contacts, Employees

THE HANDOFF: a prospect converting to a customer in CRM is what TRIGGERS creating the
Partner record in Creator. One direction, one authority. Mechanism when built: Zoho
Flow, or a Deluge call against the Creator API.

EMPLOYEES STAYS OUT OF CRM ENTIRELY. It is tied to login identity, NPI, and the
signature on clinical notes. HR and provider-credential data in a sales tool buys
nothing and risks the resolver.

--------------------------------------------------------------------------------
## PHI posture
--------------------------------------------------------------------------------
Zoho CRM is on Zoho's HIPAA-eligible services list and is covered under the existing
Zoho One BAA. Confirm it appears in the signed service list rather than assuming, and
check whether HIPAA mode must be explicitly enabled per module (Zoho typically
requires this, and some features are restricted when it is on).

BAA coverage is NOT the constraint; the data model is. Partner organizations and
their staff are businesses and business contacts, not patients, so that data is clean
in CRM. Keep the boundary at the ORG level: no patient names, DOB, MRN, diagnoses, or
visit detail in prospecting notes or campaign data. Marketing automation, email
sequences, and lead exports all touch CRM records, which is exactly the exposure the
QuickBooks de-identification rule exists to prevent.

--------------------------------------------------------------------------------
## When it is picked up (post-launch)
--------------------------------------------------------------------------------
1. Stand up CRM as a PROSPECTING-ONLY sandbox. No contact with Creator data. This
   satisfies the "play with it" goal with zero risk to the billing path.
2. Design the prospect-to-Partner handoff. Decide the trigger (stage change to Closed
   Won) and the transport (Flow vs Deluge).
3. Only then consider whether any Creator partner data should surface IN CRM as
   read-only context. Default answer is no; a report or lookup is usually enough.

Related SPF note: adding CRM justifies keeping include:zoho.com in the sosreferrals.com
SPF record. It had been flagged as possibly vestigial after the Zoho Mail to SendGrid
migration. CRM sends email, so the include stays.

--------------------------------------------------------------------------------
END
--------------------------------------------------------------------------------
