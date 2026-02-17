# SSL Certificate Troubleshooting

## Problem: `CERTIFICATE_VERIFY_FAILED` in WSL2 with Corporate Proxy

If you're running bb2gh inside WSL2 on a machine with a corporate HTTPS proxy (Zscaler, Netskope, Cisco Umbrella, Palo Alto, etc.), you'll see SSL certificate verification errors:

```
httpx.ConnectError: [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed:
  unable to get local issuer certificate (_ssl.c:1000)
```

or in PostHog telemetry output:

```
SSLError(SSLCertVerificationError(1, '[SSL: CERTIFICATE_VERIFY_FAILED] certificate
  verify failed: unable to get issuer certificate (_ssl.c:1000)')): /batch/
```

This affects all bb2gh operations that connect to Bitbucket, GitHub, or PostHog APIs.

## Why This Happens

The problem has four layers:

1. **Your corporate proxy intercepts HTTPS traffic** — Zscaler (and similar proxies) perform TLS inspection by replacing server certificates with ones signed by the proxy's own Root CA. On the Windows host, the proxy installer adds this CA to the Windows Certificate Store, so browsers trust it transparently.

2. **WSL2 has a separate certificate store** — WSL2 runs its own Linux instance with an independent certificate store (`/etc/ssl/certs/`). Microsoft has [not implemented automatic synchronization](https://github.com/microsoft/WSL/issues/5134) between the Windows and WSL2 certificate stores. This is an open issue since 2020.

3. **Hatch/linuxbrew Python uses its own OpenSSL** — bb2gh uses [Hatch](https://hatch.pypa.io/) as its build system, which installs Python via linuxbrew. This Python links against linuxbrew's own OpenSSL at `/home/linuxbrew/.linuxbrew/etc/openssl@3/cert.pem` — a path that is **not** updated by `sudo update-ca-certificates`. Even after installing your proxy's CA into the WSL2 system store, linuxbrew Python won't see it without the `SSL_CERT_FILE` environment variable.

4. **bb2gh and PostHog use different HTTP libraries** — bb2gh's API calls use **httpx** (respects `SSL_CERT_FILE`), while PostHog telemetry uses **requests** internally (respects `REQUESTS_CA_BUNDLE`). Both need separate environment variables pointing to a CA bundle that includes your proxy's certificate.

## Solution

### Step 1: Export the Proxy Root CA from Windows

**Option A — PowerShell (recommended)**

Open PowerShell **on Windows** and run:

```powershell
# Find your proxy's root certificate (replace "Zscaler" with your proxy name)
Get-ChildItem -Path Cert:\LocalMachine\Root\ | Where-Object {
    $_.Issuer -like "*Zscaler*"
} | ForEach-Object {
    $pemContent = "-----BEGIN CERTIFICATE-----`n"
    $pemContent += [System.Convert]::ToBase64String($_.RawData, 'InsertLineBreaks')
    $pemContent += "`n-----END CERTIFICATE-----"
    $pemContent | Out-File -FilePath "$env:USERPROFILE\proxy-root-ca.pem" -Encoding ASCII
    Write-Host "Exported: $($_.Subject)"
}
```

> **Tip**: If you're unsure of the certificate name, list all root CAs:
> ```powershell
> Get-ChildItem -Path Cert:\LocalMachine\Root\ | Format-Table Subject, Issuer -AutoSize
> ```

**Option B — Certificate Manager GUI**

1. Press `Win+R`, type `certmgr.msc`, press Enter
2. Navigate to **Trusted Root Certification Authorities > Certificates**
3. Find your proxy's certificate (e.g., "Zscaler Root CA")
4. Right-click > **All Tasks** > **Export**
5. Choose **Base-64 encoded X.509 (.CER)** format
6. Save as `proxy-root-ca.pem` in your user profile folder

**Option C — From Chrome**

1. Open Chrome, navigate to any HTTPS site
2. Click the padlock icon in the address bar > **Connection is secure** > **Certificate is valid**
3. Go to the **Certification Path** tab
4. Click the root certificate (top of the chain — should show your proxy's name)
5. Click **View Certificate** > **Details** tab > **Copy to File**
6. Export as **Base-64 encoded X.509 (.CER)**

### Step 2: Install into WSL2 System Certificate Store

Open your WSL2 terminal:

```bash
# Copy the certificate from Windows into WSL2
cp /mnt/c/Users/YOUR_WINDOWS_USERNAME/proxy-root-ca.pem /tmp/proxy-root-ca.crt

# Install into the system certificate store
sudo cp /tmp/proxy-root-ca.crt /usr/local/share/ca-certificates/proxy-root-ca.crt
sudo update-ca-certificates
```

You should see output like:
```
Updating certificates in /etc/ssl/certs...
1 added, 0 removed; done.
```

This updates the system CA bundle at `/etc/ssl/certs/ca-certificates.crt` which now includes your proxy's Root CA alongside the standard Mozilla CA certificates. This fixes `curl`, `git`, `wget`, and other tools that use the system CA store.

> **Important**: The system bundle at `/etc/ssl/certs/ca-certificates.crt` contains the same Mozilla root CAs that Python's certifi package provides, plus your proxy CA. There is no need to create a separate combined bundle.

### Step 3: Set Environment Variables

After Step 2, the system bundle has everything needed. You just need to tell Python to use it instead of its built-in paths.

### Step 3: Configure bb2gh

**Option A — bb2gh config setting (recommended)**

Set the `BB2GH_SSL_CA_BUNDLE` environment variable or add it to your bb2gh config:

```bash
# Environment variable
export BB2GH_SSL_CA_BUNDLE="$HOME/combined-ca-bundle.pem"
```

Or in `~/.bb2gh/config.yaml`:

```yaml
ssl_ca_bundle: ~/combined-ca-bundle.pem
```

This configures all bb2gh httpx connections and the PostHog telemetry SDK automatically.

**Option B — Global environment variables**

Alternatively, set standard environment variables that work for all Python tools.
Add to your `~/.bashrc` (or `~/.zshrc`):

```bash
# Corporate proxy CA certificate — point Python to the system bundle
# Required because Hatch/linuxbrew Python uses its own OpenSSL cert path
export SSL_CERT_FILE=/etc/ssl/certs/ca-certificates.crt
export REQUESTS_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt
```

Then reload your shell:

```bash
source ~/.bashrc
```

**Why two variables?**

| Variable | Used By | Why It's Needed |
|----------|---------|-----------------|
| `SSL_CERT_FILE` | httpx, Python ssl module, pip | bb2gh API calls to Bitbucket and GitHub |
| `REQUESTS_CA_BUNDLE` | requests library, PostHog SDK | bb2gh telemetry (PostHog uses requests internally) |

> **Note**: You can optionally also set `CURL_CA_BUNDLE`, `NODE_EXTRA_CA_CERTS`, and `GIT_SSL_CAINFO` if you use other tools that need the proxy CA. However, `curl` and `git` already use the system CA store by default after Step 2, so these are usually not required.

#### Alternative: Use a `.env` File

If you prefer to keep the variables scoped to bb2gh, add them to your `.env` file:

```bash
# Corporate proxy SSL fix
SSL_CERT_FILE=/etc/ssl/certs/ca-certificates.crt
REQUESTS_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt

# Bitbucket credentials
BB_USERNAME=your-username
BB_API_TOKEN=your-app-password
```

Then source before running:

```bash
set -a && source .env && set +a
hatch run bb2gh discover --workspace myworkspace --output inventory.json
```

### Step 4: Verify

```bash
# Test Python + httpx (what bb2gh uses for API calls)
hatch run python -c "import httpx; r = httpx.get('https://api.bitbucket.org/2.0'); print(f'Bitbucket API: {r.status_code}')"

# Test Python + requests (what PostHog SDK uses for telemetry)
hatch run python -c "import requests; r = requests.get('https://eu.i.posthog.com'); print(f'PostHog: {r.status_code}')"

# Test bb2gh directly
set -a && source .env && set +a
hatch run bb2gh discover --workspace myworkspace --output inventory.json
```

All commands should succeed without SSL errors.

## Automated Setup Script

For convenience, save this as `setup-proxy-certs.sh` and run it once:

```bash
#!/bin/bash
set -euo pipefail

PROXY_CERT="${1:?Usage: $0 /mnt/c/Users/YOU/proxy-root-ca.pem}"

echo "==> Installing proxy CA into system store..."
sudo cp "$PROXY_CERT" /usr/local/share/ca-certificates/proxy-root-ca.crt
sudo update-ca-certificates

echo "==> Configuring environment variables..."
if ! grep -q 'SSL_CERT_FILE' ~/.bashrc 2>/dev/null; then
    cat >> ~/.bashrc << 'ENVEOF'

# Corporate proxy CA certificate — point Python to the system bundle
export SSL_CERT_FILE=/etc/ssl/certs/ca-certificates.crt
export REQUESTS_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt
ENVEOF
    echo "    Added to ~/.bashrc"
else
    echo "    Environment variables already configured in ~/.bashrc"
fi

echo ""
echo "Done! Run: source ~/.bashrc"
echo "Then verify: hatch run python -c \"import httpx; print(httpx.get('https://api.bitbucket.org/2.0').status_code)\""
```

Usage:

```bash
chmod +x setup-proxy-certs.sh
./setup-proxy-certs.sh /mnt/c/Users/YOUR_WINDOWS_USERNAME/proxy-root-ca.pem
source ~/.bashrc
```

## Environment Variable Reference

| Variable | Used By | Purpose |
|----------|---------|---------|
| `BB2GH_SSL_CA_BUNDLE` | bb2gh (all connections) | Custom CA bundle for bb2gh — **recommended** |
| `SSL_CERT_FILE` | httpx, Python ssl, pip | CA bundle path for Python HTTPS clients |
| `REQUESTS_CA_BUNDLE` | requests, PostHog SDK, boto3 | CA bundle path for requests-based libraries |
| `CURL_CA_BUNDLE` | curl | CA bundle path for curl |
| `NODE_EXTRA_CA_CERTS` | Node.js, npm | Additional CA certs for Node.js |
| `GIT_SSL_CAINFO` | git | CA bundle path for git HTTPS operations |

## How It Works with bb2gh

bb2gh supports custom CA bundles through a dedicated setting:

- **`BB2GH_SSL_CA_BUNDLE`** env var or `ssl_ca_bundle` in config — passes the bundle path directly to all httpx clients and sets `REQUESTS_CA_BUNDLE` for the PostHog SDK

bb2gh also respects the standard environment variables as a fallback:

| Component | Library | Env Var | Purpose |
|-----------|---------|---------|---------|
| Bitbucket API calls | httpx | `SSL_CERT_FILE` | Repository discovery, PR listing, metadata |
| GitHub API calls | httpx | `SSL_CERT_FILE` | Repository creation, PR migration, validation |
| PostHog telemetry | requests | `REQUESTS_CA_BUNDLE` | Anonymous usage analytics |
| git clone/push | git binary | System CA store | Repository data transfer |

## PostHog Telemetry SSL Errors

If you see these errors in stderr while bb2gh is running:

```
Retrying ... after connection broken by 'SSLError(SSLCertVerificationError(...))': /batch/
error uploading: HTTPSConnectionPool(host='eu.i.posthog.com', port=443): Max retries exceeded
```

This means PostHog's telemetry is failing to reach `eu.i.posthog.com` due to the proxy CA not being trusted by the `requests` library.

**Fix**: Set `BB2GH_SSL_CA_BUNDLE` (recommended) or ensure `REQUESTS_CA_BUNDLE` is set. The `requests` library has its own CA resolution logic separate from `SSL_CERT_FILE`.

**Impact**: These errors are **non-blocking** — bb2gh continues working normally. The PostHog SDK has a silent error handler (`on_error`) that logs failures at debug level and never interrupts CLI execution. Telemetry data is simply not sent when this fails.

## Maintenance

The system bundle approach requires **no ongoing maintenance**:

- `/etc/ssl/certs/ca-certificates.crt` is managed by the OS package `ca-certificates`
- It automatically includes Mozilla root CAs (same source as Python's certifi package)
- Your proxy CA persists across `apt update` / `apt upgrade`
- No need to regenerate bundles when Python, certifi, or httpx are upgraded

The only time you need to repeat the process is if:
- Your proxy's Root CA is rotated (rare — typically 10+ year validity)
- You reinstall WSL2 from scratch

## Other Corporate Proxies

This guide uses Zscaler as the primary example, but the same approach works for any proxy that performs HTTPS inspection:

| Proxy | Certificate Name to Look For |
|-------|------------------------------|
| Zscaler | "Zscaler Root CA" or "Zscaler Intermediate Root CA" |
| Netskope | "Netskope Root CA" |
| Cisco Umbrella | "Cisco Umbrella Root CA" |
| Palo Alto | Your organization's custom root CA |
| Blue Coat / Symantec | "Blue Coat" or "Symantec" root CA |
| Forcepoint | "Forcepoint" root CA |

The key is finding and exporting the correct Root CA certificate from the Windows certificate store (`certmgr.msc`).

## Troubleshooting the Fix

### `update-ca-certificates` succeeded but Python still fails

You installed the cert into the system store but didn't set `SSL_CERT_FILE`. Hatch/linuxbrew Python uses its own OpenSSL at `/home/linuxbrew/.linuxbrew/etc/openssl@3/cert.pem`, which is not the system store. The `SSL_CERT_FILE` variable redirects Python to the updated system bundle.

```bash
# Verify Python's default cert path (without SSL_CERT_FILE)
hatch run python -c "import ssl; print(ssl.get_default_verify_paths())"

# You'll likely see something like:
# DefaultVerifyPaths(cafile='/home/linuxbrew/.linuxbrew/etc/openssl@3/cert.pem', ...)
# This path does NOT contain your proxy CA
```

### bb2gh API calls work but PostHog still shows SSL errors

You set `SSL_CERT_FILE` but not `REQUESTS_CA_BUNDLE`. The PostHog SDK uses the `requests` library which does **not** respect `SSL_CERT_FILE`. It has its own CA resolution:

1. `REQUESTS_CA_BUNDLE` (if set) — **this is what you need**
2. `CURL_CA_BUNDLE` (fallback)
3. `certifi.where()` (default — does not include your proxy CA)

Fix: `export REQUESTS_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt`

### Wrong certificate exported

If you exported the wrong certificate, verify by checking the certificate chain:

```bash
# Show the certificate chain for Bitbucket (from the proxy's perspective)
openssl s_client -connect api.bitbucket.org:443 -showcerts < /dev/null 2>/dev/null | \
    openssl x509 -noout -issuer -subject
```

The issuer should show your proxy's CA name. Export that specific CA from the Windows certificate store.

### Multiple proxy certificates

Some proxies (including Zscaler) use a chain: Root CA > Intermediate CA > Server Certificate. You only need the **Root CA** in the system store. The intermediate certificates are provided by the proxy during the TLS handshake.

If verification still fails after installing the Root CA, try also installing the Intermediate CA:

```bash
# Install both certificates
sudo cp proxy-root-ca.crt /usr/local/share/ca-certificates/proxy-root-ca.crt
sudo cp proxy-intermediate-ca.crt /usr/local/share/ca-certificates/proxy-intermediate-ca.crt
sudo update-ca-certificates
```

### Environment variables not taking effect

Make sure variables are exported (not just set):

```bash
# Wrong — variable exists but not exported to child processes
SSL_CERT_FILE=/etc/ssl/certs/ca-certificates.crt

# Correct — exported to hatch/python subprocesses
export SSL_CERT_FILE=/etc/ssl/certs/ca-certificates.crt

# Or when sourcing .env:
set -a && source .env && set +a  # set -a exports all variables
```
