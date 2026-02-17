# bb2gh

**Bitbucket to GitHub migration tool** — Migrate repositories with full metadata preservation including Pull Requests, comments, user attribution, and secrets.

- **Get Started in 5 Minutes**

    Install bb2gh and run your first migration with a simple four-step workflow.

    [Getting started](getting-started/installation.md)

- **Full Git History**

    Preserve complete Git history including branches, tags, and all commits with proper attribution.

    [Learn more](guides/index.md)

- **PR & Review Preservation**

    Migrate Pull Requests with all comments, reviews, and approval history intact.

    [PR Migration](guides/index.md)

- **Enterprise Ready**

    Support for GitHub Enterprise Cloud, Data Residency, and Enterprise Server deployments.

    [Enterprise](guides/enterprise.md)

## Why bb2gh?

Moving from Bitbucket to GitHub is more than just pushing code. You need to preserve:

- **Pull Request history** — All PRs, comments, and reviews
- **User attribution** — Map Bitbucket users to GitHub accounts
- **Branch protections** — Convert Bitbucket restrictions to GitHub rules
- **Secrets** — Migrate pipeline variables securely
- **LFS objects** — Handle large files correctly

bb2gh handles all of this with a **Terraform-inspired workflow**:

```bash
# 1. Discover what you have
bb2gh discover --workspace my-company --output inventory.json

# 2. Plan the migration (review before executing)
bb2gh plan --inventory inventory.json --target-org my-gh-org --output plan.json

# 3. Execute with confidence
bb2gh migrate --plan plan.json

# 4. Verify everything worked
bb2gh validate --migration mig_xxx
```

## Quick Links

- [Installation Guide](getting-started/installation.md) — Get bb2gh installed on your system
- [Command Reference](commands/index.md) — Detailed documentation for all commands
- [User Mapping Guide](guides/user-mapping.md) — Configure user attribution
- [bb2gh.dev](https://bb2gh.dev) — Landing page & overview

## Contributing

Want to contribute? See the [Contributing Guide](https://github.com/n8group-oss/bb2gh/blob/main/CONTRIBUTING.md) on GitHub.

## Licensing

bb2gh requires a free license to operate. Register in seconds — no credit card required:

```bash
bb2gh license register --email you@company.com
```

See [Licensing](getting-started/licensing.md) for setup details and [Plans & Features](guides/plans-and-features.md) for plan comparison.

## Source License

bb2gh is licensed under the [Business Source License 1.1](https://github.com/n8group-oss/bb2gh/blob/main/LICENSE). You can use it freely for any purpose except offering a competing migration service. After 4 years from each release, that version converts to Apache 2.0.
