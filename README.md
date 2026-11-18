# Evidence-Governed AI Document Engineering

An AI-assisted document-engineering workflow that combines structured evidence management, requirements analysis, controlled content generation, deterministic validation and human oversight to produce accurate, traceable and purpose-specific documents.

The broader architecture uses AI to help establish and maintain an approved evidence register, interpret requirements from source documents, assess whether sufficient evidence exists to satisfy those requirements, and generate the structured artefacts needed for document production.

AI-assisted drafting then produces content grounded in the approved evidence, while programmatic controls validate evidence references, structural requirements and document integrity. Human approval is incorporated at defined checkpoints, including before and after final document rendering.

**This public-facing repository demonstrates one component of that architecture:** deterministic claim-to-evidence validation using fictional data. The complete AI orchestration, evidence-management and document-generation implementations remain private.

## Architecture overview

The broader workflow separates interpretation and content generation from repeatable quality controls:

```text
Source requirements ──────────────── Approved evidence register
         │                                     ▲
         ▼                                     │
AI-assisted requirements assessment    AI-assisted evidence preparation
         │                             + human verification and approval
         └────────────────┬────────────────────┘
                          ▼
              Structured workflow artefacts
                          │
                          ▼
              Evidence-grounded AI drafting
                          │
                          ▼
                   Human content review
                          │
                          ▼
               Controlled document rendering
                          │
                          ▼
          Programmatic output and integrity checks
                          │
                          ▼
                 Human visual review
```

This is a conceptual overview of the **broader private system**, not an execution diagram for the public Python package. Its review, validation and correction stages can recur as artefacts are refined.

The **implemented public example** is deliberately narrower:

```text
Fictional evidence register ─┐
                             ├──> Deterministic reference validator
Fictional draft claims ──────┘                  │
                                     JSON findings + exit status
                                               │
                                       Human review required
```

## The engineering problem

AI-generated or manually drafted material may contain claims linked to evidence that is absent, pending, withdrawn or not approved. Fluent prose alone is not an assurance of factual accuracy or permission to use the cited evidence. Separating approved evidence from generated text makes a useful portion of document quality measurable and reproducible.

The demonstrated control checks **whether declared evidence references are valid and approved**. It does not independently establish factual truth, assess semantic entailment or authorise publication.

## Design decisions

| Decision | Engineering rationale |
|---|---|
| Maintain evidence independently from drafts | Makes evidence status and approval reviewable without relying on generated text |
| Structure requirements and intermediate artefacts | Creates explicit inputs and checkpoints for a multi-stage workflow |
| Apply deterministic reference checks | Produces repeatable validation independent of variability in AI drafting |
| Fail closed on missing or unapproved references | Prevents absent evidence from silently being accepted |
| Emit structured findings and exit statuses | Supports automation, diagnosis and subsequent human review |
| Preserve human approval checkpoints | A valid reference does not establish whether wording is truthful, complete or suitable |

Only the reference-validation decisions are implemented in this public repository; the broader workflow decisions are described as architectural context.

## Public demonstration

The Python 3.11+ standard-library validator accepts two JSON inputs: a fictional evidence register and fictional draft claims. It validates input shape, unique identifiers, non-empty claim text, referenced evidence status and explicit approval. Its JSON report includes reason-coded findings, `passed_reference_checks` and `human_review_required: true`.

| Exit code | Meaning |
|---|---|
| `0` | Inputs are valid and all references pass the implemented checks |
| `1` | Inputs are valid but one or more references fail |
| `2` | Invalid JSON, schema or file access |

### Run locally

```bash
python3 -m unittest discover -s tests -v
python3 -m demo.validator examples/evidence.json examples/claims_valid.json
python3 -m demo.validator examples/evidence.json examples/claims.json
```

The last command deliberately produces a finding and returns status `1`.

### Example finding

```json
{
  "claim_id": "CLAIM-02",
  "evidence_id": "EVENT-03",
  "reason": "unsupported_evidence"
}
```

The fictional draft claims that accessibility details are confirmed, but the referenced evidence remains pending and unapproved. The validator detects this inconsistency in evidence status; it cannot determine whether the draft paraphrases a source faithfully.

## Continuous Integration and Quality Assurance

The architecture combines AI-assisted document generation with deterministic validation and human approval. This separates probabilistic content generation from reproducible engineering controls.

Within the broader workflow, structured inputs, evidence references, document specifications and generated outputs are subject to defined validation checkpoints. These controls help detect unsupported claims, structural inconsistencies and document-quality issues before final approval.

The public demonstration implements a limited subset of these controls through GitHub Actions. Its CI workflow automatically:

- Executes seven Python unit tests.
- Validates a synthetic document containing approved evidence references.
- Confirms that a document referencing unapproved evidence is rejected.
- Fails when the implemented validation checks do not behave as expected.

The demonstration's CI workflow runs on pushes to `main` and pull requests. It uses Python 3.11, commit-pinned GitHub Actions dependencies and read-only repository permissions.

**Scope:** Public CI validates the demonstrated Python component. It does not execute the broader AI-assisted drafting, document-rendering or human-approval workflow.

## Limitations and scope

This repository is **not** an LLM evaluation system, a factual verifier, a semantic entailment engine or the full document-production system. A fabricated evidence register or misleading paraphrase can pass these reference checks. The example does not maintain an immutable evidence audit log or verify that files remain unchanged after validation.

The fictional community-event fixtures are designed solely to exercise reference validation. They are not real source records, employer material, client material or production outputs.

See [Architecture and engineering boundaries](docs/architecture.md) for detailed input contracts and what remains outside the demonstration.

## Copyright

Copyright © 2026 David Brown. **All rights reserved.** No open-source licence or general permission to reuse, modify or redistribute the implementation is granted. The original private systems and their source code are not included.
