# Evidence-Governed Document Validation

**A compact Python demonstration of deterministic quality gates for AI-assisted document workflows.**

In systems that use generative AI to draft reports, summaries or application material, fluent text is not evidence of correctness. A useful engineering control is to maintain a separate register of approved evidence and validate every declared claim-to-evidence reference before human review.

This demonstration implements that **reference-integrity gate**, using fictional community-event data. It does not call an AI model or determine whether a claim is factually true.

## The engineering problem

A generated or manually drafted document may contain claims supported by references that are missing, withdrawn, pending or not approved for use. Allowing those references through creates an avoidable quality-control failure. The objective is a small, predictable validation boundary that can be automated and tested independently of how the prose was produced.

## System boundary

```text
                        Illustrative wider workflow (not implemented)
  AI-assisted or human drafting
               |
               v
  Draft claims + evidence IDs -----------------+
                                               |
  Independently maintained evidence register --+--> Deterministic validator
                                                       |
                                      +----------------+-----------------+
                                      |                                  |
                              Machine-readable                      Exit status
                              findings (JSON)                       0 / 1 / 2
                                      |
                                      v
                         Human assessment of meaning,
                         source quality and final release
```

Only the **deterministic validator**, its input fixtures, tests and CI are implemented in this repository. The surrounding AI-assisted workflow is architectural context, not claimed functionality.

## Design decisions

| Decision | Engineering rationale |
|---|---|
| Separate claims from evidence | Makes the approval state independently inspectable rather than embedding it in draft text |
| Validate references deterministically | Creates reproducible checks independent of model output variability |
| Fail closed on missing or unapproved records | Prevents absent evidence from being silently treated as accepted |
| Return structured findings | Supports automated quality gates and human triage |
| Distinguish error exit statuses | Separates invalid inputs from valid inputs that contain unacceptable references |
| Retain mandatory human review | A valid reference cannot establish semantic entailment, truth or appropriateness |

## Implemented behaviour

The Python 3.11+ standard-library validator checks input shape, unique record identifiers, non-empty claim text, valid evidence references, evidence status and explicit approval. It emits a JSON report containing reason-coded findings, a `passed_reference_checks` boolean and `human_review_required: true`.

| Exit code | Meaning |
|---|---|
| `0` | Input accepted; all references pass the implemented checks |
| `1` | Input accepted; one or more evidence-reference checks fail |
| `2` | Invalid JSON, input schema or file access |

### Run it

```bash
python3 -m unittest discover -s tests -v
python3 -m demo.validator examples/evidence.json examples/claims_valid.json
python3 -m demo.validator examples/evidence.json examples/claims.json
```

The third command is an intentionally failing example and should exit with status `1`.

### Example finding

```json
{
  "claim_id": "CLAIM-02",
  "evidence_id": "EVENT-03",
  "reason": "unsupported_evidence"
}
```

The fictional draft asserts that accessibility details have been confirmed, but the referenced evidence is still pending and unapproved. The validator detects that approval-state conflict. It does **not** judge whether the draft wording accurately reflects the evidence.

## Testing and reproducibility

- Seven `unittest` cases exercise accepted references, missing evidence, pending/withdrawn evidence, unapproved evidence, duplicate identifiers, invalid reference types and empty claim text.
- GitHub Actions runs the unit tests plus positive and intentionally failing validation examples.
- No external Python packages, network calls, secrets or real-person datasets are required.

## What this demonstrates

Small, testable controls around data provenance and document quality: explicit approval state, input contracts, fail-closed validation, machine-readable results and a human approval boundary. These are transferable design principles for analytical pipelines and AI-assisted business processes.

## Limitations

This is **not** an LLM evaluation system, factual verifier, semantic entailment engine, document generator, security assurance or full production workflow. A fabricated evidence register or misleading paraphrase can pass these reference checks. The example also does not maintain an immutable evidence audit log or prove that input files remained unchanged after validation.

Detailed contracts and failure boundaries are in [Architecture and limitations](docs/architecture.md).

## Copyright

Copyright © 2026 David Brown. **All rights reserved.** No open-source licence or general permission to reuse, modify or redistribute the implementation is granted. This repository is an independently authored, synthetic demonstration; the underlying private systems and original source implementations are not included.
