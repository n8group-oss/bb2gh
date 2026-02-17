# LFS Migration

Migrate Git Large File Storage (LFS) objects from Bitbucket to GitHub.

## Overview

Git LFS stores large files (binaries, assets, datasets) outside the Git repository. When migrating:

1. LFS pointer files are in Git history
2. Actual objects are stored in Bitbucket's LFS server
3. Objects must be transferred to GitHub's LFS server

## Detection

bb2gh automatically detects LFS during discovery:

```json
{
  "name": "assets-repo",
  "lfs": {
    "enabled": true,
    "objects_count": 1234,
    "total_size_mb": 5678
  }
}
```

## Migration Process

### Automatic Migration

bb2gh handles LFS migration automatically:

```bash
# LFS objects are migrated with the repository
bb2gh migrate --plan plan.json
```

### What Happens

1. Clone repository with `git lfs fetch --all`
2. Push to GitHub with `git lfs push --all`
3. Verify LFS objects transferred

## Storage Considerations

### GitHub LFS Quotas

| Plan | Storage | Bandwidth |
|------|---------|-----------|
| Free | 1 GB | 1 GB/month |
| Pro | 2 GB | 2 GB/month |
| Team | 2 GB | 4 GB/month |
| Enterprise | 50 GB | Unlimited |

Additional packs: $5/month for 50 GB storage + 50 GB bandwidth.

### Recommendations

- Check total LFS size before migration
- Purchase data packs if needed
- Consider splitting large repos

## Troubleshooting

### "LFS object not found"

The object may not have been fetched:

```bash
# Fetch all LFS objects manually
git lfs fetch --all origin

# Verify objects
git lfs ls-files
```

### Bandwidth Exceeded

If you hit bandwidth limits:

1. Wait for monthly reset
2. Purchase bandwidth packs
3. Migrate in smaller batches
