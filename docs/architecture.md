# Architecture and engineering boundaries

## Responsibility

This example is one small, deterministic validation component in the *conceptual* lifecycle of an AI-assisted document. The only implemented responsibilities are parsing two JSON inputs, checking claim/evidence reference integrity, and returning structured findings plus a process exit status.

It intentionally separates **reference governance** from **semantic verification**. An evidence ID can be valid while the linked prose remains misleading or false.

## Interface contracts

**Evidence registry**: JSON object with `records`, a list of objects containing a unique non-empty string `id`, a `status` of `supported`, `pending` or `withdrawn`, and a boolean `approved`.

**Draft**: JSON object with `claims`, a list of objects containing a unique non-empty string `id`, a non-empty string `text`, and a non-empty list of non-empty string `evidence_ids`.

Additional fields are ignored. Multiple references to the same evidence ID within one claim are deduplicated by the current implementation.

## Validation sequence

1. Parse both input JSON files.
2. Check required collections, record types and unique identifiers.
3. Validate evidence statuses, approval types, claim text and reference lists.
4. Index evidence records by ID.
5. For each distinct referenced ID, classify missing, unsupported or unapproved evidence.
6. Emit JSON findings and an exit status while retaining `human_review_required: true`.

| Condition | Classification |
|---|---|
| Evidence ID not present | `missing_evidence` |
| Evidence exists but status is not `supported` | `unsupported_evidence` |
| Evidence supported but `approved` is `false` | `unapproved_evidence` |
| All references supported and approved | No reference-level finding |
| Input JSON, schema or file invalid | Input error; status `2` |

**Priority rule:** Status checks precede approval checks. A pending, unapproved record receives `unsupported_evidence`, not two separate findings.

## Design trade-offs

- **Determinism over sophistication:** Simple explicit rules are inspectable and repeatable, but they cannot assess meaning.
- **Fail-closed references:** A missing record is rejected instead of assuming approval; this is safer for controlled document outputs.
- **Small JSON contract:** Keeps the demonstration easy to reproduce without services, but omits a database, change history and concurrency controls.
- **Structured findings:** Supports downstream review and automation while limiting the report to identifiers and classification rather than exporting evidence contents.
- **Human approval retained:** The component reports reference consistency, not permission to publish.

## Controls outside the demonstration

No model calls, prompt orchestration, semantic entailment tests, evidence quality assessment, original application workflows, production database, audit trail, authorisation layer, PDF generation, ATS validation or client/employer data appear in this project.

A stronger real-world implementation would also need to address evidence provenance, immutable versions, temporal validity, content-to-source alignment, concurrent updates and appropriate access controls. Those are identified design considerations, **not features implemented here**.

## Verification

Run `python3 -m unittest discover -s tests -v` and the two examples in the README. The deliberately invalid-approval example should produce a reference finding and return exit status `1`. The positive example should return `0`.
