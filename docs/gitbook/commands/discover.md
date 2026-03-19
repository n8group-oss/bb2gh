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
| `--output FILE` | Custom output file for the inventory JSON. When omitted, discovery writes to the workspace bundle directory. |
| `--include PATTERN` | Include repositories matching pattern |
| `--exclude PATTERN` | Exclude repositories matching pattern |
| `--project TEXT` | Filter by Bitbucket project key |
| `--format FORMAT` | Output format: json, yaml (default: json) |
| `--report / --no-report` | Generate an HTML discovery report (default: enabled) |
| `--report-path FILE` | Custom path for the HTML report file |
| `--excel / --no-excel` | Generate an Excel discovery workbook (default: enabled) |
| `--excel-path FILE` | Custom path for the Excel workbook file |

## Examples

```bash
# Scan entire workspace
bb2gh discover --workspace my-company

# Filter by project
bb2gh discover --workspace my-company --project CORE

# Filter by pattern
bb2gh discover --workspace my-company \
  --include "backend-*" \
  --exclude "*-deprecated"

# Skip HTML report generation
bb2gh discover --workspace my-company --no-report

# Custom report output path
bb2gh discover --workspace my-company --report-path ./reports/discovery.html

# Skip Excel workbook generation
bb2gh discover --workspace my-company --no-excel

# Custom Excel output path
bb2gh discover --workspace my-company --excel-path ./reports/discovery.xlsx
```

## Output

`discover` now produces three deliverables by default:

- `.bb2gh/reports/<workspace>/inventory.json`
- `.bb2gh/reports/<workspace>/discovery-report.html`
- `.bb2gh/reports/<workspace>/discovery-report.xlsx`

If `--project` is used, the default outputs are grouped one level deeper:

- `.bb2gh/reports/<workspace>/<project-slug>/inventory.json`
- `.bb2gh/reports/<workspace>/<project-slug>/discovery-report.html`
- `.bb2gh/reports/<workspace>/<project-slug>/discovery-report.xlsx`

This keeps repeated discoveries for different workspaces or project-filtered runs from overwriting each other.

At the start of each run, the CLI prints the resolved bundle paths:

- output directory
- inventory JSON path
- HTML report path
- Excel workbook path

If you override only one file with `--output`, `--report-path`, or `--excel-path`, the other deliverables keep using the default workspace bundle paths.

The inventory file contains:

- Repository metadata (name, size, language)
- Branch and tag counts
- LFS status and objects
- Open pull requests
- Migration complexity assessment
- Workspace user count summary when available from the source adapter

### HTML Discovery Report

By default, `discover` also generates a self-contained HTML dashboard at `.bb2gh/reports/<workspace>/discovery-report.html`. The report includes:

- **Summary cards** — total repositories, size, workspace user count, complexity breakdown, LFS/large file counts
- **Charts** — complexity distribution, pipeline migration complexity, project breakdown, size distribution
- **Projects section** — derived Bitbucket project rollups with repository, visibility, size, and warning totals
- **Sortable table** — all repositories with search, filtering by project/complexity/pipeline status, and pagination
- **Warnings panel** — explicit repository warnings captured during discovery analysis
- **Provenance links** — the exact `bb2gh` version plus product and GitHub repository links

The report is a single HTML file with no external dependencies — it works offline and can be shared with stakeholders directly. See the [Discovery Report Guide](../guides/discovery-report.md) for details on interpreting the dashboard.
When discovery runs with `--no-analyze`, the HTML report still renders repository metadata but leaves analysis-derived fields blank and shows a notice that deep analysis was skipped.

### Excel Discovery Workbook

By default, `discover` also generates an Excel workbook at `.bb2gh/reports/<workspace>/discovery-report.xlsx`.

The workbook contains four sheets:

- **Summary** — an ADO-style branded summary sheet with metadata, discovery totals, provenance hyperlinks, and an embedded project rollup table
- **Projects** — derived Bitbucket project rollups with human-readable total sizes
- **Repositories** — one row per discovered repository with migration-relevant fields, including exact `Size Bytes` and readable `Size`
- **Warnings** — one row per explicit warning or follow-up item

The HTML report and Excel workbook use the same internal projection, so project rollups and provenance links stay aligned across both deliverables. The workbook styling matches the ADO2GH presentation approach with branded summary rows, styled section blocks, wrapped cells, freeze panes, tab colors, and semantic fills for complexity and warning severity.
When discovery runs with `--no-analyze`, the workbook leaves analysis-derived cells blank instead of showing implicit zero/default values.

See [Plan Command](plan.md) for using the inventory.
