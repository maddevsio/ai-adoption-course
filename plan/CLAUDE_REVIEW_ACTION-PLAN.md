# Action Plan: Addressing Review Feedback

**Based on:** /review/external-review/review-claude-opus.md
**Date:** 2026-02-24

---

## Overview

20 issues identified, grouped into 3 waves by priority and dependency. Each task includes the exact file, the problem, and a concrete fix description.

**Estimated effort:**
- Wave 1 (Critical fixes): ~30 min — text edits only, no new content
- Wave 2 (Important fixes): ~2-3 hours — mix of edits and small additions
- Wave 3 (Enhancements): ~4-6 hours — new content creation

---

## Wave 1: Critical Fixes (do first, before next cohort)

These are factual errors and inconsistencies that will confuse students.

### Task 1.1 — Fix name inconsistency in Level 5 persona

- **File:** `course/module-1-why-ai/theory.md:214`
- **Problem:** Paragraph introduces "Антон, tech lead" but switches to "Игорь" mid-text: _"Утром Игорь получает задачу..."_, _"Игорь пишет runbook..."_
- **Fix:** Replace both occurrences of "Игорь" with "Антон" on line 214.

### Task 1.2 — Fix scoring scale mismatch in diagnostics

- **File:** `course/module-1-why-ai/diagnostics.md:70-83`
- **Problem:** The file has two conflicting interpretation keys:
  - Lines 62-66: correct 5-25 point scale matching the 5 questions
  - Lines 72-83: second key using 8-40 point scale (leftover from the 10-question `self-assessment.md`)
- **Fix:** Remove lines 70-83 entirely (the "Интерпретация результатов" section with 35-40 / 25-34 / 15-24 / 8-14 ranges and the "Дисбаланс навыков" subsection). The "Ключ интерпретации" section on lines 58-68 already provides the correct interpretation. Alternatively, add a note: _"Для расширенной оценки (10 вопросов, 40 баллов) пройдите `self-assessment.md`"_ right after the first key.

### Task 1.3 — Fix glossary meta-reference

- **File:** `course/GLOSSARY.md:49`
- **Problem:** Entry reads: _"**Forward reference** — упоминание термина до его определения в тексте, создающее путаницу для читателя. См. review/student-experience-report.md."_ — references an internal review document that students should not see.
- **Fix:** Remove the `review/student-experience-report.md` reference. Replace with a course example, e.g.: _"Например, если модуль 3 упоминает 'SDD' до его определения в модуле 5."_

---

## Wave 2: Important Fixes (do before next active teaching period)

These fix inconsistencies, missing content, and formatting issues.

### Task 2.1 — Align level names between diagnostics and theory

- **File:** `course/module-1-why-ai/diagnostics.md:64`
- **Problem:** Level 3 is "Активный экспериментатор" here, but "Agentic developer" / "Драйвер агента" in `theory.md`.
- **Fix:** Rename level names in diagnostics.md to match theory.md:
  - Line 62: "Уровень 1 — Начальный пользователь" → "Уровень 1 — Chat-помощник"
  - Line 63: "Уровень 2 — Интегрированный помощник" → "Уровень 2 — Копилот"
  - Line 64: "Уровень 3 — Активный экспериментатор" → "Уровень 3 — Драйвер агента"
  - Line 65: "Уровень 4 — Специалист по одному агенту" → "Уровень 4 — Специалист по агенту"
  - Line 66: keep as-is (already matches)
- **Verify:** Cross-reference with `self-assessment.md` level names for consistency.

### Task 2.2 — Add note about constitution size growth

- **File:** `course/module-5-context-engineering/theory/05-context-organization.md:14`
- **Problem:** Text recommends "~400-500 lines", but the Enji Fleet table shows ~800 lines.
- **Fix:** After line 14, add a note: _"> [!NOTE] 400-500 строк — ориентир для старта. По мере развития проекта конституция растёт. Конституция Enji Fleet достигла ~800 строк за 23 плана. Это нормально — главное, чтобы каждая строка была полезной."_

### Task 2.3 — Expand MCP practice section

- **File:** `course/module-6-mcp/practice/01-setup-mcp-servers.md`
- **Problem:** Missing Step 2, no `mcp.json` example, exercises require paid accounts (Jira/Figma) with no alternatives.
- **Fix (3 changes):**
  1. Add "Шаг 2: Конфигурация" between existing Steps 1 and 3, with a concrete `mcp.json` example:
     ```json
     {
       "mcpServers": {
         "git": {
           "command": "npx",
           "args": ["@modelcontextprotocol/server-git"]
         }
       }
     }
     ```
  2. Under the Figma/Jira tasks, add: _"Если у вас нет доступа к Jira/Figma — пропустите эти задания. Git MCP и PostgreSQL MCP доступны бесплатно и достаточны для освоения концепции."_
  3. Add a troubleshooting subsection with 2-3 common MCP failures (server not found, env var missing, version mismatch).

