[← Оглавление](../../../README.md)

# Чеклист выполнения

## Что вы сделали

1. **Установили MCP-серверы** 
2. **Настроили конфигурацию** 
3. **Проверили работу** — агент видит MCP-серверы и может использовать их инструменты

## Проверьте себя

- [ ] Установлены минимум 2 MCP-сервера (github + jira)
- [ ] Файл `~/.claude/mcp.json` создан и валиден
- [ ] Environment variables настроены (`echo $GITHUB_TOKEN`)
- [ ] Claude Code видит MCP-серверы (`claude -p "List MCP tools"`)
- [ ] Выполнена базовая проверка работы

## Дополнительные серверы

- **Данные:** PostgreSQL, MongoDB
- **Автоматизация:** Puppeteer (E2E), BrowserStack
- **Документация:** Mermaid (диаграммы), Obsidian
- **Коллаборация:** Miro (whiteboard)

Каталог: [mcp-awesome.com](https://mcp-awesome.com/) (1200+ серверов)

**Безопасность:** Используйте переменные окружения для токенов: `"env": { "TOKEN": "${TOKEN}" }`
---

[← Настройка MCP-серверов](01-setup-mcp-servers.md) | [Оглавление](../../../README.md) | [Модуль 7: Параллельные агенты и оркестрация →](../../module-7-orchestration/theory/01-role-and-parallelism.md)
