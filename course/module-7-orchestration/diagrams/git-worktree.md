# Git Worktree: изоляция агентов

Один Git-репозиторий, одна `.git` директория, но несколько рабочих копий. Каждый агент работает в своей директории на своей ветке. Агенты не видят незакоммиченные изменения друг друга.

```mermaid
flowchart TD
    Git[".git<br>(общий репозиторий,<br>одна история)"]

    W1["./project<br>branch: main<br>Разработчик работает здесь"]
    W2["../project-auth<br>branch: feat/auth<br>Агент A"]
    W3["../project-api<br>branch: feat/api<br>Агент B"]
    W4["../project-tests<br>branch: feat/tests<br>Агент C"]

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
