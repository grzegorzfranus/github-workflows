# Ansible Security (`ansible-security.yml`)

> **Version pinning**: the example below uses `@main` for readability. In production, pin a release tag instead — see [Versioning & Upgrade](../../README.md#-versioning--upgrade).

TruffleHog secrets detection and Trivy IaC security scans. Each scanner can be independently enabled or disabled. Contains a Security Gate job.

**Inputs:**

| Input | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `enable-trufflehog` | boolean | no | `true` | Enable TruffleHog secret scanning |
| `enable-trivy` | boolean | no | `true` | Enable Trivy IaC security scans (HIGH/CRITICAL severity) |
| `runner` | string | no | `"ubuntu-latest"` | Runner label to execute jobs on |

**Usage Example:**

```yaml
jobs:
  security:
    uses: grzegorzfranus/github-workflows/.github/workflows/ansible-security.yml@main
    with:
      enable-trufflehog: true
      enable-trivy: true
```
