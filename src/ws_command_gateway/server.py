from __future__ import annotations

import asyncio
import json
import logging
from contextlib import suppress
from typing import Any
from uuid import UUID, uuid4

import websockets

from ws_command_gateway.dispatcher import CommandDispatcher
from ws_command_gateway.handlers import register_default_handlers
from ws_command_gateway.manager import ConnectionManager
from ws_command_gateway.schemas import build_error_response, decode_request
from ws_command_gateway.services import ServiceContainer
from ws_command_gateway.session import ClientSession

logger = logging.getLogger(__name__)


class CommandBusServer:
    def __init__(
        self,
        *,
        host: str = "127.0.0.1",
        port: int = 8765,
        services: ServiceContainer | None = None,
        manager: ConnectionManager | None = None,
        dispatcher: CommandDispatcher | None = None,
    ) -> None:
        self.host = host
        self.port = port
        self.services = services or ServiceContainer()
        self.manager = manager or ConnectionManager()
        self.dispatcher = dispatcher or register_default_handlers(CommandDispatcher(self.services))
        self._server: Any | None = None

    async def start(self) -> None:
        if self._server is not None:
            return

        self._server = await websockets.serve(self._handle_connection, self.host, self.port)

        sockets = getattr(self._server, "sockets", None) or []
        if sockets:
            self.port = sockets[0].getsockname()[1]

    async def stop(self) -> None:
        if self._server is None:
            return

        self._server.close()
        await self._server.wait_closed()
        self._server = None

    async def serve_forever(self) -> None:
        await self.start()
        stop_signal = asyncio.Future()
        try:
            await stop_signal
        finally:
            if not stop_signal.done():
                stop_signal.cancel()

    async def __aenter__(self) -> "CommandBusServer":
        await self.start()
        return self

    async def __aexit__(self, exc_type: Any, exc: Any, tb: Any) -> None:
        await self.stop()

    async def _handle_connection(self, websocket: Any) -> None:
        session = await self.manager.register(websocket)
        logger.info("Client connected: %s", session.remote_address)

        try:
            async for raw_message in websocket:
                await self._process_message(session, raw_message)
        except websockets.ConnectionClosed:
            logger.info("Client disconnected: %s", session.remote_address)
        finally:
            with suppress(Exception):
                await self.manager.unregister(session)

    async def _process_message(self, session: ClientSession, raw_message: str) -> None:
        try:
            request = decode_request(raw_message)
        except Exception as exc:
            await session.send_model(
                build_error_response(
                    reply_to=self._extract_reply_to(raw_message),
                    cmd=self._extract_cmd(raw_message),
                    code="bad_request",
                    message=str(exc),
                )
            )
            return

        response = await self.dispatcher.dispatch(session, request)
        await session.send_model(response)

    @staticmethod
    def _extract_reply_to(raw_message: str) -> UUID:
        try:
            payload = json.loads(raw_message)
        except json.JSONDecodeError:
            return uuid4()

        candidate = payload.get("mid")
        try:
            return UUID(str(candidate))
        except (TypeError, ValueError):
            return uuid4()

    @staticmethod
    def _extract_cmd(raw_message: str) -> str:
        try:
            payload = json.loads(raw_message)
        except json.JSONDecodeError:
            return "invalid_request"

        candidate = payload.get("cmd")
        if isinstance(candidate, str) and candidate:
            return candidate
        return "invalid_request"

