# Stage 1 Public Release Hardening

## Purpose

Stage 1 moves release authority to the public repository without rebuilding
artifacts from source. The public repo owns the visible release, the canonical
public tag, and the final PyPI publish step.

## Required Repository Configuration

- `RELEASE_SIGNING_PUBLIC_KEY` GitHub Actions secret containing the PEM-encoded
  public verification key for `release-manifest.json.sig`
- PyPI trusted publishing configured for this repository environment

## Dispatch Contract

The private repository dispatches `publish-bundle` with:

- `version`
- `tag`
- `draft_tag`
- `manifest_filename`
- `manifest_signature_filename`
- `manifest_sha256`
- `wheel_filename`
- `checksum_filename`
- `source_sha`

The staging release in this repository must stay on `bundle-v<version>` until
verification and PyPI publish both succeed.

## Verification Order

The public workflow must:

1. Download the staged release assets from the public draft release
2. Validate `release-manifest.json` against `.github/release-manifest.schema.json`
3. Verify the detached manifest signature before checksum validation
4. Run `sha256sum -c SHA256SUMS`
5. Confirm the wheel named in `release-manifest.json` matches the dispatched
   wheel filename and digest
6. Publish the exact uploaded wheel to PyPI
7. Create the canonical public release `v<version>` only after the publish step
   succeeds

Operators must verify the detached manifest signature before checksum validation.

The public repo must publish the exact uploaded wheel. It must not rebuild from
source and treat that as equivalent.

## Release Notes Source

The canonical public release body comes from the matching `CHANGELOG.md`
section in this repository plus a provenance footer that includes the verified
staging draft tag, manifest filename, and private source SHA.

## Failure Handling

- If schema validation, signature verification, or checksum validation fails,
  stop before PyPI publish.
- If PyPI publish fails, the release stays draft if PyPI publish fails and the
  canonical `v<version>` release must not be created.
- If final release creation fails after PyPI publish, keep the staging bundle
  intact and retry only the public-side release finalization steps.
