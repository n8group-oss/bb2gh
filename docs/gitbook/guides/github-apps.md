# GitHub App Authentication

GitHub Apps provide the recommended authentication method for production migrations, offering:

- **Higher rate limits** - 15,000 requests/hour vs 5,000 for PATs
- **Granular permissions** - Least privilege access
- **No user dependency** - App tokens don't expire when users leave
- **Multi-app scaling** - Multiple apps for parallel workers (Enterprise)

## Quick Comparison

| Feature | Personal Access Token | GitHub App | Multi-App |
|---------|----------------------|------------|-----------|
| Rate limit | 5,000/hour | 15,000/hour | 15,000/hour x N apps |
| Setup complexity | Simple | Moderate | Advanced |
| Permission scope | User-level | Repository/Org | Repository/Org |
| Ideal for | Testing, small migrations | Production | Enterprise scale |

## Creating a GitHub App

### Step 1: Create the App

1. Go to your organization: `https://github.com/organizations/YOUR-ORG/settings/apps`
2. Click **New GitHub App**
3. Fill in the details:

| Field | Value |
|-------|-------|
| App name | `bb2gh-migration` (or your choice) |
| Homepage URL | `https://github.com/n8group/bb2gh` |
| Webhook | Uncheck "Active" (not needed) |

### Step 2: Configure Permissions

Under **Repository permissions**:

| Permission | Access | Why |
|------------|--------|-----|
| Contents | Read and write | Push git history |
| Pull requests | Read and write | Create/update PRs |
| Issues | Read and write | Create migrated PRs as issues |
| Metadata | Read-only | Required for API access |
| Administration | Read and write | Create repositories |

Under **Organization permissions**:

| Permission | Access | Why |
|------------|--------|-----|
| Members | Read-only | User mapping |

### Step 3: Generate Private Key

1. After creating the app, scroll to **Private keys**
2. Click **Generate a private key**
3. Save the downloaded `.pem` file securely:
   ```bash
   mkdir -p ~/.bb2gh
   mv ~/Downloads/your-app.*.private-key.pem ~/.bb2gh/github-app.pem
   chmod 600 ~/.bb2gh/github-app.pem
   ```

### Step 4: Install the App

1. Go to your app's page: `https://github.com/apps/YOUR-APP-NAME`
2. Click **Install App**
3. Select your target organization
4. Choose **All repositories** or select specific ones
5. Note the **Installation ID** from the URL after install:
   `https://github.com/organizations/YOUR-ORG/settings/installations/INSTALLATION_ID`

### Step 5: Note Your Credentials

You now have three values needed for configuration:

| Credential | Where to find |
|------------|---------------|
| App ID | App settings page -> App ID |
| Private Key | Downloaded `.pem` file |
| Installation ID | URL after installing the app |

## Configuration

### Environment Variables

```bash
# GitHub App Authentication
export GH_APP_ID=12345
export GH_APP_PRIVATE_KEY_FILE=~/.bb2gh/github-app.pem
export GH_APP_INSTALLATION_ID=67890
export GH_ORG=your-target-org
```

Or provide the key directly (useful for CI/CD):

```bash
export GH_APP_ID=12345
export GH_APP_PRIVATE_KEY="-----BEGIN RSA PRIVATE KEY-----
...
-----END RSA PRIVATE KEY-----"
export GH_APP_INSTALLATION_ID=67890
```

### Config File

Create `~/.bb2gh/config.yaml`:

```yaml
github:
  # Single GitHub App
  app_id: 12345
  app_private_key_file: ~/.bb2gh/github-app.pem
  installation_id: 67890
  organization: your-target-org
```

## Multi-App Configuration (Enterprise)

For large-scale migrations with parallel workers, configure multiple GitHub Apps to multiply your rate limits.

### Why Multi-App?

Each GitHub App has independent rate limits. With 4 apps and `--workers 4`:

- **Total rate limit**: 60,000 requests/hour (4 x 15,000)
- **Parallel throughput**: 4x faster migrations
- **Automatic failover**: If one app hits limits, others continue

### Setup

