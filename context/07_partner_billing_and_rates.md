# Partner Model, Locations, Rates, ID Design, Onboarding, and Billing-Branch Resolution (Session June 26, 2026)

END-OF-DAY CONSOLIDATED VERSION. This supersedes BOTH the June 25 version and the
earlier mid-session June 26 version of this file. The mid-session version described
an email-resolver linkage through Partner_Portal_Users; that approach was REVERSED
later the same day. Partner_Portal_Users is ELIMINATED and billing-branch
determination now runs on a TERRITORY RESOLVER (patient address to branch). Read
this whole file as the current truth.

================================================================================
LATE-SESSION REVERSAL (LOCKED June 26): BRANCH IS DECOUPLED FROM REFERRAL IDENTITY
================================================================================
This is the most important correction in the file and it overrides the REF/PVS ID
format described further below where they conflict.

The error we backed into: making ONE string do two unrelated jobs, identify the
referral AND encode who gets billed. Those are different jobs with different timing.
Welding them together created the whole "what if there is no branch" problem.

LOCKED FIX: separate identity from billing.
- REFERRAL ID = REF-SEQ, a clean sequence only. Example: REF-1001, REF-1002.
  Prefix + sequence, base 1001. Mints On Success of EVERY referral, no dependency,
  no branch token, no PHI. Identity only. Never blocked by an unknown branch.
- BRANCH = a Billing_Branch lookup field on the referral, pointing to the Location.
  Filled when known (typed/aliased now, or resolved from patient address later).
  Blank = pending-branch FOR BILLING ONLY; the referral is fully identified the
  whole time. Billing, reporting, filtering, and grouping all key off this field,
  NOT off the ID string.
- PVS follows the same principle: identity is a clean sequence, branch is not in the
  string. (Referral-linked PVS still ties to its parent referral; exact PVS identity
  to be specced when PVS is built. Principle: identity is not billing.)
- The descriptive PARTNERBRANCH token (ACCHIL) STAYS where it is genuinely identity:
  Partner (PAR-ACC-1001) and Location (LOC-ACCJAX-1001). The referral REFERENCES
  those records; it does not re-encode their codes in its own ID.

Why this is right (not just easier): it matches Neil's audit reality (referrals are
identified by referral, billing is by branch), it makes "no branch yet" a blank
field rather than a crisis, it shrinks the held-referral/Pending-ID machinery to
"fill a lookup when you can", and it is simpler logic.

This REVERSES the REF-ACCHIL-1001 / PVS-ACCHIL-1001 scheme in the "ID FORMAT" and
"PVS ID PATHS" sections below. Those sections remain accurate for PAR and LOC
(branch IS identity there). For REF and PVS, the rule above wins: clean sequence
identity, branch as a separate Billing_Branch lookup. The territory resolver and
the tiered branch resolution still apply, but they now populate Billing_Branch,
they do not build the referral ID.

Where this file conflicts with context/03 or context/06, THIS FILE WINS (those are
flagged stale at their relevant points). The app is being REBUILT in a new Creator
instance; these areas are designed fresh.

================================================================================
DECISION ZERO (RESOLVED June 26, 2026)
================================================================================
Blocker was: a partner code that does not collide with the 3-letter object prefixes
(EMP-for-Empath vs EMP-for-Employee).
RESOLUTION: partner and branch codes are STORED FIELDS Neil/Josh assign at
onboarding, not derived or parsed.
- Partner_Code on the Partner record (ACC). Neil picks it.
- Branch_Code on the Location record (HIL, JAX, MIA). Neil picks it.
The generator reads them off the linked records and concatenates. No construction
rule to invent, no collision (partner token sits in a different slot than the object
prefix; a partner code matching an object prefix reads fine).

================================================================================
ID FORMAT (LOCKED: tier 2, fused token, no PHI)
================================================================================
Canonical: PREFIX-PARTNERBRANCH-SEQ
- PARTNERBRANCH is a FUSED token: Partner_Code immediately followed by Branch_Code,
  no separator. ACC + HIL = ACCHIL. Not ACC-HIL.
