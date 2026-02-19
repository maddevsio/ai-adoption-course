# Модуль 6: Model Context Protocol (MCP)

> **Цель модуля:** Научиться расширять возможности AI-агентов через протокол MCP, интегрируя их с внешними инструментами, сервисами и системами.

---

## 1. Введение: Что такое MCP и зачем он нужен

### Проблема: ограниченность базовых возможностей агента

Представьте, что вы работаете с AI-агентом над реальным проектом. Агент может читать и редактировать файлы, выполнять команды в терминале, работать с Git. Но что происходит, когда задача требует большего?

- **Code archaeology**: нужно понять, кто, когда и почему изменил критичный участок кода — для этого требуется глубокий анализ истории Git с использованием `git blame`, `git log --grep`, `git log -S` и других advanced команд
- **Task tracking**: вы реализуете задачу из Jira, и нужно автоматически залогировать время работы (worklogs), обновить статус задачи, добавить комментарий с summary изменений
- **Design-to-code workflow**: дизайнер создал компонент в Figma с точными spacing, colors, typography — вам нужно сгенерировать код, который на 100% соответствует дизайну, а не приблизительно
- **Debugging**: вы отлаживаете сложный баг и хотите, чтобы агент поставил breakpoint в IDE, запустил отладчик и показал значения переменных в момент остановки

Базовые возможности агента (файловая система + терминал) не покрывают эти сценарии. Можно попытаться решить через bash-команды, но это неудобно, ненадежно и требует постоянного контекста от пользователя.

### Решение: MCP расширяет возможности агента

**Model Context Protocol (MCP)** — это универсальный стандарт для подключения инструментов к Large Language Models, разработанный Anthropic. MCP решает проблему фрагментированности: вместо того чтобы каждый AI-инструмент (Claude Code, Cursor, OpenCode, Codex CLI) создавал свои собственные интеграции с тысячами сервисов, все используют единый протокол.

**Ключевые преимущества MCP:**

1. **Единый стандарт вместо N интеграций**: Один MCP-сервер работает со всеми AI-агентами, поддерживающими протокол
2. **Plug-and-play архитектура**: Установил MCP-сервер через npm, добавил конфигурацию в `~/.claude/mcp.json` — готово
3. **Open-source и vendor-neutral**: Протокол открыт, не привязан к конкретному провайдеру
4. **Широкая поддержка**: Cursor, Claude Code, Codex CLI, OpenCode, и другие

**Официальные ресурсы:**
- Сайт: https://modelcontextprotocol.io
- Спецификация: https://modelcontextprotocol.io/specification/2025-11-25
- Официальные серверы: https://github.com/modelcontextprotocol/servers
- Каталоги: [mcp-awesome.com](https://mcp-awesome.com/) (1200+ серверов), [aiagentslist.com/mcp-servers](https://aiagentslist.com/mcp-servers) (593+ серверов)

### Что дает MCP на практике

После установки нескольких MCP-серверов вы можете:

```
Claude, найди все коммиты, которые изменяли auth.py за последний месяц
→ Git MCP выполняет git log --grep, git log -S, анализирует историю

Claude, реализуй задачу PROJ-123 и автоматически залогируй время в Jira
→ Jira MCP читает задачу, вы работаете, агент создает worklog

Claude, поставь breakpoint на строке 45 в auth.py и покажи значение user_id
→ JetBrains MCP взаимодействует с отладчиком IDE

Claude, сгенерируй React компонент на основе Figma компонента "UserCard"
→ Figma MCP читает структуру слоев, design tokens, auto-layout
```

Агент перестает быть ограниченным файловой системой и терминалом — он получает доступ к IDE, task tracker, design tools, базам данных, и любым другим инструментам через MCP.

---

## 2. Архитектура MCP

### Client-Server модель

> [Диаграмма: Архитектура MCP (Agent -> Servers -> Tools)](./diagrams/mcp-architecture.md)

MCP использует классическую **client-server** архитектуру:

```
┌─────────────────┐         MCP Protocol        ┌──────────────────┐
│   AI Agent      │◄──────────────────────────►│   MCP Server     │
│ (Claude Code,   │    (JSON-RPC over stdio/    │  (Git, Jira,     │
│  Cursor, etc.)  │     SSE, WebSocket)         │   Figma, etc.)   │
└─────────────────┘                             └──────────────────┘
                                                         │
                                                         ▼
                                                ┌──────────────────┐
                                                │  External Tool   │
                                                │ (Git, Jira API,  │
                                                │  Figma API, IDE) │
                                                └──────────────────┘
```

**Компоненты:**

1. **MCP Client (встроен в AI-агент)**: Claude Code, Cursor, OpenCode — все они умеют говорить на MCP
2. **MCP Server**: Node.js/Python-процесс, который предоставляет доступ к конкретному инструменту (Git, Jira, Figma)
3. **External Tool**: Сам инструмент (Git CLI, Jira REST API, Figma Dev Mode API, IDE)

### Протокол: JSON-RPC 2.0

MCP использует **JSON-RPC 2.0** для коммуникации между клиентом и сервером. Это простой текстовый протокол на базе JSON.

**Пример запроса от агента к Git MCP серверу:**

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "git_log",
    "arguments": {
      "path": "/home/user/project",
      "grep": "auth",
      "since": "1 month ago"
    }
  }
}
```

**Пример ответа от сервера:**

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "content": [
      {
        "type": "text",
        "text": "commit abc123...\nAuthor: John Doe\nDate: 2026-01-15\n\nfix: update auth logic"
      }
    ]
  }
}
```

