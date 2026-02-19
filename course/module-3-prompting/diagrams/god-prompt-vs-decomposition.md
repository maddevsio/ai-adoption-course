# Антипаттерн: God-Prompt vs Декомпозиция

God-Prompt — попытка описать все в одном промпте. Результат: поверхностная реализация, пропущенные детали, несогласованность между компонентами.

```mermaid
flowchart TB
    subgraph bad["God-Prompt (плохо)"]
        GP["'Создай микросервис с\nStripe, PostgreSQL, Redis,\nRabbitMQ, REST, GraphQL,\nadmin, JWT, rate limiting,\nPrometheus, тесты, Docker'"]
        GP --> Result1["Поверхностная реализация\n- Нет error handling\n- Несогласованные компоненты\n- Пропущенные edge cases"]
    end

    subgraph good["Декомпозиция (хорошо)"]
        D1["1. Архитектура\nмодули и зависимости"]
        D2["2. Модели и БД\nSQLAlchemy + миграции"]
        D3["3. Stripe интеграция\nerror handling + retry"]
        D4["4. API endpoints\nREST + валидация"]
        D5["5. Тесты\nunit + integration"]
        D6["6. Observability\nлоги + метрики"]

        D1 --> D2 --> D3 --> D4 --> D5 --> D6
        D6 --> Result2["Глубокая реализация\nна каждом уровне"]
    end
```

**Правило:** если промпт длиннее 10-15 строк — скорее всего, это God-Prompt. Разбейте на шаги. Каждый шаг = одна ответственность.
