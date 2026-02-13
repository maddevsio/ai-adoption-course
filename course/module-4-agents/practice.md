# Модуль 4: Практика — Упражнения по работе с агентом

Четыре практических шага для освоения агентских паттернов. Общее время: 45 минут.

Работаем по flow: настройка AGENTS.md → описание проблемы → агент-планировщик → реализация → ревью → итерация.

## Чек-лист готовности

Перед началом убедитесь что:
- [ ] Песочница task-manager настроена (Модуль 2)
- [ ] Claude Code настроен и работает
- [ ] Вы знакомы с промптингом (Модуль 3)
- [ ] Есть 45 минут для упражнений

---

## Шаг 1: Создай AGENTS.md для проекта (10 мин)

### Цель

Научиться создавать конфигурационный файл, который задаёт правила работы агента с вашим проектом. AGENTS.md — это "конституция" проекта, которую агент читает перед началом любой задачи.

### Контекст

**AGENTS.md = CLAUDE.md = .cursorrules** — это разные названия одной идеи. Называйте файл в зависимости от инструмента:
- `AGENTS.md` — универсальное имя (рекомендуется)
- `CLAUDE.md` — для Claude Code CLI
- `.cursorrules` — для Cursor IDE

Если работаете с несколькими инструментами, создайте `AGENTS.md` и симлинк:

```bash
ln -s AGENTS.md CLAUDE.md
```

### Для какого проекта создавать

**Вариант A: Ваш реальный проект**

Если у вас есть рабочий проект на Python, TypeScript, Go, или другом стеке — используйте его.

**Вариант B: Учебная песочница**

Если нет подходящего проекта, используйте песочницу task-manager из Модуля 2 (practice-setup.md). Она была создана специально для упражнений курса:
- 3-5 файлов исходного кода
- Работающие эндпоинты (GET/POST /tasks)
- SQLite база данных
- Pytest или Jest тесты
- Намеренные "точки роста" для развития

**Проверка готовности песочницы:**

```bash
# Перейти в директорию
cd ~/practice/task-manager

# Проверить что проект работает
pytest  # для Python
# или
npm test  # для TypeScript

# Убедиться что есть git
git status
```

### Минимальная структура AGENTS.md

AGENTS.md должен содержать четыре обязательные секции: **Project**, **Stack**, **Conventions**, **Rules**.

#### Шаблон с комментариями

Создайте файл `AGENTS.md` в корне вашего проекта:

```markdown
# Project: [Название проекта]

[2-3 предложения о том, что делает проект]

Пример:
Task Manager — REST API для управления задачами.
Используется для практики AI-assisted разработки.
Основные операции: создание, чтение задач через HTTP API.

## Stack

[Точные версии технологий — не "используем Python", а "Python 3.11, FastAPI 0.104.1"]

Пример для Python:
- Python 3.11
- FastAPI 0.104.1
- SQLite (файл tasks.db)
- SQLAlchemy 2.0 для работы с БД
- pytest 7.4 + httpx для тестов
- ruff для линтинга

Пример для TypeScript:
- Node.js 20.x
- TypeScript 5.3
- Express 4.18
- SQLite3 для БД
- Jest 29 для тестов
- ESLint + Prettier для code style

## Structure

[Структура директорий и назначение файлов]

Пример для Python:
- main.py — точка входа, FastAPI app
- models.py — SQLAlchemy модели БД
- routes.py — API endpoints
- db.py — подключение к БД
- tests/ — pytest тесты

Пример для TypeScript:
- src/app.ts — Express приложение
- src/db.ts — подключение к SQLite
- src/routes/tasks.ts — маршруты API
- tests/tasks.test.ts — тесты endpoints

## Conventions

[Правила именования, стилевые соглашения]

Пример для Python:
- Следовать PEP 8
- Type hints обязательны для всех функций
- Docstrings в Google Style для публичных функций
- Файлы: snake_case, классы: PascalCase, функции: snake_case
- Все async handlers, никакого sync кода в endpoints

Пример для TypeScript:
- ESLint + Prettier (конфиг в .eslintrc)
- Строгий режим TypeScript (strict: true)
- Явные типы для всех параметров функций
- Файлы и переменные: camelCase, классы: PascalCase
- Async/await для всех database операций

## Rules

[Обязательные паттерны и процессы разработки]

Пример:
1. Каждый новый endpoint должен иметь минимум 1 тест
2. Перед коммитом запустить тесты: pytest (или npm test)
3. Проверить линтинг: ruff check . (или npm run lint)
4. Не изменять схему БД без миграций
5. Error handling: возвращать HTTP 400 для валидации, 404 для NotFound, 500 для server errors

## Forbidden

[Что агент НЕ должен делать]

Пример:
- НЕ коммитить .env файлы или secrets
- НЕ удалять существующие тесты без обсуждения
- НЕ использовать deprecated зависимости
- НЕ делать breaking changes в существующих endpoints
- НЕ пропускать тесты ("добавлю потом")

## Before Starting Work

[Инструкции для первого шага любой задачи]

Пример:
Перед началом любой задачи:
1. Прочитай этот файл (AGENTS.md)
2. Найди связанные файлы и тесты
3. Убедись что существующие тесты проходят
4. При изменении API — обнови тесты
```

### Эталонный AGENTS.md для песочницы task-manager

Для сверки и проверки. Если создаёте AGENTS.md для песочницы из Модуля 2, используйте этот эталон:

#### Для Python + FastAPI

