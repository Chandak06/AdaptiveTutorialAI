from adaptive_tutor.assessment.bloom import (
    classify_bloom_level,
    bloom_score,
    bloom_difficulty,
)


class QuestionRanker:

    def __init__(self):
        pass

    def rank(self, question):

        bloom_level = classify_bloom_level(
            question
        )

        score = bloom_score(
            question
        )

        difficulty = bloom_difficulty(
            question
        )

        complexity_score = score

        misconception_score = min(
            100,
            score + 10
        )

        final_score = int(
            (
                score * 0.4
                + complexity_score * 0.3
                + misconception_score * 0.3
            )
        )

        return {
            "question": question,
            "bloom_level": bloom_level,
            "difficulty_score": score,
            "complexity_score": complexity_score,
            "misconception_score": misconception_score,
            "final_score": final_score,
            "difficulty": difficulty,
        }