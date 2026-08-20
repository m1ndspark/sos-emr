# 31. Modernization Spec - Task Brief

Scoped and confirmed by Neil 2026-08-20 (Session 36).

**This file is the brief, not the spec.** The spec itself is NOT written. It has
**no deadline**. This file exists so that whoever writes it, whenever that
happens, does not have to re-derive the scope.

See also `context/13_platform_migration_options.md`, which holds the host and
app-layer candidate evaluation. That file asks "should we move?"; this one
describes "what would have to be written down before we could."

--------------------------------------------------------------------------------
## 1. What the spec is for

A conversion specification: enough structural and behavioral detail about the
live Creator app that a competent team could rebuild it on a modern stack without
having to reverse-engineer Creator.

--------------------------------------------------------------------------------
## 2. Scope, as confirmed

**Stack-agnostic.** No target platform is chosen and the spec must not assume
one. It describes what the system does and what constraints it operates under,
not which framework implements it. Choosing a stack is a separate decision that
`context/13` tracks.

**Whole app.** Not a module or a slice.

**MPU reporting is called out separately.** It is an out-of-band analytics
pipeline, not application functionality. The savings model, the CMS source files,
the annual refresh cycle and the partner reports are a reporting practice that
sits beside the EMR and reads from it. A rebuild of the app does not rebuild MPU
reporting, and the spec must say so explicitly rather than leaving it implied.

**Structure and logic only. No record migration.** The spec covers entities,
relationships, rules and behavior. Moving live data is out of scope, and the data
migration plan is a separate piece of work that cannot start until a target
exists.

--------------------------------------------------------------------------------
## 3. Required sections

These are the sections the spec must contain when it is written. Counts are as of
2026-08-20 and should be re-derived from `MANIFEST.tsv` and `schema/` at writing
time rather than trusted from this list.

### 3.1 Entity model as normalized tables

34 forms. Creator forms are not normalized tables, so this is a translation, not
a transcription. The large forms are where the denormalization lives:

| Form | Fields |
|---|---|
| `Encounter_PatientVisit` (PVS) | 101 |
| `Services_Procedures` | 84 |
| `Referrals_Main` | 73 |
| `Imaging_Orders` | 44 |
| `Fax_Log` | 28 |

A 101-field PVS is a flattened encounter carrying patient demographics, referral
copy, provider copy, partner copy, clinical content, billing state and fax state
in one row. Expect it to decompose into several tables. The spec must say which,
and must be explicit about which duplicated fields are deliberate point-in-time
snapshots (a copied partner name is a record of what was true at the visit) and
which are just denormalization.

### 3.2 Trigger translation table

Creator has four form events. Each maps to a different place in a conventional
architecture, and the mapping is not one-to-one:

| Creator event | Count | Translates to |
|---|---|---|
| On User Input | 30 | client-side state and reactivity |
| On Validate | 15 | API-side validation |
| On Success | 20 | post-commit jobs |
| On Load | 10 | client state at mount |
| standalone functions | 74 | services, jobs, batch operations |

The table matters more than the counts. Creator collapses "what the form shows",
"what the server rejects" and "what happens after the save" into one scripting
surface, and a rebuild has to pull them apart. On Success in particular is doing
work that a modern stack would split between a transaction, a queue and a
webhook.

### 3.3 Creator-specific behaviors that produced workarounds

From `context/05_deluge_learnings.md`. **These are the ones a rebuild should NOT
inherit.** The spec must list each workaround, name the Creator limitation that
forced it, and state plainly that the workaround disappears on a normal stack.
Examples that already exist in the log:

- ID generation split into its own workflow because Creator cannot guarantee
  ordering between two On Success scripts on the same form.
- Field-level Mandatory abandoned entirely on the PVS in favor of an On Validate
  script, because Mandatory fires on Deluge-hidden fields.
- Form workflows not firing on a Deluge insert, so every insert-side function
  re-implements what the form would have done.
- Sequence numbers minted by read-increment-write against a `Sequence_Tracker`
  row, with no locking, because there is no database sequence.
