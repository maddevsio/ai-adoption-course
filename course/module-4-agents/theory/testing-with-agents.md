# Тестирование в AI-assisted разработке

Дополнительный материал к Модулю 4. Без тестов AI-assisted разработка **развалится**. Агент генерирует код, который "выглядит правильно", но может содержать subtle bugs, нарушения контрактов и regression. Тесты — единственная детерминистическая защита.

## Почему тесты критичны именно для AI-разработки

Когда человек пишет код, он держит в голове контекст: как работает система, какие edge cases, какие зависимости. Агент не держит — он видит только то, что загружено в контекстное окно. Это создаёт специфические риски:

1. **Агент не видит side effects.** Он может изменить функцию, не зная, что её вызывают из 15 мест. Без тестов эти 15 мест сломаются молча.

2. **Агент оптимизирует на "работает на happy path".** Без тестов на edge cases (пустой вход, null, максимальные значения, concurrent access) код будет падать в production.

3. **Агент может "обмануть".** Если попросить "сделай чтобы тесты проходили", агент может упростить тест вместо исправления кода. Хорошо написанные тесты это предотвращают.

4. **Каждая сессия — чистый лист.** Агент в новой сессии не помнит, что менял предыдущий. Тесты ловят regression между сессиями.

**Принцип из Enji Fleet:** "Machine acceptance precedes human acceptance" — прежде чем человек посмотрит на код, он должен пройти все автоматические проверки.

## Пирамида тестирования

```
         /\
        /  \         E2E тесты
       / E2E\        (немного, медленные, дорогие)
      /------\
     /        \      Интеграционные тесты
    / Integr.  \     (средне, средняя скорость)
   /------------\
  /              \   Unit тесты
 /    Unit        \  (много, быстрые, дешёвые)
/------------------\
```

| Тип | Количество | Скорость | Что проверяет |
|-----|-----------|----------|---------------|
| Unit | Много (70-80%) | Миллисекунды | Отдельные функции и модули |
| Integration | Средне (15-20%) | Секунды | Взаимодействие компонентов |
| E2E | Мало (5-10%) | Минуты | Весь пользовательский сценарий |

Для AI-разработки пирамида особенно важна: **unit тесты дают быстрый feedback loop**. Агент написал код → запустил unit тесты → увидел ошибку → исправил → повторил. Если feedback loop медленный (только E2E), агент потратит токены впустую.

## Unit тесты: быстрый feedback для агента

Unit тесты проверяют отдельные функции и модули **в изоляции** от внешних зависимостей (БД, сеть, файловая система). Зависимости заменяются моками.

### Зачем нужны unit тесты

- **Быстрый feedback.** Запуск за миллисекунды. Агент может итерировать: написал код → тест → исправил → тест → готово.
- **Изоляция ошибок.** Если unit тест падает, проблема в конкретной функции, а не "где-то в системе".
- **Документация поведения.** Тест показывает, как функция должна работать: какие входы, какие выходы, какие ошибки.
- **Regression protection.** Следующий агент изменит код — unit тест сразу покажет, что сломалось.

### Паттерны unit тестов

#### Table-driven tests (Go)

Стандартный паттерн в Go — параметризованные тесты через таблицу:

```go
func TestParseURL(t *testing.T) {
    tests := []struct {
        name    string
        input   string
        want    string
        wantErr bool
    }{
        {"valid https", "https://example.com", "example.com", false},
        {"valid http", "http://example.com", "example.com", false},
        {"no scheme", "example.com", "", true},
        {"empty", "", "", true},
        {"very long", strings.Repeat("a", 10000), "", true},
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            got, err := ParseURL(tt.input)
            if (err != nil) != tt.wantErr {
                t.Errorf("ParseURL(%q) error = %v, wantErr %v",
                    tt.input, err, tt.wantErr)
                return
            }
            if got != tt.want {
                t.Errorf("ParseURL(%q) = %q, want %q",
                    tt.input, got, tt.want)
            }
        })
    }
}
```

