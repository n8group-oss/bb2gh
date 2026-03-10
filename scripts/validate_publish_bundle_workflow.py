from __future__ import annotations

import json
from pathlib import Path


def _assert_contains(text: str, needle: str) -> None:
    assert needle in text, f"Expected to find {needle!r}"


def _assert_in_order(text: str, needles: list[str]) -> None:
    positions = []
    for needle in needles:
        position = text.find(needle)
        assert position != -1, f"Expected to find {needle!r}"
        positions.append(position)
    assert positions == sorted(positions), f"Expected strings in order: {needles!r}"


def main() -> None:
    workflow_path = Path(".github/workflows/publish-bundle.yml")
    schema_path = Path(".github/release-manifest.schema.json")
    docs_path = Path("docs/release-hardening-stage1.md")

    workflow = workflow_path.read_text(encoding="utf-8")
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    docs = docs_path.read_text(encoding="utf-8")

    _assert_contains(workflow, "repository_dispatch:")
    _assert_contains(workflow, "publish-bundle")
    _assert_contains(workflow, "gh-action-pypi-publish")
    _assert_contains(workflow, "sha256sum -c SHA256SUMS")
    _assert_contains(workflow, "release-manifest.json")
    _assert_contains(workflow, "release-manifest.schema.json")
    _assert_contains(workflow, "openssl dgst -sha256 -verify")
    _assert_contains(workflow, "packages-dir: pypi-dist/")
    _assert_contains(workflow, "bundle-v")
    _assert_contains(workflow, "draft")

    _assert_in_order(
        workflow,
        [
            "name: Verify manifest schema",
            "name: Verify manifest signature",
            "name: Verify exact bundle checksums",
            "name: Publish exact uploaded wheel to PyPI",
            "name: Publish canonical GitHub Release",
        ],
    )

    assert schema["type"] == "object"
    assert schema["required"] == ["version", "git_sha", "artifacts", "sbom_files"]
    assert schema["properties"]["artifacts"]["minItems"] == 1
    assert schema["properties"]["artifacts"]["maxItems"] == 1

    _assert_contains(docs, "public repo owns the visible release")
    _assert_contains(docs, "publish the exact uploaded wheel")
    _assert_contains(docs, "verify the detached manifest signature before checksum validation")
    _assert_contains(docs, "release stays draft if PyPI publish fails")


if __name__ == "__main__":
    main()
