# Структура AGENTS.md

AGENTS.md — конституция проекта для агента. Каждая секция отвечает за свой аспект: что использовать, как писать код, что обязательно, что запрещено, с чего начать.

```mermaid
flowchart TD
    Root["AGENTS.md"] --> Stack
    Root --> Conv
    Root --> Rules
    Root --> Forbid
    Root --> Before

    Stack["Stack<br>Точные версии: язык,<br>фреймворк, БД, тесты"]
    Conv["Conventions<br>Именование файлов,<br>структура папок, code style"]
    Rules["Rules<br>Обязательные паттерны:<br>error handling, тесты, миграции"]
    Forbid["Forbidden<br>Антипаттерны: что агент<br>НЕ должен делать"]
    Before["Before Starting<br>Первые шаги: что прочитать,<br>что проверить, что запустить"]
```

**Порядок важен:** агент читает AGENTS.md сверху вниз. Stack и Conventions задают контекст, Rules и Forbidden — ограничения, Before Starting — стартовый чеклист.
