# Архитектура MCP: Client -> Server -> Tool

Один AI-агент подключается к нескольким MCP-серверам. Каждый сервер — адаптер между агентом и конкретным внешним инструментом. Протокол единый (JSON-RPC), инструменты — разные.

```mermaid
flowchart LR
    Agent["AI-агент\n(Claude Code,\nCursor, OpenCode)"]

    MCP1["MCP Server\nGit"]
    MCP2["MCP Server\nJira"]
    MCP3["MCP Server\nFigma"]
    MCP4["MCP Server\nPostgreSQL"]

    Tool1["Git\nрепозиторий"]
    Tool2["Jira\nREST API"]
    Tool3["Figma\nDev Mode API"]
    Tool4["PostgreSQL\nБД"]

    Agent -->|"JSON-RPC\n(stdio)"| MCP1 --> Tool1
    Agent -->|"JSON-RPC\n(stdio)"| MCP2 --> Tool2
    Agent -->|"JSON-RPC\n(stdio)"| MCP3 --> Tool3
    Agent -->|"JSON-RPC\n(stdio)"| MCP4 --> Tool4
```

**Аналогия:** MCP — это "USB для AI". Как USB позволяет подключить любое устройство к компьютеру через единый разъем, MCP позволяет подключить любой инструмент к AI-агенту через единый протокол.

**Ключевые свойства:**
- Один MCP-сервер работает со всеми AI-агентами, поддерживающими протокол
- Агент не знает деталей API каждого инструмента — MCP-сервер абстрагирует их
- Серверы запускаются как отдельные процессы, общение через stdin/stdout
