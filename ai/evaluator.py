import ollama
import json

from utils.constants import MODEL_NAME


def evaluate_answer(
    question,
    correct_answer,
    user_answer
):

    prompt = f"""
You are an intelligent evaluator.

QUESTION:
{question}

CORRECT ANSWER:
{correct_answer}

USER ANSWER:
{user_answer}

Evaluate whether the user's answer is conceptually correct.

Return ONLY valid JSON.

FORMAT:

{{
   "is_correct": true,
   "feedback": ""
}}
"""

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
    text = text.replace("```", "").strip()

    result = json.loads(text)

    return result