Одна функция — одна таблица с 5+ кейсами. Легко добавить новый edge case: просто строка в таблицу.

#### describe/it (JavaScript/TypeScript)

```typescript
describe('TaskService', () => {
  describe('createTask', () => {
    it('should create task with valid title', async () => {
      const task = await service.createTask({ title: 'Test' });
      expect(task.id).toBeDefined();
      expect(task.title).toBe('Test');
      expect(task.status).toBe('pending');
    });

    it('should reject empty title', async () => {
      await expect(service.createTask({ title: '' }))
        .rejects.toThrow('Title cannot be empty');
    });

    it('should reject title over 200 characters', async () => {
      const longTitle = 'a'.repeat(201);
      await expect(service.createTask({ title: longTitle }))
        .rejects.toThrow('Title too long');
    });

    it('should trim whitespace from title', async () => {
      const task = await service.createTask({ title: '  Test  ' });
      expect(task.title).toBe('Test');
    });
  });
});
```

#### Мокирование зависимостей

Unit тесты изолируют код от внешних зависимостей через моки:

```go
// Go: мок через интерфейс
type mockRepo struct {
    createFn func(ctx context.Context, task *Task) error
    getFn    func(ctx context.Context, id string) (*Task, error)
}

func (m *mockRepo) Create(ctx context.Context, task *Task) error {
    return m.createFn(ctx, task)
}

func TestServiceCreate_DBError(t *testing.T) {
    repo := &mockRepo{
        createFn: func(_ context.Context, _ *Task) error {
            return errors.New("connection refused")
        },
    }
    svc := NewService(repo)
    _, err := svc.Create(context.Background(), "test")
    if err == nil {
        t.Fatal("expected error, got nil")
    }
}
```

```typescript
// TypeScript: мок через vi.mock
vi.mock('@/shared/api/client', () => ({
  apiClient: {
    get: vi.fn(),
    post: vi.fn(),
  },
}));

it('should handle API error gracefully', async () => {
  vi.mocked(apiClient.get).mockRejectedValue(new Error('Network error'));
  const result = await fetchTasks();
  expect(result).toEqual([]);
});
```

### Что просить агента в unit тестах

**Хороший промпт:**
```
Напиши unit тесты для функции calculateDiscount в pricing.ts.

Покрой сценарии:
1. Скидка 10% для суммы > 1000
2. Скидка 5% для суммы 500-1000
3. Нет скидки для суммы < 500
4. Edge case: сумма = 0
5. Edge case: отрицательная сумма (должна вернуть ошибку)
6. Edge case: сумма = ровно 500 и ровно 1000 (граничные значения)

Используй describe/it структуру. Каждый тест проверяет ОДИН сценарий.
Запусти тесты после написания.
```

**Плохой промпт:**
```
Напиши тесты для pricing.ts
```

Без конкретных сценариев агент напишет 1-2 теста на happy path и пропустит edge cases.

## Интеграционные тесты: проверка взаимодействия

Интеграционные тесты проверяют **взаимодействие между компонентами**: код + БД, сервис + API, модуль + файловая система. Внешние зависимости — реальные (или близкие к реальным через тестовые контейнеры).

### Зачем нужны интеграционные тесты

- **Unit тесты не ловят проблемы интеграции.** Функция работает в изоляции, но ломается при реальном SQL-запросе (неправильный тип колонки, missing index, constraint violation).
- **Проверка контрактов.** API endpoint возвращает правильный JSON? Middleware корректно обрабатывает ошибки? Rate limiter действительно блокирует после N попыток?
- **Проверка миграций.** БД-схема соответствует коду? Миграция не сломала существующие данные?

### Паттерны интеграционных тестов

#### API integration tests

