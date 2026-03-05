# discover

Scan a Bitbucket workspace and create an inventory of repositories.

## Usage

```bash
bb2gh discover [OPTIONS]
```

## Options

| Option | Description |
|--------|-------------|
| `--workspace TEXT` | Bitbucket workspace to scan (required) |
| `--output FILE` | Output file for inventory (default: inventory.json) |
| `--include PATTERN` | Include repositories matching pattern |
| `--exclude PATTERN` | Exclude repositories matching pattern |
| `--project TEXT` | Filter by Bitbucket project key |
| `--format FORMAT` | Output format: json, yaml (default: json) |
| `--report / --no-report` | Generate an HTML discovery report (default: enabled) |
| `--report-path FILE` | Custom path for the HTML report file |

## Examples

```bash
# Scan entire workspace
bb2gh discover --workspace my-company --output inventory.json

# Filter by project
bb2gh discover --workspace my-company --project CORE --project PLATFORM

# Filter by pattern
bb2gh discover --workspace my-company \
  --include "backend-*" \
  --exclude "*-deprecated"

# Skip HTML report generation
bb2gh discover --workspace my-company --no-report

# Custom report output path
bb2gh discover --workspace my-company --report-path ./reports/discovery.html
```

## Output

The inventory file contains:

- Repository metadata (name, size, language)
- Branch and tag counts
- LFS status and objects
- Open pull requests
- Migration complexity assessment

### HTML Discovery Report

By default, `discover` also generates a self-contained HTML dashboard at `.bb2gh/reports/discovery-report.html`. The report includes:

- **Summary cards** — total repositories, size, complexity breakdown, LFS/large file counts
- **Charts** — complexity distribution, pipeline migration complexity, project breakdown, size distribution
- **Sortable table** — all repositories with search, filtering by project/complexity/pipeline status, and pagination
- **Warnings panel** — flagged issues like large files, LFS usage, high pipeline complexity, archived repos

The report is a single HTML file with no external dependencies — it works offline and can be shared with stakeholders directly. See the [Discovery Report Guide](../guides/discovery-report.md) for details on interpreting the dashboard.

See [Plan Command](plan.md) for using the inventory.
