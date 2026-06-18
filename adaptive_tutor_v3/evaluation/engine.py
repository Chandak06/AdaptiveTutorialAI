from __future__ import annotations

from evaluation.scoring import estimate_confidence, infer_misconception, mastery_delta, retention_delta, score_correctness


class EvaluationEngine:
    def evaluate(self, question, answer_text: str, learner_state=None, confidence: float | None = None) -> dict:
        mastery = float(getattr(learner_state, "mastery", 0.2) if learner_state is not None else 0.2)
        recommended_difficulty = int(question.difficulty)
        is_correct, semantic_score = score_correctness(
            {
                "correct_answer": question.correct_answer,
                "concept_slug": question.concept_slug,
            },
            answer_text,
        )
        eval_confidence = estimate_confidence(confidence, semantic_score, mastery)
        mis = infer_misconception(
            {"concept_slug": question.concept_slug},
            answer_text,
            is_correct,
            eval_confidence,
        )
        m_delta = mastery_delta(is_correct, eval_confidence, recommended_difficulty, mastery)
        r_delta = retention_delta(is_correct, eval_confidence)
        next_action = "advance" if is_correct and mastery > 0.45 else "revision"
        if not is_correct and eval_confidence < 0.45:
            next_action = "reteach"
        if not is_correct and eval_confidence >= 0.75:
            next_action = "misconception_fix"

        return {
            "correct": is_correct,
            "confidence": eval_confidence,
            "mastery_change": m_delta,
            "retention_change": r_delta,
            "misconception": mis,
            "recommended_difficulty": max(1, min(5, recommended_difficulty + (1 if is_correct else -1))),
            "next_action": next_action,
            "next_concept": question.metadata_json.get("next_concept", ""),
            "answer_text": answer_text,
            "semantic_score": semantic_score,
        }
