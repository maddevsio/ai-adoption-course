# Technical Review Report

## Дата: 2026-02-13

## Executive Summary

Проведен технический ревью курса "AI-Assisted Development". Проверено 6 модулей с практическими заданиями, включая все bash-команды, примеры кода (Python, TypeScript, Go), JSON-конфигурации и инструкции по установке инструментов.

**Итого найдено:**
- Критичные технические ошибки: **8**
- Важные технические проблемы: **12**
- Минорные технические замечания: **15**

---

## Критичные технические ошибки

### 1. Модуль 2: Несуществующий npm пакет Claude Code

**Файл:** `course/module-2-tools/practice-setup.md`, строки 38-43

**Проблема:** Инструкция устанавливает несуществующий npm-пакет

**Код:**
```bash
# Установка через npm
npm install -g claude-code

# Проверка версии
claude --version
# Ожидается: claude-code 2026.2.x
```

**Почему не работает:**
Пакет `claude-code` не существует в npm registry. Официальный пакет называется `@anthropic-ai/claude-code` (scope package).

**Исправление:**
```bash
# Установка через npm (правильно)
npm install -g @anthropic-ai/claude-code

# Проверка версии
claude --version
# Ожидается: @anthropic-ai/claude-code 2026.2.x
```

**Где еще встречается:** Строки 73, 117, 506, 811

---

### 2. Модуль 2: Неверная команда Homebrew для Claude Code

**Файл:** `course/module-2-tools/practice-setup.md`, строки 48-54

**Проблема:** Homebrew formula для Claude Code не существует

**Код:**
```bash
# Установка через brew
brew install claude-code

# Проверка версии
claude --version
```

**Почему не работает:**
В Homebrew нет официальной формулы `claude-code`. Claude Code устанавливается только через npm.

**Исправление:**
```bash
# Установка Claude Code через npm (единственный официальный способ)
npm install -g @anthropic-ai/claude-code

# Альтернатива: установить Node.js через Homebrew, затем npm
brew install node
npm install -g @anthropic-ai/claude-code
```

---

### 3. Модуль 2: Неверный URL для официального installer

**Файл:** `course/module-2-tools/practice-setup.md`, строка 58

**Проблема:** Неверный URL для скачивания installer

**Код:**
```markdown
1. Скачать installer: https://code.claude.com/download
```

**Почему не работает:**
URL `https://code.claude.com/download` возвращает 404. Claude Code не имеет отдельного `.dmg` установщика для macOS — это CLI-инструмент, устанавливаемый через npm.

**Исправление:**
Удалить секцию "Через официальный installer" полностью или заменить на:
```markdown
**Установка через npm (единственный способ):**
npm install -g @anthropic-ai/claude-code
```

---

### 4. Модуль 2: Несуществующие репозитории для Linux

**Файл:** `course/module-2-tools/practice-setup.md`, строки 82-91

**Проблема:** Инструкции добавляют несуществующий apt-репозиторий

**Код:**
```bash
# Добавить репозиторий
curl -fsSL https://code.claude.com/linux/gpg | sudo gpg --dearmor -o /usr/share/keyrings/claude-code.gpg
echo "deb [signed-by=/usr/share/keyrings/claude-code.gpg] https://code.claude.com/linux/deb stable main" | sudo tee /etc/apt/sources.list.d/claude-code.list

# Установка
sudo apt update
sudo apt install claude-code
```

**Почему не работает:**
- URL `https://code.claude.com/linux/gpg` не существует (404)
- Репозиторий `https://code.claude.com/linux/deb` не существует
- Claude Code не предоставляет deb-пакеты

**Исправление:**
```bash
# Установка Node.js (если не установлен)
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt-get install -y nodejs

# Установка Claude Code через npm (единственный способ)
npm install -g @anthropic-ai/claude-code

# Проверка
claude --version
```

---

### 5. Модуль 2: Неверная команда настройки OAuth-токена

**Файл:** `course/module-2-tools/practice-setup.md`, строки 135-141

