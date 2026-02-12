# Каталог MCP-серверов (Model Context Protocol)

> Последнее обновление: 12 февраля 2026

## Обзор

Model Context Protocol (MCP) — универсальный стандарт для подключения инструментов к LLM, разработанный Anthropic. MCP заменяет множество разрозненных API-интеграций единым протоколом, позволяя AI-агентам взаимодействовать с любыми инструментами: от IDE и баз данных до дизайн-систем и облачных сервисов.

**Ключевые преимущества:**
- Единый стандарт вместо N различных интеграций
- Plug-and-play архитектура
- Open-source и vendor-neutral
- Поддержка от Cursor, Claude Code, Codex CLI, OpenCode, и других

**Официальный сайт:** https://modelcontextprotocol.io

**Каталоги серверов:**
- https://mcp-awesome.com/ (1200+ серверов)
- https://aiagentslist.com/mcp-servers (593+ серверов)
- https://github.com/modelcontextprotocol/servers (официальные reference implementations)

---

## 1. Обязательные MCP-серверы для курса

### 1.1. Git MCP Server

**Назначение:** Глубокая работа с Git — не просто commit/push, а интеллектуальный анализ истории, конфликтов, веток, и code archaeology.

**Возможности:**
- Анализ истории изменений (`git log`, `git blame`)
- Поиск в истории коммитов (`git log --grep`, `git log -S`)
- Работа с ветками (создание, merge, rebase)
- Разрешение конфликтов
- Cherry-pick и bisect
- Анализ contribution patterns
- Code archaeology (кто, когда, почему изменил код)

**Установка:**
```bash
# npm
npm install -g @modelcontextprotocol/server-git

# Или через MCP registry
mcp install git
```

**Конфигурация (Claude Code):**
```json
{
  "mcpServers": {
    "git": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-git"],
      "cwd": "."
    }
  }
}
```

**Примеры использования:**
```
Claude, найди все коммиты, которые изменяли auth.py за последний месяц

Claude, кто последним менял функцию calculate_price и почему?

Claude, проанализируй конфликт слияния в файле database.py и предложи решение

Claude, покажи contribution pattern для модуля payments
```

**Совместимость:**
- ✅ Claude Code
- ✅ Cursor
- ✅ OpenCode
- ✅ Codex CLI

**Зрелость:** ⭐⭐⭐⭐⭐ (Official Anthropic implementation)

**Ссылка:** https://github.com/modelcontextprotocol/servers/tree/main/src/git

---

### 1.2. Jira MCP Server (Atlassian)

**Назначение:** Интеграция с Jira для работы с задачами, worklogs, спринтами. Позволяет AI-агенту видеть контекст задачи, автоматически логировать время, обновлять статусы.

**Возможности:**
- Поиск и чтение задач (JQL queries)
- Создание и обновление задач
- **Worklogs**: автоматическое логирование времени работы агента
- Комментирование задач
- Работа со спринтами
- Transition задач по workflow
- Получение данных из Confluence

**Установка:**
```bash
npm install -g @atlassian/atlassian-mcp-server
```

**Конфигурация:**
```json
{
  "mcpServers": {
    "jira": {
      "command": "npx",
      "args": ["-y", "@atlassian/atlassian-mcp-server"],
      "env": {
        "ATLASSIAN_SITE": "your-domain.atlassian.net",
        "ATLASSIAN_EMAIL": "your-email@example.com",
        "ATLASSIAN_API_TOKEN": "your-api-token"
      }
    }
  }
}
```

**Примеры использования:**
```
Claude, покажи все задачи в спринте "Sprint 23" со статусом "In Progress"

Claude, реализуй задачу PROJ-123 и автоматически залогируй потраченное время в Jira

Claude, обнови статус PROJ-456 на "Done" и добавь комментарий с summary изменений

Claude, найди все open баги с priority High в компоненте "Authentication"
```

**Worklogs автоматически:**
Агент может отслеживать время работы над задачей и автоматически создавать worklog записи:
```json
{
  "issue": "PROJ-123",
  "timeSpentSeconds": 3600,
  "comment": "Implemented OAuth2 authentication flow using Claude Code"
}
```

**Совместимость:**
- ✅ Claude Code
- ✅ Cursor
- ✅ OpenCode
- ⚠️ Codex CLI (ограниченная поддержка)

