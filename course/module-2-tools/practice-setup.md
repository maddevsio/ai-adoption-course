# Установка рабочего окружения

> Пошаговая инструкция по установке Claude Code CLI — основного инструмента курса

## Системные требования

### Поддерживаемые ОС

**macOS** (рекомендуется):
- macOS 11+ (Big Sur или новее)
- M1/M2/M3 (ARM) или Intel
- 8GB+ RAM (16GB для комфортной работы)

**Linux** (полная поддержка):
- Ubuntu 20.04+, Debian 11+, Fedora, Arch
- 8GB+ RAM
- Bash 4.0+

**Windows** (через WSL2):
- Windows 10 версии 2004+ или Windows 11
- WSL2 установлен с Ubuntu 20.04+
- 16GB RAM рекомендуется

### Дополнительное ПО

- **Node.js**: 18.0+ (для MCP-серверов)
- **Python**: 3.8+ (опционально, для некоторых MCP-серверов)
- **Git**: 2.30+
- **Терминал**: любой современный терминал (Terminal.app, iTerm2, Alacritty, GNOME Terminal)

## Установка Claude Code CLI

### Вариант 1: macOS

**Через npm (рекомендуется):**

```bash
# Установка через npm
npm install -g claude-code

# Проверка версии
claude --version
# Ожидается: claude-code 2026.2.x
```

**Через Homebrew:**

```bash
# Установка через brew
brew install claude-code

# Проверка версии
claude --version
```

**Через официальный installer:**

1. Скачать installer: https://code.claude.com/download
2. Открыть `.dmg` файл
3. Перетащить `Claude Code` в `/Applications`
4. Проверить установку: `claude --version`

### Вариант 2: Linux

**Через npm (универсальный способ):**

```bash
# Установка Node.js (если не установлен)
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt-get install -y nodejs

# Установка Claude Code
npm install -g claude-code

# Проверка версии
claude --version
```

**Через пакетный менеджер (Ubuntu/Debian):**

```bash
# Добавить репозиторий
curl -fsSL https://code.claude.com/linux/gpg | sudo gpg --dearmor -o /usr/share/keyrings/claude-code.gpg
echo "deb [signed-by=/usr/share/keyrings/claude-code.gpg] https://code.claude.com/linux/deb stable main" | sudo tee /etc/apt/sources.list.d/claude-code.list

# Установка
sudo apt update
sudo apt install claude-code

# Проверка
claude --version
```

### Вариант 3: Windows (WSL2)

**Установка WSL2:**

```powershell
# PowerShell от администратора
wsl --install -d Ubuntu-22.04

# Перезагрузка компьютера
# После перезагрузки запустить Ubuntu из меню Пуск
```

**В терминале WSL2 Ubuntu:**

```bash
# Обновление системы
sudo apt update && sudo apt upgrade -y

# Установка Node.js
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt-get install -y nodejs

# Установка Claude Code
npm install -g claude-code

# Проверка
claude --version
```

## Настройка доступа к API

### Вариант A: OAuth токен (рекомендуется для новичков)

**Требования:**
- Активная подписка Claude Max ($100/мес)
- Браузер для аутентификации

**Шаги:**

```bash
# Запустить процесс настройки
claude setup-token

# Откроется браузер с OAuth flow
# 1. Войти в аккаунт claude.ai
# 2. Разрешить доступ для Claude Code
# 3. Токен автоматически сохранится в ~/.claude/auth.json
```

**Проверка:**

```bash
# Тестовый запрос
claude -p "What is 2+2?"

# Ожидается: ответ от модели
```

**Срок действия токена:** 1 год (автоматическое обновление при следующем запуске после истечения)

### Вариант B: API key (для продвинутых пользователей)

**Требования:**
- Аккаунт на console.anthropic.com
- Баланс API (pay-as-you-go) или корпоративный API key

**Получение API key:**

1. Открыть https://console.anthropic.com
2. Перейти в раздел "API Keys"
3. Нажать "Create Key"
4. Скопировать ключ (формат: `sk-ant-api03-...`)
5. Сохранить в безопасном месте (ключ показывается только один раз)

