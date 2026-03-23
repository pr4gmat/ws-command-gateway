from __future__ import annotations

import asyncio

import websockets

from ws_command_gateway.schemas import RequestMessage, ResponseMessage
from ws_command_gateway.server import CommandBusServer


def test_server_ping_round_trip() -> None:
    async def scenario() -> None:
        server = CommandBusServer(host="127.0.0.1", port=0)
        await server.start()

        try:
            uri = f"ws://127.0.0.1:{server.port}"
            async with websockets.connect(uri) as websocket:
                request = RequestMessage(cmd="ping")
                await websocket.send(request.model_dump_json())

                raw_response = await websocket.recv()
                response = ResponseMessage.model_validate_json(raw_response)

                assert response.ok is True
                assert response.reply_to == request.mid
                assert response.arg["message"] == "pong"
        finally:
            await server.stop()

    asyncio.run(scenario())