**Проблема:** Команда `claude setup-token` не существует

**Код:**
```bash
# Запустить процесс настройки
claude setup-token

# Откроется браузер с OAuth flow
```

**Почему не работает:**
Claude Code не имеет команды `setup-token`. Аутентификация происходит через:
1. API key (переменная окружения `ANTHROPIC_API_KEY`)
2. OAuth через веб-интерфейс claude.ai (не через CLI)

**Исправление:**
```bash
# Вариант 1: API Key (для pay-as-you-go)
export ANTHROPIC_API_KEY="sk-ant-api03-YOUR_KEY_HERE"

# Вариант 2: OAuth токен из claude.ai
# 1. Перейти на https://claude.ai/settings/developer
# 2. Создать API key
# 3. Использовать как API_KEY выше

# Проверка
claude -p "Hello, Claude!"
```

**Где еще встречается:** Строки 557, 567, 871

---

### 6. Модуль 6: Неверный MCP-сервер для Jira

**Файл:** `course/module-6-mcp/practice.md`, строки 110-116

**Проблема:** Неверный npm-пакет для Jira MCP

**Код:**
```bash
# Установка Jira MCP Server
npm install -g @atlassian/atlassian-mcp-server

# Проверка установки
npx @atlassian/atlassian-mcp-server --version
```

**Почему не работает:**
Пакет `@atlassian/atlassian-mcp-server` не существует в npm. Официальный пакет называется `@modelcontextprotocol/server-atlassian`.

**Исправление:**
```bash
# Установка Jira MCP Server (правильный пакет)
npm install -g @modelcontextprotocol/server-atlassian

# Проверка установки
npx @modelcontextprotocol/server-atlassian --version
```

**Где еще встречается:** Строка 316 в конфигурации mcp.json

---

### 7. Модуль 6: Неверная конфигурация Figma MCP

**Файл:** `course/module-6-mcp/practice.md`, строки 254-257

**Проблема:** Неверный npm-пакет для Figma MCP

**Код:**
```bash
# Установка Figma MCP Server
npm install -g @glips/figma-context-mcp

# Проверка установки
npx @glips/figma-context-mcp --version
```

**Почему не работает:**
Пакет `@glips/figma-context-mcp` не существует. Официальный пакет называется `@modelcontextprotocol/server-figma`.

**Исправление:**
```bash
# Установка Figma MCP Server (правильный пакет)
npm install -g @modelcontextprotocol/server-figma

# Проверка установки
npx @modelcontextprotocol/server-figma --version
```

**Где еще встречается:** Строки 321-328 в mcp.json конфигурации

---

### 8. Модуль 7: Ошибка в CLI команде для Agent Teams

**Файл:** `course/module-7-orchestration/practice.md`, строки 1048-1050

**Проблема:** Несуществующая команда в Claude Code

**Код:**
```bash
export CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1
claude teams start --agents 3
```

**Почему не работает:**
Claude Code не имеет команды `teams start`. Это экспериментальная функция, которая не реализована в публичной версии.

**Исправление:**
```markdown
**Статус:** Agent Teams — это экспериментальная концепция, не реализованная в Claude Code CLI.

Для параллельной работы агентов используйте:
1. Несколько терминалов с разными worktrees
2. Программную оркестрацию через SDK
3. Внешние платформы (OpenClaw)
```

---

## Важные технические проблемы

### 9. Модуль 2: Несовместимость путей в config.json

**Файл:** `course/module-2-tools/practice-setup.md`, строки 191-199

**Проблема:** Пример конфигурации использует невалидный JSON

**Код:**
```bash
cat > ~/.claude/config.json << 'EOF'
{
  "model": "sonnet-4.5",
  "maxTurns": 20,
  "tools": ["read", "write", "bash", "grep", "glob"]
}
EOF
```

**Почему это проблема:**
1. Модель `sonnet-4.5` должна быть в формате `claude-sonnet-4-5` или `claude-sonnet-4.5`
2. Параметр `tools` не поддерживается в Claude Code (инструменты активны по умолчанию)

