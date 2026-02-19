# Реализация и ревью результата

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

**SQL Injection**

```python
# ❌ ПЛОХО: SQL injection уязвимость
def delete_task(task_id):
    cursor.execute(f"DELETE FROM tasks WHERE id = {task_id}")

# ✅ ХОРОШО: параметризованный запрос или ORM
def delete_task(task_id):
    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
```

**Input Validation**

```python
# ❌ ПЛОХО: нет валидации — можно передать пустой title или 1MB строку
def create_task(title: str):
    cursor.execute("INSERT INTO tasks (title) VALUES (?)", (title,))

# ✅ ХОРОШО: валидация входных данных
def create_task(title: str):
    if not title or len(title) > 200:
        raise ValueError("Title must be 1-200 characters")
    cursor.execute("INSERT INTO tasks (title) VALUES (?)", (title,))
```

**Credentials в коде**

```python
# ❌ ПЛОХО: пароли попадают в Git историю навсегда
DATABASE_URL = "postgresql://user:password123@localhost/db"

# ✅ ХОРОШО: из environment variables
import os
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable not set")
```

**Что искать:**
- ❌ Raw SQL с интерполяцией строк (f-strings, template literals)
- ❌ Отсутствие валидации входных данных
- ❌ Credentials в коде (API keys, пароли, connection strings)

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
