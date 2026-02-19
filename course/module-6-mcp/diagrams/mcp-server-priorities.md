# Карта MCP-серверов по приоритету

С чего начать и в каком порядке расширять набор MCP-серверов. Начните с обязательных четырех, затем добавляйте по необходимости.

```mermaid
flowchart TD
    subgraph must["Обязательные (начните с этих)"]
        G["Git MCP\nCode archaeology,\nанализ истории"]
        J["Jira MCP\nЗадачи, worklogs,\nстатусы"]
        I["JetBrains MCP\nDebugger, refactoring,\ncode analysis"]
        F["Figma MCP\nDesign-to-code,\ndesign tokens"]
    end

    subgraph rec["Рекомендуемые (когда освоите базу)"]
        P["PostgreSQL MCP\nNatural language SQL,\nschema analysis"]
        B["Puppeteer MCP\nWeb automation,\nE2E тесты"]
    end

    subgraph opt["Опциональные (для специфических задач)"]
        M["Mermaid MCP\nГенерация диаграмм"]
        O["Obsidian MCP\nKnowledge base"]
        MR["Miro MCP\nWhiteboarding"]
    end

    must --> rec --> opt
```

**Совет:** не устанавливайте все серверы сразу. 3-5 активных серверов — оптимум. Больше 10 — деградация производительности.