**Настройка:**

```bash
# Добавить в ~/.bashrc или ~/.zshrc
export ANTHROPIC_API_KEY="sk-ant-api03-ВАШИ_СИМВОЛЫ_КЛЮЧА"

# Применить изменения
source ~/.bashrc  # или source ~/.zshrc

# Проверка
echo $ANTHROPIC_API_KEY
# Должен показать ваш ключ
```

**Проверка работы:**

```bash
claude -p "Hello, Claude!"
```

### Выбор модели по умолчанию

```bash
# Создать конфигурацию
mkdir -p ~/.claude
cat > ~/.claude/config.json << 'EOF'
{
  "model": "sonnet-4.5",
  "maxTurns": 20,
  "tools": ["read", "write", "bash", "grep", "glob"]
}
EOF
```

**Доступные модели:**
- `opus-4.6` — умная модель для сложных задач ($5-21 за 1M токенов)
- `sonnet-4.5` — рабочая модель для 90% задач ($1.75-3 за 1M токенов) — **рекомендуется**
- `haiku-4.5` — быстрая модель для простых задач ($0.03-1 за 1M токенов)

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

[Ссылки на архитектурную документацию]

- Общая архитектура: `docs/ARCHITECTURE.md`
- API спецификация: `docs/API.md`
- ADR (Architecture Decision Records): `docs/adr/`
```

**Сохраните этот файл в корне проекта.**

### Настройка разрешений (permissions)

Claude Code по умолчанию может использовать все инструменты. Для безопасности можно ограничить их:

```bash
# Редактировать ~/.claude/config.json
cat > ~/.claude/config.json << 'EOF'
{
  "model": "sonnet-4.5",
  "maxTurns": 20,
  "tools": ["read", "write", "bash", "grep", "glob"],
  "allowedCommands": ["npm", "pytest", "git", "curl"],
  "blockedPaths": [".env", "secrets.json", "*.key"]
}
EOF
```

**Рекомендуемые настройки:**
- `tools`: разрешенные инструменты Claude (read, write, bash, grep, glob)
- `allowedCommands`: белый список bash-команд (для безопасности)
- `blockedPaths`: файлы, которые агент не должен читать или изменять

## Troubleshooting: Решение типовых проблем

### Проблема 1: `npm ERR! EACCES` при установке

**Симптомы:**
```
npm ERR! Error: EACCES: permission denied, access '/usr/local/lib/node_modules'
```

**Причина:** Недостаточно прав для глобальной установки npm пакетов.

**Решение A: Использовать nvm (рекомендуется):**

```bash
# Установка nvm
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash

# Перезапуск терминала или
source ~/.bashrc

# Установка Node.js через nvm
nvm install 20
nvm use 20

# Теперь можно устанавливать без sudo
npm install -g claude-code
```

**Решение B: Изменить директорию npm:**

```bash
# Создать директорию для глобальных пакетов
mkdir ~/.npm-global

# Настроить npm
npm config set prefix '~/.npm-global'

# Добавить в PATH (~/.bashrc или ~/.zshrc)
export PATH=~/.npm-global/bin:$PATH

# Применить изменения
source ~/.bashrc

# Установка без sudo
npm install -g claude-code
```

### Проблема 2: "Invalid API key" или "Unauthorized"

**Симптомы:**
```
Error: Invalid API key
Status: 401 Unauthorized
```

**Проверка 1: Формат ключа**

```bash
echo $ANTHROPIC_API_KEY
# Должен начинаться с sk-ant-api03-
# Длина примерно 100+ символов
```

**Проверка 2: Регион и план**

- API keys с console.anthropic.com — только для US регiona
- Для EU нужно использовать https://console.anthropic.eu
- Проверьте, что у вас есть активная подписка или положительный баланс

**Проверка 3: OAuth токен**

```bash
# Проверить наличие токена
ls -la ~/.claude/auth.json

# Если файла нет, запустить setup заново
claude setup-token
```

**Решение:**

```bash
# Удалить старый токен
rm ~/.claude/auth.json

