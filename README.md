# GitHub Workflows

| Source                                                                                                            | Version                                                                                                                                | CI                                                                                                                                                              | License                                                           |
| ----------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------- |
| [![Source Code](https://img.shields.io/badge/source-github-blue.svg)](https://github.com/grzegorzfranus/github-workflows) | [![Version](https://img.shields.io/github/v/release/grzegorzfranus/github-workflows)](https://github.com/grzegorzfranus/github-workflows/releases) | [![CI](https://github.com/grzegorzfranus/github-workflows/actions/workflows/ci.yml/badge.svg)](https://github.com/grzegorzfranus/github-workflows/actions/workflows/ci.yml) | [![Repository License](https://img.shields.io/badge/license-apache2.0-brightgreen.svg)](LICENSE) |

Centralized, reusable, and secure GitHub Actions workflows and configuration templates designed to establish enterprise-grade CI/CD and repository hygiene standards.

This repository serves as a model blueprint ("wzór") for corporate workflows. It incorporates strict security hardening, automated release cycles, and automated local lints.

## ✨ Features

- 🔒 **Immutable Third-Party Actions**: All external actions are pinned to their full 40-character commit SHA instead of mutable tags.
- 🔑 **Job-Level Least Privilege**: Strict job-level GITHUB_TOKEN permissions (`contents: read` default) to prevent unauthorized access.
- 🚀 **Isolated CI Executions**: Lint checks run inside clean environments using `pipx run` to prevent python package pollution.
- 🤖 **Automated Release Management**: Zero-touch versioning, tagging, and changelog generation using Google Release Please.
- 📋 **Corporate Governance Templates**: Premium templates for pull requests and issues to streamline team review cycles.

## 📋 Requirements

- **Local Linters**: `yamllint` and `actionlint` are required for local verification before submitting code changes.
- **GitHub Runner**: Workflows are designed and tested on standard `ubuntu-latest` environments.

## 🚀 Quick Start

### 1. Development Setup

Initialize development dependencies and activate local Git Hooks:
```bash
npm install
```

### 2. Manual Verification

To verify your workflow definitions manually:

```bash
# Run yamllint on workflow definitions
pipx run yamllint .github/workflows/*.yml

# Run actionlint to check actions schema
actionlint
```


## ⚙️ Configuration

### 1. Branch Naming Convention

All branches created in this repository must use category prefixes to ensure a clean history:

- `feature/` — New workflows, features, or enhancements
- `bugfix/` — Fixing a bug in a workflow
- `hotfix/` — Critical quick-fixes applied to production
- `docs/` — Documentation updates
- `refactor/` — Code refactoring without behavior changes
- `test/` — Adding or fixing validation tests
- `chore/` — Maintenance, updating dependencies
- `ci/` — Pipeline-specific configurations and lint gates

### 2. Commit Message Convention

This repository strictly enforces Conventional Commits:

- `feat:` — Minor version bump (e.g. `1.0.0` ➡️ `1.1.0`)
- `fix:` — Patch version bump (e.g. `1.0.0` ➡️ `1.0.1`)
- `feat!:` / `BREAKING CHANGE:` — Major version bump (e.g. `1.0.0` ➡️ `2.0.0`)
- `docs:`, `chore:`, `refactor:`, `test:`, `ci:` — Changelog entry only (no bump)

### 3. Issue & PR Templates

All issues, tasks, and bug reports created in this repository must strictly follow the interactive forms defined under [`.github/ISSUE_TEMPLATE/`](.github/ISSUE_TEMPLATE/) (which comply with the `task-creation` skill format).

Similarly, all Pull Requests must be structured according to the template located under [`.github/PULL_REQUEST_TEMPLATE/pull_request_template.md`](.github/PULL_REQUEST_TEMPLATE/pull_request_template.md) (which complies with the `git-workflow` skill format).



## 🛡️ Security Features

- ✅ **SHA Pinned Actions**: Immutable external dependencies (e.g. `actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683`).
- ✅ **Minimal Job Permissions**: Jobs elevate access only when required (e.g. `release-please` has `contents: write`, validation has `contents: read`).
- ✅ **Isolated Linters**: Zero global pip packages; using `pipx` run commands.
- ✅ **Automated Branch Name Gate**: Rejects PR branches failing naming conventions.
- ✅ **Automated PR Title Gate**: Rejects PRs failing Conventional Commits formats.

## 📁 File Structure

```
github-workflows/
├── .github/
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug_report.yml             # Interactive Bug report form
│   │   ├── config.yml                 # Issue templates config
│   │   ├── feature_request.yml        # Interactive Feature request form
│   │   └── task.yml                   # Interactive Task chore form
│   ├── PULL_REQUEST_TEMPLATE/
│   │   └── pull_request_template.md   # PR checklist template
│   ├── workflows/
│   │   ├── ansible-ci.yml             # Ansible CI orchestrator
│   │   ├── ansible-lint.yml           # Reusable Ansible lint validations
│   │   ├── ansible-molecule.yml       # Reusable Molecule test runner
│   │   ├── ansible-publish.yml        # Reusable Galaxy publish template
│   │   ├── ansible-security.yml       # Reusable TruffleHog & Trivy scans
│   │   ├── ci.yml                     # Validator CI pipeline
│   │   └── release.yml                # Release Please automation
│   └── dependabot.yml                 # Actions dependency updates config
├── .husky/                            # Git hooks configuration (Husky)
│   ├── commit-msg                     # Commit message validation hook
│   └── pre-commit                     # Pre-commit workflows validation hook
├── scripts/
│   └── validate.sh                    # Pre-commit validation runner script
├── .gitignore                         # Git ignore configurations
├── .release-please-manifest.json      # Google Release Please version tracking
├── .yamllint                          # yamllint settings
├── CHANGELOG.md                       # Repository changelog
├── LICENSE                            # Apache-2.0 License
├── README.md                          # This documentation
├── commitlint.config.js               # Commitlint config file
├── package.json                       # Node dependencies file
└── release-please-config.json         # Google Release Please config
```

## 📦 Reusable Workflows

This repository provides modular, reusable workflows designed to standardize quality checks across your Ansible role repositories.

### 1. Ansible CI Orchestrator (`ansible-ci.yml`)

The primary CI pipeline. It coordinates the execution of linting, security, and functional integration tests in sequence.

**Usage Example:**
Add the following to `.github/workflows/ci.yml` in your Ansible role repository:

```yaml
name: CI

on:
  pull_request:

permissions:
  contents: read

concurrency:
  group: ci-${{ github.ref }}
  cancel-in-progress: true

jobs:
  ansible-ci:
    uses: grzegorzfranus/github-workflows/.github/workflows/ansible-ci.yml@v1.2.0
    with:
      ansible-lint-profile: "production"
      molecule-distros: '["ubuntu2404", "debian12", "rockylinux9"]'
      molecule-scenarios: '["default"]'
      python-version: "3.12"
      enable-trufflehog: true
      enable-trivy: true
      enable-galaxy-metadata-check: true
```

### 2. Ansible Galaxy Publish (`ansible-publish.yml`)

Validates metdata formats and description length, and publishes tagged role releases to Ansible Galaxy.

**Usage Example:**
Add the following to `.github/workflows/publish.yml` in your Ansible role repository:

```yaml
name: Publish

on:
  push:
    tags:
      - 'v*'

permissions:
  contents: read

jobs:
  publish:
    uses: grzegorzfranus/github-workflows/.github/workflows/ansible-publish.yml@v1.2.0
    with:
      python-version: "3.12"
    secrets:
      galaxy-api-key: ${{ secrets.GALAXY_API_KEY }}
```

### 3. Granular Reusable Workflows

If you need to run specific suites independently, you can invoke the low-level workflows directly:
- **[`ansible-lint.yml`](.github/workflows/ansible-lint.yml)**: Static YAML and Ansible linting.
- **[`ansible-security.yml`](.github/workflows/ansible-security.yml)**: TruffleHog secrets detection and Trivy IaC scans.
- **[`ansible-molecule.yml`](.github/workflows/ansible-molecule.yml)**: Syntax checks and Molecule testing matrix.


## 📝 License

This project is licensed under the Apache-2.0 License - see the LICENSE file for details.

## 👥 Author Information

This repository was created by [Grzegorz Franus](https://github.com/grzegorzfranus).

