import re

def update_workout_plan(original_plan: str, user_feedback: str) -> str:
    """Apply simple intensity or rest adjustments without an external service."""
    feedback = user_feedback.strip()
    feedback_lower = feedback.lower()
    updated_plan = original_plan

    if any(word in feedback_lower for word in ("easier", "less intense", "reduce", "beginner")):
        updated_plan = re.sub(
            r"\b([2-4]) sets\b",
            lambda match: f"{max(2, int(match.group(1)) - 1)} sets",
            updated_plan,
        )
        change = "Reduced exercise sets where possible."
    elif any(word in feedback_lower for word in ("harder", "more intense", "increase", "challenging")):
        updated_plan = re.sub(
            r"\b([2-3]) sets\b",
            lambda match: f"{min(4, int(match.group(1)) + 1)} sets",
            updated_plan,
        )
        change = "Increased exercise sets where possible."
    elif "more rest" in feedback_lower or "longer rest" in feedback_lower:
        updated_plan = re.sub(
            r"(Rest between sets: about )(\d+)( seconds\.)",
            lambda match: f"{match.group(1)}{min(120, int(match.group(2)) + 15)}{match.group(3)}",
            updated_plan,
        )
        change = "Added 15 seconds of rest between sets where possible."
    elif "less rest" in feedback_lower or "shorter rest" in feedback_lower:
        updated_plan = re.sub(
            r"(Rest between sets: about )(\d+)( seconds\.)",
            lambda match: f"{match.group(1)}{max(30, int(match.group(2)) - 15)}{match.group(3)}",
            updated_plan,
        )
        change = "Reduced rest between sets by 15 seconds where possible."
    else:
        change = "Feedback recorded; no automatic adjustment matched."

    return f"{updated_plan}\n\nFeedback: {feedback}\n{change}"