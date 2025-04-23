def prepare_search_instant_food_message(data: dict) -> str:
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


def prepare_food_nutrition_message(data: dict) -> str:
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


def prepare_exercise_message(data: dict) -> str:
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
