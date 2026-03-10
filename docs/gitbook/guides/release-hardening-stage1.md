# Stage 1 Public Release Hardening

Stage 1 hardens the public release flow so this repository becomes the visible
release authority without rebuilding wheels from source.

## What The Public Repo Owns

- the draft staging release `bundle-v<version>`
- signature and checksum verification for the uploaded bundle
- the final PyPI publication of the exact uploaded wheel
- the canonical public release `v<version>`

## Verification Order

1. Download the staged assets from the draft release
2. Validate `release-manifest.json` against the public schema
3. Verify the detached manifest signature before checksum validation
4. Run `sha256sum -c SHA256SUMS`
5. Publish the exact uploaded wheel to PyPI
6. Finalize the canonical public release only after publish succeeds

## Retry Behavior

- If verification fails, the staging release remains draft and PyPI publish does
  not run.
- If PyPI publish succeeds but release finalization fails, rerun the workflow.
  The PyPI step uses `skip-existing` so the already-published wheel is not
  uploaded again.

For the fuller operator contract, see [the release hardening reference](../../release-hardening-stage1.md).
