from __future__ import annotations

from dataclasses import dataclass, field

from ws_command_gateway.integrations.database import DatabaseGateway
from ws_command_gateway.integrations.optimization import OptimizationGateway
from ws_command_gateway.integrations.topology import TopologyGateway


@dataclass(slots=True)
class ServiceContainer:
    topology: TopologyGateway = field(default_factory=TopologyGateway)
    database: DatabaseGateway = field(default_factory=DatabaseGateway)
    optimization: OptimizationGateway = field(default_factory=OptimizationGateway)

