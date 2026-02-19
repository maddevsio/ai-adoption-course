# Git Worktree: изоляция агентов

Один Git-репозиторий, одна `.git` директория, но несколько рабочих копий. Каждый агент работает в своей директории на своей ветке. Агенты не видят незакоммиченные изменения друг друга.

```mermaid
flowchart TD
    Git[".git\n(общий репозиторий,\nодна история)"]

    W1["./project\nbranch: main\nРазработчик работает здесь"]
    W2["../project-auth\nbranch: feat/auth\nАгент A"]
    W3["../project-api\nbranch: feat/api\nАгент B"]
    W4["../project-tests\nbranch: feat/tests\nАгент C"]

    Git --> W1
    Git --> W2
    Git --> W3
    Git --> W4

    W2 -->|"PR"| Merge["main"]
    W3 -->|"PR"| Merge
    W4 -->|"PR"| Merge
```

**Правило:** каждый план = отдельный worktree. Агент начинает — создаем worktree. Агент закончил — удаляем worktree. Это предотвращает 90% конфликтов.

**Команды:**
```bash
git worktree add ../project-auth -b feat/auth   # создать
git worktree remove ../project-auth              # удалить
```
