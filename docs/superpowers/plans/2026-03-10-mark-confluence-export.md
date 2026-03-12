# Mark Confluence Export — Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add mark headers to all 90 markdown files in `course/` so they can be published to Confluence space CTO under "AI adoption course" page.

**Architecture:** A Python script walks `course/`, computes parent chain from directory path, and prepends `<!-- Space -->` + `<!-- Parent -->` headers. It also handles the one image attachment and removes nav links. Then we review and adjust generated headers manually.

**Tech Stack:** Python 3, mark CLI

---

## File Structure

- Create: `scripts/inject-mark-headers.py` — script that injects headers
- Modify: all 90 `.md` files in `course/` — add mark headers at top

## Directory → Confluence Hierarchy Mapping

```
course/GLOSSARY.md              → Parent: "AI adoption course"
course/useful-links.md          → Parent: "AI adoption course"
course/module-0-intro/          → Parent: "AI adoption course" > "Модуль 0. Введение"
course/module-1-why-ai/         → Parent: "AI adoption course" > "Модуль 1. Зачем ИИ"
course/module-1-why-ai/diagrams/→ Parent: ... > "Модуль 1. Зачем ИИ" > "Диаграммы"
course/module-2-tools/theory/   → Parent: ... > "Модуль 2. Инструменты" > "Теория"
course/module-2-tools/practice/ → Parent: ... > "Модуль 2. Инструменты" > "Практика"
course/module-2-tools/diagrams/ → Parent: ... > "Модуль 2. Инструменты" > "Диаграммы"
...same pattern for modules 3-8...
course/module-9-final/          → Parent: "AI adoption course" > "Модуль 9. Финал"
course/module-5-context-engineering/templates/ → Parent: ... > "Модуль 5. Context Engineering" > "Шаблоны"
```

Module name mapping (used in Parent headers):
| Directory name | Confluence parent title |
|---|---|
| module-0-intro | Модуль 0. Введение |
| module-1-why-ai | Модуль 1. Зачем ИИ |
| module-2-tools | Модуль 2. Инструменты |
| module-3-prompting | Модуль 3. Промптинг |
| module-4-agents | Модуль 4. Агенты |
| module-5-context-engineering | Модуль 5. Context Engineering |
| module-6-mcp | Модуль 6. MCP |
| module-7-orchestration | Модуль 7. Оркестрация |
| module-8-responsibility | Модуль 8. Ответственность |
| module-9-final | Модуль 9. Финал |

Subdirectory mapping:
| Subdirectory | Confluence parent title |
|---|---|
| theory | Теория |
| practice | Практика |
| diagrams | Диаграммы |
| templates | Шаблоны |

---

## Chunk 1: Script + Injection

### Task 1: Write the header injection script

**Files:**
- Create: `scripts/inject-mark-headers.py`

- [ ] **Step 1: Write the script**

The script must:
1. Walk all `.md` files in `course/`
2. For each file, compute parent chain from its path relative to `course/`
3. Remove the nav link line (`[← Оглавление](...)\n\n`) if present at the top
4. For `course/module-1-why-ai/03-yegge-levels.md` — add `<!-- Attachment: diagrams/yegge-8-levels.png -->` since it references an image
5. Prepend headers in this order:
   - `<!-- Space: CTO -->`
   - `<!-- Parent: AI adoption course -->`
   - `<!-- Parent: Модуль N. ... -->` (if inside a module dir)
   - `<!-- Parent: Теория|Практика|Диаграммы|Шаблоны -->` (if inside a subdirectory)
6. Do NOT add a `<!-- Title: -->` header (we'll use `--title-from-h1`)

Example output for `course/module-2-tools/theory/01-types-of-tools.md`:
```markdown
<!-- Space: CTO -->
<!-- Parent: AI adoption course -->
<!-- Parent: Модуль 2. Инструменты -->
<!-- Parent: Теория -->

# Типы ИИ-инструментов для разработчика
...
```

Example output for `course/GLOSSARY.md`:
```markdown
<!-- Space: CTO -->
<!-- Parent: AI adoption course -->

# Глоссарий терминов курса
...
```

```python
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
```

- [ ] **Step 2: Dry-run the script**

Run: `python3 scripts/inject-mark-headers.py --dry-run`
Expected: prints all 90 files with their parent chains, no files modified.

- [ ] **Step 3: Run the script for real**

Run: `python3 scripts/inject-mark-headers.py`
Expected: prints 90 files with checkmarks, all files now have headers.

- [ ] **Step 4: Verify a few files**

Run: `head -8 course/module-2-tools/theory/01-types-of-tools.md`
Expected: Space + 3 Parent headers, then blank line, then H1.

Run: `head -6 course/GLOSSARY.md`
Expected: Space + 1 Parent header, then blank line, then H1.

Run: `head -8 course/module-1-why-ai/03-yegge-levels.md`
Expected: Space + 2 Parent headers + Attachment header, then blank line, then H1.

- [ ] **Step 5: Verify nav links removed**

Run: `grep -r "← Оглавление" course/ | wc -l`
Expected: 0

- [ ] **Step 6: Commit**

```bash
git add scripts/inject-mark-headers.py course/
git commit -m "add mark confluence headers to all course markdown files"
```

---

## Chunk 2: Review and adjust headers

### Task 2: Review all generated headers

After the script runs, review every file's headers and adjust:

- [ ] **Step 1: Generate a summary of all headers for review**

Run: `grep -A4 "^<!-- Space:" course/**/*.md | head -400`

Review the output and fix any issues:
- Wrong parent chain
- Missing or wrong module name
- Files that need special treatment

- [ ] **Step 2: Test with mark dry-run**

Run: `mark -f 'course/**/*.md' --title-from-h1 --drop-h1 --features=mermaid --dry-run 2>&1 | head -100`

Check for:
- Title extraction working correctly
- Parent pages resolving
- No errors

- [ ] **Step 3: Fix any issues found in review**

Edit individual files as needed.

- [ ] **Step 4: Commit adjustments**

```bash
git add course/
git commit -m "adjust mark headers after review"
```

---

## Chunk 3: Publish

### Task 3: Publish to Confluence

- [ ] **Step 1: Configure mark auth**

Create `~/.config/mark` with:
```toml
username = "your-email@maddevs.io"
password = "your-api-token"
base-url = "https://maddevs.atlassian.net/wiki"
```

- [ ] **Step 2: Publish one file as test**

Run: `mark -f course/module-0-intro/theory.md --title-from-h1 --drop-h1 --features=mermaid --minor-edit`

Verify the page appears in Confluence under CTO > AI adoption course > Модуль 0. Введение.

- [ ] **Step 3: Publish all files**

Run: `mark -f 'course/**/*.md' --title-from-h1 --drop-h1 --features=mermaid --minor-edit`

- [ ] **Step 4: Verify in Confluence**

Check the page hierarchy matches the expected structure. Verify mermaid diagrams render. Verify the yegge image attachment uploaded.
