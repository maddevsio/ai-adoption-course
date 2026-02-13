# Практика: Установка и использование MCP-серверов

> Практические упражнения по установке, настройке и использованию MCP-серверов для расширения возможностей AI-агентов

**Время выполнения:** 55 минут (20 мин установка + 10 мин конфигурация + 15 мин комплексная задача + 10 мин каталог)

**Цель:** Установить 4 обязательных MCP-сервера, настроить их для работы с Claude Code, и выполнить практическую задачу, демонстрирующую ценность MCP в реальной разработке.

---

## Предварительные требования

### Проверьте установку базового окружения

Вы должны были пройти **Модуль 2: Практика — Установка окружения** (файл `course/module-2-tools/practice-setup.md`).

```bash
# Проверка Claude Code
claude --version
# Ожидается: claude-code 2026.2+

# Проверка Node.js (для MCP-серверов)
node --version
# Ожидается: v18.0.0 или выше

# Проверка npm
npm --version
# Ожидается: 8.0+ или выше
```

### Рабочий проект или песочница

Вам понадобится проект с Git-историей:

- **Если есть свой проект**: используйте его
- **Если нет**: используйте песочницу `task-manager` из Модуля 2

```bash
# Проверка проекта
cd ~/practice/task-manager  # или путь к вашему проекту
git status
# Должен показать git репозиторий

# Проверка что есть хотя бы 1 коммит
git log
# Должен показать историю коммитов
```

---

## Шаг 1: Установка обязательных MCP-серверов (20 мин)

### 1.1. Git MCP Server

**Назначение:** Глубокий анализ Git-истории — code archaeology, поиск в истории, анализ конфликтов.

**Установка:**

```bash
# Установка Git MCP Server
npm install -g @modelcontextprotocol/server-git

# Проверка установки
npx @modelcontextprotocol/server-git --version
# Должна показаться версия (например, 0.5.0)
```

**Что дает Git MCP:**
- `git log --grep` — поиск коммитов по тексту
- `git log -S` — поиск коммитов по содержимому (code search)
- `git blame` — построчный анализ авторства
- `git diff` — детальное сравнение веток и коммитов
- Анализ contribution patterns

**Проверка работы:**

```bash
# Перейти в ваш проект
cd ~/practice/task-manager

# Запустить Git MCP сервер вручную (для теста)
npx @modelcontextprotocol/server-git

# Нажмите Ctrl+C для остановки
# Если сервер запустился без ошибок — всё работает
```

---

### 1.2. Jira MCP Server (или альтернатива)

**Назначение:** Интеграция с task tracker — чтение задач, worklogs, обновление статусов.

#### Вариант A: Jira (если у вас есть доступ)

**Требования:**
- Jira Cloud аккаунт (например, `your-company.atlassian.net`)
- Email для входа
- API Token

**Получение API Token:**

1. Перейти: https://id.atlassian.com/manage-profile/security/api-tokens
2. Нажать "Create API token"
3. Название токена: "Claude Code MCP"
4. Скопировать токен (показывается один раз!)

**Установка:**

```bash
# Установка Jira MCP Server
npm install -g @atlassian/atlassian-mcp-server

# Проверка установки
npx @atlassian/atlassian-mcp-server --version
```

**Environment variables:**

```bash
# Добавить в ~/.bashrc или ~/.zshrc
export ATLASSIAN_SITE="your-company.atlassian.net"
export ATLASSIAN_EMAIL="your-email@example.com"
export ATLASSIAN_API_TOKEN="ваш_токен_здесь"

# Применить изменения
source ~/.bashrc  # или source ~/.zshrc

# Проверка
echo $ATLASSIAN_SITE
# Должен показать ваш сайт
```

#### Вариант B: GitHub Issues (альтернатива для тех, у кого нет Jira)

**Почему GitHub Issues:**
- Бесплатно
- У всех разработчиков есть GitHub
- Функциональности достаточно для практики курса

**Получение GitHub Token:**

1. Перейти: https://github.com/settings/tokens
2. Generate new token (classic)
3. Scopes: `repo` (полный доступ к репозиториям)
4. Скопировать токен

**Установка:**

```bash
# Установка GitHub MCP Server
npm install -g @modelcontextprotocol/server-github

# Environment variables
export GITHUB_TOKEN="ваш_github_токен"
export GITHUB_REPO="username/repository"  # например, "john/task-manager"

# Применить
source ~/.bashrc
```

**Проверка работы (GitHub Issues):**

```bash
# Создать тестовую задачу в вашем репозитории
# Перейти в браузере: https://github.com/username/repository/issues/new
# Создать issue: "Test issue for MCP practice"

# Проверить что GitHub MCP видит issues
# Это будем проверять позже через Claude Code
```

#### Вариант C: Todoist MCP (минимальная альтернатива)

Если нет ни Jira, ни GitHub Issues с задачами:

