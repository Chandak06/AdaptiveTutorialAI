import ollama
import json

from utils.constants import MODEL_NAME


def load_prompt(path):

    with open(path, "r", encoding="utf-8") as file:

        return file.read()


def evaluate_answer(
    question,
    correct_answer,
    user_answer
):

    evaluation_prompt = load_prompt(
        "prompts/evaluation_prompt.txt"
    )

    prompt = evaluation_prompt.format(

        question=question,

        correct_answer=correct_answer,

        user_answer=user_answer
    )

    response = ollama.chat(

        model=MODEL_NAME,

        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    text = response["message"]["content"]

    text = text.replace("```json", "")
    text = text.replace("```", "")
    text = text.strip()

    return json.loads(text)

