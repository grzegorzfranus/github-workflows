# github-workflows

[![CI](https://github.com/grzegorzfranus/github-workflows/actions/workflows/ci.yml/badge.svg)](https://github.com/grzegorzfranus/github-workflows/actions/workflows/ci.yml)
[![Release](https://github.com/grzegorzfranus/github-workflows/actions/workflows/release.yml/badge.svg)](https://github.com/grzegorzfranus/github-workflows/actions/workflows/release.yml)
[![License](https://img.shields.io/github/license/grzegorzfranus/github-workflows)](LICENSE)

Centralized, reusable, and secure GitHub Actions workflows and configuration templates designed to establish enterprise-grade CI/CD and repository hygiene standards.

This repository serves as a model blueprint ("wzór") for corporate workflows. It incorporates strict security hardening, automated release cycles, and automated local lints.

---

## Author & Licensing

| Field      | Value                                                              |
| ---------- | ------------------------------------------------------------------ |
| **Author** | Grzegorz Franus                                                    |
| **Company**| EWARE                                                              |
| **License**| [Apache-2.0](LICENSE)                                              |
| **Repository**| [github-workflows](https://github.com/grzegorzfranus/github-workflows) |

---

## Repository Workflows

| Workflow | File | Scope | Purpose & Description |
| -------- | ---- | ----- | --------------------- |
| **CI** | [`ci.yml`](.github/workflows/ci.yml) | Internal | Validates branch names, PR titles (Conventional Commits), and runs `yamllint` and `actionlint` gates. |
| **Release** | [`release.yml`](.github/workflows/release.yml) | Internal | Triggers Google Release Please to automate changelogs, tags, and releases on merges to `main`. |

---

## Project Standards & Conventions

To maintain a showcase-level repository structure, all developers must adhere to the following standards.

### 1. Branch Naming Convention

All branches created in this repository must use structured naming prefixes to ensure logical grouping and clean history:

- `feature/` — New workflows, features, or enhancements (e.g., `feature/add-terraform-validation`)
- `bugfix/` — Fixing a bug in a workflow (e.g., `bugfix/fix-checkout-sha`)
- `hotfix/` — Critical quick-fixes applied to production workflows (e.g., `hotfix/security-patch`)
- `release/` — Release branches (e.g., `release/v1.0.0`)
- `docs/` — Documentation updates (e.g., `docs/update-readme`)
- `refactor/` — Code refactoring without behavior changes (e.g., `refactor/cleanup-jobs`)
- `test/` — Adding or fixing validation tests (e.g., `test/add-lint-scenario`)
- `chore/` — Maintenance, updating dependencies or repository files (e.g., `chore/bump-actionlint`)
- `ci/` — Pipeline-specific configurations and lint gates (e.g., `ci/harden-actionlint-config`)

Branch naming is verified automatically in the CI pipeline on every Pull Request.

### 2. Commit Message Convention

This repository strictly enforces the [Conventional Commits](https://www.conventionalcommits.org/) standard. Commit messages trigger automated version bumps and changelog updates via Google Release Please.

#### Format:
```text
<type>(<optional-scope>): <description>

[optional body]

[optional footer(s)]
```

#### Mapping to Version Bumps:
- `feat:` — Minor version bump (e.g., `1.0.0` ➡️ `1.1.0`)
- `fix:` — Patch version bump (e.g., `1.0.0` ➡️ `1.0.1`)
- `feat!:` / `BREAKING CHANGE:` — Major version bump (e.g., `1.0.0` ➡️ `2.0.0`)
- `docs:`, `chore:`, `refactor:`, `test:`, `ci:` — No version bump (changelog entry only)

---

## Enterprise Security Hardening

To satisfy enterprise-grade security compliance, we implement the following controls:

### 1. Immutable Third-Party Actions (SHA Pinning)
All external actions are pinned to their full 40-character commit SHA instead of mutable tags (e.g., `@v4`). A comment is appended to identify the human-readable version.
```yaml
- name: "Checkout repository"
  uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683 # v4.2.2
```

### 2. Granular Job-Level Least Privilege
To minimize the impact of token compromises, we disable global write permissions (`permissions: read-all` or `contents: read` at the workflow root) and only elevate permissions on specific jobs that strictly require write access.
- **Example**: In `release.yml`, write permissions are elevated *only* for the `release-please` job, while validation steps remain read-only.

### 3. Isolated CI Executions (`pipx`)
No global python packages are installed on GitHub runners. Lint checks are executed within isolated, container-safe environments using `pipx run`.
```yaml
- name: "Lint workflow files"
  run: pipx run yamllint .github/workflows/*.yml
```

---

## Local Verification & Quality Gates

Before committing and pushing changes, developers are required to run quality checks locally. 

### 1. Verify YAML Syntax
Validate all YAML files for syntax and formatting:
```bash
pipx run yamllint .github/workflows/*.yml
```

### 2. Verify GitHub Actions Schemas
Validate that the actions syntax and expressions are correct:
```bash
actionlint
```

Both linters must pass cleanly (0 errors) before a Pull Request is merged. The final status check is consolidated into a single `Merge Check` job, which is a required check in the repository's branch protection rules.
