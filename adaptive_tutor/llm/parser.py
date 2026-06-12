from __future__ import annotations

import json
import re
from typing import Any


class JSONParseError(ValueError):
    pass


def extract_json_object(text: str) -> str:
    if not isinstance(text, str):
        raise JSONParseError("LLM output is not text.")

    fenced_match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL)
    if fenced_match:
        return fenced_match.group(1)

    start = text.find("{")
    if start == -1:
        raise JSONParseError("No JSON object found.")

    depth = 0
    in_string = False
    escaping = False

    for index in range(start, len(text)):
        char = text[index]

        if escaping:
            escaping = False
            continue

        if char == "\\":
            escaping = True
            continue

        if char == '"':
            in_string = not in_string
            continue

        if in_string:
            continue

        if char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                return text[start : index + 1]

    raise JSONParseError("Unbalanced JSON object.")


def parse_json_object(text: str) -> dict[str, Any]:
    candidate = extract_json_object(text)

    try:
        payload = json.loads(candidate)
    except json.JSONDecodeError as exc:
        raise JSONParseError(f"Invalid JSON: {exc}") from exc

    if not isinstance(payload, dict):
        raise JSONParseError("Top-level JSON must be an object.")

    return payload


def coerce_roadmap_payload(topic: str, payload: dict[str, Any]) -> dict[str, Any]:
    payload["topic"] = payload.get("topic") or topic
    levels = payload.get("levels")
    if not isinstance(levels, list):
        raise JSONParseError("Roadmap must contain a levels list.")
    return payload


def coerce_lesson_payload(
    payload: dict[str, Any],
    request: dict[str, Any],
) -> dict[str, Any]:
    question = payload.get("question")
    if not isinstance(question, dict):
        raise JSONParseError("Lesson question must be an object.")

    question_type = question.get("type") or request["question_type"]
    question_type = str(question_type).strip() or request["question_type"]
    if question_type != request["question_type"]:
        raise JSONParseError("Question type did not match the requested type.")
    prompt = question.get("prompt") or question.get("question")
    answer = question.get("answer")

    if not isinstance(prompt, str) or not prompt.strip():
        raise JSONParseError("Question prompt is missing.")

    if answer is None or str(answer).strip() == "":
        raise JSONParseError("Question answer is missing.")

    options = question.get("options", [])
    if not isinstance(options, list):
        options = []

    rubric = question.get("rubric", [])
    if not isinstance(rubric, list):
        rubric = []

    lesson = {
        "message": str(payload.get("message", "")).strip(),
        "question": {
            "type": question_type,
            "prompt": str(prompt).strip(),
            "options": [str(option).strip() for option in options if str(option).strip()],
            "answer": str(answer).strip(),
            "rubric": [str(item).strip() for item in rubric if str(item).strip()],
            "concept_name": request["concept_name"],
        },
        "hint": str(payload.get("hint", "")).strip(),
        "answer_explanation": str(payload.get("answer_explanation", "")).strip(),
        "takeaways": payload.get("takeaways", []),
    }

    if question_type == "mcq" and len(lesson["question"]["options"]) != 4:
        raise JSONParseError("MCQ questions must contain exactly 4 options.")

    if question_type == "true_false":
        normalized_answer = lesson["question"]["answer"].strip().lower()
        if normalized_answer not in {"true", "false"}:
            raise JSONParseError("True/False answer must be True or False.")

    return lesson


def coerce_evaluation_payload(payload: dict[str, Any]) -> dict[str, Any]:
    if "is_correct" not in payload:
        raise JSONParseError("Evaluation payload is missing is_correct.")

    return {
        "is_correct": bool(payload["is_correct"]),
        "feedback": str(payload.get("feedback", "")).strip(),
        "score": float(payload.get("score", 0) or 0),
    }
