# SOS Module - Platform Migration Options (Stay on Zoho vs Modern Stack)

Purpose: capture the standing "should the EMR leave Zoho Creator for a self-owned
stack" question so the trade-offs and candidate vendors live on disk, not just in
chat. This is a decision-space log, NOT a decision. No migration is planned or
approved.

First logged: 2026-07-11 (from the 2026-06-27 "pay for hosting + a BAA and write
in a good language" discussion; Fly.io added as a named candidate this session).

--------------------------------------------------------------------------------
1. THE QUESTION
--------------------------------------------------------------------------------
Stay on Zoho Creator, or rebuild the EMR on a self-owned modern stack (relational
DB + real auth + a JS/React frontend on a HIPAA-capable host).

The real framing is NOT "Zoho vs a modern language." The deciding variable is how
much more app is left to build, over what horizon:
- Near feature-complete and shifting into operating the app: Creator friction is
  front-loaded and nearly sunk. Rebuilding throws away paid value.
- Genuinely early, with years of feature-building ahead against Deluge's ceiling:
  friction compounds and a one-time migration could pay back.

--------------------------------------------------------------------------------
2. SHARED-RESPONSIBILITY PRINCIPLE (why a host BAA is not enough)
--------------------------------------------------------------------------------
HIPAA compliance on a self-owned stack is TWO layers, and a host BAA covers only
one of them:
- HOST layer (covered by the host BAA): datacenters, encryption at rest and in
  transit, network isolation, the hypervisor. Security OF the cloud.
- APPLICATION layer (built and owned by you, in code): audit logging on every PHI
  read and write, role-based access control, authentication with unique user IDs
  and MFA, automatic session logoff, integrity controls, breach detection,
  backups. Security IN the cloud.
- A separate BAA is required with EVERY service that touches PHI (host, auth
  provider, email, SMS), not just the host.
- The application layer is exactly what Zoho Creator rents you prebuilt. Leaving
  means owning all of it as maintained code, solo. THAT is the real cost of
  migration, not the hosting line item.

--------------------------------------------------------------------------------
3. CANDIDATE HOSTS (infra layer only)
--------------------------------------------------------------------------------
- Fly.io (https://fly.io/compliance): BAA pre-signed by Fly, activates when you
  sign it. SOC2 Type2 report. Hardware in ISO 27001 datacenters. GDPR DPA
  pre-signed. Firecracker VM isolation (no shared kernel). Default-deny public
  networking. SSO and MFA included. Full app-hosting platform; slots in as the
  host + BAA layer ONLY, not the application layer above.
- Named generically 2026-06-27, not yet evaluated: AWS RDS under BAA, Supabase
  HIPAA tier, Aptible.

--------------------------------------------------------------------------------
4. CANDIDATE APP-LAYER PIECES (not yet evaluated)
--------------------------------------------------------------------------------
- Relational DB: Postgres.
- Auth provider that signs a BAA: Auth0, AWS Cognito.
- Frontend: React.
- Everything listed in Section 2's application layer would still be custom-built
  and owned regardless of these choices.

--------------------------------------------------------------------------------
5. STATUS
--------------------------------------------------------------------------------
Open decision space. No action approved. Revisit only if the build horizon shifts
from "operating the EMR" to "years of new feature-building."