```markdown
# Project: Task Manager API

REST API для управления задачами (CRUD операции).
Учебный проект для практики AI-assisted разработки.
База: SQLite, основные endpoints: GET/POST /tasks.

## Stack

- Python 3.11
- FastAPI 0.104.1
- SQLite (tasks.db)
- SQLAlchemy 2.0 для ORM
- pytest 7.4 + httpx для тестов
- ruff для линтинга и форматирования

## Structure

- main.py — FastAPI app, точка входа
- models.py — SQLAlchemy модели
- routes.py — API endpoints (если отдельно от main.py)
- db.py — database session и подключение
- tests/ — pytest тесты для endpoints

## Conventions

- Следовать PEP 8 (проверка через ruff)
- Type hints для всех функций: def create_task(title: str) -> Task
- Docstrings для публичных функций (Google Style)
- Async/await для всех endpoint handlers
- Pydantic models для request/response schemas

## Rules

1. Каждый endpoint покрыт минимум 1 integration тестом
2. Перед коммитом: pytest && ruff check .
3. HTTP status codes: 200 OK, 201 Created, 404 Not Found, 400 Bad Request
4. Все database операции через SQLAlchemy ORM (никаких raw SQL)
5. При добавлении полей в Task — создать Alembic миграцию

## Forbidden

- НЕ коммитить .env, __pycache__, *.db файлы
- НЕ удалять существующие тесты
- НЕ использовать sync database calls (только async)
- НЕ делать breaking changes без обсуждения

## Before Starting Work

Перед любой задачей:
1. Прочитай AGENTS.md
2. Запусти существующие тесты: pytest
3. Проверь что dev сервер работает: uvicorn main:app
```

#### Для TypeScript + Express

```markdown
# Project: Task Manager API

REST API для управления задачами.
Учебный проект для AI-assisted development практики.
Стек: TypeScript + Express + SQLite.

## Stack

- Node.js 20.x
- TypeScript 5.3
- Express 4.18
- SQLite3 для базы данных
- Jest 29 + supertest для тестов
- ESLint + Prettier для code style

## Structure

- src/app.ts — Express приложение и роутинг
- src/db.ts — SQLite подключение и queries
- src/routes/tasks.ts — task endpoints (если отдельно)
- src/types.ts — TypeScript типы и интерфейсы
- tests/tasks.test.ts — integration тесты

## Conventions

- ESLint + Prettier (конфигурация в .eslintrc и .prettierrc)
- Strict TypeScript mode (strict: true в tsconfig.json)
- Явные типы для всех параметров: function createTask(title: string): Promise<Task>
- Async/await для database операций
- CamelCase для переменных, PascalCase для типов и классов

## Rules

1. Каждый endpoint имеет минимум 1 integration тест
2. Перед коммитом: npm test && npm run lint
3. HTTP codes: 200, 201, 404, 400, 500
4. Error handling через try/catch в async handlers
5. Database queries через prepared statements (защита от SQL injection)

## Forbidden

- НЕ коммитить .env, node_modules/, *.db
- НЕ удалять существующие тесты
- НЕ использовать any тип (кроме крайних случаев)
- НЕ делать breaking changes в API без обсуждения
- НЕ использовать sync операции для I/O

## Before Starting Work

Перед началом задачи:
1. Прочитай AGENTS.md
2. Запусти тесты: npm test
3. Проверь сборку: npm run build
4. Убедись что dev сервер работает: npm start
```

### Задание

1. Создайте файл `AGENTS.md` в корне вашего проекта (или песочницы task-manager)
2. Заполните все обязательные секции: Project, Stack, Structure, Conventions, Rules, Forbidden, Before Starting Work
3. Убедитесь что файл отражает реальное состояние проекта (версии зависимостей, структуру папок)
4. Сохраните файл и закоммитьте в git:

```bash
git add AGENTS.md
git commit -m "docs: add AGENTS.md configuration for AI agent"
```

### Проверка

Ваш AGENTS.md готов к использованию, если:

- ✅ Содержит все 7 секций (Project, Stack, Structure, Conventions, Rules, Forbidden, Before Starting Work)
- ✅ Stack указывает точные версии (не "FastAPI", а "FastAPI 0.104.1")
- ✅ Rules содержат минимум 3-5 конкретных правил
- ✅ Forbidden явно перечисляет запреты (минимум 3 пункта)
- ✅ Файл находится в корне проекта
- ✅ Закоммичен в git

### Время выполнения

10 минут

---

## Шаг 2: Опиши проблему и получи план от агента (15 мин)

### Цель

Научиться правильно формулировать задачу для агента-планировщика и получать детализированный план реализации с критериями приёмки.

### Новый flow (не "вот тебе готовый промпт")

Вместо копирования готового промпта, вы проходите весь цикл самостоятельно:

1. **Описываете проблему** своими словами (как бы описали коллеге)
2. **Ставите задачу агенту-планировщику**: попросить декомпозировать на подзадачи
3. **Агент выдаёт план** с подзадачами и критериями
4. **Вы ревьюите план** и корректируете
5. **Дополняете требования**: просите добавить тесты, линтер-проверки, etc
6. **Агент реализует** утверждённый план

Это учит думать как Product Owner, который декомпозирует фичи на задачи для команды.

### Пример описания проблемы

**Задача для песочницы task-manager:**

Сейчас в task-manager есть только GET и POST для задач. Нужно добавить возможность обновлять существующую задачу.

**Описание своими словами (как бы сказали коллеге):**

> Нужен эндпоинт для обновления задачи. Должен работать так: клиент отправляет PUT /tasks/{id} с новым title, сервер обновляет задачу в БД и возвращает обновлённую версию. Если задачи с таким ID нет — вернуть 404.

### Промпт для агента-планировщика

Скопируйте этот промпт и запустите в вашем AI-агенте (Claude Code, Cursor, или другой инструмент):