```bash
# Установка Todoist MCP
npm install -g @ivo-/todoist-mcp-server

# Получить API токен: https://app.todoist.com/app/settings/integrations/developer
export TODOIST_API_TOKEN="ваш_todoist_токен"

# Применить
source ~/.bashrc
```

---

### 1.3. JetBrains MCP Server (PyCharm / IntelliJ / WebStorm)

**Назначение:** Интеграция с IDE — debugger, refactoring, code analysis, navigation.

**Требования:**
- JetBrains IDE версии 2024.3+ (PyCharm, IntelliJ IDEA, WebStorm, GoLand, Rider)
- Установленный JetBrains AI Assistant plugin

#### Если у вас НЕТ JetBrains IDE

**Альтернатива: VS Code с базовыми инструментами**

Для целей курса можно пропустить JetBrains MCP и использовать стандартные возможности Claude Code (чтение файлов, терминал). Это не критично, но JetBrains MCP значительно упрощает debugging.

**Если хотите попробовать JetBrains IDE:**
- PyCharm Community Edition (бесплатно): https://www.jetbrains.com/pycharm/download/
- IntelliJ IDEA Community Edition (бесплатно): https://www.jetbrains.com/idea/download/

```bash
# macOS (через Homebrew)
brew install --cask pycharm-ce

# Linux (через snap)
sudo snap install pycharm-community --classic
```

#### Установка MCP в JetBrains IDE

1. **Открыть IDE** (PyCharm / IntelliJ / WebStorm)

2. **Включить MCP Server:**
   - Settings (Cmd+, на macOS или Ctrl+Alt+S на Linux/Windows)
   - Tools → Model Context Protocol
   - Enable MCP Server: ✅
   - Port: `8765` (по умолчанию)
   - Apply → OK

3. **Проверка:**
   - В статус-баре IDE должна появиться иконка MCP (зелёная, если активен)
   - Или: View → Tool Windows → MCP Server Status

**Важно:** JetBrains MCP работает только когда IDE запущена. Перед использованием убедитесь, что IDE открыта с вашим проектом.

---

### 1.4. Figma MCP Server

**Назначение:** Design-to-code workflow — AI читает структуру дизайна и генерирует код с точными стилями.

**Требования:**
- Figma аккаунт (бесплатный plan подойдёт)
- Personal Access Token

#### Получение Figma Token

1. Перейти: https://www.figma.com/
2. Войти в аккаунт
3. Settings → Account → Personal Access Tokens
4. Generate new token
5. Название: "Claude Code MCP"
6. Скопировать токен

**Установка:**

```bash
# Установка Figma MCP Server
npm install -g @glips/figma-context-mcp

# Проверка установки
npx @glips/figma-context-mcp --version
```

**Environment variables:**

```bash
# Добавить в ~/.bashrc или ~/.zshrc
export FIGMA_ACCESS_TOKEN="ваш_figma_токен_здесь"

# Применить
source ~/.bashrc

# Проверка
echo $FIGMA_ACCESS_TOKEN
# Должен показать токен
```

#### Подготовка демо Figma файла

Если у вас нет готовых дизайнов:

1. Перейти: https://www.figma.com/community
2. Найти "UI Kit" или "Design System"
3. Дублировать любой понравившийся файл (Duplicate)
4. Скопировать URL файла (например: `https://www.figma.com/file/ABC123/My-Design`)
5. Запомнить File ID (`ABC123` в примере)

**Альтернатива без Figma:**

Можно пропустить Figma MCP, если не работаете с дизайном. Это не критично для backend-разработки.

---

## Шаг 2: Настройка конфигурации (10 мин)

### 2.1. Конфигурация для Claude Code

Создайте файл `~/.claude/mcp.json` (или отредактируйте существующий):

```bash
# Создать директорию если её нет
mkdir -p ~/.claude

# Создать конфигурацию MCP
cat > ~/.claude/mcp.json << 'EOF'
{
  "mcpServers": {
    "git": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-git"],
      "cwd": "."
    },
    "jira": {
      "command": "npx",
      "args": ["-y", "@atlassian/atlassian-mcp-server"],
      "env": {
        "ATLASSIAN_SITE": "${ATLASSIAN_SITE}",
        "ATLASSIAN_EMAIL": "${ATLASSIAN_EMAIL}",
        "ATLASSIAN_API_TOKEN": "${ATLASSIAN_API_TOKEN}"
      }
    },
    "figma": {
      "command": "npx",
      "args": ["-y", "@glips/figma-context-mcp"],
      "env": {
        "FIGMA_ACCESS_TOKEN": "${FIGMA_ACCESS_TOKEN}"
      }
    }
  }
}
EOF
```

**Если используете GitHub Issues вместо Jira:**

```json
{
  "mcpServers": {
    "git": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-git"],
      "cwd": "."
    },
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_TOKEN": "${GITHUB_TOKEN}"
      }
    },
    "figma": {
      "command": "npx",
      "args": ["-y", "@glips/figma-context-mcp"],
      "env": {
        "FIGMA_ACCESS_TOKEN": "${FIGMA_ACCESS_TOKEN}"
      }
    }
  }
}
```

