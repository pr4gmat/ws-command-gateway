from __future__ import annotations

import asyncio
from typing import Any


class OptimizationGateway:
    async def build_plan(self, payload: dict[str, Any]) -> dict[str, Any]:
        await asyncio.sleep(0)
        return {
            "accepted": True,
            "mode": "stub",
            "received": payload,
        }

