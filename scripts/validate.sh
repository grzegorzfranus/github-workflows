#!/usr/bin/env bash
set -Eeuo pipefail

# Safe path resolution
readonly SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
readonly REPO_ROOT="$(cd -- "$SCRIPT_DIR/.." && pwd -P)"

log_info()  { printf '[%s] INFO:  %s\n' "$(date +'%H:%M:%S')" "$*" >&2; }
log_warn()  { printf '[%s] WARN:  %s\n' "$(date +'%H:%M:%S')" "$*" >&2; }
log_error() { printf '[%s] ERROR: %s\n' "$(date +'%H:%M:%S')" "$*" >&2; }

trap 'log_error "Validation script failed at line $LINENO (exit status $?)"' ERR

validate_workflows() {
    local exit_code=0

    # Move to repo root to run checks
    (
        cd -- "$REPO_ROOT"

        # Check if there are changes in workflow files being committed/pushed
        local has_wf_changes=0
        if git rev-parse --git-dir &>/dev/null; then
            if git diff --cached --name-only | grep -q '^\.github/workflows/'; then
                has_wf_changes=1
            fi
        fi

        # 1. yamllint
        local has_yamllint=0
        if command -v yamllint &>/dev/null; then
            has_yamllint=1
            log_info "Running yamllint..."
            if ! yamllint .github/workflows/*.yml .github/ISSUE_TEMPLATE/*.yml; then
                log_error "yamllint failed!"
                exit_code=1
            fi
        elif command -v pipx &>/dev/null; then
            has_yamllint=1
            log_info "Running yamllint via pipx..."
            if ! pipx run yamllint .github/workflows/*.yml .github/ISSUE_TEMPLATE/*.yml; then
                log_error "yamllint failed!"
                exit_code=1
            fi
        fi

        if [[ "$has_yamllint" -eq 0 ]]; then
            if [[ "$has_wf_changes" -eq 1 ]]; then
                log_error "yamllint is not installed, but workflow changes are detected! Install it to proceed."
                log_error "To install: brew install yamllint  OR  pip install yamllint"
                exit_code=1
            else
                log_warn "yamllint is not installed. Skipping YAML lint check."
                log_warn "To install: brew install yamllint  OR  pip install yamllint"
            fi
        fi

        # 2. actionlint
        local has_actionlint=0
        if command -v actionlint &>/dev/null; then
            has_actionlint=1
            log_info "Running actionlint..."
            if ! actionlint; then
                log_error "actionlint failed!"
                exit_code=1
            fi
        fi

        if [[ "$has_actionlint" -eq 0 ]]; then
            if [[ "$has_wf_changes" -eq 1 ]]; then
                log_error "actionlint is not installed, but workflow changes are detected! Install it to proceed."
                log_error "To install: brew install actionlint"
                exit_code=1
            else
                log_warn "actionlint is not installed. Skipping GitHub Actions schema check."
                log_warn "To install: brew install actionlint"
            fi
        fi

        # 3. zizmor (Warning only, per user feedback "nie uzywaj lokalnie zizmora")
        local has_zizmor=0
        if command -v zizmor &>/dev/null; then
            has_zizmor=1
            log_info "Running zizmor..."
            if ! zizmor .github/workflows; then
                log_error "zizmor scan failed!"
                exit_code=1
            fi
        elif command -v pipx &>/dev/null; then
            has_zizmor=1
            log_info "Running zizmor via pipx..."
            if ! pipx run zizmor .github/workflows; then
                log_error "zizmor scan failed!"
                exit_code=1
            fi
        fi

        if [[ "$has_zizmor" -eq 0 ]]; then
            log_warn "zizmor is not installed. Skipping workflow security check."
            log_warn "To install: pipx install zizmor  OR  pip install zizmor"
        fi

        return "$exit_code"
    )
}

main() {
    log_info "Starting pre-commit workflow validation..."
    if ! validate_workflows; then
        log_error "Pre-commit validation failed. Please fix the linting errors above before committing."
        exit 1
    fi
    log_info "Pre-commit validation passed successfully."
}

main "$@"