- SEQ from the object's Sequence_Tracker row, base 1001.
- No patient data in any ID.

Examples:
  Referral:          REF-ACCHIL-1001
  Visit note (PVS):  PVS-ACCHIL-1001
  Partner:           PAR-ACC-1001        (partner-level, NO branch token)
  Location:          LOC-ACCJAX-1001

This fused layout supersedes the v1.2 suffix format in context/03 (REF-1001-VIT01).
The suffix format is dead. Rejected: encoding patient initials or DOB (HIPAA
identifiers; the ID travels into Flow logs, exports, toward QuickBooks).

================================================================================
PVS ID PATHS (LOCKED)
================================================================================
- Referral-linked PVS: INHERITS PARTNERBRANCH-SEQ from the parent REF.
    REF-ACCHIL-1001 -> PVS-ACCHIL-1001. No REF infix, no M.
- No-referral PVS: MINTS from a DEDICATED manual counter (Option A), base 1001,
    appends M. PVS-ACCHIL-1001M. The M is the only marker of a no-referral note.
- The old MPR token and MPR-path naming are RETIRED; the M suffix replaces them.
- Build note: 1001M is not a pure integer; strip the M before parsing the sequence.

================================================================================
PARTNER MODEL (LOCKED: A / hybrid)
================================================================================
Partner = the ORGANIZATION. Locations = its branches, as a SEPARATE STANDALONE
object (not a subform). Branch_Code lives on the Location.

DESIGN TARGET (explicit): large multi-site partners. The model must hold a
VITAS-style statewide contract: one organization, ~50 locations, hundreds of staff,
uniform statewide pricing. This killed the one-record-per-branch model (Model B),
which duplicates org data and rates per branch and makes a contract-wide rate change
~50 manual edits (a billing-integrity hole). B also does NOT help the territory
problem (territory data still lives on the branch either way), so it loses on every
axis. A/hybrid is locked.

Why Locations are STANDALONE and NOT a subform (verified against Zoho docs June 26):
- A standard lookup CANNOT target an individual subform row (subform rows are
  dynamic child records embedded in the parent, not lookup targets).
- Other forms must point at ONE specific branch (Referral to Location, per-location
  Rate to Location), so the Location must be an independently lookup-able record.
- Each Location has a Partner_Link lookup UP to its Partner (the bi-directional
  relationship Zoho recommends). Referral and Rates look DOWN at the Location.

Hierarchy:
  Partner (PAR)            org identity: legal name, display name, address, phone,
                           Partner_Code, contract file, status, Rate_Structure.
    Location (LOC)         branch; lookup up to Partner; holds Branch_Code and the
                           Location lifecycle status.
    Branch_Territory       child of Location; County/City rules for address routing.
    Partner_Rates (RAT)    contracted rates; lookup up to Partner (stamp only).
    Billing Contact (PBC)  AP contact; routes by Location; holds mailing address
                           and phone (stamp only).

Every partner has at least one Location, including single-site partners. Billing
and routing always resolve through a Location. Single-site is just n=1.

================================================================================
SEQUENCING
================================================================================
- Per-object counters in Sequence_Tracker, each its own row, base 1001.
- Columns: Object_Name, Object_Prefix (3-letter), Object_Sequence, Object_Lock_Status.
- PVS inherits on the referral path (no own row); the no-referral PVS uses a
  dedicated manual counter, base 1001, M-suffixed.
- ALL generators start at 1001 for now.
- PARKED (Neil): distinct starting bases per object later (REF/PVS most-tracked).
  Does not affect REF or PVS; only relevant to the other generators.

================================================================================
COLLISION / UNIQUENESS (LOCKED)
================================================================================
- "No duplicate values" on the FULL custom ID STRING (text plus number), on every
  object that HAS a custom ID.
