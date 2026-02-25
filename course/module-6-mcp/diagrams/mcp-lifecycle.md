[← Оглавление](../../../README.md)

# Жизненный цикл MCP-вызова

Что происходит "под капотом", когда агент использует MCP-инструмент: от инициализации до shutdown.

```mermaid
sequenceDiagram
    participant A as AI-агент
    participant M as MCP-сервер
    participant T as Внешний инструмент

    Note over A,M: 1. Initialization (при запуске)
    A->>M: initialize (capabilities)
    M-->>A: OK (server info, protocol version)

    Note over A,M: 2. Discovery (какие tools доступны?)
    A->>M: tools/list
    M-->>A: [git_log, git_blame, git_search, ...]

    Note over A,T: 3. Execution (повторяется при каждом вызове)
    A->>M: tools/call (git_log, {grep: "auth"})
    M->>T: git log --grep="auth"
    T-->>M: Список коммитов
    M-->>A: Результат (JSON)
    Note over A: Агент анализирует результат<br/>и продолжает работу

    Note over A,M: 4. Shutdown (при завершении)
    A->>M: shutdown
    M-->>A: OK
```

**Что важно понимать:**
- Discovery происходит один раз — агент узнает, какие инструменты доступны
- Execution повторяется многократно за сессию
- Агент сам решает, когда вызвать какой tool — на основе контекста задачи
- Если сервер не отвечает — агент может продолжить работу без этого инструмента
