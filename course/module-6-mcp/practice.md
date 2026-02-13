# Практика: Настройка MCP

> Установка и базовая настройка MCP-серверов для работы с внешними инструментами

**Время выполнения:** 30 минут (10 мин установка + 5 мин конфигурация + 10 мин проверка + 5 мин практика)

**Цель:** Установить минимальный набор MCP-серверов и выполнить базовую задачу с их использованием.

## Чек-лист готовности

- [ ] Claude Code установлен (Модуль 2)
- [ ] Node.js 18+ установлен (`node --version`)
- [ ] Git репозиторий с проектом готов
- [ ] Есть 30 минут для упражнений

---

## Шаг 1: Установка обязательных серверов (10 мин)

Установите минимальный набор для работы:

```bash
# 1. Filesystem MCP
npm install -g @modelcontextprotocol/server-filesystem

# 2. GitHub MCP
npm install -g @modelcontextprotocol/server-github

# Настройка GitHub Token
export GITHUB_TOKEN="ваш_токен"  # Получить: github.com/settings/tokens
source ~/.bashrc
```

**Опционально:**
- **Git MCP**: `npm install -g @mseep/git-mcp-server`
- **Figma MCP**: `npm install -g figma-developer-mcp` (для design-to-code)
- **JetBrains IDE 2025.2+**: встроенная поддержка MCP (Settings → Tools → MCP)

---

## Шаг 2: Конфигурация mcp.json (5 мин)

Создайте файл `~/.claude/mcp.json`:

```bash
mkdir -p ~/.claude
cat > ~/.claude/mcp.json << 'EOF'
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/path/to/your/project"]
    },
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_TOKEN": "${GITHUB_TOKEN}"
      }
    }
  }
}
EOF
```

**Замените** `/path/to/your/project` на реальный путь (например, `~/practice/task-manager`).

**Проверка:**
```bash
# Валидировать JSON
python3 -m json.tool ~/.claude/mcp.json

# Перезапустить Claude Code
claude
```

---

## Шаг 3: Проверка работоспособности (10 мин)

**Перезапустите Claude Code и проверьте MCP:**

```bash
cd ~/practice/task-manager
claude
```

**В интерактивном режиме:**
```
List all available MCP tools
```

**Ожидаемый результат:** Агент покажет список инструментов от MCP-серверов (filesystem_read, github_issues_list, и т.д.).

**Если агент не видит MCP-серверы** — см. секцию Troubleshooting ниже.

---

## Шаг 4: Практическая задача (5 мин)

**Быстрая проверка интеграции:**

```bash
claude -p "Прочитай файл README.md из проекта и покажи его структуру (заголовки)"
```

Агент должен использовать filesystem MCP для чтения файла.

**Для тех, у кого настроен GitHub MCP:**

```bash
# Создайте тестовый issue в вашем репозитории
# Затем запустите:
claude -p "Покажи список открытых issues в репозитории"
```

Агент должен использовать GitHub MCP для получения списка.

---

## Следующие шаги

После базовой настройки MCP вы можете:

1. **Изучить дополнительные серверы** — см. Приложение ниже
2. **Использовать MCP в Модуле 7** — headless workflows и CI/CD интеграция
3. **Настроить ограничения** — Модуль 8 (контроль и безопасность)

---

## Troubleshooting (3 частые проблемы)

### 1. MCP-сервер не подключается

**Симптомы:** `Error: Failed to connect to MCP server`

**Решение:**
```bash
# Проверить что сервер установлен
npx @modelcontextprotocol/server-github --version

# Проверить Node.js версию (нужна 18+)
node --version

# Перезапустить Claude Code
claude
```

---

### 2. Environment variables не работают

**Симптомы:** `Error: Missing required environment variable`

**Решение:**
```bash
# Проверить что переменная установлена
echo $GITHUB_TOKEN

# Если пусто — добавить в ~/.bashrc
echo 'export GITHUB_TOKEN="your_token"' >> ~/.bashrc
source ~/.bashrc

# Проверить синтаксис в mcp.json (должно быть ${VAR_NAME})
cat ~/.claude/mcp.json | grep GITHUB_TOKEN
```

---

### 3. Агент не видит MCP-инструменты

**Симптомы:** Агент отвечает "I don't have access to MCP tools"

**Решение:**
```bash
# Проверить что mcp.json существует
ls -la ~/.claude/mcp.json

# Проверить JSON синтаксис
python3 -m json.tool ~/.claude/mcp.json

# Перезапустить Claude Code
claude
```

---

## Чеклист выполнения

- [ ] Установлены минимум 2 MCP-сервера (filesystem + github)
- [ ] Файл `~/.claude/mcp.json` создан и валиден
- [ ] Environment variables настроены (`echo $GITHUB_TOKEN`)
- [ ] Claude Code видит MCP-серверы (`claude -p "List MCP tools"`)
- [ ] Выполнена базовая проверка работы

---

## Приложение: Дополнительные серверы

**Данные:** PostgreSQL, MongoDB
**Автоматизация:** Puppeteer (E2E), BrowserStack (кросс-браузерность)
**Документация:** Mermaid (диаграммы), Obsidian (knowledge base), PowerPoint
**Коллаборация:** Miro (whiteboard)

**Каталог:** https://mcp-awesome.com/ (1200+ серверов)

**Безопасность:** Используйте переменные окружения: `"env": { "TOKEN": "${TOKEN}" }`

---

**Время выполнения:** 30 минут

**Следующий модуль:** Модуль 7 — Оркестрация агентов
