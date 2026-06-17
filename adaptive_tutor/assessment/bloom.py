from __future__ import annotations


BLOOM_KEYWORDS = {
    "remember": [
        "define",
        "list",
        "identify",
        "name",
    ],
    "understand": [
        "explain",
        "describe",
        "summarize",
    ],
    "apply": [
        "solve",
        "implement",
        "use",
    ],
    "analyze": [
        "compare",
        "differentiate",
        "analyze",
    ],
    "evaluate": [
        "justify",
        "evaluate",
        "critique",
    ],
    "create": [
        "design",
        "develop",
        "create",
    ],
}


BLOOM_SCORES = {
    "Remember": 20,
    "Understand": 40,
    "Apply": 60,
    "Analyze": 75,
    "Evaluate": 90,
    "Create": 100,
}


def classify_bloom_level(question: str) -> str:
    q = question.lower()

    for level, words in BLOOM_KEYWORDS.items():
        for word in words:
            if word in q:
                return level.title()

    return "Understand"


def bloom_score(question: str) -> int:
    level = classify_bloom_level(question)

    return BLOOM_SCORES.get(
        level,
        40,
    )


def bloom_difficulty(question: str) -> str:
    score = bloom_score(question)

    if score >= 90:
        return "Expert"

    if score >= 75:
        return "Hard"

    if score >= 50:
        return "Medium"

    return "Easy"