Агент анализирует ответ и использует его для продолжения работы.

### Transport: stdio, SSE, WebSocket

MCP поддерживает три способа транспорта:

1. **stdio (Standard Input/Output)** — самый распространенный для локальных серверов:
   - Агент запускает MCP-сервер как процесс
   - Общение через stdin/stdout
   - Пример: `npx @modelcontextprotocol/server-git`

2. **SSE (Server-Sent Events)** — для удаленных серверов:
   - MCP-сервер работает как HTTP-сервер
   - Агент подключается через SSE
   - Используется для cloud-based серверов

3. **WebSocket** — для двусторонней real-time коммуникации:
   - Полнодуплексный протокол
   - Используется для интерактивных инструментов (live debugging, real-time collaboration)

**Для курса**: мы будем использовать **stdio**, так как все обязательные серверы (Git, Jira, JetBrains, Figma) работают локально.

### Как агент взаимодействует с MCP-сервером

> [Диаграмма: Жизненный цикл MCP-вызова](./diagrams/mcp-lifecycle.md)

**Lifecycle MCP-сервера:**

1. **Initialization (при запуске агента)**:
   - Агент читает `~/.claude/mcp.json`
   - Запускает MCP-серверы как дочерние процессы
   - Отправляет `initialize` запрос каждому серверу

2. **Discovery (при начале работы)**:
   - Агент запрашивает список доступных tools: `tools/list`
   - Сервер возвращает список (например, `git_log`, `git_blame`, `git_search`)
   - Агент добавляет tools в свой prompt context

3. **Execution (во время работы)**:
   - AI принимает решение вызвать tool (например, `git_log`)
   - Агент отправляет `tools/call` с параметрами
   - Сервер выполняет команду, возвращает результат
   - Агент анализирует результат и продолжает

4. **Shutdown (при завершении)**:
   - Агент отправляет `shutdown` всем серверам
   - Серверы корректно завершают работу

**Важно**: MCP-серверы запускаются **лениво** (только когда нужны) и могут переиспользоваться между сессиями (connection pooling).

---

## 3. Категории MCP-серверов

> [Диаграмма: Карта MCP-серверов по приоритету](./diagrams/mcp-server-priorities.md)

MCP-серверы можно разделить на несколько категорий по функциональности.

### 3.1. Development Tools

**Назначение**: Инструменты для разработки — Git, IDE, отладчики, линтеры.

| Сервер | Что дает | Примеры использования |
|--------|----------|----------------------|
| **Git MCP** | Code archaeology, анализ истории, конфликты | `git log --grep`, `git blame`, `git bisect` |
| **GitHub MCP** | Issues, Pull Requests, Code Reviews, Releases | Создание PR, анализ code review, управление issues |
| **JetBrains MCP** | Debugger, refactoring, code analysis, navigation | Breakpoints, step-through, rename refactoring |
| **Docker MCP** | Управление контейнерами, образами, сетями | Запуск контейнера, просмотр логов, очистка |

### 3.2. Data Sources

**Назначение**: Доступ к базам данных и хранилищам данных.

| Сервер | Что дает | Примеры использования |
|--------|----------|----------------------|
| **PostgreSQL MCP** | Natural language SQL queries, schema analysis | Запросы на естественном языке, анализ схемы БД |
| **MySQL MCP** | Аналогично для MySQL | Миграции, оптимизация запросов |
| **MongoDB MCP** | NoSQL queries, aggregations | Aggregation pipelines, data exploration |
| **Redis MCP** | Cache operations, pub/sub | Управление кэшем, real-time messaging |

### 3.3. External Services

**Назначение**: Интеграция с внешними сервисами и платформами.

| Сервер | Что дает | Примеры использования |
|--------|----------|----------------------|
| **Jira MCP** | Tasks, worklogs, sprints, workflow transitions | Автоматическое логирование времени, обновление статусов |
| **Slack MCP** | Messaging, channels, bots | Отправка уведомлений, чтение сообщений |
| **Figma MCP** | Design structure, tokens, auto-layout, components | Design-to-code workflow, извлечение design tokens |
| **Notion MCP** | Pages, databases, blocks | Создание документации, управление knowledge base |

### 3.4. Utilities

**Назначение**: Вспомогательные инструменты — диаграммы, браузер-автоматизация, PDF.

| Сервер | Что дает | Примеры использования |
|--------|----------|----------------------|
| **Mermaid MCP** | Генерация диаграмм (flowcharts, sequence, ER) | Визуализация архитектуры, документирование workflows |
| **Puppeteer MCP** | Web automation, screenshots, E2E тесты | Заполнение форм, тестирование UI, scraping |
| **PDF MCP** | PDF generation, parsing | Генерация отчетов, извлечение данных из PDF |
| **Miro MCP** | Whiteboarding, диаграммы из кода | Collaborative brainstorming, визуализация идей |

---

## 4. Обязательные MCP-серверы для курса

