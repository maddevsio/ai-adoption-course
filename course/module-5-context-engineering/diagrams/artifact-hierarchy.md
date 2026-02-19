# Иерархия артефактов SDD

Три уровня артефактов: чем выше — тем стабильнее документ и тем реже он меняется. Constitution один на проект, Spec один на фичу, Trace один на сессию.

```mermaid
flowchart TD
    C["Constitution\n1 файл на проект\nМеняется редко\n(tech stack, ADR, паттерны)"]

    S1["Spec: Auth"]
    S2["Spec: Payments"]
    S3["Spec: Search"]

    T1["Trace 1"]
    T2["Trace 2"]
    T3["Trace 3"]
    T4["Trace 4"]
    T5["Trace 5"]

    C -->|"1 спека на фичу"| S1 & S2 & S3
    S1 -->|"1 trace на сессию"| T1 & T2
    S2 --> T3
    S3 --> T4 & T5
```

**Как они взаимодействуют:**

| Уровень | Документ | Частота изменений | Кто пишет |
|---------|----------|-------------------|-----------|
| Constitution | `AGENTS.md` / `constitution.md` | Раз в неделю (reflect-mode) | Человек + reflect-агент |
| Specification | `specs/003-auth.md` | Раз на фичу | Человек |
| Trace | `traces/003-auth.trace.md` | Каждая сессия | Агент |
