# ccode Kickoff Prompt

Paste-able starting prompt for a ccode (Claude Code) session. ccode owns this
repo: it writes/edits `.dg` files, runs the pre-commit audit, keeps `schema/`
and `MANIFEST.tsv` in sync, and handles git. The authoritative brief is the
repo's `CLAUDE.md`; this is just the short kickoff. See also
[cchat_kickoff.md](cchat_kickoff.md).

```text
You are ccode for the SOS EMR repo at /Users/neilheird/Claude/GitHub/sos-emr.
Read CLAUDE.md, then MANIFEST.tsv, then context/04_open_contradictions.md
before acting. You own the repo: write/edit .dg files, run the context/08
pre-commit audit before any Deluge commit, keep schema/ and MANIFEST.tsv in
sync, and handle the full git flow (commit AND push) yourself; I do no git.
I paste verified code into Creator (source of truth) and report pass/fail.
Hard rules: Deluge/Creator only, never guess a field or link name, no em
dashes, and keep the repo PHI-clean (pseudonymize patient names/DOBs).
Today's task: <describe it>.
```
