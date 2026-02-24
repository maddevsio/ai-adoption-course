# Чеклист и следующие шаги

## Что вы сделали

- [ ] Изучили источники по SDD и примеры конституций
- [ ] Установили и протестировали skills
- [ ] Создали конституцию проекта
- [ ] Написали спецификацию фичи
- [ ] Реализовали фичу по спецификации
- [ ] Создали trace с заметками по реализации

## Ключевые паттерны

- **SDD-цикл:** спецификация → реализация → ревью → trace → constitution
- **Constitution защищена:** агенты не пишут напрямую, предлагают через traces
- **Traces заполняются инкрементально** — не в конце сессии
- **"Опционально" для агента = "не делать"** — важное пишите "ОБЯЗАТЕЛЬНО"

> [!IMPORTANT]
> Агент берёт вежливые рекомендации как необязательные и пропускает их. Если что-то критично — будьте директивны: "ОБЯЗАТЕЛЬНО", а не "желательно".
- **Начните с малого:** AGENTS.md + traces, добавляйте уровни по мере роста
- **Не повторяйте паттерн** — если делаете что-то третий раз, сделайте из этого скилл или документ. Это работает и для LLM (переиспользует инструкции), и для вас (не тратите время на повторные объяснения)

## Рефлексия

Периодически (раз в 1-2 недели) разбирайте свою документацию:

- Нет ли **противоречий** между AGENTS.md и traces?
- Нет ли **архаизмов** — правил, которые уже неактуальны?
- Не стал ли контекст **слишком большим** — агент тратит токены на чтение неактуальных файлов?

> [!WARNING]
> Устаревшая документация хуже отсутствующей — агент будет следовать неактуальным правилам с полной уверенностью.

## Пример организации `/docs`

```
docs/
├── ARCHITECTURE.md        # Общая архитектура
├── API.md                 # Спецификация API
├── adr/                   # Architecture Decision Records
│   ├── 001-use-fastapi.md
│   └── 002-sqlite-to-postgres.md
├── specs/                 # Спецификации фич
│   ├── task-filtering.spec.md
│   └── auth.spec.md
└── traces/                # Implementation notes
    ├── 2026-01-15-task-filtering.md
    └── 2026-01-20-auth.md
```

## Следующие шаги

1. **Примените на реальном проекте:** создайте AGENTS.md, напишите спецификацию следующей фичи
2. **Изучите продвинутые техники:** Memory Bank, Reflect-mode, Decision Log
3. **Экспериментируйте с инструментами:** сравните легковесную vs формальную спецификацию

## Полезные ссылки

**Стандарты:**
- [AGENTS.md specification](https://agents.md/)

**Коллекции:**
- [awesome-claude-md](https://github.com/josix/awesome-claude-md) — примеры конституций
- [awesome-claude-code](https://github.com/hesreallyhim/awesome-claude-code) — skills для Claude Code

**Инструменты:**
- [superpowers](https://github.com/obra/superpowers)
- [cc-sdd](https://github.com/gotalab/cc-sdd) — SDD-workflow для Claude Code
- [GitHub Spec Kit](https://github.com/github/spec-kit) — SDD-тулкит от GitHub
- [claude-skills-starter](https://github.com/angakh/claude-skills-starter) — starter pack skills

**Статьи:**
- [Creating the Perfect CLAUDE.md](https://dometrain.com/blog/creating-the-perfect-claudemd-for-claude-code/) — Dometrain
- [Spec-driven development with AI](https://github.blog/ai-and-ml/generative-ai/spec-driven-development-with-ai-get-started-with-a-new-open-source-toolkit/) — GitHub Blog

---

## Обратная связь

1. Какой шаг оказался самым сложным? Почему?
2. Какие паттерны из конституций реальных проектов показались наиболее ценными?
3. Изменилось ли ваше представление о том, как работать с AI-агентами?
4. Какие skills оказались наиболее полезными?
5. Планируете ли вы применить SDD в своих проектах? Если да, с чего начнёте?
