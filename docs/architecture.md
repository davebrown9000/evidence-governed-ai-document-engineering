# Architecture and boundaries

## Narrow question

Can a submitted draft's declared evidence references be checked *deterministically* against an approved registry, before a separate human review?

## Contract

- Evidence JSON: `records` list of objects with unique string `id`, `status` (`supported`, `pending`, `withdrawn`), and boolean `approved`.
- Claims JSON: `claims` list of objects with unique string `id`, non-empty string `text`, and list `evidence_ids` containing one or more strings.
- Every claim must reference existing, supported, approved evidence. Extra fields are ignored. Invalid input or schema yields exit status `2`; evidence findings yield `1`; a clean report yields `0`.
- The report lists claim IDs and finding categories without exporting evidence text.

## Engineering choices

- A static JSON input format allows tests without networking or secrets.
- Validation is conservative: an absent reference blocks rather than silently defaulting to approval.
- The validator makes no assertions about AI-authored language, truthfulness or semantic fidelity.
- The output is a decision aid; a human review boundary remains mandatory even when all checks pass.

## Explicitly excluded

Any AI prompt/model execution, rich document rendering, production-grade evidence registry, sensitive data ingestion, PDF/ATS checks, identity/chronology reconciliation, security guarantees, and the original application's operational workflow.

## Threat model / what is not solved

A fabricated evidence register can pass. A materially misleading claim can pass if it references approved evidence. The content of evidence may be inaccurate or outdated. Changes to input files after validation are not tracked. External publication must be separately authorised.
