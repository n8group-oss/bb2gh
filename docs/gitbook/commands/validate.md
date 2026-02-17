# validate

Verify a migration completed successfully.

## Usage

```bash
bb2gh validate [OPTIONS]
```

## Options

| Option | Description |
|--------|-------------|
| `--migration ID` | Migration ID to validate (required) |
| `--repo NAME` | Validate only specified repository |
| `--strict` | Fail on any warning |
| `--output FILE` | Save validation report |

## Examples

```bash
# Validate migration
bb2gh validate --migration mig_abc123

# Validate single repository
bb2gh validate --migration mig_abc123 --repo backend-api

# Generate report
bb2gh validate --migration mig_abc123 --output report.json
```

## Validation Checks

bb2gh validates:

- **Commits** -- All commits present in GitHub
- **Branches** -- All branches created
- **Tags** -- All tags pushed
- **Pull Requests** -- PRs migrated with comments
- **User Attribution** -- Commit authors mapped correctly
- **LFS Objects** -- Large files transferred

## Output

```
Validation Report for mig_abc123
================================

backend-api
  Commits:      1,234 / 1,234
  Branches:     12 / 12
  Tags:         45 / 45
  Pull Requests: 89 / 89

frontend-web
  Commits:      5,678 / 5,678
  Branches:     8 / 8
  Tags:         23 / 23
  Pull Requests: 156 / 158  <- 2 PRs failed
```
