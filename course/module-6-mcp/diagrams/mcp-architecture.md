[← Оглавление](../../../README.md)

# Архитектура MCP: Client -> Server -> Tool

Один AI-агент подключается к нескольким MCP-серверам. Каждый сервер — адаптер между агентом и конкретным внешним инструментом. Протокол единый (JSON-RPC), инструменты — разные.

```mermaid
flowchart LR
    Agent["AI-агент<br>(Claude Code,<br>Cursor, OpenCode)"]

    MCP1["MCP Server<br>Git"]
    MCP2["MCP Server<br>Jira"]
    MCP3["MCP Server<br>Figma"]
    MCP4["MCP Server<br>PostgreSQL"]

    Tool1["Git<br>репозиторий"]
    Tool2["Jira<br>REST API"]
    Tool3["Figma<br>Dev Mode API"]
    Tool4["PostgreSQL<br>БД"]

    Agent -->|"JSON-RPC<br>(stdio)"| MCP1 --> Tool1
    Agent -->|"JSON-RPC<br>(stdio)"| MCP2 --> Tool2
    Agent -->|"JSON-RPC<br>(stdio)"| MCP3 --> Tool3
    Agent -->|"JSON-RPC<br>(stdio)"| MCP4 --> Tool4
```

**Аналогия:** MCP — это "USB для AI". Как USB позволяет подключить любое устройство к компьютеру через единый разъем, MCP позволяет подключить любой инструмент к AI-агенту через единый протокол.

**Ключевые свойства:**
- Один MCP-сервер работает со всеми AI-агентами, поддерживающими протокол
- Агент не знает деталей API каждого инструмента — MCP-сервер абстрагирует их
- Серверы запускаются как отдельные процессы, общение через stdin/stdout
