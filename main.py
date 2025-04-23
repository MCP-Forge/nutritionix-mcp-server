import argparse
from contextlib import asynccontextmanager
from collections.abc import AsyncIterator
from dataclasses import dataclass

import httpx
from mcp.server.fastmcp import FastMCP, Context


NUTRITIONIX_BASE_URL = "https://trackapi.nutritionix.com/v2"


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


@mcp.tool()
async def get_exercise_nutrition(query: str, ctx: Context) -> str:
    """Get estimated exercise calories burned from natural language input.
    It would be good to provide age, gender, weight in kg and height in cm.

    Args:
        query: Description of exercise (e.g. "ran 3 miles and biked for 30 minutes")
    """
    url = f"{NUTRITIONIX_BASE_URL}/natural/exercise"
    headers = {
        **ctx.request_context.lifespan_context.get_headers(),
        "Content-Type": "application/json",
    }
    payload = {"query": query}

    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, json=payload)

    if response.status_code != 200:
        return f"Failed to get exercise data: {response.status_code} - {response.text}"

    data = response.json()
    results = []

    for exercise in data.get("exercises", []):
        results.append(
            f"""
            🏃 {exercise['name'].title()}
                Duration: {exercise['duration_min']} min
                Calories Burned: {exercise['nf_calories']} kcal
                MET: {exercise.get('met', 'N/A')}
            """
        )

    return "\n".join(results) if results else "No exercise data found."


@mcp.tool()
async def get_food_nutrition(query: str, ctx: Context) -> str:
    """Get detailed nutritional information from a natural language food query.

    Args:
        query: A sentence or phrase describing the food (e.g. "1 egg and 2 slices of toast")
    """
    url = f"{NUTRITIONIX_BASE_URL}/natural/nutrients"
    headers = ctx.request_context.lifespan_context.get_headers()
    payload = {"query": query}

    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, json=payload)

    if response.status_code != 200:
        return f"Failed to get nutrition info: {response.status_code} - {response.text}"

    data = response.json()
    results = []

    for food in data.get("foods", []):
        results.append(
            f"""
            🍽️ {food['food_name'].title()}
                Serving: {food['serving_qty']} {food['serving_unit']} ({food['serving_weight_grams']}g)
                Calories: {food['nf_calories']} kcal
                Protein: {food['nf_protein']}g
                Carbs: {food['nf_total_carbohydrate']}g
                Fat: {food['nf_total_fat']}g
            """
        )

    return "\n".join(results) if results else "No nutrition data found."


@mcp.tool()
async def search_food(query: str, ctx: Context) -> str:
    """Search for common and branded food items.

    Args:
        query: The food search string (e.g. 'banana', 'egg', 'yogurt')
    """
    url = f"{NUTRITIONIX_BASE_URL}/search/instant?query={query}"
    headers = ctx.request_context.lifespan_context.get_headers()

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)

    if response.status_code != 200:
        return f"Failed to search foods: {response.status_code} - {response.text}"

    data = response.json()
    common = [item["food_name"] for item in data.get("common", [])]
    branded = [
        f"{item['brand_name']} - {item['food_name']}"
        for item in data.get("branded", [])
    ]

    results = []

    if common:
        results.append(
            "🔸 **Common Foods:**\n" + "\n".join(f"- {name}" for name in common[:5])
        )
    if branded:
        results.append(
            "🔹 **Branded Products:**\n"
            + "\n".join(f"- {name}" for name in branded[:5])
        )

    return "\n\n".join(results) if results else "No matching food items found."


def main():
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
