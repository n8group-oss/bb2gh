# Plans & Features

bb2gh offers three plans to match your migration needs.

## Plan Overview

- **Free** — For small teams migrating up to 50 repositories. All core migration features included.
- **Pro** — For teams that need faster migrations with parallel workers.
- **Ultimate** — For enterprise-scale migrations with distributed workers, secrets management, and compliance reporting.

## Feature Comparison

| Feature | Free | Pro | Ultimate |
|---------|:----:|:---:|:--------:|
| **Core Migration** | | | |
| Repository discovery | Yes | Yes | Yes |
| Migration planning | Yes | Yes | Yes |
| Git history, branches, tags | Yes | Yes | Yes |
| Pull request migration | Yes | Yes | Yes |
| PR comments & reviews | Yes | Yes | Yes |
| LFS object migration | Yes | Yes | Yes |
| Rollback | Yes | Yes | Yes |
| Post-migration validation | Yes | Yes | Yes |
| **Performance** | | | |
| Parallel workers | - | Up to 4 | Unlimited |
| Distributed workers (Redis) | - | - | Yes |
| **Enterprise** | | | |
| Batch wave execution | - | - | Yes |
| Secrets migration (Infisical) | - | - | Yes |
| Compliance reports (PDF) | - | - | Yes |
| Repository cleanup tools | - | - | Yes |

## Limits

| Limit | Free | Pro | Ultimate |
|-------|:----:|:---:|:--------:|
| Repositories per migration | 50 | 50-2,000 (select plan) | Custom |
| Concurrent workers | 1 | 4 | Unlimited |

## Getting a License

### Free

Register directly from the CLI:

```bash
bb2gh license register --email you@company.com
```

Check your email for the license key and activate it:

```bash
bb2gh license activate BB2GH-1-...
```

### Pro

Visit [bb2gh.dev/#pricing](https://bb2gh.dev/#pricing) to select your repository count and purchase a Pro license. Breakpoints from 50 to 2,000 repositories are available.

Need more than 2,000 repos or a custom plan? Contact [sales@n8-group.com](mailto:sales@n8-group.com).

### Ultimate

Contact [sales@n8-group.com](mailto:sales@n8-group.com) for Ultimate licensing. Include:

- Your organization name
- Expected number of repositories
- Migration timeline

## Expired Licenses

When a license expires, bb2gh falls back to Free plan limits automatically. Your migrations continue to work within Free plan boundaries (50 repositories, 1 worker). To restore your full plan, renew your license or register for a new one.

## Checking Your Plan

View your current plan and enabled features:

```bash
bb2gh license status
```

This shows your tier, repository limit, worker count, expiration date, and a checklist of all features.
