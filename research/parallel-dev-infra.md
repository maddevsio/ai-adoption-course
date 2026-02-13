# Инфраструктура параллельной разработки с AI-агентами

> Последнее обновление: 12 февраля 2026

## Обзор

Параллельная разработка с AI-агентами — ключевая компетенция **Уровней 5-6** по классификации Steve Yegge. Этот документ описывает инфраструктуру, инструменты и паттерны для запуска и управления несколькими агентами одновременно.

---

## 1. Claude Code Headless Mode

### Назначение

Headless режим позволяет запускать Claude Code без интерактивного UI — через скрипты, CI/CD, или оркестраторы. Это основа для автоматизации и параллельного запуска агентов.

### Основные возможности

#### Флаги командной строки

```bash
# Базовый headless запуск
claude -p "Fix all linting errors in src/" --output-format json

# Ограничение инструментов (безопасность)
claude -p "Review code" --allowedTools read,grep --max-turns 5

# Возобновление сессии
claude --resume <session-id> -p "Continue previous task"

# Установка модели
claude -p "Implement feature" --model sonnet-4.5
```

#### Параметры

| Параметр | Описание | Пример |
|----------|----------|--------|
| `-p, --prompt` | Промпт для агента | `-p "Fix bug #123"` |
| `--output-format` | Формат вывода (text/json) | `--output-format json` |
| `--allowedTools` | Ограничение доступных инструментов | `--allowedTools read,write,bash` |
| `--max-turns` | Максимум итераций агента | `--max-turns 10` |
| `--resume` | Возобновить сессию | `--resume abc123` |
| `--model` | Выбор модели | `--model opus-4.6` |
| `--no-confirm` | Без подтверждений (YOLO) | `--no-confirm` |

#### JSON Output для парсинга

```json
{
  "session_id": "abc123",
  "status": "completed",
  "turns": 5,
  "files_changed": [
    "src/auth.py",
    "tests/test_auth.py"
  ],
  "commands_run": [
    "pytest tests/test_auth.py",
    "black src/auth.py"
  ],
  "cost": {
    "input_tokens": 12500,
    "output_tokens": 8300,
    "usd": 0.42
  },
  "result": "Successfully fixed authentication bug"
}
```

### Use Cases

**CI/CD интеграция:**
```bash
# В GitHub Actions / GitLab CI
claude -p "Review PR changes and suggest improvements" \
  --output-format json \
  --max-turns 3 \
  --allowedTools read,grep > review.json
```

**Parallel task execution:**
```bash
# Запуск 3 агентов параллельно
claude -p "Fix linting in frontend/" --output-format json > frontend.json &
claude -p "Fix linting in backend/" --output-format json > backend.json &
claude -p "Update documentation" --output-format json > docs.json &
wait
```

**Документация:** https://code.claude.com/docs/en/headless

---

## 2. Claude Code в облаке

### claude.ai/code/ — Облачный сервис