Для курса мы сфокусируемся на **4 ключевых серверах**, которые решают реальные задачи профессиональных разработчиков.

### 4.1. Git MCP Server

**Назначение**: Глубокая работа с Git — не просто commit/push, а интеллектуальный анализ истории, конфликтов, веток, и code archaeology.

#### Что дает Git MCP

Базовые Git-команды (`git add`, `git commit`, `git push`) доступны через терминал. Но Git MCP предоставляет **аналитические возможности**:

- **Code archaeology**: Кто, когда, почему изменил код
- **Поиск в истории**: `git log --grep`, `git log -S` (поиск по содержимому)
- **Анализ веток**: Сравнение, merge conflicts, divergence
- **Blame analysis**: Построчный анализ авторства
- **Bisect**: Поиск коммита, который ввел баг
- **Contribution patterns**: Анализ активности разработчиков

#### Когда использовать

- **Legacy code**: Нужно понять, почему код написан именно так
- **Bug investigation**: Найти, когда появился баг
- **Code review**: Проанализировать изменения в контексте истории
- **Refactoring**: Понять, как код эволюционировал

#### Пример задачи

**Сценарий**: В production обнаружен баг в функции `calculate_discount()`. Нужно найти, когда он появился.

**Команда для агента:**
```
Claude, найди все коммиты, которые изменяли функцию calculate_discount
в файле pricing.py за последние 3 месяца. Покажи автора, дату,
и причину изменений из commit message.
```

**Что делает Git MCP:**
1. Выполняет `git log -S "calculate_discount" --since="3 months ago" -- pricing.py`
2. Для каждого коммита показывает diff
3. Анализирует commit messages
4. Предоставляет агенту полную картину эволюции функции

**Результат**: Агент находит коммит, который ввел баг, и предлагает fix.

#### Установка

```bash
npm install -g @modelcontextprotocol/server-git
```

#### Конфигурация (Claude Code)

`~/.claude/mcp.json`:
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

**Зрелость**: ⭐⭐⭐⭐⭐ (Official Anthropic implementation)

**Ссылка**: https://github.com/modelcontextprotocol/servers/tree/main/src/git

---

### 4.2. Jira MCP Server (Atlassian)

**Назначение**: Интеграция с Jira для работы с задачами, worklogs, спринтами. Позволяет AI-агенту видеть контекст задачи, автоматически логировать время, обновлять статусы.

#### Что дает Jira MCP

В enterprise-разработке вы не просто пишете код — вы работаете с задачами в Jira:
- Читаете описание задачи и acceptance criteria
- Логируете время работы (worklogs)
- Обновляете статус задачи (In Progress → Code Review → Done)
- Добавляете комментарии с summary изменений

Без MCP это требует ручных действий или скриптов. С Jira MCP агент делает это автоматически.

**Основные возможности:**
- **Поиск задач**: JQL queries (`project = PROJ AND status = "In Progress"`)
- **Чтение задач**: Описание, комментарии, attachments
- **Создание/обновление задач**: Новые баги, subtasks, status transitions
- **Worklogs**: Автоматическое логирование времени работы агента
- **Комментарии**: Добавление summary изменений
- **Спринты**: Работа с Agile boards

#### Когда использовать

- **Task-driven development**: Реализация фичи по задаче из Jira
- **Time tracking**: Автоматическое логирование времени (важно для enterprise)
- **Status automation**: Обновление статусов после завершения работы
- **Cross-team collaboration**: Чтение контекста от других команд

#### Пример задачи

**Сценарий**: Нужно реализовать задачу PROJ-456 "Add OAuth2 authentication".

**Команда для агента:**
```
Claude, прочитай задачу PROJ-456 из Jira, реализуй её согласно
acceptance criteria, и автоматически залогируй потраченное время в Jira.
```

**Что делает Jira MCP:**
1. Читает задачу PROJ-456 (описание, acceptance criteria)
2. Предоставляет агенту контекст
3. Агент реализует фичу
4. Jira MCP создает worklog: `{"issue": "PROJ-456", "timeSpentSeconds": 3600, "comment": "Implemented OAuth2 flow using Claude Code"}`
5. Обновляет статус задачи на "Code Review"

**Результат**: Фича реализована, время залогировано, статус обновлен — без единого клика в Jira UI.

#### Установка

```bash
npm install -g @atlassian/atlassian-mcp-server
```

#### Конфигурация

`~/.claude/mcp.json`:
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

**Получение API токена**: https://id.atlassian.com/manage-profile/security/api-tokens

**Зрелость**: ⭐⭐⭐⭐⭐ (Official Atlassian implementation)

**Ссылки**:
- GitHub: https://github.com/atlassian/atlassian-mcp-server
- Документация: https://support.atlassian.com/atlassian-rovo-mcp-server/docs/getting-started-with-the-atlassian-remote-mcp-server/

---

### 4.3. JetBrains MCP Server (PyCharm, IntelliJ, WebStorm)

**Назначение**: Интеграция с JetBrains IDE — доступ к отладчику, рефакторингу, навигации, code analysis прямо из AI-агента.

#### Что дает JetBrains MCP