```python
# Python/FastAPI: интеграционный тест endpoint
import pytest
from httpx import AsyncClient
from main import app

@pytest.fixture
async def client():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

@pytest.mark.asyncio
async def test_create_and_get_task(client):
    # Create
    response = await client.post("/tasks", json={"title": "Test task"})
    assert response.status_code == 201
    task_id = response.json()["id"]

    # Get
    response = await client.get(f"/tasks/{task_id}")
    assert response.status_code == 200
    assert response.json()["title"] == "Test task"

@pytest.mark.asyncio
async def test_update_nonexistent_task(client):
    response = await client.put("/tasks/99999", json={"title": "Updated"})
    assert response.status_code == 404

@pytest.mark.asyncio
async def test_create_task_empty_title(client):
    response = await client.post("/tasks", json={"title": ""})
    assert response.status_code == 400
```

```typescript
// TypeScript/Express: интеграционный тест
import request from 'supertest';
import { app } from '../src/app';

describe('POST /tasks', () => {
  it('should create task and return 201', async () => {
    const response = await request(app)
      .post('/tasks')
      .send({ title: 'Test task' })
      .expect(201);

    expect(response.body.id).toBeDefined();
    expect(response.body.title).toBe('Test task');
  });

  it('should return 400 for empty title', async () => {
    await request(app)
      .post('/tasks')
      .send({ title: '' })
      .expect(400);
  });
});

describe('PUT /tasks/:id', () => {
  it('should return 404 for nonexistent task', async () => {
    await request(app)
      .put('/tasks/99999')
      .send({ title: 'Updated' })
      .expect(404);
  });
});
```

#### Database integration tests (Go)

В Go интеграционные тесты отделяются build-тегами:

```go
//go:build integration

package repository_test

import (
    "context"
    "testing"
)

func TestTaskRepository_CRUD(t *testing.T) {
    pool := testDB(t) // Подключение к тестовой БД
    repo := NewTaskRepository(pool)
    ctx := context.Background()

    // Create
    task, err := repo.Create(ctx, "Test task")
    if err != nil {
        t.Fatalf("Create failed: %v", err)
    }

    // Read
    got, err := repo.GetByID(ctx, task.ID)
    if err != nil {
        t.Fatalf("GetByID failed: %v", err)
    }
    if got.Title != "Test task" {
        t.Errorf("title = %q, want %q", got.Title, "Test task")
    }

    // Update
    got.Title = "Updated"
    err = repo.Update(ctx, got)
    if err != nil {
        t.Fatalf("Update failed: %v", err)
    }

    // Delete
    err = repo.Delete(ctx, task.ID)
    if err != nil {
        t.Fatalf("Delete failed: %v", err)
    }

    // Verify deletion
    _, err = repo.GetByID(ctx, task.ID)
    if err == nil {
        t.Fatal("expected error after deletion, got nil")
    }
}
```

Запуск: `go test -tags=integration ./...` (требует DATABASE_URL).

Без тега: `go test ./...` — запускает только unit тесты (быстро, без зависимостей).

### Разделение unit и integration тестов

Разделение важно для скорости feedback loop:

| | Unit тесты | Интеграционные тесты |
|---|-----------|---------------------|
| Скорость | Миллисекунды | Секунды-минуты |
| Зависимости | Нет (моки) | БД, Docker, сеть |
| Когда запускать | После каждого изменения | Перед коммитом / в CI |
| Что ловят | Логические ошибки | Проблемы интеграции |

**Go:** build-теги (`//go:build integration`).
**Python:** маркеры pytest (`@pytest.mark.integration`), отдельные директории.
**TypeScript:** конфиги Jest/Vitest для разных наборов тестов.

## E2E тесты: проверка всей системы

E2E (End-to-End) тесты проверяют **весь пользовательский сценарий** — от UI (или API-вызова) до базы данных и обратно. Это самый дорогой, но самый убедительный вид тестирования.

### Зачем нужны E2E тесты

- **Ловят проблемы, которые не видны на уровне компонентов.** Каждый сервис работает правильно, но вместе — нет (пример: CLI name deadlock из Enji Fleet, где Agent Service и SDK использовали разные имена).
- **Проверяют реальный пользовательский опыт.** Страница загружается? Форма отправляется? Данные отображаются после создания?
- **Валидируют развёртывание.** Все сервисы запущены? Миграции применены? Конфигурация корректна?

