from transformers import pipeline

tip_generator = pipeline("text2text-generation", model="google/flan-t5-base")

def generate_fitness_tip(goal):
    prompt = f"Give one short fitness tip for someone whose goal is {goal}"
    result = tip_generator(prompt, max_length=60)
    return result[0]["generated_text"]