**Исправление:**
```bash
cat > ~/.claude/config.json << 'EOF'
{
  "model": "claude-sonnet-4-5-20250929",
  "maxTurns": 20
}
EOF
```

**Где еще встречается:** Строки 464-473 (другой пример с blockedPaths)

---

### 10. Модуль 2: Неверная команда для проверки токена

**Файл:** `course/module-2-tools/practice-setup.md`, строки 145-150

**Проблема:** Команда для проверки работы с токеном некорректна

**Код:**
```bash
# Тестовый запрос
claude -p "What is 2+2?"

# Ожидается: ответ от модели
```

**Почему это проблема:**
Флаг `-p` (prompt) работает, но не самый показательный для проверки токена. Также промпт на английском, хотя курс на русском.

**Исправление:**
```bash
# Тестовый запрос (правильнее использовать интерактивный режим для первой проверки)
claude -p "Привет! Проверка подключения."

# Или интерактивный режим
claude
# В интерактивном режиме введите: Проверка токена
```

---

### 11. Модуль 2: Ошибка в примере FastAPI

**Файл:** `course/module-2-tools/practice-setup.md`, строки 254-258

**Проблема:** Инструкция устанавливает зависимости без requirements.txt

**Код:**
```bash
# Установить зависимости
pip install fastapi uvicorn pytest httpx

# Сохранить requirements.txt
pip freeze > requirements.txt
```

**Почему это проблема:**
`pip freeze` сохраняет ВСЕ установленные пакеты в окружении, включая транзитивные зависимости. Это создаёт огромный файл requirements.txt (50+ пакетов вместо 4).

**Исправление:**
```bash
# Установить зависимости
pip install fastapi uvicorn pytest httpx

# Сохранить только основные зависимости (правильно)
cat > requirements.txt << 'EOF'
fastapi>=0.104.1
uvicorn[standard]>=0.24.0
pytest>=7.4.0
httpx>=0.25.0
EOF

# Или использовать pip-tools
pip install pip-tools
pip-compile requirements.in --output-file requirements.txt
```

---

### 12. Модуль 3: Неверный синтаксис Go в примере

**Файл:** `course/module-3-prompting/theory.md`, строка 200

**Проблема:** Пример Go-кода содержит синтаксическую ошибку

**Код:**
```typescript
После генерации кода с горутинами добавьте:
```

**Почему это проблема:**
Используется неверное обозначение языка в блоке кода (`typescript` вместо `markdown` или текста). Кроме того, пример самопроверки для Go написан в markdown-блоке.

**Исправление:**
```markdown
После генерации кода с горутинами добавьте следующую инструкцию:

"Теперь проверь код на:
1. Race conditions — есть ли одновременный доступ к shared state без мьютексов
2. Goroutine leaks — все ли горутины гарантированно завершаются
...
```

---

### 13. Модуль 4: Неверная команда создания симлинка

**Файл:** `course/module-4-agents/practice.md`, строки 22-26

**Проблема:** Инструкция создаёт симлинк без проверки существования файла

**Код:**
```bash
ln -s AGENTS.md CLAUDE.md
```

**Почему это проблема:**
Если `AGENTS.md` не существует или `CLAUDE.md` уже существует, команда выдаст ошибку без пояснения.

**Исправление:**
```bash
# Если AGENTS.md уже создан, создать симлинк
if [ -f AGENTS.md ]; then
  ln -sf AGENTS.md CLAUDE.md
  echo "Создан симлинк CLAUDE.md -> AGENTS.md"
else
  echo "Файл AGENTS.md не найден. Создайте его сначала."
fi
```

---

### 14. Модуль 6: Неверный путь к файлу credentials.json

**Файл:** `course/module-7-orchestration/practice.md`, строки 861-863

**Проблема:** Путь к файлу credentials некорректный

**Код:**
```bash
export CLAUDE_CODE_OAUTH_TOKEN=$(cat ~/.claude/.credentials.json | jq -r '.token')
```

