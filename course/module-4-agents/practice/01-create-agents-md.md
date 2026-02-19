# Создай AGENTS.md для проекта

### Чек-лист готовности

Перед началом убедитесь что:
- [ ] Песочница task-manager настроена (Модуль 2)
- [ ] Claude Code настроен и работает
- [ ] Вы знакомы с промптингом (Модуль 3)
- [ ] Есть 45 минут для упражнений

---

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
