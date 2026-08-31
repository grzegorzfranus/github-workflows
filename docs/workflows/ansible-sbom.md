# Ansible SBOM (`ansible-sbom.yml`)

> **Version pinning**: the example below uses `@main` for readability. In production, pin a release tag instead — see [Versioning & Upgrade](../../README.md#-versioning--upgrade).

Emits a CycloneDX Software Bill of Materials for the scanned tree and publishes it as a build artifact. Reports only — it never fails a build.

**Inputs:**

| Input | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `scan-ref` | string | no | `"."` | Path to inventory |
| `artifact-name` | string | no | `"sbom-ansible"` | Name of the published SBOM artifact |
| `runner-group` | string | no | `"infra-privileged"` | Runner group to execute jobs on. Ignored when `runner` is set |
| `runner` | string | no | `""` | Explicit runner label. Overrides `runner-group` when non-empty |

**Artifacts:**

| Artifact | Retention | Contents |
| --- | --- | --- |
| `<artifact-name>` | 90 days | CycloneDX SBOM of the scanned tree |

**Expected result for a role repository:**

Trivy has no analyzer for Ansible Galaxy collections, so `requirements.yml` is not read as a dependency manifest. A role repository is therefore expected to report an SBOM with **no components** — measured against a representative role, the count is zero.

The workflow records the count in the run summary and emits a warning rather than failing. Callers must keep it outside their merge gate, because a job that reports an expected result must not block a build.

The value today is structural. The workflow, its artifact name and its retention are fixed, so the day a Galaxy analyzer exists — or the day the shipped artifact is redefined — only the scanner invocation changes.

**Where to call it from:**

`ansible-ci.yml` calls this workflow on every run, which gives visibility per pull request.

The moment a role actually ships is the Galaxy publish, not the pull request, so `ansible-publish.yml` is the more meaningful caller once there is something to inventory. That wiring is deliberately left out for now: an SBOM of zero components attached to a release would be a record of nothing.

**Usage Example:**

```yaml
jobs:
  sbom:
    uses: grzegorzfranus/github-workflows/.github/workflows/ansible-sbom.yml@main
```
