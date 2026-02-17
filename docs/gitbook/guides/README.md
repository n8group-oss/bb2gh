# Guides

In-depth guides for common migration scenarios.

## Migration Guides

- [GitHub Apps](github-apps.md) -- Setting up GitHub App authentication for production migrations
- [User Mapping](user-mapping.md) -- Map Bitbucket users to GitHub accounts
- [LFS Migration](lfs-migration.md) -- Handle Git LFS objects
- [Secrets Migration](secrets-migration.md) -- Migrate pipeline variables securely
- [Enterprise Features](enterprise.md) -- Advanced features for large organizations
- [Plans & Features](plans-and-features.md) -- Compare Free, Pro, and Ultimate plans
- [License Management](license-management.md) -- Register, activate, and manage your license

## Support

- [Troubleshooting](troubleshooting.md) -- Common issues and solutions

## Development Guides

- [Linear Workflow](linear-workflow.md) -- Project management and issue tracking integration

## Planning Your Migration

Before starting, consider:

1. **Scope** -- Which repositories to migrate?
2. **Timeline** -- When can teams switch over?
3. **User mapping** -- Who needs GitHub accounts?
4. **CI/CD** -- How to migrate pipelines?
5. **Secrets** -- How to handle credentials?

## Migration Checklist

- [ ] Create inventory with `bb2gh discover`
- [ ] Review repository complexity
- [ ] Prepare user mapping CSV
- [ ] Set up GitHub organization
- [ ] Configure authentication
- [ ] Test with a small repository
- [ ] Schedule migration window
- [ ] Notify affected teams
- [ ] Execute migration
- [ ] Validate results
- [ ] Update CI/CD pipelines
- [ ] Archive Bitbucket repos (optional)
