# Карта MCP-серверов по приоритету

С чего начать и в каком порядке расширять набор MCP-серверов. Начните с обязательных четырех, затем добавляйте по необходимости.

```mermaid
flowchart TD
    subgraph must["Обязательные (начните с этих)"]
        G["Git MCP<br>Code archaeology,<br>анализ истории"]
        J["Jira MCP<br>Задачи, worklogs,<br>статусы"]
        I["JetBrains MCP<br>Debugger, refactoring,<br>code analysis"]
        F["Figma MCP<br>Design-to-code,<br>design tokens"]
    end

    subgraph rec["Рекомендуемые (когда освоите базу)"]
        P["PostgreSQL MCP<br>Natural language SQL,<br>schema analysis"]
        B["Puppeteer MCP<br>Web automation,<br>E2E тесты"]
    end

    subgraph opt["Опциональные (для специфических задач)"]
        M["Mermaid MCP<br>Генерация диаграмм"]
        O["Obsidian MCP<br>Knowledge base"]
        MR["Miro MCP<br>Whiteboarding"]
    end

    must --> rec --> opt
```

**Совет:** не устанавливайте все серверы сразу. 3-5 активных серверов — оптимум. Больше 10 — деградация производительности.