### Task 2.4 — Add price volatility caveat

- **File:** `course/module-2-tools/theory/02-available-tools.md`
- **Problem:** Specific model prices will become stale.
- **Fix:** Add a note at the top of the pricing table: _"> [!NOTE] Цены на модели обновляются часто. Актуальные цены: [anthropic.com/pricing](https://anthropic.com/pricing), [openai.com/pricing](https://openai.com/pricing). Данные ниже актуальны на февраль 2026."_

### Task 2.5 — Fix step numbering gaps (4 files)

4 files have skipped step numbers. Each is a one-line renumber.

- **File 1:** `course/module-6-mcp/practice/01-setup-mcp-servers.md:26`
  - Current: Шаг 1, Шаг 3, Шаг 4
  - Fix: After adding Step 2 (Task 2.3), renumber Шаг 3 → Шаг 3, Шаг 4 → Шаг 4 (numbers will be correct after insertion)

- **File 2:** `course/module-4-agents/practice/02-agent-planning.md:92`
  - Current: numbered list `1. ... 2. ... 3. ... 5. ... 6. ... 7.` (skips 4)
  - Fix: Renumber `5.` → `4.`, `6.` → `5.`, `7.` → `6.`

- **File 3:** `course/module-5-context-engineering/practice/04-implementation.md:20`
  - Current: numbered list `1. ... 3. ... 4.` (skips 2)
  - Fix: Renumber `3.` → `2.`, `4.` → `3.`

- **File 4:** `course/module-7-orchestration/practice/02-generator-reviewer.md:30`
  - Current: `**1. Терминал 1 — Агент-генератор:**` then `**3. Терминал 2 — Агент-ревьюер:**` (skips 2)
  - Fix: Renumber `**3.` → `**2.`

### Task 2.6 — Align feature spec template with practice exercise

- **File:** `course/module-5-context-engineering/templates/feature-spec-template.md`
- **Problem:** Template lacks "Out of Scope" and "API Examples" sections, but `practice/03-specification.md` asks students to fill those.
- **Fix:** Add two sections after "Ограничения":
  ```markdown
  ---

  ## Out of Scope

  Что НЕ входит в эту фичу (чтобы агент не ушёл в сторону):

  - [Пример: "Не реализовывать bulk-операции"]
  - [Пример: "Не менять существующие endpoints"]

  ---

  ## Примеры API

  Примеры запросов и ответов для каждого acceptance criteria:

  **Пример 1: Успешный запрос**
  \`\`\`
  GET /api/tasks?status=pending
  → 200 [{ "id": 1, "status": "pending", ... }]
  \`\`\`

  **Пример 2: Невалидный фильтр**
  \`\`\`
  GET /api/tasks?status=invalid
  → 400 { "error": "Invalid status. Allowed: pending, in_progress, done" }
  \`\`\`
  ```

### Task 2.7 — Add mcp.json example to MCP practice

This is covered by Task 2.3 (the new Step 2). No separate action needed.

### Task 2.8 — Fix formatting error in Module 8 practice

- **File:** `course/module-8-responsibility/practice/01-checklists.md:8`
- **Current:** `*В промпте и контексте нет чувствительных данных?**`
- **Fix:** Change to `**В промпте и контексте нет чувствительных данных?**` (add missing opening `**`)

---

## Wave 3: Enhancements (nice-to-have, can be done incrementally)

These improve the course but don't fix errors.

### Task 3.1 — Suggest starter projects in Module 0

- **File:** `course/module-0-intro/theory.md`
- **What:** Add 2-3 recommended starter project types after the "what project to use" section. E.g.:
  - A simple REST API (task manager, bookmarks) — ideal for modules 3-5
  - A full-stack app with frontend — ideal for modules 6-7
  - An existing open-source project with tests — ideal for all modules
- **Effort:** ~15 min

### Task 3.2 — Add cost worked example to Module 7

- **File:** `course/module-7-orchestration/theory/04-playbook-and-operations.md` (or a new subsection)
- **What:** Add a concrete cost calculation for a typical 3-agent orchestrated workflow. Example: Planning (Opus, 50K tokens) + 3x Development (Haiku, 100K tokens each) + Review (Sonnet, 80K tokens) = total cost breakdown by model.
- **Effort:** ~30 min

