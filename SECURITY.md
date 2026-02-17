# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 0.x.x   | :white_check_mark: |

## Reporting a Vulnerability

We take security vulnerabilities seriously. If you discover a security issue in bb2gh,
please report it responsibly.

### How to Report

**DO NOT** create a public GitHub issue for security vulnerabilities.

Instead, please report security vulnerabilities by emailing:

**security@n8group.com**

Include the following information in your report:

1. **Description**: A clear description of the vulnerability
2. **Steps to Reproduce**: Detailed steps to reproduce the issue
3. **Impact**: The potential impact of the vulnerability
4. **Affected Versions**: Which versions are affected
5. **Suggested Fix**: If you have one (optional)

### What to Expect

- **Acknowledgment**: We will acknowledge receipt of your report within 48 hours
- **Initial Assessment**: We will provide an initial assessment within 7 days
- **Updates**: We will keep you informed of our progress
- **Resolution**: We aim to resolve critical vulnerabilities within 30 days

### Disclosure Policy

- We follow responsible disclosure practices
- We will coordinate with you on the disclosure timeline
- We will credit you in the security advisory (unless you prefer to remain anonymous)

## Security Best Practices

When using bb2gh, follow these security best practices:

### Credentials

- **Never** commit credentials to version control
- Use environment variables or secure secret managers for tokens
- Rotate API tokens regularly
- Use the minimum required permissions for API tokens

### Configuration

- Keep bb2gh updated to the latest version
- Review migration plans before execution
- Use the `--dry-run` flag to preview changes
- Enable audit logging in enterprise deployments

### Secrets Migration

- Use Infisical or similar vault solutions for secrets
- Never store secrets in plain text
- Verify secret migration completeness
- Rotate secrets after migration

### Network Security

- Use HTTPS for all API communications (enforced by default)
- Consider network isolation for large migrations
- Use VPN or private networks for sensitive migrations

## Security Features

bb2gh includes several security features:

- **TLS 1.3**: All API communications use TLS 1.3
- **No Credential Logging**: Credentials are never logged or stored in state files
- **Secure Deletion**: Temporary files are securely deleted after use
- **Encrypted Storage**: Optional encrypted temp storage (paid tiers)
- **Audit Trail**: Complete audit logging for compliance

## Known Security Considerations

### State Files

Migration state files do not contain credentials but may contain:
- Repository names and metadata
- User mappings (usernames/emails)
- Migration progress and status

Treat state files as sensitive and store them securely.

### Temporary Files

During migration, temporary git clones are created. These are:
- Stored in system temp directory by default
- Automatically deleted after migration
- Can be configured to use encrypted storage (paid tiers)

## Compliance

bb2gh is designed to support compliance with:
- SOC 2
- GDPR (data residency support)
- HIPAA (with appropriate configuration)

Contact us for enterprise compliance requirements.