1. Create multiple GitHub Apps (e.g., `bb2gh-migration-1`, `bb2gh-migration-2`)
2. Install each app on the target organization
3. Configure in `~/.bb2gh/config.yaml`:

```yaml
github:
  organization: your-target-org

  # Multi-app configuration for parallel workers
  apps:
    - name: migration-app-1
      app_id: 11111
      private_key_file: ~/.bb2gh/app1.pem
      installation_id: 10001

    - name: migration-app-2
      app_id: 22222
      private_key_file: ~/.bb2gh/app2.pem
      installation_id: 20002

    - name: migration-app-3
      app_id: 33333
      private_key_file: ~/.bb2gh/app3.pem
      installation_id: 30003

    - name: migration-app-4
      app_id: 44444
      private_key_file: ~/.bb2gh/app4.pem
      installation_id: 40004
```

### Usage

```bash
# Parallel migration with 4 workers (one per app)
bb2gh migrate --workers 4

# Check rate limit status across all apps
bb2gh status --rate-limits
```

### Load Distribution

bb2gh automatically:
- **Round-robins** requests across apps
- **Detects rate limits** and falls back to other apps
- **Tracks** remaining quota per app
- **Reports** which app handles each operation (in DEBUG mode)

## Verifying Setup

Test your GitHub App configuration:

```bash
# Verify credentials
bb2gh auth verify

# Check rate limits
bb2gh auth rate-limit
```

Expected output for App auth:
```
GitHub authentication verified
  Type: GitHub App
  App ID: 12345
  Installation: 67890
  Rate limit: 15000/hour (14832 remaining)
```

## Troubleshooting

### "Bad credentials" Error

- Verify the App ID is correct (not Installation ID)
- Check the private key file is readable: `cat ~/.bb2gh/github-app.pem | head -1`
- Ensure the key hasn't been regenerated (re-download if needed)

### "Resource not accessible by integration" Error

- The app doesn't have required permissions
- Re-check permissions in App settings
- Ensure the app is installed on the target organization

### "Installation not found" Error

- The Installation ID is incorrect
- The app was uninstalled from the organization
- Visit the app's installation page to get the correct ID

### Rate Limit Hit Despite Multi-App

- Check that all apps are configured correctly
- Verify each app is installed on the organization
- Use `bb2gh status --rate-limits` to see per-app status

## GitHub Enterprise Server

For GitHub Enterprise Server, add the API URL:

```yaml
github:
  base_url: https://github.mycompany.com/api/v3
  app_id: 12345
  app_private_key_file: ~/.bb2gh/github-app.pem
  installation_id: 67890
```

## CI/CD Integration

### GitHub Actions

```yaml
jobs:
  migrate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup bb2gh
        run: pip install bb2gh

      - name: Run migration
        env:
          BB_USERNAME: ${{ secrets.BB_USERNAME }}
          BB_API_TOKEN: ${{ secrets.BB_API_TOKEN }}
          GH_APP_ID: ${{ secrets.GH_APP_ID }}
          GH_APP_PRIVATE_KEY: ${{ secrets.GH_APP_PRIVATE_KEY }}
          GH_APP_INSTALLATION_ID: ${{ secrets.GH_APP_INSTALLATION_ID }}
        run: |
          bb2gh migrate --plan migration-plan.json
```

### GitLab CI

```yaml
migrate:
  image: python:3.11
  script:
    - pip install bb2gh
    - bb2gh migrate --plan migration-plan.json
  variables:
    BB_USERNAME: ${BB_USERNAME}
    BB_API_TOKEN: ${BB_API_TOKEN}
    GH_APP_ID: ${GH_APP_ID}
    GH_APP_PRIVATE_KEY: ${GH_APP_PRIVATE_KEY}
    GH_APP_INSTALLATION_ID: ${GH_APP_INSTALLATION_ID}
```

## Next Steps

- [Getting Started](../getting-started/quickstart.md) - Run your first migration
- [Enterprise Features](enterprise.md) - Distributed workers and compliance
- [Configuration Reference](../getting-started/configuration.md) - All options
