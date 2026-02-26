[← Оглавление](../../../README.md)

## 5. Установка и настройка

Установка и конфигурация каждого сервера описана в его README. Ниже — ссылки и общий принцип.

### 5.1. Обязательные серверы

- **Git MCP** — [README](https://github.com/modelcontextprotocol/servers/tree/main/src/git#installation)
- **Jira MCP (Atlassian)** — [README](https://github.com/atlassian/atlassian-mcp-server). Токен можно создать в настройках Atlassian
- **JetBrains MCP** — встроен в IDE 2025.2+. [Docs](https://www.jetbrains.com/help/pycharm/mcp-server.html)
- **Figma MCP** — [README](https://github.com/GLips/Figma-Context-MCP). Токен: Figma → Settings → Personal Access Tokens

### 5.2. Конфигурация

MCP-серверы настраиваются в JSON-файле:

| Инструмент | Файл конфигурации |
|------------|-------------------|
| Claude Code | `~/.claude/mcp.json` · [docs](https://docs.anthropic.com/en/docs/claude-code/mcp) |
| Cursor | `.cursor/mcp.json` (проект или глобально) · Settings → MCP → Add Server |

Формат одинаковый — объект `mcpServers`. Каждый ключ описывает сервер: `command`, `args`, `env` (для токенов и credentials).

### 5.3. Проверка работоспособности

```bash
# Проверить что агент видит MCP-серверы
claude -p "List available MCP servers and their tools"
```

Если сервер не подключается:

```bash
# Проверить версии
node --version    # ≥18.0.0
npx --version     # должен работать

# Запустить сервер вручную (должен запуститься без ошибок)
npx @modelcontextprotocol/server-git

# Проверить environment variables
echo $ATLASSIAN_API_TOKEN
```

**Community:** [MCP Discord](https://discord.gg/modelcontextprotocol) · [GitHub Issues](https://github.com/modelcontextprotocol/servers/issues)
---

[← 3. Категории MCP-серверов](02-mcp-servers.md) | [Оглавление](../../../README.md) | [6. Создание своего MCP-сервера →](04-custom-servers.md)