- Partner_Code is NOT unique (repeats across a partner's branches). Do NOT constrain
  Partner_Code. Uniqueness lives on the assembled ID.
- Generator uses BOUNDED retry on a duplicate rejection (bump sequence, cap ~5,
  never infinite). On exhaustion: save without an ID, flag INTERNALLY
  (Needs_Manual_ID / admin notice). No partner-facing message.
- Volume ~170 to 200 referrals/month; same-instant collisions are very rare.
- BUILD-TIME VERIFY: Creator On Success serial vs parallel, and messaging options.

================================================================================
WHICH OBJECTS GET A CUSTOM ID vs STAMP-ONLY (LOCKED)
================================================================================
Decided by Neil's audit experience (never needed an ID to identify a branch in an
audit; never needs a single concatenated partner+branch+rate string).
- Custom ID: Referral (REF), PVS, Partner (PAR), Location (LOC).
- Native 19-digit stamp ONLY (no custom ID): Partner_Rates, Partner_Billing_Contacts.
  (Partner_Portal_Users is ELIMINATED entirely; see linkage section.)
Terminology stays strict: "stamp" = native 19-digit system ID; "ID" = the custom
human-readable string. Stamp can only be set On Success. All ID/Stamp fields are
read-only, workflow-generated.

================================================================================
RATE MODEL (LOCKED: row model; rates link to Partner)
================================================================================
One record per rate line. Rates link UP to the PARTNER; uniform pricing is entered
ONCE, not per branch.

Rate_Structure flag (on Partners): "Uniform (All Branches/Locations)" |
"Per Branch (Location)". Default Uniform.
- Uniform: one rate set at the Partner level applies to all locations; override
  blank; billing keys on Partner.
- Per Branch: rates attach per Location; billing tries the location-specific rate
  first, falls back to the partner rate.
The flag SELECTS the lookup path. A contract fact only Neil knows, so it is stored
(not derivable).

Rate fields (one per rate line, stamp only):
  Partner_Link, Location_Link (optional; blank = partner-wide, set = override/
  per-location row), Rate_Category (flat: Acuity Level|Premium|Service|Other),
  Rate_Type (flat), Rate_Amount, Effective_Date, Status (Active|Inactive).
Dropdowns FLAT and INDEPENDENT. Optional, not built: a Validate check rejecting an
invalid Category+Type pairing.

RATE VALIDATION:
- Billing-time guard (the spine): if a PVS/invoice finds no resolvable rate for a
  location, BLOCK the charge and flag it. "Can this location be billed" only has an
  answer at billing time.
- Onboarding visibility (convenience): under Per Branch, the Partner shows
  incomplete until every Location has an Active rate. Non-blocking, self-clears. A
  whole-partner completeness check, NOT an On-Success-of-Partner check (Locations
  and Rates do not exist yet at Partner save).
- No hard onboarding gate; the billing-time guard covers the dangerous case.

================================================================================
PVS -> INVOICE BILLING RULE (LOCKED logic, build later on the PVS)
================================================================================
- Exactly ONE acuity level per visit (single-select, required).
- Premiums and services STACK (multi-select, zero or more).
- Equipment entered MANUALLY (description + price); no contracted rate.
- On PVS submit, assemble invoice LINE ITEMS: acuity, each premium, each service
  (rates looked up per type), each equipment (price from the entry).
- Rate lookup keys on Partner (+ Location if Per Branch), Active rate effective as of
  date of service.
- PVS invoice line items are the ONE correct use of a subform (see subform policy).
- The invoice carries patient-identifier ePHI (incl. the Hospice ID/MRN) so the
  partner's AP can reconcile line items. See Hospice ID note below.

================================================================================
INTAKE AND BILLING-BRANCH RESOLUTION (LOCKED June 26, REVERSED from mid-session)
================================================================================
PRIOR (now dead): an email-resolver On Success script matched Partner_POC_Email
against Partner_Portal_Users to pull a verified Partner + Location. REVERSED.

FINAL MODEL:
- INTAKE IS OPEN. Partners use the public Zoho Form. No login, no per-org URL, no
  email prepopulation, no user list. Anyone may submit a completed referral. The
  referrer types their own info (name, title, phone, email) every time.
  Benchmark: RapidX (comparable mobile-diagnostic service) runs an open public
  order form. Open intake is industry-normal.