**Зрелость:** ⭐⭐⭐⭐⭐ (Official Atlassian implementation)

**Ссылки:**
- https://github.com/atlassian/atlassian-mcp-server
- https://support.atlassian.com/atlassian-rovo-mcp-server/docs/getting-started-with-the-atlassian-remote-mcp-server/
- https://www.atlassian.com/platform/remote-mcp-server

---

### 1.3. JetBrains MCP Server (PyCharm, IntelliJ, WebStorm)

**Назначение:** Интеграция с JetBrains IDE — доступ к отладчику, рефакторингу, навигации, code analysis прямо из AI-агента.

**Возможности:**
- **Debugger integration**: Установка breakpoints, step-through, inspect variables
- **Code analysis**: Inspections, warnings, errors
- **Refactoring tools**: Rename, extract method, inline, move
- **Project navigation**: Go to definition, find usages, class hierarchy
- **Run configurations**: Запуск тестов, приложения
- **Terminal commands**: Выполнение команд в IDE terminal
- **File operations**: Чтение, запись, навигация

**Установка:**

MCP Server встроен в JetBrains IDE начиная с версии 2025.2+. Нужно только включить:

```
Settings → Tools → Model Context Protocol → Enable MCP Server
```

Порт по умолчанию: `localhost:8765`

**Конфигурация (Claude Code):**
```json
{
  "mcpServers": {
    "pycharm": {
      "command": "jetbrains-mcp-client",
      "args": ["--host", "localhost", "--port", "8765"],
      "env": {
        "IDE": "pycharm"
      }
    }
  }
}
```

**Примеры использования:**
```
Claude, поставь breakpoint на строке 45 в auth.py и покажи значение переменной user_id когда код остановится

Claude, запусти тесты для модуля payments и покажи failed тесты

Claude, используя рефакторинг-инструменты PyCharm, переименуй класс OldUser в User во всем проекте

Claude, найди все места, где используется функция calculate_total, и покажи их

Claude, запусти Django dev server через run configuration
```

**Поддерживаемые IDE:**
- PyCharm (Python)
- IntelliJ IDEA (Java, Kotlin)
- WebStorm (JavaScript, TypeScript)
- Android Studio (Android)
- Rider (.NET)
- GoLand (Go)

**Совместимость:**
- ✅ Claude Code
- ✅ Cursor
- ✅ OpenCode
- ✅ Codex CLI

**Зрелость:** ⭐⭐⭐⭐⭐ (Official JetBrains implementation)

**Ссылки:**
- https://github.com/JetBrains/mcp-jetbrains
- https://www.jetbrains.com/help/pycharm/mcp-server.html
- https://www.jetbrains.com/help/idea/mcp-server.html

---

### 1.4. Figma MCP Server

**Назначение:** Интеграция с Figma Dev Mode — AI видит структуру дизайна (слои, auto-layout, variants, tokens) и генерирует код, соответствующий реальному дизайну.

**Возможности:**
- Чтение структуры слоев (hierarchy)
- Извлечение design tokens (colors, typography, spacing)
- Анализ auto-layout
- Работа с variants и component sets
- Экспорт assets
- Генерация кода на основе реального дизайна (не screenshots)

**Установка:**
```bash
npm install -g @glips/figma-context-mcp
```

**Конфигурация:**
```json
{
  "mcpServers": {
    "figma": {
      "command": "npx",
      "args": ["-y", "@glips/figma-context-mcp"],
      "env": {
        "FIGMA_ACCESS_TOKEN": "your-figma-token"
      }
    }
  }
}
```

**Примеры использования:**
```
Claude, подключись к Figma файлу "Mobile App Design" и покажи структуру экрана LoginScreen

Claude, сгенерируй React компонент на основе Figma компонента "UserCard" с точными стилями из design tokens

Claude, извлеки все color tokens из Figma и создай CSS variables

Claude, проанализируй auto-layout в компоненте "Dashboard Header" и сгенерируй соответствующий CSS Grid код
```

**Workflow:**
1. Дизайнер создает дизайн в Figma
2. AI читает структуру через MCP (не screenshot!)
3. AI генерирует код с точными значениями (spacing, colors, typography)
4. Код соответствует дизайну на 100%

