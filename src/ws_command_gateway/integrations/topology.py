from __future__ import annotations

import asyncio
from typing import Any


class TopologyGateway:
    async def fetch_snapshot(self) -> dict[str, Any]:
        await asyncio.sleep(0)
        return {
            "nodes": [
                {"id": "node-a", "kind": "source"},
                {"id": "node-b", "kind": "consumer"},
            ],
            "links": [
                {"source": "node-a", "target": "node-b"},
            ],
            "status": "stub",
        }

