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

To verify your workflow definitions locally:

```bash
# 1. Run yamllint on workflow definitions
pipx run yamllint .github/workflows/*.yml

# 2. Run actionlint to check actions schema
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

All issues, tasks, and bug reports created in this repository must strictly follow the templates located in [`.github/ISSUE_TEMPLATE/`](.github/ISSUE_TEMPLATE/) (which comply with the `task-creation` skill format).

Similarly, all Pull Requests must be structured according to the format defined in [`.github/pull_request_template.md`](.github/pull_request_template.md) (which complies with the `git-workflow` skill format).


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
│   │   ├── bug_report.md
│   │   ├── feature_request.md
│   │   └── task.md
│   ├── workflows/
│   │   ├── ci.yml                     # Validator CI pipeline
│   │   └── release.yml                # Release Please automation
│   └── pull_request_template.md       # PR checklist template
├── .gitignore                         # Git ignore configurations
├── .release-please-manifest.json      # Google Release Please version tracking
├── .yamllint                          # yamllint settings
├── CHANGELOG.md                       # Repository changelog
├── LICENSE                            # Apache-2.0 License
├── README.md                          # This documentation
└── release-please-config.json         # Google Release Please config
```

## 📝 License

This project is licensed under the Apache-2.0 License - see the LICENSE file for details.

## 👥 Author Information

This repository was created by [Grzegorz Franus](https://github.com/grzegorzfranus).

