#!/bin/sh
# Shared mechanical content checks for sos-emr.
# Scans the files passed as arguments and is reused by both the local
# pre-commit hook (.githooks/pre-commit) and CI (.github/workflows).
#
# SCOPE: deterministic, pattern-level rules only. Link-name verification,
# workflow collisions, trigger correctness and other JUDGMENT calls are the
# sos-precommit-audit subagent's job, not this script's. Passing here is NOT
# a substitute for that audit or for the live Creator test.
#
# Exit 1 if any BLOCK-level issue is found; 0 otherwise (warnings still pass).

fail=0

for f in "$@"; do
  [ -f "$f" ] || continue
  case "$f" in
    *.dg|*.md|*.txt|*.json|*.html|*.css|*.js) : ;;
    *) continue ;;
  esac

  # BLOCK: em dash (context/08 forbids em dashes anywhere).
  em=$(perl -ne 'print "  $ARGV:$.: ", $_ if /\xe2\x80\x94/' "$f")
  if [ -n "$em" ]; then
    echo "BLOCK  Em dash found in $f (context/08: no em dashes anywhere):"
    printf '%s' "$em"
    fail=1
  fi

  # BLOCK: high-confidence hard-coded secrets / tokens.
  sec=$(grep -nE 'ghp_[A-Za-z0-9]{20,}|AKIA[0-9A-Z]{16}|xox[bpar]-[A-Za-z0-9-]{10,}|-----BEGIN [A-Z ]*PRIVATE KEY-----|Bearer [A-Za-z0-9._-]{20,}|eyJ[A-Za-z0-9_-]{15,}\.[A-Za-z0-9_-]{15,}' "$f")
  if [ -n "$sec" ]; then
    echo "BLOCK  Possible hard-coded secret/token in $f:"
    printf '%s\n' "$sec" | sed 's/^/  /'
    fail=1
  fi

  # BLOCK: SSN-shaped value (PHI must never reach the repo).
  ssn=$(grep -nE '(^|[^0-9])[0-9]{3}-[0-9]{2}-[0-9]{4}([^0-9]|$)' "$f")
  if [ -n "$ssn" ]; then
    echo "BLOCK  SSN-shaped value in $f (PHI must never be committed):"
    printf '%s\n' "$ssn" | sed 's/^/  /'
    fail=1
  fi

  # WARN: soft secret keyword assigned a literal (may be a false positive).
  soft=$(grep -niE '(password|passwd|client[_-]?secret|api[_-]?key|access[_-]?token)[[:space:]]*[:=]' "$f")
  if [ -n "$soft" ]; then
    echo "WARN   Secret-like assignment in $f (confirm it is not a real credential):"
    printf '%s\n' "$soft" | sed 's/^/  /'
  fi
done

exit $fail
