#!/usr/bin/env python3
"""Run a dependency-free installation and file health check."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


def read_utf8(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "root",
        nargs="?",
        type=Path,
        default=Path(__file__).resolve().parents[4],
        help="app-spec-coach repository root (default: inferred from this script)",
    )
    args = parser.parse_args()
    root = args.root.resolve()
    skill = root / ".agents/skills/app-spec-coach/SKILL.md"
    references = root / ".agents/skills/app-spec-coach/references"
    checks: list[tuple[bool, str]] = []

    checks.append((sys.version_info >= (3, 9), f"Python >= 3.9 ({sys.version.split()[0]})"))
    checks.append((root.is_dir(), f"repository root: {root}"))
    checks.append((skill.is_file(), f"Skill file: {skill}"))
    checks.append((references.is_dir(), f"reference directory: {references}"))

    if skill.is_file():
        try:
            text = read_utf8(skill)
            checks.append((text.startswith("---\n"), "SKILL.md frontmatter starts correctly"))
            checks.append((bool(re.search(r"^name:\s*\"app-spec-coach\"\s*$", text, re.MULTILINE)), "Skill name is app-spec-coach"))
            checks.append(("구현 승인" in text, "implementation approval rule is present"))
        except (OSError, UnicodeDecodeError) as exc:
            checks.append((False, f"SKILL.md is readable as UTF-8 ({exc})"))

    if references.is_dir():
        reference_files = sorted(references.glob("*.md"))
        checks.append((len(reference_files) >= 10, f"reference files found: {len(reference_files)}"))
        for path in reference_files:
            try:
                read_utf8(path)
                checks.append((True, f"UTF-8 readable: {path.name}"))
            except (OSError, UnicodeDecodeError) as exc:
                checks.append((False, f"UTF-8 readable: {path.name} ({exc})"))

    failed = 0
    for passed, message in checks:
        print(f"[{'PASS' if passed else 'FAIL'}] {message}")
        failed += int(not passed)

    print(f"\nResult: {'PASS' if failed == 0 else 'FAIL'}; checks={len(checks)}; failures={failed}")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())

