# Docker & CI/CD Usage

bb2gh publishes multi-architecture Docker images to GitHub Container Registry (GHCR), making it easy to run migrations in CI/CD pipelines without installing Python.

## Docker Image

```bash
docker pull ghcr.io/n8group-oss/bb2gh:latest
```

### Available Tags

| Tag | Example | Description |
|-----|---------|-------------|
| `latest` | `ghcr.io/n8group-oss/bb2gh:latest` | Latest release |
| `{version}` | `ghcr.io/n8group-oss/bb2gh:0.3.0` | Exact version |
| `{major}.{minor}` | `ghcr.io/n8group-oss/bb2gh:0.3` | Latest patch in minor |
| `{major}` | `ghcr.io/n8group-oss/bb2gh:0` | Latest in major |

### Architectures

Images are built for both `linux/amd64` and `linux/arm64`, so they work on standard CI runners and ARM-based machines (e.g., Graviton, Apple Silicon).

### Image Details

- **Base**: `python:3.11-slim`
- **Size**: ~200MB
- **User**: Non-root `bb2gh` user
- **Includes**: git, git-lfs
- **Entrypoint**: `bb2gh`

## Local Usage

### Basic Commands

```bash
# Run discovery
docker run --rm \
  -e BB_USERNAME=your-username \
  -e BB_API_TOKEN=your-token \
  -e GH_TOKEN=ghp_your-token \
  -v $(pwd):/workspace \
  ghcr.io/n8group-oss/bb2gh:latest \
  discover --workspace my-workspace

# Run migration
docker run --rm \
  -e BB_USERNAME=your-username \
  -e BB_API_TOKEN=your-token \
  -e GH_TOKEN=ghp_your-token \
  -v $(pwd):/workspace \
  ghcr.io/n8group-oss/bb2gh:latest \
  migrate --plan plan.yaml
```

### With Docker Compose

A `docker-compose.yml` is included in the repository for convenient local usage:

```bash
# Set credentials in .env file
echo "BB_USERNAME=your-username" >> .env
echo "BB_API_TOKEN=your-token" >> .env
echo "GH_TOKEN=ghp_your-token" >> .env

# Run commands
docker compose run --rm bb2gh discover --workspace my-workspace
docker compose run --rm bb2gh migrate --plan plan.yaml
```

### Persisting State

bb2gh stores migration state in `~/.bb2gh/state.db`. To persist state across Docker runs, mount a volume:

```bash
docker run --rm \
  -v bb2gh-state:/home/bb2gh/.bb2gh \
  -v $(pwd):/workspace \
  -e BB_USERNAME=... -e BB_API_TOKEN=... -e GH_TOKEN=... \
  ghcr.io/n8group-oss/bb2gh:latest \
  migrate --plan plan.yaml
```

## GitHub Actions

Use the Docker image in GitHub Actions workflows to automate migrations:

```yaml
name: Migrate Repositories

on:
  workflow_dispatch:
    inputs:
      workspace:
        description: 'Bitbucket workspace to migrate'
        required: true

jobs:
  migrate:
    runs-on: ubuntu-latest
    container:
      image: ghcr.io/n8group-oss/bb2gh:latest
    env:
      BB_USERNAME: ${{ secrets.BB_USERNAME }}
      BB_API_TOKEN: ${{ secrets.BB_API_TOKEN }}
      GH_TOKEN: ${{ secrets.GH_TOKEN }}
    steps:
      - name: Discover repositories
        run: bb2gh discover --workspace ${{ inputs.workspace }}

      - name: Generate migration plan
        run: bb2gh plan --workspace ${{ inputs.workspace }}

      - name: Run migration
        run: bb2gh migrate --plan plan.yaml

      - name: Validate migration
        run: bb2gh validate --plan plan.yaml

      - name: Upload results
        uses: actions/upload-artifact@v4
        if: always()
        with:
          name: migration-results
          path: |
            plan.yaml
            .bb2gh/
```

### Step-by-Step Workflow

For more control, run each phase as a separate job:

