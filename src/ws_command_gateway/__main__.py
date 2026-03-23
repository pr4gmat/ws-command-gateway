from __future__ import annotations

import argparse
import asyncio
import logging

from ws_command_gateway.server import CommandBusServer


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run the WebSocket command gateway.")
    parser.add_argument("--host", default="127.0.0.1", help="Bind host.")
    parser.add_argument("--port", default=8765, type=int, help="Bind port.")
    parser.add_argument("--log-level", default="INFO", help="Logging level.")
    return parser


async def run_server(host: str, port: int) -> None:
    server = CommandBusServer(host=host, port=port)
    await server.start()

    print(f"Server listening on ws://{server.host}:{server.port}")

    try:
        await asyncio.Future()
    finally:
        await server.stop()


def main() -> None:
    args = build_parser().parse_args()
    logging.basicConfig(level=getattr(logging, args.log_level.upper(), logging.INFO))

    try:
        asyncio.run(run_server(args.host, args.port))
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()

