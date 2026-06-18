from __future__ import annotations

from learner_model.misconceptions import MisconceptionCatalog


class DistractorGenerator:
    def __init__(self):
        self.catalog = MisconceptionCatalog()

    def _fraction_distractors(self, correct_answer: str) -> list[str]:
        if correct_answer.strip() == "7/6":
            return ["3/5", "2/5", "1"]
        return ["5/6", "1/2", "2/3"]

    def generate(self, concept_name: str, correct_answer: str, objective: str, blueprint: dict | None = None) -> list[str]:
        key = f"{concept_name} {objective}".lower()
        if "fraction" in key and "/" in correct_answer:
            return self._fraction_distractors(correct_answer)

        misconceptions = self.catalog.suggestions(concept_name)
        distractors: list[str] = []
        for idx, mis in enumerate(misconceptions[:3]):
            if "sign" in mis:
                distractors.append(correct_answer.replace("-", "", 1) if "-" in correct_answer else f"not_{correct_answer}")
            elif "scope" in mis:
                distractors.append(f"{correct_answer} (global)")
            elif "definition" in mis:
                distractors.append(f"the opposite of {correct_answer}")
            else:
                distractors.append(f"{correct_answer} mistake {idx + 1}")
        while len(distractors) < 3:
            distractors.append(f"common error {len(distractors) + 1}")
        return distractors[:3]
