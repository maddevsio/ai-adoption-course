## 5. Установка и настройка

Установка и конфигурация каждого сервера описана в его README. Ниже — ссылки и общий принцип.

### 5.1. Обязательные серверы

| Сервер | Установка                                                                                                |
|--------|----------------------------------------------------------------------------------------------------------|
| Git MCP | [README](https://github.com/modelcontextprotocol/servers/tree/main/src/git#installation)                 |
| Jira MCP (Atlassian) | [README](https://github.com/atlassian/atlassian-mcp-server) · токен можно создать в настройках Atlassian |
| JetBrains MCP | Встроен в IDE 2025.2+ · [docs](https://www.jetbrains.com/help/pycharm/mcp-server.html)                   |
| Figma MCP | [README](https://github.com/GLips/Figma-Context-MCP) · токен: Figma → Settings → Personal Access Tokens  |

### 5.2. Конфигурация

MCP-серверы настраиваются в JSON-файле:

| Инструмент | Файл конфигурации |
|------------|-------------------|
| Claude Code | `~/.claude/mcp.json` · [docs](https://docs.anthropic.com/en/docs/claude-code/mcp) |
| Cursor | `.cursor/mcp.json` (проект или глобально) · Settings → MCP → Add Server |

Формат одинаковый — объект `mcpServers`, где каждый ключ описывает сервер: `command`, `args`, `env` (для токенов и credentials).

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
