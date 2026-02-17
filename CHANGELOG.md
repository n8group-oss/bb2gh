## 0.1.0 (2026-01-26)

### Feat

- Initial project scaffolding
- CLI skeleton with Typer
- Bitbucket and GitHub adapter stubs
- Comprehensive test setup with pytest
- Code quality tools (Ruff, mypy, pre-commit)
- CI/CD pipelines with GitHub Actions
- Security scanning with CodeQL and Dependabot
- PR migration state tracking with `--include-prs` validation support
- High-fidelity PR migration with activity timeline preservation
- GEI mannequin export for author attribution

### Fix

- PR migration state tracking: Fixed FK constraint violation that prevented PR records from being stored in state database
- LFS detection: Fixed validation to use GitHub API for accurate LFS detection
- GitHub token fallback: Added `gh auth token` fallback when GH_TOKEN not set

## v0.5.4 (2026-02-17)

### Fix

- pre-cutover hygiene — URL, Docker naming, license reference

## v0.5.3 (2026-02-13)

### Refactor

- **licensing**: consolidation, tests, and audit [N8-279] (#42)

## v0.5.2 (2026-02-13)

### Fix

- **licensing**: wire license checks into all CLI commands [N8-278] (#41)

## v0.5.1 (2026-02-13)

### Fix

- **licensing**: security foundation — keypair separation, allowlist, hardening [N8-277] (#40)

## v0.5.0 (2026-02-13)

### Feat

- **licensing**: implement three-tier licensing system [N8-135]

## v0.4.1 (2026-02-12)

### Fix

- **ssl**: auto-detect system CA bundle for PostHog SDK connectivity (#38)

## v0.4.0 (2026-02-12)

### Feat

- **docker**: multi-arch builds, semantic tags, and CI/CD docs [N8-182] (#37)

## v0.3.0 (2026-02-12)

### Feat

- **telemetry**: wire PostHog events into all CLI commands (#36)

## v0.2.2 (2026-02-12)

### Fix

- **ci**: make release pipeline PyPI-ready (#35)

## v0.2.1 (2026-02-12)

### Fix

- **ci**: use git tag comparison instead of action output for release trigger (#34)

## v0.2.0 (2026-02-12)

### Feat

- **auth**: add credential management and profile system [N8-268] (#29)
- **config**: add SSL CA bundle support for corporate proxies (#30)
- **telemetry**: enrich migration events with detailed metrics (#27)
- **telemetry**: integrate PostHog EU with official SDK [N8-167] (#25)
- **branch-protection**: complete branch protection migration system [N8-250] (#26)
- **rollback**: add progress UI, webhook notifications, and granular rollback [N8-100]
- **validation**: add comment count and attribution validation [N8-101]
- **pr-migration**: reviewer-author filter, BB label parsing, merge commit tests [N8-97] (#24)
- **versioning**: add commitizen for automated version management (#18)

### Fix

- **ci**: remove pre_bump_hooks from commitizen config (#33)
- **ci**: replace PAT with GITHUB_TOKEN in bump-version workflow (#32)
- **models**: replace deprecated class Config with ConfigDict
- **ci**: resolve all lint, type-check, and security workflow failures [N8-225] (#23)

## v0.1.0 (2026-02-09)

### Feat

- **identity**: add IdP-aware 5-stage identity resolution engine (#17)
- **identity**: add identity source adapters for SCIM, SAML, Org API, git email
- add AI-native development infrastructure
- **config**: add app_private_key_file support for GitHub App auth
- **prs**: add state database tracking for PR migrations
- **cli**: add 'users export-mannequins' command for GEI mapping
- **mannequin**: add MannequinService for GEI user mapping export
- **gei**: add source_id to users for mannequin mapping support
- **migration**: add activity timeline to PR description body
- **migration**: integrate activity migration into PR migration flow
- **services**: add PRActivityService for migrating PR activities
- **adapter**: add list_pr_activity to fetch PR activity log from Bitbucket
- **models**: add PRActivity and PRActivityType for activity tracking
- implement dual PR migration with GEI for Enterprise and Issue fallback
- add PR migration and LFS validation enhancements
- add migrations list command to view all migration runs
- add --auto-resume flag for automatic migration resumption
- improve progress display with real-time streaming and ETA
- enable deep analysis by default in discover command
- implement Phase 3 non-enterprise features (E3.2, E3.7, E3.8)
- **licensing**: implement E3.6 Licensing foundation
- **secrets**: implement E3.1 Secrets Management
- **phase2**: implement PR Migration (E2.1-E2.6)
- **validation**: implement E1.8 Basic Validation
- **state**: implement E1.7 State Management
- **cli**: implement E1.5 Planning Command (#6)
- **services**: implement E1.6 Git Migration service and CLI
- **cli**: implement E1.4 Discovery Command with complexity scoring
- **adapters**: implement E1.2 Bitbucket and E1.3 GitHub adapters
- **cli**: implement E1.1 CLI framework and E1.2 adapter interfaces
- **core**: initialize Python project structure with Hatch and CLI skeleton

### Fix

- stop hook should ignore untracked files
- **ci**: fix Trivy version tag, gitleaks license, and PR regex
- resolve FK constraint violation in PR migration state tracking
- activity timeline in PR description and API pagelen bug
- **validation**: add LFS detection via API with proper authentication
- remove verbose stack trace from validation exit
- handle closed PRs with missing branches by creating Issues
- resolve LFS authentication for Bitbucket and GitHub
- show proper LFS progress with object counts during migration
- add --rename option to target conflict error message
- prevent traceback dump when plan validation fails
- map branch_count and has_lfs from inventory to plan items
- resolve API response handling bugs in PR migration
- add target repo collision check and validation fixes
- **ci**: add .trivyignore to exclude config files from secret scanning
- **ci**: update security workflow for repos without Advanced Security
- **build**: use license file reference for non-SPDX license
- **docs**: install package for API docs generation
- **legal**: replace MIT with BSL 1.1 license and add CLA
