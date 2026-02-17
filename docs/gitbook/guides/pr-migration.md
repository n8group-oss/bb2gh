# PR Migration Guide

Migrate pull requests from Bitbucket to GitHub with high-fidelity preservation.

## Overview

bb2gh supports high-fidelity PR migration from Bitbucket to GitHub, preserving:

- PR metadata (title, description, branches)
- Author attribution (via user mapping)
- All comments and review discussions
- Activity timeline (approvals, updates, state changes)
- Original timestamps

## Prerequisites

Set the required environment variables:

```bash
export BB_API_TOKEN="your-bitbucket-app-password"
export BB_USERNAME="your-bitbucket-username"
export GH_TOKEN="your-github-token"
```

## Commands

### Migrate Open PRs

Migrate currently open PRs from Bitbucket to GitHub:

```bash
bb2gh prs migrate workspace/repo org/repo
```

Options:

- `--user-mapping, -u` - Path to user mapping CSV for attribution
- `--dry-run` - Preview without creating PRs

### Migrate Closed PRs

Migrate closed/merged PRs for historical record:

```bash
bb2gh prs migrate-closed workspace/repo org/repo
```

Options:

- `--user-mapping, -u` - Path to user mapping CSV for attribution
- `--since` - Only migrate PRs updated after this date (ISO format)
- `--dry-run` - Preview without creating PRs

### Migrate All PRs

Batch migrate PRs using a migration plan file:

```bash
bb2gh prs migrate-all --plan plan.yaml --user-mapping mapping.csv
```

## User Mapping for Attribution

To preserve author attribution, first export users and create a mapping:

```bash
# Export Bitbucket users
bb2gh users export bitbucket --workspace your-workspace

# Export GitHub users
bb2gh users export github --org your-org

# Generate mapping
bb2gh users map users-bb-*.csv users-gh-*.csv --output mapping.csv
```

Then use the mapping during migration:

```bash
bb2gh prs migrate workspace/repo org/repo --user-mapping mapping.csv
```

## Mannequin Mapping (GitHub Enterprise)

For GitHub Enterprise with GEI, export mannequin mapping:

```bash
bb2gh users export-mannequins your-workspace --output mannequins.csv
```

Fill in the `target-user` column, then run:

```bash
gh gei reclaim-mannequin --csv mannequins.csv --github-target-org your-org
```

## Activity Timeline

Migrated PRs include an activity timeline in the description showing:

| Time | User | Action |
|------|------|--------|
| 2024-01-15 10:30 | John Doe | Commented |
| 2024-01-15 14:00 | Jane Doe | Approved |

## Limitations

- PR creator cannot be changed via GitHub REST API (author shown in attribution header)
- Inline code review comments become general comments
- Draft PR status is preserved for open PRs only
- Closed PRs with missing branches are migrated as GitHub Issues
