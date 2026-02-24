# Установка рабочего окружения

## Установить Claude Code 
> Пошаговая инструкция по установке Claude Code CLI — основного инструмента курса

https://code.claude.com/docs/en/quickstart

Проверить, что работает:
```bash
claude -p "Привет, Claude!"
```

## Первый тест: Анализ архитектуры проекта

### Если у вас есть свой проект

```bash
# Перейти в директорию вашего проекта
cd ~/projects/your-project

# Запустить Claude Code
claude

# В интерактивном режиме дать задачу:
# > Проанализируй архитектуру этого проекта. Создай файл ARCHITECTURE.md
# > со следующими секциями: технологический стек, структура директорий,
# > основные модули и их взаимодействие, точки входа.
```

**Ожидаемый результат:**
1. Агент прочитает файлы проекта (package.json, requirements.txt, src/, и т.д.)
2. Проанализирует структуру директорий
3. Определит используемые технологии
4. Создаст файл `ARCHITECTURE.md` с подробным описанием архитектуры
5. Время выполнения: 2-5 минут

**Критерии успеха:**
- Файл `ARCHITECTURE.md` создан
- Все основные компоненты проекта описаны
- Технологический стек определен корректно
- Диаграмма взаимодействия модулей присутствует

### Если у вас нет подходящего проекта

Создайте учебную песочницу за 5 минут:

#### Python + FastAPI

```bash
# Создать директорию проекта
mkdir -p ~/practice/task-manager && cd ~/practice/task-manager

# Инициализировать git
git init

# Создать виртуальное окружение
python3 -m venv venv
source venv/bin/activate  # или venv\Scripts\activate на Windows

# Установить зависимости
pip install fastapi uvicorn pytest httpx

# Сохранить requirements.txt
pip freeze > requirements.txt
```

**Промпт для агента:**

```bash
claude
```

```
Создай минимальный FastAPI-проект Task Manager со следующими требованиями:

1. Эндпоинты:
   - GET /tasks — список всех задач
   - POST /tasks — создание новой задачи
   - GET /tasks/{id} — получение задачи по ID

2. Хранилище: SQLite (файл tasks.db)

3. Структура задачи:
   - id (автоинкремент)
   - title (строка)
   - created_at (timestamp)

4. Pytest тесты для всех эндпоинтов

5. НЕ делай:
   - Валидацию данных (будем добавлять позже)
   - PUT/DELETE эндпоинты (будем добавлять позже)
   - Аутентификацию

Цель: создать работающую базу для дальнейшего развития в упражнениях курса.
```

#### TypeScript + Express (альтернатива)

```bash
# Создать проект
mkdir -p ~/practice/task-manager && cd ~/practice/task-manager
git init

# Инициализировать Node.js проект
npm init -y

# Установить зависимости
npm install express sqlite3
npm install -D typescript @types/node @types/express ts-node jest @types/jest supertest @types/supertest

# Создать tsconfig.json
npx tsc --init
```

**Промпт для агента:**

```
Создай минимальный Express + TypeScript проект Task Manager:

1. Эндпоинты:
   - GET /tasks
   - POST /tasks
   - GET /tasks/:id

2. База: SQLite (tasks.db)

3. Типы TypeScript для Task

4. Jest тесты для всех эндпоинтов

5. БЕЗ валидации, БЕЗ PUT/DELETE, БЕЗ авторизации

Структура проекта:
- src/app.ts
- src/db.ts
- src/routes/tasks.ts
- tests/tasks.test.ts
```

**Ожидаемый результат песочницы:**
- 3-5 файлов исходного кода
- Работающие эндпоинты (можно проверить через `curl` или Postman)
- Тесты проходят (все зелёные)
- Намеренные "точки роста" для упражнений модулей 4-7:
  - Нет валидации входных данных
  - Нет PUT/DELETE операций
  - Нет обработки ошибок
  - Нет документации AGENTS.md

**Проверка песочницы:**

```bash
# Python
pytest
# Ожидается: все тесты прошли

uvicorn main:app --reload
# Ожидается: сервер запущен на http://localhost:8000

curl http://localhost:8000/tasks
# Ожидается: []
```

```bash
# TypeScript
npm test
# Ожидается: все тесты прошли

npm start
# Ожидается: сервер запущен на http://localhost:3000

curl http://localhost:3000/tasks
# Ожидается: []
```

## Базовая настройка проекта

### Создание CLAUDE.md

Каждый проект должен иметь файл `CLAUDE.md` в корне — это инструкция для AI-агента о правилах работы с вашим проектом.

```bash
cd ~/projects/your-project
```

**Создайте `CLAUDE.md`:**

```markdown
# Claude Code Configuration

## Project Context

[Краткое описание проекта — 2-3 предложения]

Пример:
Task Manager — REST API для управления задачами. FastAPI + SQLite.
Используется для обучения AI-assisted разработке.

## Code Style

[Правила кодирования для вашего стека]

Пример для Python:
- Следовать PEP 8
- Обязательные type hints для всех функций
- Docstrings в формате Google Style
- Максимальная длина строки: 100 символов

Пример для TypeScript:
- ESLint + Prettier
- Строгий режим TypeScript (strict: true)
- Functional components для React
- Явные типы для всех параметров функций

## Testing

[Требования к тестам]

Пример:
- Pytest для unit и integration тестов
- Минимальный coverage: 80%
- Обязательные тесты для каждого нового эндпоинта
- Fixtures в tests/conftest.py

## Workflow

[Процесс работы — что делать после изменений]

Пример:
1. После изменений запустить тесты: `pytest`
2. Проверить линтинг: `ruff check .`
3. Обновить документацию при изменении API
4. Использовать conventional commits: feat:, fix:, docs:, refactor:

## Commands

[Полезные команды проекта]

```bash
# Запуск dev сервера
uvicorn main:app --reload

# Запуск тестов
pytest -v

# Линтинг
ruff check . && mypy .

# Миграции БД
alembic upgrade head
```

## Architecture

- Общая архитектура: `docs/ARCHITECTURE.md`
- API спецификация: `docs/API.md`
- ADR (Architecture Decision Records): `docs/adr/`
```

**Сохраните этот файл в корне проекта.**

### Настройка разрешений (permissions)

Claude Code по умолчанию может использовать все инструменты. Для безопасности можно ограничить доступ:

```bash
# Редактировать ~/.claude/config.json
cat > ~/.claude/config.json << 'EOF'
{
  "model": "claude-sonnet-4-5-20250929",
  "maxTurns": 20,
  "blockedPaths": [".env", "secrets.json", "*.key", "credentials/"]
}
EOF
```

**Рекомендуемые настройки безопасности:**
- `blockedPaths`: файлы и директории, которые агент не должен читать или изменять
  - Обязательно добавьте: `.env`, файлы с секретами, приватные ключи
  - Пример: `[".env", "*.key", "*.pem", "secrets/", "credentials.json"]`

**Примечание:**
- Параметр `tools` НЕ поддерживается в Claude Code (все инструменты активны по умолчанию)
- Параметр `allowedCommands` может не поддерживаться в вашей версии
- Для максимальной безопасности используйте `blockedPaths`
