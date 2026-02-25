[← Оглавление](../README.md)

# Полезные ссылки

Ссылки из материалов курса, сгруппированные по темам.

---

## Промптинг

- [Prompting Guide (русский)](https://www.promptingguide.ai/ru) -- комплексный гайд по промпт-инжинирингу
- [OpenAI Prompt Engineering Guide](https://platform.openai.com/docs/guides/prompt-engineering) -- официальный гайд с примерами структур

## Инструменты: документация

| Инструмент | Документация | Тип |
|-----------|-------------|-----|
| Claude Code | [code.claude.com/docs](https://code.claude.com/docs) | CLI |
| Cursor | [cursor.sh](https://cursor.sh/) | IDE |
| OpenCode | [opencode-ai/opencode](https://github.com/opencode-ai/opencode) | CLI |
| Codex CLI | [developers.openai.com/codex/cli](https://developers.openai.com/codex/cli/features/) | CLI |
| Google Antigravity | [antigravity.google](https://antigravity.google/) | IDE |
| GitHub Copilot | [github.com/features/copilot](https://github.com/features/copilot) | IDE plugin |
| Gemini CLI | [google-gemini/gemini-cli](https://github.com/google-gemini/gemini-cli) | CLI |
| Ollama | [ollama.com](https://ollama.com/download) | Локальные модели |

## AGENTS.md и конституции проектов

- [agents.md](https://agents.md/) -- спецификация открытого стандарта
- [Написание хорошего CLAUDE.md](https://www.humanlayer.dev/blog/writing-a-good-claude-md) -- HumanLayer
- [Awesome Claude.md](https://github.com/josix/awesome-claude-md) -- коллекция примеров
- [Awesome Cursor Rules](https://github.com/PatrickJS/awesome-cursorrules) -- коллекция для Cursor

## Spec-Driven Development (SDD)

- [Spec-Driven Development (GitHub Blog)](https://github.blog/ai-and-ml/generative-ai/spec-driven-development-with-ai-get-started-with-a-new-open-source-toolkit/) -- GitHub + spec-kit
- [SDD Tools (Martin Fowler)](https://martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html) -- Kiro, spec-kit, Tessl
- [SDD (Thoughtworks)](https://www.thoughtworks.com/en-us/insights/blog/agile-engineering-practices/spec-driven-development-unpacking-2025-new-engineering-practices) -- практика 2025
- [GitHub Spec Kit](https://github.com/github/spec-kit) -- инструмент для SDD
- [cc-sdd](https://github.com/gotalab/cc-sdd) -- SDD workflow для Claude Code

## Claude Code: продвинутое использование

- [Курс Claude Code in Action](https://anthropic.skilljar.com/claude-code-in-action)
- [Headless Mode](https://code.claude.com/docs/en/headless) -- автоматизация без UI
- [Agent Teams](https://code.claude.com/docs/en/agent-teams) -- мульти-агентные команды (experimental)
- [GitHub Actions](https://code.claude.com/docs/en/github-actions) -- CI/CD интеграция
- [Docker Sandbox](https://docs.docker.com/ai/sandboxes/claude-code/) -- изоляция агента
- [Claude Skills Starter](https://github.com/angakh/claude-skills-starter) -- 12 slash-commands
- [Awesome Claude Code](https://github.com/hesreallyhim/awesome-claude-code) -- коллекция skills

## MCP (Model Context Protocol)

**Спецификация и SDK:**
- [modelcontextprotocol.io](https://modelcontextprotocol.io) -- официальный сайт
- [MCP Specification](https://modelcontextprotocol.io/specification/2025-11-25) -- спецификация
- [MCP SDK](https://github.com/modelcontextprotocol/sdk) -- SDK

**Каталоги серверов:**
- [Official MCP Servers](https://github.com/modelcontextprotocol/servers) -- официальные серверы
- [MCP Awesome](https://mcp-awesome.com/) -- 1200+ серверов
- [MCP Catalog](https://mcp-catalog.com/) -- каталог
- [Best MCP Servers 2026](https://www.builder.io/blog/best-mcp-servers-2026) -- Builder.io

**Серверы:**

| Сервер | Репозиторий |
|--------|-----------|
| Git | [modelcontextprotocol/servers/git](https://github.com/modelcontextprotocol/servers/tree/main/src/git) |
| PostgreSQL | [modelcontextprotocol/servers/postgres](https://github.com/modelcontextprotocol/servers/tree/main/src/postgres) |
| Puppeteer | [modelcontextprotocol/servers/puppeteer](https://github.com/modelcontextprotocol/servers/tree/main/src/puppeteer) |
| Atlassian (Jira/Confluence) | [atlassian/atlassian-mcp-server](https://github.com/atlassian/atlassian-mcp-server) |
| JetBrains | [JetBrains/mcp-jetbrains](https://github.com/JetBrains/mcp-jetbrains) |
| Figma | [GLips/Figma-Context-MCP](https://github.com/GLips/Figma-Context-MCP) |
| Obsidian | [MarkusPfundstein/mcp-obsidian](https://github.com/MarkusPfundstein/mcp-obsidian) |

## Оркестрация и параллельные агенты

**Ralph Loop:**
- [ghuntley.com/ralph](https://ghuntley.com/ralph/) -- оригинальная концепция
- [ralph-orchestrator](https://github.com/mikeyobrien/ralph-orchestrator) -- реализация

**Оркестраторы:**
- [Claude Squad](https://github.com/smtg-ai/claude-squad) -- мульти-агентная система
- [claude-flow](https://github.com/ruvnet/claude-flow) -- оркестрация
- [OpenClaw](https://docs.openclaw.ai/) -- мульти-агентная платформа
- [Claude Agent SDK (Python)](https://github.com/anthropics/claude-agent-sdk-python)

**Git worktree:**
- [git-scm.com/docs/git-worktree](https://git-scm.com/docs/git-worktree) -- документация

**Режимы работы с агентами:**
- [AI Coding Workflow (Cursor)](https://carlrannaberg.medium.com/my-current-ai-coding-workflow-f6bdc449df7f) -- Planner/Executor modes
- [Agentic Coding](https://research.aimultiple.com/agentic-coding/) -- task-based execution
- [Agentic Coding Manifesto](https://agentic-coding.github.io/) -- манифест
- [Agentic Coding на практике](https://ed-wentworth.medium.com/how-im-using-agentic-coding-with-claude-and-cursor-in-real-world-projects-b4b6694c132d) -- story -> tasks workflow

## Context Engineering

- [Context Engineering (Lance Martin)](https://rlancemartin.github.io/2025/06/23/context_engineering/) -- обзор с примерами
- [Cline Memory Bank](https://docs.cline.bot/prompting/cline-memory-bank) -- концепция memory bank

## Ответственность и безопасность

- [HIPAA Enforcement](https://www.hhs.gov/hipaa/for-professionals/compliance-enforcement/agreements/index.html) -- действия регулятора
- [Sycophancy Research (Anthropic)](https://www.anthropic.com/research/measuring-model-persuasiveness) -- исследование угодливости моделей
- [Линтеры для агентов](https://factory.ai/news/using-linters-to-direct-agents) -- Factory.ai

## Кейсы и исследования

- [YC: 25% стартапов с AI-кодом](https://techcrunch.com/2025/03/06/a-quarter-of-startups-in-ycs-current-cohort-have-codebases-that-are-almost-entirely-ai-generated/) -- TechCrunch
- [Vibe Coding Hangover](https://hackernoon.com/the-vibe-coding-hangover-what-happens-when-ai-writes-95percent-of-your-code) -- что бывает, когда 95% кода от ИИ
- [Multi-Agent Org Chart](https://medium.com/@procoder/i-replaced-my-entire-ai-workflow-with-an-org-chart-of-7-agents-heres-the-complete-technical-eda367b91b39) -- 7 агентов вместо workflow

## Бенчмарки

- [SWE-Bench](https://www.swebench.com/) -- бенчмарк для software engineering агентов
- [The Agent Company](https://the-agent-company.com/) -- бенчмарк для бытовых задач агентов

## Практика

- [Gandalf (Lakera)](https://gandalf.lakera.ai/intro) -- интерактивная игра на prompt injection
