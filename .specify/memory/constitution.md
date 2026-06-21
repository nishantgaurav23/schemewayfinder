# SchemeWayfinder — Project Constitution

Version: 1.0.0

Non-negotiable principles. The plan and analyze phases validate against these; violations are CRITICAL.

## Principle 1 — Citizen data is never persisted
No identifiable PII (name, phone, Aadhaar, raw audio, full profile) is stored beyond session scope. Session state uses Firestore with a TTL. Logs are metadata-only (timestamp, language, scheme_count, latency). Any code that would persist or log PII is rejected.

## Principle 2 — Eligibility is informational, never a guarantee
Every result is framed as candidates to verify with the issuing authority, with a persistent disclaimer. The RejectionRiskAuditor critic loop must run before results reach the user; matches it flags weak are surfaced honestly, not hidden. Human-in-the-loop confirmation precedes generating any application draft.

## Principle 3 — Grounded, not invented
Scheme matches must come from the scheme-search MCP over the real corpus — no agent invents schemes, eligibility rules, or required documents. Agents hand off via structured state, not free-form text.

## Principle 4 — Test-driven, secrets-safe, simple
A file is not done until its tests pass (Red → Green → Refactor). No hardcoded secrets — config + Secret Manager only. Follow existing file/naming conventions; prefer the simplest design that satisfies the spec.
