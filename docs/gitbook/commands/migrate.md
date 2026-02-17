# migrate

Execute a migration according to a plan.

## Usage

```bash
bb2gh migrate [OPTIONS]
```

## Options

| Option | Description |
|--------|-------------|
| `--plan FILE` | Migration plan file (required) |
| `--parallel NUMBER` | Repositories to migrate in parallel (default: 1) |
| `--resume` | Resume from last checkpoint |
| `--repo NAME` | Migrate only specified repository |
| `--skip-prs` | Skip pull request migration |
| `--skip-webhooks` | Skip webhook migration |

## Examples

```bash
# Execute migration
bb2gh migrate --plan plan.json

# Parallel migration
bb2gh migrate --plan plan.json --parallel 4

# Resume failed migration
bb2gh migrate --plan plan.json --resume

# Migrate single repository
bb2gh migrate --plan plan.json --repo backend-api
```

## Progress Tracking

During migration, bb2gh displays progress:

```
Migrating repositories...
  [1/10] backend-api        ████████████████████ 100% (2m 34s)
  [2/10] frontend-web       ████████████░░░░░░░░  60% (cloning...)
  [3/10] shared-lib         ░░░░░░░░░░░░░░░░░░░░   0% (pending)
```

## Checkpoints

bb2gh saves checkpoints automatically. If migration fails, use `--resume` to continue from the last successful repository.

See [Status Command](status.md) to check migration progress.
