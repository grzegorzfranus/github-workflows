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

        # Check for yamllint
        if command -v yamllint &>/dev/null; then
            log_info "Running yamllint..."
            if ! yamllint .github/workflows/*.yml .github/ISSUE_TEMPLATE/*.yml; then
                log_error "yamllint failed!"
                exit_code=1
            fi
        elif command -v pipx &>/dev/null; then
            log_info "Running yamllint via pipx..."
            if ! pipx run yamllint .github/workflows/*.yml .github/ISSUE_TEMPLATE/*.yml; then
                log_error "yamllint failed!"
                exit_code=1
            fi
        else
            log_warn "yamllint is not installed. Skipping YAML lint check."
            log_warn "To install yamllint, run: brew install yamllint  OR  pip install yamllint"
        fi

        # Check for actionlint
        if command -v actionlint &>/dev/null; then
            log_info "Running actionlint..."
            if ! actionlint; then
                log_error "actionlint failed!"
                exit_code=1
            fi
        else
            log_warn "actionlint is not installed. Skipping GitHub Actions schema check."
            log_warn "To install actionlint, run: brew install actionlint"
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