### Инструменты для E2E

**Frontend E2E:**
- **Playwright** (рекомендуется) — кроссбраузерные тесты, автоматические ожидания, screenshots при ошибках
- **Cypress** — альтернатива Playwright

**Backend/API E2E:**
- Скрипты с curl/httpie для проверки API lifecycle
- Docker Compose для поднятия всей инфраструктуры
- Проверка: создать → прочитать → обновить → удалить → проверить что удалено

### Паттерны E2E тестов

#### Playwright (Frontend)

```typescript
import { test, expect } from '@playwright/test';

test.describe('Task Management', () => {
  test('user can create and view task', async ({ page }) => {
    // Navigate to app
    await page.goto('/');

    // Create task
    await page.click('button:has-text("New Task")');
    await page.fill('input[name="title"]', 'E2E Test Task');
    await page.click('button:has-text("Create")');

    // Verify task appears in list
    await expect(page.locator('text=E2E Test Task')).toBeVisible();
  });

  test('task board shows correct columns', async ({ page }) => {
    await page.goto('/');
    await expect(page.locator('text=Pending')).toBeVisible();
    await expect(page.locator('text=In Progress')).toBeVisible();
    await expect(page.locator('text=Done')).toBeVisible();
  });
});
```

#### API lifecycle E2E

```bash
#!/bin/bash
# scripts/e2e-test.sh — проверка полного lifecycle через API

BASE_URL="http://localhost:8080/api/v1"
TOKEN="Bearer $(make generate-token)"

echo "=== E2E Test: Task Lifecycle ==="

# 1. Create task
echo "Step 1: Create task"
TASK=$(curl -s -X POST "$BASE_URL/tasks" \
  -H "Authorization: $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title": "E2E Test", "description": "Automated test"}')
TASK_ID=$(echo $TASK | jq -r '.id')

if [ "$TASK_ID" = "null" ] || [ -z "$TASK_ID" ]; then
  echo "FAIL: Could not create task"
  exit 1
fi
echo "OK: Created task $TASK_ID"

# 2. Get task
echo "Step 2: Get task"
GOT=$(curl -s "$BASE_URL/tasks/$TASK_ID" -H "Authorization: $TOKEN")
GOT_TITLE=$(echo $GOT | jq -r '.title')

if [ "$GOT_TITLE" != "E2E Test" ]; then
  echo "FAIL: Title mismatch: $GOT_TITLE"
  exit 1
fi
echo "OK: Got task with correct title"

# 3. Update task
echo "Step 3: Update task"
curl -s -X PUT "$BASE_URL/tasks/$TASK_ID" \
  -H "Authorization: $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title": "E2E Updated"}'
UPDATED=$(curl -s "$BASE_URL/tasks/$TASK_ID" -H "Authorization: $TOKEN")
UPDATED_TITLE=$(echo $UPDATED | jq -r '.title')

if [ "$UPDATED_TITLE" != "E2E Updated" ]; then
  echo "FAIL: Update did not persist: $UPDATED_TITLE"
  exit 1
fi
echo "OK: Task updated successfully"

# 4. Delete task
echo "Step 4: Delete task"
curl -s -X DELETE "$BASE_URL/tasks/$TASK_ID" -H "Authorization: $TOKEN"
DELETE_CHECK=$(curl -s -o /dev/null -w "%{http_code}" \
  "$BASE_URL/tasks/$TASK_ID" -H "Authorization: $TOKEN")

if [ "$DELETE_CHECK" != "404" ]; then
  echo "FAIL: Task not deleted (status: $DELETE_CHECK)"
  exit 1
fi
echo "OK: Task deleted, returns 404"

echo "=== ALL E2E TESTS PASSED ==="
```

### E2E в Enji Fleet: test-e2e workflow

В Enji Fleet E2E тестирование — это отдельный **workflow mode** с чёткими фазами:

