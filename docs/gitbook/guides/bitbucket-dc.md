# Bitbucket Data Center Migration

bb2gh supports migrating from Bitbucket Data Center (7.x and 8.x) in addition to Bitbucket Cloud.

> **Prerequisite:** Bitbucket DC support requires an active bb2gh license. Run `bb2gh license register` before proceeding.

## Authentication

DC uses Personal Access Tokens (PAT) instead of API tokens or OAuth.

### Create a PAT

1. Log in to your DC instance
2. Navigate to **Manage account > Personal access tokens**
   (or visit `https://<your-dc-server>/plugins/servlet/access-tokens/manage`)
3. Create a token with permissions:
   - **Repository Read** (required)
   - **Pull Request Read** (required for PR migration)

### Configure credentials

**Option A: Environment variables (recommended for CI)**

```bash
export BB_DC_TOKEN=your-pat-token
export BB_DC_URL=https://bitbucket.mycompany.com
# Optional: export BB_DC_SSL_VERIFY=false  # or path to CA bundle
```

**Option B: Interactive login**

```bash
bb2gh auth login
# Select "bitbucket-dc" as source type
# Enter your DC base URL and PAT
```

**Option C: Quick auth (DC only)**

```bash
bb2gh auth dc --url https://bitbucket.mycompany.com
# Prompts for PAT, verifies, and stores credentials
```

## Usage

All standard bb2gh commands work with DC sources:

```bash
# Discover repositories
bb2gh discover -w PROJECT_KEY -o inventory.json --source bitbucket-dc

# Plan migration
bb2gh plan -i inventory.json -o plan.json

# Migrate PRs
bb2gh prs migrate --source-repo PROJ/repo --target-repo org/repo
```

## DC vs Cloud differences

| Feature | Cloud | DC |
|---------|-------|----|
| Auth | API token, OAuth2 | PAT only |
| Repo identifier | `workspace/repo` | `PROJECT_KEY/repo` |
| Large files API | Available | Not available (returns empty) |
| LFS detection | Via API | Reads `.gitattributes` |
| PR state: SUPERSEDED | Supported | Not supported (skipped) |
| Webhook-based events | Yes | Limited |

## SSL and Corporate Proxies

If your DC instance uses a self-signed certificate or is behind a corporate proxy:

```bash
# Skip SSL verification (not recommended for production)
bb2gh auth dc --url https://bitbucket.mycompany.com --insecure

# Use custom CA bundle
export BB_DC_SSL_VERIFY=/path/to/ca-bundle.pem
```

See the [SSL certificates guide](ssl-certificates.md) for detailed proxy configuration.

## Version requirements

- Bitbucket DC 7.x or 8.x
- REST API v1.0 (latest) endpoints
