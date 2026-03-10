from __future__ import annotations

import json
from pathlib import Path


def _fail(message: str) -> None:
    raise SystemExit(message)


def _require(condition: bool, message: str) -> None:
    if not condition:
        _fail(message)


def _require_contains(text: str, needle: str) -> None:
    _require(needle in text, f"Expected to find {needle!r}")


def _require_in_order(text: str, needles: list[str]) -> None:
    positions = []
    for needle in needles:
        position = text.find(needle)
        _require(position != -1, f"Expected to find {needle!r}")
        positions.append(position)
    _require(positions == sorted(positions), f"Expected strings in order: {needles!r}")


def main() -> None:
    workflow_path = Path(".github/workflows/publish-bundle.yml")
    schema_path = Path(".github/release-manifest.schema.json")
    docs_path = Path("docs/release-hardening-stage1.md")
    guide_path = Path("docs/gitbook/guides/release-hardening-stage1.md")
    summary_path = Path("docs/gitbook/SUMMARY.md")

    workflow = workflow_path.read_text(encoding="utf-8")
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    docs = docs_path.read_text(encoding="utf-8")
    guide = guide_path.read_text(encoding="utf-8")
    summary = summary_path.read_text(encoding="utf-8")

    _require_contains(workflow, "repository_dispatch:")
    _require_contains(workflow, "publish-bundle")
    _require_contains(workflow, "gh-action-pypi-publish")
    _require_contains(workflow, "sha256sum -c SHA256SUMS")
    _require_contains(workflow, "release-manifest.json")
    _require_contains(workflow, "release-manifest.schema.json")
    _require_contains(workflow, "openssl dgst -sha256 -verify")
    _require_contains(workflow, "packages-dir: pypi-dist/")
    _require_contains(workflow, "skip-existing: true")
    _require_contains(workflow, "bundle-v")
    _require_contains(workflow, "draft")
    _require_contains(workflow, "environment:")
    _require_contains(workflow, "name: pypi")
    _require_contains(workflow, "release-bundle/*")
    _require_contains(workflow, "jsonschema==4.22.0")
    _require_contains(workflow, ".dist-info/METADATA")
    _require_contains(workflow, "staged wheel METADATA version does not match the dispatch payload")

    _require_in_order(
        workflow,
        [
            "name: Verify manifest schema",
            "name: Verify manifest signature",
            "name: Verify exact bundle checksums",
            "name: Publish exact uploaded wheel to PyPI",
            "name: Publish canonical GitHub Release",
        ],
    )

    _require(schema["type"] == "object", "release-manifest schema must be an object")
    _require(
        schema["required"] == ["version", "git_sha", "artifacts", "sbom_files"],
        "release-manifest schema required fields changed unexpectedly",
    )
    _require(
        schema["properties"]["artifacts"]["minItems"] == 1,
        "release-manifest schema must require one artifact",
    )
    _require(
        schema["properties"]["artifacts"]["maxItems"] == 1,
        "release-manifest schema must cap artifacts at one item",
    )

    _require_contains(docs, "public repo owns the visible release")
    _require_contains(docs, "publish the exact uploaded wheel")
    _require_contains(docs, "verify the detached manifest signature before checksum validation")
    _require_contains(docs, "leave the staging release as a draft and do not create")
    _require_contains(docs, "skip-existing")
    _require_contains(docs, "environment: pypi")
    _require_contains(guide, "Stage 1 Public Release Hardening")
    _require_contains(summary, "guides/release-hardening-stage1.md")


if __name__ == "__main__":
    main()
