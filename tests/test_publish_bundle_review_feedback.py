from __future__ import annotations

import unittest
from pathlib import Path


class PublishBundleReviewFeedbackTest(unittest.TestCase):
    def test_validator_uses_explicit_failures(self) -> None:
        validator = Path("scripts/validate_publish_bundle_workflow.py").read_text(
            encoding="utf-8"
        )

        self.assertNotIn("assert ", validator)
        self.assertIn("raise SystemExit", validator)

    def test_workflow_pins_jsonschema_and_verifies_wheel_metadata_version(self) -> None:
        workflow = Path(".github/workflows/publish-bundle.yml").read_text(encoding="utf-8")

        self.assertIn("jsonschema==", workflow)
        self.assertIn(".dist-info/METADATA", workflow)
        self.assertIn("staged wheel METADATA version does not match the dispatch payload", workflow)

    def test_workflow_cleanup_tolerates_missing_staging_tag(self) -> None:
        workflow = Path(".github/workflows/publish-bundle.yml").read_text(encoding="utf-8")

        self.assertIn(
            'gh release delete "$DRAFT_TAG" --repo "$GITHUB_REPOSITORY" --yes',
            workflow,
        )
        self.assertIn(
            'if gh api "repos/$GITHUB_REPOSITORY/git/refs/tags/$DRAFT_TAG" >/dev/null 2>&1; then',
            workflow,
        )
        self.assertIn(
            'gh api -X DELETE "repos/$GITHUB_REPOSITORY/git/refs/tags/$DRAFT_TAG"',
            workflow,
        )
        self.assertNotIn("--cleanup-tag", workflow)

    def test_docs_use_single_pypi_failure_statement(self) -> None:
        docs = Path("docs/release-hardening-stage1.md").read_text(encoding="utf-8")

        self.assertNotIn("the release stays draft if PyPI publish fails and the", docs)
        self.assertIn("leave the staging release as a draft and do not create", docs)


if __name__ == "__main__":
    unittest.main()
