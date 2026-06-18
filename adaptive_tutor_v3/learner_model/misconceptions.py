from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class MisconceptionCatalog:
    concepts: dict[str, list[str]] = field(default_factory=lambda: {
        "fraction addition": [
            "adds denominators instead of finding a common denominator",
            "adds numerators and denominators independently",
            "simplifies before combining unlike fractions",
        ],
        "linear equations": [
            "moves a term without changing its sign",
            "divides only one side of the equation",
            "forgets to distribute across parentheses",
        ],
        "variables": [
            "confuses assignment with equality",
            "treats scope as global in every block",
            "assumes names change the stored value",
        ],
    })

    def suggestions(self, concept: str) -> list[str]:
        key = concept.lower()
        for name, items in self.concepts.items():
            if name in key:
                return items
        return [
            "drops a key term from the definition",
            "reverses cause and effect",
            "applies the rule in the wrong direction",
        ]


def detect_misconception(correct: bool, confidence: float) -> bool:
    return (not correct) and confidence >= 0.6
