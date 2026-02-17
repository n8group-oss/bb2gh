# Installation

bb2gh can be installed via pip, pipx, Docker, or from source.

## Requirements

- **Python 3.11+** — bb2gh uses modern Python features
- **Git 2.25+** — Required for repository operations
- **git-lfs** — Required if migrating LFS-enabled repositories

## Installation Methods

### pipx (Recommended)

[pipx](https://pipx.pypa.io/) installs CLI tools in isolated environments:

```bash
pipx install bb2gh
```

This keeps bb2gh's dependencies separate from your system Python.

### pip

Install directly with pip:

```bash
pip install bb2gh
```

For user installation (no sudo required):

```bash
pip install --user bb2gh
```

### Docker

Pull the official Docker image (multi-arch: amd64 + arm64):

```bash
docker pull ghcr.io/n8group-oss/bb2gh:latest
```

Run with:

```bash
docker run --rm \
  -e BB_USERNAME=your-username \
  -e BB_API_TOKEN=your-token \
  -e GH_TOKEN=ghp_your-token \
  -v $(pwd):/workspace \
  ghcr.io/n8group-oss/bb2gh:latest \
  discover --workspace my-workspace
```

Or use Docker Compose (a `docker-compose.yml` is included in the repository):

```bash
docker compose run --rm bb2gh discover --workspace my-workspace
```

For CI/CD pipeline usage, see the [Docker & CI/CD Guide](../guides/docker-cicd.md).

### From Source

Clone and install in development mode:

```bash
git clone https://github.com/n8group-oss/bb2gh.git
cd bb2gh
pip install -e .
```

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
