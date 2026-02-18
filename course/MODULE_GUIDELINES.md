# Module Content Guidelines

Guidelines for structuring course modules. Based on module-2-tools and module-3-prompting reference implementations.

## Core Principles

### 1. Directory structure: theory/ and practice/

Each module separates content into `theory/` and `practice/` subdirectories. Files are numbered with `NN-` prefix for reading order.

```
module-X-name/
  theory/
    01-first-topic.md       (60-150 lines)
    02-second-topic.md      (60-200 lines)
    03-third-topic.md       (60-200 lines)
  practice/
    01-first-exercise.md    (100-300 lines)
    02-second-exercise.md   (50-200 lines)
    03-checklist.md         (20-50 lines)
```

### 2. No monolithic files

Break large files into focused, topic-scoped documents. A single `theory.md` or `practice.md` covering everything is the anti-pattern.

### 3. File size targets

| Type | Target | Hard max |
|------|--------|----------|
| Theory topic file | 60-200 lines | 300 lines |
| Practice file | 50-300 lines | 400 lines |
| Checklist | 20-50 lines | 80 lines |

If a file exceeds the hard max — split it.

### 4. File naming

Files use `NN-descriptive-name.md` format:
- `NN-` prefix: two-digit number for reading order (`01-`, `02-`, ...)
- `descriptive-name`: describes the content, not the format

**Bad:** `01-theory.md`, `02-practice.md`, `01-part1.md`

**Good:** `01-types-of-tools.md`, `02-available-tools.md`, `01-setup.md`, `02-troubleshooting.md`

### 5. One file — one purpose

Each file should answer one question or cover one topic. If you need a "and also..." — that belongs in a separate file.

Examples from module-2:
- `theory/01-types-of-tools.md` — what categories of AI tools exist
- `theory/02-available-tools.md` — what specific tools are available and at what cost
- `theory/03-multi-model.md` — how to combine models strategically
- `practice/01-setup.md` — how to install and configure the environment
- `practice/02-troubleshooting.md` — how to fix common problems
- `practice/03-checklist.md` — am I ready to proceed

### 6. Section numbering spans files

Theory files share a continuous numbering scheme. The numbering follows the reading order and continues across files.

Example from module-2:
- `theory/01-types-of-tools.md` → `## 1. Четыре категории инструментов`
- `theory/02-available-tools.md` → `## 2. Бесплатные и дешевые варианты`
- `theory/03-multi-model.md` → `## 3. Модели и мульти-модельная стратегия`, `## 4. Как выбирать`

File prefix (`01-`, `02-`) is the file order. Section number (`## 1.`, `## 2.`) is the content numbering. They may not match 1:1 since one file can contain multiple sections.

### 7. Heading structure

- Theory files: start with `## N. Section Title` (H2 with section number)
- Practice files: start with `# Title` (H1)
- Subsections: use `### N.M.` for theory, `### Subsection` for practice

Exception: the first theory file in a module may optionally include a module-level H1 title and a `> **Цель модуля:**` blockquote before the first H2.

### 8. Trim aggressively

Remove content that:
- **Duplicates official docs** — link to them instead (e.g., installation instructions → `https://code.claude.com/docs/en/quickstart`)
- **Lists obvious things** — system requirements, OS-specific installation steps
- **Adds fluff** — verbose descriptions where a table or bullet list suffices
- **Won't be re-read** — detailed comparison tables, exhaustive examples the reader skips

### 9. Prefer tables and structured formats

Use tables for comparisons, decision matrices, and multi-dimensional data. Use flowcharts (text-based) for decision trees.

### 10. Keep practical content actionable

Practice files should contain:
- Clear steps (numbered or sequential)
- Copy-pasteable commands and prompts
- Expected results / success criteria
- NOT lengthy explanations (that belongs in theory files)

---

## How to Apply to Existing Modules

### Step-by-step process

1. **Analyze the current module** — identify distinct topics within theory.md and distinct activities within practice.md
2. **Plan the split** — map sections to new files, choose descriptive names
3. **Create directories** — `theory/` and `practice/` under the module
4. **Extract and trim** — move content to new files with `NN-` prefixes, cut bloat as you go
5. **Number sections** — assign continuous numbers across theory files
6. **Delete the old files** — remove theory.md and practice.md after extraction
7. **Verify** — ensure no content was lost that the reader actually needs

### Modules that need updating

| Module | Current state | Expected work |
|--------|--------------|---------------|
| module-4-agents | theory.md (303L) + practice.md (1453L) | Practice urgently needs splitting (1453 lines!), theory may stay or split |
| module-5-context-engineering | theory.md (383L) + practice.md (624L) + templates/ | Split both, keep templates/ |
| module-6-mcp | theory.md (1364L) + practice.md (213L) | Theory urgently needs splitting (1364 lines!), practice is ok-sized |
| module-7-orchestration | theory.md (514L) + practice.md (1464L) | Both need splitting |
| module-8-responsibility | theory.md (437L) | Split into 2-3 topic files |

Modules 0 and 1 are small enough to leave as-is (90 and 374 lines respectively).
Modules 2 and 3 are already done — use them as reference.

### What NOT to change

- Don't rewrite content — only restructure and trim
- Don't change the teaching order within a module
- Don't add new topics or examples
- Don't remove content that's unique and valuable — only remove duplication and fluff
- Keep the Russian language and existing terminology
- Keep existing templates/ directories and supporting assets