- Partner_Portal_Users is ELIMINATED. No POC list to seed or sync; the
  dual-maintenance problem disappears. (Trade-off accepted: frequent referrers
  re-type their info; the portal-for-repeats path is parked if that ever becomes a
  partner complaint. A real portal would cost ~$100/mo per 250 external users,
  verify at decision time.)

BILLING-BRANCH IS DERIVED, NOT TYPED. Because no verified branch rides in on the
referral, the billing branch is determined by a TERRITORY RESOLVER:
- Billing follows the PATIENT'S location, not the referrer's. Neil's rule: a Tampa
  referrer sending a Miami patient bills Miami. The patient address is the AUTHORITY,
  not a hint.
- Each Location owns Branch_Territory rules (Type: County | City; Value: "Broward",
  "Miami"). Territory unit is NOT uniform across partners: VITAS draws by county,
  AccentCare by city, so the model stores BOTH types per rule.
- Resolution is SCOPED TO THE REFERRAL'S PARTNER: match the patient's county/city
  against THAT partner's branches' territory rules to find the owning branch. Scoping
  to the partner avoids cross-partner city/county collisions (Miami city vs
  Miami-Dade county only collide if one partner double-claims, which it will not).
- Enabling fact: branch territories are clean and NON-OVERLAPPING within a partner,
  so a patient address maps to exactly one branch deterministically.
- If a typed branch is present, it is a CROSS-CHECK only; the address-derived branch
  wins on conflict (per the rule), and a mismatch is flagged for a human glance.

This territory resolver is now PRIMARY and LOAD-BEARING for billing accuracy (not a
fallback). It must be built well.

OPTIONAL HELPER (not the authority): an alias/mapping table at invoice time that maps
messy typed branch text ("Tampa", "Hills") to a real Location, match-and-remember
(a human approves each new alias once, then exact-match thereafter). Handles the
"known branch, messy text" case; it does NOT invent a billing contact for a truly
new branch. Build only if typed-branch text is worth reconciling; territory is the
primary path regardless.

CLINICAL AUTHORIZATION: NONE needed at the form. A completed referral suffices; SOS
acts on anything and phone-verifies before dispatch. No NPI / signature / physician-
order gate (unlike RapidX, whose diagnostic orders legally require it). The phone
verification is the safety check, outside the form.

HOSPICE ID: it is the PATIENT'S MRN at the hospice, nothing else. It is the
partner's reconciliation key (their AP ties the invoice line back to their patient),
printed on the invoice as ePHI. It is NOT a branch or account identifier and plays
NO role in billing-branch routing. Territory does the routing; Hospice ID does the
partner's reconciliation. Two separate jobs.

================================================================================
LOCATION LIFECYCLE (LOCKED June 26)
================================================================================
Location_Status: Active | Pending | Inactive.
- Active: billable; can source a minted ID; resolvable by the territory resolver.
- Pending: captured, not yet billable. Arises when a referral surfaces a branch the
  partner does not yet have set up (territory resolution finds no matching branch, or
  a genuinely new branch is identified).
- Inactive: a real branch turned off (closed, contract ended). Was billable, no
  longer. Distinct from Pending (no-longer vs never-yet).

Pending -> Active is a DELIBERATE Neil/Josh action (never automatic) because it
requires two human-supplied facts:
  1. Assign Branch_Code (goes in every ID; cannot be derived).
  2. Confirm/add the billing contact for the branch (a new branch with no contact =
     an invoice with nowhere to go).
