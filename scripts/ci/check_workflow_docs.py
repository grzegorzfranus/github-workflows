#!/usr/bin/env python3
"""Workflow documentation parity checker.

Verifies that every reusable workflow in .github/workflows/ has a matching
documentation page in docs/workflows/<stem>.md, that inputs, secrets, and
outputs declared in the workflow YAML match the documentation tables, that
descriptions are identical, that secrets referenced in the workflow are
declared, and that usage examples in documentation are valid.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple

import yaml

# Resolves repository root from its own location (two levels up)
REPO_ROOT = Path(__file__).resolve().parent.parent.parent


def normalize_description(text: str) -> str:
    """Normalise description for comparison.

    Removes backticks, single quotes, double quotes, collapses whitespace,
    strips, and removes one trailing dot. Case-sensitive.
    """
    s = re.sub(r"[`'\"]", "", text)
    s = re.sub(r"\s+", " ", s)
    s = s.strip()
    if s.endswith("."):
        s = s[:-1]
    return s


def strip_cell_backticks(val: str) -> str:
    """Strip enclosing backticks from a markdown table cell."""
    s = val.strip()
    return re.sub(r"^`+|`+$", "", s).strip()


def parse_row(line: str) -> List[str]:
    """Split cells on '|' not preceded by backslash, strip each, unescape \\|."""
    line = line.strip()
    parts = re.split(r"(?<!\\)\|", line)
    if parts and parts[0] == "":
        parts = parts[1:]
    if parts and parts[-1] == "":
        parts = parts[:-1]
    return [p.strip().replace(r"\|", "|") for p in parts]


def extract_sections(content: str) -> Dict[str, List[str]]:
    """Extract sections keyed by title (e.g. 'Inputs', 'Secrets', 'Outputs').

    A section starts with a line '## <Title>' and ends at the next line starting
    with '## ' or at the end of the file.
    """
    sections: Dict[str, List[str]] = {}
    lines = content.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.startswith("## "):
            title = line[3:].strip()
            section_lines: List[str] = []
            i += 1
            while i < len(lines) and not lines[i].startswith("## "):
                section_lines.append(lines[i])
                i += 1
            sections[title] = section_lines
        else:
            i += 1
    return sections


def extract_table(
    section_lines: List[str],
) -> Optional[Tuple[List[str], List[List[str]]]]:
    """Extract the first markdown table from section lines.

    The table is the first contiguous block of lines starting with '|'.
    Row 0 is header, row 1 is separator matching ^\\|\\s*:?-+.
    Returns (headers, data_rows) or None if no valid table is present.
    """
    tbl_lines: List[str] = []
    in_table = False
    for line in section_lines:
        if line.startswith("|"):
            tbl_lines.append(line)
            in_table = True
        elif in_table:
            break

    if len(tbl_lines) < 2:
        return None

    if not re.match(r"^\|\s*:?-+", tbl_lines[1]):
        return None

    headers = parse_row(tbl_lines[0])
    rows = [parse_row(r) for r in tbl_lines[2:]]
    return headers, rows


def find_reusable_workflows(
    repo_root: Path,
) -> Dict[str, Tuple[Path, dict]]:
    """Discover all reusable workflows in .github/workflows/.

    A reusable workflow is any *.yml or *.yaml whose top-level 'on' mapping
    contains 'workflow_call'.
    """
    workflows: Dict[str, Tuple[Path, dict]] = {}
    workflows_dir = repo_root / ".github" / "workflows"
    if not workflows_dir.is_dir():
        return workflows

    for wf_path in sorted(workflows_dir.glob("*.y*ml")):
        if not wf_path.is_file():
            continue
        try:
            with open(wf_path, encoding="utf-8") as f:
                data = yaml.safe_load(f)
        except Exception:
            continue

        if not isinstance(data, dict):
            continue

        on_data = data.get("on") if "on" in data else data.get(True)
        if isinstance(on_data, dict) and "workflow_call" in on_data:
            stem = wf_path.name
            if stem.endswith(".yml"):
                stem = stem[:-4]
            elif stem.endswith(".yaml"):
                stem = stem[:-5]
            workflows[stem] = (wf_path, data)

    return workflows


def find_workflow_docs(repo_root: Path) -> Dict[str, Path]:
    """Discover all workflow documentation pages in docs/workflows/*.md."""
    docs: Dict[str, Path] = {}
    docs_dir = repo_root / "docs" / "workflows"
    if not docs_dir.is_dir():
        return docs

    for doc_path in sorted(docs_dir.glob("*.md")):
        if doc_path.is_file():
            docs[doc_path.stem] = doc_path

    return docs


def check_undeclared_secrets(
    wf_rel: str,
    wf_content: str,
    wc_secrets: dict,
    problems: List[str],
) -> None:
    """Report every secrets.NAME in workflow file not declared in workflow_call."""
    declared = set(wc_secrets.keys())
    seen: Set[str] = set()
    for m in re.finditer(r"secrets\.([A-Za-z0-9_-]+)", wf_content):
        sec = m.group(1)
        if sec == "GITHUB_TOKEN" or sec in seen:
            continue
        seen.add(sec)
        if sec not in declared:
            problems.append(
                f"::error file={wf_rel}::Undeclared secret '{sec}' referenced in workflow"
            )


def check_table_columns(
    doc_rel: str,
    section_title: str,
    yaml_key: str,
    col_indices: Dict[str, int],
    problems: List[str],
) -> None:
    """Validate that all required columns are present in the table header."""
    req_cols: List[str] = []
    if yaml_key == "inputs":
        req_cols = ["type", "required", "default", "description"]
    elif yaml_key == "secrets":
        req_cols = ["required", "description"]
    elif yaml_key == "outputs":
        req_cols = ["description"]

    for col in req_cols:
        if col not in col_indices:
            problems.append(
                f"::error file={doc_rel}::Missing required column '{col.capitalize()}' in {section_title} table"
            )


def check_input_row(
    doc_rel: str,
    name: str,
    doc_row: Dict[str, str],
    y_entry: dict,
    col_indices: Dict[str, int],
    problems: List[str],
) -> None:
    """Validate type, required, and default values for an input row."""
    if "type" in col_indices:
        doc_type = doc_row.get("type", "").strip()
        yaml_type = str(y_entry.get("type", "")).strip()
        if doc_type != yaml_type:
            problems.append(
                f"::error file={doc_rel}::Type mismatch for input '{name}': doc has '{doc_type}', YAML has '{yaml_type}'"
            )

    if "required" in col_indices:
        doc_req = doc_row.get("required", "").strip()
        yaml_req = "yes" if y_entry.get("required") is True else "no"
        if doc_req != yaml_req:
            problems.append(
                f"::error file={doc_rel}::Required mismatch for input '{name}': doc has '{doc_req}', YAML has '{yaml_req}'"
            )

    if "default" in col_indices:
        doc_def = strip_cell_backticks(doc_row.get("default", ""))
        has_default = "default" in y_entry and y_entry["default"] is not None
        if not has_default:
            if doc_def not in ("—", "-"):
                problems.append(
                    f"::error file={doc_rel}::Default mismatch for input '{name}': doc has '{doc_def}', YAML has no default (expected '—' or '-')"
                )
        else:
            y_def = y_entry["default"]
            if isinstance(y_def, str) and "\n" in y_def:
                if not doc_def:
                    problems.append(
                        f"::error file={doc_rel}::Default mismatch for input '{name}': doc has empty default, YAML has multi-line default"
                    )
            elif isinstance(y_def, bool):
                exp = "true" if y_def else "false"
                if doc_def != exp:
                    problems.append(
                        f"::error file={doc_rel}::Default mismatch for input '{name}': doc has '{doc_def}', YAML has '{exp}'"
                    )
            elif y_def == "":
                if doc_def not in ('""', "''"):
                    problems.append(
                        f"::error file={doc_rel}::Default mismatch for input '{name}': doc has '{doc_def}', YAML has empty string (expected '\"\"' or '\'\'')"
                    )
            else:
                exp = str(y_def)
                if doc_def != exp:
                    problems.append(
                        f"::error file={doc_rel}::Default mismatch for input '{name}': doc has '{doc_def}', YAML has '{exp}'"
                    )


def check_secret_row(
    doc_rel: str,
    name: str,
    doc_row: Dict[str, str],
    y_entry: dict,
    col_indices: Dict[str, int],
    problems: List[str],
) -> None:
    """Validate required and required-when values for a secret row."""
    yaml_req_bool = y_entry.get("required") is True
    if "required" in col_indices:
        doc_req = doc_row.get("required", "").strip()
        exp_req = "yes" if yaml_req_bool else "no"
        if doc_req != exp_req:
            problems.append(
                f"::error file={doc_rel}::Required mismatch for secret '{name}': doc has '{doc_req}', YAML has '{exp_req}'"
            )

    if "required when" in col_indices:
        if not yaml_req_bool:
            req_when = doc_row.get("required when", "").strip()
            if not req_when:
                problems.append(
                    f"::error file={doc_rel}::Secret '{name}' is not required, so 'Required when' column must not be empty"
                )


def check_section_items(
    doc_rel: str,
    wf_rel: str,
    section_title: str,
    yaml_key: str,
    kind: str,
    wc: dict,
    sections: Dict[str, List[str]],
    problems: List[str],
) -> None:
    """Compare Inputs/Secrets/Outputs section between docs and workflow YAML."""
    yaml_entries = wc.get(yaml_key) or {}
    has_yaml = bool(yaml_entries)
    section_lines = sections.get(section_title)
    tbl_info = extract_table(section_lines) if section_lines else None
    has_table = tbl_info is not None

    if has_yaml and not has_table:
        problems.append(
            f"::error file={doc_rel}::Missing {section_title} section or table when YAML declares {yaml_key}"
        )
        return

    if not has_yaml and has_table:
        problems.append(
            f"::error file={doc_rel}::{section_title} table present in documentation when YAML declares none"
        )
        return

    if not has_yaml and not has_table:
        return

    assert tbl_info is not None
    headers, rows = tbl_info

    # Columns located by header text, case-insensitively
    col_indices: Dict[str, int] = {"name": 0}
    for idx, h in enumerate(headers[1:], start=1):
        hl = h.strip().lower()
        if hl in ("type", "required", "required when", "default", "description"):
            col_indices[hl] = idx

    check_table_columns(doc_rel, section_title, yaml_key, col_indices, problems)

    doc_rows: List[Dict[str, str]] = []
    for r in rows:
        name = strip_cell_backticks(r[0])
        row_dict: Dict[str, str] = {"name": name}
        for col_name, c_idx in col_indices.items():
            if col_name != "name":
                row_dict[col_name] = r[c_idx] if c_idx < len(r) else ""
        doc_rows.append(row_dict)

    doc_names = [r["name"] for r in doc_rows]
    yaml_names = list(yaml_entries.keys())

    # Check missing YAML descriptions
    for y_name, y_entry in yaml_entries.items():
        desc = y_entry.get("description") if isinstance(y_entry, dict) else None
        if desc is None or str(desc).strip() == "":
            problems.append(
                f"::error file={wf_rel}::Missing description in YAML for {kind} '{y_name}'"
            )

    # Names: missing names, extra names, order differences reported separately
    missing = [n for n in yaml_names if n not in doc_names]
    if missing:
        problems.append(
            f"::error file={doc_rel}::Missing {kind}(s) in documentation: {', '.join(missing)}"
        )

    extra = [n for n in doc_names if n not in yaml_names]
    if extra:
        problems.append(
            f"::error file={doc_rel}::Extra {kind}(s) in documentation not declared in YAML: {', '.join(extra)}"
        )

    common_yaml = [n for n in yaml_names if n in doc_names]
    common_doc = [n for n in doc_names if n in yaml_names]
    if common_yaml != common_doc:
        problems.append(
            f"::error file={doc_rel}::Order difference in {section_title} table between documentation and YAML"
        )

    # Compare row properties for entries in both doc and YAML
    for r in doc_rows:
        name = r["name"]
        if name not in yaml_entries:
            continue
        y_entry = yaml_entries[name]
        if not isinstance(y_entry, dict):
            continue

        # Description check
        if "description" in col_indices:
            doc_desc = r.get("description", "")
            yaml_desc = str(y_entry.get("description") or "")
            if normalize_description(doc_desc) != normalize_description(yaml_desc):
                problems.append(
                    f"::error file={doc_rel}::Description mismatch for {kind} '{name}': doc={doc_desc!r} vs yaml={yaml_desc!r}"
                )

        if yaml_key == "inputs":
            check_input_row(doc_rel, name, r, y_entry, col_indices, problems)
        elif yaml_key == "secrets":
            check_secret_row(doc_rel, name, r, y_entry, col_indices, problems)


def check_usage_examples(
    doc_rel: str,
    doc_content: str,
    reusable_wfs: Dict[str, Tuple[Path, dict]],
    problems: List[str],
) -> None:
    """Verify all yaml/yml code blocks and caller job specifications."""
    block_pattern = re.compile(
        r"^```(?:yaml|yml)[ \t]*\r?\n(.*?)\r?\n```", re.MULTILINE | re.DOTALL
    )
    for block in block_pattern.findall(doc_content):
        try:
            parsed = yaml.safe_load(block)
        except yaml.YAMLError as err:
            problems.append(
                f"::error file={doc_rel}::YAML parse error in usage example: {err}"
            )
            continue

        if not isinstance(parsed, dict):
            continue
        jobs = parsed.get("jobs")
        if not isinstance(jobs, dict):
            continue

        for j_name, j_spec in jobs.items():
            if not isinstance(j_spec, dict):
                continue
            uses_str = j_spec.get("uses")
            if not isinstance(uses_str, str):
                continue

            m = re.search(r"\.github/workflows/([^/@]+)\.ya?ml(?:@|$)", uses_str)
            if not m:
                continue
            called_stem = m.group(1)
            if called_stem not in reusable_wfs:
                continue

            _, called_wf_data = reusable_wfs[called_stem]
            called_on = (
                called_wf_data.get("on")
                if "on" in called_wf_data
                else called_wf_data.get(True)
            )
            called_wc = (called_on or {}).get("workflow_call") or {}
            called_inputs = called_wc.get("inputs") or {}
            called_secrets = called_wc.get("secrets") or {}

            # secrets: inherit -> report
            if j_spec.get("secrets") == "inherit":
                problems.append(
                    f"::error file={doc_rel}::Usage example job '{j_name}' uses 'secrets: inherit'"
                )
            elif isinstance(j_spec.get("secrets"), dict):
                job_secrets = j_spec["secrets"]
                for sec_key in job_secrets.keys():
                    if sec_key not in called_secrets:
                        problems.append(
                            f"::error file={doc_rel}::Usage example job '{j_name}' passes undeclared secret '{sec_key}' to '{called_stem}'"
                        )
                for sec_name, sec_info in called_secrets.items():
                    if isinstance(sec_info, dict) and sec_info.get("required") is True:
                        if sec_name not in job_secrets:
                            problems.append(
                                f"::error file={doc_rel}::Usage example job '{j_name}' missing required secret '{sec_name}' for '{called_stem}'"
                            )

            # with
            if isinstance(j_spec.get("with"), dict):
                job_with = j_spec["with"]
                for inp_key in job_with.keys():
                    if inp_key not in called_inputs:
                        problems.append(
                            f"::error file={doc_rel}::Usage example job '{j_name}' passes undeclared input '{inp_key}' to '{called_stem}'"
                        )
                for inp_name, inp_info in called_inputs.items():
                    if isinstance(inp_info, dict):
                        if (
                            inp_info.get("required") is True
                            and "default" not in inp_info
                        ):
                            if inp_name not in job_with:
                                problems.append(
                                    f"::error file={doc_rel}::Usage example job '{j_name}' missing required input '{inp_name}' without default for '{called_stem}'"
                                )


def main() -> int:
    """Run all workflow documentation parity checks and return exit code."""
    repo_root = REPO_ROOT
    problems: List[str] = []

    reusable_wfs = find_reusable_workflows(repo_root)
    doc_pages = find_workflow_docs(repo_root)

    # Discovery checks
    for stem, (wf_path, _) in reusable_wfs.items():
        if stem not in doc_pages:
            problems.append(
                f"::error file=docs/workflows/{stem}.md::Reusable workflow '.github/workflows/{wf_path.name}' has no matching documentation page"
            )

    for stem, doc_path in doc_pages.items():
        if stem not in reusable_wfs:
            doc_rel = doc_path.relative_to(repo_root).as_posix()
            problems.append(
                f"::error file={doc_rel}::Documentation page has no matching reusable workflow in .github/workflows/"
            )

    # Check each reusable workflow against its documentation page
    for stem in sorted(reusable_wfs.keys()):
        if stem not in doc_pages:
            continue

        wf_path, wf_data = reusable_wfs[stem]
        doc_path = doc_pages[stem]

        wf_rel = wf_path.relative_to(repo_root).as_posix()
        doc_rel = doc_path.relative_to(repo_root).as_posix()

        with open(wf_path, encoding="utf-8") as f:
            wf_content = f.read()
        with open(doc_path, encoding="utf-8") as f:
            doc_content = f.read()

        on_data = (
            wf_data.get("on") if "on" in wf_data else wf_data.get(True)
        )
        wc = on_data.get("workflow_call") or {}

        # Undeclared secrets
        wc_secrets = wc.get("secrets") or {}
        check_undeclared_secrets(wf_rel, wf_content, wc_secrets, problems)

        # Sections and tables
        sections = extract_sections(doc_content)
        for section_title, yaml_key, kind in [
            ("Inputs", "inputs", "input"),
            ("Secrets", "secrets", "secret"),
            ("Outputs", "outputs", "output"),
        ]:
            check_section_items(
                doc_rel,
                wf_rel,
                section_title,
                yaml_key,
                kind,
                wc,
                sections,
                problems,
            )

        # Usage examples
        check_usage_examples(doc_rel, doc_content, reusable_wfs, problems)

    # Output results
    for p in problems:
        print(p)

    wf_count = len(reusable_wfs)
    prob_count = len(problems)
    summary_suffix = "problems" if prob_count != 1 else "problem"
    print(f"Checked {wf_count} reusable workflows: {prob_count} {summary_suffix}")

    return 0 if prob_count == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
