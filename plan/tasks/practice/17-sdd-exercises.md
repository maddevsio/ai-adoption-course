# Задача 17: Упражнения по SDD и управлению артефактами

## Цель

Практика для Модуля 5. Ученик изучает источники, устанавливает skills, создаёт систему артефактов и работает по spec-driven подходу.

## Что сделать

### Подготовка: Изучить источники и установить skills (10 мин)

- Список источников по SDD для чтения:
  - Anthropic: "Building a C compiler with a team of parallel Claudes" (https://www.anthropic.com/engineering/building-c-compiler) — кейс 16 агентов, 100K строк, SDD на практике
  - Thoughtworks: "Spec-driven development" (https://www.thoughtworks.com/en-us/insights/blog/agile-engineering-practices/spec-driven-development-unpacking-2025-new-engineering-practices) — определение и принципы SDD
  - Martin Fowler: "Understanding SDD: Kiro, spec-kit, Tessl" (https://martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html) — сравнение SDD-инструментов, три уровня строгости спецификации
- Примеры конституций из реальных проектов:
  - Next.js AGENTS.md (https://github.com/vercel/next.js/blob/canary/AGENTS.md) — эталон для крупного монорепо
  - Anthropic claude-code-action CLAUDE.md (https://github.com/anthropics/claude-code-action/blob/main/CLAUDE.md) — секция "Things That Will Bite You"
  - GitHub Spec Kit AGENTS.md (https://github.com/github/spec-kit/blob/main/AGENTS.md) — конституция SDD-тулкита
  - Коллекция: awesome-claude-md (https://github.com/josix/awesome-claude-md) — анализ паттернов из десятков проектов
- Skills для установки:
  1. **cc-sdd** (https://github.com/gotalab/cc-sdd) — полный SDD-workflow (requirements → design → tasks → implementation). Установка: `npx cc-sdd@latest --claude --lang ru`. 11 slash-команд: `/kiro:spec-init`, `/kiro:spec-requirements`, `/kiro:spec-design`, `/kiro:spec-tasks`, `/kiro:spec-impl` и др.
  2. **GitHub Spec Kit** (https://github.com/github/spec-kit) — конституция, спеки, планы, задачи. Установка: `uv tool install specify-cli --from git+https://github.com/github/spec-kit.git && specify init my-project --ai claude`. Команды: `/speckit.constitution`, `/speckit.specify`, `/speckit.plan`, `/speckit.tasks`, `/speckit.implement`.
  3. **claude-skills-starter** (https://github.com/angakh/claude-skills-starter) — 12 slash-команд для Claude Code: `/commit`, `/quality`, `/scaffold`, `/test`, `/pr-create` и др. Установка: скопировать `.claude/` в корень проекта.
  - Для каждого: пошаговая инструкция установки + проверка: skill работает

### Шаг 1: Конституция проекта (10 мин)

- Шаблон конституции (project constitution)
- Ученик пишет для своего репозитория
- Секции: цель проекта, стек, архитектура, конвенции, правила для агентов, запреты

### Шаг 2: Спецификация фичи (15 мин)

Подготовленный сценарий: "Добавить фильтрацию задач по статусу и приоритету"
- Шаблон спецификации: цель, acceptance criteria, технические ограничения, примеры API, out of scope
- Ученик заполняет шаблон

### Шаг 3: Реализация по спецификации (10 мин)

- Дать агенту спецификацию + конституцию
- Агент реализует
- Ученик ревьюит: спецификация выполнена? Criteria met?

### Шаг 4: Заметки по реализации (5 мин)

- Шаблон: что агент сделал хорошо / не так / какие решения приняты / что бы изменил в спеке

## Формат результата

- MD-файл `course/module-5-sdd/practice.md`
- Шаблоны в `course/module-5-sdd/templates/`
- Список источников и skills с инструкциями установки

## Критерии приёмки

- Список источников по SDD (2-3 ссылки)
- 2-3 skill для установки с инструкциями
- Шаблон конституции (заполняемый)
- Шаблон спецификации (заполняемый)
- Шаблон заметок по реализации
- Суммарно 50 мин (с учётом подготовки)

## Зависимости

- Задача 08 (теория SDD)

## Дополнительные ресурсы

- awesome-cursorrules (https://github.com/PatrickJS/awesome-cursorrules) — коллекция .cursorrules для разных фреймворков
- awesome-claude-code (https://github.com/hesreallyhim/awesome-claude-code) — каталог skills, hooks, slash-команд для Claude Code
- AGENTS.md specification (https://agents.md/) — открытый стандарт, поддерживается Google, OpenAI, Sourcegraph, Cursor