IDE как PyCharm, IntelliJ IDEA, WebStorm имеют мощнейшие инструменты для разработки:
- **Debugger**: Breakpoints, step-through, watch variables
- **Refactoring**: Rename, extract method, inline, move class
- **Code Analysis**: Inspections, warnings, type checking
- **Navigation**: Go to definition, find usages, class hierarchy
- **Run/Test**: Запуск приложения, тестов, configurations

Без MCP эти инструменты доступны только через UI. С JetBrains MCP агент может:
- Поставить breakpoint и запустить отладчик
- Провести рефакторинг (rename variable во всем проекте)
- Найти все использования функции
- Запустить тесты и показать failed

#### Когда использовать

- **Debugging**: Анализ сложных багов с breakpoints
- **Refactoring**: Безопасное переименование, extract method
- **Code navigation**: Исследование незнакомого codebase
- **Testing**: Запуск тестов через IDE test runner
- **Type checking**: Анализ типов в TypeScript/Python

#### Пример задачи

**Сценарий**: Нужно отладить баг в функции `process_payment()`.

**Команда для агента:**
```
Claude, поставь breakpoint на строке 67 в payment.py (внутри process_payment),
запусти отладчик, и покажи значения переменных user_id, amount, payment_method
в момент остановки.
```

**Что делает JetBrains MCP:**
1. Устанавливает breakpoint на строке 67 в `payment.py`
2. Запускает debug configuration
3. Код останавливается на breakpoint
4. MCP читает значения переменных из debugger
5. Возвращает агенту: `{"user_id": 123, "amount": -50, "payment_method": "card"}`

**Результат**: Агент видит, что `amount` отрицательный (баг!), и предлагает добавить валидацию.

#### Установка

MCP Server **встроен** в JetBrains IDE начиная с версии 2025.2+. Нужно только включить:

1. Открыть IDE (PyCharm/IntelliJ/WebStorm)
2. Settings → Tools → Model Context Protocol
3. Enable MCP Server
4. Порт по умолчанию: `localhost:8765`

#### Конфигурация (Claude Code)

`~/.claude/mcp.json`:
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

**Поддерживаемые IDE:**
- PyCharm (Python)
- IntelliJ IDEA (Java, Kotlin)
- WebStorm (JavaScript, TypeScript)
- Android Studio (Android)
- Rider (.NET)
- GoLand (Go)

**Зрелость**: ⭐⭐⭐⭐⭐ (Official JetBrains implementation)

**Ссылки**:
- GitHub: https://github.com/JetBrains/mcp-jetbrains
- Документация: https://www.jetbrains.com/help/pycharm/mcp-server.html

---

### 4.4. Figma MCP Server

**Назначение**: Интеграция с Figma Dev Mode — AI видит структуру дизайна (слои, auto-layout, variants, tokens) и генерирует код, соответствующий реальному дизайну.

#### Что дает Figma MCP

Традиционный design-to-code workflow:
1. Дизайнер создает дизайн в Figma
2. Разработчик смотрит на дизайн (или screenshot)
3. Разработчик **вручную** переводит дизайн в код (приблизительно)
4. Дизайнер проверяет → несоответствия → правки

