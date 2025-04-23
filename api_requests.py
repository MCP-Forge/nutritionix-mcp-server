from httpx import AsyncClient, HTTPStatusError, RequestError

from exceptions import NutritionixAPIError

NUTRITIONIX_BASE_URL = "https://trackapi.nutritionix.com/v2"


async def _safe_request(
    method: str, url: str, **kwargs: dict,
) -> dict:
    async with AsyncClient() as client:
        try:
            if method == "GET":
                response = await client.get(url, **kwargs)
            elif method == "POST":
                response = await client.post(url, **kwargs)
            else:
                raise ValueError(f"Unsupported method: {method}")
            
            response.raise_for_status()
            return response.json()

        except HTTPStatusError as e:
            raise NutritionixAPIError(
                f"API error {e.response.status_code} at {url}: {e.response.text}"
            ) from e

        except RequestError as e:
            raise NutritionixAPIError(
                f"Network error during request to {url}: {str(e)}"
            ) from e

        except Exception as e:
            raise NutritionixAPIError(
                f"Unexpected error during request to {url}: {str(e)}"
            ) from e


async def search_food_instant(query: str, headers: dict) -> dict:
    url = f"{NUTRITIONIX_BASE_URL}/search/instant?query={query}"
    return await _safe_request("GET", url, headers=headers)


async def get_nutrition_from_natural_query(query: str, headers: dict) -> dict:
    url = f"{NUTRITIONIX_BASE_URL}/natural/nutrients"
    payload = {"query": query}
    return await _safe_request("POST", url, headers=headers, json=payload)


async def get_calories_burned(query: str, headers: dict) -> dict:
    url = f"{NUTRITIONIX_BASE_URL}/natural/exercise"
    payload = {"query": query}
    return await _safe_request("POST", url, headers=headers, json=payload)
