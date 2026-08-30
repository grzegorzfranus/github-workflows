# Ansible Lint (`ansible-lint.yml`)

> **Version pinning**: the example below uses `@main` for readability. In production, pin a release tag instead — see [Versioning & Upgrade](../../README.md#-versioning--upgrade).

Static YAML and Ansible linting. Contains yamllint and ansible-lint checks. Note: Galaxy metadata check has been deprecated in this workflow (moved to `ansible-meta-validate.yml`).

**Inputs:**

| Input | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `ansible-lint-profile` | string | no | `"production"` | ansible-lint profile (e.g., `shared`, `production`) |
| `python-version` | string | no | `"3.12"` | Python version to use on the runner |
| `requirements-ci-file` | string | no | `""` | Path to CI `requirements.txt` for pinned tool versions |
| `enable-galaxy-metadata-check` | boolean | no | `true` | [DEPRECATED] Ignored, moved to dedicated workflow |
| `runner` | string | no | `"ubuntu-latest"` | Runner label to execute jobs on |

**Usage Example:**

```yaml
jobs:
  lint:
    uses: grzegorzfranus/github-workflows/.github/workflows/ansible-lint.yml@main
    with:
      ansible-lint-profile: "production"
```