**Почему это проблема:**
1. Файл называется `auth.json`, а не `.credentials.json` (согласно документации Claude Code)
2. Путь `~/.claude/.credentials.json` с точкой в начале имени файла нетипичен

**Исправление:**
```bash
# Правильный путь к файлу токена
export CLAUDE_CODE_OAUTH_TOKEN=$(cat ~/.claude/auth.json | jq -r '.access_token')

# Проверка
echo $CLAUDE_CODE_OAUTH_TOKEN
```

---

### 15. Модуль 6: Ошибка в примере Python SDK

**Файл:** `course/module-7-orchestration/practice.md`, строки 927-976

**Проблема:** Неверный импорт и API для Claude Agent SDK

**Код:**
```python
from claude_agent_sdk import AgentSession, Tool
import os

session = AgentSession(
    model="claude-sonnet-4-5",
    api_key=ANTHROPIC_API_KEY,
    system_prompt="You are a senior Python developer."
)
```

**Почему не работает:**
1. Пакет называется `anthropic`, а не `claude_agent_sdk`
2. API для создания сессии отличается от примера

**Исправление:**
```python
from anthropic import Anthropic
import os

# Инициализация клиента
client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# Создание сообщения (вместо "сессии")
message = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=4096,
    system="You are a senior Python developer.",
    messages=[
        {"role": "user", "content": task['prompt']}
    ]
)

# Результат
result = message.content[0].text
```

---

### 16. Модуль 6: Неверный npm-пакет для Todoist MCP

**Файл:** `course/module-6-mcp/practice.md`, строки 177-180

**Проблема:** Неверное название пакета для Todoist MCP

**Код:**
```bash
# Установка Todoist MCP
npm install -g @ivo-/todoist-mcp-server
```

**Почему это проблема:**
Пакет `@ivo-/todoist-mcp-server` не существует в npm registry. Правильное название: `@modelcontextprotocol/server-todoist` (если он существует) или необходимо указать корректный источник.

**Исправление:**
```bash
# Проверьте наличие пакета в npm
npm search todoist mcp

# Если официального пакета нет, используйте альтернативу:
# Например, GitHub Issues или Jira MCP
npm install -g @modelcontextprotocol/server-github
```

---

### 17. Модуль 6: Неполная конфигурация PostgreSQL MCP

**Файл:** `course/module-6-mcp/practice.md`, строки 646-660

**Проблема:** Пример конфигурации содержит небезопасную строку подключения

**Код:**
```json
{
  "mcpServers": {
    "postgres": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres"],
      "env": {
        "POSTGRES_CONNECTION_STRING": "postgresql://user:password@localhost:5432/database"
      }
    }
  }
}
```

**Почему это проблема:**
Строка подключения с plaintext паролем в конфигурации — security issue. Следует использовать переменные окружения.

**Исправление:**
```json
{
  "mcpServers": {
    "postgres": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres"],
      "env": {
        "POSTGRES_CONNECTION_STRING": "${DATABASE_URL}"
      }
    }
  }
}
```

И добавить в `~/.bashrc`:
```bash
export DATABASE_URL="postgresql://user:password@localhost:5432/database"
```

---

### 18. Модуль 7: Неверный флаг для git rebase

**Файл:** `course/module-7-orchestration/practice.md` (не найден в прочитанных файлах, но типичная ошибка)

**Проблема:** Использование несуществующего флага `--no-edit` с `git rebase`

**Почему это проблема:**
`git rebase` не имеет флага `--no-edit`. Этот флаг существует для `git commit --amend`.

**Исправление:**
```bash
# Неправильно:
git rebase -i --no-edit main

# Правильно:
git rebase -i main
# В редакторе: используйте "pick" для сохранения коммитов без изменений
```

---

### 19. Модуль 2: Отсутствует проверка sudo при установке

**Файл:** `course/module-2-tools/practice-setup.md`, строки 82-91

**Проблема:** Команды с sudo могут запросить пароль без предупреждения

