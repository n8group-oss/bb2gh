# Troubleshooting Guide

Common issues and their solutions when using bb2gh.

## Authentication Issues

### Bitbucket Authentication Failed (401)

**Symptom**: `401 Unauthorized` when running discover or migrate.

**Solution**:

1. Verify your Bitbucket credentials. bb2gh supports two authentication methods:

   **App Password** (recommended):
   ```bash
   export BB_USERNAME="your-username"
   export BB_APP_PASSWORD="your-app-password"
   ```

   **API Token** (alternative — same as App Password, different variable name):
   ```bash
   export BB_USERNAME="your-username"
   export BB_API_TOKEN="your-app-password"
   ```

2. Ensure the App Password has required permissions:
   - **Account: Read** — required for credential verification (`/2.0/user` endpoint)
   - **Repositories: Read** — required for listing and cloning repositories
   - **Pull Requests: Read** — required for PR migration

   > **Common mistake**: Creating an App Password without **Account: Read** scope. This causes a `403 Forbidden` on credential verification (see below).

3. For Bitbucket Data Center, use personal access tokens:
   ```bash
   export BB_TOKEN="your-personal-access-token"
   ```

### Bitbucket Permission Denied (403)

**Symptom**: `403 Forbidden` on `https://api.bitbucket.org/2.0/user` during credential verification.

**Cause**: The App Password authenticates successfully but lacks the **Account: Read** scope needed for the `/2.0/user` endpoint.

**Solution**: Recreate the App Password with **Account: Read** scope included:

1. Go to **Bitbucket** > **Personal settings** > **App passwords**
2. Click **Create app password**
3. Select: **Account: Read**, **Repositories: Read**, **Pull requests: Read**
4. Copy the new password and update your `BB_APP_PASSWORD` or `BB_API_TOKEN`

### GitHub Authentication Failed

**Symptom**: `401 Unauthorized` or `403 Forbidden` on GitHub operations.

**Solution**:

1. Create a GitHub Personal Access Token (classic) with scopes:
   - `repo` (full control)
   - `admin:org` (for organization operations)
   - `workflow` (if migrating Actions)

2. Set the token:
   ```bash
   export GH_TOKEN="ghp_xxxxxxxxxxxx"
   ```

3. For GitHub Enterprise Server:
   ```bash
   export GH_ENTERPRISE_URL="https://github.mycompany.com"
   ```

## Rate Limiting

### Bitbucket Rate Limit Exceeded

**Symptom**: `429 Too Many Requests` errors.

**Solution**:

1. bb2gh automatically handles rate limiting with exponential backoff
2. For large migrations, use `--delay` to add delays between operations:
   ```bash
   bb2gh migrate --plan plan.json --delay 1000  # 1 second between repos
   ```

### GitHub Rate Limit Exceeded

**Symptom**: `403` with "rate limit exceeded" message.

**Solution**:

1. Check your current rate limit:
   ```bash
   curl -H "Authorization: token $GH_TOKEN" https://api.github.com/rate_limit
   ```

2. For authenticated requests, you get 5000 requests/hour
3. Use `--delay` for large migrations
4. Enterprise Server users: contact your admin about rate limits

## Repository Migration Issues

### LFS Objects Not Migrating

**Symptom**: LFS pointers remain after migration.

**Solution**:

1. Ensure `git-lfs` is installed:
   ```bash
   git lfs version
   ```

2. Verify LFS is enabled in your config:
   ```yaml
   # bb2gh.yaml
   migration:
     include_lfs: true
   ```

3. Check LFS storage quota on GitHub

### Large Repository Timeout

**Symptom**: Migration times out for large repositories.

**Solution**:

1. Increase timeout in config:
   ```yaml
   # bb2gh.yaml
   migration:
     timeout_seconds: 7200  # 2 hours
   ```

2. Use shallow clone for history-heavy repos:
   ```yaml
   migration:
     shallow_clone: true
     shallow_depth: 1000
   ```

### Repository Already Exists

**Symptom**: `Repository already exists` error.

**Solution**:

1. Use `--skip-existing` to skip:
   ```bash
   bb2gh migrate --plan plan.json --skip-existing
   ```

2. Or use `--overwrite` to replace (requires confirmation):
   ```bash
   bb2gh migrate --plan plan.json --overwrite
   ```

## Pull Request Migration Issues

### Missing PR Comments

**Symptom**: Some PR comments are not migrated.

**Solution**:

1. Ensure your tokens have read permissions for PR comments
2. Check if comments were made by deleted users
3. Review the migration log for specific errors

### User Attribution Incorrect

**Symptom**: PRs show wrong author or "ghost" user.

**Solution**:

1. Create a user mapping CSV:
   ```csv
   bitbucket_username,github_username
   john.doe,johndoe
   jane.smith,janesmith
   ```

2. Use the mapping:
   ```bash
   bb2gh migrate --plan plan.json --user-map users.csv
   ```

3. See [User Mapping Guide](user-mapping.md) for details

## State and Resume Issues

### Migration State Corrupted

**Symptom**: Cannot resume migration, state errors.

**Solution**:

1. View current state:
   ```bash
   bb2gh status --migration mig_xxx
   ```

2. Reset a specific repository:
   ```bash
   bb2gh migrate --plan plan.json --reset-repo my-repo
   ```

3. Full state reset (last resort):
   ```bash
   bb2gh migrate --plan plan.json --reset-state
   ```

