# Evidence-Governed Document Validation — Minimal Demonstration

A small **fictional** technical demonstration of how a document's material claims can be checked against a separately maintained, approved evidence register. The program produces a validation report; it **does not generate documents, call an AI model, verify that underlying facts are true, or authorise publication**.

## What it demonstrates

- Explicit separation of draft claims and the evidence used to justify them.
- Deterministic checks for missing, unsupported, withdrawn and unapproved evidence.
- Machine-readable findings and a non-zero exit status for failed checks.
- Synthetic test fixtures, automated tests and a minimal CI workflow.

## Architecture

```text
Fictional evidence register ─┐
                             ├─> Deterministic validator ─> JSON report / exit status
Fictional draft claims ──────┘                                │
                                                               v
                                                       Human review required
```

The validator checks **referential and approval consistency**, not semantic entailment. A supported evidence ID does not prove that the claim text accurately paraphrases the evidence. A human reviewer must assess that relationship, evidence quality, context and final suitability.

## Run (Python 3.11+; standard library only)

```bash
python -m demo.validator examples/evidence.json examples/claims.json
python -m unittest discover -s tests -v
```

The supplied draft intentionally contains a claim linked to evidence that is not approved. Therefore the first command prints a report containing a finding and exits with status `1`. Use `examples/claims_valid.json` for a passing example:

```bash
python -m demo.validator examples/evidence.json examples/claims_valid.json
```

## Scope and limits

This is **new, deliberately narrow demonstration code**. It is not a distribution, derivative copy, or performance benchmark of the author's private document-engineering workflow. It does not reproduce its data model, production validator, PDF builder, chronology logic, ATS checks, provenance implementation or internal governance. All people, organisations, claims and records are fictitious.

The hypothetical document setting is a community event announcement, not a job application. No actual client, employer or applicant information is used.

## Publication and licence

**PUBLICATION CANDIDATE — NOT YET AUTHORISED FOR PUBLICATION.** Copyright © 2026 David Brown. All rights reserved. No open-source licence or general permission to reuse, modify or redistribute this demonstration is granted. This candidate must pass final security review and receive exact-snapshot approval before being made public.

See [architecture and limits](docs/architecture.md) and [NOTICE](NOTICE.md).