**Примечание:** `${VAR_NAME}` автоматически заменяется на значение переменной окружения.

### 2.2. Конфигурация для Cursor (опционально)

Если вы используете Cursor IDE вместо Claude Code CLI:

```bash
# Создать конфигурацию для Cursor
mkdir -p ~/.cursor
cat > ~/.cursor/mcp.json << 'EOF'
{
  "mcpServers": {
    "git": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-git"]
    },
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_TOKEN": "your_token_here"
      }
    }
  }
}
EOF
```

**Важно:** В Cursor замените `"your_token_here"` на реальный токен (не используйте `${VAR_NAME}` — не поддерживается).

### 2.3. Проверка конфигурации

```bash
# Проверить что файл создан
cat ~/.claude/mcp.json

# Проверить JSON валидность
python3 -m json.tool ~/.claude/mcp.json
# Или:
node -e "JSON.parse(require('fs').readFileSync('$HOME/.claude/mcp.json', 'utf8'))"

# Если ошибок нет — конфигурация валидна
```

### 2.4. Проверка видимости серверов

```bash
# Запустить Claude Code с запросом о MCP
cd ~/practice/task-manager
claude -p "List all available MCP tools"
```

**Ожидаемый результат:**

Агент должен показать список инструментов от MCP-серверов:

```
Available MCP tools:
- git_log (from Git MCP): Show git history with filters
- git_blame (from Git MCP): Show line-by-line authorship
- git_search (from Git MCP): Search through git history
- jira_search (from Jira MCP): Search Jira issues
- jira_read (from Jira MCP): Read issue details
- figma_read (from Figma MCP): Read Figma file structure
...
```

**Если агент НЕ видит MCP-серверы:**
- Проверьте, что переменные окружения установлены: `echo $ATLASSIAN_SITE`
- Проверьте логи: `tail -f ~/.claude/logs/mcp.log` (если файл существует)
- См. секцию "Troubleshooting" внизу этого файла

---

## Шаг 3: Комплексная задача с MCP (15 мин)

Эта задача демонстрирует реальную ценность MCP: агент использует **несколько серверов** для решения одной задачи.

### Задача A: Code Archaeology + Task Planning (с Jira/GitHub)

**Сценарий:**
Вы работаете над задачей из вашего issue tracker. Нужно:
1. Прочитать задачу из Jira/GitHub
2. Проанализировать связанные файлы через Git MCP
3. Предложить план реализации

**Подготовка:**

```bash
# Перейти в ваш проект
cd ~/practice/task-manager

# Создать задачу в GitHub Issues (если используете GitHub)
# Браузер: https://github.com/username/task-manager/issues/new
# Название: "Add input validation for POST /tasks"
# Описание:
# ```
# Currently POST /tasks accepts any input without validation.
# Need to add:
# - title is required (string, max 200 chars)
# - created_at should be auto-generated
# ```

