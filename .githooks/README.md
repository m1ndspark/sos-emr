# sos-emr git hooks

Mechanical pre-commit checks for the sos-emr repo. These catch *pattern-level*
mistakes only. They do **not** replace the `sos-precommit-audit` subagent
(judgment: link names, collisions, trigger correctness) or the live test in
Zoho Creator.

## What runs

`sos-checks.sh` (shared by the local hook and CI) scans changed text files:

- **BLOCK** em dash anywhere (context/08 rule)
- **BLOCK** high-confidence secrets/tokens (GitHub PAT, AWS key, Slack, JWT, private keys, Bearer)
- **BLOCK** SSN-shaped values (PHI)
- **WARN** soft secret-like assignments (a hard-coded password, API key, or access token)

`pre-commit` adds two commit-scoped warnings:

- **WARN** `.dg` filename without a known `On<Event>__` prefix
- **WARN** a `.dg` staged with no `_INDEX.md` change

## Enable the local hook (once per clone)

```sh
git config core.hooksPath .githooks
```

Honored by both the git CLI and GitHub Desktop. To bypass in a pinch
(discouraged for Deluge/PHI code): `git commit --no-verify`.

## Cloud backstop

`.github/workflows/precommit-checks.yml` re-runs the same content checks on
every push and pull request, so a `--no-verify` commit or a clone that never
enabled the hook is still caught on GitHub.
