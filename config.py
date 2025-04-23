import argparse
from contextlib import asynccontextmanager
from collections.abc import AsyncIterator
from dataclasses import dataclass

from mcp.server.fastmcp import FastMCP


@dataclass
class AppContext:
    app_id: str
    app_key: str

    def get_headers(self) -> dict:
        """Return headers for Nutritionix API requests."""
        return {"x-app-id": self.app_id, "x-app-key": self.app_key}


@asynccontextmanager
async def app_lifespan(server: FastMCP) -> AsyncIterator[AppContext]:
    parser = argparse.ArgumentParser(description="MCP app for Nutritionix.")
    parser.add_argument("--app-id", dest="app_id", help="The app id from Nutritionix.")
    parser.add_argument(
        "--app-key", dest="app_key", help="The app key from Nutritionix."
    )
    args = parser.parse_args()

    if not args.app_id or not args.app_key:
        raise Exception(
            "The --app-id arg, --app-key arg or both args was not provided!"
        )

    yield AppContext(app_id=args.app_id, app_key=args.app_key)


mcp = FastMCP("Nutritionix MCP App", lifespan=app_lifespan)
