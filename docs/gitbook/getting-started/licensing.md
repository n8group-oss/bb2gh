# Licensing

bb2gh requires a license to operate. A free license is available for small teams and individual use — no credit card required.

## Get Your Free License

Register for a free license in three steps:

### 1. Register

```bash
bb2gh license register --email you@company.com
```

### 2. Check Your Email

You will receive a license key at the email address you provided. The key looks like:

```
BB2GH-1-eyJ2Ijox...
```

### 3. Activate

```bash
bb2gh license activate BB2GH-1-eyJ2Ijox...
```

Your license is now stored at `~/.bb2gh/license` and bb2gh is ready to use.

## Verify Your License

Check your current license status at any time:

```bash
bb2gh license status
```

## CI/CD Environments

For automated pipelines, set the license key as an environment variable instead of activating it on disk:

```bash
export BB2GH_LICENSE="BB2GH-1-eyJ2Ijox..."
bb2gh migrate --plan plan.json
```

No file is written when using the environment variable.

## Plans

bb2gh offers three plans:

| | Free | Pro | Ultimate |
|---|---|---|---|
| Repositories | Up to 100 | Unlimited | Unlimited |
| Workers | 1 | Up to 4 | Unlimited |
| Enterprise features | - | - | Yes |

The free plan covers all core migration features. See [Plans & Features](../guides/plans-and-features.md) for a full comparison.

## Need More?

- **Pro** — Parallel workers for faster migrations
- **Ultimate** — Batch waves, secrets migration, distributed workers, compliance reports

Contact [sales@n8-group.com](mailto:sales@n8-group.com) for Pro and Ultimate licensing.

## Next Steps

- [Authentication](authentication.md) — Set up Bitbucket and GitHub credentials
- [Plans & Features](../guides/plans-and-features.md) — Full feature comparison
- [License Management](../guides/license-management.md) — Detailed license operations
