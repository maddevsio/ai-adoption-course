[← Оглавление](../../../README.md)

## 7. AGENTS.md / CLAUDE.md

Это "README для агентов" — файл в корне проекта, который агенты читают автоматически. Содержит описание проекта, архитектуры, команды для запуска, конвенции кода. Ключевое отличие от README: AGENTS.md содержит детальный контекст для агентов (build steps, test conventions, паттерны), который захламлял бы обычный README.

**Важно:** не превращайте AGENTS.md в замену линтеру. Code style проверяется автоматически (prettier/eslint). Пишите только то, что не проверяется автоматически.

Примеры: [Next.js AGENTS.md](https://github.com/vercel/next.js/blob/canary/AGENTS.md), [Anthropic CLAUDE.md](https://github.com/anthropics/claude-code-action/blob/main/CLAUDE.md).

## 8. Memory Bank

Контекст, который агент должен помнить между сессиями. В Claude Code есть встроенная система memories — агент может сохранять и читать заметки о проекте.

```
.claude/memories/
  ├── auth.md          # Аутентификация и авторизация
  ├── database.md      # Схема БД, миграции
  ├── api-design.md    # Конвенции API, error handling
  └── testing.md       # Стратегия тестирования
```

Примеры: [Cline Memory Bank](https://docs.cline.bot/prompting/cline-memory-bank), Claude Code memories.

## 9. Skills

**Skills** — это готовые промпты и подходы, заточенные под конкретные повторяющиеся задачи. Вместо повторения промпта "сделай code review..." создаёте skill `/review`.

В Claude Code skills — это markdown-файлы с front matter, которые хранятся в `~/.claude/skills/` (глобально) или `project/.claude/skills/` (для конкретного проекта). Skills всегда сохраняются в файле `SKILL.md`, а имя skill определяется именем папки.

### 9.1. Пример skills
**SDD workflow:**
```markdown
---
skill: sdd
description: Spec-driven development процесс
---

# SDD Workflow

1. Прочитай constitution
2. Прочитай feature specification
3. Напиши тесты (TDD)
4. Реализуй минимальный код для прохождения тестов
5. Запусти линтеры и тесты
6. Создай trace файл
7. Создай PR
```

### 9.2. Готовые решения

- **[superpowers](https://github.com/obra/superpowers):** полный набор скиллов для разработки на Claude Code, Cursor, Codex, OpenCode
- **[claude-skills-starter](https://github.com/angakh/claude-skills-starter):** 12 готовых slash-команд — `/commit`, `/quality`, `/test`, `/scaffold`

### 9.3. Как создать skill

1. Создайте директорию: `.claude/skills/my-skill/`
2. Создайте файл `SKILL.md` в этой директории
3. Добавьте front matter:
```markdown
---
skill: my-skill
description: Краткое описание того, что делает skill
---
```
4. Опишите процесс или чеклист в markdown
5. Вызывайте: `/my-skill` в Claude Code

Skills автоматизируют повторяющиеся workflow.
---

[← 4. Plans: пронумерованные и самодостаточные](03-plans-traces-fails.md) | [Оглавление](../../../README.md) | [10. Организация контекста в проекте →](05-context-organization.md)
