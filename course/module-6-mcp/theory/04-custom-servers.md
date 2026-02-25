[← Оглавление](../../../README.md)

## 6. Создание своего MCP-сервера

### 6.1. Когда это нужно

Создавайте собственный MCP-сервер, если:
- Нужна интеграция с **internal tools** вашей компании
- Используете **proprietary APIs**, для которых нет готового сервера
- Работаете с **legacy systems**
- Хотите создать **custom workflow** для команды

### 6.2. SDK

```bash
npm install @modelcontextprotocol/sdk
```

Документация: [github.com/modelcontextprotocol/sdk](https://github.com/modelcontextprotocol/sdk)

### 6.3. Минимальный пример

```typescript
import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';

const server = new Server({
  name: 'weather-server',
  version: '1.0.0',
});

server.setRequestHandler('tools/list', async () => ({
  tools: [
    {
      name: 'get_weather',
      description: 'Get current weather for a city',
      inputSchema: {
        type: 'object',
        properties: {
          city: { type: 'string', description: 'City name' }
        },
        required: ['city']
      }
    }
  ]
}));

server.setRequestHandler('tools/call', async (request) => {
  if (request.params.name === 'get_weather') {
    const { city } = request.params.arguments;
    const weather = `Sunny, 22°C in ${city}`;
    return {
      content: [{ type: 'text', text: weather }]
    };
  }
});

const transport = new StdioServerTransport();
await server.connect(transport);
```

Конфигурация в `mcp.json`:

```json
{
  "mcpServers": {
    "weather": {
      "command": "node",
      "args": ["/path/to/weather-server.js"]
    }
  }
}
```

### 6.4. Структура production-сервера

```
my-mcp-server/
├── src/
│   ├── index.ts          # Entry point
│   ├── tools/            # Tool implementations
│   ├── api/              # External API client
│   └── utils/            # Helpers
├── tests/
├── package.json
└── tsconfig.json
```

Production-сервер включает: multiple tools, error handling, authentication (API keys, OAuth), caching, logging, тесты.
---

[← 5. Установка и настройка](03-setup-and-config.md) | [Оглавление](../../../README.md) | [Настройка MCP-серверов →](../practice/01-setup-mcp-servers.md)
