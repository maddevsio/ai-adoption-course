# Структура AGENTS.md

AGENTS.md — конституция проекта для агента. Каждая секция отвечает за свой аспект: что использовать, как писать код, что обязательно, что запрещено, с чего начать.

```mermaid
flowchart TD
    Root["AGENTS.md"] --> Stack
    Root --> Conv
    Root --> Rules
    Root --> Forbid
    Root --> Before

    Stack["Stack\nТочные версии: язык,\nфреймворк, БД, тесты"]
    Conv["Conventions\nИменование файлов,\nструктура папок, code style"]
    Rules["Rules\nОбязательные паттерны:\nerror handling, тесты, миграции"]
    Forbid["Forbidden\nАнтипаттерны: что агент\nНЕ должен делать"]
    Before["Before Starting\nПервые шаги: что прочитать,\nчто проверить, что запустить"]
```

**Порядок важен:** агент читает AGENTS.md сверху вниз. Stack и Conventions задают контекст, Rules и Forbidden — ограничения, Before Starting — стартовый чеклист.