```
Я описываю проблему. Твоя задача — проанализировать её, разбить на мелкие подзадачи, для каждой подзадачи указать критерии приёмки.

Проблема:
Нужен эндпоинт для обновления задачи в task-manager API.
Должен работать так: клиент отправляет PUT /tasks/{id} с новым title в body,
сервер обновляет задачу в БД и возвращает обновлённую версию.
Если задачи с таким ID нет — вернуть 404 Not Found.

Контекст проекта:
- Прочитай AGENTS.md в корне проекта (там указан стек и правила)
- Изучи существующие endpoints (GET /tasks, POST /tasks)
- Посмотри как структурированы тесты для существующих endpoints

Задачи для плана:
1. Опиши текущую архитектуру проекта (какие файлы, как организованы endpoints и БД)
2. Разбей задачу на мелкие подзадачи (например: обновить БД-слой, создать endpoint, написать тесты)
3. Для каждой подзадачи укажи:
   - Что нужно сделать
   - Какие файлы создать или изменить
   - Критерии приёмки (как проверить, что сделано правильно)
   - Какие тесты написать

НЕ реализуй код — только план. Я хочу проверить план перед тем, как ты начнёшь писать код.
```

### Пример ожидаемого плана от агента

Агент должен вернуть план примерно такой структуры:

```markdown
# План реализации: PUT /tasks/{id} endpoint

## Текущая архитектура

- Python + FastAPI проект
- БД: SQLite через SQLAlchemy
- Endpoints в main.py
- Модель Task в models.py с полями: id, title, created_at
- Тесты в tests/test_tasks.py

## Подзадачи

### Подзадача 1: Добавить БД-метод для обновления задачи

**Файл:** db.py (или models.py, в зависимости от структуры)

**Что сделать:**
- Создать функцию update_task(task_id: int, title: str) -> Task | None
- Функция находит задачу по ID, обновляет title, сохраняет в БД
- Возвращает обновлённую задачу или None если не найдена

**Критерии приёмки:**
- Функция имеет type hints
- Использует SQLAlchemy ORM (не raw SQL)
- Обрабатывает случай "задача не найдена"

### Подзадача 2: Создать Pydantic schema для запроса

**Файл:** main.py (или schemas.py)

**Что сделать:**
- Создать класс TaskUpdate(BaseModel) с полем title: str
- Добавить валидацию: title не пустой, длина 1-200 символов

**Критерии приёмки:**
- Schema наследуется от pydantic.BaseModel
- Валидация через Field или validator

### Подзадача 3: Создать PUT /tasks/{id} endpoint

**Файл:** main.py (или routes.py)

**Что сделать:**
- Endpoint принимает task_id (path parameter) и TaskUpdate (body)
- Вызывает update_task() из БД-слоя
- Возвращает 200 + обновлённую задачу или 404 если не найдена

**Критерии приёмки:**
- Endpoint использует async def
- Status codes: 200 для успеха, 404 для not found
- Возвращает Task модель (не dict)

### Подзадача 4: Написать integration тесты

**Файл:** tests/test_tasks.py

**Что сделать:**
Создать тесты для сценариев:
1. Успешное обновление задачи (PUT существующей задачи → 200)
2. Попытка обновить несуществующую задачу → 404
3. Валидация: пустой title → 400 (если есть валидация)
4. Проверка что title действительно обновился в БД

**Критерии приёмки:**
- Все тесты проходят (pytest)
- Coverage для нового endpoint минимум 80%
- Используется тот же паттерн, что и для существующих тестов

### Подзадача 5: Запустить проверки качества

**Что сделать:**
- Запустить pytest (все тесты должны проходить)
- Запустить линтер (ruff check . или npm run lint)
- Убедиться что нет TypeScript/mypy ошибок

**Критерии приёмки:**
- pytest: все тесты зелёные
- Линтер: 0 ошибок
- Код соответствует AGENTS.md conventions
```

### Чеклист: что должно быть в плане

План от агента считается хорошим, если содержит:

- ✅ **Анализ текущей архитектуры** (агент прочитал файлы и понял структуру)
- ✅ **Декомпозиция на подзадачи** (минимум 3-5 подзадач)
- ✅ **Для каждой подзадачи**: что делать, какие файлы, критерии приёмки
- ✅ **Тесты явно указаны** (какие сценарии покрыть)
- ✅ **Проверки качества** (линтер, тесты) включены как отдельная подзадача
- ✅ **Соответствие AGENTS.md** (агент учёл правила из конфигурации)

### Ревью и корректировка плана

После получения плана от агента:

**1. Проверьте, что агент прочитал AGENTS.md:**

Поищите в плане ссылки на технологии, conventions, или правила из AGENTS.md. Например, если в AGENTS.md указано "использовать async/await", план должен содержать "async def" для endpoints.

**2. Проверьте полноту:**

Все ли сценарии покрыты тестами? Агент предусмотрел случаи ошибок (404, валидация)?

**3. Дополните план (пример промпта):**

```
Хороший план. Дополни каждую подзадачу:

1. Для подзадачи с тестами — добавь конкретные assert'ы (что именно проверять)
2. Для подзадачи с endpoint — укажи точную сигнатуру функции
3. Добавь подзадачу: обновить документацию (если есть README с описанием API)

После дополнения — жду финальный план для утверждения.
```

**4. Утвердите план:**

```
План утверждён. Реализуй его. Следуй порядку подзадач. После каждой подзадачи — запускай тесты и проверяй линтер. Если тесты падают — исправь перед переходом к следующей подзадаче.
```

### Задание

1. Откройте ваш AI-агент (Claude Code, Cursor, или другой инструмент)
2. Перейдите в директорию вашего проекта (task-manager)
3. Скопируйте "Промпт для агента-планировщика" (см. выше)
4. Запустите промпт, получите план от агента
5. Проверьте план по чеклисту
6. Дополните план (попросите добавить детали по тестам и линтеру)
7. Утвердите финальный план

**НЕ переходите к реализации на этом шаге.** Остановитесь после получения утверждённого плана.

### Проверка

План готов к реализации, если:

- ✅ Агент прочитал AGENTS.md и учёл правила проекта
- ✅ План содержит 4-6 подзадач
- ✅ Для каждой подзадачи указаны файлы и критерии приёмки
- ✅ Тесты включены в план (минимум 3-4 тестовых сценария)
- ✅ Линтер и quality checks упомянуты
- ✅ Вы понимаете каждую подзадачу и согласны с подходом

### Время выполнения

15 минут

