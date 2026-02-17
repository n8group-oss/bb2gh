# rollback

Revert a failed or unwanted migration.

## Usage

```bash
bb2gh rollback [OPTIONS]
```

## Options

| Option | Description |
|--------|-------------|
| `--migration ID` | Migration ID to rollback (required) |
| `--repo NAME` | Rollback only specified repository |
| `--confirm` | Skip confirmation prompt |
| `--keep-repos` | Keep GitHub repos but reset state |

## Examples

```bash
# Rollback entire migration
bb2gh rollback --migration mig_abc123

# Rollback single repository
bb2gh rollback --migration mig_abc123 --repo backend-api

# Skip confirmation
bb2gh rollback --migration mig_abc123 --confirm
```

## What Gets Rolled Back

1. **GitHub repositories** -- Deleted (unless `--keep-repos`)
2. **Migration state** -- Reset to allow re-migration
3. **Checkpoints** -- Cleared

> **warning: Rollback is Destructive**
> Rollback deletes the migrated GitHub repositories. Make sure no one is using them before proceeding.

## Partial Rollback

To rollback only specific repositories while keeping others:

```bash
# Rollback only failed repo
bb2gh rollback --migration mig_abc123 --repo frontend-web

# Then resume migration
bb2gh migrate --plan plan.json --resume
```

## After Rollback

After rollback, you can:

1. Fix the issue that caused failure
2. Update the migration plan
3. Re-run migration with `bb2gh migrate --plan plan.json`
