import os
from openai import OpenAI

# ---------------- ENV CHECK ----------------
if "HF_TOKEN" not in os.environ:
    raise EnvironmentError(
        "HF_TOKEN not found. Please set it using:\n"
        "setx HF_TOKEN \"hf_your_token_here\" and restart terminal."
    )

# ---------------- CLIENT ----------------
client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=os.environ["HF_TOKEN"],
)

# ---------------- SYSTEM PROMPT ----------------
SYSTEM_PROMPT = (
    "You are a friendly fitness companion. "
    "You talk like a close friend. "
    "You are supportive, motivating, and human-like. "
    "Keep responses short and warm. "
    "Ask natural follow-up questions."
)

# ---------------- CHAT FUNCTION ----------------
def ask_bot(user_message, chat_history=None):
    if chat_history is None:
        chat_history = []

    messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    # Add last few messages for memory
    for msg in chat_history[-6:]:
        messages.append({
            "role": msg["role"],
            "content": msg["content"]
        })

    messages.append({"role": "user", "content": user_message})

    try:
        completion = client.chat.completions.create(
            model="meta-llama/Llama-3.2-3B-Instruct:novita",
            messages=messages,
            temperature=0.7,
            max_tokens=150,
        )

        return completion.choices[0].message.content.strip()

    except Exception as e:
        return f"AI is having trouble right now 😅 ({e})"