# Переполучить OAuth токен
claude setup-token

# Или обновить API key
export ANTHROPIC_API_KEY="ваш_новый_ключ"
```

### Проблема 3: `claude: command not found`

**Симптомы:**
```bash
claude --version
# bash: claude: command not found
```

**Причина:** Исполняемый файл claude не в PATH.

**Решение для npm установки:**

```bash
# Найти где установлен claude
npm root -g
# Пример вывода: /usr/local/lib/node_modules

# Проверить бинарники
ls -la $(npm root -g)/../bin/claude

# Добавить в PATH (если нужно)
export PATH="$(npm root -g)/../bin:$PATH"

# Добавить в ~/.bashrc для постоянного эффекта
echo 'export PATH="$(npm root -g)/../bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

**Решение для Homebrew:**

```bash
# Проверить установку
brew list claude-code

# Переустановить если нужно
brew reinstall claude-code

# Проверить PATH
echo $PATH | grep homebrew
```

**Универсальное решение: перезапуск терминала**

Часто после установки нужно просто перезапустить терминал для обновления PATH.

### Проблема 4: Таймаут или "Connection refused"

**Симптомы:**
```
Error: connect ETIMEDOUT
Error: Connection refused
```

**Причина:** Проблемы сетевого подключения (VPN, firewall, proxy).

**Решение A: Проверить сетевое подключение**

```bash
# Проверить доступность API Anthropic
curl -I https://api.anthropic.com/v1/messages
# Ожидается: HTTP/1.1 или HTTP/2 ответ

# Если не отвечает, проблема в сети
```

**Решение B: Настроить proxy**

```bash
# Если вы за корпоративным proxy
export HTTP_PROXY=http://proxy.company.com:8080
export HTTPS_PROXY=http://proxy.company.com:8080

# Добавить в ~/.bashrc
echo 'export HTTP_PROXY=http://proxy.company.com:8080' >> ~/.bashrc
echo 'export HTTPS_PROXY=http://proxy.company.com:8080' >> ~/.bashrc
```

**Решение C: VPN**

Если Anthropic API заблокирован в вашем регионе, используйте VPN:
- Подключиться к VPN с сервером в US или EU
- Проверить: `curl https://api.anthropic.com`

**Решение D: Firewall**

```bash
# Проверить firewall (Linux)
sudo ufw status

# Разрешить исходящие HTTPS
sudo ufw allow out 443/tcp
```

### Проблема 5: "Permission denied" при чтении файлов

**Симптомы:**
```
Error: EACCES: permission denied, open '/path/to/file'
```

**Причина:** Агент не имеет прав доступа к файлам проекта.

**Решение A: Запускать из корня проекта**

```bash
# НЕПРАВИЛЬНО: запускать из ~
cd ~
claude -p "Analyze project at ~/projects/my-app"

# ПРАВИЛЬНО: запускать из корня проекта
cd ~/projects/my-app
claude -p "Analyze this project"
```

**Решение B: Проверить права файлов**

```bash
# Проверить права
ls -la

# Если файлы принадлежат другому пользователю
sudo chown -R $USER:$USER .

# Если недостаточно прав на чтение
chmod -R u+r .
```

**Решение C: Настроить blockedPaths в конфигурации**

```json
{
  "blockedPaths": [".env", "secrets/"]
}
```

Убедитесь, что нужные файлы НЕ в списке заблокированных.

## Чеклист готовности

Перед началом основного курса убедитесь, что:

### ✅ Установка и доступ

- [ ] Claude Code установлен: `claude --version` показывает версию 2026.2+
- [ ] OAuth токен настроен ИЛИ `ANTHROPIC_API_KEY` установлен
- [ ] Тестовый запрос работает: `claude -p "Hello"`
- [ ] Подписка активна (Claude Max) или есть баланс API

### ✅ Проект для практики

- [ ] Есть рабочий проект (свой или созданная песочница task-manager)
- [ ] Проект под git: `git status` работает
- [ ] Проект запускается локально
- [ ] Тесты проходят (если есть)

### ✅ Базовая конфигурация

