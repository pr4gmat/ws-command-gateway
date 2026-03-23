from __future__ import annotations

import asyncio
from typing import Any
from uuid import UUID

from ws_command_gateway.schemas import EventMessage
from ws_command_gateway.session import ClientSession


class ConnectionManager:
    def __init__(self) -> None:
        self._sessions: dict[UUID, ClientSession] = {}
        self._lock = asyncio.Lock()

    async def register(self, websocket: Any) -> ClientSession:
        session = ClientSession.from_websocket(websocket)
        async with self._lock:
            self._sessions[session.session_id] = session
        return session

    async def unregister(self, session: ClientSession) -> None:
        async with self._lock:
            self._sessions.pop(session.session_id, None)

    async def broadcast(self, event: EventMessage) -> int:
        async with self._lock:
            sessions = list(self._sessions.values())

        await asyncio.gather(*(session.send_model(event) for session in sessions), return_exceptions=True)
        return len(sessions)

    async def send_event(self, session_id: UUID, event: EventMessage) -> bool:
        async with self._lock:
            session = self._sessions.get(session_id)

        if session is None:
            return False

        await session.send_model(event)
        return True

    async def count(self) -> int:
        async with self._lock:
            return len(self._sessions)

