# Ansible Galaxy Publish (`ansible-publish.yml`)

> **Version pinning**: the example below uses `@main` for readability. In production, pin a release tag instead — see [Versioning & Upgrade](../../README.md#-versioning--upgrade).

Publishes tagged role releases to Ansible Galaxy. Includes retry logic with exponential backoff (up to 3 attempts). Note: Metadata validation is NOT performed by this workflow and must be run beforehand (e.g. via `ansible-meta-validate.yml`).

**Inputs:**

| Input | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `python-version` | string | no | `"3.12"` | Python version to use on the runner |
| `runner` | string | no | `"ubuntu-latest"` | Runner label to execute jobs on |

**Secrets:**

| Secret | Required | Description |
| --- | --- | --- |
| `galaxy-api-key` | **yes** | Ansible Galaxy API Key for role publishing |

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
  validate-metadata:
    uses: grzegorzfranus/github-workflows/.github/workflows/ansible-meta-validate.yml@main

  publish:
    needs: [validate-metadata]
    uses: grzegorzfranus/github-workflows/.github/workflows/ansible-publish.yml@main
    with:
      python-version: "3.12"
    secrets:
      galaxy-api-key: ${{ secrets.GALAXY_API_KEY }}
```
