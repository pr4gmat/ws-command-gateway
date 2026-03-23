# WebSocket Command Gateway

Небольшая заготовка серверной шины обмена по WebSocket на `asyncio`, `websockets` и `pydantic`. Проект сделан как чистый стартовый шаблон: без REST, ORM, Docker, авторизации и реальной БД, но с понятными точками расширения для будущей интеграции.

## Что внутри

- WebSocket-сервер на `asyncio`
- схема сообщений `request` / `response` / `event`
- клиентская сессия и менеджер соединений
- диспетчер команд с регистрацией handler-функций
- заглушки интеграций для topology / database / optimization
- пример клиента
- минимальные тесты на протокол и серверный round-trip

## Структура

```text
src/ws_command_gateway/
  __main__.py
  dispatcher.py
  handlers.py
  manager.py
  schemas.py
  server.py
  services.py
  session.py
  integrations/
    database.py
    optimization.py
    topology.py
example_client.py
tests/
```

## Протокол

`request`

```json
{
  "type": "request",
  "mid": "uuid",
  "cmd": "ping",
  "arg": {}
}
```

`response`

```json
{
  "type": "response",
  "mid": "uuid",
  "reply_to": "uuid",
  "cmd": "ping",
  "ok": true,
  "arg": {
    "message": "pong"
  },
  "error": null,
  "next_cmd": null
}
```

`event`

```json
{
  "type": "event",
  "mid": "uuid",
  "cmd": "something_happened",
  "arg": {}
}
```

## Доступные команды

- `ping` -> проверка доступности сервера
- `topology_snapshot` -> заглушка получения topology snapshot
- `database_status` -> заглушка статуса database integration
- `optimization_plan` -> заглушка запуска optimization workflow

## Быстрый старт

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -e .[dev]
python -m ws_command_gateway --host 127.0.0.1 --port 8765
```

В другом терминале:

```bash
python example_client.py --uri ws://127.0.0.1:8765 --cmd ping
python example_client.py --uri ws://127.0.0.1:8765 --cmd topology_snapshot
```

## Расширение

1. Добавьте новую integration-обвязку в `src/ws_command_gateway/integrations/`.
2. Расширьте `ServiceContainer`, если нужен новый внешний ресурс.
3. Реализуйте handler в `src/ws_command_gateway/handlers.py`.
4. Зарегистрируйте команду в `register_default_handlers`.

## Тесты

```bash
pytest
```

## Архитектурные замечания

- `schemas.py` централизует контракт протокола и валидацию сообщений.
- `session.py` и `manager.py` изолируют работу с жизненным циклом WebSocket-подключений.
- `dispatcher.py` не зависит от транспорта и знает только про команды, handler-функции и сервисы.
- `integrations/*` оставлены как асинхронные stub-адаптеры, чтобы их можно было заменить реальными реализациями без пересборки базовой архитектуры.

