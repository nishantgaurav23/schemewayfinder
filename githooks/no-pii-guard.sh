#!/usr/bin/env bash
# no-pii-guard.sh — guard against persisting identifiable citizen data (PII).
# Enforces AGENTS.md rule: session-scoped state only; metadata-only logs; Firestore TTL.
# This is a heuristic guard: it FAILS on clearly risky patterns and WARNS on suspicious ones.
set -euo pipefail

if git rev-parse --git-dir >/dev/null 2>&1 && ! git diff --cached --quiet 2>/dev/null; then
  TARGET="$(git diff --cached --name-only | grep -E '\.py$' || true)"
else
  TARGET="$(git ls-files '*.py' 2>/dev/null || find app -name '*.py' 2>/dev/null)"
fi

BLOCK=0
WARN=0
for f in $TARGET; do
  [ -f "$f" ] || continue

  # Hard block: logging raw profile / audio / identifying fields.
  if grep -EnI '(logger|log|loguru)\.(info|debug|warning|error).*(profile|aadhaar|phone|audio_bytes|raw_text|full_name)' "$f" >/dev/null 2>&1; then
    echo "PII RISK (block) in $f — looks like raw PII is being logged."
    BLOCK=1
  fi

  # Warn: writing profile/PII to a persistent store without an obvious TTL/session scope.
  if grep -EnI '(firestore|collection|\.set\(|\.add\(|INSERT INTO).*(profile|aadhaar|phone|full_name)' "$f" >/dev/null 2>&1; then
    if ! grep -EnI '(ttl|expire|session)' "$f" >/dev/null 2>&1; then
      echo "PII RISK (warn) in $f — persisting profile-like data without a visible TTL/session scope."
      WARN=1
    fi
  fi
done

if [ "$BLOCK" -ne 0 ]; then
  echo "❌ no-pii-guard failed — do not log/persist raw PII. Commit blocked."
  exit 1
fi
[ "$WARN" -ne 0 ] && echo "⚠️  no-pii-guard warnings above — confirm session-scope/TTL before shipping."
echo "✅ no-pii-guard checked"
exit 0
