from adaptive_tutor.llm.ollama_client import OllamaClient


class DistractorGenerator:

    def __init__(self):

        self.llm = OllamaClient()

    def generate(
        self,
        question,
        answer,
        context=""
    ):

        prompt = f"""
Question:
{question}

Correct Answer:
{answer}

Context:
{context}

Generate 3 highly confusing distractors.

Requirements:

- plausible
- technically correct looking
- target common misconceptions
- similar length to answer
- not obviously incorrect

Return STRICT JSON:

{{
    "options": {{
        "A": "",
        "B": "",
        "C": "",
        "D": ""
    }},
    "correct": "A"
}}

Rules:

- Exactly 4 options
- One option must be the correct answer
- Three options must be distractors
- Randomize option order
- Return JSON only
"""

        response = self.llm._chat(
            [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response