Проблемы:
- Spacing/colors/typography **не точные** (8px вместо 12px, #333 вместо #2C2C2C)
- Долго (часы на верстку компонента)
- Ошибки (забыл hover state, responsive breakpoints)

**С Figma MCP:**
1. Дизайнер создает дизайн в Figma
2. AI **читает структуру** через MCP (не screenshot, а structured data!)
3. AI генерирует код с **точными** значениями из design tokens
4. Код соответствует дизайну на 100%

**Основные возможности:**
- **Чтение структуры слоев**: Hierarchy, names, properties
- **Design tokens**: Colors, typography, spacing, shadows
- **Auto-layout**: Flexbox/Grid параметры
- **Components & Variants**: Component sets, properties
- **Export assets**: Icons, images, SVG
- **Code generation**: React/Vue/HTML с точными стилями

#### Когда использовать

- **Design system implementation**: Генерация компонентов из Figma
- **Frontend development**: Верстка по дизайну
- **Design tokens extraction**: Создание CSS variables/Tailwind config
- **Component library**: Синхронизация дизайна с кодом

#### Пример задачи

**Сценарий**: Дизайнер создал компонент "UserCard" в Figma. Нужно сгенерировать React компонент.

**Команда для агента:**
```
Claude, подключись к Figma файлу "Mobile App Design", найди компонент
"UserCard", и сгенерируй React компонент с точными стилями из design tokens.
```

**Что делает Figma MCP:**
1. Читает Figma файл через Dev Mode API
2. Находит компонент "UserCard"
3. Извлекает структуру:
   ```json
   {
     "type": "FRAME",
     "children": [
       {"type": "IMAGE", "name": "Avatar", "width": 48, "height": 48, "borderRadius": 24},
       {"type": "TEXT", "name": "Name", "fontSize": 16, "fontWeight": 600, "color": "#2C2C2C"},
       {"type": "TEXT", "name": "Role", "fontSize": 14, "fontWeight": 400, "color": "#666666"}
     ],
     "layout": {"mode": "HORIZONTAL", "gap": 12, "padding": 16}
   }
   ```
4. Извлекает design tokens
5. Возвращает агенту

**Результат**: Агент генерирует React компонент:
```jsx
export const UserCard = ({ avatar, name, role }) => (
  <div style={{
    display: 'flex',
    gap: '12px',
    padding: '16px'
  }}>
    <img
      src={avatar}
      alt={name}
      style={{
        width: '48px',
        height: '48px',
        borderRadius: '24px'
      }}
    />
    <div>
      <h3 style={{
        fontSize: '16px',
        fontWeight: 600,
        color: '#2C2C2C',
        margin: 0
      }}>
        {name}
      </h3>
      <p style={{
        fontSize: '14px',
        fontWeight: 400,
        color: '#666666',
        margin: 0
      }}>
        {role}
      </p>
    </div>
  </div>
);
```

**100% соответствие дизайну** — spacing, colors, typography взяты из Figma.

#### Установка

```bash
npm install -g @glips/figma-context-mcp
```

#### Конфигурация

`~/.claude/mcp.json`:
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

**Получение токена**: Figma → Settings → Personal Access Tokens

**Зрелость**: ⭐⭐⭐⭐ (Community-driven, активно развивается)

**Ссылки**:
- GitHub: https://github.com/GLips/Figma-Context-MCP
- Figma Guide: https://help.figma.com/hc/en-us/articles/32132100833559-Guide-to-the-Figma-MCP-server

---

## 5. Установка и настройка

### 5.1. Глобальная установка через npm

Рекомендуется устанавливать MCP-серверы **глобально**, чтобы они были доступны из любого проекта.

#### Обязательные серверы для курса

```bash
# Git MCP
npm install -g @modelcontextprotocol/server-git

# Jira MCP
npm install -g @atlassian/atlassian-mcp-server

# Figma MCP
npm install -g @glips/figma-context-mcp
```

#### Дополнительные серверы (опционально)

```bash
# PostgreSQL MCP
npm install -g @modelcontextprotocol/server-postgres

# Puppeteer MCP
npm install -g @modelcontextprotocol/server-puppeteer

# Mermaid MCP
npm install -g mermaid-mcp-server
```

**Примечание**: JetBrains MCP Server встроен в IDE (версия 2025.2+), отдельная установка не требуется.

### 5.2. Конфигурация для Claude Code

Создайте файл `~/.claude/mcp.json` (или отредактируйте существующий):

```json
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
        "ATLASSIAN_SITE": "your-domain.atlassian.net",
        "ATLASSIAN_EMAIL": "your-email@example.com",
        "ATLASSIAN_API_TOKEN": "your-api-token"
      }
    },
    "pycharm": {
      "command": "jetbrains-mcp-client",
      "args": ["--host", "localhost", "--port", "8765"],
      "env": {
        "IDE": "pycharm"
      }
    },
    "figma": {
      "command": "npx",
      "args": ["-y", "@glips/figma-context-mcp"],
      "env": {
        "FIGMA_ACCESS_TOKEN": "your-figma-token"
      }
    },
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

**Важно:**
- Замените `your-domain.atlassian.net`, `your-email@example.com`, `your-api-token` на реальные значения
- Замените `your-figma-token` на токен из Figma
- Для PostgreSQL используйте реальный connection string

### 5.3. Конфигурация для Cursor

В Cursor MCP-серверы настраиваются в `.cursor/mcp.json` (в корне проекта или глобально).

**Создайте `.cursor/mcp.json`:**

```json
{
  "mcpServers": {
    "git": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-git"]
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

**Альтернатива**: Cursor также поддерживает GUI для добавления MCP-серверов:
1. Settings → MCP
2. Add Server
3. Выбрать сервер из каталога или указать custom

### 5.4. Проверка работоспособности

#### Claude Code

```bash
# Запустите Claude Code с вопросом о MCP
claude -p "List available MCP servers and their tools"
```

**Ожидаемый результат**: Агент покажет список подключенных серверов и их tools.

#### Cursor

1. Откройте Cursor
2. Settings → MCP → View Connected Servers
3. Проверьте, что серверы в статусе "Connected"

#### Отладка

Если сервер не подключается:

1. **Проверьте логи**:
   ```bash
   # Claude Code логи
   tail -f ~/.claude/logs/mcp.log
   ```

2. **Запустите сервер вручную**:
   ```bash
   npx @modelcontextprotocol/server-git
   # Должен запуститься без ошибок
   ```

3. **Проверьте environment variables**:
   ```bash
   echo $ATLASSIAN_API_TOKEN
   # Должен вывести токен (если настроен глобально)
   ```

---

## 6. Расширенные MCP-серверы (обзор)

Помимо обязательных 4 серверов, существуют сотни других MCP-серверов для различных use cases.

### 6.1. PostgreSQL MCP Server

**Use case**: Работа с PostgreSQL через natural language — запросы, анализ схемы, миграции.

**Что дает:**
- Natural language SQL queries: "Покажи всех пользователей, зарегистрированных за последнюю неделю"
- Schema analysis: Анализ структуры таблиц, индексов, foreign keys
- Query optimization: Предложения по оптимизации медленных запросов
- Migrations: Генерация SQL-миграций на основе описания изменений

**Пример:**
```
Claude, покажи все заказы со статусом "pending" дольше 24 часов

→ PostgreSQL MCP:
SELECT * FROM orders
WHERE status = 'pending'
AND created_at < NOW() - INTERVAL '24 hours'
```

**Установка**: `npm install -g @modelcontextprotocol/server-postgres`

**Конфигурация**: Требует `POSTGRES_CONNECTION_STRING` в env.

---

### 6.2. Puppeteer MCP Server

**Use case**: Web automation — навигация, заполнение форм, screenshots, E2E тестирование.

**Что дает:**
- Навигация по сайтам
- Заполнение и submit форм
- Клики, scroll, hover
- Screenshots и PDF generation
- E2E test scenarios

**Пример:**
```
Claude, открой staging.example.com, залогинься с тестовым пользователем
(test@example.com / password123), и сделай screenshot дашборда
```

**Установка**: `npm install -g @modelcontextprotocol/server-puppeteer`

---

### 6.3. Mermaid MCP Server

**Use case**: Генерация диаграмм Mermaid (flowcharts, sequence diagrams, ER diagrams, architecture diagrams).

**Что дает:**
- Конвертация Mermaid syntax в PNG/SVG
- Валидация Mermaid syntax
- Рендеринг через headless browser
- Поддержка всех типов диаграмм

**Пример:**
```
Claude, создай sequence diagram для OAuth2 authentication flow

→ Mermaid MCP генерирует:
sequenceDiagram
    User->>App: Request Login
    App->>OAuth: Redirect to OAuth
    OAuth->>User: Show Login Form
    User->>OAuth: Enter Credentials
    OAuth->>App: Return Auth Code
    App->>OAuth: Exchange Code for Token
    OAuth->>App: Return Access Token
```

**Установка**: `npm install -g mermaid-mcp-server`

---

### 6.4. Miro MCP Server

**Use case**: Whiteboarding, создание диаграмм на Miro boards прямо из кода.

**Что дает:**
- Создание Miro boards
- Добавление shapes, connectors, text
- Экспорт в различные форматы
- Collaborative brainstorming

**Пример:**
```
Claude, создай Miro board с архитектурой микросервисов для нашего проекта
```

**Установка**: `npm install -g @k-jarzyna/mcp-miro`

---

### 6.5. Obsidian MCP Server

**Use case**: Работа с Obsidian vault — notes, links, knowledge graphs.

**Что дает:**
- Чтение и создание заметок
- Навигация по ссылкам
- Поиск по vault
- Анализ knowledge graph

**Пример:**
```
Claude, найди все заметки в Obsidian, связанные с "authentication",
и создай summary документ
```

**Установка**: `npm install -g mcp-obsidian`

---

### 6.6. PowerPoint MCP Server

**Use case**: Создание и редактирование PowerPoint презентаций.

**Что дает:**
- Генерация слайдов из текста
- Добавление диаграмм, images
- Форматирование и стилизация
- Экспорт в PDF

**Пример:**
```
Claude, создай PowerPoint презентацию на тему "MCP Architecture"
с 5 слайдами: введение, архитектура, примеры, установка, заключение
```

**Установка**: `npm install -g office-powerpoint-mcp-server`

---

## 7. Создание своего MCP-сервера

### 7.1. Когда это нужно

Создавайте собственный MCP-сервер, если:
- Нужна интеграция с **internal tools** вашей компании
- Используете **proprietary APIs**, для которых нет готового сервера
- Работаете с **legacy systems**
- Хотите создать **custom workflow** для команды

**Примеры:**
- Internal ticketing system
- Company-specific databases
- Proprietary deployment tools
- Custom analytics platforms

### 7.2. SDK: @modelcontextprotocol/sdk

Anthropic предоставляет официальный SDK для создания MCP-серверов на TypeScript/JavaScript.

**Установка:**
```bash
npm install @modelcontextprotocol/sdk
```

### 7.3. Минимальный пример (10 строк кода)

```typescript
import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';

const server = new Server({
  name: 'weather-server',
  version: '1.0.0',
});

// Регистрируем список tools
server.setRequestHandler('tools/list', async () => ({
  tools: [
    {
      name: 'get_weather',
      description: 'Get current weather for a city',
      inputSchema: {
        type: 'object',
        properties: {
          city: { type: 'string', description: 'City name' }
        },
        required: ['city']
      }
    }
  ]
}));

// Обрабатываем вызовы tools
server.setRequestHandler('tools/call', async (request) => {
  if (request.params.name === 'get_weather') {
    const { city } = request.params.arguments;

    // Здесь можно вызвать реальный weather API
    const weather = `Sunny, 22°C in ${city}`;

    return {
      content: [
        { type: 'text', text: weather }
      ]
    };
  }
});

// Запускаем сервер
const transport = new StdioServerTransport();
await server.connect(transport);
```

**Сохраните как `weather-server.js` и запустите:**
```bash
node weather-server.js
```

**Конфигурация в Claude Code:**
```json
{
  "mcpServers": {
    "weather": {
      "command": "node",
      "args": ["/path/to/weather-server.js"]
    }
  }
}
```

**Использование:**
```
Claude, what's the weather in London?
→ Sunny, 22°C in London
```

### 7.4. Структура production MCP-сервера

Реальный MCP-сервер обычно включает:

1. **Multiple tools**: Несколько endpoints (не один)
2. **Error handling**: Обработка ошибок API
3. **Authentication**: API keys, OAuth
4. **Caching**: Кэширование ответов
5. **Logging**: Логирование запросов
6. **Testing**: Unit и integration тесты

**Пример структуры проекта:**
```
my-mcp-server/
├── src/
│   ├── index.ts          # Entry point
│   ├── tools/            # Tool implementations
│   │   ├── search.ts
│   │   ├── create.ts
│   │   └── update.ts
│   ├── api/              # External API client
│   │   └── client.ts
│   └── utils/            # Helpers
│       └── cache.ts
├── tests/
│   └── tools.test.ts
├── package.json
└── tsconfig.json
```

**Документация**: https://github.com/modelcontextprotocol/sdk

---

## 8. Troubleshooting

### Проблема 1: MCP сервер не подключается

**Симптомы:**
```
❌ Failed to connect to MCP server 'filesystem'
Connection timeout after 30s
```

**Причины и решения:**

1. **Неправильный путь к серверу:**
   ```bash
   # Проверьте что путь существует
   which npx  # Должно показать /usr/local/bin/npx или подобное

   # Для filesystem сервера
   ls -la ~/.claude/mcp/servers/filesystem
   ```

2. **Node.js не установлен или старая версия:**
   ```bash
   node --version  # Должно быть ≥18.0.0
   npm install -g npx  # Если npx не найден
   ```

3. **Права доступа:**
   ```bash
   chmod +x ~/.claude/mcp/servers/filesystem/index.js
   ```

4. **Проверка логов:**
   ```bash
   # Claude Code показывает логи MCP
   # Ищите строки с [MCP] в выводе
   ```

---

### Проблема 2: Environment variables не работают

**Симптомы:**
```typescript
// Сервер не видит GITHUB_TOKEN
Error: Missing required environment variable: GITHUB_TOKEN
```

**Решения:**

1. **Проверьте синтаксис в claude.json:**
   ```json
   {
     "mcpServers": {
       "github": {
         "command": "npx",
         "args": ["-y", "@modelcontextprotocol/server-github"],
         "env": {
           "GITHUB_TOKEN": "${GITHUB_TOKEN}"  // ✅ Правильно
         }
       }
     }
   }
   ```

2. **Установите переменные в shell:**
   ```bash
   # Добавьте в ~/.bashrc или ~/.zshrc
   export GITHUB_TOKEN="ghp_your_token_here"

   # Перезапустите shell или:
   source ~/.bashrc
   ```

3. **Альтернатива: .env файл:**
   ```bash
   # ~/.claude/.env
   GITHUB_TOKEN=ghp_your_token_here

   # claude.json с dotenv сервером
   {
     "mcpServers": {
       "dotenv": {
         "command": "npx",
         "args": ["-y", "@modelcontextprotocol/server-dotenv"]
       }
     }
   }
   ```

---

### Проблема 3: Производительность деградирует

**Симптомы:**
- Claude Code тормозит при большом количестве MCP серверов
- Timeout при вызове инструментов
- Высокое использование памяти

**Решения:**

1. **Оптимизируйте количество серверов:**
   ```json
   // ❌ Плохо: 10+ серверов одновременно
   // ✅ Хорошо: 3-5 активных серверов

   // Используйте проекто-специфичные конфиги
   // ~/projects/web-app/.claude/claude.json
   {
     "mcpServers": {
       "filesystem": { /* только для web проектов */ }
     }
   }
   ```

2. **Кэшируйте результаты:**
   ```typescript
   // В вашем MCP сервере
   const cache = new Map();

   server.setRequestHandler(ListToolsRequestSchema, async () => {
     if (cache.has('tools')) {
       return cache.get('tools');  // Не пересчитываем каждый раз
     }
     const tools = await loadTools();
     cache.set('tools', tools);
     return tools;
   });
   ```

3. **Lazy loading:**
   ```json
   // Запускайте тяжёлые серверы по требованию
   {
     "mcpServers": {
       "database": {
         "command": "npx",
         "args": ["-y", "@modelcontextprotocol/server-postgres"],
         "autoStart": false  // Запустится при первом вызове
       }
     }
   }
   ```

---

### Проблема 4: Конфликты между серверами

**Симптомы:**
```
Error: Tool 'read_file' is provided by multiple servers:
- filesystem
- custom-reader
```

**Решения:**

1. **Именуйте инструменты уникально:**
   ```typescript
   // ❌ Плохо
   { name: "read_file" }

   // ✅ Хорошо
   { name: "custom_reader_read_file" }
   ```

2. **Используйте namespaces:**
   ```typescript
   server.setRequestHandler(ListToolsRequestSchema, async () => ({
     tools: [{
       name: "myserver/read_file",  // Префикс = namespace
       description: "...",
       inputSchema: { /* ... */ }
     }]
   }));
   ```

3. **Отключите ненужные серверы:**
   ```json
   {
     "mcpServers": {
       "filesystem": { "enabled": true },
       "custom-reader": { "enabled": false }  // Временно выключен
     }
   }
   ```

---

### Проблема 5: JetBrains IDE не видит MCP

**Симптомы:**
- В VS Code MCP работает
- В JetBrains (IntelliJ, WebStorm) инструменты не появляются

**Решения:**

1. **Проверьте поддержку MCP в вашей IDE:**
   ```bash
   # MCP поддерживается в:
   # - JetBrains AI Assistant 2024.3+
   # - IntelliJ IDEA 2024.3+
   # - WebStorm 2024.3+

   # Обновите IDE до последней версии
   ```

2. **Конфигурация для JetBrains:**
   ```json
   // ~/.config/JetBrains/IntelliJIdea2024.3/options/mcp.json
   {
     "mcpServers": {
       "filesystem": {
         "command": "npx",
         "args": ["-y", "@modelcontextprotocol/server-filesystem", "/path/to/allowed/dir"]
       }
     }
   }
   ```

3. **Перезапустите AI Assistant:**
   ```
   Tools → AI Assistant → Settings → Reset AI Assistant
   ```

4. **Альтернатива: используйте Claude Code CLI:**
   ```bash
   # В JetBrains Terminal
   claude "analyze this codebase using MCP"
   ```

---

### Общие советы по отладке

1. **Проверьте версии:**
   ```bash
   claude --version  # ≥1.0.0
   node --version    # ≥18.0.0
   npx --version     # должен работать
   ```

2. **Посмотрите логи:**
   ```bash
   # Claude Code логи
   tail -f ~/.claude/logs/mcp.log

   # Или запустите с дебагом
   DEBUG=mcp:* claude
   ```

3. **Минимальный тест:**
   ```bash
   # Проверьте что базовый сервер работает
   npx -y @modelcontextprotocol/server-filesystem /tmp

   # Должно запуститься без ошибок
   ```

4. **Community:**
   - [MCP Discord](https://discord.gg/modelcontextprotocol)
   - [GitHub Issues](https://github.com/modelcontextprotocol/servers/issues)
   - [Stack Overflow #mcp](https://stackoverflow.com/questions/tagged/mcp)

---

## Связь с практикой (Модуль 6 Practice)

В практической части модуля 6 вы будете:

1. **Установите и настроите** все 4 обязательных MCP-сервера
2. **Code archaeology**: Используйте Git MCP для анализа истории legacy проекта
3. **Task-driven development**: Реализуйте задачу из Jira с автоматическим логированием времени
4. **Design-to-code**: Сгенерируете React компонент из Figma дизайна с точными стилями
5. **Debugging**: Используйте JetBrains MCP для отладки сложного бага с breakpoints
6. **Bonus**: Создадите собственный простой MCP-сервер для internal tool

**Если возникнут проблемы**: см. секцию "8. Troubleshooting" выше.

**Цель**: К концу модуля вы будете владеть MCP на уровне, достаточном для реальной enterprise-разработки.

---

## Итоги

**Что вы узнали:**

1. **MCP — это универсальный протокол** для подключения AI-агентов к инструментам
2. **Архитектура MCP**: Client-Server модель на базе JSON-RPC
3. **4 ключевых сервера**: Git (code archaeology), Jira (task tracking), JetBrains (debugging/refactoring), Figma (design-to-code)
4. **Установка и настройка**: npm + конфигурация в `~/.claude/mcp.json`
5. **Расширенные серверы**: PostgreSQL, Puppeteer, Mermaid, Miro, Obsidian, PowerPoint
6. **Создание своих серверов**: SDK от Anthropic для custom integrations

**Следующие шаги:**

1. Установите обязательные MCP-серверы на своей машине
2. Настройте конфигурацию для Claude Code или Cursor
3. Протестируйте каждый сервер с простыми запросами
4. Переходите к практической части модуля 6

**MCP превращает AI-агента из простого code editor в полноценного члена команды**, интегрированного со всеми инструментами и процессами разработки.

---

## Источники

### Официальные ресурсы
- [Model Context Protocol](https://modelcontextprotocol.io)
- [MCP Specification 2025-11-25](https://modelcontextprotocol.io/specification/2025-11-25)
- [Official MCP Servers](https://github.com/modelcontextprotocol/servers)
- [MCP SDK Documentation](https://github.com/modelcontextprotocol/sdk)

### Каталоги серверов
- [Awesome MCP Servers (1200+)](https://mcp-awesome.com/)
- [AI Agents List MCP Servers (593+)](https://aiagentslist.com/mcp-servers)
- [MCP Catalog](https://mcp-catalog.com/)

### Документация серверов
- [Git MCP](https://github.com/modelcontextprotocol/servers/tree/main/src/git)
- [Atlassian MCP](https://github.com/atlassian/atlassian-mcp-server)
- [Atlassian MCP Docs](https://support.atlassian.com/atlassian-rovo-mcp-server/docs/getting-started-with-the-atlassian-remote-mcp-server/)
- [JetBrains MCP](https://github.com/JetBrains/mcp-jetbrains)
- [PyCharm MCP Guide](https://www.jetbrains.com/help/pycharm/mcp-server.html)
- [Figma MCP](https://github.com/GLips/Figma-Context-MCP)
- [Figma MCP Guide](https://help.figma.com/hc/en-us/articles/32132100833559-Guide-to-the-Figma-MCP-server)

### Статьи и обзоры
- [Top 10 Best MCP Servers (2026)](https://cybersecuritynews.com/best-model-context-protocol-mcp-servers/)
- [Best MCP Servers for Developers](https://www.builder.io/blog/best-mcp-servers-2026)
- [Top 10 Essential MCP Servers](https://apidog.com/blog/top-10-mcp-servers-for-claude-code/)
