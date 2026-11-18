import unittest

from demo.validator import InputError, validate


class ValidatorTests(unittest.TestCase):
    def setUp(self):
        self.evidence = {"records": [
            {"id": "A", "status": "supported", "approved": True},
            {"id": "B", "status": "pending", "approved": False},
            {"id": "C", "status": "supported", "approved": False},
            {"id": "D", "status": "withdrawn", "approved": False},
        ]}

    def claim(self, *refs):
        return {"claims": [{"id": "C1", "text": "Fictional claim", "evidence_ids": list(refs)}]}

    def test_pass_with_human_review_still_required(self):
        result = validate(self.evidence, self.claim("A"))
        self.assertTrue(result["passed_reference_checks"])
        self.assertTrue(result["human_review_required"])

    def test_missing_reference_rejected(self):
        result = validate(self.evidence, self.claim("ABSENT"))
        self.assertEqual(result["findings"][0]["reason"], "missing_evidence")

    def test_pending_or_withdrawn_evidence_rejected(self):
        result = validate(self.evidence, self.claim("B", "D"))
        self.assertEqual([x["reason"] for x in result["findings"]], ["unsupported_evidence", "unsupported_evidence"])

    def test_not_approved_rejected(self):
        self.assertEqual(validate(self.evidence, self.claim("C"))["findings"][0]["reason"], "unapproved_evidence")

    def test_duplicate_evidence_id_is_error(self):
        with self.assertRaises(InputError):
            validate({"records": [self.evidence["records"][0]] * 2}, self.claim("A"))

    def test_invalid_reference_type_is_error(self):
        with self.assertRaises(InputError):
            validate(self.evidence, {"claims": [{"id": "C1", "text": "x", "evidence_ids": [5]}]})

    def test_draft_cannot_be_empty_claim_text(self):
        with self.assertRaises(InputError):
            validate(self.evidence, {"claims": [{"id": "C1", "text": "  ", "evidence_ids": ["A"]}]})


if __name__ == "__main__":
    unittest.main()
