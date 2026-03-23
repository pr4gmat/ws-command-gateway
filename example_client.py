from __future__ import annotations

import argparse
import asyncio
import json

import websockets

from ws_command_gateway.schemas import RequestMessage


async def send_and_print(uri: str, command: str, arg: dict[str, object] | None = None) -> None:
    request = RequestMessage(cmd=command, arg=arg or {})

    async with websockets.connect(uri) as websocket:
        await websocket.send(request.model_dump_json())
        raw_response = await websocket.recv()
        print(json.dumps(json.loads(raw_response), indent=2))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Send a demo request to the WebSocket gateway.")
    parser.add_argument("--uri", default="ws://127.0.0.1:8765", help="Gateway URI.")
    parser.add_argument(
        "--cmd",
        default="ping",
        choices=["ping", "topology_snapshot", "database_status", "optimization_plan"],
        help="Command to send.",
    )
    return parser


def main() -> None:
    args = build_parser().parse_args()
    payload = {"request_id": "demo"} if args.cmd == "optimization_plan" else {}
    asyncio.run(send_and_print(args.uri, args.cmd, payload))


if __name__ == "__main__":
    main()

