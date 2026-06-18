from __future__ import annotations


def question_prompt(topic: str, concept: str, objective: str, blueprint: dict) -> str:
    return (
        "You are an expert tutor generating a concept-driven question.\n"
        f"Topic: {topic}\n"
        f"Concept: {concept}\n"
        f"Learning objective: {objective}\n\n"
        f"Blueprint: {blueprint}\n\n"
        "Rules:\n"
        "- never generate from the topic alone\n"
        "- align the item to the objective\n"
        "- keep distractors misconception-based\n"
        "- return concise pedagogically meaningful output"
    )
