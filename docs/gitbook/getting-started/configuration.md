# Configuration

bb2gh can be configured through environment variables, config files, or command-line options.

## Configuration Hierarchy

Settings are loaded in order of precedence (highest first):

1. Command-line arguments
2. Environment variables
3. OS keychain (for secrets, via profiles)
4. Config file (`~/.bb2gh/config.yaml`)
5. Default values

## Setting Up Credentials

For detailed authentication setup, see the dedicated [Authentication](authentication.md) guide. Quick options:

```bash
# Recommended: interactive setup (stores secrets in OS keychain)
bb2gh auth login

# Alternative: environment variables
export BB_USERNAME=your-username
export BB_API_TOKEN=your-api-token
export GH_TOKEN=ghp_your-token
```

## Config File

The config file lives at `~/.bb2gh/config.yaml`. Create it with:

```bash
bb2gh config init
```

Or run `bb2gh auth login` which creates it automatically.

### Profile-based configuration

Profiles let you store separate settings for different Bitbucket workspaces or GitHub organizations:

```yaml
# ~/.bb2gh/config.yaml

# Default profile used when --profile is not specified
default_profile: default

profiles:
  default:
    source:
      type: bitbucket-cloud
      username: your-username
      workspace: my-company
      auth_method: api-token          # or oauth2
      # base_url: https://api.bitbucket.org/2.0
    target:
      type: github-cloud              # or github-server, github-cloud-dr
      organization: my-github-org
      auth_method: pat                # or app
      # base_url: https://api.github.com

  production:
    source:
      type: bitbucket-cloud
      username: prod-service-account
      workspace: prod-workspace
      auth_method: api-token
    target:
      type: github-cloud
      organization: prod-github-org
      auth_method: app
      app_id: 12345
      installation_id: 67890
      app_private_key_file: ~/.bb2gh/prod-app.pem
```

> **Note**: Secrets (tokens, passwords, private keys) are **never** stored in the config file. They go into the OS keychain via `bb2gh auth login` or are read from environment variables. See [Authentication](authentication.md) for details.

### Legacy flat configuration

The older flat format still works for backward compatibility:

```yaml
bitbucket:
  username: your-username
  workspace: my-company

github:
  organization: my-github-org

logging:
  level: INFO
  format: console
```

Profile-based configuration takes precedence over flat configuration when both are present.

### GitHub App configuration (profile)

For GitHub App auth via profiles:

```yaml
profiles:
  my-profile:
    target:
      type: github-cloud
      auth_method: app
      app_id: 12345
      installation_id: 67890
      app_private_key_file: ~/.bb2gh/github-app.pem
      organization: my-org
```

### Multi-App configuration (enterprise)

For parallel workers with maximum throughput:

```yaml
github:
  apps:
    - name: app-1
      app_id: 11111
      private_key_file: ~/.bb2gh/app1.pem
      installation_id: 10001
    - name: app-2
      app_id: 22222
      private_key_file: ~/.bb2gh/app2.pem
      installation_id: 20002
```

See [GitHub Apps Guide](../guides/github-apps.md#multi-app-configuration) for details.

## Environment Variables

### Bitbucket

| Variable | Description | Default |
|----------|-------------|---------|
| `BB_USERNAME` | Bitbucket username | — |
| `BB_API_TOKEN` | API token (replaces deprecated app passwords) | — |
| `BB_CLIENT_ID` | OAuth2 client ID | — |
| `BB_CLIENT_SECRET` | OAuth2 client secret | — |
| `BB_WORKSPACE` | Default workspace | — |
| `BB_API_URL` | API base URL | `https://api.bitbucket.org/2.0` |

Aliases: `BITBUCKET_USERNAME`, `BITBUCKET_API_TOKEN`, `BITBUCKET_APP_PASSWORD`, `BITBUCKET_CLIENT_ID`, `BITBUCKET_CLIENT_SECRET`

> **Warning**: `BB_APP_PASSWORD` and `BITBUCKET_APP_PASSWORD` still work but map to the same field as `BB_API_TOKEN`. Bitbucket App Passwords are deprecated and will stop working in June 2026.

### GitHub

| Variable | Description | Default |
|----------|-------------|---------|
| `GH_TOKEN` | Personal access token | — |
| `GH_APP_ID` | GitHub App ID | — |
| `GH_APP_PRIVATE_KEY` | Private key content (PEM format) | — |
| `GH_APP_PRIVATE_KEY_FILE` | Path to private key file | — |
| `GH_APP_INSTALLATION_ID` | App installation ID | — |
| `GH_ORG` | Default target organization | — |
| `GH_API_URL` | API base URL | `https://api.github.com` |

Alias: `GITHUB_TOKEN` (for `GH_TOKEN`)

### General

| Variable | Description | Default |
|----------|-------------|---------|
| `BB2GH_LOG_LEVEL` | Logging level (DEBUG, INFO, WARNING, ERROR) | `INFO` |
| `BB2GH_CONFIG_FILE` | Path to config file | `~/.bb2gh/config.yaml` |
| `BB2GH_STATE_DIR` | Directory for migration state | `~/.bb2gh/state` |

## Migration Settings

```yaml
migration:
  state_dir: ~/.bb2gh/state
  parallel_repos: 4
  retry_attempts: 3

logging:
  level: INFO
  format: console            # or json
  file: ~/.bb2gh/bb2gh.log   # optional log file
```

## Next Steps

- [Authentication](authentication.md) — Detailed credential setup
- [Quick Start](quickstart.md) — Run your first migration
- [Command Reference](../commands/README.md) — Detailed command options
