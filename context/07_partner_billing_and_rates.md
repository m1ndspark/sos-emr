# Partner Billing, Rates, Sequencing, and ID Design (Session June 25, 2026)

Decisions made in design discussion. These supersede older docs where they
conflict. The app is being REBUILT in a new Creator instance, so there is no
legacy live code to preserve for these areas; we design them fresh.

================================================================================
REBUILD CONTEXT
================================================================================
- The EMR is being rebuilt in a new Creator instance. As of this session there
  is no code in place for any object IDs or stamps.
- This retires the "what is live vs what the docs say" framing for ID/sequence
  work. We decide the design here; the new instance is built to it.
- The .dg stubs and extraction checklist describe the OLD instance. Treat them as
  build targets, not extraction targets, for the rebuilt areas.

================================================================================
ID FORMAT (LOCKED: tier 2, no PHI)
================================================================================
- Format: PREFIX-PARTNERBRANCH-SEQ. Partner code + branch + sequence. No patient
  data in any ID. Patient linkage comes from the record relationship, not the ID.
- Examples:
    Referral:    REF-ACCHIL-1001
    Visit note:  PVS-ACCHIL-1001   (PVS prepends/echoes the parent referral key)
    Partner:     PAR-ACCHIL-1001
- Rejected during design: encoding patient initials or DOB in the ID. DOB and
  partial DOB are HIPAA identifiers and the ID travels into Flow logs, exports,
  and toward QuickBooks. Kept out deliberately.
- OPEN: final PVS echo form. Decided to drop a redundant "REF" so PVS reads
  PVS-ACCHIL-1001 (not PVS-REF-ACCHIL-1001). Confirm this is final.

================================================================================
SEQUENCING (Sequence_Tracker redesign)
================================================================================
- Per-object counters. CONFIRMED against the live tracker (each object row has
  its own Object_Sequence, all at 1001). This RESOLVES old contradiction 4-C in
  favor of per-object counters. The single-global-counter model is dead.
- Tracker columns: Object_Name, Object_Prefix (3-letter), Object_Sequence,
  Object_Lock_Status.
- Two kinds of objects:
    1. SEQUENCED objects mint their own number from a tracker row.
       REF, MPR, PAR, LOC, EMP, PBR, PBC, PPU, INV, ASN, ADR.
    2. INHERITING objects do not mint and have NO tracker row. PVS is the only
       one: a referral-linked PVS inherits the parent REF's number; a no-referral
       PVS inherits its parent MPR's number.
- ACTION on the rebuild tracker: remove the PVS row (PVS inherits, never mints).
  The MPR row was at 1005 in the old instance; reset to 1001 for a clean start
  unless those four were real and the gap should be preserved.
- No-referral path is parallel to the referral path:
    Referral path:     REF-...-1001  ->  PVS-...-1001
    No-referral path:  MPR-...-1001  ->  PVS-...-1001 (inherits MPR)
- OPEN: starting numbers. Object sequences NEVER reset. Decision pending on
  whether every object starts at 1001 (rely on prefix for type, simplest, the
  v1.2 default) or distinct bases per object. Recommendation on record: all 1001,
  prefix carries the type signal.

================================================================================
COLLISION / DUPLICATE-ID SAFETY (LOCKED approach)
================================================================================
- The ID field uses Creator's field-level "No duplicate values" constraint. The
  database rejects any duplicate of the full ID string. This is the real
  safeguard and it is already enabled on Referral_ID.
- The constraint checks the ENTIRE field value (the whole string), not just the
  sequence segment. Uniqueness is per-field, scoped to that form's field.
- Generator must handle rejection with BOUNDED retry: on a duplicate rejection,
  bump the sequence and retry, capped (about 5 attempts), never an infinite loop.
- On retry exhaustion: the record saved without an ID. Flag it INTERNALLY (admin
  notification or a Needs_Manual_ID status). No partner-facing message: referral
  intake is via Zoho Form, System Fields are hidden from partners, and ID
  generation is backend, so the partner has no window into a conflict. This
  follows the notify-and-retrieve pattern (exceptions handled in the internal
  layer).
- Volume context: ~170-200 referrals/month (~6-7/day), so true same-instant
  collisions are very rare. Retry is cheap insurance for a clinical referral we
  do not want dropped, not a high-concurrency necessity.
- BUILD-TIME VERIFY (do not assume): whether Creator serializes On Success
  workflows or runs them in parallel, and exact Creator v6 messaging options from
  On Success. The no-duplicate constraint makes the design safe either way.
- ACTION: confirm "No duplicate values" is set on EVERY generated ID field
  (Partner_ID, PVS ID, all object IDs), not only Referral_ID.

================================================================================
ID vs STAMP (terminology, LOCKED)
================================================================================
- ID  = custom human-readable string (REF-ACCHIL-1001). Built by workflow.
- Stamp = Creator's native 19-digit system record ID. Captured on submit.
- Both are attached to each object for tracking through automations.
- Stamp can only be set ON SUCCESS (the native ID exists only after save).
- All ID and Stamp fields are read-only to users, workflow-generated. They render
  as editable now only because the views are admin-only pre-launch; set them
  read-only once logic is wired.
