# plan

Generate a migration plan from an inventory file.

## Usage

```bash
bb2gh plan [OPTIONS]
```

## Options

| Option | Description |
|--------|-------------|
| `--inventory FILE` | Inventory file from discover (required) |
| `--target-org TEXT` | GitHub organization name (required) |
| `--user-mapping FILE` | CSV file mapping Bitbucket users to GitHub |
| `--output FILE` | Output file for plan (default: plan.json) |
| `--max-complexity LEVEL` | Skip repos above complexity level |
| `--max-size-gb NUMBER` | Skip repos larger than size |
| `--dry-run` | Validate plan without saving |

## Examples

```bash
# Basic plan
bb2gh plan \
  --inventory inventory.json \
  --target-org my-github-org \
  --output plan.json

# With user mapping
bb2gh plan \
  --inventory inventory.json \
  --target-org my-github-org \
  --user-mapping users.csv \
  --output plan.json

# Filter complex repositories
bb2gh plan \
  --inventory inventory.json \
  --target-org my-github-org \
  --max-complexity medium \
  --max-size-gb 5
```

## User Mapping File

Create a CSV file mapping Bitbucket users to GitHub:

```csv
bitbucket_username,github_username,email
jsmith,john-smith,john@company.com
mjones,mary-jones,mary@company.com
```

See [User Mapping Guide](../guides/user-mapping.md) for details.
