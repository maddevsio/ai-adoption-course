#!/usr/bin/env python3
import os
import re
import sys

COURSE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "course")

MODULE_NAMES = {
    "module-0-intro": "Модуль 0. Введение",
    "module-1-why-ai": "Модуль 1. Зачем ИИ",
    "module-2-tools": "Модуль 2. Инструменты",
    "module-3-prompting": "Модуль 3. Промптинг",
    "module-4-agents": "Модуль 4. Агенты",
    "module-5-context-engineering": "Модуль 5. Context Engineering",
    "module-6-mcp": "Модуль 6. MCP",
    "module-7-orchestration": "Модуль 7. Оркестрация",
    "module-8-responsibility": "Модуль 8. Ответственность",
    "module-9-final": "Модуль 9. Финал",
}

SUBDIR_NAMES = {
    "theory": "Теория",
    "practice": "Практика",
    "diagrams": "Диаграммы",
    "templates": "Шаблоны",
}

NAV_LINK_RE = re.compile(r"^\[← Оглавление\]\([^)]+\)\s*\n\s*\n")

SPACE = "CTO"
TOP_PARENT = "AI adoption course"


def compute_parents(rel_path):
    parts = rel_path.split(os.sep)
    parents = [TOP_PARENT]
    if len(parts) >= 2 and parts[0] in MODULE_NAMES:
        parents.append(MODULE_NAMES[parts[0]])
    if len(parts) >= 3 and parts[1] in SUBDIR_NAMES:
        parents.append(SUBDIR_NAMES[parts[1]])
    return parents


def build_headers(parents, attachments=None):
    lines = [f"<!-- Space: {SPACE} -->"]
    for p in parents:
        lines.append(f"<!-- Parent: {p} -->")
    if attachments:
        for a in attachments:
            lines.append(f"<!-- Attachment: {a} -->")
    return "\n".join(lines) + "\n\n"


def process_file(filepath, rel_path):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    content = NAV_LINK_RE.sub("", content)

    parents = compute_parents(rel_path)

    attachments = None
    if rel_path == os.path.join("module-1-why-ai", "03-yegge-levels.md"):
        attachments = ["diagrams/yegge-8-levels.png"]

    header = build_headers(parents, attachments)
    content = header + content

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"  ✓ {rel_path}")


def main():
    dry_run = "--dry-run" in sys.argv
    count = 0
    for root, dirs, files in os.walk(COURSE_DIR):
        for fname in sorted(files):
            if not fname.endswith(".md"):
                continue
            filepath = os.path.join(root, fname)
            rel_path = os.path.relpath(filepath, COURSE_DIR)
            if dry_run:
                parents = compute_parents(rel_path)
                print(f"  {rel_path} → {' > '.join(parents)}")
            else:
                process_file(filepath, rel_path)
            count += 1
    print(f"\n{'Would process' if dry_run else 'Processed'} {count} files")


if __name__ == "__main__":
    main()
