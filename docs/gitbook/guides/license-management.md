# License Management

Complete reference for managing your bb2gh license.

## Registration

Register for a license using the CLI:

```bash
bb2gh license register --email you@company.com
```

### Options

| Option | Description |
|--------|-------------|
| `--email`, `-e` | Your email address (required) |
| `--tier`, `-t` | Plan tier: `free`, `pro`, or `ultimate` (default: `free`) |
| `--force` | Skip email format validation |

### Free Plan

Free plan licenses are sent automatically to your email:

```bash
bb2gh license register --email you@company.com --tier free
```

### Pro and Ultimate Plans

For paid plans, registration directs you to the sales team:

```bash
bb2gh license register --tier pro
```

Contact [sales@n8-group.com](mailto:sales@n8-group.com) for pricing and license keys.

## Activation

Activate a license key after receiving it. There are three ways to provide the key:

### Option 1: Command Line Argument

```bash
bb2gh license activate BB2GH-1-eyJ2Ijox...
```

### Option 2: Key File

Save the license key to a file and reference it:

```bash
bb2gh license activate --key-file license.key
```

### Option 3: Environment Variable

Set the `BB2GH_LICENSE` environment variable. This is the recommended method for CI/CD:

```bash
export BB2GH_LICENSE="BB2GH-1-eyJ2Ijox..."
```

When using the environment variable, no file is written to disk. The license is validated on each run.

### Where Licenses Are Stored

When activated via the CLI, the license is saved to `~/.bb2gh/license` with restricted permissions (owner read/write only).

bb2gh checks for a license in this order:

1. `BB2GH_LICENSE` environment variable
2. `~/.bb2gh/license` file
3. `.bb2gh/license` file in the current directory

The first valid license found is used.

## Checking Status

View your current license details:

```bash
bb2gh license status
```

Example output:

```
License Status
  Tier:          pro
  Organization:  Acme Corp
  Email:         admin@acme.com
  License ID:    lic_a1b2c3d4
  Expires:       2027-01-15 (337 days remaining)
  Status:        Valid
  Repo limit:    Unlimited
  Workers:       Up to 4

Features
  [x] Discover
  [x] Plan
  [x] Migrate Repos
  [x] Migrate PRs
  [x] Migrate Comments
  [x] LFS
  [x] Rollback
  [x] Validate
  [x] Parallel Workers
  [ ] Batch Waves
  [ ] Secrets Management
  [ ] Distributed Workers
  [ ] Compliance Reports
```

## Deactivation

Remove the stored license:

```bash
bb2gh license deactivate
```

This deletes the `~/.bb2gh/license` file and clears the in-memory cache.

> **Note**: If the `BB2GH_LICENSE` environment variable is set, deactivation removes the file but the environment variable still takes effect. Unset the variable separately if needed.

## CI/CD Integration

### GitHub Actions

```yaml
jobs:
  migrate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Install bb2gh
        run: pip install bb2gh
      - name: Run migration
        env:
          BB2GH_LICENSE: ${{ secrets.BB2GH_LICENSE }}
          BB_USERNAME: ${{ secrets.BB_USERNAME }}
          BB_API_TOKEN: ${{ secrets.BB_API_TOKEN }}
          GH_TOKEN: ${{ secrets.GH_TOKEN }}
        run: bb2gh migrate --plan plan.json
```

### GitLab CI

```yaml
migrate:
  image: python:3.12
  variables:
    BB2GH_LICENSE: $BB2GH_LICENSE
    BB_USERNAME: $BB_USERNAME
    BB_API_TOKEN: $BB_API_TOKEN
    GH_TOKEN: $GH_TOKEN
  script:
    - pip install bb2gh
    - bb2gh migrate --plan plan.json
```

### Docker

```bash
docker run --rm \
  -e BB2GH_LICENSE="$BB2GH_LICENSE" \
  -e BB_USERNAME="$BB_USERNAME" \
  -e BB_API_TOKEN="$BB_API_TOKEN" \
  -e GH_TOKEN="$GH_TOKEN" \
  -v $(pwd):/work \
  ghcr.io/n8group-oss/bb2gh:latest \
  migrate --plan /work/plan.json
```

## Troubleshooting

See [Troubleshooting > License Issues](troubleshooting.md#license-issues) for common problems and solutions.