**Совместимость:**
- ✅ Claude Code
- ✅ Cursor
- ✅ OpenCode
- ⚠️ Codex CLI (partial)

**Зрелость:** ⭐⭐⭐⭐ (Community-driven, активно развивается)

**Ссылки:**
- https://github.com/GLips/Figma-Context-MCP
- https://help.figma.com/hc/en-us/articles/32132100833559-Guide-to-the-Figma-MCP-server

---

## 2. Рекомендуемые MCP-серверы для курса

### 2.1. Mermaid MCP Server

**Назначение:** Генерация и рендеринг диаграмм Mermaid (flowcharts, sequence diagrams, ER diagrams, architecture diagrams).

**Возможности:**
- Конвертация Mermaid syntax в PNG/SVG
- Валидация Mermaid syntax
- Рендеринг через headless browser (Puppeteer)
- Поддержка всех типов диаграмм Mermaid

**Установка:**
```bash
npm install -g mermaid-mcp-server
```

**Примеры использования:**
```
Claude, создай sequence diagram для OAuth2 authentication flow

Claude, визуализируй архитектуру микросервисов проекта как C4 diagram

Claude, сгенерируй ER-диаграмму для базы данных на основе Django models

Claude, создай flowchart для процесса onboarding пользователя
```

**Зачем это нужно на курсе:**
- Автоматическая генерация диаграмм из кода
- Визуализация архитектуры
- Документирование workflows
- Presentations и technical specs

**Совместимость:**
- ✅ Claude Code
- ✅ Cursor
- ✅ OpenCode
- ✅ Codex CLI

**Зрелость:** ⭐⭐⭐⭐

**Ссылки:**
- https://github.com/hustcc/mcp-mermaid
- https://github.com/peng-shawn/mermaid-mcp-server

---

### 2.2. PostgreSQL MCP Server

**Назначение:** Работа с PostgreSQL через natural language — запросы, анализ схемы, миграции.

**Возможности:**
- Natural language SQL queries
- Schema analysis и documentation
- Query optimization suggestions
- Database migrations
- Data exploration

**Установка:**
```bash
npm install -g @modelcontextprotocol/server-postgres
```

**Конфигурация:**
```json
{
  "mcpServers": {
    "postgres": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres"],
      "env": {
        "POSTGRES_CONNECTION_STRING": "postgresql://user:pass@localhost/db"
      }
    }
  }
}
```

**Примеры использования:**
```
Claude, покажи всех пользователей, зарегистрированных за последнюю неделю

Claude, найди все заказы со статусом "pending" дольше 24 часов

Claude, проанализируй схему таблицы users и предложи индексы для оптимизации

Claude, создай миграцию для добавления поля email_verified в таблицу users
```

**Зачем это нужно на курсе:**
- AI работает с базой данных напрямую
- Автоматический анализ данных
- Генерация миграций
- Debugging производительности

**Совместимость:**
- ✅ Claude Code
- ✅ Cursor
- ✅ OpenCode
- ✅ Codex CLI

**Зрелость:** ⭐⭐⭐⭐⭐ (Official implementation)

**Ссылка:** https://github.com/modelcontextprotocol/servers/tree/main/src/postgres

---

### 2.3. Puppeteer MCP Server

**Назначение:** Web automation — навигация, заполнение форм, скриншоты, E2E тестирование.

**Возможности:**
- Навигация по сайтам
- Заполнение и submit форм
- Клики, scroll, hover
- Захват screenshots
- PDF generation
- E2E test scenarios
- Web scraping

**Установка:**
```bash
npm install -g @modelcontextprotocol/server-puppeteer
```

**Примеры использования:**
```
Claude, открой staging.example.com, залогинься с тестовым пользователем, и сделай screenshot дашборда

Claude, пройди через форму регистрации на сайте, заполни все поля, и проверь что email подтверждения отправлен

Claude, создай E2E тест для checkout flow: добавление товара в корзину → оформление заказа → payment

Claude, сгенерируй PDF-репорт со страницы /reports/monthly
```

**Зачем это нужно на курсе:**
- Автоматизация E2E тестирования
- Visual regression testing
- Web scraping для исследования
- Автогенерация test scenarios

**Совместимость:**
- ✅ Claude Code
- ✅ Cursor
- ✅ OpenCode
- ⚠️ Codex CLI (limited)

