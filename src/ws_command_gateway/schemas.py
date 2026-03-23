from __future__ import annotations

import json
from typing import Any, Annotated, Literal
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, Field, TypeAdapter, ValidationError

JsonDict = dict[str, Any]


class ErrorPayload(BaseModel):
    model_config = ConfigDict(extra="forbid")

    code: str
    message: str
    details: JsonDict | None = None


class MessageBase(BaseModel):
    model_config = ConfigDict(extra="forbid")

    mid: UUID = Field(default_factory=uuid4)
    cmd: str
    arg: JsonDict = Field(default_factory=dict)


class RequestMessage(MessageBase):
    type: Literal["request"] = "request"


class ResponseMessage(MessageBase):
    type: Literal["response"] = "response"
    reply_to: UUID
    ok: bool
    error: ErrorPayload | None = None
    next_cmd: str | None = None


class EventMessage(MessageBase):
    type: Literal["event"] = "event"


MessageEnvelope = Annotated[
    RequestMessage | ResponseMessage | EventMessage,
    Field(discriminator="type"),
]

MESSAGE_ADAPTER = TypeAdapter(MessageEnvelope)


class MessageDecodeError(ValueError):
    """Raised when an inbound WebSocket payload doesn't match the protocol."""


def decode_message(raw_payload: str) -> RequestMessage | ResponseMessage | EventMessage:
    try:
        payload = json.loads(raw_payload)
    except json.JSONDecodeError as exc:
        raise MessageDecodeError("Payload is not valid JSON.") from exc

    try:
        return MESSAGE_ADAPTER.validate_python(payload)
    except ValidationError as exc:
        raise MessageDecodeError("Payload does not match the message schema.") from exc


def decode_request(raw_payload: str) -> RequestMessage:
    message = decode_message(raw_payload)
    if not isinstance(message, RequestMessage):
        raise MessageDecodeError("Server accepts only request messages from clients.")
    return message


def build_error_response(
    *,
    reply_to: UUID,
    cmd: str,
    code: str,
    message: str,
    details: JsonDict | None = None,
) -> ResponseMessage:
    return ResponseMessage(
        reply_to=reply_to,
        cmd=cmd,
        ok=False,
        arg={},
        error=ErrorPayload(code=code, message=message, details=details),
    )

