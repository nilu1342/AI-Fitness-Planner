# utils/food_analyzer.py

import base64
import os
from openai import OpenAI

# Initialize Hugging Face OpenAI-compatible client
client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=os.environ["HF_TOKEN"],
)

def analyze_food_image(image_path):
    """
    Analyze uploaded food image using Qwen/Qwen2.5-VL-7B-Instruct
    """

    # Read and encode image as base64
    with open(image_path, "rb") as img:
        image_base64 = base64.b64encode(img.read()).decode("utf-8")

    prompt = (
        "You are a nutrition expert.\n"
        "Identify the food in the image and provide:\n"
        "1. Food name\n"
        "2. Estimated calories\n"
        "3. Protein, carbs, fats\n"
        "Respond briefly."
    )

    completion = client.chat.completions.create(
        model="Qwen/Qwen2.5-VL-7B-Instruct:hyperbolic",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{image_base64}"
                        }
                    }
                ]
            }
        ],
        max_tokens=300,
        temperature=0.4,
    )

    response_text = completion.choices[0].message.content

    # Basic food detection for UI
    food = "Unknown"
    for f in ["burger", "pizza", "salad", "pasta", "sandwich", "rice"]:
        if f in response_text.lower():
            food = f.capitalize()
            break

    return {
        "food": food,
        "caption": response_text,
        "nutrition": {
            "details": "Estimated values (AI-based)"
        }
    }