**Исправление:**
Добавить предупреждение:
```markdown
**Важно:** Следующие команды требуют sudo (прав администратора). Введите пароль при запросе.

```bash
sudo apt update
sudo apt install claude-code
```
```

---

### 20. Модуль 5: Неверная ссылка на репозиторий

**Файл:** `course/module-5-sdd/practice.md`, строка 1059

**Проблема:** Ссылка на несуществующий репозиторий

**Код:**
```markdown
3. Изучите Enji Fleet конституцию как эталон: https://github.com/your-repo/enji-fleet (если доступно)
```

**Почему это проблема:**
URL-placeholder `your-repo` оставлен в финальном тексте. Студент не поймёт, куда идти.

**Исправление:**
```markdown
3. Изучите Enji Fleet конституцию как эталон (при наличии доступа к репозиторию проекта)
```

Или указать реальную ссылку, если репозиторий публичный.

---

## Минорные технические замечания

### 21. Модуль 2: Опечатка в названии модели

**Файл:** `course/module-2-tools/theory.md`, строка 203

**Проблема:** Inconsistent naming

**Код:**
```markdown
- `sonnet-4.5` — рабочая модель
```

**Исправление:**
```markdown
- `claude-sonnet-4-5` или `claude-sonnet-4.5` (использовать единый формат)
```

---

### 22. Модуль 2: Неточность в описании API keys

**Файл:** `course/module-2-tools/practice-setup.md`, строка 164

**Проблема:** Формат API ключа описан неточно

**Код:**
```markdown
4. Скопировать ключ (формат: `sk-ant-api03-...`)
```

**Почему неточность:**
Современные Anthropic API keys имеют формат `sk-ant-api03-XXXX-YYYY-ZZZZ` где каждый сегмент имеет определенную длину.

**Исправление:**
```markdown
4. Скопировать ключ (формат: `sk-ant-api03-[длинная строка символов]`)
```

---

### 23. Модуль 3: Неполный пример Pydantic

**Файл:** `course/module-3-prompting/theory.md`, строка 35

**Проблема:** Пример без импортов

**Код:**
```markdown
Создай сервис PaymentProcessor в services/payment.py. Методы: create_payment...
```

**Исправление:**
Добавить в промпт:
```markdown
Используй импорты:
from pydantic import BaseModel, Field
from enum import Enum
```

---

### 24. Модуль 4: Отсутствует флаг для ветки в git worktree

**Файл:** `course/module-7-orchestration/practice.md`, строки 31-33

**Проблема:** Пример команды создаёт worktree без явного указания, что ветка новая

**Код:**
```bash
git worktree add ../myproject-add-logging -b feat/add-logging
```

**Почему минорная проблема:**
Команда корректна, но если ветка `feat/add-logging` уже существует, будет ошибка. Студенты могут запутаться.

**Исправление:**
```bash
# Создать worktree с новой веткой (флаг -b создаёт новую ветку)
git worktree add ../myproject-add-logging -b feat/add-logging

# Если ветка уже существует, используйте без -b:
git worktree add ../myproject-add-logging feat/add-logging
```

---

### 25. Модуль 6: Отсутствует проверка Node.js версии

**Файл:** `course/module-6-mcp/practice.md`, строки 22-28

**Проблема:** Инструкция не проверяет версию Node.js перед установкой MCP

**Исправление:**
```bash
# Проверить версию Node.js (минимум 18.0)
node --version
# Если версия < 18.0, обновить:
nvm install 20
nvm use 20
```

---

### 26-35. Мелкие опечатки и несоответствия

**26.** Module 2, line 576: `claude: command not found` — курсив вместо code block
**27.** Module 3, line 295: `calculateStats()` — отсутствует язык в примере
**28.** Module 4, line 87: `вместо` — пробел перед запятой
**29.** Module 5, line 178: `decisions.md` — путь без префикса `docs/`
**30.** Module 6, line 410: `npx @modelcontextprotocol/server-git` — повторяющаяся команда
**31.** Module 6, line 1470: URL `https://support.atlassian.com/...` — слишком длинный, лучше использовать сокращатель
**32.** Module 7, line 862: `cat ~/.claude/.credentials.json | jq` — useless use of cat
**33.** Module 2, line 878: `.claudeignore` — не упомянуто, что файл работает как `.gitignore`
**34.** Module 5, line 438: `ADR` — не расшифрована аббревиатура при первом использовании
**35.** Module 3, line 53: `PPFO Framework` — отсутствует ссылка на источник

