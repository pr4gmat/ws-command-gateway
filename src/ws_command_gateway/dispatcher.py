from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Any, Awaitable, Callable

from ws_command_gateway.schemas import ErrorPayload, RequestMessage, ResponseMessage, build_error_response
from ws_command_gateway.services import ServiceContainer
from ws_command_gateway.session import ClientSession

logger = logging.getLogger(__name__)

CommandHandler = Callable[
    [ClientSession, RequestMessage, ServiceContainer],
    Awaitable["CommandResult"],
]


@dataclass(slots=True)
class CommandResult:
    ok: bool
    arg: dict[str, Any] = field(default_factory=dict)
    error: ErrorPayload | None = None
    next_cmd: str | None = None

    @classmethod
    def success(cls, arg: dict[str, Any] | None = None, next_cmd: str | None = None) -> "CommandResult":
        return cls(ok=True, arg=arg or {}, next_cmd=next_cmd)

    @classmethod
    def failure(
        cls,
        *,
        code: str,
        message: str,
        details: dict[str, Any] | None = None,
        next_cmd: str | None = None,
    ) -> "CommandResult":
        return cls(
            ok=False,
            arg={},
            error=ErrorPayload(code=code, message=message, details=details),
            next_cmd=next_cmd,
        )


class CommandDispatcher:
    def __init__(self, services: ServiceContainer) -> None:
        self._services = services
        self._handlers: dict[str, CommandHandler] = {}

    def register(self, command: str, handler: CommandHandler) -> None:
        self._handlers[command] = handler

    async def dispatch(self, session: ClientSession, request: RequestMessage) -> ResponseMessage:
        handler = self._handlers.get(request.cmd)
        if handler is None:
            return build_error_response(
                reply_to=request.mid,
                cmd=request.cmd,
                code="unknown_command",
                message=f"Command '{request.cmd}' is not registered.",
            )

        try:
            result = await handler(session, request, self._services)
        except Exception:
            logger.exception("Unhandled exception while executing command '%s'", request.cmd)
            return build_error_response(
                reply_to=request.mid,
                cmd=request.cmd,
                code="internal_error",
                message="Command handler raised an unexpected exception.",
            )

        return ResponseMessage(
            reply_to=request.mid,
            cmd=request.cmd,
            ok=result.ok,
            arg=result.arg,
            error=result.error,
            next_cmd=result.next_cmd,
        )

