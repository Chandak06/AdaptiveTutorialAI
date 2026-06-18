from __future__ import annotations

from assessment.normalizer import normalize_text


class QuestionValidator:
    def validate(self, question: dict) -> tuple[bool, list[str]]:
        issues: list[str] = []
        prompt = question.get("prompt", "")
        options = question.get("options", [])
        correct = question.get("correct_answer", "")

        if not prompt.strip():
            issues.append("empty prompt")
        if len(options) != 4:
            issues.append("mcq must contain exactly 4 options")
        if not correct.strip():
            issues.append("missing correct answer")
        normalized = [normalize_text(opt) for opt in options]
        if len(set(normalized)) != len(normalized):
            issues.append("duplicate options")
        if correct not in options and normalize_text(correct) not in normalized:
            issues.append("correct answer not in options")
        return len(issues) == 0, issues
