# Feature Specification: [Название фичи]

**Автор:** [Ваше имя]
**Дата:** [YYYY-MM-DD]
**Статус:** [Draft / In Review / Approved / Implemented]

---

## Цель

[1-2 предложения: что делает фича, зачем она нужна, какую проблему решает]

**Пример:**
> Пользователь может фильтровать список задач по статусу и приоритету, чтобы быстро находить нужные задачи без необходимости просматривать весь список.

---

## Acceptance Criteria

Чёткие критерии готовности. Фича считается выполненной, когда все пункты ниже реализованы:

- [ ] [Критерий 1: например, "пользователь может фильтровать задачи по статусу (pending/in_progress/done)"]
- [ ] [Критерий 2: например, "пользователь может фильтровать задачи по приоритету (low/medium/high)"]
- [ ] [Критерий 3: например, "фильтры можно комбинировать (статус + приоритет одновременно)"]
- [ ] [Критерий 4: например, "пустой фильтр возвращает все задачи"]
- [ ] [Критерий 5: например, "неверные значения фильтров возвращают ошибку 400"]
- [ ] [Критерий 6: например, "есть тесты для всех сценариев фильтрации"]

**Примечание:** Каждый критерий должен быть измеримым и проверяемым.

---

## Технические ограничения

Какие технологии использовать, какие паттерны применять, каким правилам следовать.

### Технологии

- **Backend:** [язык, фреймворк, версия]
- **Database:** [какая БД, нужны ли индексы, миграции]
- **API:** [REST/GraphQL/gRPC, формат данных]
- **Frontend (если применимо):** [фреймворк, библиотеки]

**Пример:**
> - Backend: Go 1.22, Echo v4
> - Database: PostgreSQL 15 (добавить индексы на поля status и priority)
> - API: REST (query parameters для фильтров)

### Паттерны и соглашения

- **Следовать:** [ссылка на конституцию проекта, например, "AGENTS.md"]
- **Обязательные паттерны:** [перечислить специфичные для этой фичи]
- **Conventions:** [именование, структура файлов]

**Пример:**
> - Следовать паттернам из AGENTS.md (Repository pattern, error handling)
> - Фильтры передаются через query parameters (RESTful)
> - Валидация на уровне handler, бизнес-логика в service layer

### Ограничения

- **Performance:** [требования к производительности, если есть]
- **Security:** [аутентификация, авторизация, валидация]
- **Compatibility:** [обратная совместимость, версионирование API]

**Пример:**
> - Запрос должен выполняться < 100ms на 10,000 задач
> - Фильтрация доступна только авторизованным пользователям
> - Обратная совместимость: старые клиенты без фильтров продолжают работать

---

## Примеры использования

Конкретные примеры того, как будет работать фича. Для API — примеры запросов и ответов. Для UI — скриншоты или описания.

### API Examples (для backend)

**Пример 1: Фильтрация по статусу**

Request:
```http
GET /api/tasks?status=pending HTTP/1.1
Authorization: Bearer <token>
```

Response:
```json
{
  "tasks": [
    {
      "id": "1",
      "title": "Task 1",
      "description": "...",
      "status": "pending",
      "priority": "high"
    },
    {
      "id": "2",
      "title": "Task 2",
      "description": "...",
      "status": "pending",
      "priority": "low"
    }
  ],
  "total": 2
}
```

---

**Пример 2: Фильтрация по приоритету**

Request:
```http
GET /api/tasks?priority=high HTTP/1.1
Authorization: Bearer <token>
```

Response:
```json
{
  "tasks": [
    {
      "id": "1",
      "title": "Task 1",
      "description": "...",
      "status": "pending",
      "priority": "high"
    },
    {
      "id": "3",
      "title": "Task 3",
      "description": "...",
      "status": "in_progress",
      "priority": "high"
    }
  ],
  "total": 2
}
```

---

**Пример 3: Комбинированная фильтрация**

Request:
```http
GET /api/tasks?status=pending&priority=high HTTP/1.1
Authorization: Bearer <token>
```

Response:
```json
{
  "tasks": [
    {
      "id": "1",
      "title": "Task 1",
      "description": "...",
      "status": "pending",
      "priority": "high"
    }
  ],
  "total": 1
}
```

---

**Пример 4: Пустой фильтр (все задачи)**

Request:
```http
GET /api/tasks HTTP/1.1
Authorization: Bearer <token>
```

Response:
```json
{
  "tasks": [
    {
      "id": "1",
      "title": "Task 1",
      "status": "pending",
      "priority": "high"
    },
    {
      "id": "2",
      "title": "Task 2",
      "status": "pending",
      "priority": "low"
    },
    {
      "id": "3",
      "title": "Task 3",
      "status": "in_progress",
      "priority": "high"
    }
  ],
  "total": 3
}
```

---

**Пример 5: Неверное значение фильтра (ошибка)**

Request:
```http
GET /api/tasks?status=invalid HTTP/1.1
Authorization: Bearer <token>
```

Response:
```http
HTTP/1.1 400 Bad Request
Content-Type: application/json

{
  "error": "Invalid status value",
  "details": "status must be one of: pending, in_progress, done"
}
```

---

### UI Examples (если применимо)