- [ ] Файл `~/.claude/config.json` создан с моделью по умолчанию
- [ ] Файл `CLAUDE.md` создан в корне проекта
- [ ] Permissions настроены (опционально, для безопасности)

### ✅ Первый успешный тест

- [ ] Агент проанализировал структуру проекта
- [ ] Создан файл `ARCHITECTURE.md` с описанием проекта
- [ ] Агент корректно определил технологический стек
- [ ] Вы понимаете, как агент читает и анализирует файлы

### ✅ Понимание основ

- [ ] Знаю, как запустить Claude Code: `claude` (интерактивный) или `claude -p "..."` (one-shot)
- [ ] Знаю, как выбрать модель: `--model opus-4.6` или в config.json
- [ ] Понимаю разницу между OAuth токеном и API key
- [ ] Знаю, где искать помощь: `claude --help` и https://code.claude.com/docs

## Дополнительные инструменты (опционально)

### GitHub Copilot

GitHub Copilot дополняет Claude Code для inline автодополнения кода прямо в редакторе.

**Установка:**

1. Оформить подписку GitHub Copilot Pro ($10/мес): https://github.com/features/copilot
2. Установить расширение для вашей IDE:
   - **VS Code**: Extensions → "GitHub Copilot"
   - **JetBrains** (PyCharm, IntelliJ): Plugins → "GitHub Copilot"
   - **Neovim**: https://github.com/github/copilot.vim

**Когда использовать:**
- Claude Code — для сложных задач (рефакторинг, архитектура, debugging)
- GitHub Copilot — для быстрых правок и автодополнения внутри IDE

### Cursor (альтернативная IDE)

Cursor — форк VS Code со встроенным AI-агентом.

**Установка:**

1. Скачать: https://cursor.sh/
2. Оформить Cursor Pro ($20/мес)
3. Импортировать настройки из VS Code (опционально)

**Особенности:**
- Agent Mode (Ctrl+K) — похож на Claude Code
- YOLO mode — автоматическое применение изменений
- Встроенный терминал с AI

**Когда использовать:**
- Если предпочитаете визуальную IDE вместо CLI
- Для фронтенд-разработки с live preview

## Связь с практическими модулями

### Модуль 3: Промптинг и итерации

**Вы будете использовать песочницу task-manager:**
- Добавлять валидацию входных данных (урок 3.2)
- Реализовывать PUT и DELETE эндпоинты (урок 3.3)
- Писать промпты для генерации тестов (урок 3.4)

**Критичная зависимость:** Функциональная песочница с работающими GET/POST эндпоинтами.

### Модуль 4: Агентские паттерны

**Вы будете использовать свой проект или песочницу:**
- Создавать файл `AGENTS.md` (урок 4.1)
- Настраивать циклы планирования-реализации (урок 4.2)
- Интегрировать pre-commit hooks (урок 4.3)

**Критичная зависимость:** Проект под git с историей коммитов.

### Модуль 5: Specification-Driven Development

**Вы будете работать с реальными спецификациями:**
- Генерировать код из спецификаций API (урок 5.2)
- Создавать тесты на основе контрактов (урок 5.3)

**Критичная зависимость:** Понимание структуры вашего проекта (файл ARCHITECTURE.md).

### Модуль 6: MCP и интеграции

**Вам понадобятся:**
- Git история проекта (для Git MCP)
- Аккаунт Jira или GitHub Issues (для Jira/GitHub MCP)
- JetBrains IDE установлен (для JetBrains MCP)
- Figma designs (опционально, для Figma MCP)

**Критичная зависимость:** Рабочий проект с реальными задачами в issue tracker.

### Модуль 7: Оркестрация агентов

**Вы будете настраивать:**
- Headless режим для автоматизации
- Параллельные агенты для разных частей проекта
- CI/CD интеграцию с GitHub Actions

**Критичная зависимость:** Проект с тестами и линтингом.

## Практические советы

### Оптимизация затрат

**Выбирайте модель под задачу:**