```
Phase 1: Build & Deploy → поднять всю платформу
Phase 2: Create Task & Monitor → создать задачу, следить за lifecycle
Phase 3: Verify Lifecycle → проверить state machine transitions
Phase 4: UI Verification → проверить фронтенд
Phase 5: Document Results → записать в trace
```

Правила безопасности при E2E:
- **Мониторить количество контейнеров.** Spawner может создавать контейнеры в цикле
- **При crash loop — сначала остановить сервис**, потом разбираться
- **Фиксировать каждый найденный баг** в trace сразу (не накапливать)

## Стратегия тестирования для AI-проектов

### Минимальный набор (для старта)

1. **Unit тесты для бизнес-логики.** Каждая функция с нетривиальной логикой покрыта 3-5 тестами (happy path + edge cases).
2. **Интеграционные тесты для API endpoints.** Каждый endpoint: успех + основные ошибки (404, 400).
3. **Линтер + type checker** в pre-commit hook.

### Стандартный набор (для активной разработки)

1. Всё из минимального набора
2. **Coverage > 80%** для нового кода
3. **Интеграционные тесты с реальной БД** (через тестовые контейнеры)
4. **E2E тесты для критических сценариев** (авторизация, основной CRUD)
5. **Автоматический запуск** в CI/CD

### Полный набор (для production)

1. Всё из стандартного набора
2. **E2E тесты через Playwright** для UI
3. **Performance тесты** для критичных endpoints
4. **Security сканирование** (dependency audit, SAST)
5. **Contract тесты** между сервисами

### Статистика из Enji Fleet

| Компонент | Unit тесты | Integration | E2E | Инструменты |
|-----------|-----------|-------------|-----|-------------|
| Backend (Go) | 195 файлов | build-tag separated | API lifecycle | go test, golangci-lint |
| Frontend (React) | 54 файла | — | 8 suites | Vitest, Playwright |
| **Итого** | 365+ тестов | DB-dependent | 16 Playwright tests | |

## Как агент должен писать тесты

### TDD workflow для агента

Самый эффективный подход — **Test-Driven Development**: сначала тесты, потом код.

```
1. Агент пишет тесты на основе спецификации
2. Запускает тесты → все падают (RED)
3. Пишет минимальный код для прохождения тестов
4. Запускает тесты → все проходят (GREEN)
5. Рефакторит код (если нужно)
6. Запускает тесты → всё ещё проходят
```

**Промпт для TDD:**
```
Задача: реализовать функцию validateEmail(email: string): boolean

Шаг 1: Напиши тесты ПЕРЕД реализацией. Покрой сценарии:
- Валидный email: user@example.com → true
- Без @ → false
- Без домена: user@ → false
- Без имени: @example.com → false
- Пустая строка → false
- С пробелами → false
- Несколько @: user@@example.com → false

Шаг 2: Реализуй функцию так, чтобы ВСЕ тесты прошли.
Шаг 3: Запусти тесты. Если падают — исправь код, не тесты.
```

### Блокирующие правила для тестов

Включите в AGENTS.md:

```markdown
## Testing Rules

**ОБЯЗАТЕЛЬНО:**
- Каждый новый endpoint покрыт минимум 1 integration тестом
- Каждая функция с бизнес-логикой покрыта unit тестами (min 3 сценария)
- Перед коммитом: все тесты проходят (0 failures)
- Coverage нового кода > 80%

**ЗАПРЕЩЕНО:**
- Код без тестов
- Пропускать falling tests ("добавлю потом")
- Удалять существующие тесты без обсуждения
- Изменять тест вместо исправления кода (если тест корректен)

**СТОП и исправь:**
- Тест падает → исправь код, пока тест не пройдёт
- Coverage ниже минимума → добавь тесты
- Линтер ругается → исправь все ошибки
```

### Типичные ошибки агентов с тестами

**Ошибка 1: Агент "исправляет" тест вместо кода**

Агент видит falling test и изменяет assertion вместо исправления бага. Это опасно — тест перестаёт проверять правильное поведение.

