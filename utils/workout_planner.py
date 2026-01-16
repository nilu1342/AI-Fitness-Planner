import pandas as pd

def generate_workout(goal, bmi):

    # Read dataset
    df = pd.read_csv("data/workout_dataset.csv")
    df.columns = df.columns.str.strip()

    workout_plan = []

    # Decide intensity using BMI
    if bmi < 18.5:
        workout_type = "Light"
        duration = 0.6
        calories = 300
        experience = "Beginner"
        frequency = 3
        water = 2.5
    elif bmi < 25:
        workout_type = "Moderate"
        duration = 1.0
        calories = 500
        experience = "Intermediate"
        frequency = 4
        water = 3.0
    else:
        workout_type = "Intense"
        duration = 1.2
        calories = 650
        experience = "Advanced"
        frequency = 5
        water = 3.5

    fat_percentage = round((bmi / 40) * 100, 2)

    # Generate 7-day plan
    for day in range(1, 8):
        workout_plan.append({
            "day": f"Day {day}",
            "workout_type": workout_type,
            "session_duration": duration,
            "calories_burned": calories,
            "fat_percentage": fat_percentage,
            "water": water,
            "frequency": frequency,
            "experience": experience,
            "bmi": round(bmi, 2)
        })

    return workout_plan