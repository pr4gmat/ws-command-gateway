from __future__ import annotations

from ws_command_gateway.schemas import RequestMessage, ResponseMessage, decode_request


def test_request_round_trip() -> None:
    request = RequestMessage(cmd="ping")
    restored = decode_request(request.model_dump_json())

    assert restored.type == "request"
    assert restored.cmd == "ping"
    assert restored.mid == request.mid


def test_response_serializes_reply_to() -> None:
    request = RequestMessage(cmd="ping")
    response = ResponseMessage(
        reply_to=request.mid,
        cmd="ping",
        ok=True,
        arg={"message": "pong"},
    )

    restored = ResponseMessage.model_validate_json(response.model_dump_json())

    assert restored.reply_to == request.mid
    assert restored.arg["message"] == "pong"

