# AI для разработчиков: от копилота до оркестрации агентов

Курс для разработчиков Mad Devs. Ведёт от уровня «спросить ChatGPT» до «управлять несколькими агентами параллельно». На выходе с помощью практических заданий создается сетап для agentic разработки

## С чего начать

1. [Введение в курс](course/module-0-intro/theory.md) — формат, ожидания, как проходить
2. [Самооценка](course/self-assessment.md) — определите свой текущий уровень (5 мин)
3. Двигайтесь по модулям последовательно, начиная с Модуля 1

## Содержание

### Модуль 0. Введение

- [Введение в курс](course/module-0-intro/theory.md)
- [Самооценка уровня](course/self-assessment.md)

### Модуль 1. Зачем разработчику ИИ `30 мин`

Модель зрелости, калибровка ожиданий, самодиагностика.

**Теория:**
- [Уровни зрелости использования ИИ](course/module-1-why-ai/01-theory.md)
- [8 уровней по Стиву Йегге](course/module-1-why-ai/02-yegge-levels.md)
- [Самодиагностика](course/module-1-why-ai/03-diagnostics.md)

### Модуль 2. Инструменты и установка `60 мин`

Четыре категории инструментов, мульти-модельная стратегия, установка CLI-агента.

**Теория:**
- [Ландшафт инструментов](course/module-2-tools/theory/01-types-of-tools.md)
- [Бесплатные и дешёвые варианты](course/module-2-tools/theory/02-available-tools.md)
- [Мульти-модельная стратегия](course/module-2-tools/theory/03-multi-model.md)

**Практика:**
- [Установка рабочего окружения](course/module-2-tools/practice/01-setup.md)
- [Troubleshooting](course/module-2-tools/practice/02-troubleshooting.md)
- [Чеклист готовности](course/module-2-tools/practice/03-checklist.md)

### Модуль 3. Промптинг `60 мин`

От вопросов к заданиям. Структура промпта, продвинутые техники, антипаттерны.

**Теория:**
- [Структура промпта](course/module-3-prompting/theory/01-prompt-structure.md)
- [Продвинутые техники](course/module-3-prompting/theory/02-advanced-techniques.md)
- [Антипаттерны](course/module-3-prompting/theory/03-antipatterns.md)
- [Промпты для разных задач](course/module-3-prompting/theory/04-task-specific-prompts.md)

**Практика:**
- [Улучши промпт](course/module-3-prompting/practice/01-improve-prompts.md)
- [Шаблоны промптов](course/module-3-prompting/practice/02-prompt-templates.md)
- [Игра Gandalf](course/module-3-prompting/practice/03-gandalf.md)

### Модуль 4. Работа с AI-агентом `75 мин`

Plan/Act режимы, AGENTS.md, TDD с агентами, контроль качества.

**Теория:**
- [Основы работы с агентом](course/module-4-agents/theory/01-agent-fundamentals.md)
- [HITL и контроль качества](course/module-4-agents/theory/02-hitl-and-quality.md)
- [Тестирование с агентами](course/module-4-agents/theory/03-testing-with-agents.md)

**Практика:**
- [Создай AGENTS.md](course/module-4-agents/practice/01-create-agents-md.md)
- [Получи план от агента](course/module-4-agents/practice/02-agent-planning.md)
- [Ревью результата](course/module-4-agents/practice/03-review-result.md)
- [Итерация](course/module-4-agents/practice/04-iteration.md)
- [Тестирование с агентом](course/module-4-agents/practice/05-testing.md)
- [Чеклист](course/module-4-agents/practice/06-checklist.md)

### Модуль 5. Context Engineering и SDD `75 мин`

Спецификация как источник истины. Конституция, планы, traces, fails.

**Теория:**
- [Context Engineering и SDD](course/module-5-context-engineering/theory/01-context-and-sdd.md)
- [Иерархия артефактов](course/module-5-context-engineering/theory/02-artifact-hierarchy.md)
- [Планы, traces, fails](course/module-5-context-engineering/theory/03-plans-traces-fails.md)
- [AGENTS.md и спецартефакты](course/module-5-context-engineering/theory/04-special-artifacts.md)
- [Организация контекста](course/module-5-context-engineering/theory/05-context-organization.md)

