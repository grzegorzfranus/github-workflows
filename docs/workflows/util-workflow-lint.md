# Workflow Lint (`util-workflow-lint.yml`)

> **Version pinning**: the example below uses `@main` for readability. In production, pin a release tag instead — see [Versioning & Upgrade](../../README.md#-versioning--upgrade).

Validates `.github/workflows` with yamllint, actionlint and zizmor, skips linting when a pull request changes no file matching `paths`, and reports one result through the `✅ Workflow Lint Gate` job. Jobs run on `ubuntu-latest` unless `runner` or `runner-group` says otherwise. Tool versions are pinned for reproducibility (yamllint 1.38.0, zizmor 1.28.0, pyflakes 3.4.0 and shellcheck-py 0.11.0.1). The workflow installs every tool itself, so the runner needs no preinstalled linters or pipx.

## Inputs

| Input           | Type   | Required | Default         | Description                                                                                                             |
| --------------- | ------ | -------- | --------------- | ----------------------------------------------------------------------------------------------------------------------- |
| paths           | string | no       | `.github/**`    | Space-separated git pathspec globs; linting runs only when a pull request changes a matching file (empty = always lint) |
| yamllint-config | string | no       | `""`            | Path to a yamllint config in the caller repository (empty = the caller .yamllint, else the github-workflows default)    |
| python-version  | string | no       | `3.12`          | Python version used to install yamllint, zizmor, pyflakes and shellcheck                                                |
| runner-group    | string | no       | `""`            | Runner group to execute jobs on. Ignored when 'runner' is set.                                                          |
| runner          | string | no       | `ubuntu-latest` | Explicit runner label. Overrides 'runner-group' when non-empty.                                                         |

## Jobs

| Job            | Description                                                                                                                                                                                                            |
| -------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `detect`       | Checks git diff against the pull request base SHA using `paths`. Skips linting (`changed=false`) when no matching files changed, or runs linting (`changed=true`) on changes, non-PR events, or when `paths` is empty. |
| `yaml-lint`    | Validates YAML syntax with yamllint (1.38.0). Uses the `yamllint-config` input, else the caller repository's `.yamllint`, else a default embedded in the workflow that matches `.yamllint` of this repository.         |
| `actions-lint` | Validates GitHub Actions workflow syntax, schemas, and expressions using actionlint, with pinned pyflakes and shellcheck (from shellcheck-py) for the embedded scripts.                                                |
| `zizmor-scan`  | Runs a security audit across workflow files using zizmor (1.28.0) to detect issues such as unpinned actions or template injection.                                                                                     |
| `lint-gate`    | Aggregates all check results; passes if all checks succeed or if linting was skipped, and fails if any check failed or was cancelled.                                                                                  |

## Usage

```yaml
jobs:
  workflow-lint:
    uses: grzegorzfranus/github-workflows/.github/workflows/util-workflow-lint.yml@main

  merge-check:
    name: "Merge Check Gate"
    needs: [workflow-lint]
    if: always()
    runs-on: ubuntu-latest
    timeout-minutes: 5
    steps:
      - name: Evaluate results
        env:
          WORKFLOW_LINT_RESULT: ${{ needs.workflow-lint.result }}
        run: |
          if [[ "$WORKFLOW_LINT_RESULT" == "failure" || "$WORKFLOW_LINT_RESULT" == "cancelled" ]]; then
            echo "::error::Workflow lint failed or was cancelled"
            exit 1
          fi
          echo "All checks passed"
```

Callers do not require extra permissions (`contents: read` is enough). When no files matching `paths` are modified in a pull request, workflow linting is skipped and the gate still passes.
