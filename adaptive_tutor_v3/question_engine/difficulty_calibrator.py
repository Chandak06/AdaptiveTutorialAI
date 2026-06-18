from __future__ import annotations


class DifficultyCalibrator:
    def calibrate(self, blueprint: dict, question_text: str, distractors: list[str]) -> int:
        difficulty = int(blueprint.get("difficulty", 1))
        length_factor = 1 if len(question_text.split()) > 20 else 0
        distractor_factor = 1 if any("mistake" in d.lower() or "error" in d.lower() for d in distractors) else 0
        bloom = str(blueprint.get("bloom_level", "understand"))
        bloom_factor = {"remember": 0, "understand": 0, "apply": 1, "analyze": 2, "evaluate": 2, "create": 3}.get(bloom, 0)
        return max(1, min(5, difficulty + length_factor + distractor_factor + min(1, bloom_factor)))