---

## Шаг 3: Реализация и ревью результата (10 мин)

### Цель

Агент реализует утверждённый план. Ваша задача — провести code review результата по чеклисту и найти типичные проблемы.

### Реализация

Если вы остановились на Шаге 2 с утверждённым планом, продолжите в том же chat-сессии:

```
План утверждён. Реализуй его.

Важно:
- Следуй порядку подзадач из плана
- После каждой подзадачи запускай тесты (pytest или npm test)
- Если тесты падают — исправляй до перехода к следующей подзадаче
- Проверяй линтер после завершения (ruff check . или npm run lint)

Не спрашивай разрешения на создание файлов или установку зависимостей — действуй автономно в рамках плана.
```

Агент начнёт работу. Дождитесь завершения всех подзадач.

### Чеклист ревью

После того как агент завершил реализацию, проверьте результат по этому чеклисту:

#### 1. Код работает?

```bash
# Для Python
pytest
# Ожидается: все тесты прошли (зелёные)

# Для TypeScript
npm test
# Ожидается: все тесты прошли
```

**Проверка вручную:**

```bash
# Запустить dev сервер
uvicorn main:app --reload  # Python
# или
npm start  # TypeScript

# В другом терминале — тестовый запрос
curl -X POST http://localhost:8000/tasks -H "Content-Type: application/json" -d '{"title": "Test task"}'
# Ожидается: 201, вернётся задача с ID

curl -X PUT http://localhost:8000/tasks/1 -H "Content-Type: application/json" -d '{"title": "Updated title"}'
# Ожидается: 200, вернётся задача с обновлённым title

curl -X PUT http://localhost:8000/tasks/999 -H "Content-Type: application/json" -d '{"title": "Updated"}'
# Ожидается: 404 Not Found
```

**Что искать:**
- ❌ Тесты падают — агент не проверил результат
- ❌ Endpoint не отвечает — ошибка в роутинге или БД
- ❌ Неправильные status codes (200 вместо 404)

#### 2. Тесты проходят?

```bash
# Запустить тесты с verbose выводом
pytest -v  # Python
npm test -- --verbose  # TypeScript
```

**Что искать:**
- ❌ Есть падающие тесты — агент не довёл задачу до конца
- ❌ Тесты пропущены (skipped) — агент не реализовал все сценарии
- ❌ Coverage ниже 80% для нового кода

**Проверка coverage (опционально):**

```bash
# Python
pytest --cov=. --cov-report=term

# TypeScript
npm test -- --coverage
```

#### 3. Линтер чистый?

```bash
# Python
ruff check .
# Ожидается: 0 ошибок

# TypeScript
npm run lint
# Ожидается: 0 errors, 0 warnings
```

**Что искать:**
- ❌ Ошибки импортов (unused imports)
- ❌ Type errors (для TypeScript/Python с mypy)
- ❌ Нарушения code style (длинные строки, отсутствие пробелов)

#### 4. Стиль соответствует AGENTS.md?

Откройте изменённые файлы и проверьте:

```bash
# Посмотреть diff
git diff
```

**Проверка:**

- ✅ Type hints есть для всех функций (Python) или типы указаны (TypeScript)
- ✅ Docstrings для публичных функций (если требуются в AGENTS.md)
- ✅ Используется async/await (если указано в правилах)
- ✅ Naming conventions соблюдены (snake_case, camelCase, etc)
- ✅ Код форматирован согласно AGENTS.md (PEP 8, Prettier, etc)

**Что искать:**
- ❌ Отсутствуют type hints: `def update_task(task_id, title)` вместо `def update_task(task_id: int, title: str) -> Task | None`
- ❌ Не используется async: `def get_task()` вместо `async def get_task()`
- ❌ Неправильное именование: `UpdateTask` вместо `update_task` (для функций)

#### 5. Нет лишних файлов/зависимостей?

```bash
# Проверить что добавлено в git
git status

# Проверить изменения в зависимостях
git diff requirements.txt  # Python
git diff package.json      # TypeScript
```

**Что искать:**
- ❌ Файлы БД закоммичены (tasks.db, *.sqlite)
- ❌ .env файл в git
- ❌ __pycache__, node_modules/ добавлены
- ❌ Лишние зависимости установлены (агент добавил библиотеку, которая не нужна)

#### 6. Нет security-проблем?

**Проверка кода:**

**Пример 1: SQL Injection**

```python
# ❌ ПЛОХО: SQL injection уязвимость
def delete_task(task_id):
    cursor.execute(f"DELETE FROM tasks WHERE id = {task_id}")

def update_task(task_id, title):
    cursor.execute(f"UPDATE tasks SET title = '{title}' WHERE id = {task_id}")

# Почему это опасно:
# Злоумышленник может передать task_id="1 OR 1=1" и удалить ВСЕ задачи
# Или title="'; DROP TABLE tasks; --" и уничтожить таблицу целиком
# f-strings и конкатенация строк в SQL-запросах = критическая уязвимость

# ✅ ХОРОШО: Используем параметризованный запрос
def delete_task(task_id):
    # Параметризованный запрос защищает от SQL injection
    # Драйвер БД автоматически экранирует специальные символы
    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))

def update_task(task_id, title):
    # ORM автоматически экранирует данные и использует prepared statements
    # Это безопасный способ работы с БД
    task = session.query(Task).filter(Task.id == task_id).first()
    task.title = title
```

```typescript
// ❌ ПЛОХО: SQL injection
function deleteTask(id: number) {
  db.run(`DELETE FROM tasks WHERE id = ${id}`);
}

function updateTask(id: number, title: string) {
  db.run(`UPDATE tasks SET title = '${title}' WHERE id = ${id}`);
}

// Почему это опасно:
// Template literals (${}) в SQL-запросах позволяют инъекцию произвольного кода
// Атакующий может передать title = "'; DROP TABLE tasks; --" и уничтожить данные
// Даже type checking TypeScript не защищает от SQL injection

// ✅ ХОРОШО: prepared statement
function deleteTask(id: number) {
  // Prepared statement с placeholder (?) защищает от SQL injection
  // БД получает SQL и параметры раздельно, никакого смешивания строк
  db.run('DELETE FROM tasks WHERE id = ?', [id]);
}

function updateTask(id: number, title: string) {
  // Параметры передаются отдельно и автоматически экранируются
  // Это единственный безопасный способ работы с пользовательскими данными в SQL
  db.run('UPDATE tasks SET title = ? WHERE id = ?', [title, id]);
}
```

