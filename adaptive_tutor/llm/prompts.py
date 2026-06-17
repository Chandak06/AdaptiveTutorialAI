from __future__ import annotations

from typing import Any


def _format_history(history: list[dict[str, str]]) -> str:
    if not history:
        return "No recent turns."

    lines = []

    for item in history[-6:]:

        role = item.get(
            "role",
            "unknown"
        ).upper()

        content = item.get(
            "content",
            ""
        ).strip().replace(
            "\n",
            " "
        )

        content = content[:160]

        lines.append(
            f"{role}: {content}"
        )

    return "\n".join(lines)


def build_roadmap_messages(
    topic: str
) -> list[dict[str, str]]:

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
    {{
      "index": 0,
      "name": "Introduction",
      "concepts": ["...", "...", "..."]
    }}
  ]
}}

Rules:
- Include levels with indexes 0 through 9.
- Each level needs 3 to 5 concepts.
- Progress from beginner to expert.
- Concepts must be specific.
- Return JSON only.
"""

    return [
        {
            "role": "system",
            "content": system_prompt
        },
        {
            "role": "user",
            "content": user_prompt
        }
    ]


def build_lesson_messages(
    request: dict[str, Any]
) -> list[dict[str, str]]:

    system_prompt = (
        "You are a warm but rigorous tutor. "
        "Return strict JSON only."
    )

    user_prompt = f"""
Topic: {request["topic"]}
Current level index: {request["level_index"]}
Current level name: {request["level_name"]}
Concept: {request["concept_name"]}
Learning mode: {request["mode"]}
Required question type: {request["question_type"]}
Highest level reached: {request["highest_level_reached"]}
Confidence: {request["confidence"]}
Weak areas: {request["weak_areas"]}
Recent summary: {request["summary"] or "No prior summary."}

Conversation:
{_format_history(request["recent_history"])}

Return JSON:

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
- Match required question type.
- Keep concise.
- If MCQ provide exactly 4 options.
- Return JSON only.
"""

    return [
        {
            "role": "system",
            "content": system_prompt
        },
        {
            "role": "user",
            "content": user_prompt
        }
    ]


def build_evaluation_messages(
    question: dict[str, Any],
    user_answer: str,
) -> list[dict[str, str]]:

    system_prompt = (
        "You evaluate learner answers. "
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
"""

    return [
        {
            "role": "system",
            "content": system_prompt
        },
        {
            "role": "user",
            "content": user_prompt
        }
    ]


def build_hard_question_messages(
    topic: str,
    context: str,
    related_questions: str,
) -> list[dict[str, str]]:

    return [
        {
            "role": "system",
            "content": (
                "You create advanced adaptive tutor questions. "
                "Return JSON only."
            )
        },
        {
            "role": "user",
            "content": f"""
Topic:
{topic}

Learning Context:
{context}

Previous Related Questions:
{related_questions}

Generate a significantly harder question.

Requirements:

- analytical
- scenario based
- multi-step reasoning
- difficult distractors
- higher bloom level

Return JSON:

{{
  "question":"",
  "answer":"",
  "difficulty":"Hard"
}}
"""
        }
    ]


def build_expert_question_messages(
    topic: str,
    context: str,
    related_questions: str,
) -> list[dict[str, str]]:

    return [
        {
            "role": "system",
            "content": (
                "You create expert-level questions. "
                "Return JSON only."
            )
        },
        {
            "role": "user",
            "content": f"""
Topic:
{topic}

Learning Context:
{context}

Previous Expert Questions:
{related_questions}

Generate an expert-level question.

Requirements:

- synthesis
- evaluation
- reasoning
- interview quality

Return JSON:

{{
  "question":"",
  "answer":"",
  "difficulty":"Expert"
}}
"""
        }
    ]


def build_distractor_messages(
    question: str,
    answer: str,
) -> list[dict[str, str]]:

    return [
        {
            "role": "system",
            "content": (
                "Generate highly confusing MCQ distractors. "
                "Return JSON only."
            )
        },
        {
            "role": "user",
            "content": f"""
Question:
{question}

Correct Answer:
{answer}

Generate 3 confusing distractors.

Requirements:

- plausible
- misconception based
- same length as answer

Return JSON:

{{
  "options": {{
    "A":"",
    "B":"",
    "C":"",
    "D":""
  }},
  "correct":""
}}
"""
        }
    ]


def build_question_ranking_messages(
    question: str,
) -> list[dict[str, str]]:

    return [
        {
            "role": "system",
            "content": (
                "Rank educational questions. "
                "Return JSON only."
            )
        },
        {
            "role": "user",
            "content": f"""
Question:
{question}

Return:

{{
  "bloom_level":"",
  "difficulty_score":0,
  "difficulty":""
}}
"""
        }
    ]