### Cannot Resume After Error

**Symptom**: Migration won't resume from checkpoint.

**Solution**:

1. Check the migration ID:
   ```bash
   bb2gh status --list
   ```

2. Resume explicitly:
   ```bash
   bb2gh migrate --resume mig_xxx
   ```

3. If checkpoint is corrupted, reset the failed repo:
   ```bash
   bb2gh migrate --resume mig_xxx --reset-repo failed-repo-name
   ```

## Network Issues

### Connection Timeouts

**Symptom**: Frequent connection timeouts.

**Solution**:

1. Increase connection timeout:
   ```yaml
   # bb2gh.yaml
   network:
     connect_timeout: 30
     read_timeout: 60
   ```

2. Check proxy settings:
   ```bash
   export HTTPS_PROXY="http://proxy.company.com:8080"
   ```

### SSL Certificate Errors

**Symptom**: `SSL: CERTIFICATE_VERIFY_FAILED` or `unable to get local issuer certificate`.

**Common cause**: Running bb2gh in WSL2 behind a corporate HTTPS proxy (Zscaler, Netskope, etc.) that intercepts TLS traffic.

**Solution**: See the dedicated [SSL Certificate Troubleshooting](ssl-certificates.md) guide for step-by-step instructions.

**Quick fix** — install the proxy Root CA and set environment variables:

```bash
# After installing proxy CA into WSL2 system store (see SSL guide for details)
export SSL_CERT_FILE=/etc/ssl/certs/ca-certificates.crt
export REQUESTS_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt
```

### PostHog Telemetry SSL Errors

**Symptom**: `SSLError` messages mentioning `eu.i.posthog.com` in stderr while bb2gh runs.

```
error uploading: HTTPSConnectionPool(host='eu.i.posthog.com', port=443): Max retries exceeded
```

**Cause**: PostHog SDK uses the `requests` library which needs `REQUESTS_CA_BUNDLE` (not `SSL_CERT_FILE`) to trust the proxy CA.

**Solution**: `export REQUESTS_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt`

**Impact**: These errors are non-blocking. bb2gh migration and discovery work normally regardless. Only anonymous telemetry is affected.

See the [SSL Certificate Troubleshooting](ssl-certificates.md#posthog-telemetry-ssl-errors) guide for full details.

## License Issues

### No License Found

**Symptom**: `No license found. Register for a free license: bb2gh license register`

**Solution**:

1. Register for a free license:
   ```bash
   bb2gh license register --email you@company.com
   ```

2. Check your email for the license key

3. Activate the license:
   ```bash
   bb2gh license activate BB2GH-1-...
   ```

4. For CI/CD, set the environment variable instead:
   ```bash
   export BB2GH_LICENSE="BB2GH-1-..."
   ```

### License Signature Invalid

**Symptom**: `License signature is invalid. Your license may be corrupted or tampered with.`

**Solution**:

1. Verify you copied the full license key (it starts with `BB2GH-1-` and can be long)
2. Check for extra whitespace or line breaks in the key
3. Re-download the license key from your original email
4. If the issue persists, contact [support](https://github.com/n8group-oss/bb2gh/issues)

### License Format Invalid

**Symptom**: `License format is invalid. Check that you copied the full license key.`

**Solution**:

1. Ensure the key starts with `BB2GH-1-`
2. Check that the key was not truncated during copy/paste
3. If using a key file, verify it contains only the key with no extra characters

### License Expired

**Symptom**: `License has expired.` or features are limited to Free plan.

**Solution**:

1. Check your current license status:
   ```bash
   bb2gh license status
   ```

2. Register for a new free license:
   ```bash
   bb2gh license register --email you@company.com
   ```

3. For Pro/Ultimate renewals, contact [sales@n8-group.com](mailto:sales@n8-group.com)

> **Note**: Expired licenses automatically fall back to Free plan limits (100 repositories, 1 worker). Your existing migrations are not affected.

### Feature Requires Pro or Ultimate

**Symptom**: `Feature '<name>' requires Pro or Ultimate tier.`

**Solution**:

1. Check which features your plan includes:
   ```bash
   bb2gh license status
   ```

2. See [Plans & Features](plans-and-features.md) for a comparison of what each plan offers

3. Contact [sales@n8-group.com](mailto:sales@n8-group.com) to upgrade

### Repository Limit Exceeded

**Symptom**: `Repository limit exceeded: N repositories requested but your plan allows M.`

**Solution**:

1. The Free plan allows up to 100 repositories per migration
2. Split your migration into batches of 100 or fewer
3. Upgrade to Pro or Ultimate for unlimited repositories — contact [sales@n8-group.com](mailto:sales@n8-group.com)

## Getting More Help

### Enable Verbose Logging

```bash
bb2gh migrate --plan plan.json --verbose
# or
bb2gh migrate --plan plan.json -vvv  # Even more detail
```

### Export Debug Logs

```bash
bb2gh migrate --plan plan.json --log-file debug.log --verbose
```

### Check Version

Ensure you're on the latest version:

```bash
bb2gh --version
pip install --upgrade bb2gh
```

### Report an Issue

If you've tried the above and still have issues:

1. Search [existing issues](https://github.com/n8group-oss/bb2gh/issues)
2. Open a [new issue](https://github.com/n8group-oss/bb2gh/issues/new/choose) with:
   - bb2gh version
   - Python version
   - Error message and logs (sanitized)
   - Steps to reproduce
