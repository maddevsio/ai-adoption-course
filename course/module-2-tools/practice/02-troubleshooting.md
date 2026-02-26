[← Оглавление](../../../README.md)

## Troubleshooting: Решение типовых проблем

### Проблема 1: `npm ERR! EACCES` при установке

**Симптомы:**
```
npm ERR! Error: EACCES: permission denied, access '/usr/local/lib/node_modules'
```

**Причина:** Недостаточно прав для глобальной установки npm пакетов.

**Решение: Использовать официальный установщик:**

```bash
# Официальный установщик не требует npm или sudo
curl -fsSL https://claude.ai/install.sh | bash

# Проверка установки
claude --version
```

**Примечание:** NPM-установка больше не поддерживается. Используйте только официальный установщик.


### Проблема 2: "Invalid API key" или "Unauthorized"

**Симптомы:**
```
Error: Invalid API key
Status: 401 Unauthorized
```

**Проверка 1: Формат ключа**

```bash
echo $ANTHROPIC_API_KEY
# Должен начинаться с sk-ant-api03-
# Длина примерно 100+ символов
```

**Проверка 2: Регион и план**

- API keys с console.anthropic.com — только для US регiona
- Для EU нужно использовать https://console.anthropic.eu
- Проверьте, что у вас есть активная подписка или положительный баланс

**Проверка 3: Файл конфигурации**

```bash
# Проверить наличие конфигурации
ls -la ~/.claude/config.json

# Если файла нет, создать его
mkdir -p ~/.claude
cat > ~/.claude/config.json << 'EOF'
{
  "model": "claude-sonnet-4-5-20250929"
}
EOF
```

**Решение:**

```bash
# Обновить или создать API key
export ANTHROPIC_API_KEY="sk-ant-api03-ваш_новый_ключ"

# Добавить в ~/.bashrc для постоянного эффекта
echo 'export ANTHROPIC_API_KEY="sk-ant-api03-ваш_ключ"' >> ~/.bashrc
source ~/.bashrc
```

### Проблема 3: `claude: command not found`

**Симптомы:**
```bash
claude --version
# bash: claude: command not found
```

**Причина:** Исполняемый файл claude не в PATH.

**Решение для официального установщика:**

```bash
# Переустановить Claude Code
curl -fsSL https://claude.ai/install.sh | bash

# Проверить установку
which claude
# Должен показать путь к исполняемому файлу

# Проверить PATH
echo $PATH
```

**Решение для Homebrew (macOS):**

```bash
# Проверить установку
brew list anthropics/tap/claude

# Переустановить если нужно
brew reinstall anthropics/tap/claude

# Проверить PATH
echo $PATH | grep homebrew
```

**Универсальное решение: перезапуск терминала**

Часто после установки нужно просто перезапустить терминал для обновления PATH.

### Проблема 4: Таймаут или "Connection refused"

**Симптомы:**
```
Error: connect ETIMEDOUT
Error: Connection refused
```

**Причина:** Проблемы сетевого подключения (VPN, firewall, proxy).

**Решение A: Проверить сетевое подключение**

```bash
# Проверить доступность API Anthropic
curl -I https://api.anthropic.com/v1/messages
# Ожидается: HTTP/1.1 или HTTP/2 ответ

# Если не отвечает, проблема в сети
```

**Решение B: Настроить proxy**

```bash
# Если вы за корпоративным proxy
export HTTP_PROXY=http://proxy.company.com:8080
export HTTPS_PROXY=http://proxy.company.com:8080

# Добавить в ~/.bashrc
echo 'export HTTP_PROXY=http://proxy.company.com:8080' >> ~/.bashrc
echo 'export HTTPS_PROXY=http://proxy.company.com:8080' >> ~/.bashrc
```

**Решение C: VPN**

Если Anthropic API заблокирован в вашем регионе, используйте VPN:
- Подключиться к VPN с сервером в US или EU
- Проверить: `curl https://api.anthropic.com`

**Решение D: Firewall**

```bash
# Проверить firewall (Linux)
sudo ufw status

# Разрешить исходящие HTTPS
sudo ufw allow out 443/tcp
```

### Проблема 5: "Permission denied" при чтении файлов

**Симптомы:**
```
Error: EACCES: permission denied, open '/path/to/file'
```

**Причина:** Агент не имеет прав доступа к файлам проекта.

**Решение A: Запускать из корня проекта**

```bash
# НЕПРАВИЛЬНО: запускать из ~
cd ~
claude -p "Analyze project at ~/projects/my-app"

# ПРАВИЛЬНО: запускать из корня проекта
cd ~/projects/my-app
claude -p "Analyze this project"
```

**Решение B: Проверить права файлов**

```bash
# Проверить права
ls -la

# Если файлы принадлежат другому пользователю
sudo chown -R $USER:$USER .

# Если недостаточно прав на чтение
chmod -R u+r .
```

**Решение C: Настроить blockedPaths в конфигурации**

```json
{
  "blockedPaths": [".env", "secrets/"]
}
```

Убедитесь, что нужные файлы НЕ в списке заблокированных.
---

[← Установка рабочего окружения](01-setup.md) | [Оглавление](../../../README.md) | [Чеклист готовности →](03-checklist.md)