Plus the branch's territory rules so the resolver can route to it.
Enforce on activation (validate-on-activate): cannot flip to Active with Branch_Code
or billing contact missing. So "Active" MEANS "fully billable", not just clicked.
(Active may instead be a DERIVED status: present and complete -> Active; Neil's call.)

PROMPT / WORKLIST:
- A Pending queue/report (Location_Status == Pending, and the parallel held-referral
  view). The worklist. Build this.
- A push notification on a new Pending branch (Twilio SMS, already in the stack, with
  a deep link to the record). So it is not a queue you must remember to check.
- Optional: a dashboard count.

HELD REFERRALS: a referral whose branch is unresolved/Pending is HELD (no final ID,
not billable) with a visible "Pending Partner Setup" status. When the location goes
Active, the held referral(s) RETROACTIVELY mint their ID and become billable. They
are captured the whole time, just held.

PENDING IS A MONEY QUEUE, not a cleanup queue: a held referral cannot bill until the
branch is Active with a contact, so it should be worked promptly (hence the push).

ACTIVATION ACCESS: open question. Activation is billing-affecting; likely Super
Admin (Josh) plus Neil, not all staff. Confirm.

================================================================================
FORMS SPEC (LOCKED June 26)
================================================================================
PARTNERS (modify existing):
- REMOVE/RETIRE (vestigial under A/hybrid; branch now on the Location):
    Partner_Branch_ID ("01"), Partner_ID_Branch_Stamp. Confirm before deleting.
- ADD: Rate_Structure (radio): "Uniform (All Branches/Locations)" |
    "Per Branch (Location)". Default Uniform.
- KEEP: Partner_Type, Partner_Legal_Name, Partner_Display_Name, Partner_Address,
    Partner_Phone, Partner_Code, Hospice_ID (note: this maps to the PATIENT MRN on a
    referral, not a partner attribute here; on Partners it is a legacy field, confirm
    intent), Partner_Contract_Effective_Date, Partner_Contract_Upload, Partner_Status;
    System: Partner_ID, Partner_ID_Stamp.

PARTNER_LOCATIONS (lean; may already exist, confirm):
    Partner_Link (lookup to Partners; carries the org identity, e.g. "AccentCare")
    Location_Name (the branch's OWN name only, e.g. "Jacksonville"; do NOT repeat the
      partner name; full label is composed: Partner_Display_Name + " " + Location_Name
      -> "AccentCare Jacksonville", assembled on demand, never stored)
    Branch_Code (e.g. JAX)
    Location_Status (Active | Pending | Inactive)
    System: Location_ID (LOC-ACCJAX-1001), Location_ID_Stamp
    NO branch address and NO branch phone. Mailing address lives on the billing
    contact; phone belongs to the person (billing contact / POC), not the location.
    The territory resolver uses the PATIENT'S address, not the branch's.

BRANCH_TERRITORY (NEW; child of Location):
    Location_Link (lookup to Partner_Locations)
    Territory_Type (County | City)
    Territory_Value ("Broward", "Miami")
    One row per county/city a branch owns. Only needed for partners that need
    address routing (multi-branch). Resolver scopes within the referral's partner.

PARTNER_RATES (modify to the locked structure; stamp only):
    Partner_Link, Location_Link (optional override), Rate_Category, Rate_Type,
    Rate_Amount, Effective_Date, Status.

PARTNER_BILLING_CONTACTS (links to a Location; stamp only):
    Location_Link, contact name, email, phone, MAILING ADDRESS (for the invoice;
    may be the branch or a central/corporate office, wherever AP sits).
    A no-branch partner has ONE Location; the contact hangs off it. Billing ALWAYS
    routes through a Location (no partner-direct billing path), so the lookup logic
    is uniform and never has to ask "branch or not".

PARTNER_PORTAL_USERS: ELIMINATED. Not part of intake or onboarding.

================================================================================
ONBOARDING (LOCKED June 26)
================================================================================
Trigger: Neil/Josh take on a partner and fill the Partner form. IDs mint On Success
of each form as it is saved.
Sequence (each step feeds the next):
1. Partner -> mints PAR-ACC-1001 (+ stamp). Neil assigns Partner_Code and
   Rate_Structure.
2. Partner_Locations -> mints LOC-ACCJAX-1001 (+ stamp), reading Partner_Code from
   the parent, Branch_Code from the Location. Neil assigns Branch_Code.
3. Branch_Territory -> county/city rules per location (where address routing is
   needed).
4. Partner_Rates -> rate rows (stamp only).
5. Partner_Billing_Contacts -> per Location (stamp only).
PAR carries NO branch token (no Location exists at Partner save).
There is NO user/POC onboarding step (Partner_Portal_Users eliminated; intake is
open and typed).

Onboarding UX (one screen, no subform):
- ENTRY: a Creator PAGE with embedded quick-add blocks for Locations, Territory,
  Rates, Billing Contacts, scoped to the partner. Each block writes to its real
  standalone object. VERIFY page-embed + auto-set-parent-lookup behavior in the live
  build before speccing (do not narrate Creator UI from memory).
- READ: the Partner detail view auto-shows related Locations and Rates.

================================================================================
SUBFORM POLICY (LOCKED)
================================================================================
- Standalone form whenever another form must point AT the row (Locations, Rates,
  Territory, Billing Contacts).
- Subform ONLY for data read solely in its parent's context, never linked elsewhere.
  Intended use: PVS invoice line items. Never use a subform for Locations.

================================================================================
LIVE SCHEMA NOTES (from Creator screenshots, June 26)
================================================================================
Referrals_Main:
- Partner lookup link name is Partner_Link (Neil renamed it from "Partners";
  context/06 fixed).
- A Partner_Location lookup is NO LONGER required for an email resolver (that model
  is dead). Whether the referral stores a resolved Location at all, or the branch is
  resolved only at billing time by territory, is an OPEN build decision. Likeliest:
  the referral holds the patient address; the territory resolver assigns the billing
  branch at invoice build and stamps it then.
Partners form live fields: Partner_Type, Partner_Legal_Name, Partner_Display_Name,
  Partner_Address, Partner_Phone, Partner_Code, Partner_Branch_ID ("01", VESTIGIAL),
  Hospice_ID, Partner_Contract_Effective_Date, Partner_Contract_Upload,
  Partner_Status; System: Partner_ID, Partner_ID_Stamp, Partner_ID_Branch_Stamp
  (VESTIGIAL). Add Rate_Structure.

================================================================================
OPEN ITEMS CARRIED FORWARD
================================================================================
[ ] Build the generators. NONE written yet. First: Partner On Success generator
    (PAR-ACC-1001 + stamp), the root pattern.
[ ] Capture Partner-form link names (Partner_Code, Partner_ID, Partner_ID_Stamp) and
    confirm the PAR row exists in Sequence_Tracker at 1001 (REF confirmed).
[ ] Retire vestigial Partner_Branch_ID and Partner_ID_Branch_Stamp (confirm first).
[ ] Add Rate_Structure to Partners (Uniform | Per Branch), default Uniform.
[ ] Build Partner_Locations (lean), Branch_Territory (new), confirm Location_Link on
    Partner_Rates, build Partner_Billing_Contacts (with mailing address).
[ ] TERRITORY RESOLVER: design and build. Patient address -> county/city -> the
    partner's branch. VERIFY what Patient_Address captures: does it yield COUNTY, or
    only city/ZIP? VITAS routes by county, so county is required; may need a
    ZIP-to-county step. Define the edge case: patient outside ALL of a partner's
    territories -> flag for review.
[ ] LOCATION LIFECYCLE: Active/Pending/Inactive, validate-on-activate (or derive
    Active), Pending queue + Twilio push, held-referral retroactive release. Confirm
    who can activate.
[ ] Optional: alias table for messy typed branch text (invoice-time helper).
[ ] Onboarding page: verify Creator page-embed + auto-parent-set behavior.
[ ] Build-time: verify On Success serial-vs-parallel and messaging.
[ ] Distinct starting bases per object (parked; only the other generators).
[ ] Confirm Hospice_ID intent on the Partners form (the referral-side Hospice ID is
    the patient MRN; the Partners-form field may be legacy).

================================================================================
NEXT SESSION PLAN
================================================================================
1. Capture the Partner-form link names; confirm the PAR tracker row at 1001.
2. Write the Partner On Success generator (PAR-ACC-1001 + stamp) as the root, then
   Location (LOC-ACCJAX-1001) reusing the pattern.
3. Design the territory resolver against the real Patient_Address (confirm county
   availability first). This is the load-bearing billing mechanism now.
4. Then the Location lifecycle (Pending queue, push, held-referral release).
5. Then PVS (inherit REF or mint M) and the PVS line-item subform + invoice assembly.
Reminder: confirm live Creator behavior before writing (On Success concurrency,
messaging, page-embed, what Patient_Address captures). Do not assume.