**Пример 2: Input Validation**

```python
# ❌ ПЛОХО: Нет валидации
def create_task(title: str, description: str):
    cursor.execute(
        "INSERT INTO tasks (title, description) VALUES (?, ?)",
        (title, description)
    )

# Почему это опасно:
# - Можно создать задачу с пустым title
# - Можно передать title длиной 1 миллион символов и переполнить БД
# - Никакой защиты от некорректных данных
# - Агент может обработать невалидный input и создать проблемы

# ✅ ХОРОШО: Валидация входных данных
def create_task(title: str, description: str):
    # Проверка обязательных полей
    if not title or len(title) > 200:
        raise ValueError("Title must be 1-200 characters")

    if len(description) > 2000:
        raise ValueError("Description too long (max 2000 characters)")

    # Безопасное сохранение с параметризованным запросом
    cursor.execute(
        "INSERT INTO tasks (title, description) VALUES (?, ?)",
        (title, description)
    )

# ✅ ЕЩЕ ЛУЧШЕ: Валидация с типами и санитизацией
def create_task(title: str, description: str):
    # Валидация типов
    if not isinstance(title, str) or not isinstance(description, str):
        raise TypeError("Title and description must be strings")

    # Очистка от лишних пробелов
    title = title.strip()
    description = description.strip()

    # Проверка обязательных полей
    if not title:
        raise ValueError("Title cannot be empty")

    if len(title) > 200:
        raise ValueError("Title too long (max 200 characters)")

    if len(description) > 2000:
        raise ValueError("Description too long (max 2000 characters)")

    # Защита от специальных символов (опционально, зависит от требований)
    import html
    title = html.escape(title)
    description = html.escape(description)

    # Безопасное сохранение
    cursor.execute(
        "INSERT INTO tasks (title, description) VALUES (?, ?)",
        (title, description)
    )
```

```typescript
// ❌ ПЛОХО: Нет валидации
function createTask(title: string, description: string) {
  db.run('INSERT INTO tasks (title, description) VALUES (?, ?)',
    [title, description]);
}

// Почему это опасно:
// - TypeScript проверяет типы на этапе компиляции, но не валидирует содержимое
// - Пользователь может передать пустую строку или строку длиной 1MB
// - Нет защиты от некорректных данных во время выполнения

// ✅ ХОРОШО: Валидация входных данных
function createTask(title: string, description: string) {
  // Проверка обязательных полей
  if (!title || title.length > 200) {
    throw new Error("Title must be 1-200 characters");
  }

  if (description.length > 2000) {
    throw new Error("Description too long (max 2000 characters)");
  }

  // Безопасное сохранение
  db.run('INSERT INTO tasks (title, description) VALUES (?, ?)',
    [title, description]);
}

// ✅ ЕЩЕ ЛУЧШЕ: Валидация с санитизацией и детальными ошибками
function createTask(title: string, description: string) {
  // Проверка типов во время выполнения
  if (typeof title !== 'string' || typeof description !== 'string') {
    throw new TypeError("Title and description must be strings");
  }

  // Очистка от лишних пробелов
  title = title.trim();
  description = description.trim();

  // Детальная валидация с понятными сообщениями
  if (!title) {
    throw new Error("Title cannot be empty");
  }

  if (title.length > 200) {
    throw new Error(`Title too long: ${title.length} characters (max 200)`);
  }

  if (description.length > 2000) {
    throw new Error(`Description too long: ${description.length} characters (max 2000)`);
  }

  // Защита от специальных символов (опционально)
  const escapeHtml = (str: string) =>
    str.replace(/[&<>"']/g, (char) => ({
      '&': '&amp;', '<': '&lt;', '>': '&gt;',
      '"': '&quot;', "'": '&#39;'
    }[char] || char));

  const sanitizedTitle = escapeHtml(title);
  const sanitizedDescription = escapeHtml(description);

  // Безопасное сохранение
  db.run('INSERT INTO tasks (title, description) VALUES (?, ?)',
    [sanitizedTitle, sanitizedDescription]);
}
```

**Пример 3: Plaintext Credentials**

```python
# ❌ ПЛОХО: Credentials в коде
DATABASE_URL = "postgresql://user:password123@localhost/db"
API_KEY = "sk-ant-api03-xyz123"

# Почему это катастрофа:
# - Пароли попадают в Git историю и остаются там навсегда
# - Любой с доступом к репозиторию получает все credentials
# - При утечке кода (публичный GitHub, stolen laptop) — компрометация всей системы
# - Нельзя ротировать пароли без изменения кода
# - Один код для dev, staging, production — нарушение безопасности

# ✅ ХОРОШО: Из environment variables
import os

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable not set")

API_KEY = os.getenv("ANTHROPIC_API_KEY")
if not API_KEY:
    raise ValueError("ANTHROPIC_API_KEY not set")

# Преимущества этого подхода:
# - Credentials не в коде и не в Git
# - Разные credentials для разных окружений (dev/staging/prod)
# - Легко ротировать: изменили переменную окружения, перезапустили сервис
# - Соответствует 12-factor app principles
# - Безопасно при утечке исходного кода

# ✅ ЕЩЕ ЛУЧШЕ: Использование .env файла для локальной разработки
from dotenv import load_dotenv
import os

# Загрузить .env файл (только в dev окружении)
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL not set. Create .env file with DATABASE_URL=...")

# Важно: .env файл добавлен в .gitignore, не попадает в Git
# На production используются реальные environment variables от облачного провайдера
```