**Зрелость:** ⭐⭐⭐⭐⭐ (Official implementation)

**Ссылка:** https://github.com/modelcontextprotocol/servers/tree/main/src/puppeteer

---

## 3. Расширенный список MCP-серверов

### 3.1. Development Tools

| Сервер | Назначение | Установка | Зрелость |
|--------|-----------|-----------|----------|
| **GitHub MCP** | Issues, PRs, code reviews, releases | `npm i -g @modelcontextprotocol/server-github` | ⭐⭐⭐⭐⭐ |
| **GitLab MCP** | GitLab API integration | `npm i -g gitlab-mcp-server` | ⭐⭐⭐⭐ |
| **Docker MCP** | Управление containers, images, networks | `npm i -g @modelcontextprotocol/server-docker` | ⭐⭐⭐⭐ |
| **Kubernetes MCP** | Pods, deployments, services management | `npm i -g k8s-mcp-server` | ⭐⭐⭐ |

### 3.2. Databases

| Сервер | Назначение | Установка | Зрелость |
|--------|-----------|-----------|----------|
| **MySQL MCP** | MySQL natural language queries | `npm i -g @modelcontextprotocol/server-mysql` | ⭐⭐⭐⭐⭐ |
| **MongoDB MCP** | NoSQL queries и aggregations | `npm i -g mongodb-mcp-server` | ⭐⭐⭐⭐ |
| **Redis MCP** | Cache operations, pub/sub | `npm i -g redis-mcp-server` | ⭐⭐⭐⭐ |
| **Supabase MCP** | Postgres + Auth + Storage | `npm i -g @supabase/mcp-server` | ⭐⭐⭐⭐ |

### 3.3. Cloud & Infrastructure

| Сервер | Назначение | Установка | Зрелость |
|--------|-----------|-----------|----------|
| **AWS MCP** | EC2, S3, Lambda, и др. | `npm i -g aws-mcp-server` | ⭐⭐⭐⭐ |
| **Google Cloud MCP** | GCP services integration | `npm i -g gcp-mcp-server` | ⭐⭐⭐⭐ |
| **Terraform MCP** | Infrastructure as Code | `npm i -g terraform-mcp-server` | ⭐⭐⭐ |

### 3.4. Design & Collaboration

| Сервер | Назначение | Установка | Зрелость |
|--------|-----------|-----------|----------|
| **Miro MCP** | Whiteboarding, diagrams из кода | `npm i -g @k-jarzyna/mcp-miro` | ⭐⭐⭐ |
| **Obsidian MCP** | Knowledge base, notes | `npm i -g mcp-obsidian` | ⭐⭐⭐⭐ |
| **Notion MCP** | Notion pages и databases | `npm i -g @notionhq/mcp-server` | ⭐⭐⭐⭐⭐ |
| **Slack MCP** | Messaging, channels, bots | `npm i -g slack-mcp-server` | ⭐⭐⭐⭐ |

### 3.5. Office & Documents

| Сервер | Назначение | Установка | Зрелость |
|--------|-----------|-----------|----------|
| **PowerPoint MCP** | Create/edit презентации | `npm i -g office-powerpoint-mcp-server` | ⭐⭐⭐ |
| **Google Sheets MCP** | Spreadsheets automation | `npm i -g google-sheets-mcp` | ⭐⭐⭐⭐ |
| **PDF MCP** | PDF generation/parsing | `npm i -g pdf-mcp-server` | ⭐⭐⭐⭐ |

### 3.6. Testing & Monitoring

| Сервер | Назначение | Установка | Зрелость |
|--------|-----------|-----------|----------|
| **BrowserStack MCP** | Cross-browser testing | `npm i -g browserstack-mcp` | ⭐⭐⭐ |
| **Sentry MCP** | Error tracking | `npm i -g sentry-mcp-server` | ⭐⭐⭐⭐ |
| **Datadog MCP** | Monitoring, logs, traces | `npm i -g datadog-mcp-server` | ⭐⭐⭐⭐ |

**Ссылки:**
- https://github.com/k-jarzyna/mcp-miro
- https://github.com/MarkusPfundstein/mcp-obsidian
- https://github.com/GongRzhe/Office-PowerPoint-MCP-Server

---

## 4. Рекомендации для курса

