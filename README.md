# sos-emr

Canonical git mirror of the Deluge code in the SOS EMR app (Zoho Creator). The
live Creator app is the source of truth; this repo mirrors it. See CLAUDE.md for
the working loop and conventions.

## Source of truth for Deluge: the .ds export (as of 2026-07-29)

`run_schema_monitor` versions field tables (schema/) only. It does NOT version
workflow or function bodies. Before 2026-07-29, that Deluge existed nowhere but
the live Creator instance, so any drift between commits was unrecorded.

Going forward the Application IDE export (`.ds`) is the versioned artifact for
Deluge:

- Commit each dated export as `SOS_Referrals_App_YYYY-MM-DD.ds`.
- Keep `SOS_Referrals_App.ds` as a copy of the newest export.
- `.gitignore` no longer excludes `*.ds` (the exports are definition-only: no
  record data, no PHI).
- Reconcile the `.dg` mirror against a new export with:
  `python3 tools/ds_sync.py --ds SOS_Referrals_App.ds --repo . --apply`
  then regenerate the manifest with `--manifest`.

The `.dg` files remain the per-workflow, paste-back-into-Creator form; the `.ds`
is the whole-app snapshot they are extracted from.