```typescript
// ❌ ПЛОХО: Credentials в коде
const DATABASE_URL = "postgresql://user:password123@localhost/db";
const API_KEY = "sk-ant-api03-xyz123";

// Почему это катастрофа:
// - Пароли в Git истории навсегда (даже после удаления коммита)
// - Компрометация при утечке кода или публикации в публичный репозиторий
// - Невозможно использовать разные credentials для dev/staging/prod
// - Нарушение всех security best practices

// ✅ ХОРОШО: Из environment variables
const DATABASE_URL = process.env.DATABASE_URL;
if (!DATABASE_URL) {
  throw new Error("DATABASE_URL environment variable not set");
}

const API_KEY = process.env.ANTHROPIC_API_KEY;
if (!API_KEY) {
  throw new Error("ANTHROPIC_API_KEY not set");
}

// ✅ ЕЩЕ ЛУЧШЕ: Использование dotenv для локальной разработки
import dotenv from 'dotenv';

// Загрузить .env файл (только в dev окружении)
if (process.env.NODE_ENV !== 'production') {
  dotenv.config();
}

const DATABASE_URL = process.env.DATABASE_URL;
if (!DATABASE_URL) {
  throw new Error("DATABASE_URL not set. Create .env file with DATABASE_URL=...");
}

const API_KEY = process.env.ANTHROPIC_API_KEY;
if (!API_KEY) {
  throw new Error("ANTHROPIC_API_KEY not set");
}

// Важно:
// 1. Добавьте .env в .gitignore
// 2. Создайте .env.example с примерами (без реальных значений)
// 3. В production используйте environment variables от облачного провайдера
// 4. Никогда не коммитьте .env в Git
```

**Что искать:**
- ❌ Raw SQL с интерполяцией строк (f-strings, template literals)
- ❌ Отсутствие валидации входных данных
- ❌ Credentials в коде (API keys, пароли, connection strings)

**Пример 4: Валидация агентского input**

```python
# ❌ ПЛОХО: Агент обрабатывает user_id без проверки
def get_user_tasks(user_id):
    # Если user_id = -1 или "admin" или None — непредсказуемое поведение
    return db.query(f"SELECT * FROM tasks WHERE user_id = {user_id}")

# ✅ ХОРОШО: Валидация перед обработкой
def get_user_tasks(user_id):
    # Валидация обязательна даже для "внутренних" функций
    if not isinstance(user_id, int):
        raise TypeError(f"user_id must be int, got {type(user_id)}")

    if user_id <= 0:
        raise ValueError(f"user_id must be positive, got {user_id}")

    # Безопасный запрос с параметризацией
    return db.query("SELECT * FROM tasks WHERE user_id = ?", (user_id,))
```

```typescript
// ❌ ПЛОХО: Агент обрабатывает task_id без проверки
function deleteTask(task_id: any) {
  // any тип отключает проверки TypeScript
  db.run(`DELETE FROM tasks WHERE id = ${task_id}`);
}

// ✅ ХОРОШО: Валидация типов и значений
function deleteTask(task_id: number) {
  // Runtime проверка, даже если TypeScript указывает number
  if (typeof task_id !== 'number' || !Number.isInteger(task_id)) {
    throw new TypeError(`task_id must be integer, got ${typeof task_id}`);
  }

  if (task_id <= 0) {
    throw new RangeError(`task_id must be positive, got ${task_id}`);
  }

  // Безопасное удаление
  db.run('DELETE FROM tasks WHERE id = ?', [task_id]);
}
```

**Принцип:** Никогда не доверяйте входным данным, даже если они от "доверенного" источника. Агент может получить некорректные данные из-за ошибки в другой части системы.

### Подводные камни: что агент типично делает не так

На основе реальной практики с AI-агентами, вот типичные ошибки:

#### Ошибка 1: Агент создал функционал, но не написал тесты

**Симптомы:** Код работает вручную (через curl), но в tests/ нет новых тестов.

**Как проверить:**

```bash
git diff tests/
# Если нет изменений — тесты не добавлены
```

**Почему происходит:** Агент не включил тесты в критерии приёмки, или вы не указали это явно в плане.

#### Ошибка 2: Тесты есть, но они не покрывают edge cases

**Симптомы:** Есть тест для "успешного обновления", но нет тестов для 404, валидации, пустых данных.

**Как проверить:** Посмотреть список тестов:

```bash
pytest --collect-only  # Python
npm test -- --listTests  # TypeScript
```

**Что должно быть:**
- test_update_task_success
- test_update_task_not_found (404)
- test_update_task_invalid_title (валидация)

#### Ошибка 3: Агент сломал существующие тесты

**Симптомы:** Новые тесты проходят, но старые падают.

**Как проверить:**

```bash
pytest  # все тесты
# Смотрим на FAILED секцию
```

**Почему происходит:** Агент изменил что-то в shared коде (models, database setup), что затронуло другие части.

#### Ошибка 4: Линтер игнорируется

**Симптомы:** Код работает, но линтер выдаёт ошибки.

**Почему происходит:** Агент не запустил линтер после изменений, или AGENTS.md не содержал требование "линтер чистый".

#### Ошибка 5: Агент добавил ненужную зависимость

**Пример:** Для обновления задачи агент установил библиотеку `pydantic-validators`, хотя встроенной валидации Pydantic достаточно.

**Как проверить:**

```bash
git diff requirements.txt
# или
git diff package.json
```

**Что делать:** Удалить лишнюю зависимость, попросить агента переписать код без неё.

#### Ошибка 6: Игнорирование AGENTS.md

**Пример:** В AGENTS.md указано "async/await обязательно", но агент написал sync функцию.

**Как проверить:** Открыть diff и найти `def function_name():` вместо `async def function_name():`.

### Задание

