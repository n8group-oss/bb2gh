# Enterprise Features

Advanced features for large-scale migrations.

## Overview

Enterprise features require:

```bash
pip install "bb2gh[enterprise]"
```

And a valid enterprise license key.

## Authentication for Scale

### GitHub App (Recommended)

For enterprise migrations, use GitHub App authentication:

```bash
export GH_APP_ID=12345
export GH_APP_PRIVATE_KEY_FILE=~/.bb2gh/github-app.pem
export GH_APP_INSTALLATION_ID=67890
```

Benefits:
- 3x higher rate limits (15,000/hour vs 5,000)
- No dependency on individual user accounts
- Granular repository permissions

See [GitHub Apps Guide](github-apps.md) for setup.

### Multi-App for Maximum Throughput

For large-scale migrations with parallel workers, configure multiple GitHub Apps:

```yaml
# ~/.bb2gh/config.yaml
github:
  apps:
    - name: migration-1
      app_id: 11111
      private_key_file: ~/.bb2gh/app1.pem
      installation_id: 10001
    - name: migration-2
      app_id: 22222
      private_key_file: ~/.bb2gh/app2.pem
      installation_id: 20002
    - name: migration-3
      app_id: 33333
      private_key_file: ~/.bb2gh/app3.pem
      installation_id: 30003
    - name: migration-4
      app_id: 44444
      private_key_file: ~/.bb2gh/app4.pem
      installation_id: 40004
```

Run with parallel workers:

```bash
bb2gh migrate --plan plan.json --workers 4
```

This gives you:
- **60,000 requests/hour** (4 x 15,000)
- **Automatic load balancing** across apps
- **Failover** if one app hits rate limits

## Distributed Migration

Migrate hundreds of repositories in parallel using Redis-based job distribution.

### Setup

```bash
# Start Redis (or use managed Redis)
docker run -d -p 6379:6379 redis:7

# Configure bb2gh
export BB2GH_REDIS_URL="redis://localhost:6379"
```

### Usage

```bash
# Start worker nodes (run on multiple machines)
bb2gh worker start --concurrency 4

# Submit migration job
bb2gh migrate --plan plan.json --distributed
```

### Monitoring

```bash
# View job queue status
bb2gh worker status

# View individual job progress
bb2gh status --migration mig_xxx --distributed
```

## Compliance Reporting

Generate detailed compliance reports for auditors.

```bash
bb2gh report compliance \
  --migration mig_xxx \
  --format pdf \
  --output compliance-report.pdf
```

Report includes:

- Complete audit trail
- User mapping verification
- Data integrity checksums
- Access control comparison

## Deep Validation

Enhanced validation for mission-critical repositories.

```bash
bb2gh validate --migration mig_xxx --deep
```

Checks:

- File content SHA comparison
- LFS object integrity
- PR comment threading
- Webhook payload compatibility

## GitHub Enterprise Support

### GitHub Enterprise Cloud

```bash
export GH_API_URL="https://api.github.com"
export GH_TOKEN="ghp_xxx"
```

### GitHub Enterprise Server

```bash
export GH_API_URL="https://github.mycompany.com/api/v3"
export GH_TOKEN="xxx"
```

### Data Residency (EU)

```bash
export GH_API_URL="https://api.github.eu"
```

## License Activation

Enterprise features require a Pro or Ultimate license. See [License Management](license-management.md) for activation instructions and [Plans & Features](plans-and-features.md) for a comparison of what each plan offers.

Contact [sales@n8-group.com](mailto:sales@n8-group.com) for enterprise licensing.
