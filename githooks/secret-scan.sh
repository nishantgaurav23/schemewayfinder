#!/usr/bin/env bash
# secret-scan.sh — block hardcoded secrets before they enter the repo.
# Enforces AGENTS.md rule: NEVER hardcode API keys; all secrets via .env / Secret Manager.
set -euo pipefail

# Scan staged changes if any, else the working tree (excluding common safe paths).
if git rev-parse --git-dir >/dev/null 2>&1 && ! git diff --cached --quiet 2>/dev/null; then
  TARGET="$(git diff --cached --name-only)"
else
  TARGET="$(git ls-files 2>/dev/null || find app eval -type f 2>/dev/null)"
fi

# Patterns for common key formats. Extend as needed.
PATTERNS=(
  'AIza[0-9A-Za-z_\-]{35}'              # Google API key
  'sk-[A-Za-z0-9]{20,}'                 # OpenAI-style
  'sk-ant-[A-Za-z0-9_\-]{20,}'          # Anthropic-style
  'ya29\.[0-9A-Za-z_\-]+'               # Google OAuth token
  '-----BEGIN [A-Z ]*PRIVATE KEY-----'  # private keys
)

FOUND=0
for f in $TARGET; do
  # Skip non-existent, binary, env-example, and the hook itself.
  [ -f "$f" ] || continue
  case "$f" in
    *.env.example|*.png|*.jpg|*.jpeg|*.gif|*.pdf|*.lock|githooks/secret-scan.sh) continue ;;
  esac
  for p in "${PATTERNS[@]}"; do
    if grep -EnI "$p" "$f" >/dev/null 2>&1; then
      echo "SECRET DETECTED in $f (pattern: $p)"
      FOUND=1
    fi
  done
  # Flag any committed .env file outright.
  case "$f" in
    .env|*/.env) echo "REFUSING to commit an .env file: $f"; FOUND=1 ;;
  esac
done

if [ "$FOUND" -ne 0 ]; then
  echo "❌ secret-scan failed — remove secrets, use .env / Secret Manager. Commit blocked."
  exit 1
fi
echo "✅ secret-scan clean"