```yaml
name: Phased Migration

on:
  workflow_dispatch:
    inputs:
      workspace:
        description: 'Bitbucket workspace'
        required: true

jobs:
  discover:
    runs-on: ubuntu-latest
    container:
      image: ghcr.io/n8group-oss/bb2gh:0
    env:
      BB_USERNAME: ${{ secrets.BB_USERNAME }}
      BB_API_TOKEN: ${{ secrets.BB_API_TOKEN }}
    steps:
      - name: Discover
        run: bb2gh discover --workspace ${{ inputs.workspace }} --output repos.json
      - uses: actions/upload-artifact@v4
        with:
          name: discovery
          path: repos.json

  plan:
    needs: discover
    runs-on: ubuntu-latest
    container:
      image: ghcr.io/n8group-oss/bb2gh:0
    env:
      BB_USERNAME: ${{ secrets.BB_USERNAME }}
      BB_API_TOKEN: ${{ secrets.BB_API_TOKEN }}
      GH_TOKEN: ${{ secrets.GH_TOKEN }}
    steps:
      - uses: actions/download-artifact@v4
        with:
          name: discovery
      - name: Plan
        run: bb2gh plan --input repos.json
      - uses: actions/upload-artifact@v4
        with:
          name: plan
          path: plan.yaml

  migrate:
    needs: plan
    runs-on: ubuntu-latest
    container:
      image: ghcr.io/n8group-oss/bb2gh:0
    env:
      BB_USERNAME: ${{ secrets.BB_USERNAME }}
      BB_API_TOKEN: ${{ secrets.BB_API_TOKEN }}
      GH_TOKEN: ${{ secrets.GH_TOKEN }}
    steps:
      - uses: actions/download-artifact@v4
        with:
          name: plan
      - name: Migrate
        run: bb2gh migrate --plan plan.yaml
      - uses: actions/upload-artifact@v4
        if: always()
        with:
          name: migration-state
          path: .bb2gh/
```

## GitLab CI

Use the Docker image in GitLab CI pipelines:

```yaml
# .gitlab-ci.yml

variables:
  BB_USERNAME: $BB_USERNAME
  BB_API_TOKEN: $BB_API_TOKEN
  GH_TOKEN: $GH_TOKEN

stages:
  - discover
  - plan
  - migrate
  - validate

discover:
  stage: discover
  image: ghcr.io/n8group-oss/bb2gh:latest
  script:
    - bb2gh discover --workspace $WORKSPACE
  artifacts:
    paths:
      - repos.json

plan:
  stage: plan
  image: ghcr.io/n8group-oss/bb2gh:latest
  script:
    - bb2gh plan --input repos.json
  artifacts:
    paths:
      - plan.yaml
  needs:
    - discover

migrate:
  stage: migrate
  image: ghcr.io/n8group-oss/bb2gh:latest
  script:
    - bb2gh migrate --plan plan.yaml
  artifacts:
    when: always
    paths:
      - .bb2gh/
  needs:
    - plan

validate:
  stage: validate
  image: ghcr.io/n8group-oss/bb2gh:latest
  script:
    - bb2gh validate --plan plan.yaml
  needs:
    - migrate
```

## Environment Variables

All bb2gh configuration can be passed via environment variables, which is the recommended approach for CI/CD:

| Variable | Description | Required |
|----------|-------------|----------|
| `BB_USERNAME` | Bitbucket username | Yes |
| `BB_API_TOKEN` | Bitbucket app password or API token | Yes |
| `GH_TOKEN` | GitHub personal access token or app token | Yes |
| `GH_BASE_URL` | GitHub Enterprise API URL | No (defaults to github.com) |
| `BB2GH_LOG_LEVEL` | Log verbosity: `debug`, `info`, `warning`, `error` | No (defaults to `info`) |
| `BB2GH_STATE_DIR` | Directory for state database | No (defaults to `.bb2gh`) |
| `BB2GH_NO_UPDATE_CHECK` | Set to `1` to disable update checks | No |

> **Warning**: Never hardcode credentials in pipeline files. Always use your CI platform's secrets management.

## Pinning Versions

For reproducible CI/CD pipelines, pin to a specific version or minor version:

```yaml
# Pin to exact version (most reproducible)
image: ghcr.io/n8group-oss/bb2gh:0.3.0

# Pin to minor (gets patch updates)
image: ghcr.io/n8group-oss/bb2gh:0.3

# Pin to major (gets minor + patch updates)
image: ghcr.io/n8group-oss/bb2gh:0
```

> **Tip**: Use the exact version tag for production pipelines and `latest` for testing.
