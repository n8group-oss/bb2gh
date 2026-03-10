# Installation

Stage 1 hardened distribution supports two public release channels: PyPI and
GitHub Releases.

The private repository builds the hardened release bundle, and the public
repository now owns the visible GitHub Release plus the final PyPI publication
of that exact wheel.

## Requirements

- **Python 3.11+** — bb2gh uses modern Python features
- **Git 2.25+** — Required for repository operations
- **git-lfs** — Required if migrating LFS-enabled repositories
- **supported platforms** — The current hardened wheel is a pure Python
  `py3-none-any` artifact, so the supported public platforms are Linux, macOS,
  and Windows environments that provide Python 3.11+, Git, and git-lfs.
  Other environments are outside the supported Stage 1 matrix, and the public
  release path does not provide a source-distribution fallback.

## Install From PyPI

### pipx (Recommended)

[PyPI](https://pypi.org/project/bb2gh/) is the default public install channel.
[pipx](https://pipx.pypa.io/) installs CLI tools in isolated environments:

```bash
pipx install bb2gh
```

This keeps bb2gh's dependencies separate from your system Python.

### pip

Install the published hardened wheel directly from PyPI:

```bash
pip install bb2gh
```

For user installation (no sudo required):

```bash
pip install --user bb2gh
```

## Install From GitHub Releases

The public repository publishes the exact wheel that was verified from the
private release bundle. Download the wheel plus `SHA256SUMS` from
[GitHub Releases](https://github.com/n8group-oss/bb2gh/releases) and verify the
checksum before installing.

Linux:

```bash
sha256sum -c SHA256SUMS
```

macOS:

```bash
shasum -a 256 -c SHA256SUMS
```

Windows PowerShell:

```powershell
$expected = (Get-Content .\SHA256SUMS | Select-String 'bb2gh-<version>-py3-none-any.whl').ToString().Split(' ')[0]
$actual = (Get-FileHash .\bb2gh-<version>-py3-none-any.whl -Algorithm SHA256).Hash.ToLower()
if ($actual -ne $expected) { throw "SHA256 mismatch" }
```

After checksum verification succeeds, install the wheel:

```bash
pip install ./bb2gh-<version>-py3-none-any.whl
```

## Unsupported Or Paused Paths

- `source-install from the public repo is unsupported` in Stage 1 because the
  hardened release path is wheel-only.
- Docker publication is paused in the hardened lane until it can consume the
  exact hardened wheel instead of rebuilding from source.
- Homebrew is paused until a hardened formula exists.

## Verify Installation

Check that bb2gh is installed correctly:

```bash
bb2gh --version
```

You should see the installed version number printed.

## Shell Completion

bb2gh supports shell completion for bash, zsh, and fish.

### Bash

Add to your `~/.bashrc`:

```bash
eval "$(_BB2GH_COMPLETE=bash_source bb2gh)"
```

### Zsh

Add to your `~/.zshrc`:

```bash
eval "$(_BB2GH_COMPLETE=zsh_source bb2gh)"
```

### Fish

Add to your `~/.config/fish/completions/bb2gh.fish`:

```fish
_BB2GH_COMPLETE=fish_source bb2gh | source
```

## Enterprise Installation

For enterprise features (distributed migrations, compliance tools), install with extras:

```bash
pip install "bb2gh[enterprise]"
```

This includes additional dependencies for Redis-based job distribution and advanced compliance reporting.

## Next Steps

- [Quick Start Guide](quickstart.md) — Run your first migration
- [Configuration](configuration.md) — Set up authentication and defaults
