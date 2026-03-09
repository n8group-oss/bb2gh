# Parallel Execution

Migrate multiple repositories concurrently to reduce total migration time.

## Overview

By default, bb2gh migrates repositories one at a time. For workspaces with many repositories, parallel execution can dramatically reduce total migration time by running multiple migrations concurrently.

```bash
# Migrate 4 repositories at a time
bb2gh migrate --plan plan.json --workers 4
```

Parallel execution uses asyncio tasks within a single process. All workers share the same API connections, credentials, and rate limits — no additional infrastructure is required.

## When to Use Parallel Workers

| Scenario | Recommended Workers |
|----------|-------------------|
| Testing or small migration (<10 repos) | 1 (default) |
| Medium migration (10-50 repos) | 2-4 |
| Large migration (50-200 repos) | 4-8 |
| Enterprise migration (200+ repos) | 8-16 with multi-app |

> **Note**: More workers does not always mean faster. The bottleneck is usually GitHub's API rate limit (5,000 requests/hour per app). Beyond 4 workers with a single GitHub App, you will likely hit rate limits. See [Scaling with Multiple GitHub Apps](#scaling-with-multiple-github-apps) below.

## How It Works

### Scheduling

When `--workers N` is specified (N > 1), bb2gh:

1. Filters out already-completed repositories (for resume support)
2. Sorts remaining repositories by size, **largest first**
3. Enqueues all repositories into a shared work queue
4. Spawns N asyncio worker tasks that pull from the queue
5. Each worker runs the full migration pipeline for one repository at a time

Largest-first scheduling (LPT) prevents the common problem where a single large repository delays completion while other workers sit idle at the end.

### Rate Limiting

All workers share the same GitHub adapter and its rate limits. bb2gh does not bypass rate limiting — if the API returns a rate limit response, the adapter backs off automatically and all workers wait.

| Setup | Rate Limit | Recommended Workers |
|-------|-----------|-------------------|
| 1 PAT | 5,000 req/hr | 1-2 |
| 1 GitHub App | 5,000 req/hr (REST) | 1-4 |
| 2 GitHub Apps | 10,000 req/hr | 4-8 |
| 4 GitHub Apps | 20,000 req/hr | 8-16 |

### Progress Tracking

In parallel mode, progress is calculated based on completion count rather than sequential index. This means the progress bar accurately reflects overall throughput even when repositories finish out of order.

Failed and skipped repositories are counted as processed — the progress bar will always reach 100% when all work is done.

## Checkpoint and Resume

Parallel execution supports the same checkpoint/resume as sequential mode. Each repository's status (pending, in-progress, completed, failed) is tracked independently in the state database.

If a migration is interrupted (Ctrl+C, crash, or `--stop-on-error`):

```bash
# Resume from where it left off — completed repos are skipped
bb2gh migrate --plan plan.json --workers 4 --auto-resume
```

Repositories that were in-progress when interrupted are retried on resume.

## Stop on Error

By default, parallel workers continue even if one repository fails. Use `--stop-on-error` to prevent new work from starting after a failure:

```bash
bb2gh migrate --plan plan.json --workers 4 --stop-on-error
```

> **Note**: `--stop-on-error` does not cancel repositories already in flight. Workers that have already started a migration will finish their current repository before stopping. Only the work queue is drained.

## Scaling with Multiple GitHub Apps

For migrations with more than 4 workers, configure multiple GitHub Apps to multiply your rate limits. Each GitHub App gets independent rate limits (5,000 req/hr REST, 15,000 req/hr for Apps), so N apps = N times the throughput.

### Setup

1. Create multiple GitHub Apps on your target organization (e.g., `bb2gh-migration-1`, `bb2gh-migration-2`)
2. Install each app on the target organization
3. Configure in `~/.bb2gh/config.yaml`:

```yaml
github:
  organization: your-target-org
  apps:
    - name: migration-app-1
      app_id: 11111
      private_key_file: ~/.bb2gh/app1.pem
      installation_id: 10001
    - name: migration-app-2
      app_id: 22222
      private_key_file: ~/.bb2gh/app2.pem
      installation_id: 20002
```

4. Run with matching worker count:

```bash
bb2gh migrate --plan plan.json --workers 4
```

When more than 4 workers are used, bb2gh displays a tip reminding you to add more GitHub Apps for better throughput.

See [GitHub Apps Guide](github-apps.md) for detailed setup instructions.

## License Requirements

Parallel worker count is capped by your license tier:

| Tier | Max Workers |
|------|------------|
| Free | 1 (sequential only) |
| Pro | Up to 4 |
| Ultimate | Unlimited |

If you request more workers than your tier allows, bb2gh silently caps the count and logs a warning. See [Plans & Features](plans-and-features.md) for plan details.

## Troubleshooting

### Migration is slow despite multiple workers

- **Check rate limits**: Use `bb2gh auth rate-limit` to see remaining quota. If you're near zero, add more GitHub Apps.
- **Large repositories**: A few very large repos may dominate migration time. This is expected — largest-first scheduling minimizes the impact.
- **Network bandwidth**: Parallel git clone/push operations share network bandwidth. On slow connections, more than 2-4 workers may not help.

### Some repositories failed but others succeeded

This is normal — parallel workers are isolated. Failed repositories can be retried:

```bash
bb2gh migrate --plan plan.json --workers 4 --auto-resume
```

### "workers must be >= 1" error

The `--workers` flag requires a positive integer. Minimum value is 1.

### Workers capped below requested count

Your license tier limits the maximum workers. Check your plan:

```bash
bb2gh license status
```

Upgrade to Pro (up to 4 workers) or Ultimate (unlimited) for higher parallelism.
