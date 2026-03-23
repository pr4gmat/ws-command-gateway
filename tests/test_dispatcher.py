from __future__ import annotations

import asyncio

from ws_command_gateway.dispatcher import CommandDispatcher
from ws_command_gateway.handlers import register_default_handlers
from ws_command_gateway.schemas import RequestMessage
from ws_command_gateway.services import ServiceContainer
from ws_command_gateway.session import ClientSession


class DummyWebSocket:
    remote_address = ("127.0.0.1", 9000)

    async def send(self, payload: str) -> None:
        self.payload = payload


def test_dispatcher_returns_ping_payload() -> None:
    async def scenario() -> None:
        dispatcher = register_default_handlers(CommandDispatcher(ServiceContainer()))
        session = ClientSession.from_websocket(DummyWebSocket())
        request = RequestMessage(cmd="ping")

        response = await dispatcher.dispatch(session, request)

        assert response.ok is True
        assert response.reply_to == request.mid
        assert response.arg["message"] == "pong"

    asyncio.run(scenario())


def test_dispatcher_handles_unknown_command() -> None:
    async def scenario() -> None:
        dispatcher = register_default_handlers(CommandDispatcher(ServiceContainer()))
        session = ClientSession.from_websocket(DummyWebSocket())
        request = RequestMessage(cmd="missing")

        response = await dispatcher.dispatch(session, request)

        assert response.ok is False
        assert response.error is not None
        assert response.error.code == "unknown_command"

    asyncio.run(scenario())

