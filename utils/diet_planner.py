import pandas as pd

def generate_diet(diet_type, budget):
    df = pd.read_csv("data/diet_dataset.csv")
    df.columns = df.columns.str.strip()

    # Optional filters
    if "Diet Type" in df.columns:
        df = df[df["Diet Type"].str.lower() == diet_type.lower()]

    if "Budget" in df.columns:
        df = df[df["Budget"].str.lower() == budget.lower()]

    # If dataset is smaller than 7, allow repeat
    df = df.sample(7, replace=True).reset_index(drop=True)

    days = [
        "Monday", "Tuesday", "Wednesday",
        "Thursday", "Friday", "Saturday", "Sunday"
    ]

    meal_plan = []

    for i in range(7):
        row = df.iloc[i]

        meal_plan.append({
            "day": days[i],
            "dish": row.get("Dish Name", "-"),
            "calories": row.get("Calories (kcal)", "-"),
            "carbs": row.get("Carbohydrates (g)", "-"),
            "protein": row.get("Protein (g)", "-"),
            "fats": row.get("Fats (g)", "-"),
            "water": "3 liters"
        })

    return meal_plan
