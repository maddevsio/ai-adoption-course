# Настройка MCP-серверов

### Чек-лист готовности

- [ ] Claude Code установлен (Модуль 2)
- [ ] Node.js 18+ установлен (`node --version`)
- [ ] Git репозиторий с проектом готов

---

### Шаг 1: Установка серверов (10 мин)

Установите серверы по инструкциям из официальных README:

| Сервер | README |
|--------|--------|
| GitHub MCP | [github.com/modelcontextprotocol/servers/.../github](https://github.com/modelcontextprotocol/servers/tree/main/src/github) |
| Jira MCP | [github.com/atlassian/atlassian-mcp-server](https://github.com/atlassian/atlassian-mcp-server) |
| Figma MCP | [github.com/GLips/Figma-Context-MCP](https://github.com/GLips/Figma-Context-MCP) |
| JetBrains | Встроен в IDE 2025.2+ · [docs](https://www.jetbrains.com/help/pycharm/mcp-server.html) |

Конфигурация Claude Code MCP: [docs.anthropic.com](https://docs.anthropic.com/en/docs/claude-code/mcp)

---

### Шаг 3: Проверка работоспособности (10 мин)

```
List all available MCP tools
```

Агент должен показать список инструментов от MCP-серверов (filesystem_read, github, и т.д.).

---

### Шаг 4: Практическая задача (5 мин)

> [!NOTE]
> Задача "Покажи список открытых PR" работает и без MCP — через `gh` CLI. Цель упражнений ниже — проверить что MCP-серверы отвечают и агент может ими пользоваться.

```bash
"Покажи список моих задач в Jira"
```

```bash
"Создай на меня задачу в Jira `Настроить MCP`, опиши прогресс в комментарии, залогай время, закрой задачу"
```

```bash
"Открой Figma-файл проекта и перечисли все компоненты на странице Design System"
```
