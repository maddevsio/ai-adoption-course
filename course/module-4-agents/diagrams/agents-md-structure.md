[← Оглавление](../../../README.md)

# Структура AGENTS.md

AGENTS.md — конституция проекта для агента. Это **главная точка входа**: агент читает AGENTS.md первым и ориентируется по нему во всём проекте.

```mermaid
flowchart TD
    Root["AGENTS.md"] --> Stack
    Root --> Conv
    Root --> Rules
    Root --> Forbid
    Root --> Before
    Root --> Finish

    Stack["Stack<br>Точные версии: язык,<br>фреймворк, БД, тесты"]
    Conv["Conventions<br>Именование файлов,<br>структура папок, code style"]
    Rules["Rules<br>Обязательные паттерны:<br>error handling, тесты, миграции"]
    Forbid["Forbidden<br>Антипаттерны: что агент<br>НЕ должен делать"]
    Before["Before Starting<br>Первые шаги: что прочитать,<br>что проверить, что запустить"]
    Finish["Before Finishing<br>Чеклист перед коммитом:<br>тесты, линтер, coverage"]
```

**Порядок важен:** агент читает AGENTS.md сверху вниз. Stack и Conventions задают контекст, Rules и Forbidden — ограничения, Before Starting — стартовый чеклист, Before Finishing — финальная проверка.

> [!TIP]
> Если контекста много — раскидайте по файлам, в AGENTS.md оставьте ссылки. Пример:
> ```
> ## References
> - Стек и архитектура → docs/architecture.md
> - API-контракты → docs/api.md
> - ADR → docs/adr/
> ```
> AGENTS.md остаётся компактным и читаемым, а детали живут рядом с кодом.
