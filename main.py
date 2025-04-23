from typing import Union

from mcp.server.fastmcp import Context
from mcp.types import CallToolResult, TextContent

from config import mcp
from exceptions import NutritionixAPIError
from api_requests import (
    search_food_instant,
    get_nutrition_from_natural_query,
    get_calories_burned,
)
from utils import (
    prepare_search_instant_food_message,
    prepare_food_nutrition_message,
    prepare_exercise_message,
)


@mcp.tool()
async def get_exercise_calories_burned(query: str, ctx: Context) -> Union[str, CallToolResult]:
    """Get estimated exercise calories burned from natural language input.
    It would be good to provide age, gender, weight in kg and height in cm.

    Args:
        query: Description of exercise (e.g. "ran 3 miles and biked for 30 minutes")
    """
    headers = {
        **ctx.request_context.lifespan_context.get_headers(),
        "Content-Type": "application/json",
    }
    try:
        data = await get_calories_burned(query, headers)
    except NutritionixAPIError as e:
        return CallToolResult(
            isError=True,
            content=[TextContent(type="text", text=f"Nutritionix API Error {e}")],
        )

    return prepare_exercise_message(data)


@mcp.tool()
async def get_food_nutrition(query: str, ctx: Context) -> Union[str, CallToolResult]:
    """Get detailed nutritional information from a natural language food query.

    Args:
        query: A sentence or phrase describing the food (e.g. "1 egg and 2 slices of toast")
    """
    headers = ctx.request_context.lifespan_context.get_headers()

    try:
        data = await get_nutrition_from_natural_query(query, headers)
    except NutritionixAPIError as e:
        return CallToolResult(
            isError=True,
            content=[TextContent(type="text", text=f"Nutritionix API Error {e}")],
        )

    return prepare_food_nutrition_message(data)


@mcp.tool()
async def search_food(query: str, ctx: Context) -> Union[str, CallToolResult]:
    """Search for common and branded food items.

    Args:
        query: The food search string (e.g. 'banana', 'egg', 'yogurt')
    """
    headers = ctx.request_context.lifespan_context.get_headers()

    try:
        data = await search_food_instant(query, headers)
    except NutritionixAPIError as e:
        return CallToolResult(
            isError=True,
            content=[TextContent(type="text", text=f"Nutritionix API Error {e}")],
        )

    return prepare_search_instant_food_message(data)


def main():
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