### Task 3.3 — Add "Minimum Viable SDD" fast-path to Module 5

- **File:** `course/module-5-context-engineering/theory/01-context-and-sdd.md` (add section at the end)
- **What:** A 10-line "Quick Start" section: _"Don't want the full hierarchy yet? Start with: (1) Write AGENTS.md, (2) After each task ask agent to create a trace in docs/traces/, (3) Review traces monthly and update AGENTS.md. That's it — you already have 80% of the value."_
- **Effort:** ~15 min

### Task 3.4 — Add cross-tool mapping table to Module 4

- **File:** `course/module-4-agents/theory/01-agent-fundamentals.md` (add after the AGENTS.md section)
- **What:** A table:
  | Tool | Agent file | Config file | Plan mode command |
  |------|-----------|-------------|-------------------|
  | Claude Code | CLAUDE.md | ~/.claude/ | `/plan` |
  | Cursor | .cursorrules | .cursor/ | Composer |
  | OpenCode | AGENTS.md | .opencode/ | — |
- **Effort:** ~15 min

### Task 3.5 — Split final test into questions + answer key

- **File:** `course/final-test.md`
- **What:** Create `course/final-test-answers.md` with explanations. Keep `final-test.md` as questions-only with a note: _"Ключ ответов — в final-test-answers.md"_
- **Effort:** ~20 min (mostly copy-paste split)

### Task 3.6 — Expand thin practice files

Three practice files need more content:

- **File 1:** `course/module-4-agents/practice/05-testing.md` (32 lines)
  - Add expected outcomes for exercises 2 and 3, add a verification checklist, add time estimates
  - Effort: ~20 min

- **File 2:** `course/module-5-context-engineering/practice/05-trace.md` (24 lines)
  - Add an inline example of a completed trace (5-10 lines), add "what makes a good trace" checklist
  - Effort: ~15 min

- **File 3:** `course/module-7-orchestration/practice/04-install-maestro.md` (26 lines)
  - Add basic troubleshooting, a brief UI overview, and note about platform support
  - Effort: ~15 min

### Task 3.7 — Add fallback exercises for external dependencies

- **File 1:** `course/module-3-prompting/practice/03-gandalf.md`
  - Add: _"Если gandalf.lakera.ai недоступен: попробуйте [prompt injection playground] или выполните упражнение с вашим собственным агентом — попросите его НЕ раскрывать определённое слово, затем попытайтесь его извлечь."_

- **File 2:** `course/module-7-orchestration/practice/04-install-maestro.md`
  - Add: _"Если Maestro недоступен для вашей платформы: используйте два окна терминала + git worktree (см. упражнение 01) как ручную альтернативу. Концепция playbook-ов применима независимо от инструмента оркестрации."_

- **Effort:** ~15 min total

### Task 3.8 — Add prompt templates for debugging and refactoring

- **File:** `course/module-3-prompting/practice/02-prompt-templates.md`
- **What:** Add 1-2 template types: debugging (describe bug → expected behavior → actual behavior → stack trace → acceptance criteria) and/or refactoring (code smell → desired improvement → constraints → acceptance criteria).
- **Effort:** ~30 min

### Task 3.9 — Update stale date references

- **Files:** Various practice files and templates
- **What:** Search for `2025` date references and update to `2026` where they appear in examples. Run: `grep -r "2025" course/` to find all instances.
- **Effort:** ~10 min

---

## Execution Order

```
Wave 1 (30 min) — do immediately
  1.1 → 1.2 → 1.3  (independent, can be done in any order)

Wave 2 (2-3 hours) — before next teaching session
  2.8 → 2.5 → 2.1 → 2.4  (quick text fixes first)
  2.2 → 2.6            (content additions)
  2.3                   (largest task — MCP practice expansion)

Wave 3 (4-6 hours) — do incrementally as time allows
  3.9 → 3.3 → 3.4 → 3.1  (quick wins first)
  3.8 → 3.6              (content creation)
  3.7 → 3.2 → 3.5        (remaining tasks)
```

---

## Verification

After all changes, run:
1. `grep -rn "Игорь" course/module-1-why-ai/` — should return 0 results
2. `grep -rn "35-40" course/module-1-why-ai/diagnostics.md` — should return 0 results
3. `grep -rn "student-experience-report" course/` — should return 0 results
4. Verify all practice files have sequential step numbering
5. Confirm `mcp.json` example exists in Module 6 practice
6. Confirm feature-spec-template.md has "Out of Scope" and "Примеры API" sections
