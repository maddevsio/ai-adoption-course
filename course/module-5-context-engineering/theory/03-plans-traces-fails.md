[← Оглавление](../../../README.md)

## 4. Plans: пронумерованные и самодостаточные

Plans — это **единицы работы** для агентов. Каждый план — самодостаточный документ, который содержит всё необходимое для выполнения задачи.

```
docs/plans/
├── 001-mvp-project-structure.plan.md
├── 002-mvp-store-service.plan.md
├── ...
├── 022-execution-flow-e2e.plan.md
└── 023-agent-pipeline-quality.plan.md
```

Нумерация обеспечивает порядок выполнения. Агент не начинает Plan 023, пока Plan 022 не завершён.

Типичный план содержит:

```markdown
# Plan 022: Execution Flow E2E

status: in_progress
Prerequisites: Plan 020, Plan 021

## Tasks

| # | Задача | Статус | Файлы |
|---|--------|--------|-------|
| 1 | Stage-per-worker lifecycle | done | task/internal/service/ |
| 2 | Flow-aware task acquisition | done | task/internal/repository/ |
| 3 | Trigger normalization | done | agent/internal/domain/ |

## Checkpoints

- CP-1: Unit tests pass (go test ./...)
- CP-2: Integration test: task → worker → completion
- CP-3: No orphaned containers after test run
```

Почему планы важны для агентов:
1. **Контекст одним файлом.** Агент читает план и понимает: что делать, в каком порядке, какие файлы менять, как проверить.
2. **Scope ограничен.** Агент не уходит "рефакторить всё" — план определяет границы работы.
3. **Progress tracking.** Статусы задач показывают, что уже сделано.

## 5. Traces: детальная структура

Trace — **лог выполнения плана**. Не просто "что сделано", а полный контекст: решения, проблемы, находки, предложения.

### Шаблон trace (из Enji Fleet)

```markdown
# Trace: <plan-name>

**Дата:** YYYY-MM-DD
**План:** [NNN-plan-name.plan.md](../plans/NNN-plan-name.plan.md)
**Агент:** <имя агента: Claude, Codex, Gemini, etc.>
**Статус:** completed | partial | failed

## Что сделано
- Краткий список выполненных задач

## Что узнал
- Технические детали, которые не очевидны из кода

## Проблемы
- Что не работало, как решил

## Технические решения
| # | Решение | Причина |
|---|---------|---------|
| D-xxx | ... | ... |

## Техдолг
Новый техдолг, обнаруженный или созданный.

## Для конституции
Что стоит перенести в constitution.
```

### Каждая секция решает свою задачу

**"Что сделано"** — краткий отчёт:

```markdown
- TASK-1: DB Migrations — 000007 rename, add columns
- TASK-2: Domain model — WorkerState enum, transition validation
- TASK-3: Repository — UpdateStatus with retry_count increment
```

**"Что узнал"** — знания, которые не очевидны из кода:

```markdown
- Task Service Create() устанавливает current_stage из entry stage flow
- Port 8005 занят Agent Service, не использовать для Runtime
- gRPC маппинг ошибок: InvalidArgument/NotFound/FailedPrecondition
```

Это самая ценная секция. Код показывает *что* сделано, но не *почему* или *как это работает в runtime*.

**"Проблемы"** — что пошло не так:

```markdown
- gRPC handler тесты не доведены до 85%: отсутствует helper `stringPtr`
- Spawner создаёт контейнеры в бесконечном цикле — retry_count не
  инкрементируется из-за вызова UpdateTaskStatus вместо ReleaseTask
```

**"Технические решения"** — отклонения от плана:

```markdown
| # | Решение | Причина |
|---|---------|---------|
| D-030 | ResolveAcquireFilters итерирует только static flows | Custom flows — chicken-and-egg problem |
| D-031 | AcquireTask repo принимает statuses+stages | Separation of concerns: repo = SQL executor |
```

**"Для конституции"** — предложения на обновление:

```markdown
- Зафиксировать требование Go toolchain 1.24.x
- Добавить паттерн: buf lint BASIC с отключением PACKAGE_DIRECTORY_MATCH
- Антипаттерн: не использовать UpdateTaskStatus для финальных переходов
```

> Обновляйте trace **инкрементально** — после каждой находки записывайте сразу. Не накапливайте в памяти. Если агент записывает trace только в конце сессии, он забудет детали.

## 6. Fails: постмортемы инцидентов

Fails — **постмортемы инцидентов**. Когда что-то идёт не так, агент создаёт документ с анализом причин и мерами предотвращения.

### Пример: расхождение паттернов между сервисами

Агент реализовал 3 плана в отдельных сессиях. Каждый план выполнен качественно, но между сервисами возникли системные расхождения:

| Аспект | Store Service | Credentials Service |
|--------|--------------|---------------------|
| Logger | `zap` (shared/pkg/logger) | `slog` (internal/logging) |
| Миграции | `backend/migrations/` | `credentials/migrations/` |
| DI | Интерфейсы (mockable) | Конкретные типы (не mockable) |

**Root cause:** Constitution на момент реализации была почти пустой — шаблон с placeholder'ами.

**Lessons learned:**
- **Constitution — не шаблон, а инструмент.** Пустая constitution = каждый агент решает сам
- **"Опционально" для агента = "не делать".** Важное — пишите "ОБЯЗАТЕЛЬНО"
- **Checkpoint должен быть machine-checkable.** Не "smoke test проходит", а "Create → ID, Get → object, Delete → 404"
- **Ревью по одному плану дешевле, чем пачкой**

### Пример: E2E blockers

При первом E2E прогоне система не смогла довести ни одну задачу до завершения. Найдено 7 багов, 2 из которых CRITICAL:

- **CLI name deadlock** — Agent Service и SDK использовали разные имена для CLI tools. Ни одно имя не проходило обе валидации.
- **Бесконечный respawn** — Spawner создавал контейнеры в цикле, потому что retry_count не инкрементировался в БД. 17 мёртвых контейнеров за 2 минуты.

### Структура fail-документа

```markdown
# Postmortem: <название инцидента>

**Дата:** YYYY-MM-DD
**Серьёзность:** HIGH | MEDIUM | LOW
**Статус:** mitigated | resolved | open

## Что произошло
Краткое описание проблемы.

## Почему произошло
### Root cause
Главная причина.
### Contributing factors
Что усугубило ситуацию.

## Impact
Прямые и косвенные последствия.

## Что сделано для предотвращения
Конкретные изменения в коде, процессе, документации.

## Lessons learned
Выводы для будущих агентов.
```

Без постмортемов ошибки повторяются. С постмортемами — следующий агент читает `docs/fails/` перед работой и знает, что проверять.
---

[← 3. Артефакты SDD](02-artifact-hierarchy.md) | [Оглавление](../../../README.md) | [7. AGENTS.md / CLAUDE.md →](04-special-artifacts.md)
