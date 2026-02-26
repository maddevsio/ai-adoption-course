[← Оглавление](../../../README.md)

## 3. Категории MCP-серверов

> [Диаграмма: Карта MCP-серверов по приоритету](../diagrams/mcp-server-priorities.md)

Каталоги: 
- [mcp-awesome.com](https://mcp-awesome.com/) (1200+ серверов) 
- [aiagentslist.com/mcp-servers](https://aiagentslist.com/mcp-servers)


### 3.1. Development Tools

| Сервер | Что дает | Примеры |
|--------|----------|---------|
| **Git MCP** | Code archaeology, анализ истории | `git log --grep`, `git blame`, `git bisect` |
| **GitHub MCP** | Issues, PRs, Code Reviews | Создание PR, управление issues |
| **JetBrains MCP** | Debugger, refactoring, navigation | Breakpoints, rename refactoring |
| **Docker MCP** | Контейнеры, образы, сети | Запуск контейнера, логи |

### 3.2. Data Sources

| Сервер | Что дает | Примеры |
|--------|----------|---------|
| **PostgreSQL MCP** | Natural language SQL, анализ схемы | Запросы на естественном языке |
| **MySQL MCP** | Аналогично для MySQL | Миграции, оптимизация |
| **MongoDB MCP** | NoSQL queries, aggregations | Aggregation pipelines |

### 3.3. External Services

| Сервер | Что дает | Примеры |
|--------|----------|---------|
| **Jira MCP** | Tasks, worklogs, sprints | Логирование времени, статусы |
| **Slack MCP** | Messaging, channels | Уведомления, чтение сообщений |
| **Figma MCP** | Design structure, tokens | Design-to-code, design tokens |
| **Notion MCP** | Pages, databases | Документация, knowledge base |

### 3.4. Utilities

| Сервер | Что дает | Примеры |
|--------|----------|---------|
| **Puppeteer MCP** | Web automation, screenshots | E2E тесты, UI тестирование |
| **Mermaid MCP** | Диаграммы (flowcharts, ER) | Визуализация архитектуры |

---

## 4. Обязательные MCP-серверы для курса

### 4.1. Git MCP Server

Git MCP: анализ истории и code archaeology, не только commit/push.

**Возможности:** code archaeology (кто, когда, почему изменил код), поиск в истории (`git log -S`), анализ веток, blame analysis, bisect.

**Когда использовать:** legacy code, bug investigation, code review, рефакторинг.

**Пример:** "Найди все коммиты, которые изменяли функцию `calculate_discount` за последние 3 месяца" → Git MCP выполняет `git log -S`, показывает diff и commit messages.

[GitHub](https://github.com/modelcontextprotocol/servers/tree/main/src/git) (Official Anthropic)

### 4.2. Jira MCP Server (Atlassian)

Интеграция с Jira: чтение задач, логирование времени, обновление статусов.

**Возможности:** JQL queries, чтение задач (описание, acceptance criteria), worklogs, status transitions, комментарии.

**Когда использовать:** task-driven development, автоматическое логирование времени, обновление статусов.

**Пример:** "Прочитай задачу PROJ-456, реализуй её и залогируй время" → Jira MCP читает задачу, агент реализует, создает worklog, обновляет статус.

[GitHub](https://github.com/atlassian/atlassian-mcp-server) · [Документация](https://support.atlassian.com/atlassian-rovo-mcp-server/docs/getting-started-with-the-atlassian-remote-mcp-server/) (Official Atlassian)

### 4.3. JetBrains MCP Server

Интеграция с PyCharm, IntelliJ, WebStorm — debugger, refactoring, code analysis из AI-агента.

**Возможности:** breakpoints и step-through, rename/extract refactoring, find usages, запуск тестов через IDE runner.

**Когда использовать:** debugging сложных багов, безопасный рефакторинг, исследование незнакомого codebase.

**Пример:** "Поставь breakpoint на строке 67 в payment.py, запусти отладчик и покажи значения переменных" → JetBrains MCP устанавливает breakpoint, запускает debug, возвращает значения.

MCP Server **встроен** в JetBrains IDE 2025.2+: Settings → Tools → Model Context Protocol.

[GitHub](https://github.com/JetBrains/mcp-jetbrains) · [Документация](https://www.jetbrains.com/help/pycharm/mcp-server.html) (Official JetBrains)

### 4.4. Figma MCP Server

AI видит структуру дизайна (слои, auto-layout, variants, tokens) и генерирует код с точными стилями.

**Возможности:** чтение структуры слоев, design tokens (colors, typography, spacing), auto-layout → flexbox/grid, components и variants.

**Когда использовать:** генерация компонентов из Figma, верстка по дизайну, создание CSS variables / Tailwind config из design tokens.

**Пример:** "Найди компонент UserCard в Figma и сгенерируй React компонент" → Figma MCP читает structured data через Dev Mode API, извлекает tokens, агент генерирует код с точными стилями.

[Бесплатный Figma MCP](https://github.com/GLips/Figma-Context-MCP)
---

[← Модуль 6: Model Context Protocol (MCP)](01-what-is-mcp.md) | [Оглавление](../../../README.md) | [5. Установка и настройка →](03-setup-and-config.md)
