[← Оглавление](../../../README.md)

## 3. Категории MCP-серверов

> [Диаграмма: Карта MCP-серверов по приоритету](../diagrams/mcp-server-priorities.md)

Каталоги: 
- [mcp-awesome.com](https://mcp-awesome.com/) (1200+ серверов) 
- [aiagentslist.com/mcp-servers](https://aiagentslist.com/mcp-servers)


### 3.1. Development Tools

- **Git MCP** — code archaeology, анализ истории. `git log --grep`, `git blame`, `git bisect`
- **GitHub MCP** — Issues, PRs, Code Reviews. Создание PR, управление issues
- **JetBrains MCP** — debugger, refactoring, navigation. Breakpoints, rename refactoring
- **Docker MCP** — контейнеры, образы, сети. Запуск контейнера, логи

### 3.2. Data Sources

- **PostgreSQL MCP** — natural language SQL, анализ схемы. Запросы на естественном языке
- **MySQL MCP** — аналогично для MySQL. Миграции, оптимизация
- **MongoDB MCP** — NoSQL queries, aggregations. Aggregation pipelines

### 3.3. External Services

- **Jira MCP** — tasks, worklogs, sprints. Логирование времени, статусы
- **Slack MCP** — messaging, channels. Уведомления, чтение сообщений
- **Figma MCP** — design structure, tokens. Design-to-code, design tokens
- **Notion MCP** — pages, databases. Документация, knowledge base

### 3.4. Utilities

- **Puppeteer MCP** — web automation, screenshots. E2E тесты, UI тестирование
- **Mermaid MCP** — диаграммы (flowcharts, ER). Визуализация архитектуры

---

## 4. Обязательные MCP-серверы для курса

### 4.1. Git MCP Server

Git MCP дает анализ истории и code archaeology. Это не только commit/push.

**Возможности:**
- **Code archaeology** — кто, когда и почему изменил код
- **Поиск в истории** — `git log -S`, анализ веток
- **Blame analysis**, bisect

**Когда использовать:** legacy code, bug investigation, code review, рефакторинг.

**Пример:** "Найди все коммиты, которые изменяли функцию `calculate_discount` за последние 3 месяца." Git MCP выполняет `git log -S`, показывает diff и commit messages.

[GitHub](https://github.com/modelcontextprotocol/servers/tree/main/src/git) (Official Anthropic)

### 4.2. Jira MCP Server (Atlassian)

Интеграция с Jira: чтение задач, логирование времени, обновление статусов.

**Возможности:**
- **JQL queries** — поиск задач
- **Чтение задач** — описание, acceptance criteria
- **Worklogs**, status transitions, комментарии

**Когда использовать:** task-driven development, автоматическое логирование времени, обновление статусов.

**Пример:** "Прочитай задачу PROJ-456, реализуй её и залогируй время." Jira MCP читает задачу, агент реализует, создает worklog и обновляет статус.

[GitHub](https://github.com/atlassian/atlassian-mcp-server) · [Документация](https://support.atlassian.com/atlassian-rovo-mcp-server/docs/getting-started-with-the-atlassian-remote-mcp-server/) (Official Atlassian)

### 4.3. JetBrains MCP Server

Интеграция с PyCharm, IntelliJ, WebStorm. Дает debugger, refactoring и code analysis из AI-агента.

**Возможности:**
- **Breakpoints** и step-through
- **Rename/extract** refactoring, find usages
- **Запуск тестов** через IDE runner

**Когда использовать:** debugging сложных багов, безопасный рефакторинг, исследование незнакомого codebase.

**Пример:** "Поставь breakpoint на строке 67 в payment.py, запусти отладчик и покажи значения переменных." JetBrains MCP устанавливает breakpoint, запускает debug и возвращает значения.

MCP Server **встроен** в JetBrains IDE 2025.2+: Settings → Tools → Model Context Protocol.

[GitHub](https://github.com/JetBrains/mcp-jetbrains) · [Документация](https://www.jetbrains.com/help/pycharm/mcp-server.html) (Official JetBrains)

### 4.4. Figma MCP Server

AI видит структуру дизайна и генерирует код с точными стилями. Слои, auto-layout, variants, tokens — все доступно.

**Возможности:**
- **Чтение структуры слоев** и components/variants
- **Design tokens** — colors, typography, spacing
- **Auto-layout** → flexbox/grid

**Когда использовать:** генерация компонентов из Figma, верстка по дизайну, создание CSS variables / Tailwind config из design tokens.

**Пример:** "Найди компонент UserCard в Figma и сгенерируй React компонент." Figma MCP читает structured data через Dev Mode API, извлекает tokens. Агент генерирует код с точными стилями.

[Бесплатный Figma MCP](https://github.com/GLips/Figma-Context-MCP)
---

[← Модуль 6: Model Context Protocol (MCP)](01-what-is-mcp.md) | [Оглавление](../../../README.md) | [5. Установка и настройка →](03-setup-and-config.md)
