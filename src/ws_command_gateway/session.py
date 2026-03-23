from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any
from uuid import UUID, uuid4

from pydantic import BaseModel


def _format_remote_address(raw_address: Any) -> str:
    if isinstance(raw_address, tuple) and len(raw_address) >= 2:
        return f"{raw_address[0]}:{raw_address[1]}"
    if raw_address is None:
        return "unknown"
    return str(raw_address)


@dataclass(slots=True)
class ClientSession:
    websocket: Any
    session_id: UUID = field(default_factory=uuid4)
    remote_address: str = "unknown"
    connected_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    metadata: dict[str, str] = field(default_factory=dict)

    @classmethod
    def from_websocket(cls, websocket: Any) -> "ClientSession":
        return cls(
            websocket=websocket,
            remote_address=_format_remote_address(getattr(websocket, "remote_address", None)),
        )

    async def send_model(self, message: BaseModel) -> None:
        await self.websocket.send(message.model_dump_json())

