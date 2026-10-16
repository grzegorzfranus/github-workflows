# Ansible CI Orchestrator (`ansible-ci.yml`)

> **Version pinning**: the example below uses `@main` for readability. In production, pin a release tag instead — see [Versioning & Upgrade](../../README.md#-versioning--upgrade).

The primary CI pipeline. It coordinates the execution of linting, security, metadata validation, and functional integration tests in a strict dependency chain. Contains a final Merge Check Gate that aggregates all results into a single required status check.

## Inputs

| Input                        | Type    | Required | Default                                     | Description                                                                               |
| ---------------------------- | ------- | -------- | ------------------------------------------- | ----------------------------------------------------------------------------------------- |
| ansible-lint-profile         | string  | no       | `production`                                | ansible-lint profile (e.g., shared, production)                                           |
| molecule-scenarios           | string  | no       | `["default"]`                               | JSON array of scenarios to run (e.g., '["default"]')                                      |
| molecule-distros             | string  | no       | `["ubuntu2404", "debian12", "rockylinux9"]` | JSON array of distros to test against (e.g., '["ubuntu2404", "debian12", "rockylinux9"]') |
| python-version               | string  | no       | `3.12`                                      | Python version to use                                                                     |
| enable-trufflehog            | boolean | no       | `true`                                      | Enable TruffleHog secret scanning                                                         |
| enable-trivy                 | boolean | no       | `true`                                      | Enable Trivy IaC security scans                                                           |
| enable-galaxy-metadata-check | boolean | no       | `true`                                      | [DEPRECATED → dedicated ansible-meta-validate.yml] Enable Galaxy meta/main.yml validation |
| vars-validation-mode         | string  | no       | `warn`                                      | Variable consistency validation: 'off', 'warn' (report only) or 'error' (fail the build)  |
| molecule-timeout             | number  | no       | `30`                                        | Timeout in minutes for Molecule test jobs                                                 |
| requirements-ci-file         | string  | no       | `""`                                        | Path to CI requirements.txt for pinned tool versions (empty = use defaults)               |
| runner-group                 | string  | no       | `""`                                        | Runner group to execute jobs on. Ignored when 'runner' is set.                            |
| runner                       | string  | no       | `ubuntu-latest`                             | Explicit runner label. Overrides 'runner-group' when non-empty.                           |

## SBOM

The orchestrator calls [`ansible-sbom.yml`](ansible-sbom.md) on every run, publishing a CycloneDX SBOM as the `sbom-ansible` artifact. That job is deliberately absent from the Merge Check Gate: Trivy has no analyzer for Ansible Galaxy collections, so a role repository is expected to report zero components, and a build must not fail on an expected result.

## Usage

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
    uses: grzegorzfranus/github-workflows/.github/workflows/ansible-ci.yml@main
    with:
      ansible-lint-profile: "production"
      molecule-distros: '["ubuntu2404", "debian12", "rockylinux9"]'
      molecule-scenarios: '["default"]'
      python-version: "3.12"
      enable-trufflehog: true
      enable-trivy: true
      enable-galaxy-metadata-check: true
      vars-validation-mode: "warn"
```