```bash
# Простые задачи — Haiku (дешево)
claude -p "Add comments to this function" --model haiku-4.5

# Обычные задачи — Sonnet (по умолчанию)
claude -p "Implement user registration"

# Сложные задачи — Opus (умная модель)
claude -p "Design microservices architecture" --model opus-4.6
```

**Используйте prompt caching:**

Claude Code автоматически кеширует контекст проекта. Повторные запросы в той же сессии экономят 90% токенов.

```bash
# Первый запрос: читает весь проект (дорого)
claude -p "Analyze project structure"

# Последующие запросы: используют кеш (дешево)
claude -p "Add logging to API endpoints"
claude -p "Write tests for user model"
```

### Работа с большими проектами

**Ограничивайте контекст:**

```bash
# Вместо анализа всего проекта
claude -p "Refactor entire codebase"  # Дорого и медленно

# Фокусируйтесь на конкретных файлах
claude -p "Refactor src/api/users.py and its tests"  # Дешево и быстро
```

**Используйте .claudeignore:**

```bash
# Создать .claudeignore в корне проекта
cat > .claudeignore << 'EOF'
node_modules/
.git/
*.log
dist/
build/
coverage/
.env
EOF
```

Агент будет игнорировать эти файлы при чтении контекста проекта.

### Итеративная разработка

**Не пытайтесь сделать всё за один промпт:**

```bash
# НЕЭФФЕКТИВНО: огромный промпт
claude -p "Создай полноценный User Management со всеми CRUD операциями,
валидацией, тестами, документацией, миграциями БД и API эндпоинтами"

# ЭФФЕКТИВНО: итеративный подход
claude -p "Создай SQLAlchemy модель User с полями id, email, name"
# Проверяем результат, затем:
claude -p "Добавь CRUD операции для User в src/db/users.py"
# Проверяем результат, затем:
claude -p "Создай тесты для CRUD операций User"
# И так далее
```

**Преимущества итеративного подхода:**
- Контроль на каждом шаге
- Легче найти и исправить ошибки
- Дешевле (меньше токенов на запрос)
- Быстрее получить первый результат

### Проверка перед коммитом

**Всегда проверяйте изменения агента:**

```bash
# После того, как агент внес изменения
git diff

# Проверить тесты
pytest

# Проверить линтинг
ruff check .

# Если всё ок, коммитить
git add .
git commit -m "feat: add user authentication"
```

**Не коммитьте вслепую!** Агент может допустить ошибку.

## Следующие шаги

После прохождения этого setup guide:

1. **Модуль 1: Почему AI-assisted разработка**
   - Понимание ROI и метрик продуктивности
   - Когда AI помогает, а когда мешает

2. **Модуль 2: Выбор инструментов**
   - Сравнение Claude Code, Cursor, Copilot
   - Мульти-модельная стратегия

3. **Модуль 3: Промптинг**
   - Как писать эффективные промпты
   - Итеративная разработка
   - Debugging и code review с AI

4. **Модуль 4: Агентские паттерны**
   - Циклы планирования-реализации
   - Файл AGENTS.md для проекта

5. **Модуль 5: Specification-Driven Development**
   - Генерация кода из спецификаций
   - Contract testing

6. **Модуль 6: MCP интеграции**
   - Git, Jira, JetBrains, Figma MCP-серверы
   - Enterprise workflows

7. **Модуль 7: Оркестрация**
   - Headless режим и автоматизация
   - Multi-agent workflows
   - CI/CD интеграция

## Полезные ссылки

### Официальная документация
- Claude Code: https://code.claude.com
- Documentation: https://code.claude.com/docs
- Anthropic API: https://docs.anthropic.com

### Сообщество
- Discord: https://discord.gg/claude-code
- GitHub Discussions: https://github.com/anthropics/claude-code/discussions
- Reddit: r/ClaudeAI

### Дополнительные ресурсы
- GitHub Copilot: https://github.com/features/copilot
- Model Context Protocol: https://modelcontextprotocol.io
- Cursor IDE: https://cursor.sh

---

**Время выполнения setup:** 30-40 минут

**Готовы начать?** Переходите к Модулю 1: Почему AI-assisted разработка.
