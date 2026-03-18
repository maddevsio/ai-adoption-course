# Экспорт GitHub-репозитория в SCORM

Сборка SCORM 1.2 пакета из markdown-курса. На выходе — `.zip` для загрузки в LMS.

## Что такое SCORM

SCORM 1.2 пакет — это ZIP-архив:

- `imsmanifest.xml` — метаданные: структура курса, список ресурсов
- HTML-страницы — контент
- Ассеты — CSS, JS, картинки

LMS читает манифест, показывает контент и отслеживает прогресс через JS API.

## Подготовка репозитория

### Структура

```
course/
├── module-0-intro/
│   └── theory.md
├── module-1-topic/
│   ├── theory/
│   │   ├── 01-intro.md
│   │   └── 02-deep-dive.md
│   ├── practice/
│   │   └── 01-exercise.md
│   └── diagrams/
│       └── overview.md
├── glossary.md
└── links.md
```

- `module-{N}-{slug}/` — модули с номерами для порядка
- `theory/`, `practice/`, `diagrams/` — секции внутри модуля
- `01-`, `02-` — префиксы для сортировки файлов
- `# H1` заголовок → название страницы в навигации

### Сжатие картинок

LMS Mad Devs ограничивает размер файла внутри SCORM-пакета до **1 МБ**. Скриншоты и PNG легко превышают лимит.

Найти тяжёлые файлы:

```bash
find course/ -type f \( -name "*.png" -o -name "*.jpg" \) -size +1M
```

Сжать через ImageMagick:

```bash
convert input.png -resize 1200x1200\> -quality 70 output.jpg
```

Или автоматизировать в билд-скрипте через Pillow (PNG → JPEG, max 1200px, quality 70%).

### Mermaid-диаграммы

Если в markdown есть ` ```mermaid ` блоки — рендерить в SVG при сборке:

```bash
npm install -g @mermaid-js/mermaid-cli
```

На headless-сервере нужен Chromium:

```bash
apt-get install -y chromium-browser
```

Кешировать SVG по хешу контента чтобы не рендерить повторно.

## Билд-скрипт

Скрипт должен:

1. Обойти `course/`, собрать страницы с учётом порядка модулей и секций
2. Сконвертировать markdown → HTML (таблицы, code blocks, task lists)
3. Отрендерить mermaid-блоки в SVG
4. Сжать картинки до < 1 МБ
5. Сгенерировать `index.html` с навигацией (sidebar + iframe)
6. Сгенерировать `imsmanifest.xml`
7. Запаковать в `.zip` с `ZIP_DEFLATED`

### Манифест SCORM 1.2

```xml
<manifest identifier="course-id" version="1.0"
  xmlns="http://www.imsproject.org/xsd/imscp_rootv1p1p2"
  xmlns:adlcp="http://www.adlnet.org/xsd/adlcp_rootv1p2">
  <metadata>
    <schema>ADL SCORM</schema>
    <schemaversion>1.2</schemaversion>
  </metadata>
  <organizations default="org-1">
    <organization identifier="org-1">
      <title>Название курса</title>
      <item identifier="item-1" identifierref="res-1" isvisible="true">
        <title>Название курса</title>
      </item>
    </organization>
  </organizations>
  <resources>
    <resource identifier="res-1" type="webcontent" adlcp:scormtype="sco" href="index.html">
      <file href="index.html"/>
      <file href="assets/style.css"/>
      <!-- каждый файл в архиве -->
    </resource>
  </resources>
</manifest>
```

Каждый файл в ZIP должен быть указан как `<file>` в ресурсе.

### Трекинг прогресса

- При загрузке: `API.LMSInitialize("")`, прочитать `cmi.suspend_data` (посещённые страницы)
- При просмотре страницы: сохранить индекс в `cmi.suspend_data`, обновить `cmi.core.score.raw`
- При завершении: `cmi.core.lesson_status = "completed"` когда все страницы просмотрены
- При выгрузке: `API.LMSFinish("")`
- Помечать страницу прочтенной только если юзер долистал до конца страницы

API объект находится в parent/opener window — нужно пройти по иерархии фреймов.

## Загрузка в LMS

1. Course management → Create course → отметить **SCORM course**
2. Загрузить `.zip`

## Проверка

Локально без LMS — открыть `scorm_build/index.html` в браузере. Трекинг не работает, но навигация и контент — да.

Проверить большие файлы в архиве:

```bash
unzip -l course.zip | sort -k1 -n | tail -20
```

## Проблемы

**MD не конвертируется в HTML** — попросить агента написать скрипт для поиска и исправления сломанного форматирования.

**Mermaid показывается как код** — не установлен mermaid CLI или Chromium.

**LMS отклоняет файл (too large)** — файл внутри ZIP > 1 МБ. Найти через `unzip -l` и сжать.

**Большой ZIP** — SVG от mermaid бывают тяжёлые. Использовать `ZIP_DEFLATED`, упростить диаграммы.

**Ошибки кодировки** — все `.md` должны быть UTF-8. Проверить: `file -i course/**/*.md`.
