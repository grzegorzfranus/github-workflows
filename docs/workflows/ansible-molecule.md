# Ansible Molecule Testing (`ansible-molecule.yml`)

> **Version pinning**: the example below uses `@main` for readability. In production, pin a release tag instead — see [Versioning & Upgrade](../../README.md#-versioning--upgrade).

Syntax checks and Molecule integration test matrix. Creates a test matrix from `molecule-scenarios × molecule-distros`. Contains a Molecule Gate job.

## Inputs

| Input                | Type   | Required | Default                                     | Description                                                                               |
| -------------------- | ------ | -------- | ------------------------------------------- | ----------------------------------------------------------------------------------------- |
| molecule-scenarios   | string | no       | `["default"]`                               | JSON array of scenarios to run (e.g., '["default"]')                                      |
| molecule-distros     | string | no       | `["ubuntu2404", "debian12", "rockylinux9"]` | JSON array of distros to test against (e.g., '["ubuntu2404", "debian12", "rockylinux9"]') |
| python-version       | string | no       | `3.12`                                      | Python version to use                                                                     |
| molecule-timeout     | number | no       | `30`                                        | Timeout in minutes for Molecule test jobs                                                 |
| requirements-ci-file | string | no       | `""`                                        | Path to CI requirements.txt for pinned tool versions (empty = use defaults)               |
| runner-group         | string | no       | `""`                                        | Runner group to execute jobs on. Ignored when 'runner' is set.                            |
| runner               | string | no       | `ubuntu-latest`                             | Explicit runner label. Overrides 'runner-group' when non-empty.                           |

## Usage

```yaml
jobs:
  molecule:
    uses: grzegorzfranus/github-workflows/.github/workflows/ansible-molecule.yml@main
    with:
      molecule-distros: '["ubuntu2404", "debian12", "rockylinux9"]'
      molecule-scenarios: '["default"]'
      python-version: "3.12"
      molecule-timeout: 30
```
