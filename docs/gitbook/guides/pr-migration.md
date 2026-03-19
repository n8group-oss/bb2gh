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

Closed PRs receive the same high-fidelity treatment as open PRs:

- **Activity timeline** included in the PR body
- **Comments** migrated as issue or review comments
- **Labels** applied automatically, including state labels (`migrated-pr`, `pr-merged`, `pr-declined`)
- **Reviewer info** recorded in the PR body with approval status

When a source branch no longer exists, closed PRs are created as **GitHub Issues** with a structured audit-friendly body containing full metadata (see [Historical Issue Fallback](#historical-issue-fallback) below).

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

## Historical Issue Fallback

When a closed PR's source branch no longer exists in GitHub, the PR cannot be recreated as a GitHub pull request. In this case, bb2gh creates a **GitHub Issue** as a structured historical record.

The issue body includes:

- **Header** with state, timestamps, and branch info
- **Author** with mapped GitHub username (when available)
- **Reviewer table** showing each reviewer and their approval status
- **Original description**
- **Activity timeline** (approvals, updates, state changes)
- **Comment summary** with count from the source system
- **Link** to the original Bitbucket PR

The issue is automatically closed and labeled with `migrated-pr` plus a state label (`pr-merged`, `pr-declined`, or `pr-superseded`).

> **Note**: The migration result tracks whether a PR was migrated as an actual PR or as an issue fallback via the `fallback_type` field (`pr`, `issue`, or `gei`).

## Limitations

- PR creator cannot be changed via GitHub REST API (author shown in attribution header)
- Inline code review comments become general comments
- Draft PR status is preserved for open PRs only
- Closed PRs with missing branches are migrated as GitHub Issues (see above)