# Или создать задачу в Jira:
# Браузер: https://your-company.atlassian.net/jira/software/projects/PROJ/boards/1
# Создать issue "PROJ-123: Add validation for POST /tasks"
```

**Запуск Claude Code:**

```bash
claude
```

**Промпт для агента:**

```
Я работаю над задачей [PROJ-123] (или #1 для GitHub) "Add input validation for POST /tasks".

Шаги:
1. Прочитай задачу из Jira/GitHub Issues
2. Используй Git MCP для анализа:
   - Найди все коммиты, которые изменяли файлы, связанные с POST /tasks
   - Посмотри как реализованы другие эндпоинты в проекте
3. Проанализируй текущую реализацию POST /tasks
4. Предложи план реализации валидации:
   - Какие изменения нужны в коде
   - Какие тесты нужно добавить
   - Какие библиотеки использовать (если нужны)

Не реализуй пока, только план.
```

**Ожидаемый результат:**

Агент должен:
1. Прочитать задачу через Jira/GitHub MCP
2. Выполнить `git log` через Git MCP для поиска связанных коммитов
3. Проанализировать текущий код
4. Предложить детальный план с конкретными шагами

**Пример вывода:**

```
## Анализ задачи PROJ-123

### Контекст из Jira:
Задача требует добавить валидацию для POST /tasks:
- title обязательно, строка, макс 200 символов
- created_at автогенерируемое

### Анализ Git истории:
Коммиты связанные с POST /tasks:
- abc123 (2026-01-15) "feat: add POST /tasks endpoint" — первая реализация
- def456 (2026-01-20) "fix: handle empty requests" — добавлена базовая проверка

### Текущая реализация:
Файл: src/routes/tasks.py
Проблемы:
- Нет валидации title
- created_at принимается от клиента (должно генерироваться)

### План реализации:

1. Добавить Pydantic модель для валидации:
   - TaskCreate с полем title: str (max_length=200)
   - created_at исключить из модели

2. Изменить эндпоинт POST /tasks:
   - Использовать TaskCreate для валидации
   - Автоматически добавлять created_at при сохранении

3. Тесты:
   - Тест валидации: title > 200 символов → 422 ошибка
   - Тест валидации: пустой title → 422 ошибка
   - Тест автогенерации: created_at не передается → генерируется сервером

4. Библиотеки: Pydantic (уже в зависимостях FastAPI)

Оценка: 30 минут работы
```

**Время выполнения задачи:** 5-10 минут

---

### Задача B: Design-to-Code (с Figma MCP)

**Сценарий:**
У вас есть дизайн компонента в Figma. Нужно сгенерировать код с точными стилями из design tokens.

**Подготовка (если нет своего дизайна):**

1. Откройте Figma Community: https://www.figma.com/community
2. Найдите "Button Component" или любой простой UI Kit
3. Дублируйте файл (Duplicate)
4. Скопируйте File ID из URL (например: `https://www.figma.com/file/ABC123/...` → `ABC123`)

**Промпт для агента:**

```bash
claude
```

```
Подключись к Figma файлу с ID [ABC123] (замените на ваш File ID).

Найди компонент "Button" (или любой простой компонент из вашего файла).

Сгенерируй React компонент с точными стилями:
- Используй inline styles или Tailwind (что удобнее)
- Извлеки точные значения: padding, font-size, colors, border-radius
- Сохрани компонент в src/components/Button.jsx

Покажи:
1. Структуру слоёв из Figma
2. Извлечённые design tokens (colors, spacing, typography)
3. Финальный код компонента
```

**Ожидаемый результат:**

Агент через Figma MCP:
1. Прочитает структуру Figma файла
2. Извлечёт свойства компонента (размеры, цвета, шрифты)
3. Сгенерирует React компонент с **точными** значениями из Figma

**Пример вывода:**

```jsx
// src/components/Button.jsx

// Извлечённые design tokens из Figma:
// - Background: #2C2C2C
// - Text color: #FFFFFF
// - Padding: 12px 24px
// - Border radius: 8px
// - Font size: 16px
// - Font weight: 600

export const Button = ({ children, onClick }) => (
  <button
    onClick={onClick}
    style={{
      backgroundColor: '#2C2C2C',
      color: '#FFFFFF',
      padding: '12px 24px',
      borderRadius: '8px',
      fontSize: '16px',
      fontWeight: 600,
      border: 'none',
      cursor: 'pointer'
    }}
  >
    {children}
  </button>
);
```

**Преимущество MCP:** Без Figma MCP вы бы смотрели на screenshot и вручную переносили значения (с неизбежными ошибками: 10px вместо 12px, #333 вместо #2C2C2C). С MCP — 100% точность.

**Время выполнения задачи:** 5 минут

---

## Шаг 4: Расширенный каталог MCP-серверов (10 мин)

Помимо обязательных 4 серверов, существуют сотни других. В этом шаге вы изучите каталог и установите 1 сервер по выбору.

### 4.1. Обзор полезных MCP-серверов

#### PostgreSQL MCP Server

**Use case:** Работа с PostgreSQL через natural language запросы.

**Когда использовать:**
- Нужно выполнить SQL-запрос, но не помните синтаксис
- Хотите проанализировать схему БД
- Генерируете миграции на основе описания

**Установка:**

```bash
npm install -g @modelcontextprotocol/server-postgres
```

**Конфигурация (~/.claude/mcp.json):**

```json
{
  "mcpServers": {
    "postgres": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres"],
      "env": {
        "POSTGRES_CONNECTION_STRING": "postgresql://user:password@localhost:5432/database"
      }
    }
  }
}
```

**Пример использования:**

```bash
claude -p "Покажи все таблицы в БД и количество записей в каждой"
claude -p "Найди всех пользователей, зарегистрированных за последнюю неделю"
claude -p "Создай SQL-миграцию для добавления поля email_verified в таблицу users"
```

**Ссылка:** https://github.com/modelcontextprotocol/servers/tree/main/src/postgres

---

#### Puppeteer MCP Server

**Use case:** Web automation — заполнение форм, screenshots, E2E тестирование.

**Когда использовать:**
- Нужно автоматизировать действия в браузере
- Делаете screenshots для документации
- Пишете E2E тесты

**Установка:**

```bash
npm install -g @modelcontextprotocol/server-puppeteer
```

**Конфигурация:**

```json
{
  "mcpServers": {
    "puppeteer": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-puppeteer"]
    }
  }
}
```

**Пример использования:**

```bash
claude -p "Открой https://example.com, заполни форму логина (user: test@example.com, password: test123), и сделай screenshot дашборда"
claude -p "Создай E2E тест для регистрации пользователя на staging.myapp.com"
```

**Ссылка:** https://github.com/modelcontextprotocol/servers/tree/main/src/puppeteer

---

#### Mermaid MCP Server

**Use case:** Генерация диаграмм (flowcharts, sequence, ER diagrams) из кода.

**Когда использовать:**
- Создаёте архитектурную документацию
- Визуализируете workflows
- Документируете процессы

**Установка:**

```bash
npm install -g mermaid-mcp-server
```

**Конфигурация:**

```json
{
  "mcpServers": {
    "mermaid": {
      "command": "npx",
      "args": ["-y", "mermaid-mcp-server"]
    }
  }
}
```

**Пример использования:**

```bash
claude -p "Создай sequence diagram для OAuth2 authentication flow и сохрани как docs/oauth-flow.png"
claude -p "Проанализируй код в src/ и создай architecture diagram с основными модулями"
```

**Ссылка:** https://github.com/mermaid-js/mermaid-mcp-server

---

#### Miro MCP Server

**Use case:** Создание whiteboard диаграмм на Miro boards.

**Когда использовать:**
- Коллаборативное планирование с командой
- Визуализация идей на доске
- Создание mind maps

**Установка:**

```bash
npm install -g @k-jarzyna/mcp-miro
```

**Требования:**
- Miro аккаунт
- API Token: https://miro.com/app/settings/user-profile/apps

**Конфигурация:**

```json
{
  "mcpServers": {
    "miro": {
      "command": "npx",
      "args": ["-y", "@k-jarzyna/mcp-miro"],
      "env": {
        "MIRO_ACCESS_TOKEN": "your_miro_token"
      }
    }
  }
}
```

**Пример использования:**

```bash
claude -p "Создай Miro board с архитектурой микросервисов для нашего проекта"
```

**Ссылка:** https://github.com/k-jarzyna/mcp-miro

---

#### Obsidian MCP Server

**Use case:** Работа с Obsidian vault — заметки, knowledge graph, links.

**Когда использовать:**
- Ведёте knowledge base в Obsidian
- Нужно найти связанные заметки
- Создаёте документацию из кода

**Установка:**

```bash
npm install -g mcp-obsidian
```

**Требования:**
- Obsidian установлен
- Vault path (путь к папке с заметками)

**Конфигурация:**

```json
{
  "mcpServers": {
    "obsidian": {
      "command": "npx",
      "args": ["-y", "mcp-obsidian"],
      "env": {
        "OBSIDIAN_VAULT_PATH": "/Users/username/Documents/MyVault"
      }
    }
  }
}
```

**Пример использования:**

```bash
claude -p "Найди все заметки в Obsidian, связанные с 'authentication', и создай summary"
claude -p "Создай заметку в Obsidian с ADR для выбора PostgreSQL вместо MySQL"
```

**Ссылка:** https://github.com/your-obsidian-mcp

---

#### PowerPoint MCP Server

**Use case:** Создание презентаций из текста.

**Когда использовать:**
- Нужно быстро создать презентацию
- Генерируете slides из документации

**Установка:**

```bash
npm install -g office-powerpoint-mcp-server
```

**Конфигурация:**

```json
{
  "mcpServers": {
    "powerpoint": {
      "command": "npx",
      "args": ["-y", "office-powerpoint-mcp-server"]
    }
  }
}
```

**Пример использования:**

```bash
claude -p "Создай PowerPoint презентацию на тему 'MCP Architecture' с 5 слайдами: intro, architecture, examples, installation, conclusion"
```

**Ссылка:** https://github.com/microsoft/office-powerpoint-mcp

---

#### BrowserStack MCP Server

**Use case:** Кросс-браузерное тестирование.

**Когда использовать:**
- Нужно протестировать сайт в разных браузерах
- Проверяете responsive design

**Установка:**

```bash
npm install -g browserstack-mcp-server
```

**Требования:**
- BrowserStack аккаунт
- API credentials

**Конфигурация:**

```json
{
  "mcpServers": {
    "browserstack": {
      "command": "npx",
      "args": ["-y", "browserstack-mcp-server"],
      "env": {
        "BROWSERSTACK_USERNAME": "your_username",
        "BROWSERSTACK_ACCESS_KEY": "your_access_key"
      }
    }
  }
}
```

**Пример использования:**

```bash
claude -p "Протестируй https://myapp.com на Safari iOS 17, Chrome Android, и покажи screenshots"
```

**Ссылка:** https://github.com/browserstack/mcp-server

---

### 4.2. Практическое задание: Установка одного сервера

Выберите **один** MCP-сервер из списка выше, который подходит под ваш проект:

**Для backend-разработки:**
- PostgreSQL MCP (работа с БД)

**Для frontend-разработки:**
- Puppeteer MCP (E2E тесты)
- BrowserStack MCP (кросс-браузерность)

**Для документации:**
- Mermaid MCP (диаграммы)
- Obsidian MCP (knowledge base)
- PowerPoint MCP (презентации)

**Для визуализации:**
- Miro MCP (collaborative boards)

**Шаги:**

1. Установите выбранный сервер
2. Добавьте конфигурацию в `~/.claude/mcp.json`
3. Перезапустите Claude Code
4. Проверьте работу с простым запросом

**Пример для PostgreSQL MCP:**

```bash
# Установка
npm install -g @modelcontextprotocol/server-postgres

# Добавление в конфигурацию
# (Отредактируйте ~/.claude/mcp.json, добавьте секцию "postgres")

# Проверка
claude -p "List all tables in the database"
```

**Время выполнения:** 10 минут

---

## Troubleshooting: Решение типовых проблем

### Проблема 1: MCP-сервер не подключается

**Симптомы:**

```
Error: Failed to connect to MCP server 'git'
Connection timeout after 30s
```

**Решения:**

**Шаг 1: Проверить что сервер установлен**

```bash
# Для Git MCP
npx @modelcontextprotocol/server-git --version

# Для Jira MCP
npx @atlassian/atlassian-mcp-server --version

# Если выдаёт ошибку "command not found" — переустановить
npm install -g @modelcontextprotocol/server-git
```

**Шаг 2: Проверить Node.js версию**

```bash
node --version
# Должно быть v18.0.0 или выше

# Если версия старая:
nvm install 20
nvm use 20
```

**Шаг 3: Запустить сервер вручную для диагностики**

```bash
# Попробовать запустить Git MCP вручную
cd ~/practice/task-manager
npx @modelcontextprotocol/server-git

# Смотрите на ошибки в выводе
# Ctrl+C для остановки
```

**Шаг 4: Проверить логи Claude Code**

```bash
# Если файл логов существует
tail -f ~/.claude/logs/mcp.log

# Ищите строки с [ERROR] или [WARN]
```

---

### Проблема 2: Environment variables не работают

**Симптомы:**

```
Error: Missing required environment variable: ATLASSIAN_API_TOKEN
```

**Решения:**

**Шаг 1: Проверить что переменные установлены**

```bash
echo $ATLASSIAN_SITE
echo $ATLASSIAN_API_TOKEN

# Если пусто — переменные не установлены
```

**Шаг 2: Добавить в shell profile**

```bash
# Определить используемый shell
echo $SHELL
# /bin/bash → редактировать ~/.bashrc
# /bin/zsh → редактировать ~/.zshrc

# Добавить в конец файла
echo 'export ATLASSIAN_SITE="your-company.atlassian.net"' >> ~/.bashrc
echo 'export ATLASSIAN_EMAIL="your-email@example.com"' >> ~/.bashrc
echo 'export ATLASSIAN_API_TOKEN="your_token"' >> ~/.bashrc

# Применить изменения
source ~/.bashrc
```

**Шаг 3: Перезапустить терминал**

После добавления переменных в profile **обязательно** перезапустите терминал или выполните `source ~/.bashrc`.

**Шаг 4: Проверить синтаксис в mcp.json**

```bash
cat ~/.claude/mcp.json | grep ATLASSIAN

# Должно быть:
# "ATLASSIAN_SITE": "${ATLASSIAN_SITE}"
# НЕ должно быть:
# "ATLASSIAN_SITE": "$ATLASSIAN_SITE"  # ❌ неправильно
```

---

### Проблема 3: "Invalid API token" для Jira/GitHub

**Симптомы:**

```
Error: 401 Unauthorized
Invalid API token
```

**Решения для Jira:**

**Проверка 1: Формат токена**

Jira API token — это длинная строка (примерно 24 символа), **НЕ** начинающаяся с префикса.

```bash
echo $ATLASSIAN_API_TOKEN
# Должно быть примерно: ABCDabcd1234XYZ9876wxyz
```

**Проверка 2: Email и Site**

```bash
# Email должен совпадать с аккаунтом Jira
echo $ATLASSIAN_EMAIL
# Пример: john.doe@company.com

# Site должен быть без https://
echo $ATLASSIAN_SITE
# Правильно: company.atlassian.net
# Неправильно: https://company.atlassian.net
```

**Проверка 3: Переполучить токен**

1. Перейти: https://id.atlassian.com/manage-profile/security/api-tokens
2. Удалить старый токен
3. Создать новый токен
4. Обновить в environment variables

**Решения для GitHub:**

**Проверка 1: Scopes токена**

Токен должен иметь scope `repo` (полный доступ к репозиториям).

1. Перейти: https://github.com/settings/tokens
2. Проверить scopes вашего токена
3. Если `repo` нет — создать новый токен с нужным scope

**Проверка 2: Формат токена**

GitHub Personal Access Token начинается с `ghp_`.

```bash
echo $GITHUB_TOKEN
# Должно быть: ghp_abcd1234WXYZ5678efgh90...
```

---

### Проблема 4: Агент не видит MCP-инструменты

**Симптомы:**

```bash
claude -p "List available MCP tools"
# Агент отвечает: "I don't have access to MCP tools"
```

**Решения:**

**Шаг 1: Проверить что mcp.json существует**

```bash
ls -la ~/.claude/mcp.json
# Должен показать файл

# Если файла нет — создать заново (см. Шаг 2 этого документа)
```

**Шаг 2: Проверить JSON синтаксис**

```bash
# Валидация JSON
python3 -m json.tool ~/.claude/mcp.json

# Или через Node.js
node -e "JSON.parse(require('fs').readFileSync('$HOME/.claude/mcp.json', 'utf8'))"

# Если ошибки — исправить синтаксис
```

**Шаг 3: Перезапустить Claude Code**

```bash
# Если Claude Code был запущен ДО создания mcp.json:
# Завершить текущую сессию (exit или Ctrl+D)
# Запустить заново
claude
```

**Шаг 4: Проверить права доступа**

```bash
chmod 644 ~/.claude/mcp.json
```

---

### Проблема 5: JetBrains IDE не подключается

**Симптомы:**

- MCP сервер в IDE показывает статус "Disconnected"
- Агент не может вызывать IDE инструменты

**Решения:**

**Шаг 1: Проверить версию IDE**

MCP поддерживается только в JetBrains IDE версии 2024.3+.

```bash
# Открыть IDE → Help → About
# Проверить версию: должно быть 2024.3 или новее

# Если версия старая — обновить IDE
```

**Шаг 2: Включить MCP Server в IDE**

1. Settings → Tools → Model Context Protocol
2. Enable MCP Server: ✅
3. Port: `8765`
4. Apply → OK

**Шаг 3: Проверить что IDE запущена**

JetBrains MCP работает только когда IDE активна.

```bash
# Убедиться что IDE открыта с вашим проектом
# Проверить статус в IDE: View → Tool Windows → MCP Server Status
```

**Шаг 4: Firewall**

Убедиться, что порт `8765` не заблокирован:

```bash
# macOS/Linux
lsof -i :8765
# Должен показать процесс IDE
```

**Альтернатива: Использовать Claude Code без JetBrains MCP**

Если JetBrains MCP не работает, можно пропустить его для целей курса. Debugging можно делать через стандартные команды:

```bash
# Вместо JetBrains debugger
claude -p "Add print statements to debug this function"
```

---

## Чеклист выполнения

Убедитесь что все пункты выполнены:

### ✅ Установка серверов

- [ ] Git MCP установлен: `npx @modelcontextprotocol/server-git --version`
- [ ] Jira MCP (или GitHub/Todoist) установлен
- [ ] Figma MCP установлен
- [ ] JetBrains MCP настроен (или пропущен осознанно)

### ✅ Конфигурация

- [ ] Файл `~/.claude/mcp.json` создан
- [ ] Environment variables установлены: `echo $ATLASSIAN_API_TOKEN` (или другие)
- [ ] JSON синтаксис валиден: `python3 -m json.tool ~/.claude/mcp.json`
- [ ] Claude Code видит MCP-серверы: `claude -p "List MCP tools"`

### ✅ Практические задачи

- [ ] Выполнена Задача A: Code Archaeology + Task Planning (или Задача B с Figma)
- [ ] Агент успешно использовал несколько MCP-серверов
- [ ] Результат задачи сохранён и проверен

### ✅ Расширенный каталог

- [ ] Изучил каталог дополнительных MCP-серверов
- [ ] Выбрал 1 сервер для своего проекта
- [ ] Установил и протестировал выбранный сервер

### ✅ Понимание MCP

- [ ] Понимаю что такое MCP и зачем он нужен
- [ ] Знаю как добавить новый MCP-сервер в конфигурацию
- [ ] Умею диагностировать проблемы с MCP (см. Troubleshooting)

---

## Связь с другими модулями

### Модуль 2: Инструменты разработки

**Зависимость:** Вы используете песочницу `task-manager`, созданную в Модуле 2 (файл `course/module-2-tools/practice-setup.md`).

**Что используется:**
- Claude Code CLI
- Git репозиторий проекта
- Базовая конфигурация `~/.claude/config.json`

### Модуль 5: Specification-Driven Development

**Связь:** MCP-серверы (особенно Git и Jira) критически важны для SDD workflows.

**Примеры использования:**
- Git MCP для анализа истории спецификаций
- Jira MCP для связи задач со спецификациями
- Генерация кода из OpenAPI specs с контекстом из Git

### Модуль 7: Оркестрация агентов

**Связь:** MCP-серверы используются в headless режиме для автоматизации.

**Примеры:**
- CI/CD pipeline с Git MCP для автоматического анализа изменений
- Автоматическое обновление Jira worklogs после завершения задачи
- Автоматическая генерация Mermaid диаграмм при изменении архитектуры

---

## Практические советы

### Выбор MCP-серверов под проект

**Для backend (Python/Node.js):**
- Git MCP (обязательно)
- PostgreSQL/MySQL MCP (если используете SQL БД)
- GitHub Issues MCP (для task tracking)
- Mermaid MCP (для диаграмм API)

**Для frontend (React/Vue):**
- Git MCP (обязательно)
- Figma MCP (design-to-code)
- Puppeteer MCP (E2E тесты)
- BrowserStack MCP (кросс-браузерность)

**Для full-stack:**
- Git MCP + Jira MCP + Figma MCP (core trio)
- PostgreSQL MCP (БД)
- Mermaid MCP (документация)

**Для DevOps:**
- Git MCP (обязательно)
- Docker MCP (управление контейнерами)
- Kubernetes MCP (оркестрация)

### Оптимизация производительности

**Проблема:** Большое количество MCP-серверов замедляет Claude Code.

**Решение:**

1. **Используйте проекто-специфичные конфиги:**

```bash
# Глобальная конфигурация (минимум серверов)
~/.claude/mcp.json

# Проекто-специфичная конфигурация (больше серверов)
~/projects/my-app/.claude/mcp.json
```

Claude Code автоматически использует локальную конфигурацию, если она существует.

2. **Отключайте ненужные серверы:**

```json
{
  "mcpServers": {
    "git": { "enabled": true },
    "figma": { "enabled": false }  // Отключить для backend проектов
  }
}
```

3. **Используйте lazy loading:**

Некоторые серверы запускаются только при первом вызове (не при старте Claude Code). Это экономит ресурсы.

### Безопасность API токенов

**НЕ храните токены в коде или git:**

```bash
# ❌ НЕПРАВИЛЬНО
# mcp.json в git с токенами

# ✅ ПРАВИЛЬНО
# mcp.json использует ${VAR_NAME}
# Реальные токены в ~/.bashrc (не в git)
```

**Используйте разные токены для разных окружений:**

```bash
# Production токены
export JIRA_TOKEN_PROD="..."

# Development токены
export JIRA_TOKEN_DEV="..."

# В mcp.json
"ATLASSIAN_API_TOKEN": "${JIRA_TOKEN_DEV}"
```

### Debugging MCP-серверов

**Включить детальное логирование:**

```bash
# Запустить Claude Code с debug режимом
DEBUG=mcp:* claude

# Или для конкретного сервера
DEBUG=mcp:git claude
```

**Проверка коммуникации:**

```bash
# Запустить сервер вручную и проверить вывод
npx @modelcontextprotocol/server-git 2>&1 | tee mcp-git.log

# Анализировать лог
cat mcp-git.log
```

---

## Следующие шаги

После завершения практики по MCP:

### Модуль 7: Оркестрация агентов

Вы будете использовать MCP-серверы для:
- Headless workflows (автоматизация без UI)
- Multi-agent collaboration (несколько агентов работают параллельно)
- CI/CD интеграция (агент в GitHub Actions с доступом к MCP)

**Подготовка:**
- Убедитесь что все MCP-серверы работают
- Создайте GitHub Actions workflow файл
- Настройте secrets для API токенов в GitHub

### Модуль 8: Ответственность и контроль

Вы будете настраивать:
- Ограничения для MCP-серверов (какие операции разрешены)
- Аудит использования MCP (логирование вызовов)
- Review процесс для изменений через MCP

---

## Полезные ссылки

### Официальные ресурсы

- **Model Context Protocol:** https://modelcontextprotocol.io
- **MCP Specification:** https://modelcontextprotocol.io/specification/2025-11-25
- **Official Servers:** https://github.com/modelcontextprotocol/servers
- **SDK Documentation:** https://github.com/modelcontextprotocol/sdk

### Каталоги серверов

- **Awesome MCP Servers (1200+):** https://mcp-awesome.com/
- **AI Agents List (593+):** https://aiagentslist.com/mcp-servers
- **MCP Catalog:** https://mcp-catalog.com/

### Документация серверов

- **Git MCP:** https://github.com/modelcontextprotocol/servers/tree/main/src/git
- **Atlassian MCP:** https://github.com/atlassian/atlassian-mcp-server
- **Atlassian Docs:** https://support.atlassian.com/atlassian-rovo-mcp-server/docs/getting-started-with-the-atlassian-remote-mcp-server/
- **JetBrains MCP:** https://github.com/JetBrains/mcp-jetbrains
- **PyCharm Guide:** https://www.jetbrains.com/help/pycharm/mcp-server.html
- **Figma MCP:** https://github.com/GLips/Figma-Context-MCP
- **Figma Guide:** https://help.figma.com/hc/en-us/articles/32132100833559-Guide-to-the-Figma-MCP-server

### Статьи и обзоры

- **Top 10 Best MCP Servers (2026):** https://cybersecuritynews.com/best-model-context-protocol-mcp-servers/
- **Best MCP Servers for Developers:** https://www.builder.io/blog/best-mcp-servers-2026
- **Essential MCP Servers:** https://apidog.com/blog/top-10-mcp-servers-for-claude-code/

### Community

- **MCP Discord:** https://discord.gg/modelcontextprotocol
- **GitHub Issues:** https://github.com/modelcontextprotocol/servers/issues
- **Stack Overflow:** https://stackoverflow.com/questions/tagged/mcp

---

**Время выполнения практики:** 55 минут

**Готовы к следующему модулю?** Переходите к **Модуль 7: Оркестрация агентов** для изучения продвинутых паттернов работы с MCP в production-окружении.
