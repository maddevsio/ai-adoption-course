[← Оглавление](../../../README.md)

# Git worktree для изоляции агентов

### Чек-лист готовности

- [ ] Claude Code установлен (Модуль 2)
- [ ] Git установлен и настроен
- [ ] Две вкладки терминала или IDE открыты

---

### Подготовка

Создайте тестовый репозиторий или используйте существующий:

```bash
mkdir ~/practice/test-orchestration && cd ~/practice/test-orchestration
git init
echo "# Test Orchestration Project" > README.md
git add README.md && git commit -m "Initial commit"
```

### Упражнение: создать worktree и запустить агента (10 мин)

**1. Запустите агента и попросите его создать worktree:**

```bash
claude
```

```
Создай git worktree для фичи "add-logging" и в нём добавь базовое логирование в проект:
1. Настрой logger с форматом "[timestamp] [level] message"
2. Добавь логирование в 2-3 ключевых местах
3. Запусти проверку что код работает
```

Агент сам создаст worktree, переключится в него и начнёт работу. Вам не нужно вручную вызывать `git worktree add`.

**2. Проверьте изоляцию:**

В отдельном терминале:
```bash
cd ~/practice/test-orchestration
git status                    # чистая — все изменения в worktree
git worktree list             # видно оба worktree
```

**3. Попросите агента завершить работу:**

```
Закоммить изменения, создай PR и удали worktree.
```

### Проверка

- [ ] Worktree создан
- [ ] Агент запущен в worktree
- [ ] Основная директория осталась чистой
- [ ] Worktree удалён

**Принцип:** Одна ветка = один план = один worktree.
---

[← 7. "Библия" и Playbook оркестратора](../theory/04-playbook-and-operations.md) | [Оглавление](../../../README.md) | [Генератор + Ревьюер →](02-generator-reviewer.md)
