# Defence in Depth: многослойная защита

Безопасность — комбинация слоёв. Базовые слои нужны всегда, дополнительные — по контексту.

```mermaid
flowchart TD
    Agent["AI-агент"]

    subgraph baseline["Базовые — всегда"]
        S1["Аудит\nлогировать действия,\ntrace-файлы"]
        S2["Whitelist команд\ngit, npm, pytest —\nявно разрешённые"]
    end

    subgraph extra["Дополнительные — для production и чувствительных данных"]
        S3["Sandboxing\nDocker, VM, git worktree"]
        S4["Ограничение сети\nfirewall, network policies"]
        S5["Read-only\nдля аудита и анализа"]
    end

    Agent --> baseline --> extra --> Protected["Защищённая система"]
```

**Принцип:** каждый слой работает независимо. Аудит + whitelist — минимум для любого проекта. Sandboxing, сеть и read-only добавляйте когда агент работает с production-данными, внешними сервисами или чувствительным кодом.