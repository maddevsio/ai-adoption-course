[← Оглавление](../../../README.md)

# Параллельная работа и слияние результатов

Два агента выполняют разные задачи одновременно. Ускорение в 2 раза.

---

### Упражнение: два worktrees, два агента (15 мин)

**1. Терминал A — Агент A:**

```bash
claude
```

```
Создай git worktree для фичи "users-api" и в нём реализуй:

GET /api/users endpoint.

Требования:
1. Возвращает массив пользователей
2. Фильтровать удалённых (deleted_at = null)
3. Pagination: ?page=1&limit=20
4. Тесты: получение списка, pagination, фильтрация удалённых
5. Запустить все тесты

Действуй автономно.
```

**2. Терминал B — Агент B (одновременно с A):**

```bash
claude
```

```
Создай git worktree для фичи "request-logging" и в нём реализуй:

Middleware для логирования HTTP-запросов.

Требования:
1. Логировать: метод, путь, IP, timestamp
2. Логировать время выполнения
3. Не логировать health-check endpoints (/health, /ping)
4. Формат: [2026-01-15 10:30:45] GET /api/users from 192.168.1.10 - 45ms
5. Тесты для middleware
6. Запустить все тесты

Действуй автономно.
```

**3. Дождитесь завершения обоих агентов.**

### Упражнение: слияние результатов (10 мин)

**1. Вернитесь в основную директорию:**

```bash
cd ../test-orchestration
git checkout main
```

**2. Merge обеих веток:**

```bash
git merge feat/users-api
git merge feat/request-logging
```

**3. Если конфликты:**

| Способ | Когда |
|--------|-------|
| Вручную | Сложная логика, критичный код |
| Через агента: `claude` → "Разреши merge conflict" | Тривиальные конфликты |
| `git checkout --ours/--theirs` | Одна версия явно правильная |

**4. Проверьте и завершите:**

```bash
git commit -m "Merge feat/request-logging into main"
pytest  # или npm test, go test
```

**5. Очистка:**

```bash
git worktree remove ../myproject-users-api
git worktree remove ../myproject-request-logging
git branch -d feat/users-api feat/request-logging
```

### Предотвращение конфликтов

| Тип конфликта | Как предотвратить |
|--------------|-------------------|
| Оба изменили app.py | Разбить на модули: users.py, logging.py |
| Оба добавили зависимости | Указать в playbook кто за какие зависимости |
| Тесты в одном файле | Раздельные файлы: test_users.py, test_logging.py |

### Проверка

- [ ] Оба worktrees созданы и агенты запущены параллельно
- [ ] Обе задачи завершены, изменения изолированы
- [ ] Ветки смержены, конфликты разрешены
- [ ] Тесты проходят, worktrees удалены
---

[← Генератор + Ревьюер](02-generator-reviewer.md) | [Оглавление](../../../README.md) | [Установите Maestro →](04-install-maestro.md)