### Топ-4 сервера для обязательного изучения

| № | Сервер | Обоснование | Приоритет |
|---|--------|-------------|-----------|
| **1** | **Git MCP** | Code archaeology, анализ истории, разрешение конфликтов — критичные навыки для работы с legacy code и командной разработки | 🔴 Критичный |
| **2** | **Jira MCP** | Автоматизация worklogs, интеграция с task tracking, работа в enterprise-среде — must-have для professional development | 🔴 Критичный |
| **3** | **JetBrains MCP** | Debugger, refactoring tools, code analysis — мощнейшие возможности IDE доступны из AI-агента. Особенно важно для PyCharm в Python-разработке | 🟠 Важный |
| **4** | **Figma MCP** | Design-to-code workflow, интеграция frontend с дизайн-системой, извлечение design tokens, auto-layout — критичные навыки для full-stack разработчиков | 🔴 Критичный |

### Дополнительные 2-3 сервера для продвинутых студентов

| № | Сервер | Use Case | Приоритет |
|---|--------|----------|-----------|
| **5** | **PostgreSQL MCP** | Natural language queries, анализ данных, автогенерация миграций | 🟠 Важный |
| **6** | **Puppeteer MCP** | E2E тестирование, web automation | 🟡 Опциональный |
| **7** | **Mermaid MCP** | Диаграммы, документация, визуализация архитектуры | 🟡 Опциональный |

### Учебный план

**Модуль 3: Работа с MCP (6 часов)**

**Часть 1 (2 часа): Основы MCP**
- Что такое MCP и зачем он нужен
- Установка и конфигурация первого сервера
- Практика: Git MCP для code archaeology

**Часть 2 (2 часа): Enterprise Integration**
- Jira MCP: автоматизация worklogs
- JetBrains MCP: debugger и refactoring
- Практика: Реализация задачи из Jira с автологированием времени

**Часть 3 (2 часа): Advanced Use Cases**
- Figma MCP: design-to-code workflow
- PostgreSQL MCP или Puppeteer MCP (на выбор)
- Практика: Комбинирование нескольких MCP-серверов в одном workflow

### Критерии выбора

Серверы выбраны по критериям:
1. **Практическая ценность**: Решают реальные задачи разработчиков
2. **Enterprise-готовность**: Используются в production-среде
3. **Зрелость**: Stable, поддерживаются официально или активным community
4. **Совместимость**: Работают со всеми основными AI-инструментами
5. **Learning curve**: Доступны для изучения за ограниченное время курса

---

## 5. Установка и настройка

### Глобальная установка (рекомендуется)

```bash
# Обязательные для курса
npm install -g @modelcontextprotocol/server-git
npm install -g @atlassian/atlassian-mcp-server
npm install -g @glips/figma-context-mcp

# Дополнительные
npm install -g @modelcontextprotocol/server-postgres
npm install -g mermaid-mcp-server
npm install -g @modelcontextprotocol/server-puppeteer
```

### Конфигурация Claude Code

Создайте `~/.claude/mcp.json`:

```json
{
  "mcpServers": {
    "git": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-git"]
    },
    "jira": {
      "command": "npx",
      "args": ["-y", "@atlassian/atlassian-mcp-server"],
      "env": {
        "ATLASSIAN_SITE": "your-domain.atlassian.net",
        "ATLASSIAN_EMAIL": "your-email@example.com",
        "ATLASSIAN_API_TOKEN": "your-api-token"
      }
    },
    "pycharm": {
      "command": "jetbrains-mcp-client",
      "args": ["--host", "localhost", "--port", "8765"]
    },
    "figma": {
      "command": "npx",
      "args": ["-y", "@glips/figma-context-mcp"],
      "env": {
        "FIGMA_ACCESS_TOKEN": "your-token"
      }
    }
  }
}
```

### Конфигурация Cursor

В `.cursor/mcp.json` (в корне проекта):

```json
{
  "mcpServers": {
    "git": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-git"]
    },
    "postgres": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres"],
      "env": {
        "POSTGRES_CONNECTION_STRING": "postgresql://localhost/mydb"
      }
    }
  }
}
```

### Проверка установки

```bash
# Claude Code
claude -p "List available MCP servers"

# Cursor
# Settings → MCP → View Connected Servers

# OpenCode
opencode mcp list
```

