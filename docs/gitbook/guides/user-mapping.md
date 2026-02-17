# User Mapping

Map Bitbucket users to GitHub accounts for proper commit attribution.

## Why User Mapping?

Git commits contain author information (name and email). When migrating:

- Commits keep their original author metadata
- GitHub links commits to accounts based on **verified email**
- Without mapping, commits may appear from "ghost" users

## Creating a Mapping File

Create a CSV file with Bitbucket to GitHub mappings:

```csv
bitbucket_username,github_username,email
jsmith,john-smith,john@company.com
mjones,mary-jones,mary@company.com
alee,alex-lee,alex@company.com
```

### Required Columns

| Column | Description |
|--------|-------------|
| `bitbucket_username` | Bitbucket username or UUID |
| `github_username` | GitHub username |
| `email` | Email (must be verified on GitHub) |

### Auto-generating Mappings

Generate a template from your inventory:

```bash
bb2gh users --inventory inventory.json --output users.csv
```

This creates a CSV with all Bitbucket users found. Fill in the GitHub usernames.

## Using the Mapping

Pass the mapping file to the plan command:

```bash
bb2gh plan \
  --inventory inventory.json \
  --target-org my-org \
  --user-mapping users.csv \
  --output plan.json
```

## Handling Unmapped Users

For users without GitHub accounts:

1. **Skip** -- Commits keep original email (appear as "ghost")
2. **Bot account** -- Map to a migration bot account
3. **Generic** -- Map to `team@company.com`

```csv
# Map former employee to bot
oldemployee,migration-bot,bot@company.com
```

## Email Verification

For commits to link correctly, users must:

1. Add email to GitHub account
2. Verify the email
3. Optionally set as primary

> **tip: Bulk verification**
> With GitHub Enterprise, admins can provision accounts with pre-verified emails via SCIM/SSO.
