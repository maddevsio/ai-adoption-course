# Задача 01: Исследование инструментов и MCP-серверов

## Цель

Собрать актуальную фактуру по AI-инструментам и MCP-серверам для разработчиков.

## Что сделать

### Часть A: Инструменты

1. Для каждого инструмента собрать: текущая цена, ключевые фичи, статус, поддерживаемые модели.

2. Инструменты для исследования:
   - **IDE**: Cursor, Windsurf, Google Antigravity (https://antigravity.google/), GitHub Copilot (в VS Code и JetBrains)
   - **CLI-агенты**: Claude Code, Codex CLI (https://developers.openai.com/codex/cli/), Aider, OpenCode
   - **Чаты**: ChatGPT, Claude.ai, Gemini, DeepSeek (API/Chat, self-hosting)
   - **Бесплатные/дешёвые**: OpenCode (open-source), Claude guest pass, self-hosted Ollama, Kilo, Antigravity (бесплатно)
   - **Модели**: Claude Opus 4.6, Claude Sonnet 4.5, GPT-5.2, Gemini 3 Pro, open-source (DeepSeek, Qwen, Llama)

3. Для каждого: проверить официальный сайт, pricing page, changelog.

4. Сравнительная таблица: инструмент / категория / цена / модели / платформы / уровень зрелости.

5. **Мульти-модельная стратегия**: описать роли моделей:
   - Умные модели (Opus, GPT-5.2) → планирование, архитектура
   - Средние (Sonnet, GPT-4o) → планирование в цикле, ревью
   - Дешёвые/быстрые (Haiku, mini, open-source) → реализация мелких задач массово
   - Как разбить задачу на минимальные части и раздать дешёвым моделям

### Часть B+: Инфраструктура параллельной разработки

1. **Claude Code headless**: документация по `claude -p`, `--output-format json`, `--allowedTools`, `--max-turns`, `--resume`. Ссылка: https://code.claude.com/docs/en/headless
2. **Claude Code в облаке**: Docker (https://docs.docker.com/ai/sandboxes/claude-code/), EC2/VPS, Claude Code Remote (teleport).
3. **Auth-токены**:
   - `ANTHROPIC_API_KEY` — API-биллинг
   - `claude setup-token` — 1-годовой OAuth для подписчиков Max
   - Cloud backends: Bedrock (`CLAUDE_CODE_USE_BEDROCK=1`), Vertex AI, Azure Foundry
   - Docs: https://code.claude.com/docs/en/authentication
4. **Claude Agent SDK**: Python (`claude-agent-sdk`) и TypeScript (`@anthropic-ai/claude-agent-sdk`). GitHub: anthropics/claude-agent-sdk-python, anthropics/claude-agent-sdk-typescript. Docs: https://platform.claude.com/docs/en/agent-sdk/overview
5. **Agent Teams** (experimental): `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`. Shared task list, inter-agent messaging. Docs: https://code.claude.com/docs/en/agent-teams
6. **GitHub Actions**: `anthropics/claude-code-action@v1`. Docs: https://code.claude.com/docs/en/github-actions
7. **OpenClaw** (https://github.com/openclaw/openclaw): статус, архитектура, multi-agent routing, интеграция с Claude Code (openclaw-claude-code-skill, openclaw-mcp). Экосистема: Claworc, Antfarm, Claude Squad.
8. **Прочие оркестраторы**: claude-flow (https://github.com/ruvnet/claude-flow), Claude Squad (https://github.com/smtg-ai/claude-squad).

### Часть C: MCP-серверы

1. Исследовать текущий каталог MCP-серверов (modelcontextprotocol.io, github).
2. Исследовать конкретные серверы, отмеченные в контент-плане:
   - **Обязательные для курса**: git, jira (ворклоги), IDE (дебаггер PyCharm, окружение), Figma (https://github.com/GLips/Figma-Context-MCP)
   - **Расширенный список для обзора**:
     - mcp-mermaid (https://github.com/hustcc/mcp-mermaid)
     - mcp-miro (https://github.com/k-jarzyna/mcp-miro)
     - mcp-obsidian (https://github.com/MarkusPfundstein/mcp-obsidian)
     - browserstack-mcp
     - Office-PowerPoint-MCP-Server (https://github.com/GongRzhe/Office-PowerPoint-MCP-Server)
     - Puppeteer MCP Server (web automation)
     - PostgreSQL MCP Server (natural language DB queries)
3. Для каждого собрать: название, ссылка, что делает, способ установки, совместимость (Cursor / Claude Code / оба), уровень зрелости.

## Формат результата

- `research/tools-comparison.md` — таблица инструментов
- `research/parallel-dev-infra.md` — инфраструктура параллельной разработки (headless, auth, SDK, Agent Teams, OpenClaw)
- `research/mcp-servers.md` — каталог MCP-серверов с рекомендациями

## Критерии приёмки

- Все цены актуальны (проверены на официальных страницах)
- Нет устаревших версий моделей
- Для каждого инструмента указан источник (ссылка)
- Таблица покрывает все 4 категории (чаты, IDE-копилоты, AI-IDE, CLI-агенты)
- Инфраструктура: headless-режим, auth-токены, Agent SDK, Agent Teams, OpenClaw — описание, ссылки, статус
- 10-15 MCP-серверов с описанием
- 3-4 сервера рекомендованы для курса с обоснованием

## Зависимости

Нет. Эту задачу можно начинать первой.

## Входные данные

- `sources/Портрет ИИ зрелости.md` — раздел "Тулинг и экономика"
- `sources/AI-Assisted Development Adoption.pdf` — секция 3: таблица инструментов (Claude Code, OpenCode, Cursor, Antigravity, Codex CLI, Kilo Code, ChatGPT, DeepSeek) с типами, моделями, use cases
- Контент-план: Модуль 1, раздел "Список проверенных инструментов"
- Контент-план: Модуль 3, раздел "Работа с MCP"
