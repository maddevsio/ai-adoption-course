#!/usr/bin/env python3
import re
import sys
from pathlib import Path

COURSE_DIR = Path(__file__).parent.parent / "course"
BUILD_DIR = Path(__file__).parent.parent / "scorm_build"


def is_inside_pre_or_code(text: str, pos: int) -> bool:
    before = text[:pos]
    last_pre_open = before.rfind("<pre")
    last_pre_close = before.rfind("</pre>")
    if last_pre_open > last_pre_close:
        return True
    last_code_open = before.rfind("<code")
    last_code_close = before.rfind("</code>")
    return last_code_open > last_code_close


def check_raw_lists_in_html() -> list[dict[str, str | int]]:
    issues: list[dict[str, str | int]] = []
    for html_file in sorted(BUILD_DIR.rglob("*.html")):
        text = html_file.read_text(encoding="utf-8")
        for m in re.finditer(r'(?m)^- .+', text):
            if is_inside_pre_or_code(text, m.start()):
                continue
            line_num = text[:m.start()].count("\n") + 1
            issues.append({
                "file": str(html_file.relative_to(BUILD_DIR)),
                "line": line_num,
                "text": m.group(0)[:100],
                "type": "raw_list_item",
            })
    return issues


def check_unrendered_bold_in_html() -> list[dict[str, str | int]]:
    issues: list[dict[str, str | int]] = []
    for html_file in sorted(BUILD_DIR.rglob("*.html")):
        text = html_file.read_text(encoding="utf-8")
        for m in re.finditer(r'\*\*[^*]+\*\*', text):
            if is_inside_pre_or_code(text, m.start()):
                continue
            line_num = text[:m.start()].count("\n") + 1
            issues.append({
                "file": str(html_file.relative_to(BUILD_DIR)),
                "line": line_num,
                "text": m.group(0)[:100],
                "type": "unrendered_bold",
            })
    return issues


def check_md_list_after_paragraph() -> list[dict[str, str | int]]:
    issues: list[dict[str, str | int]] = []
    for md_file in sorted(COURSE_DIR.rglob("*.md")):
        lines = md_file.read_text(encoding="utf-8").splitlines()
        for i, line in enumerate(lines):
            if i == 0:
                continue
            prev = lines[i - 1]
            if re.match(r'^- ', line) and prev.strip() and not re.match(r'^- ', prev) and not prev.strip() == '':
                issues.append({
                    "file": str(md_file.relative_to(COURSE_DIR)),
                    "line": i + 1,
                    "text": f"prev: {prev.strip()[:60]}  |  list: {line.strip()[:60]}",
                    "type": "list_missing_blank_line",
                })
    return issues


def check_unrendered_links_in_html() -> list[dict[str, str | int]]:
    issues: list[dict[str, str | int]] = []
    for html_file in sorted(BUILD_DIR.rglob("*.html")):
        text = html_file.read_text(encoding="utf-8")
        for m in re.finditer(r'\[([^\]]+)\]\(([^)]+)\)', text):
            start = max(0, m.start() - 100)
            before = text[start:m.start()]
            if '<code' in before or '<pre' in before:
                continue
            line_num = text[:m.start()].count("\n") + 1
            issues.append({
                "file": str(html_file.relative_to(BUILD_DIR)),
                "line": line_num,
                "text": m.group(0)[:100],
                "type": "unrendered_md_link",
            })
    return issues


def check_html_entities_leaked() -> list[dict[str, str | int]]:
    issues: list[dict[str, str | int]] = []
    for html_file in sorted(BUILD_DIR.rglob("*.html")):
        text = html_file.read_text(encoding="utf-8")
        for m in re.finditer(r'```\w*\n', text):
            start = max(0, m.start() - 100)
            before = text[start:m.start()]
            if '<pre' in before or '<code' in before:
                continue
            line_num = text[:m.start()].count("\n") + 1
            issues.append({
                "file": str(html_file.relative_to(BUILD_DIR)),
                "line": line_num,
                "text": m.group(0).strip()[:60],
                "type": "unrendered_code_fence",
            })
    return issues


def main() -> int:
    if not BUILD_DIR.exists():
        print(f"Build dir not found: {BUILD_DIR}")
        print("Run build_scorm.py first.")
        return 1

    all_issues: list[dict[str, str | int]] = []
    print("Checking for formatting issues...\n")

    print("1. Raw list items in HTML (markdown list not rendered)...")
    issues = check_raw_lists_in_html()
    all_issues.extend(issues)
    print(f"   Found: {len(issues)}")

    print("2. Unrendered **bold** in HTML...")
    issues = check_unrendered_bold_in_html()
    all_issues.extend(issues)
    print(f"   Found: {len(issues)}")

    print("3. Markdown lists missing blank line before them (source)...")
    issues = check_md_list_after_paragraph()
    all_issues.extend(issues)
    print(f"   Found: {len(issues)}")

    print("4. Unrendered markdown links in HTML...")
    issues = check_unrendered_links_in_html()
    all_issues.extend(issues)
    print(f"   Found: {len(issues)}")

    print("5. Unrendered code fences in HTML...")
    issues = check_html_entities_leaked()
    all_issues.extend(issues)
    print(f"   Found: {len(issues)}")

    if not all_issues:
        print("\nNo formatting issues found!")
        return 0

    print(f"\n{'='*80}")
    print(f"Total issues: {len(all_issues)}")
    print(f"{'='*80}\n")

    by_type: dict[str, list[dict[str, str | int]]] = {}
    for issue in all_issues:
        by_type.setdefault(str(issue["type"]), []).append(issue)

    for issue_type, items in by_type.items():
        print(f"\n--- {issue_type} ({len(items)} issues) ---")
        for item in items:
            print(f"  {item['file']}:{item['line']}")
            print(f"    {item['text']}")

    return 1


if __name__ == "__main__":
    sys.exit(main())
