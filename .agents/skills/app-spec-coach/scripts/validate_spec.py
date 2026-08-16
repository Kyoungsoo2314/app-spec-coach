#!/usr/bin/env python3
"""Validate the App Spec Coach repository and a locked SPEC file.

This script intentionally uses only Python's standard library so a beginner can
run it immediately after installing the Skill repository.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


REFERENCE_FILES = [
    "interview-policy.md",
    "ambiguity-rubric.md",
    "risk-depth.md",
    "workflow-and-ui.md",
    "visual-review.md",
    "spec-template.md",
    "spec-lock.md",
    "implementation-contract.md",
    "verification-policy.md",
    "coexistence.md",
]

REQUIRED_FILES = [
    "README.md",
    "LICENSE",
    "VERSION",
    "CHANGELOG.md",
    "SPEC.md",
    "IMPLEMENTATION_CONTRACT.md",
    ".agents/skills/app-spec-coach/SKILL.md",
    "evals/cases.yaml",
    "evals/README.md",
    "evals/manual-smoke-tests.md",
    "examples/small-personal-tool.md",
    "examples/business-data-app.md",
    "examples/sensitive-multiuser-app.md",
    "docs/installation.md",
    "docs/update.md",
    "docs/philosophy.md",
    "docs/troubleshooting.md",
    "docs/implementation-prompt.md",
]

FORBIDDEN_MODEL_PATTERNS = [
    re.compile(r"\bgpt-[0-9]", re.IGNORECASE),
    re.compile(r"\bdall[-_ ]e\b", re.IGNORECASE),
]


class Validator:
    def __init__(self, root: Path) -> None:
        self.root = root
        self.errors: list[str] = []
        self.passes: list[str] = []

    def check(self, condition: bool, message: str) -> None:
        if condition:
            self.passes.append(message)
        else:
            self.errors.append(message)

    def read(self, relative: str) -> str | None:
        path = self.root / relative
        try:
            return path.read_text(encoding="utf-8")
        except FileNotFoundError:
            self.errors.append(f"missing file: {relative}")
        except UnicodeDecodeError as exc:
            self.errors.append(f"not UTF-8: {relative} ({exc})")
        except OSError as exc:
            self.errors.append(f"cannot read {relative}: {exc}")
        return None

    def validate_required_files(self) -> None:
        for relative in REQUIRED_FILES:
            path = self.root / relative
            self.check(path.is_file(), f"required file exists: {relative}")
            if path.is_file():
                try:
                    path.read_text(encoding="utf-8")
                    self.passes.append(f"UTF-8 readable: {relative}")
                except (OSError, UnicodeDecodeError) as exc:
                    self.errors.append(f"UTF-8 read failed: {relative} ({exc})")

        ref_root = self.root / ".agents/skills/app-spec-coach/references"
        for name in REFERENCE_FILES:
            self.check((ref_root / name).is_file(), f"reference exists: {name}")

    def validate_skill(self) -> None:
        text = self.read(".agents/skills/app-spec-coach/SKILL.md")
        if text is None:
            return

        self.check(text.startswith("---\n"), "SKILL.md starts with frontmatter")
        parts = text.split("\n---\n", 2)
        self.check(len(parts) == 2, "SKILL.md has closed frontmatter")
        if len(parts) != 2:
            return

        frontmatter, body = parts
        self.check(bool(re.search(r"^name:\s*\"app-spec-coach\"\s*$", frontmatter, re.MULTILINE)), "Skill name is app-spec-coach")
        self.check(bool(re.search(r"^description:\s*\".+\"\s*$", frontmatter, re.MULTILINE)), "Skill description is present")

        for marker in (
            "명세가 부족한 신규 앱 요청",
            "모호함",
            "SPEC LOCK",
            "구현 승인",
            "NOT RUN",
            "호출 가능한 이미지 생성 capability",
            "같은 턴에 실제 이미지 생성 도구를 호출",
            "초보자용 시각 checkpoint",
        ):
            self.check(marker in body, f"SKILL.md contains behavior: {marker}")

        for pattern in FORBIDDEN_MODEL_PATTERNS:
            self.check(not pattern.search(text), f"SKILL.md has no hard-coded model ID matching {pattern.pattern}")

    def validate_spec(self) -> None:
        text = self.read("SPEC.md")
        if text is None:
            return

        checks = {
            "locked status": bool(re.search(r"^status:\s*locked\s*$", text, re.MULTILINE)),
            "spec version": bool(re.search(r"^spec_version:\s*1\.1\s*$", text, re.MULTILINE)),
            "locked heading": "LOCKED SPEC v1.1" in text,
            "interview contract": "## 6. 인터뷰 계약" in text,
            "image contract": "## 9. 화면·이미지 계약" in text,
            "verification statuses": all(token in text for token in ("PASS", "FAIL", "NOT RUN", "BLOCKED")),
            "v1 non-goal": "독립 Windows/Mac 앱" in text,
            "beginner visual checkpoint": "초보자 시각 checkpoint" in text,
        }
        for label, condition in checks.items():
            self.check(condition, f"SPEC has {label}")

    def validate_contract(self) -> None:
        text = self.read("IMPLEMENTATION_CONTRACT.md")
        if text is None:
            return
        for marker in ("AC-01", "AC-04", "AC-08", "AC-10", "AC-12", "AC-13", "PASS", "NOT RUN", "BLOCKED"):
            self.check(marker in text, f"implementation contract contains {marker}")

    def validate_evals(self) -> None:
        text = self.read("evals/cases.yaml")
        if text is None:
            return
        ids = re.findall(r"^  - id:\s*(E\d{2})\s*$", text, re.MULTILINE)
        expected = [f"E{i:02d}" for i in range(1, 16)]
        self.check(ids == expected, f"eval IDs are E01-E15 ({', '.join(ids)})")
        self.check("must_not" in text, "evals include negative behavior")
        self.check("action_contract" in text, "evals use action contracts")
        self.check("must_call_image_capability" in text, "evals require an image capability call")

    def validate_model_policy(self) -> None:
        paths = [
            self.root / ".agents/skills/app-spec-coach/SKILL.md",
            self.root / ".agents/skills/app-spec-coach/references",
        ]
        for path in paths:
            files = [path] if path.is_file() else list(path.glob("*.md"))
            for file_path in files:
                try:
                    text = file_path.read_text(encoding="utf-8")
                except (OSError, UnicodeDecodeError) as exc:
                    self.errors.append(f"cannot inspect model policy file {file_path}: {exc}")
                    continue
                for pattern in FORBIDDEN_MODEL_PATTERNS:
                    self.check(not pattern.search(text), f"no hard-coded model ID in {file_path.name}")

    def run(self) -> int:
        self.validate_required_files()
        self.validate_skill()
        self.validate_spec()
        self.validate_contract()
        self.validate_evals()
        self.validate_model_policy()

        for message in self.passes:
            print(f"[PASS] {message}")
        for message in self.errors:
            print(f"[FAIL] {message}")
        print(f"\nResult: {'PASS' if not self.errors else 'FAIL'}; checks={len(self.passes)}; failures={len(self.errors)}")
        return 0 if not self.errors else 1


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
    if not root.is_dir():
        print(f"[FAIL] repository root does not exist: {root}")
        return 1
    return Validator(root).run()


if __name__ == "__main__":
    sys.exit(main())
