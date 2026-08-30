# Ansible Galaxy Metadata & Variable Validation (`ansible-meta-validate.yml`)

> **Version pinning**: the example below uses `@main` for readability. In production, pin a release tag instead — see [Versioning & Upgrade](../../README.md#-versioning--upgrade).

Dedicated validation of Ansible Galaxy metadata structure (`meta/main.yml`) and variable consistency across role surfaces.

## Variable Consistency Validation

Checks role variable declarations and usage across four surfaces (`defaults/main.yml`, `meta/argument_specs.yml`, `tasks/assert.yml`, `README.md`) and detects dead or unused variables.

**Checks Performed:**

1. Every key in `defaults/main.yml` exists in `meta/argument_specs.yml` (`error` class).
2. Every option in `meta/argument_specs.yml` exists in `defaults/main.yml` (`error` class).
3. Every key in `defaults/main.yml` is referenced in `tasks/assert.yml` (`error` class).
4. Every key in `defaults/main.yml` is referenced in `README.md` (`error` class).
5. Dead-variable detection: tests whether every key in `defaults/main.yml` is referenced in `tasks/` (excl. `assert.yml`), `handlers/`, `templates/` or `vars/`. Classifies into four outcomes:
   - Referenced outside `assert.yml`: `alive` (no report).
   - Referenced only in `assert.yml` and listed in `ignore_dead`: `notice` (intentional opt-in guard, waived).
   - Referenced only in `assert.yml` without a waiver: `warning` (unwaived assert-only guard to review).
   - Referenced nowhere: `warning` (genuinely dead).
6. Literal default value parity between `defaults/main.yml` and `argument_specs` (`warning` class; skips Jinja expressions `{{ ... }}` and `""` sentinels).
7. Waiver entries lacking a non-empty `reason` (`error` class).
8. Stale waiver detection (`warning` class).
9. Sub-options under `options:` in `argument_specs` declaring their own `default:` (`warning` class).
10. Internal `__`-prefixed variables in `vars/**/*.yml` referenced at least once (`warning` class).

**Graceful Degradation:**

- Missing `defaults/main.yml`: skips validation with a `notice` annotation (e.g. stub repositories).
- Missing `meta/argument_specs.yml`: skips checks 1, 2, 6, 9 with a warning.
- Missing `tasks/assert.yml`: skips check 3 with a warning.

**Rollout Strategy:**

1. **`v3.1.0` (Stage 1)**: `vars-validation-mode` defaults to `warn`. Checks run and report to `$GITHUB_STEP_SUMMARY` without failing CI builds.
2. **Stage 2 (Future Major)**: Default mode flips to `error`. Individual roles can pin `vars-validation-mode: warn` if not ready.

**Role Waiver Format (`.ansible-vars-validate.yml`):**

Relying on optional dot-config at role root. Every entry **must** supply a non-empty `reason`.

> **Note:** `ignore_dead` serves a dual purpose — it silences genuinely dead variables and demotes waived assert-only guards from a warning to an informational notice.

```yaml
# .ansible-vars-validate.yml
---
ignore_dead:
  - name: docker_tcp_insecure_acknowledged
    reason: "Opt-in security acknowledgement consumed only by tasks/assert.yml"
ignore_unasserted:
  - name: appname_freeform_extra
    reason: "Arbitrary user mapping, no meaningful runtime constraint"
```

**Inputs:**

| Input | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `python-version` | string | no | `"3.12"` | Python version to use on the runner |
| `runner-group` | string | no | `""` | Runner group to execute jobs on. Ignored when `runner` is set. |
| `runner` | string | no | `"ubuntu-latest"` | Explicit runner label. Overrides `runner-group` when non-empty. |
| `vars-validation-mode` | string | no | `"warn"` | Validation mode: `'off'`, `'warn'`, or `'error'` |

**Usage Example:**

```yaml
jobs:
  validate-metadata:
    uses: grzegorzfranus/github-workflows/.github/workflows/ansible-meta-validate.yml@main
    with:
      python-version: "3.12"
      vars-validation-mode: "warn"
```