[Описание UI или ссылка на макеты]

**Пример:**
> Над списком задач добавляются два dropdown-меню:
> - "Filter by Status" (опции: All, Pending, In Progress, Done)
> - "Filter by Priority" (опции: All, Low, Medium, High)
>
> При выборе значения список автоматически фильтруется (API запрос с query parameters).

---

## Edge Cases (Граничные случаи)

Специфичные сценарии, которые нужно обработать.

- **Edge Case 1:** [Описание случая и ожидаемое поведение]
  - Пример: "Фильтр по несуществующему статусу → возвращать 400 с понятной ошибкой"

- **Edge Case 2:** [Следующий случай]
  - Пример: "Множественные значения одного параметра (?status=pending&status=done) → возвращать 400 или использовать OR-логику?"

- **Edge Case 3:** [Ещё случай]
  - Пример: "Регистр query parameters (Status vs status) → нормализовать к lowercase"

---

## Out of Scope

Что **явно НЕ входит** в эту задачу. Это важно, чтобы агент не додумывал лишнего.

- ❌ [Что не делаем 1: например, "Сортировка задач (отдельная фича)"]
- ❌ [Что не делаем 2: например, "Пагинация (отдельная фича)"]
- ❌ [Что не делаем 3: например, "Полнотекстовый поиск (отдельная фича)"]
- ❌ [Что не делаем 4: например, "Сохранение фильтров в профиле пользователя"]

---

## Testing Requirements

Какие тесты должны быть написаны для этой фичи.

### Unit Tests

- [ ] [Тест 1: например, "query parameter parsing корректно извлекает status"]
- [ ] [Тест 2: например, "query parameter parsing корректно извлекает priority"]
- [ ] [Тест 3: например, "валидация отклоняет неверные значения status"]
- [ ] [Тест 4: например, "валидация отклоняет неверные значения priority"]

### Integration Tests

- [ ] [Тест 1: например, "GET /api/tasks?status=pending возвращает только pending задачи"]
- [ ] [Тест 2: например, "GET /api/tasks?priority=high возвращает только high priority задачи"]
- [ ] [Тест 3: например, "GET /api/tasks?status=pending&priority=high работает корректно"]
- [ ] [Тест 4: например, "GET /api/tasks без параметров возвращает все задачи"]
- [ ] [Тест 5: например, "GET /api/tasks?status=invalid возвращает 400"]

### E2E Tests (если применимо)

- [ ] [Тест 1: например, "пользователь выбирает фильтр в UI → список обновляется"]

### Coverage Target

- **Минимум:** [например, 85% для нового кода]

---

## Implementation Notes

Дополнительные заметки для реализации.

### Database

- **Индексы:** [нужны ли новые индексы для оптимизации фильтрации?]
  - Пример: "Добавить составной индекс на (status, priority) для ускорения комбинированных фильтров"

- **Миграции:** [нужны ли изменения схемы?]
  - Пример: "Не требуется, поля status и priority уже существуют"

### API Design

- **Query Parameters:**
  ```
  ?status=<value>     # pending | in_progress | done
  &priority=<value>   # low | medium | high
  ```

- **Error Handling:**
  - 400 Bad Request: неверные значения фильтров
  - 401 Unauthorized: пользователь не авторизован
  - 500 Internal Server Error: ошибка на сервере

### Performance Considerations

- [Заметки о производительности]
  - Пример: "На 10,000 задач запрос должен выполняться < 100ms с индексом"
  - Пример: "Если база растёт > 100K задач, рассмотреть пагинацию"

---

## Dependencies

Зависимости от других фич, библиотек, сервисов.

- **Зависит от:**
  - [Фича/сервис 1: например, "Аутентификация (должна быть реализована)"]
  - [Фича/сервис 2: например, "Task Model с полями status и priority"]

- **Блокирует:**
  - [Фича 1: например, "Сортировка задач (логично сделать после фильтрации)"]

---

## Timeline

**Планируемое время:** [например, "3-5 часов разработки + тестирования"]

**Приоритет:** [High / Medium / Low]

**Deadline (если есть):** [YYYY-MM-DD]

---

## References

Полезные ссылки и документация.

- [Конституция проекта](../AGENTS.md)
- [REST API Guidelines](https://example.com/api-guidelines)
- [Документация фреймворка](https://example.com/framework-docs)
- [Связанные спецификации](./другая-спецификация.md)

---

## Changelog

История изменений спецификации.

- **[YYYY-MM-DD]:** [Автор] — Initial draft
- **[YYYY-MM-DD]:** [Автор] — Added edge cases
- **[YYYY-MM-DD]:** [Автор] — Approved, ready for implementation

---

## Реализация

**Статус:** [Not Started / In Progress / Completed / Deployed]

**Разработчик/Агент:** [Кто реализовывал]

**Дата начала:** [YYYY-MM-DD]

**Дата завершения:** [YYYY-MM-DD]

**PR:** [Ссылка на pull request]

**Trace:** [Ссылка на trace файл с заметками по реализации]

---

## Approval

**Reviewed by:** [Имя]

**Approved by:** [Имя]

**Date:** [YYYY-MM-DD]

**Signature:** [Подпись или commit hash, где спецификация была одобрена]
