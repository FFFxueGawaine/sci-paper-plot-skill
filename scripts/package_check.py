# -*- coding: utf-8 -*-
"""Pre-package checks for the sci-paper-plot-skill package."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


TEXT_EXTS = {".md", ".py", ".txt", ".yaml", ".yml", ".toml", ".json"}
EXPECTED_SKILL_NAME = "sci-paper-plot-skill"
FORBIDDEN_DOC_NAMES = {
    "INSTALLATION_GUIDE.md",
    "QUICK_REFERENCE.md",
    "CHANGELOG.md",
}
GENERATED_OUTPUT_EXTS = {".png", ".jpg", ".jpeg", ".tif", ".tiff", ".pdf", ".svg"}
REQUIRED_FILES = [
    "SKILL.md",
    "README.md",
    "requirements.txt",
    "agents/openai.yaml",
    "scripts/scimplstyle_mssp.py",
    "scripts/scimplstyle_mssp_cli.py",
    "scripts/audit_figures.py",
    "references/mssp-compact-dynamics-style.md",
    "references/adaptation-guide.md",
    "references/mssp-nonlinear-dynamics-examples.md",
    "references/hb-clearance-paper-figure-templates.md",
    "references/machine-learning-figure-examples.md",
    "references/matplotlib-gallery-examples.md",
]


def read_text(path: Path) -> str:
    with path.open("r", encoding="utf-8", newline="") as f:
        return f.read()


def check_required_files(root: Path) -> list[str]:
    problems: list[str] = []
    for rel_path in REQUIRED_FILES:
        if not (root / rel_path).is_file():
            problems.append(f"missing required file: {rel_path}")
    return problems


def check_skill_frontmatter(root: Path) -> list[str]:
    problems: list[str] = []
    skill_md = root / "SKILL.md"
    text = read_text(skill_md)
    if root.name != EXPECTED_SKILL_NAME:
        problems.append(f"skill folder should be named {EXPECTED_SKILL_NAME}, found {root.name}")
    if not text.startswith("---\n"):
        problems.append("SKILL.md frontmatter is missing")
    if f"\nname: {EXPECTED_SKILL_NAME}\n" not in text:
        problems.append("SKILL.md frontmatter name is missing or unexpected")
    if "\ndescription:" not in text:
        problems.append("SKILL.md frontmatter description is missing")
    if text.count("\n") > 500:
        problems.append("SKILL.md should stay under 500 lines for progressive disclosure")
    return problems


def check_agents_metadata(root: Path) -> list[str]:
    problems: list[str] = []
    path = root / "agents" / "openai.yaml"
    text = read_text(path)
    required_terms = [
        "display_name:",
        "short_description:",
        "default_prompt:",
        EXPECTED_SKILL_NAME,
        "MSSP",
        "Matplotlib",
    ]
    for term in required_terms:
        if term not in text:
            problems.append(f"agents/openai.yaml missing `{term}`")
    return problems


def check_no_cache_files(root: Path) -> list[str]:
    problems: list[str] = []
    for path in root.rglob("*"):
        if path.name == "__pycache__" and path.is_dir():
            problems.append(f"cache directory should not be packaged: {path.relative_to(root)}")
        elif path.suffix.lower() in {".pyc", ".pyo"}:
            problems.append(f"bytecode file should not be packaged: {path.relative_to(root)}")
    return problems


def check_no_forbidden_docs(root: Path) -> list[str]:
    problems: list[str] = []
    for path in root.rglob("*"):
        if path.is_file() and path.name in FORBIDDEN_DOC_NAMES:
            problems.append(f"extra documentation should not be packaged in a skill: {path.relative_to(root)}")
    return problems


def check_no_generated_outputs(root: Path) -> list[str]:
    problems: list[str] = []
    for path in root.rglob("*"):
        if path.is_file() and path.suffix.lower() in GENERATED_OUTPUT_EXTS:
            rel_path = path.relative_to(root)
            if rel_path.parts[:2] == ("assets", "examples") and path.suffix.lower() == ".png":
                continue
            problems.append(f"generated output should not be packaged: {path.relative_to(root)}")
    return problems


def check_no_private_paths(root: Path) -> list[str]:
    problems: list[str] = []
    drive_path_re = re.compile(r"(?<![A-Za-z0-9_])[A-Za-z]:[\\/]")
    private_terms = ["AI" + "-Workspace", "demo" + "_plots"]
    for path in root.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in TEXT_EXTS:
            continue
        if path.name == "package_check.py":
            continue
        text = read_text(path)
        if drive_path_re.search(text):
            problems.append(f"local drive path remains in {path.relative_to(root)}")
        for term in private_terms:
            if term in text:
                problems.append(f"private term `{term}` remains in {path.relative_to(root)}")
    return problems


def check_python_syntax(root: Path) -> list[str]:
    problems: list[str] = []
    for path in root.rglob("*.py"):
        if "__pycache__" in path.parts:
            continue
        try:
            compile(read_text(path), str(path), "exec")
        except SyntaxError as exc:
            problems.append(f"syntax error in {path.relative_to(root)}: {exc}")
    return problems


def check_demo_count(root: Path, expected_minimum: int = 20) -> list[str]:
    demos = sorted((root / "scripts" / "demos").glob("demo_*.py"))
    if len(demos) < expected_minimum:
        return [f"expected at least {expected_minimum} demos, found {len(demos)}"]
    return []


def run_checks(root: Path) -> list[str]:
    checks = [
        check_required_files,
        check_skill_frontmatter,
        check_agents_metadata,
        check_no_cache_files,
        check_no_forbidden_docs,
        check_no_generated_outputs,
        check_no_private_paths,
        check_python_syntax,
        check_demo_count,
    ]
    problems: list[str] = []
    for check in checks:
        problems.extend(check(root))
    return problems


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "root",
        nargs="?",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="Skill root directory",
    )
    args = parser.parse_args()
    root = args.root.resolve()
    problems = run_checks(root)
    if problems:
        for problem in problems:
            print(f"FAIL: {problem}")
        raise SystemExit(1)
    print("package_check: OK")


if __name__ == "__main__":
    main()
