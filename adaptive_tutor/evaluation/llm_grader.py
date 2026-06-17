from __future__ import annotations


def build_grading_prompt(
    question: str,
    reference_answer: str,
    student_answer: str,
) -> str:

    prompt = f"""
You are an expert educational evaluator.

Question:
{question}

Reference Answer:
{reference_answer}

Student Answer:
{student_answer}

Evaluate the student's answer.

Return STRICT JSON:

{{
    "score": 0,
    "missing_concepts": [],
    "misconceptions": [],
    "bloom_level": "",
    "difficulty_estimate": 0,
    "feedback": ""
}}

Rules:

- score must be between 0 and 10
- identify missing concepts
- identify misconceptions
- estimate bloom level demonstrated
- estimate answer difficulty
- keep feedback concise
- return JSON only
"""

    return prompt