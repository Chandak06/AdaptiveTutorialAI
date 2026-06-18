from __future__ import annotations

import os

from llm.base import BaseLLMClient
from llm.local import LocalLLMClient


class OpenAIClient(BaseLLMClient):
    def __init__(self, api_key: str | None = None):
        self.api_key = api_key

    def generate_answer(self, question: str, context: str = "") -> str:
        return LocalLLMClient().generate_answer(question, context)


class AnthropicClient(BaseLLMClient):
    def __init__(self, api_key: str | None = None):
        self.api_key = api_key

    def generate_answer(self, question: str, context: str = "") -> str:
        return LocalLLMClient().generate_answer(question, context)


class GeminiClient(BaseLLMClient):
    def __init__(self, api_key: str | None = None):
        self.api_key = api_key

    def generate_answer(self, question: str, context: str = "") -> str:
        return LocalLLMClient().generate_answer(question, context)


def get_llm_client(provider: str | None = None) -> BaseLLMClient:
    provider = (provider or os.getenv("LLM_PROVIDER", "local")).lower()
    if provider == "openai" and os.getenv("OPENAI_API_KEY"):
        return OpenAIClient(os.getenv("OPENAI_API_KEY"))
    if provider == "anthropic" and os.getenv("ANTHROPIC_API_KEY"):
        return AnthropicClient(os.getenv("ANTHROPIC_API_KEY"))
    if provider in {"gemini", "google"} and os.getenv("GEMINI_API_KEY"):
        return GeminiClient(os.getenv("GEMINI_API_KEY"))
    return LocalLLMClient()
