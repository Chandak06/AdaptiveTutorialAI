import ollama

from utils.constants import MODEL_NAME

from utils.json_cleaner import clean_json_response

from ai.prompt_builder import build_prompt

from ai.memory_context import get_recent_history


def generate_lesson(topic, difficulty):

    prompt = build_prompt(
        topic,
        difficulty
    )

    history = get_recent_history()

    messages = history.copy()

    messages.append({

        "role": "user",

        "content": prompt
    })

    for _ in range(3):

        response = ollama.chat(

            model=MODEL_NAME,

            messages=messages
        )

        text = response["message"]["content"]

        try:

            return clean_json_response(text)

        except:

            continue

    raise Exception(
        "Failed to generate valid JSON."
    )