- `insert into` returning a number rather than a record.

The point of this section is that roughly a third of the app's complexity is
Creator compensation, and a reader estimating rebuild effort will badly
overestimate if that is not separated out.

### 3.4 ID generation and concurrency

`Sequence_Tracker` and the object ID formats in `context/03_id_conventions.md`.
Every minter reads a counter, uses it, and writes back the increment, with no
transaction and no lock. This works today because volume is low and writes are
effectively serialized. **It is not safe under concurrency and the spec must say
so**, along with what the IDs are actually used for: they are human-facing record
locators printed on invoices and faxed documents, so they cannot simply become
opaque surrogate keys.

### 3.5 Non-obvious business rules

The rules that are not derivable from the schema and would be silently lost:

- The referral is authoritative over the source log for billing branch.
- Bill on completion date, not referral date.
- Always the with-MCC DRG tier for hospice patients.
- Never fax a cancelled visit; Attempted (Not Completed) does fax.
- The 24-hour fax clock starts at PVS save, not date of service.
- A provider may override a partner fax number, with the override logged and
  reported.
- Invoice drafts are created at save and lock at fax.

The session logs and `context/23_task_list.md` are where these live today. They
are decisions, not code, and no amount of reading the Deluge recovers them.

### 3.6 Integration contracts

For each: direction, auth model, payload shape, failure behavior and what SOS
owns versus what the vendor owns.

| Integration | Notes |
|---|---|
| Zoho Books | invoicing; ad-hoc line items, no item_id; void-and-rebill path |
| RingCentral | fax; JWT auth, multipart send, poll-for-status, no synchronous outcome |
| SendGrid | notification email; dynamic templates; **BAA still unconfirmed** |
| Zoho Forms | referral intake; fires On Success but never On User Input |
| GitHub | this repo; the schema monitor pushes to it on a schedule |

### 3.7 HIPAA application layer

Per `context/13_platform_migration_options.md` section 2. A host BAA covers
infrastructure only. Everything in the application layer stays SOS's
responsibility on any stack: audit logging, access control, session management,
encryption in transit and at rest, minimum-necessary access, breach detection.
The spec must carry this as a requirements section, not a footnote, because it is
the part most likely to be assumed away when a team is estimating from a feature
list.

--------------------------------------------------------------------------------
## 4. Where the counts in section 3 came from

Checked by ccode 2026-08-20 at the time this brief was written.

**The trigger counts in 3.2 are confirmed exactly.** Derived independently from
`MANIFEST.tsv` (149 rows, regenerated the same day): 74 standalone functions, 30
OnUserInput, 20 OnSuccess, 15 OnValidate, 10 OnLoad. All five match.

**The field counts in 3.1 mostly could not be confirmed**, because `schema/` is
written by a daily 06:00 monitor and several forms have not been re-captured in
weeks. What the mirror says today:

| Form | Brief says | schema/ says | Captured |
|---|---|---|---|
| `Encounter_PatientVisit` | 101 | 100 | 08-19 06:01 |
| `Services_Procedures` | 84 | 0 | 07-18 06:00 |
| `Referrals_Main` | 73 | 59 | 08-17 13:02 |
| `Imaging_Orders` | 44 | 33 | 07-23 06:00 |
| `Fax_Log` | 28 | 25 | 08-20 06:01 |

The PVS row reconciles: the 08-19 capture predates `PVS_3008_Upload`, and
100 + 1 = 101. The others are simply stale, and the `Services_Procedures` count of
0 looks like a failed capture rather than an empty form, which is worth a look on
its own.

None of this changes the brief. It is the reason section 3 says to re-derive the
counts at writing time rather than trusting them, and it is itself an argument
for the spec: a system whose own schema mirror drifts this far is a system whose
shape nobody currently holds in one place.

--------------------------------------------------------------------------------
## 5. Status

**Not started. No deadline.** Tracked as an OPEN row in
`context/23_task_list.md`.
