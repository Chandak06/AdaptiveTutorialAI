from __future__ import annotations

import random
from typing import Any

from adaptive_tutor.config import (
    DEFAULT_MODEL_NAME,
    LLM_MAX_RETRIES,
    OLLAMA_HOST,
    OLLAMA_TIMEOUT_SECONDS,
)
from adaptive_tutor.llm.parser import (
    JSONParseError,
    coerce_evaluation_payload,
    coerce_lesson_payload,
    coerce_roadmap_payload,
    parse_json_object,
)
from adaptive_tutor.llm.prompts import (
    build_evaluation_messages,
    build_lesson_messages,
    build_roadmap_messages,
)

try:
    from ollama import Client
except ImportError:  # pragma: no cover - import guard for test environments
    Client = None


class OllamaClient:
    def __init__(
        self,
        model_name: str = DEFAULT_MODEL_NAME,
        host: str = OLLAMA_HOST,
        timeout_seconds: int = OLLAMA_TIMEOUT_SECONDS,
    ) -> None:
        self.model_name = model_name
        self.host = host
        self.timeout_seconds = timeout_seconds
        self.client = Client(host=host, timeout=timeout_seconds) if Client else None

    def _chat(self, messages: list[dict[str, str]]) -> str:
        if self.client is None:
            raise RuntimeError("Ollama client is unavailable.")

        last_error: Exception | None = None

        for _ in range(LLM_MAX_RETRIES):
            try:
                response = self.client.chat(
                    model=self.model_name,
                    messages=messages,
                    format="json",
                    options={
                        "temperature": 0.2,
                        "num_ctx": 4096,
                    },
                )
                content = response.get("message", {}).get("content", "").strip()
                if not content:
                    raise RuntimeError("Ollama returned an empty response.")
                return content
            except Exception as exc:  # pragma: no cover - network/host failures
                last_error = exc

        raise RuntimeError(f"Ollama request failed: {last_error}") from last_error

    def generate_roadmap(self, topic: str) -> dict[str, Any] | None:
        try:
            raw_text = self._chat(build_roadmap_messages(topic))
            payload = parse_json_object(raw_text)
            return coerce_roadmap_payload(topic, payload)
        except Exception:
            return None

    def _fallback_lesson(self, request: dict[str, Any]) -> dict[str, Any]:
        concept_name = request["concept_name"]
        peer_concepts = [
            concept
            for concept in request.get("peer_concepts", [])
            if concept != concept_name
        ]
        question_type = request["question_type"]

        lesson = {
            "message": (
                f"Let's keep building your understanding of {concept_name} in {request['topic']}. "
                f"This belongs to the {request['level_name']} stage, so focus on what it is, why it matters, "
                "and one concrete use or example."
            ),
            "question": {
                "type": question_type,
                "prompt": "",
                "options": [],
                "answer": concept_name,
                "rubric": [
                    f"Clearly identify {concept_name}",
                    "State its purpose or behavior",
                    "Give one example or use case",
                ],
                "concept_name": concept_name,
            },
            "hint": f"Center your thinking on the role of {concept_name} inside {request['topic']}.",
            "answer_explanation": (
                f"A strong answer should explain what {concept_name} means, when it is used, "
                "and how it affects the topic overall."
            ),
            "takeaways": [
                f"{concept_name} is part of {request['topic']}.",
                "Mastery grows when you can explain the concept and apply it.",
            ],
        }

        if question_type == "mcq":
            options = [concept_name] + peer_concepts[:3]
            while len(options) < 4:
                options.append(f"Unrelated idea {len(options) + 1}")
            rotation = sum(ord(char) for char in concept_name) % len(options)
            options = options[rotation:] + options[:rotation]
            lesson["question"]["prompt"] = "Which concept are we focusing on right now?"
            lesson["question"]["options"] = options
            lesson["question"]["answer"] = concept_name
        elif question_type == "true_false":
            lesson["question"]["prompt"] = (
                f"True or False: {concept_name} is a concept in your current {request['topic']} roadmap."
            )
            lesson["question"]["answer"] = "True"
        elif question_type == "fill_blank":
            lesson["question"]["prompt"] = (
                f"Fill in the blank: The concept we are practicing in {request['topic']} is ____."
            )
        else:
            lesson["question"]["prompt"] = (
                f"In your own words, explain {concept_name} and give one relevant example."
            )

        return lesson

    def generate_lesson(self, request: dict[str, Any]) -> dict[str, Any]:
        last_error: Exception | None = None

        for _ in range(LLM_MAX_RETRIES):
            try:
                raw_text = self._chat(build_lesson_messages(request))
                payload = parse_json_object(raw_text)
                return coerce_lesson_payload(payload, request)
            except (RuntimeError, JSONParseError, ValueError) as exc:
                last_error = exc

        fallback = self._fallback_lesson(request)
        if last_error:
            fallback["takeaways"].append(f"Fallback used after LLM issue: {last_error}")
        return fallback

    def grade_descriptive(
        self,
        question: dict[str, Any],
        user_answer: str,
    ) -> dict[str, Any] | None:
        try:
            raw_text = self._chat(build_evaluation_messages(question, user_answer))
            payload = parse_json_object(raw_text)
            return coerce_evaluation_payload(payload)
        except Exception:
            return None
