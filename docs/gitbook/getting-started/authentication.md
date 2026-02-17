# Authentication

This guide covers all authentication options for bb2gh, from quick interactive setup to advanced CI/CD configuration.

## Quick Start: Interactive Login

The fastest way to get started is the interactive login command:

```bash
bb2gh auth login
```

This walks you through configuring both Bitbucket (source) and GitHub (target) credentials in a single flow. Secrets are stored securely in your OS keychain (macOS Keychain, Windows Credential Manager, or Linux Secret Service via `libsecret`).

> **Note**: To use keychain storage, install bb2gh with the `secure` extra:
> ```bash
> pip install bb2gh[secure]
> ```
> Without this, credentials must be provided via environment variables.

### What the login flow looks like

```
$ bb2gh auth login

Configuring profile: default

Source (Bitbucket)
Auth method [api-token/oauth2] (api-token):
Bitbucket username: your-username
Bitbucket app password / API token: ********
Default workspace (optional, press Enter to skip): my-company

Target (GitHub)
Auth method [pat/app] (pat):
GitHub personal access token: ********
Default GitHub organization (optional, press Enter to skip): my-github-org

ℹ Validating Bitbucket credentials...
✓ Bitbucket credentials valid!
ℹ Validating GitHub credentials...
✓ GitHub credentials valid!

✓ Profile 'default' configured successfully!
ℹ Secrets stored in OS keychain.
ℹ Config saved to /home/user/.bb2gh/config.yaml

Next steps:
  bb2gh auth status          # verify credentials
  bb2gh discover -w my-company  # discover repositories
```

### Verify your setup

After login, verify everything is configured:

```bash
bb2gh auth status
```

This displays a table showing each profile with credential health:

```
         Authentication Profiles
┌─────────┬─────────────────┬───────────┬─────────────┬──────────────┬────────────┬─────────────┐
│ Profile │ Source          │ Source    │ Source      │ Target       │ Target     │ Target      │
│         │                 │ Auth      │ Creds       │              │ Auth       │ Creds       │
├─────────┼─────────────────┼───────────┼─────────────┼──────────────┼────────────┼─────────────┤
│ default │ bitbucket-cloud │ api-token │     OK      │ github-cloud │ pat        │     OK      │
└─────────┴─────────────────┴───────────┴─────────────┴──────────────┴────────────┴─────────────┘
```

- **OK** — credentials found in keychain
- **MISSING** — secrets not stored; run `bb2gh auth login` or set environment variables
- **KEY FILE** — GitHub App auth configured; key file expected on disk

### Remove stored credentials

```bash
# Remove credentials for the default profile
bb2gh auth logout

# Remove credentials for a specific profile
bb2gh auth logout --profile production

# Remove credentials for all profiles
bb2gh auth logout --all
```

> **Note**: `auth logout` only removes secrets from the keychain. Profile configuration in `config.yaml` is preserved. Run `bb2gh auth login` to re-configure.

---

## Profiles: Per-Workspace Credential Scoping

Profiles let you store separate credentials for different Bitbucket workspaces or GitHub organizations. This is useful when migrating from multiple workspaces or to different target orgs.

### Creating named profiles

```bash
# Default profile (used when --profile is not specified)
bb2gh auth login

# Named profile for a specific workspace
bb2gh auth login --profile production

# Another profile for a different workspace
bb2gh auth login --profile staging
```

### Using profiles with commands

```bash
# Uses the default profile
bb2gh discover --workspace my-company

# Uses the production profile
bb2gh discover --workspace my-company --profile production
```

### How profiles are stored

Non-secret configuration is saved to `~/.bb2gh/config.yaml`:

```yaml
profiles:
  default:
    source:
      type: bitbucket-cloud
      username: your-username
      workspace: my-company
      auth_method: api-token
    target:
      type: github-cloud
      organization: my-github-org
      auth_method: pat
  production:
    source:
      type: bitbucket-cloud
      username: prod-user
      workspace: prod-workspace
      auth_method: api-token
    target:
      type: github-cloud
      organization: prod-github-org
      auth_method: pat
```

Secrets (tokens, passwords, keys) are stored in the OS keychain, keyed by profile name. They are **never** written to config files or logs.

---

## Credential Resolution Order

When bb2gh needs credentials, it checks multiple sources in this order:

1. **Environment variables** (highest priority) — always checked first
2. **OS keychain** (via profile) — checked if a profile is configured
3. **Profile config file** — non-secret fields only (username, org, workspace)

This means environment variables always override stored credentials, making it easy to use different credentials in CI/CD or for one-off runs.

---

## Bitbucket Authentication

### API Tokens (Recommended)

> **Warning**: Bitbucket App Passwords are deprecated. Atlassian is removing them in phases:
> - **September 2025**: No new app passwords can be created
> - **June 2026**: All existing app passwords stop working
>
> Migrate to API tokens now to avoid disruption.