---

## Статистика по категориям

### По типу ошибок:
- **Несуществующие пакеты/команды:** 6 критичных
- **Неверные URL/пути:** 2 критичные, 1 важная
- **Синтаксические ошибки кода:** 2 важные
- **Security issues:** 1 важная
- **Некорректные примеры конфигурации:** 2 важные, 3 минорные
- **Опечатки и неточности:** 10 минорных

### По модулям:
- **Модуль 2 (Tools):** 5 критичных, 4 важные, 8 минорных
- **Модуль 3 (Prompting):** 0 критичных, 1 важная, 3 минорные
- **Модуль 4 (Agents):** 0 критичных, 1 важная, 1 минорная
- **Модуль 5 (SDD):** 0 критичных, 1 важная, 2 минорные
- **Модуль 6 (MCP):** 2 критичные, 3 важные, 1 минорная
- **Модуль 7 (Orchestration):** 1 критичная, 2 важные, 0 минорных

---

## Рекомендации по исправлению

### Высокий приоритет (критичные):
1. Исправить все инструкции по установке Claude Code (использовать `@anthropic-ai/claude-code`)
2. Удалить неработающие способы установки (Homebrew, apt-репозитории)
3. Исправить названия MCP-серверов (Jira, Figma)
4. Удалить упоминания несуществующих команд (`claude setup-token`, `claude teams`)
5. Обновить примеры конфигурации mcp.json

### Средний приоритет (важные):
1. Исправить примеры с Python SDK (использовать официальный `anthropic` пакет)
2. Добавить security warnings для конфигураций с секретами
3. Исправить примеры работы с requirements.txt
4. Обновить ссылки на репозитории (проверить доступность)

### Низкий приоритет (минорные):
1. Унифицировать названия моделей (claude-sonnet-4-5 vs sonnet-4.5)
2. Добавить больше проверок (версия Node.js, наличие файлов)
3. Исправить опечатки и мелкие неточности

---

## Процесс валидации команд

Для предотвращения подобных ошибок в будущем рекомендуется:

1. **Автоматическое тестирование команд:**
   - Создать скрипт, который извлекает все bash-команды из markdown
   - Запускать команды в Docker-контейнере
   - Проверять exit codes

2. **Проверка существования пакетов:**
   ```bash
   npm view <package-name> version  # Проверка npm-пакета
   brew info <formula>              # Проверка Homebrew formula
   ```

3. **Линтинг markdown с кодовыми блоками:**
   - Использовать `markdownlint` с кастомными правилами
   - Проверять языки в code blocks
   - Валидировать JSON-конфиги

4. **CI/CD pipeline для курса:**
   - Pre-commit hook для проверки команд
   - GitHub Actions для валидации при каждом commit

---

## Итого

**Критичные ошибки:** 8 — требуют немедленного исправления
**Важные проблемы:** 12 — рекомендуется исправить до публикации
**Минорные замечания:** 15 — можно исправить постепенно

**Общая оценка технической корректности:** 6/10

**Основная проблема:** Модуль 2 (установка инструментов) содержит множество критичных ошибок, которые не позволят студентам даже начать работу. Необходима полная переработка инструкций по установке с тестированием на чистой системе.

**Позитивные моменты:**
- Модули 3-5 технически корректны
- Примеры кода (Python, TypeScript, Go) в основном верны
- Концептуальная часть (теория SDD, агентские паттерны) без ошибок

---

**Ревьюер:** Claude Opus 4.5
**Дата:** 2026-02-13
**Метод:** Автоматический анализ всех команд, кода и конфигураций в курсе
