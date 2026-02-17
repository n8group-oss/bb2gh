# bb2gh

[![Documentation](https://img.shields.io/badge/docs-GitBook-blue.svg)](https://n8-group.gitbook.io/bb2gh/)
[![License: BSL-1.1](https://img.shields.io/badge/License-BSL--1.1-blue.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)

**Bitbucket to GitHub migration tool** — Migrate repositories with full metadata preservation including Pull Requests, comments, user attribution, and secrets.

## Features

- **Terraform-inspired workflow**: `discover` → `plan` → `migrate` → `validate`
- **Full metadata preservation**: Git history, branches, tags, PRs, comments, user attribution
- **LFS support**: Automatic detection and migration of LFS objects
- **Secrets migration**: Assisted secrets migration via Infisical integration
- **Enterprise ready**: Supports GitHub Enterprise Cloud, Data Residency, and Enterprise Server
- **Resilient**: Checkpoint/resume capability, rollback options

## Requirements

- Python >= 3.11
- Git and git-lfs available in PATH

## Installation

```bash
# Using pipx (recommended for CLI tools)
pipx install bb2gh

# Using pip
pip install bb2gh

# Using Docker
docker pull ghcr.io/n8group-oss/bb2gh:latest
```

## Setup

### Option 1: Interactive login (recommended)

```bash
# Install with keyring support
pip install bb2gh[secure]

# Run interactive setup — prompts for Bitbucket and GitHub credentials
bb2gh auth login

# Verify your setup
bb2gh auth status
```

### Option 2: Environment variables (CI/CD)

```bash
# Bitbucket — create an API token at:
# https://id.atlassian.com/manage-profile/security/api-tokens
export BB_USERNAME=your-username
export BB_API_TOKEN=your-api-token

# GitHub — create a fine-grained PAT at:
# https://github.com/settings/personal-access-tokens/new
export GH_TOKEN=ghp_your-token
```

### Required permissions

**Bitbucket API token scopes**: `repository:read`, `pullrequest:read`

**GitHub PAT permissions**: Contents (write), Pull requests (write), Administration (write), Metadata (read)

## Quick Start

```bash
# 1. Discover your Bitbucket workspace
bb2gh discover --workspace my-company --output inventory.json

# 2. Generate a migration plan
bb2gh plan --inventory inventory.json --target-org my-gh-org --output plan.json

# 3. Execute the migration
bb2gh migrate --plan plan.json

# 4. Validate the migration
bb2gh validate --migration mig_xxx
```

## Documentation

Full documentation is available at **[n8-group.gitbook.io/bb2gh](https://n8-group.gitbook.io/bb2gh/)**

- [Getting Started Guide](https://n8-group.gitbook.io/bb2gh/getting-started/installation)
- [Command Reference](https://n8-group.gitbook.io/bb2gh/commands)
- [Configuration Reference](https://n8-group.gitbook.io/bb2gh/getting-started/configuration)
- [User Mapping Guide](https://n8-group.gitbook.io/bb2gh/guides/user-mapping)
- [Enterprise Features](https://n8-group.gitbook.io/bb2gh/guides/enterprise)

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for release history.

## Reporting Issues

- **Bug reports**: Use the [bug report template](https://github.com/n8group-oss/bb2gh/issues/new?template=bug_report.yml)
- **Feature requests**: Use the [feature request template](https://github.com/n8group-oss/bb2gh/issues/new?template=feature_request.yml)
- **Security vulnerabilities**: See [SECURITY.md](SECURITY.md) for responsible disclosure

## Contributing

Contributions are welcome! Please read our [Contributing Guide](CONTRIBUTING.md) before getting started.

## License

Business Source License 1.1 — see [LICENSE](LICENSE) for details.

The license allows free use for any purpose except offering a competing migration service. After 4 years from each release, that version converts to Apache 2.0.
