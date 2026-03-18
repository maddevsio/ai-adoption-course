# Экспорт из GitHub-репозитория в Confluence

Экспорт markdown-файлов в Confluence через [mark](https://github.com/kovetskiy/mark).

## Установка mark

```bash
go install github.com/kovetskiy/mark@latest
```

Или через Homebrew:

```bash
brew install mark
```

## Получение API-токена

1. Открыть [Atlassian API tokens](https://id.atlassian.com/manage-profile/security/api-tokens)
2. **Create API token** → задать имя (например `mark-export`) → **Create**
3. Скопировать токен — он показывается только один раз

## Подготовка файлов

В начало каждого `.md` файла добавить заголовок для mark:

```markdown
<!-- Space: AI -->
<!-- Title: Название страницы -->
<!-- Parent: Название родительской страницы -->
```

- **Space** — ключ пространства в Confluence (`AI`, `DEV`, `ENG`)
- **Title** — заголовок страницы в Confluence
- **Parent** — родительская страница (должна существовать или создаваться другим файлом в том же батче)

Пример для страницы модуля:

```markdown
<!-- Space: AI -->
<!-- Title: Кодер vs инженер -->
<!-- Parent: Модуль 9. Агентность разработчика -->

# Кодер vs инженер

Текст страницы...
```

Пример для родительской страницы:

```markdown
<!-- Space: AI -->
<!-- Title: Модуль 9. Агентность разработчика -->
<!-- Parent: AI для разработчиков -->
```

## Проверка перед экспортом

```bash
mark -f 'course/module-9-agency/**/*.md' --dry-run
```

## Настройка окружения

```bash
export MARK_USERNAME="mail@maddevs.io"
export MARK_PASSWORD="ATATT...C3E"
export MARK_BASE_URL="https://maddevs.atlassian.net/wiki"
```

- `MARK_USERNAME` — email аккаунта Atlassian
- `MARK_PASSWORD` — API-токен (не пароль от аккаунта)
- `MARK_BASE_URL` — URL Confluence с суффиксом `/wiki`

## Экспорт

Один модуль:

```bash
mark -f 'course/module-9-agency/**/*.md' --drop-h1 --features=mermaid --minor-edit
```

Все модули:

```bash
mark -f 'course/**/*.md' --drop-h1 --features=mermaid --minor-edit
```

Флаги:

| Флаг | Назначение |
|------|------------|
| `-f` | Glob-паттерн для входных файлов |
| `--drop-h1` | Убирает `# Заголовок` — Confluence берёт Title из шапки |
| `--features=mermaid` | Рендерит mermaid-диаграммы |
| `--minor-edit` | Помечает как minor edit (без уведомлений подписчикам) |
| `--dry-run` | Предпросмотр без загрузки |
| `--debug` | Подробный вывод |

## Проблемы

**401 Unauthorized** — в `MARK_PASSWORD` должен быть API-токен, не пароль аккаунта.

**Parent page not found** — родительская страница должна существовать. Создайте вручную или включите файл с таким Title в тот же батч.

**Mermaid не рендерится** — убедитесь что передан `--features=mermaid` и есть доступ в интернет.
