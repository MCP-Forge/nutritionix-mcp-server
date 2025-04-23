from httpx import AsyncClient

from exceptions import NutritionixAPIError

NUTRITIONIX_BASE_URL = "https://trackapi.nutritionix.com/v2"


async def search_food_instant(query: str, headers: dict) -> dict:
    url = f"{NUTRITIONIX_BASE_URL}/search/instant?query={query}"
    async with AsyncClient() as client:
        response = await client.get(url, headers=headers)

    if response.status_code != 200:
        raise NutritionixAPIError("The search food request failed!")

    return response.json()


async def get_nutrition_from_natural_query(query: str, headers: dict) -> dict:
    url = f"{NUTRITIONIX_BASE_URL}/natural/nutrients"
    payload = {"query": query}

    async with AsyncClient() as client:
        response = await client.post(url, headers=headers, json=payload)

    if response.status_code != 200:
        raise NutritionixAPIError("The nutrition from natural language request failed!")

    return response.json()


async def get_calories_burned(query: str, headers: dict) -> dict:
    url = f"{NUTRITIONIX_BASE_URL}/natural/exercise"
    payload = {"query": query}

    async with AsyncClient() as client:
        response = await client.post(url, headers=headers, json=payload)

    if response.status_code != 200:
        raise NutritionixAPIError("Failed to get exercises data!")

    return response.json()
