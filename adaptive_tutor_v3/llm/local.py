from __future__ import annotations

from llm.base import BaseLLMClient


class LocalLLMClient(BaseLLMClient):
    def generate_answer(self, question: str, context: str = "") -> str:
        bullets = [line.strip() for line in context.splitlines() if line.strip()]
        if bullets:
            focus = bullets[0][:240]
            return f"Using the available context, the best-supported answer is: {focus}"
        return f"The question '{question}' is best answered by isolating the core concept, checking definitions, and applying the rule step by step."
