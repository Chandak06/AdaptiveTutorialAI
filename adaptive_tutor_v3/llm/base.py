from __future__ import annotations


class BaseLLMClient:
    def generate_answer(self, question: str, context: str = "") -> str:
        raise NotImplementedError
