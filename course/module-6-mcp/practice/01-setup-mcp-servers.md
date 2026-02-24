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

### Шаг 2: Конфигурация (10 мин)

Создайте файл `.mcp.json` в корне проекта (или `~/.claude/mcp.json` для глобальной конфигурации):

```json
{
  "mcpServers": {
    "git": {
      "command": "npx",
      "args": ["@modelcontextprotocol/server-git"]
    }
  }
}
```

Для добавления других серверов расширяйте секцию `mcpServers`:

```json
{
  "mcpServers": {
    "git": {
      "command": "npx",
      "args": ["@modelcontextprotocol/server-git"]
    },
    "github": {
      "command": "npx",
      "args": ["@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_TOKEN": "your-token-here"
      }
    }
  }
}
```

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

> [!NOTE]
> Если у вас нет доступа к Jira/Figma — пропустите эти задания. Git MCP и PostgreSQL MCP доступны бесплатно и достаточны для освоения концепции.

---

### Troubleshooting

**Сервер не найден:**
```
Error: MCP server "git" not found
```
Решение: проверьте, что `npx` доступен в PATH и пакет установлен: `npx @modelcontextprotocol/server-git --help`

**Переменная окружения не задана:**
```
Error: GITHUB_TOKEN is not set
```
Решение: убедитесь, что переменная указана в секции `env` в `.mcp.json`, либо экспортирована в вашем shell: `export GITHUB_TOKEN=ghp_...`

**Несовместимость версий:**
```
Error: Unsupported protocol version
```
Решение: обновите сервер до последней версии: `npm update -g @modelcontextprotocol/server-git`. Убедитесь, что версия Claude Code тоже актуальна: `claude update`
