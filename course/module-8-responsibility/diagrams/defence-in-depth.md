[← Оглавление](../../../README.md)

# Defence in Depth: многослойная защита

Безопасность — комбинация слоёв. Базовые слои нужны всегда, дополнительные — по контексту.

```mermaid
flowchart TD
    Agent["AI-агент"]

    subgraph baseline["Базовые — всегда"]
        S1["Аудит<br>логировать действия,<br>trace-файлы"]
        S2["Whitelist команд<br>git, npm, pytest —<br>явно разрешённые"]
    end

    subgraph extra["Дополнительные — для production и чувствительных данных"]
        S3["Sandboxing<br>Docker, VM, git worktree"]
        S4["Ограничение сети<br>firewall, network policies"]
        S5["Read-only<br>для аудита и анализа"]
    end

    Agent --> baseline --> extra --> Protected["Защищённая система"]
```

**Принцип:** каждый слой работает независимо. Аудит + whitelist — минимум для любого проекта. Sandboxing, сеть и read-only добавляйте когда агент работает с production-данными, внешними сервисами или чувствительным кодом.