1. Убедитесь что агент завершил реализацию плана из Шага 2
2. Пройдитесь по чеклисту ревью (6 пунктов выше)
3. Для каждого пункта — проверьте и запишите: ✅ ОК или ❌ Проблема найдена
4. Если нашли проблемы — переходите к Шагу 4 (Итерация)

### Проверка

Ревью завершено, если вы проверили все 6 пунктов:

- ✅ Код работает (тесты проходят, endpoint отвечает)
- ✅ Тесты написаны и проходят (минимум 3-4 сценария)
- ✅ Линтер чистый (0 ошибок)
- ✅ Стиль соответствует AGENTS.md (type hints, async, naming)
- ✅ Нет лишних файлов в git (БД, .env, кеш)
- ✅ Нет security-проблем (SQL injection, credentials в коде)

### Время выполнения

10 минут

---

## Шаг 4: Итерация — исправь найденные проблемы (10 мин)

### Цель

Научиться давать агенту конкретную обратную связь для исправления проблем, найденных на ревью.

### Сценарий

На Шаге 3 вы провели ревью и нашли проблемы (например: нет тестов для 404, линтер ругается, отсутствуют type hints). Теперь нужно поставить агенту задачу исправить их.

### Как НЕ надо ставить задачу

**Плохой промпт:**

```
Исправь всё что не так
```

**Почему плохо:**
- Агент не знает, что именно не так
- Может исправить не те проблемы
- Или вообще ничего не сделать

### Как надо ставить задачу

**Хороший промпт (на основе конкретных проблем из ревью):**

```
Я провёл ревью. Найдены следующие проблемы:

1. Отсутствуют тесты для edge cases:
   - Нет теста для PUT /tasks/999 (несуществующий ID) → ожидается 404
   - Нет теста для валидации: пустой title → ожидается 400

2. Линтер ругается:
   - main.py:45 — отсутствует type hint для параметра title
   - main.py:52 — unused import: from typing import List

3. Нарушение AGENTS.md:
   - Функция update_task использует sync код вместо async
   - Отсутствует docstring для функции update_task

Задача:
1. Добавь тесты для edge cases (пункт 1)
2. Исправь ошибки линтера (пункт 2)
3. Приведи код в соответствие с AGENTS.md (пункт 3)

После исправлений:
- Запусти pytest (все тесты должны проходить)
- Запусти ruff check . (0 ошибок)
- Покажи diff изменений для проверки
```

### Типичные проблемы и промпты для исправления

#### Проблема 1: Агент не написал тесты для edge cases

**Промпт:**

```
Добавь тесты в tests/test_tasks.py для следующих сценариев:

1. test_update_task_not_found:
   - Попытка обновить задачу с ID=999 (не существует)
   - Ожидается: HTTP 404
   - Assert: response.status_code == 404

2. test_update_task_empty_title:
   - Попытка обновить задачу с пустым title: {"title": ""}
   - Ожидается: HTTP 400 (если есть валидация) или 200 (если валидации нет)
   - Assert: проверь что title не изменился в БД

3. test_update_task_title_too_long:
   - Title длиной 500 символов (если есть лимит в 200)
   - Ожидается: HTTP 400

После добавления — запусти pytest и убедись что все тесты проходят.
```

#### Проблема 2: Линтер ругается на отсутствие type hints

**Промпт:**

```
Линтер выдаёт ошибки:

main.py:45 — Missing type hint for parameter 'title'
main.py:52 — Unused import: from typing import List

Исправь:
1. Добавь type hints для всех параметров функции update_task
2. Удали unused import

Запусти ruff check . после исправлений.
```

#### Проблема 3: Агент использовал sync вместо async

**Промпт:**

```
В AGENTS.md указано: "Все endpoint handlers должны использовать async/await".

Проблема: функция update_task определена как sync:
def update_task(task_id: int, title: str):
    ...

Исправь:
1. Переделай update_task в async:
   async def update_task(task_id: int, title: str):
2. Обнови все вызовы: вместо update_task() используй await update_task()
3. Убедись что БД-операции также async (через await session.execute())

Запусти тесты после изменений — убедись что всё работает.
```

#### Проблема 4: Агент сломал существующие тесты

**Промпт:**

```
После твоих изменений падают старые тесты:

FAILED tests/test_tasks.py::test_get_tasks - AssertionError

Проблема: ты изменил структуру Task model (добавил поле 'updated_at'),
но не обновил фикстуры в tests/conftest.py.

Исправь:
1. Обнови фикстуру create_task() в tests/conftest.py — добавь поле updated_at
2. Запусти pytest — убедись что все тесты проходят (старые и новые)
```

#### Проблема 5: Лишние файлы в git

**Промпт:**

```
git status показывает:
- tasks.db (файл БД)
- __pycache__/

Эти файлы не должны попадать в git (см. AGENTS.md → Forbidden).

Исправь:
1. Убери tasks.db и __pycache__/ из staged:
   git reset HEAD tasks.db __pycache__/

2. Добавь в .gitignore:
   *.db
   __pycache__/

3. Проверь: git status не должен показывать эти файлы
```

### Повторное ревью

После того как агент исправил проблемы:

1. Запустите тесты:

```bash
pytest  # или npm test
```

2. Запустите линтер:

```bash
ruff check .  # или npm run lint
```

3. Проверьте diff:

```bash
git diff
```

4. Если всё ОК — можно коммитить:

```bash
git add .
git commit -m "feat: add PUT /tasks/{id} endpoint for updating tasks"
```

### Когда остановиться

**Правило 3 итераций:** Если после 3 попыток проблема не решена — смените подход.

Агенты не всегда могут решить задачу с первого раза. Важно знать, когда остановиться:

**Стратегия:**
1. **Итерация 1:** Дайте агенту задачу, получите результат
2. **Итерация 2:** Если есть проблемы, дайте конкретную обратную связь
3. **Итерация 3:** Последняя попытка с ещё более детальными инструкциями

