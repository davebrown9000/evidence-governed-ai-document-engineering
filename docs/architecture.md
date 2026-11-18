# Architecture and engineering boundaries

## System context

The broader evidence-governed document-engineering architecture coordinates several responsibilities:

1. **Evidence preparation and approval.** AI assists in extracting, organising and refining factual evidence; human verification and approval establish which entries may be used.
2. **Requirements interpretation.** AI analyses supplied source-document requirements and assesses whether the approved evidence can support an appropriate output.
3. **Structured intermediate artefacts.** Requirements, evidence mapping, specifications and other workflow inputs are prepared so downstream steps can be executed and checked consistently.
4. **Evidence-grounded drafting.** AI drafts purpose-specific content using the approved evidence and declared requirements.
5. **Human content approval.** Review occurs before final document rendering.
6. **Rendering and quality gates.** The broader system renders documents and checks relevant structural, evidence and output properties; correction and revalidation may follow.
7. **Final visual approval.** Human review of rendered artefacts precedes their use or release.

This is an architectural description of a **private broader system**. The publicly available Python code does not orchestrate those steps or invoke AI, produce documents or render PDFs.

## Boundary implemented in this repository

The public package implements **deterministic reference-integrity validation**. It checks whether a fictional draft's declared evidence IDs identify existing, supported, approved records. It returns structured reasons and a process exit status for other systems or reviewers to consume.

```text
Fictional register JSON ─┐
                         ├──> Input validation ──> Reference checks
Fictional claims JSON ───┘                              │
                                                        ▼
                                            JSON report + exit 0/1/2
                                                        │
                                                Human review required
```

It intentionally separates **reference governance** from **semantic verification**. A referenced record can be approved while the linked prose is misleading or false.

## Interface contracts

**Evidence register:** JSON object with `records`, a list whose entries each contain a unique non-empty string `id`, `status` (`supported`, `pending` or `withdrawn`) and boolean `approved`.

**Draft claims:** JSON object with `claims`, a list whose entries each contain a unique non-empty string `id`, non-empty string `text` and non-empty list of string `evidence_ids`.

Additional fields are ignored. Repeated references to the same evidence ID within one claim are deduplicated.

## Validation sequence

1. Parse the input JSON files.
2. Check required collections, object shapes and unique identifiers.
3. Validate evidence statuses, approval types, claim text and reference lists.
4. Index evidence by ID.
5. For each unique reference, classify missing, unsupported or unapproved evidence.
6. Emit machine-readable findings and `human_review_required: true`.

| Condition | Classification |
|---|---|
| Referenced evidence does not exist | `missing_evidence` |
| Evidence exists but its status is not `supported` | `unsupported_evidence` |
| Evidence is supported but not approved | `unapproved_evidence` |
| Every reference is supported and approved | No reference finding |
| Input JSON, schema or file invalid | Input error, exit `2` |

**Priority:** Status is checked before approval. Pending, unapproved evidence produces `unsupported_evidence`, rather than duplicate findings.

## Deterministic quality controls and CI

The broader design uses deterministic checkpoints to complement AI-assisted interpretation and drafting. In the **public implementation**, a GitHub Actions workflow tests the reference-validation component on pushes to `main` and on pull requests. It runs seven standard-library unit tests, one passing fictional example and one deliberately failing fictional example, whose exit status must be `1`.

The CI workflow has read-only repository permissions, pins the checkout and Python-setup actions to commits and uses Python 3.11. **It does not run AI inference, generate PDF outputs or perform human approval.**

## Design trade-offs and unsolved problems

- **Determinism rather than semantic depth:** The rules are inspectable and repeatable but do not evaluate meaning or truth.
- **Fail-closed references:** Missing evidence is rejected, rather than presumed approved.
- **Small JSON contracts:** Easy to reproduce without credentials or services; production persistence, temporal validity, concurrency and version control are not implemented.
- **Structured error reports:** Expose only IDs and reasons, rather than exporting evidence text.
- **Human review remains necessary:** Passing checks never establishes correctness, adequacy of evidence or permission to publish.

The repository contains no private evidence registry, original workflow code, prompt/model integration, document renderer, audit trail, ATS or PDF inspection machinery, production data or sensitive personal records. These are outside the public demonstration, not hidden features of the sample validator.

## Verification

```bash
python3 -m unittest discover -s tests -v
python3 -m demo.validator examples/evidence.json examples/claims_valid.json
python3 -m demo.validator examples/evidence.json examples/claims.json
```

Expected results: seven passing unit tests; status `0` for approved references; status `1` with reason-coded findings for unapproved or unsupported references.
