def generate_nutrition_tip_with_flash(goal: str) -> str:
    """Return a practical nutrition tip without calling an external service."""
    goal_lower = goal.lower()
    if "muscle" in goal_lower or "strength" in goal_lower:
        return "Include a protein-rich food, such as beans, eggs, yogurt, tofu, or fish, in your meals to support recovery."
    if "weight loss" in goal_lower or "fat loss" in goal_lower:
        return "Build filling meals around vegetables, a protein source, and high-fiber foods; steady habits matter more than skipping meals."
    if "endurance" in goal_lower or "cardio" in goal_lower:
        return "For longer workouts, drink water regularly and include carbohydrate-rich foods such as oats, fruit, or rice in your meals."
    return "Drink water throughout the day and include a mix of vegetables, fruit, whole grains, and protein in your meals."