**Предотвращение:** "Если тест падает — исправь код, не тест. Тесты менять можно только если они содержат ошибку в самом тесте (неправильный expected value)."

**Ошибка 2: Тесты только на happy path**

Агент пишет `test_create_task_success` и считает задачу выполненной. Нет тестов на ошибки, edge cases, boundary values.

**Предотвращение:** Явно перечислите сценарии в промпте. "Покрой: success, not found (404), invalid input (400), empty input, boundary values."

**Ошибка 3: Тесты зависят друг от друга**

Тест №2 зависит от данных, созданных в тесте №1. Если тест №1 упал — весь suite падает.

**Предотвращение:** "Каждый тест должен быть независимым. Используй setUp/tearDown (или beforeEach/afterEach) для подготовки данных."

**Ошибка 4: Тесты слишком хрупкие (brittle)**

Тест проверяет точную строку ошибки: `expect(error.message).toBe("Task with ID 123 not found in database")`. Любое изменение формулировки ломает тест.

**Предотвращение:** Проверяйте структуру, не конкретные строки: `expect(error.code).toBe(404)` или `expect(error.message).toContain("not found")`.

## Практическое задание

### Упражнение 1: Добавьте unit тесты

Возьмите любую функцию в вашем проекте и попросите агента написать тесты:

```
Напиши unit тесты для [функция] в [файл].
Покрой минимум 5 сценариев: happy path, 2 error cases, 2 edge cases.
Используй table-driven tests (Go) или describe/it (JS/TS).
Запусти тесты после написания.
```

### Упражнение 2: Добавьте интеграционный тест для API

```
Напиши интеграционный тест для [endpoint].
Тест должен:
1. Создать ресурс (POST)
2. Прочитать его (GET) — проверить данные
3. Обновить (PUT) — проверить изменение
4. Удалить (DELETE) — проверить 404 после удаления
Запусти тесты.
```

### Упражнение 3: Настройте pre-commit проверки

Добавьте автоматический запуск тестов перед коммитом:

**Python:**
```yaml
# .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: pytest
        name: Run tests
        entry: pytest --tb=short -q
        language: system
        pass_filenames: false
```

**TypeScript (Husky + lint-staged):**
```json
// package.json
{
  "lint-staged": {
    "*.{ts,tsx}": ["eslint --fix", "prettier --write"],
    "*.test.{ts,tsx}": ["vitest related --run"]
  }
}
```

**Go:**
```bash
# .githooks/pre-commit
#!/bin/sh
go test ./... || exit 1
go vet ./... || exit 1
```

## Резюме

- **Тесты — единственная детерминистическая защита** от ошибок AI-генерированного кода
- **Пирамида:** много unit (быстрый feedback) → средне integration → мало E2E
- **Unit тесты** изолируют функции, ловят логические ошибки, работают за миллисекунды
- **Интеграционные тесты** проверяют взаимодействие с БД, API, внешними сервисами
- **E2E тесты** валидируют весь пользовательский сценарий от начала до конца
- **TDD** — самый эффективный подход для AI-assisted разработки (тесты = спецификация)
- **Блокирующие правила** в AGENTS.md гарантируют, что агент не пропустит тесты
- **Разделяйте** unit и integration тесты (build-теги, маркеры) для быстрого feedback loop
- **Machine acceptance precedes human acceptance** — автоматические проверки до человеческого ревью

---

## Источники

- [Building a C compiler with parallel Claudes](https://www.anthropic.com/engineering/building-c-compiler) — Anthropic (TDD как фактор успеха)
- [Using Linters to Direct Agents](https://blog.factory.ai/using-linters-to-direct-agents) — Factory.ai
- [Testing Trophy](https://kentcdodds.com/blog/the-testing-trophy-and-testing-classifications) — Kent C. Dodds
- [Playwright Documentation](https://playwright.dev/docs/intro) — Microsoft
- Enji Fleet test infrastructure — Mad Devs (365+ тестов, Vitest + Playwright + Go test)