- NOTE: the workflow historically called "PVS Stamp Generator" actually builds
  the custom ID string, so by this terminology it is an ID generator, not a Stamp
  generator. Reconcile the name in the rebuild.

================================================================================
PARTNER BILLING HIERARCHY (LOCKED)
================================================================================
Three-level model. Partner holds identity; children link up.

  Partner (PAR)            identity: name, address, phone, primary POC,
                           contract file upload, etc.
    Location (LOC)         branches; lookup to PAR
    Partner_Rates (PBR)    contracted rates; lookup to PAR (see rate model)
    Billing Contact (PBC)  AP contact; lookup to LOCATION (see routing)

- RATES link to PARTNER. Pricing is uniform across a partner's locations today,
  so a rate is a partner-level fact. PBR has an OPTIONAL Location link for future
  per-location pricing: blank = applies partner-wide; set = that location
  overrides. Resolution rule at billing time: location-specific rate first, fall
  back to the partner rate.
- BILLING CONTACT links to LOCATION. Notes go to the requesting location and
  invoices route to that location's contact. Routing is location-level.
- Every partner has at least one Location record, including single-site partners
  (branch 01). Billing logic always resolves routing through a location, so it
  never needs to ask "is this a branch." Single-location is just the n=1 case.
- Referral carries the requesting LOCATION (not just the partner), since notes
  and billing route by location.
- OPEN (decision zero): partner code collides with object prefixes. "EMP" was
  used for Empath but EMP is already the Employee object prefix. Must choose a
  partner-code scheme that does not collide with the 3-letter object prefixes
  (REF, PAR, EMP, etc.). This blocks the partner-and-branch token in every
  partner-linked ID. UNRESOLVED.

================================================================================
RATE MODEL (LOCKED: row model, form = Partner_Rates_2)
================================================================================
Best practice: one record per rate line (one fact per record). A partner has
~10 rate rows. NOT one record per partner with many rate fields.

Form Partner_Rates_2 fields:
  Partner_Link      lookup to Partner
  Rate_Category     flat dropdown: Acuity Level | Premium | Service | Other
  Rate_Type         flat dropdown, all items (see list below)
  Rate_Amount       number (generic name; not "Acuity Level Rate")
  Effective_Date    date
  Status            Active | Inactive  (per-line status)
  Partner_Rate_ID + Stamp   generated on submit

Rate_Type values, grouped by the category they belong to (entered by Neil/Josh):
  Acuity:   High Complexity, Moderate Complexity, Low Complexity, Hospital at Home
  Premium:  After Hours, Super STAT
  Service:  Telemedicine, Care Coordination, General Consultation
  Other:    Cares 3008 Assessment   (category placement: confirm)

- Dropdowns are FLAT and INDEPENDENT (no dependent dropdowns; they are unreliable
  in Creator and only Neil/Josh enter rates). Category and Type are not enforced
  to agree.
- OPTIONAL safety net (not built, low cost): a Validate-workflow check that
  rejects an invalid Category+Type pairing on submit. Insurance on billing data
  without dependent-dropdown flakiness.
- RETIRE the original ten-field Partner_Rates form. Partner_Rates_2 is canonical.
  One rate source only.

================================================================================
PVS -> INVOICE BILLING RULE (LOCKED logic, build later on the PVS)
================================================================================
- Exactly ONE acuity level per visit (single-select on the PVS; required).
- Premiums and services STACK (zero or more; multi-select).
- Equipment is entered MANUALLY on the PVS (description + price); it has no
  contracted rate to look up.
- On PVS submit, assemble invoice LINE ITEMS:
    line: acuity charge      (rate looked up from the partner's Active acuity rate)
    line: each premium       (rate looked up per selected premium)
    line: each service       (rate looked up per selected service)
    line: each equipment     (price taken directly from the PVS entry)
  All written to the invoice; the invoice shows itemized detail for every charge.
- Rate lookup keys on Partner + Rate_Type, choosing the Active rate effective as
  of the date of service (Effective_Date + Status drive this).

================================================================================
OPEN ITEMS CARRIED FORWARD
================================================================================
[ ] DECISION ZERO: partner-code scheme that does not collide with object
    prefixes (EMP clash). Blocks all partner-linked ID tokens.
[ ] Starting sequence numbers: all 1001 (recommended) or distinct bases.
[ ] Confirm "No duplicate values" on every generated ID field, not just
    Referral_ID.
[ ] Rebuild tracker: remove PVS row; reset MPR to 1001 (or preserve gap).
[ ] Confirm final PVS ID form (PVS-ACCHIL-1001, REF dropped).
[ ] Delete the original ten-field Partner_Rates form once Partner_Rates_2 is set.
[ ] Confirm Cares 3008 category placement.
[ ] Optional: add the Validate-workflow Category/Type pairing check.
[ ] Set all ID/Stamp fields read-only once generation logic is wired.
[ ] Build-time: verify Creator On Success serial-vs-parallel and On Success
    messaging options before building the generator + retry.
