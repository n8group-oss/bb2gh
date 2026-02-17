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
```

## Output

The inventory file contains:

- Repository metadata (name, size, language)
- Branch and tag counts
- LFS status and objects
- Open pull requests
- Migration complexity assessment

See [Plan Command](plan.md) for using the inventory.
