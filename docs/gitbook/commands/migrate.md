# migrate

Execute a migration according to a plan.

## Usage

```bash
bb2gh migrate [OPTIONS]
```

## Options

| Option | Description |
|--------|-------------|
| `--plan, -p FILE` | Migration plan file (required) |
| `--mode, -m TEXT` | Transfer mode: `mirror`, `branches-only`, or `main-only` (default: `mirror`) |
| `--workers, -w NUMBER` | Number of parallel workers (default: 1, minimum: 1) |
| `--resume ID` | Resume a failed migration by ID |
| `--auto-resume` | Automatically resume the latest incomplete migration for this plan |
| `--work-dir DIR` | Working directory for git operations (uses temp dir if not specified) |
| `--stop-on-error` | Stop migration on first error |
| `--dry-run` | Preview migration without making changes |
| `--with-prs` | Also migrate open PRs after each repository |
| `--user-mapping, -u FILE` | Path to user mapping CSV for PR attribution (used with `--with-prs`) |

## Examples

```bash
# Execute migration
bb2gh migrate --plan plan.json

# Parallel migration with 4 workers
bb2gh migrate --plan plan.json --workers 4

# Resume failed migration
bb2gh migrate --plan plan.json --auto-resume

# Resume a specific migration by ID
bb2gh migrate --plan plan.json --resume mig_abc123

# Dry run preview
bb2gh migrate --plan plan.json --dry-run

# Migrate single repository
bb2gh migrate --plan plan.json --repo backend-api

# Stop on first error
bb2gh migrate --plan plan.json --workers 4 --stop-on-error
```

## Parallel Execution

When `--workers` is greater than 1, bb2gh migrates multiple repositories concurrently using asyncio tasks within a single process.

```bash
bb2gh migrate --plan plan.json --workers 4
```

Parallel mode provides:

- **Largest-first scheduling** — Biggest repositories start first to avoid bottlenecks at the end
- **Shared rate limits** — All workers share the same API adapter, respecting GitHub rate limits
- **Checkpoint/resume** — Each repository's status is tracked independently in the state database
- **Stop-on-error** — With `--stop-on-error`, no new work is started after a failure (in-flight repos finish)

> **Note**: Worker count is capped by your license tier. Free allows 1 (sequential only), Pro allows up to 4, and Ultimate is unlimited. See [Plans & Features](../guides/plans-and-features.md).

When using more than 4 workers, bb2gh recommends configuring multiple GitHub Apps for higher rate limits. See the [Parallel Execution Guide](../guides/parallel-execution.md) for details.

## Progress Tracking

During migration, bb2gh displays a progress bar with ETA:

```
Migrating 10 repositories...
  backend-api: pushing to github   ████████████████░░░░  72%
```

Progress accounts for completed, skipped, and failed repositories to provide accurate percentage tracking.

## Checkpoints

bb2gh saves checkpoints automatically to an SQLite state database at `.bb2gh/state.db`. If migration fails or is interrupted, use `--auto-resume` to continue from where it left off:

```bash
bb2gh migrate --plan plan.json --auto-resume
```

Completed repositories are skipped on resume. This works for both sequential and parallel modes.

See [Status Command](status.md) to check migration progress.