---

## 6. Best Practices

### Безопасность

1. **Храните токены в переменных окружения**, не в git:
```bash
export JIRA_API_TOKEN="..."
export FIGMA_ACCESS_TOKEN="..."
export POSTGRES_PASSWORD="..."
```

2. **Read-only доступ где возможно**: Ограничивайте permissions для MCP-серверов

3. **Sandboxing**: Используйте Docker для изоляции MCP-серверов

### Производительность

1. **Ленивая инициализация**: MCP-серверы запускаются только когда нужны
2. **Connection pooling**: Для database MCP-серверов
3. **Caching**: Кэшируйте редко меняющиеся данные (schema, metadata)

### Debugging

1. **Логирование**: Включите verbose logging для MCP-серверов:
```json
{
  "mcpServers": {
    "git": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-git"],
      "env": {
        "MCP_LOG_LEVEL": "debug"
      }
    }
  }
}
```

2. **Health checks**: Регулярно проверяйте доступность серверов
3. **Fallbacks**: Если MCP-сервер недоступен, агент должен gracefully degrade

---

## 7. Создание собственного MCP-сервера (Advanced)

### Минимальный пример (TypeScript)

```typescript
import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';

const server = new Server({
  name: 'my-custom-server',
  version: '1.0.0',
});

// Регистрация tool
server.setRequestHandler('tools/list', async () => ({
  tools: [
    {
      name: 'get_weather',
      description: 'Get current weather for a city',
      inputSchema: {
        type: 'object',
        properties: {
          city: { type: 'string' }
        },
        required: ['city']
      }
    }
  ]
}));

// Обработка вызова tool
server.setRequestHandler('tools/call', async (request) => {
  if (request.params.name === 'get_weather') {
    const { city } = request.params.arguments;
    const weather = await fetchWeather(city);
    return {
      content: [{ type: 'text', text: `Weather in ${city}: ${weather}` }]
    };
  }
});

// Запуск сервера
const transport = new StdioServerTransport();
await server.connect(transport);
```

### Use Cases для кастомных серверов

- Интеграция с internal tools компании
- Proprietary APIs
- Legacy systems
- Custom workflows

---

## Источники

### Официальные ресурсы
- [Model Context Protocol Specification](https://modelcontextprotocol.io/specification/2025-11-25)
- [Official MCP Servers Repository](https://github.com/modelcontextprotocol/servers)
- [Awesome MCP Servers (1200+)](https://mcp-awesome.com/)
- [MCP Servers Directory (593+)](https://aiagentslist.com/mcp-servers)
- [MCP Catalog](https://mcp-catalog.com/)

### Документация серверов
- [Git MCP Server](https://github.com/modelcontextprotocol/servers/tree/main/src/git)
- [Atlassian MCP Server](https://github.com/atlassian/atlassian-mcp-server)
- [Atlassian MCP Documentation](https://support.atlassian.com/atlassian-rovo-mcp-server/docs/getting-started-with-the-atlassian-remote-mcp-server/)
- [JetBrains MCP Server](https://github.com/JetBrains/mcp-jetbrains)
- [PyCharm MCP Documentation](https://www.jetbrains.com/help/pycharm/mcp-server.html)
- [Figma MCP Server](https://github.com/GLips/Figma-Context-MCP)
- [Figma MCP Guide](https://help.figma.com/hc/en-us/articles/32132100833559-Guide-to-the-Figma-MCP-server)
- [PostgreSQL MCP Server](https://github.com/modelcontextprotocol/servers/tree/main/src/postgres)
- [Puppeteer MCP Server](https://github.com/modelcontextprotocol/servers/tree/main/src/puppeteer)

### Статьи и обзоры
- [Top 10 Best MCP Servers in 2026](https://cybersecuritynews.com/best-model-context-protocol-mcp-servers/)
- [Best MCP Servers for Developers in 2026](https://www.builder.io/blog/best-mcp-servers-2026)
- [Top 10 Essential MCP Servers for Claude Code](https://apidog.com/blog/top-10-mcp-servers-for-claude-code/)
- [Data Commons MCP Server](https://developers.googleblog.com/en/datacommonsmcp/)

---

**Дата обновления:** 12 февраля 2026
**Автор:** AI Course Research Team
