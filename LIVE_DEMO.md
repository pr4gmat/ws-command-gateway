# Live Demo

Это демонстрация реального прогона проекта: сервер поднялся, клиент отправил команды, сервер вернул корректные ответы.

Команды ниже даны в нейтральном публичном виде, без привязки к локальному аккаунту или абсолютным путям. JSON-ответы и лог сервера сняты с живого запуска.

## 1. Старт сервера

Команда:

```powershell
python -m ws_command_gateway --host 127.0.0.1 --port 8765
```

Вывод сервера:

```text
INFO:websockets.server:server listening on 127.0.0.1:8765
INFO:websockets.server:connection open
INFO:ws_command_gateway.server:Client connected: 127.0.0.1:51168
INFO:websockets.server:connection open
INFO:ws_command_gateway.server:Client connected: 127.0.0.1:51171
INFO:websockets.server:connection open
INFO:ws_command_gateway.server:Client connected: 127.0.0.1:51174
INFO:websockets.server:connection open
INFO:ws_command_gateway.server:Client connected: 127.0.0.1:51177
```

## 2. Команда `ping`

Команда:

```powershell
python example_client.py --uri ws://127.0.0.1:8765 --cmd ping
```

Ответ:

```json
{
  "mid": "0c8a8789-1bf7-40ba-8650-431beb227830",
  "cmd": "ping",
  "arg": {
    "message": "pong",
    "session_id": "47b236de-9990-4193-8c5d-d8ed5181b933"
  },
  "type": "response",
  "reply_to": "8c4b15d1-11d3-43db-91d7-178de9ab4ed3",
  "ok": true,
  "error": null,
  "next_cmd": null
}
```

## 3. Команда `topology_snapshot`

Команда:

```powershell
python example_client.py --uri ws://127.0.0.1:8765 --cmd topology_snapshot
```

Ответ:

```json
{
  "mid": "1da75710-5a43-455c-81eb-c6b31c32c9f9",
  "cmd": "topology_snapshot",
  "arg": {
    "nodes": [
      {
        "id": "node-a",
        "kind": "source"
      },
      {
        "id": "node-b",
        "kind": "consumer"
      }
    ],
    "links": [
      {
        "source": "node-a",
        "target": "node-b"
      }
    ],
    "status": "stub"
  },
  "type": "response",
  "reply_to": "1c669c10-345e-444d-a2d6-07386b69e970",
  "ok": true,
  "error": null,
  "next_cmd": null
}
```

## 4. Команда `database_status`

Команда:

```powershell
python example_client.py --uri ws://127.0.0.1:8765 --cmd database_status
```

Ответ:

```json
{
  "mid": "2e45e5f9-80dd-4cdf-b2ac-5112f2a9233c",
  "cmd": "database_status",
  "arg": {
    "connected": false,
    "engine": "stub",
    "message": "No real database is configured."
  },
  "type": "response",
  "reply_to": "76ba51fb-230f-439e-bc77-ff0aba3a4992",
  "ok": true,
  "error": null,
  "next_cmd": null
}
```

## 5. Команда `optimization_plan`

Команда:

```powershell
python example_client.py --uri ws://127.0.0.1:8765 --cmd optimization_plan
```

Ответ:

```json
{
  "mid": "bc1adcc9-13a0-43a3-bb9e-3b341e94d3c5",
  "cmd": "optimization_plan",
  "arg": {
    "accepted": true,
    "mode": "stub",
    "received": {
      "request_id": "demo"
    }
  },
  "type": "response",
  "reply_to": "9a607871-3957-420a-aec8-b226c0f3bb44",
  "ok": true,
  "error": null,
  "next_cmd": "optimization_status"
}
```

## 6. Что видно по результату

- Сервер поднимается и слушает WebSocket на `127.0.0.1:8765`.
- Клиент успешно подключается и получает валидные `response` сообщения.
- `ping` подтверждает доступность шины.
- `topology_snapshot`, `database_status` и `optimization_plan` показывают, что dispatcher и integration stubs реально участвуют в обработке команд.