**Основной способ** работы с Claude Code в облаке — это облачный сервис [https://claude.ai/code/](https://claude.ai/code/), который не требует разворачивания своей инфраструктуры.

**Возможности:**
- Запуск агентов прямо в браузере
- Shared sessions для командной работы
- Интеграция с GitHub для PR review
- Автоматический sandboxing и изоляция
- Хранение сессий и истории работы
- Доступ к команде через shared workspaces

**Использование для параллельной разработки:**
- Откройте несколько вкладок с разными задачами
- Каждая сессия работает в изолированном контексте
- Результаты можно экспортировать и мержить локально

**Преимущества:**
- Не нужно управлять инфраструктурой
- Всегда последняя версия Claude Code
- Безопасность из коробки
- Shared sessions для code review

**Документация:** https://claude.ai/code/

### Docker (Self-hosting)

Для тех, кому нужен self-hosting, Claude Code поддерживает Docker.

```dockerfile
FROM anthropics/claude-code:latest
COPY . .
CMD ["claude", "-p", "$TASK", "--output-format", "json"]
```

**Документация:** https://docs.docker.com/ai/sandboxes/claude-code/

---

## 3. Аутентификация и токены

### ANTHROPIC_API_KEY

Прямой API-биллинг. Подходит для production и автоматизации.

```bash
export ANTHROPIC_API_KEY="sk-ant-api03-..."
claude -p "Task" # Использует API key
```

**Плюсы:**
- Полный контроль над биллингом
- Подходит для CI/CD
- Централизованное управление в команде

**Минусы:**
- Платите за каждый токен
- Нужно управлять ключами

### OAuth токен (claude setup-token)

1-годовой OAuth токен для подписчиков Claude Max.

```bash
claude setup-token  # Открывает браузер для авторизации
# Токен сохраняется в ~/.claude/config
```

**Плюсы:**
- Включено в подписку Max ($100-200/мес)
- Не нужно управлять API ключами
- Годовая валидность

**Минусы:**
- Только для индивидуальных пользователей
- Нельзя использовать в CI/CD (требует браузер)

### CLAUDE_CODE_OAUTH_TOKEN

Переменная окружения для OAuth токена (для скриптов).

```bash
export CLAUDE_CODE_OAUTH_TOKEN="<token from setup-token>"
claude -p "Task"  # Использует OAuth
```

### Cloud backends

#### AWS Bedrock

```bash
export CLAUDE_CODE_USE_BEDROCK=1
export AWS_REGION=us-east-1
export AWS_ACCESS_KEY_ID=...
export AWS_SECRET_ACCESS_KEY=...

claude -p "Task"  # Через Bedrock
```

**Плюсы:**
- Enterprise compliance
- Использование AWS credits
- Data residency control

#### Google Cloud Vertex AI

```bash
export CLAUDE_CODE_USE_VERTEX=1
export GOOGLE_CLOUD_PROJECT=my-project
export GOOGLE_APPLICATION_CREDENTIALS=/path/to/key.json

claude -p "Task"  # Через Vertex AI
```

#### Azure Foundry

```bash
export CLAUDE_CODE_USE_AZURE=1
export AZURE_SUBSCRIPTION_ID=...
export AZURE_RESOURCE_GROUP=...

claude -p "Task"  # Через Azure
```

**Документация:** https://code.claude.com/docs/en/authentication

---

## 4. Claude Agent SDK

Программируемый доступ к возможностям Claude Code для создания кастомных оркестраторов.

### Python SDK

#### Установка
```bash
pip install claude-agent-sdk
```

#### Пример: Простой агент
```python
from claude_agent import Agent

agent = Agent(
    model="sonnet-4.5",
    api_key="sk-ant-api03-...",
    tools=["read", "write", "bash"]
)

result = agent.run("Fix linting errors in src/")
print(result.files_changed)
print(f"Cost: ${result.cost_usd:.2f}")
```

#### Пример: Multi-agent orchestration
```python
import asyncio
from claude_agent import Agent

async def parallel_agents():
    # Создаем 3 агента с разными задачами
    agent1 = Agent(model="sonnet-4.5")
    agent2 = Agent(model="haiku-4.5")  # Дешевый для простых задач
    agent3 = Agent(model="opus-4.6")   # Умный для архитектуры

    # Запускаем параллельно
    tasks = [
        agent1.run_async("Implement feature A"),
        agent2.run_async("Generate tests"),
        agent3.run_async("Review architecture"),
    ]

    results = await asyncio.gather(*tasks)

    for i, result in enumerate(results):
        print(f"Agent {i+1}: {result.status}")
        print(f"  Files: {result.files_changed}")
        print(f"  Cost: ${result.cost_usd:.2f}")

asyncio.run(parallel_agents())
```

#### Пример: Custom workflow
```python
from claude_agent import Agent, Workflow

# Определяем workflow
workflow = Workflow([
    {
        "name": "planning",
        "agent": Agent(model="opus-4.6"),
        "prompt": "Analyze codebase and create plan",
        "output_to": "plan.md"
    },
    {
        "name": "implementation",
        "agent": Agent(model="sonnet-4.5"),
        "prompt": "Implement based on {plan.md}",
        "parallel": 3  # 3 параллельных агента
    },
    {
        "name": "review",
        "agent": Agent(model="sonnet-4.5"),
        "prompt": "Review all changes",
        "depends_on": ["implementation"]
    }
])

result = workflow.run()
print(f"Total cost: ${result.total_cost:.2f}")
print(f"Time: {result.duration_seconds}s")
```

### TypeScript SDK

#### Установка
```bash
npm install @anthropic-ai/claude-agent-sdk
```

#### Пример
```typescript
import { Agent, Workflow } from '@anthropic-ai/claude-agent-sdk';

const agent = new Agent({
  model: 'sonnet-4.5',
  apiKey: process.env.ANTHROPIC_API_KEY,
  tools: ['read', 'write', 'bash']
});

const result = await agent.run('Fix bug #123');
console.log(`Changed files: ${result.filesChanged.join(', ')}`);
console.log(`Cost: $${result.costUsd.toFixed(2)}`);
```

#### V2 SDK (Simplified)

Новый V2 SDK убирает async generators для более простого API.

```typescript
import { Agent } from '@anthropic-ai/claude-agent-sdk/v2';

const agent = new Agent({ model: 'sonnet-4.5' });

// Каждый turn — отдельный send()/stream()
const turn1 = await agent.send('Analyze this code');
const turn2 = await agent.send('Now refactor it');
const turn3 = await agent.send('Add tests');

console.log(`Total cost: $${agent.totalCost.toFixed(2)}`);
```

**Документация:** https://platform.claude.com/docs/en/agent-sdk/overview

**GitHub:**
- Python: https://github.com/anthropics/claude-agent-sdk-python
- TypeScript: https://github.com/anthropics/claude-agent-sdk-typescript

---

## 5. Agent Teams (Experimental)

**Статус:** Experimental feature, требует флаг `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`

### Концепция

Agent Teams позволяют нескольким агентам работать вместе над одной задачей:
- **Shared task list** с зависимостями
- **Inter-agent messaging** для координации
- **Parallel execution** независимых задач
- **Automatic coordination** через shared state

### Включение

```bash
export CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1
claude teams create my-project
```

### Пример: Feature development team

```yaml
# team-config.yaml
team:
  name: "Feature Implementation Team"
  shared_context:
    - README.md
    - docs/architecture.md

  agents:
    - name: architect
      model: opus-4.6
      role: "Analyze requirements and create implementation plan"

    - name: backend-dev
      model: sonnet-4.5
      role: "Implement backend code based on plan"
      depends_on: [architect]

    - name: frontend-dev
      model: sonnet-4.5
      role: "Implement frontend code based on plan"
      depends_on: [architect]

    - name: tester
      model: haiku-4.5
      role: "Generate tests for implemented code"
      depends_on: [backend-dev, frontend-dev]

    - name: reviewer
      model: sonnet-4.5
      role: "Review all code and suggest improvements"
      depends_on: [tester]
```

```bash
claude teams run team-config.yaml
```

### Координационные режимы

1. **Sequential**: Агенты работают по очереди (default)
2. **Parallel**: Агенты работают одновременно где возможно
3. **Dynamic**: Агенты сами решают когда им работать

### Shared task list

Агенты видят общий список задач и могут:
- Добавлять подзадачи
- Помечать задачи выполненными
- Блокировать задачи до завершения зависимостей

### Inter-agent messaging

```python
# Агент 1 отправляет сообщение агенту 2
agent.send_message(
    to="backend-dev",
    message="API endpoint /users ready, proceed with frontend"
)

# Агент 2 получает и обрабатывает
messages = agent.receive_messages()
for msg in messages:
    print(f"From {msg.from}: {msg.content}")
```

**Документация:** https://code.claude.com/docs/en/agent-teams

---

## 6. GitHub Actions Integration

Интеграция Claude Code в CI/CD пайплайны.

### Базовый пример

```yaml
# .github/workflows/ai-review.yml
name: AI Code Review

on:
  pull_request:
    types: [opened, synchronize]

jobs:
  ai-review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Claude Code Review
        uses: anthropics/claude-code-action@v1
        with:
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
          prompt: |
            Review this PR for:
            - Code quality and best practices
            - Security issues
            - Performance concerns
            - Test coverage
          model: sonnet-4.5
          max_turns: 5

      - name: Post review as comment
        uses: actions/github-script@v7
        with:
          script: |
            const fs = require('fs');
            const review = fs.readFileSync('claude-review.md', 'utf8');
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: review
            });
```

### Multi-agent CI/CD

```yaml
# .github/workflows/ai-multi-agent.yml
name: Multi-Agent Development

on:
  workflow_dispatch:
    inputs:
      task:
        description: 'High-level task description'
        required: true

jobs:
  planning:
    runs-on: ubuntu-latest
    outputs:
      plan: ${{ steps.plan.outputs.result }}
    steps:
      - uses: actions/checkout@v4
      - name: Create plan
        id: plan
        uses: anthropics/claude-code-action@v1
        with:
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
          prompt: "Create detailed implementation plan: ${{ inputs.task }}"
          model: opus-4.6
          output_format: json

  implementation:
    needs: planning
    runs-on: ubuntu-latest
    strategy:
      matrix:
        component: [backend, frontend, tests, docs]
    steps:
      - uses: actions/checkout@v4
      - name: Implement ${{ matrix.component }}
        uses: anthropics/claude-code-action@v1
        with:
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
          prompt: |
            Implement ${{ matrix.component }} based on this plan:
            ${{ needs.planning.outputs.plan }}
          model: sonnet-4.5

  review:
    needs: implementation
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Review all changes
        uses: anthropics/claude-code-action@v1
        with:
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
          prompt: "Review all implemented changes for quality and consistency"
          model: sonnet-4.5
```

### Scheduled automation

```yaml
# .github/workflows/nightly-refactor.yml
name: Nightly Refactoring

on:
  schedule:
    - cron: '0 2 * * *'  # 2 AM daily

jobs:
  refactor:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Find code smells
        uses: anthropics/claude-code-action@v1
        with:
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
          prompt: "Identify code smells and suggest refactorings"
          model: sonnet-4.5

      - name: Auto-fix linting
        uses: anthropics/claude-code-action@v1
        with:
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
          prompt: "Fix all linting errors"
          model: haiku-4.5  # Cheap for simple tasks

      - name: Create PR with changes
        if: steps.refactor.outputs.files_changed != '[]'
        uses: peter-evans/create-pull-request@v5
        with:
          title: "🤖 Automated refactoring"
          body: "Auto-generated by Claude Code"
          branch: auto-refactor-${{ github.run_number }}
```

**Документация:** https://code.claude.com/docs/en/github-actions

---

## 7. OpenClaw

Open-source multi-agent orchestration framework.

### Архитектура

OpenClaw — это Go-based фреймворк для запуска множества AI-агентов с:
- **Multi-agent routing**: Сообщения маршрутизируются к нужным агентам
- **Isolated workspaces**: Каждый агент имеет свою директорию
- **Separate sessions**: Нет cross-talk между агентами
- **Gateway pattern**: Один Gateway управляет N агентами

### Установка

```bash
# Docker
docker pull openclaw/openclaw:latest

# Или из исходников
git clone https://github.com/openclaw/openclaw
cd openclaw
make install
```

### Базовый пример

```bash
# Запуск Gateway
openclaw gateway start --port 8080

# Создание агентов
openclaw agent create --name backend-dev --model sonnet-4.5
openclaw agent create --name frontend-dev --model sonnet-4.5
openclaw agent create --name reviewer --model opus-4.6

# Отправка задач
openclaw send --to backend-dev "Implement /api/users endpoint"
openclaw send --to frontend-dev "Create UserList component"

# Когда оба готовы, отправляем ревьюеру
openclaw send --to reviewer "Review all changes from backend-dev and frontend-dev"
```

### Agent Teams (Experimental RFC)

Новая функциональность (февраль 2026) - координация между агентами:

```yaml
# openclaw-team.yaml
gateway:
  port: 8080

team:
  shared_task_list: true
  coordination_mode: dynamic

  agents:
    - name: architect
      model: opus-4.6
      workspace: ./workspace
      soul: |
        You are a software architect. Create detailed plans.

    - name: dev-1
      model: sonnet-4.5
      workspace: ./workspace
      teammates: [dev-2, dev-3]
      soul: |
        You are a developer. Implement features from architect's plan.
        Coordinate with other devs to avoid conflicts.

    - name: dev-2
      model: sonnet-4.5
      workspace: ./workspace
      teammates: [dev-1, dev-3]

    - name: dev-3
      model: sonnet-4.5
      workspace: ./workspace
      teammates: [dev-1, dev-2]
```

```bash
openclaw team start openclaw-team.yaml
```

**Возможности Agent Teams:**
- Shared task list с зависимостями
- Direct inter-agent messaging
- Parallel task execution
- Automatic conflict resolution

### Интеграция с Claude Code

OpenClaw поддерживает Claude Code через `openclaw-claude-code-skill`:

```bash
# Установка skill
openclaw skill install openclaw-claude-code-skill

# Использование в агенте
openclaw agent create --name coder \
  --model sonnet-4.5 \
  --skill claude-code
```

### OpenClaw MCP

OpenClaw предоставляет MCP-сервер для интеграции с другими инструментами:

```bash
openclaw mcp start --port 3000
```

Теперь Cursor, Claude Code, или другие MCP-клиенты могут подключаться к OpenClaw.

### Экосистема

- **Claworc**: Web UI для OpenClaw
- **Antfarm**: Distributed task queue для множества Gateway
- **Claude Squad**: Pre-configured agent teams

**Документация:** https://docs.openclaw.ai/

**GitHub:** https://github.com/openclaw/openclaw

**RFC Agent Teams:** https://github.com/openclaw/openclaw/discussions/10036

---

## 8. Другие оркестраторы

### claude-flow

Декларативный workflow engine для Claude.

```bash
npm install -g claude-flow
```

```yaml
# flow.yaml
flows:
  feature-development:
    steps:
      - name: plan
        agent:
          model: opus-4.6
          prompt: "Create implementation plan for: {task}"
        output: plan.md

      - name: implement
        agent:
          model: sonnet-4.5
          prompt: "Implement based on plan.md"
        parallel: 3
        depends_on: [plan]

      - name: test
        agent:
          model: haiku-4.5
          prompt: "Generate tests"
        depends_on: [implement]
```

```bash
claude-flow run flow.yaml --task "Add user authentication"
```

**GitHub:** https://github.com/ruvnet/claude-flow

### Claude Squad

Pre-configured agent teams для типовых задач.

```bash
npm install -g claude-squad
```

```bash
# Feature Squad: Architect + 2 Devs + Tester + Reviewer
claude-squad feature "Add payment processing"

# Refactor Squad: Analyzer + Refactorer + Tester
claude-squad refactor "Improve auth module"

# Debug Squad: Debugger + Fixer + Validator
claude-squad debug "Fix login timeout"
```

**Преконфигурированные команды:**
- `feature`: Полная разработка фичи
- `refactor`: Рефакторинг кода
- `debug`: Поиск и исправление багов
- `review`: Код-ревью
- `docs`: Генерация документации

**GitHub:** https://github.com/smtg-ai/claude-squad

### ralph-orchestrator

Ralph Loop orchestrator — система автоматического retry для AI-агентов, основанная на концепции "Ralph Wiggum" (непрерывный запуск агента до успеха).

```bash
npm install -g ralph-orchestrator
```

```bash
# Запуск задачи с автоматическим retry
ralph-orchestrator run "Implement feature X" \
  --max-attempts 10 \
  --retry-on-failure \
  --verify-with-tests
```

**Ключевые возможности:**
- Автоматический retry при failures
- Верификация через тесты после каждой попытки
- Hot-swap моделей при повторяющихся ошибках
- Логирование всех попыток для анализа

**Философия:** Продолжай пытаться пока не получится, как Ralph Wiggum.

**GitHub:** https://github.com/mikeyobrien/ralph-orchestrator

---

## 9. Паттерны параллельной разработки

### Plan → Implement (Parallel) → Review

```
                     ┌─────────────┐
                     │   Planner   │ (Opus)
                     │  "Architect"│
                     └──────┬──────┘
                            │ plan.md
                            ▼
                    ┌───────────────────┐
                    │  Implementers     │
                    ├───────┬───────────┤
                    │ Dev1  │  Dev2     │ (Sonnet)
                    │ Dev3  │  Dev4     │ (Parallel)
                    └───┬───┴───────┬───┘
                        │           │
                        ▼           ▼
                    ┌─────────────────┐
                    │    Reviewer     │ (Sonnet)
                    │  "Code Review"  │
                    └─────────────────┘
```

### Microservices Pattern

```
Task: "Build e-commerce platform"

                ┌─────────────────┐
                │  Orchestrator   │
                └────────┬────────┘
                         │
        ┌────────────────┼────────────────┐
        ▼                ▼                ▼
   ┌─────────┐      ┌─────────┐     ┌─────────┐
   │  Agent  │      │  Agent  │     │  Agent  │
   │  Auth   │      │Products │     │ Orders  │
   │ Service │      │ Service │     │ Service │
   └─────────┘      └─────────┘     └─────────┘
        │                │                │
        └────────────────┼────────────────┘
                         ▼
                   ┌─────────────┐
                   │  Integration│
                   │    Tests    │
                   └─────────────┘
```

### Batch Processing Pattern

```python
# Обработка 100 файлов параллельно с 10 агентами
import asyncio
from claude_agent import Agent

async def process_file(file_path, agent):
    result = await agent.run_async(f"Refactor {file_path}")
    return result

async def batch_process(files, num_agents=10):
    # Создаем пул агентов
    agents = [Agent(model="haiku-4.5") for _ in range(num_agents)]

    # Распределяем файлы по агентам
    tasks = []
    for i, file in enumerate(files):
        agent = agents[i % num_agents]
        tasks.append(process_file(file, agent))

    # Запускаем все параллельно
    results = await asyncio.gather(*tasks)
    return results

files = [f"src/file{i}.py" for i in range(100)]
results = asyncio.run(batch_process(files))
```

### Cost-Optimized Pattern

```
              ┌──────────────┐
              │   Planning   │ Opus ($$$)
              └──────┬───────┘
                     │
              ┌──────▼───────┐
              │  Breakdown   │ Sonnet ($$)
              └──────┬───────┘
                     │
         ┌───────────┼───────────┐
         ▼           ▼           ▼
    ┌────────┐  ┌────────┐  ┌────────┐
    │ Impl 1 │  │ Impl 2 │  │ Impl 3 │ Haiku ($)
    └───┬────┘  └───┬────┘  └───┬────┘
        └───────────┼───────────┘
                    ▼
              ┌──────────┐
              │  Review  │ Sonnet ($$)
              └──────────┘

Total cost: ~70% cheaper than all-Opus
```

---

## 10. Best Practices

### Безопасность

1. **Ограничивайте инструменты**: `--allowedTools read,grep` (без write/bash)
2. **Sandbox изоляция**: Используйте Docker для untrusted code
3. **Rate limiting**: Ограничивайте `--max-turns` для избежания infinite loops
4. **Secrets management**: Никогда не коммитьте API ключи

### Экономика

1. **Используйте дешевые модели для простых задач**: Haiku для boilerplate
2. **Batch API**: 50% экономии на non-urgent задачах
3. **Prompt caching**: 90% экономии на повторяющемся контексте
4. **Мониторинг затрат**: Логируйте `cost_usd` каждого агента

### Надежность

1. **Детерминистические проверки**: Линтеры, тесты, type checkers
2. **Human-in-the-loop checkpoints**: Ревью перед merge
3. **Rollback strategy**: Git branches для каждого агента
4. **Idempotency**: Агенты должны давать одинаковый результат при повторном запуске

### Debugging

1. **Логируйте все**: `--output-format json` + сохранение в файл
2. **Session replay**: `--resume` для продолжения failed сессий
3. **Visibility**: Дашборды для мониторинга агентов
4. **Alerting**: Уведомления при failures

---

## Источники

### Официальная документация
- [Claude Code Headless Mode](https://code.claude.com/docs/en/headless)
- [Claude Code Docker Integration](https://docs.docker.com/ai/sandboxes/claude-code/)
- [Claude Code Authentication](https://code.claude.com/docs/en/authentication)
- [Claude Agent SDK Overview](https://platform.claude.com/docs/en/agent-sdk/overview)
- [Claude Agent SDK Python](https://github.com/anthropics/claude-agent-sdk-python)
- [Claude Agent SDK TypeScript](https://github.com/anthropics/claude-agent-sdk-typescript)
- [Claude Code Agent Teams](https://code.claude.com/docs/en/agent-teams)
- [Claude Code GitHub Actions](https://code.claude.com/docs/en/github-actions)

### Проекты и фреймворки
- [OpenClaw GitHub](https://github.com/openclaw/openclaw)
- [OpenClaw Documentation](https://docs.openclaw.ai/)
- [OpenClaw Multi-Agent Routing](https://docs.openclaw.ai/concepts/multi-agent)
- [OpenClaw Agent Teams RFC](https://github.com/openclaw/openclaw/discussions/10036)
- [claude-flow GitHub](https://github.com/ruvnet/claude-flow)
- [Claude Squad GitHub](https://github.com/smtg-ai/claude-squad)

### Статьи и примеры
- [Building Agents with Claude Agent SDK](https://www.anthropic.com/engineering/building-agents-with-the-claude-agent-sdk)
- [OpenClaw Multi-Agent Orchestration](https://medium.com/@procoder/i-replaced-my-entire-ai-workflow-with-an-org-chart-of-7-agents-heres-the-complete-technical-eda367b91b39)
- [Run Multiple OpenClaw AI Agents](https://www.digitalocean.com/blog/openclaw-digitalocean-app-platform)

---

**Дата обновления:** 12 февраля 2026
**Автор:** AI Course Research Team