**Если после 3 итераций проблема не решена:**
- ❌ НЕ продолжайте бесконечно — агент может застрять в цикле
- ✅ Исправьте проблему вручную ИЛИ
- ✅ Разбейте задачу на более мелкие подзадачи ИЛИ
- ✅ Упростите требования

**Пример зацикливания:**
- Итерация 1: Агент добавил тесты, но они падают
- Итерация 2: Агент исправил тесты, но сломал линтер
- Итерация 3: Агент исправил линтер, но тесты снова падают

→ **Остановитесь.** Исправьте проблему вручную или разбейте на части (например: сначала только тесты, потом только линтер).

### Задание

1. Возьмите список проблем, найденных на Шаге 3 (ревью)
2. Для каждой проблемы — напишите конкретный промпт с описанием проблемы и критериями исправления
3. Дайте агенту задачу исправить проблемы
4. После исправлений — проведите повторное ревью (запустите тесты, линтер, проверьте diff)
5. Если всё ОК — закоммитьте изменения

### Проверка

Итерация завершена успешно, если:

- ✅ Все тесты проходят (pytest или npm test — зелёные)
- ✅ Линтер чистый (0 ошибок)
- ✅ Код соответствует AGENTS.md (type hints, async, conventions)
- ✅ Нет лишних файлов в git status
- ✅ Изменения закоммичены

### Время выполнения

10 минут

---

## Итоги модуля

Поздравляем! Вы прошли полный цикл работы с AI-агентом:

1. **Шаг 1:** Создали AGENTS.md — конституцию проекта для агента
2. **Шаг 2:** Описали проблему, получили план от агента-планировщика
3. **Шаг 3:** Агент реализовал план, вы провели code review по чеклисту
4. **Шаг 4:** Дали агенту обратную связь, он исправил проблемы

### Что вы научились делать

- Создавать AGENTS.md с правилами проекта (Stack, Conventions, Rules, Forbidden)
- Формулировать задачу для агента-планировщика
- Ревьюить план перед реализацией (предотвращать "агент ушёл не туда")
- Интегрировать качество в процесс (тесты, линтер, критерии приёмки)
- Проводить code review результата по чеклисту из 6 пунктов
- Давать агенту конкретную обратную связь для итераций

### Ключевые паттерны

**Flow: проблема → планировщик → план → реализация → ревью → итерация**

Вместо "вот тебе готовый промпт" вы прошли весь цикл самостоятельно — это учит думать как Product Owner или Tech Lead.

**Агент сразу фреймится на качество:**

"Реализуй endpoint" → "Реализуй endpoint, покрой тестами, убедись что pytest проходит, проверь линтер"

**Human-in-the-loop для критичных этапов:**

План проверяется до реализации. Результат ревьюится перед коммитом. Агент не работает полностью автономно.

### Связь с другими модулями

**Модуль 3 (Промптинг):** Вы применили навыки написания эффективных промптов для агента-планировщика.

**Модуль 5 (Specification-Driven Development):** AGENTS.md — это спецификация стиля и правил. В Модуле 5 добавятся спецификации API (OpenAPI, JSON Schema).

**Модуль 6 (MCP интеграции):** AGENTS.md будет дополняться правилами для MCP-серверов (Git, Jira, Figma).

**Модуль 7 (Оркестрация):** Паттерн Plan/Act будет автоматизирован через headless режим.

### Следующие шаги

1. Примените AGENTS.md к вашему реальному проекту (не только песочнице)
2. Настройте pre-commit hooks для автоматической проверки AGENTS.md правил (Модуль 6)
3. Изучите **Enji Fleet** constitution как эталон (примечание: **Enji Fleet** — учебный проект Mad Devs, документация доступна студентам курса)

### Дополнительные материалы

**Файлы-примеры AGENTS.md:**
- **Enji Fleet** (учебный проект Mad Devs): `docs/prompts/CONSTITUTION.md`
- Task Manager (эталон для песочницы): в этом файле (Шаг 1)

**Паттерны агентских систем:**
- Simon Willison: "Things we learned about LLMs in 2024" (steering, constitution)
- Swyx: "The Agents Future" (Plan/Act/Observe цикл)

### Практические советы

**Обновляйте AGENTS.md по мере работы:**

Каждая повторяющаяся ошибка агента → сигнал добавить правило в AGENTS.md. Файл должен эволюционировать вместе с проектом.

**Используйте версионирование:**

AGENTS.md в git позволяет откатывать изменения правил. Если новое правило сломало workflow — откатите через `git revert`.

**Шаблоны для типовых задач:**

Создайте папку `.claude/templates/` с промптами для частых задач:
- `add-endpoint.md` — шаблон для добавления REST endpoint
- `add-test.md` — шаблон для написания тестов
- `refactor.md` — шаблон для рефакторинга

Используйте: `claude -p "$(cat .claude/templates/add-endpoint.md)"`

---

## Следующие шаги

После завершения этого модуля вы готовы к:

1. **Модуль 5: Spec-Driven Development**
   - Применение агентов для реализации спецификаций
   - Трёхфазный подход: spec → implementation → trace
   - Практика: написать 3 skill с полным SDD циклом

2. **Модуль 6: Model Context Protocol (MCP)**
   - Расширение возможностей агентов через MCP-серверы
   - Интеграция с внешними системами (Git, Jira, Figma)
   - Практика: настроить 4 обязательных MCP-сервера

3. **Модуль 7: Оркестрация**
   - Координация нескольких агентов для сложных задач
   - Ralph Loop и fail-until-done паттерны
   - Переход от кодера к архитектору проекта

4. **Проект (Модуль 8)**
   - Применение всех навыков в реальном проекте
   - Демонстрация навыков уровня 4-5

**Рекомендация:** Сохраните созданный AGENTS.md — он станет основой для следующих модулей. Каждый новый модуль будет дополнять этот файл новыми паттернами и ограничениями.

---

**Общее время модуля:** 45 минут

**Готовы к следующему модулю?** Переходите к Модулю 5: Specification-Driven Development.
