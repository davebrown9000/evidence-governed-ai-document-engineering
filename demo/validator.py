"""Minimal, synthetic evidence-reference validation; not factual verification."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


class InputError(ValueError):
    """Invalid fictional demonstration input."""


def _items(data: object, key: str) -> list[dict]:
    if not isinstance(data, dict) or not isinstance(data.get(key), list):
        raise InputError(f"Expected JSON object containing list '{key}'")
    items = data[key]
    if any(not isinstance(item, dict) for item in items):
        raise InputError(f"Every '{key}' entry must be an object")
    ids = [item.get("id") for item in items]
    if any(not isinstance(value, str) or not value.strip() for value in ids):
        raise InputError(f"Every '{key}' entry needs a non-empty string id")
    if len(ids) != len(set(ids)):
        raise InputError(f"Duplicate ids in '{key}'")
    return items


def validate(evidence: object, draft: object) -> dict:
    """Return structured findings, not a judgement that claim wording is true."""
    register = _items(evidence, "records")
    claims = _items(draft, "claims")
    for record in register:
        if record.get("status") not in {"supported", "pending", "withdrawn"}:
            raise InputError("Evidence status must be supported, pending or withdrawn")
        if not isinstance(record.get("approved"), bool):
            raise InputError("Evidence approved must be a boolean")
    index = {record["id"]: record for record in register}
    findings = []
    for claim in claims:
        if not isinstance(claim.get("text"), str) or not claim["text"].strip():
            raise InputError("Each claim requires non-empty text")
        refs = claim.get("evidence_ids")
        if not isinstance(refs, list) or not refs or any(not isinstance(v, str) or not v.strip() for v in refs):
            raise InputError("Each claim needs a non-empty list of evidence_ids")
        for ref in sorted(set(refs)):
            record = index.get(ref)
            reason = ("missing_evidence" if record is None else
                      "unsupported_evidence" if record["status"] != "supported" else
                      "unapproved_evidence" if not record["approved"] else None)
            if reason:
                findings.append({"claim_id": claim["id"], "evidence_id": ref, "reason": reason})
    return {"passed_reference_checks": not findings, "human_review_required": True, "findings": findings}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("evidence", type=Path)
    parser.add_argument("draft", type=Path)
    args = parser.parse_args(argv)
    try:
        evidence = json.loads(args.evidence.read_text(encoding="utf-8"))
        draft = json.loads(args.draft.read_text(encoding="utf-8"))
        report = validate(evidence, draft)
    except (InputError, OSError, UnicodeError, json.JSONDecodeError) as exc:
        print(f"Input error: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["passed_reference_checks"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
