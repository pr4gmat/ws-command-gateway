from __future__ import annotations

import asyncio
from typing import Any


class DatabaseGateway:
    async def get_status(self) -> dict[str, Any]:
        await asyncio.sleep(0)
        return {
            "connected": False,
            "engine": "stub",
            "message": "No real database is configured.",
        }

