# Secrets Migration

Securely migrate pipeline secrets from Bitbucket to GitHub.

> **warning: Security First**
> bb2gh **never** stores or transmits actual secret values. We generate migration checklists and scaffold empty secrets that teams populate manually.

## Overview

Bitbucket Pipelines uses:

- **Repository variables** -- Per-repo secrets
- **Workspace variables** -- Shared across repos
- **Deployment variables** -- Environment-specific

GitHub Actions uses:

- **Repository secrets** -- Per-repo secrets
- **Organization secrets** -- Shared with visibility controls
- **Environment secrets** -- Deployment environment specific

## Discovery

bb2gh discovers configured secrets (names only):

```bash
bb2gh discover --workspace my-company --include-secrets
```

Output includes secret names:

```json
{
  "name": "backend-api",
  "secrets": {
    "repository": ["API_KEY", "DATABASE_URL"],
    "workspace": ["DOCKER_PASSWORD", "NPM_TOKEN"],
    "deployments": {
      "production": ["PROD_API_KEY"],
      "staging": ["STAGING_API_KEY"]
    }
  }
}
```

## Migration Workflow

### 1. Generate Secret Manifest

```bash
bb2gh secrets manifest --inventory inventory.json --output secrets.yaml
```

Creates a YAML file listing all secrets to create:

```yaml
repositories:
  backend-api:
    secrets:
      - name: API_KEY
        source: repository
      - name: DATABASE_URL
        source: repository
    environments:
      production:
        - name: PROD_API_KEY
```

### 2. Create Empty Secrets

```bash
bb2gh secrets scaffold --manifest secrets.yaml --target-org my-org
```

This creates empty secrets in GitHub that teams must populate.

### 3. Manual Population

Teams retrieve values from:

- Existing Bitbucket UI
- Vault/secrets manager
- Secure documentation

## Enterprise: Infisical Integration

For enterprises, use Infisical as an intermediary:

```bash
# Sync from Bitbucket to Infisical (admin action)
bb2gh secrets sync-to-infisical \
  --workspace my-company \
  --infisical-project migrations

# Sync from Infisical to GitHub
bb2gh secrets sync-from-infisical \
  --infisical-project migrations \
  --github-org my-org
```

See [Enterprise Features](enterprise.md) for details.