API tokens use the same HTTP Basic authentication as app passwords, so no code changes are needed — just a new token.

**Creating an API token:**

1. Go to [Atlassian Account Settings](https://id.atlassian.com/manage-profile/security/api-tokens)
2. Click **API tokens** in the left sidebar
3. Click **Create API token with scopes**
4. Select **Bitbucket** as the application
5. Name your token (e.g., `bb2gh-migration`)
6. Assign the required scopes:

| Scope | Required | Purpose |
|-------|----------|---------|
| `repository:read` | Yes | Read repository metadata, clone repos |
| `pullrequest:read` | Yes | Read pull requests, comments, activity |
| `webhook:read` | Optional | Migrate webhook configurations |
| `account:read` | Optional | Read workspace member information |

7. Click **Create** and copy the token immediately (it won't be shown again)

**Using the token:**

```bash
# Interactive setup (stores in keychain)
bb2gh auth login
# → Select "api-token" auth method
# → Enter your Bitbucket username
# → Paste the API token when prompted

# Or via environment variables
export BB_USERNAME=your-username
export BB_API_TOKEN=your-api-token
```

### OAuth 2.0

For automated pipelines or when you need organization-level access without personal credentials.

1. Go to **Bitbucket Settings** → **OAuth consumers** → **Add consumer**
2. Set callback URL (can be `http://localhost` for CLI use)
3. Grant permissions: Repository Read, Pull Request Read
4. Note the **Key** (client ID) and **Secret** (client secret)

```bash
# Interactive setup
bb2gh auth login
# → Select "oauth2" auth method
# → Enter client ID and client secret

# Or via environment variables
export BB_CLIENT_ID=your-client-id
export BB_CLIENT_SECRET=your-client-secret
```

### Legacy: App Passwords

> **Warning**: App passwords are deprecated and will stop working in June 2026. Use API tokens instead.

If you still have app passwords, they continue to work with the `BB_API_TOKEN` variable (same HTTP Basic auth mechanism):

```bash
export BB_USERNAME=your-username
export BB_API_TOKEN=your-existing-app-password  # works until June 2026
```

To migrate: create an API token (see above) and replace your app password value. No other changes needed.

---

## GitHub Authentication

### Personal Access Token (PAT)

Best for getting started quickly and for small-to-medium migrations.

**Creating a fine-grained PAT:**

1. Go to [GitHub Settings → Developer settings → Fine-grained personal access tokens](https://github.com/settings/personal-access-tokens/new)
2. Set a descriptive name (e.g., `bb2gh-migration`)
3. Set expiration (recommend 90 days for migration projects)
4. Under **Resource owner**, select your target organization
5. Under **Repository access**, select "All repositories" (or specific ones)
6. Assign permissions:

| Permission | Access | Purpose |
|-----------|--------|---------|
| **Contents** | Read and write | Push repository content |
| **Pull requests** | Read and write | Create migrated pull requests |
| **Administration** | Read and write | Create repositories, set branch protections |
| **Metadata** | Read-only | Required (automatically selected) |
| **Workflows** | Read and write | Optional — only if migrating GitHub Actions |

7. Click **Generate token** and copy it immediately

**Using the token:**

```bash
# Interactive setup (stores in keychain)
bb2gh auth login
# → Select "pat" auth method
# → Paste token when prompted

# Or via environment variables (either name works)
export GH_TOKEN=ghp_your-token
# or
export GITHUB_TOKEN=ghp_your-token
```

### GitHub App (Recommended for Production)

GitHub Apps provide higher rate limits (5,000 → 15,000 requests/hour), granular permissions, and organization-level control. Recommended for large migrations.

See the dedicated [GitHub Apps Guide](../guides/github-apps.md) for detailed setup.

**Quick setup via CLI:**

```bash
bb2gh auth login
# → Select "app" auth method
# → Enter App ID, Installation ID, and path to private key PEM file
```

**Via environment variables:**

```bash
export GH_APP_ID=12345
export GH_APP_INSTALLATION_ID=67890

# Option A: Key file path
export GH_APP_PRIVATE_KEY_FILE=~/.bb2gh/github-app.pem

# Option B: Key content directly (useful in CI/CD)
export GH_APP_PRIVATE_KEY="-----BEGIN RSA PRIVATE KEY-----
MIIEpAIBA...
-----END RSA PRIVATE KEY-----"
```

### Multi-App (Enterprise Scale)

For maximum throughput with parallel workers, configure multiple GitHub Apps. Each worker uses a different App to maximize rate limits.

Configure in `~/.bb2gh/config.yaml`:

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

See [Multi-App Configuration](../guides/github-apps.md#multi-app-configuration) for details.

---

## CI/CD and Headless Environments

In CI/CD pipelines, Docker containers, or other non-interactive environments, use environment variables instead of the keychain.

### GitHub Actions example

```yaml
jobs:
  migrate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - run: pip install bb2gh

      - run: bb2gh discover --workspace my-company --output inventory.json
        env:
          BB_USERNAME: ${{ secrets.BB_USERNAME }}
          BB_API_TOKEN: ${{ secrets.BB_API_TOKEN }}

      - run: bb2gh migrate --plan plan.json
        env:
          BB_USERNAME: ${{ secrets.BB_USERNAME }}
          BB_API_TOKEN: ${{ secrets.BB_API_TOKEN }}
          GH_TOKEN: ${{ secrets.GH_MIGRATION_TOKEN }}
```

### Docker example

```bash
docker run --rm \
  -e BB_USERNAME=your-username \
  -e BB_API_TOKEN=your-token \
  -e GH_TOKEN=ghp_your-token \
  bb2gh discover --workspace my-company
```

### `.env` file

For local development or scripted runs, you can use a `.env` file:

```bash
# Copy the template
cp .env.example .env

# Edit with your values
vim .env

# Source it before running
source .env
bb2gh discover --workspace my-company
```

> **Warning**: Never commit `.env` files to version control. The `.gitignore` already excludes `.env`.

---

## Environment Variable Reference

### Bitbucket

| Variable | Description | Example |
|----------|-------------|---------|
| `BB_USERNAME` | Bitbucket username | `john-doe` |
| `BB_API_TOKEN` | API token (recommended) | `ATATT3xF...` |
| `BB_APP_PASSWORD` | App password (deprecated, alias for BB_API_TOKEN) | `aBcDeFgH...` |
| `BB_CLIENT_ID` | OAuth2 client ID | `aB1cD2eF3` |
| `BB_CLIENT_SECRET` | OAuth2 client secret | `xY9wV8uT7` |
| `BB_WORKSPACE` | Default workspace | `my-company` |
| `BB_API_URL` | API base URL | `https://api.bitbucket.org/2.0` |

Aliases are also accepted: `BITBUCKET_USERNAME`, `BITBUCKET_API_TOKEN`, `BITBUCKET_APP_PASSWORD`, `BITBUCKET_CLIENT_ID`, `BITBUCKET_CLIENT_SECRET`.

### GitHub

| Variable | Description | Example |
|----------|-------------|---------|
| `GH_TOKEN` | Personal access token | `ghp_xxxx...` |
| `GITHUB_TOKEN` | Alias for `GH_TOKEN` | `ghp_xxxx...` |
| `GH_APP_ID` | GitHub App ID | `12345` |
| `GH_APP_PRIVATE_KEY` | Private key content (PEM) | `-----BEGIN RSA...` |
| `GH_APP_PRIVATE_KEY_FILE` | Path to private key file | `~/.bb2gh/app.pem` |
| `GH_APP_INSTALLATION_ID` | App installation ID | `67890` |
| `GH_ORG` | Default target organization | `my-org` |
| `GH_API_URL` | API base URL | `https://api.github.com` |

### General

| Variable | Description | Default |
|----------|-------------|---------|
| `BB2GH_LOG_LEVEL` | Logging level | `INFO` |
| `BB2GH_CONFIG_FILE` | Config file path | `~/.bb2gh/config.yaml` |
| `BB2GH_STATE_DIR` | State directory | `~/.bb2gh/state` |

---

## Troubleshooting

### "No credentials found" error

Check your credential sources in order:

1. **Environment variables set?** — `echo $BB_API_TOKEN` / `echo $GH_TOKEN`
2. **Keychain has secrets?** — `bb2gh auth status`
3. **Profile configured?** — Check `~/.bb2gh/config.yaml`

### Keyring not available

If `bb2gh auth login` fails with a keyring error:

```bash
# Install the secure extra
pip install bb2gh[secure]

# On Linux, ensure a secret service is running (GNOME Keyring or KWallet)
# On headless Linux, use environment variables instead
```

### Bitbucket "401 Unauthorized"

- Verify your username matches your Atlassian account (not your display name)
- If using API tokens: ensure the token has the correct scopes and is for Bitbucket (not Jira/Confluence)
- If using app passwords: check if they've been disabled (Atlassian deprecation timeline)

### GitHub "403 Forbidden"

- For fine-grained PATs: ensure the token has access to the target organization
- For GitHub Apps: verify the installation ID matches the target organization
- Check token expiration date

### Migrating from app passwords to API tokens

1. Create an API token at [Atlassian Account Settings](https://id.atlassian.com/manage-profile/security/api-tokens)
2. Update your credentials:
   ```bash
   # If using environment variables, just change the value
   export BB_API_TOKEN=your-new-api-token

   # If using keychain, re-run login
   bb2gh auth login
   ```
3. The same `BB_USERNAME` works with both app passwords and API tokens

---

## Next Steps

- [Quick Start](quickstart.md) — Run your first migration
- [Configuration](configuration.md) — Config file reference
- [GitHub Apps Guide](../guides/github-apps.md) — Set up GitHub App authentication
