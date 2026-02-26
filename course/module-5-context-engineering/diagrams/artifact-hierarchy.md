[← Оглавление](../../../README.md)

# Иерархия артефактов SDD

Три уровня стабильности: чем выше — тем реже меняется. На каждом уровне несколько типов артефактов.

```mermaid
classDiagram
    direction TB

    class Constitution {
        стек, правила, запреты
    }
    class Memories {
        паттерны ошибок
    }
    class ADR {
        архитектурные решения
    }

    class Spec {
        требования, контракты
    }
    class Research {
        исследование подходов
    }
    class Prompts {
        шаблоны задач
    }

    class Trace {
        решения, проблемы
    }
    class Failure {
        postmortem ошибок
    }

    Constitution --> Spec : определяет
    Research ..> Spec : информирует
    Spec --> Trace : порождает
    Spec --> Failure : порождает
    Failure ..> Memories : урок
    Trace ..> Constitution : reflect
```

**Как они взаимодействуют:**

| Уровень | Артефакты | Частота изменений | Кто пишет |
|---------|-----------|-------------------|-----------|
| Проект | `AGENTS.md`, `memories/`, ADR | Раз в неделю (reflect-mode) | Человек + reflect-агент |
| Фича | `specs/003-auth.md`, research, prompt templates | Раз на фичу | Человек |
| Сессия | `traces/003-auth.trace.md`, failure postmortems | Каждая сессия | Агент |

**Обратная связь:** failures и traces поднимаются наверх — reflect-агент анализирует их и обновляет memories и constitution. Так ошибки не повторяются.
