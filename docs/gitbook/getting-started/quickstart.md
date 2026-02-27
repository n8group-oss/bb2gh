# Quick Start

This guide walks you through your first migration from Bitbucket to GitHub.

## Prerequisites

Before you begin, ensure you have:

1. **bb2gh installed** — See [Installation](installation.md)
2. **License activated** — Register for a free license (see [Licensing](licensing.md))
3. **Bitbucket credentials** — API token (Cloud) or Personal Access Token (Data Center) with repository read access (see [Authentication](authentication.md))
4. **GitHub credentials** — Personal access token or GitHub App (see [Authentication](authentication.md))

## Step 1: Configure Authentication

The easiest way to set up credentials is the interactive login:

```bash
bb2gh auth login
```

This stores secrets in your OS keychain and saves configuration to `~/.bb2gh/config.yaml`. See [Authentication](authentication.md) for the full walkthrough.

Alternatively, use environment variables:

```bash
# Bitbucket credentials
export BB_USERNAME="your-bitbucket-username"
export BB_API_TOKEN="your-api-token"

# GitHub credentials
export GH_TOKEN="your-github-token"
```

> **Note**: Bitbucket App Passwords are deprecated and will stop working in June 2026. Use API tokens instead. See [Authentication > Bitbucket](authentication.md#bitbucket-authentication) for migration steps.

## Step 2: Discover Your Repositories

Scan your Bitbucket workspace to create an inventory:

```bash
bb2gh discover \
  --workspace my-company \
  --output inventory.json
```

This creates `inventory.json` with details about all repositories including:

- Repository metadata (size, branches, tags)
- LFS status
- Open pull requests
- Migration complexity assessment

## Step 3: Create a Migration Plan

Generate a migration plan:

```bash
bb2gh plan \
  --inventory inventory.json \
  --target-org my-github-org \
  --user-mapping users.csv \
  --output plan.json
```

Review the plan before executing:

```bash
# View plan summary
cat plan.json | jq '.summary'

# List repositories to be migrated
cat plan.json | jq '.repositories[].name'
```

## Step 4: Execute the Migration

Run the migration:

```bash
bb2gh migrate --plan plan.json
```

The migration will:

1. Clone each repository from Bitbucket
2. Push to GitHub with full history
3. Migrate pull requests and comments
4. Configure branch protections
5. Set up repository settings

## Step 5: Validate the Migration

Verify everything migrated correctly:

```bash
bb2gh validate --migration mig_xxx
```

This checks:

- Commit count matches
- Branches and tags present
- Pull requests migrated
- User attribution correct

## Migrating from Bitbucket Data Center?

If you're migrating from Bitbucket Data Center instead of Cloud, see the [Bitbucket DC Migration Guide](../guides/bitbucket-dc.md). The workflow is the same — just use `--source bitbucket-dc` with the `discover` command and authenticate with a PAT.

## Next Steps

- [Bitbucket DC Migration](../guides/bitbucket-dc.md) — Migrate from Bitbucket Data Center
- [User Mapping Guide](../guides/user-mapping.md) — Configure user attribution
- [LFS Migration](../guides/lfs-migration.md) — Handle large files
- [Command Reference](../commands/index.md) — Detailed command documentation
