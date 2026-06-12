from __future__ import annotations

from typing import Any


def _format_history(history: list[dict[str, str]]) -> str:
    if not history:
        return "No recent turns."

    lines = []
    for item in history[-6:]:
        role = item.get("role", "unknown").upper()
        content = item.get("content", "").strip().replace("\n", " ")
        content = content[:160]
        lines.append(f"{role}: {content}")
    return "\n".join(lines)


def build_roadmap_messages(topic: str) -> list[dict[str, str]]:
    system_prompt = (
        "You design rigorous learning roadmaps. "
        "Return JSON only. No markdown. "
        "Create exactly 10 levels from beginner to expert."
    )
    user_prompt = f"""
Topic: {topic}

Return JSON with this schema:
{{
  "topic": "{topic}",
  "levels": [
    {{"index": 0, "name": "Introduction", "concepts": ["...", "...", "..."]}}
  ]
}}

Rules:
- Include levels with indexes 0 through 9.
- Each level needs 3 to 5 concepts.
- Progress from intuition to exam-level to expert extensions.
- Concepts must be specific, teachable, and non-redundant.
- Return JSON only.
""".strip()
    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]


def build_lesson_messages(request: dict[str, Any]) -> list[dict[str, str]]:
    system_prompt = (
        "You are a warm but rigorous tutor. "
        "Teach only the requested concept. "
        "Do not decide progression. "
        "Return strict JSON only with no markdown."
    )
    user_prompt = f"""
Topic: {request["topic"]}
Current level index: {request["level_index"]}
Current level name: {request["level_name"]}
Concept: {request["concept_name"]}
Learning mode: {request["mode"]}
Required question type: {request["question_type"]}
Highest level reached so far: {request["highest_level_reached"]}
Current confidence: {request["confidence"]}
Weak areas: {request["weak_areas"]}
Recent summary: {request["summary"] or "No prior summary."}
Recent conversation:
{_format_history(request["recent_history"])}

Return JSON with this schema:
{{
  "message": "",
  "question": {{
    "type": "{request["question_type"]}",
    "prompt": "",
    "options": [],
    "answer": "",
    "rubric": ["", ""]
  }},
  "hint": "",
  "answer_explanation": "",
  "takeaways": ["", ""]
}}

Rules:
- Keep the explanation friendly and concrete.
- Match the required question type exactly.
- If the type is mcq, provide exactly 4 options and set answer to the exact correct option text.
- If the type is true_false, set answer to True or False.
- Use concise context because the local model is small.
- Avoid hallucinated prerequisites.
- Make the question directly test the named concept.
- Return JSON only.
""".strip()
    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]


def build_evaluation_messages(
    question: dict[str, Any],
    user_answer: str,
) -> list[dict[str, str]]:
    system_prompt = (
        "You evaluate learner answers. "
        "Be concise, fair, and structured. "
        "Return JSON only."
    )
    user_prompt = f"""
Question type: {question.get("type", "")}
Concept: {question.get("concept_name", "")}
Question: {question.get("prompt", "")}
Correct answer: {question.get("answer", "")}
Rubric: {question.get("rubric", [])}
Learner answer: {user_answer}

Return JSON:
{{
  "is_correct": true,
  "feedback": "",
  "score": 0
}}

Rules:
- Accept paraphrases if the meaning is correct.
- Reject unrelated answers.
- Keep feedback under 30 words.
- Return JSON only.
""".strip()
    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]
