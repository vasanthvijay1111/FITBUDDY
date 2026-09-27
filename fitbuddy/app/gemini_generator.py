def generate_workout_gemini(user_input):
    goal = str(user_input.get("goal", "general fitness")).strip() or "general fitness"
    intensity = str(user_input.get("intensity", "medium")).strip().lower()
    sets_by_intensity = {"low": 2, "medium": 3, "high": 4}
    sets = sets_by_intensity.get(intensity, 3)

    goal_lower = goal.lower()
    if "muscle" in goal_lower or "strength" in goal_lower:
        reps = "8-12"
        rest = 75
    elif "weight loss" in goal_lower or "fat loss" in goal_lower:
        reps = "12-15"
        rest = 45
    else:
        reps = "10-12"
        rest = 60

    days = [
        ("Day 1 - Full Body", ["Chair or bodyweight squats", "Incline push-ups", "Glute bridges", "Bird dogs"]),
        ("Day 2 - Cardio and Core", ["Brisk walk", "Dead bugs", "Standing knee raises", "Front plank"]),
        ("Day 3 - Lower Body", ["Reverse lunges", "Hip hinges", "Calf raises", "Side plank"]),
        ("Day 4 - Active Recovery", []),
        ("Day 5 - Upper Body and Core", ["Wall or incline push-ups", "Prone Y raises", "Shoulder taps", "Dead bugs"]),
        ("Day 6 - Full Body", ["Step-back squats", "Glute bridges", "Wall push-ups", "March in place"]),
        ("Day 7 - Rest", []),
    ]

    plan = [f"Goal: {goal}", f"Intensity: {intensity.title()}"]
    for day, exercises in days:
        plan.extend(["", day, "Warm-up: 5 minutes of easy marching and gentle mobility."])
        if exercises:
            plan.append("Main workout:")
            for exercise in exercises:
                if exercise == "Brisk walk":
                    plan.append(f"- {exercise}: 20-30 minutes at a comfortable pace")
                else:
                    plan.append(f"- {exercise}: {sets} sets x {reps} reps")
            plan.append(f"Rest between sets: about {rest} seconds.")
            plan.append("Cooldown: 5 minutes of easy walking and gentle stretching.")
        else:
            plan.append("Main workout: Rest, or take an easy walk if comfortable.")
            plan.append("Recovery: Drink water and prioritize sleep.")

    plan.append("\nStop if you feel pain, and adjust exercises to your ability.")
    return "\n".join(plan)