**Практика:**
- [Изучить источники и skills](course/module-5-context-engineering/practice/01-sources-and-skills.md)
- [Конституция проекта](course/module-5-context-engineering/practice/02-constitution.md)
- [Спецификация фичи](course/module-5-context-engineering/practice/03-specification.md)
- [Реализация по спецификации](course/module-5-context-engineering/practice/04-implementation.md)
- [Заметки по реализации](course/module-5-context-engineering/practice/05-trace.md)
- [Чеклист](course/module-5-context-engineering/practice/06-checklist.md)

**Шаблоны:**
- [Шаблон конституции](course/module-5-context-engineering/templates/constitution-template.md)
- [Шаблон спецификации](course/module-5-context-engineering/templates/feature-spec-template.md)
- [Шаблон implementation notes](course/module-5-context-engineering/templates/implementation-notes-template.md)

### Модуль 6. MCP `75 мин`

Model Context Protocol — подключение внешних инструментов к агенту.

**Теория:**
- [Что такое MCP](course/module-6-mcp/theory/01-what-is-mcp.md)
- [Категории MCP-серверов](course/module-6-mcp/theory/02-mcp-servers.md)
- [Установка и настройка](course/module-6-mcp/theory/03-setup-and-config.md)
- [Создание своего MCP-сервера](course/module-6-mcp/theory/04-custom-servers.md)

**Практика:**
- [Настройка MCP-серверов](course/module-6-mcp/practice/01-setup-mcp-servers.md)
- [Чеклист](course/module-6-mcp/practice/02-checklist.md)

### Модуль 7. Параллельные агенты и оркестрация `90 мин`

Git worktrees, паттерны оркестрации, ролевая модель, playbook.

**Теория:**
- [Роли и параллелизм](course/module-7-orchestration/theory/01-role-and-parallelism.md)
- [Изоляция и циклы](course/module-7-orchestration/theory/02-isolation-and-loops.md)
- [Роли и паттерны](course/module-7-orchestration/theory/03-roles-and-patterns.md)
- [Playbook и операции](course/module-7-orchestration/theory/04-playbook-and-operations.md)

**Практика:**
- [Git worktree](course/module-7-orchestration/practice/01-git-worktree.md)
- [Генератор + ревьюер](course/module-7-orchestration/practice/02-generator-reviewer.md)
- [Параллельная работа и слияние](course/module-7-orchestration/practice/03-parallel-and-merge.md)
- [Установка Maestro](course/module-7-orchestration/practice/04-install-maestro.md)
- [Создание playbook](course/module-7-orchestration/practice/05-playbook-creation.md)
- [Чеклист](course/module-7-orchestration/practice/06-checklist.md)

### Модуль 8. Ответственное использование `30 мин`

Ограничения ИИ, безопасность, ответственность по уровням автономности.

**Теория:**
- [Ограничения ИИ](course/module-8-responsibility/theory/01-ai-limitations.md)
- [Безопасность](course/module-8-responsibility/theory/02-security.md)
- [Ответственность по уровням](course/module-8-responsibility/theory/03-responsibility.md)

**Практика:**
- [Чеклисты для работы с AI-кодом](course/module-8-responsibility/practice/01-checklists.md)

### Завершение

- [Финальный тест](course/final-test.md) — 10 сценарных вопросов по всем модулям
- [Повторная самооценка](course/self-assessment.md) — сравните с результатом в начале

### Справочные материалы

- [DOs and DON'Ts](course/dos-and-donts.md) — свод правил из всех модулей
- [Глоссарий](course/GLOSSARY.md)
- [Полезные ссылки](course/useful-links.md)

## Уровни зрелости

Курс построен вокруг 5 уровней владения ИИ-инструментами:

| Уровень | Что делаете | Модули |
|---------|-------------|--------|
| 1 — Чат | Спрашиваете и копируете | 1 |
| 2 — Копилот | Реагируете на подсказки IDE | 2–3 |
| 3 — Драйвер агента | Делегируете задачу целиком | 4 |
| 4 — Специалист | Управляете контекстом и сессиями | 5–6 |
| 5 — Оркестратор | Координируете несколько агентов | 7 |

Пройдите [самооценку](course/self-assessment.md), чтобы узнать свой уровень.

## Основной пример — Enji Fleet

Курс ссылается на Enji Fleet — проект Mad Devs по оркестрации AI-агентов. Практики из флита (конституция, trace-файлы, мульти-агентные воркфлоу) применимы к любому проекту.
