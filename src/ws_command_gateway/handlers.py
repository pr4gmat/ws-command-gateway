from __future__ import annotations

from ws_command_gateway.dispatcher import CommandDispatcher, CommandResult
from ws_command_gateway.schemas import RequestMessage
from ws_command_gateway.services import ServiceContainer
from ws_command_gateway.session import ClientSession


async def ping_handler(
    session: ClientSession,
    request: RequestMessage,
    services: ServiceContainer,
) -> CommandResult:
    return CommandResult.success(
        {
            "message": "pong",
            "session_id": str(session.session_id),
        }
    )


async def topology_snapshot_handler(
    session: ClientSession,
    request: RequestMessage,
    services: ServiceContainer,
) -> CommandResult:
    snapshot = await services.topology.fetch_snapshot()
    return CommandResult.success(snapshot)


async def database_status_handler(
    session: ClientSession,
    request: RequestMessage,
    services: ServiceContainer,
) -> CommandResult:
    status = await services.database.get_status()
    return CommandResult.success(status)


async def optimization_plan_handler(
    session: ClientSession,
    request: RequestMessage,
    services: ServiceContainer,
) -> CommandResult:
    plan = await services.optimization.build_plan(request.arg)
    return CommandResult.success(plan, next_cmd="optimization_status")


def register_default_handlers(dispatcher: CommandDispatcher) -> CommandDispatcher:
    dispatcher.register("ping", ping_handler)
    dispatcher.register("topology_snapshot", topology_snapshot_handler)
    dispatcher.register("database_status", database_status_handler)
    dispatcher.register("optimization_plan", optimization_plan_handler)
    return dispatcher

