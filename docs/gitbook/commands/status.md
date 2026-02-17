# status

Check the status of a migration.

## Usage

```bash
bb2gh status [OPTIONS]
```

## Options

| Option | Description |
|--------|-------------|
| `--migration ID` | Migration ID to check |
| `--list` | List all migrations |
| `--watch` | Continuously update status |

## Examples

```bash
# Check specific migration
bb2gh status --migration mig_abc123

# List all migrations
bb2gh status --list

# Watch migration progress
bb2gh status --migration mig_abc123 --watch
```

## Output

```
Migration: mig_abc123
Started:   2026-01-26 10:30:00
Status:    In Progress

Repositories:
  backend-api       completed    2m 34s
  frontend-web      in_progress  1m 12s (cloning)
  shared-lib        pending
  data-pipeline     pending

Progress: 1/4 completed (25%)
Elapsed:  3m 46s
```

## Migration States

| State | Description |
|-------|-------------|
| `pending` | Not started |
| `in_progress` | Currently migrating |
| `completed` | Successfully migrated |
| `failed` | Migration failed |
| `rolled_back` | Reverted after failure |
