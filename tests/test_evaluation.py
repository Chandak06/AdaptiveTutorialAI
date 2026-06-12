import unittest

from adaptive_tutor.evaluation.descriptive import evaluate_descriptive_answer
from adaptive_tutor.evaluation.mcq import normalize_mcq_answer
from adaptive_tutor.evaluation.true_false import normalize_true_false_answer


class EvaluationTests(unittest.TestCase):
    def test_mcq_normalizes_numeric_letter_and_text_inputs(self) -> None:
        options = ["Push", "Pop", "Peek", "isEmpty"]

        self.assertEqual(normalize_mcq_answer("2", options), "Pop")
        self.assertEqual(normalize_mcq_answer("b", options), "Pop")
        self.assertEqual(normalize_mcq_answer("peek", options), "Peek")

    def test_true_false_normalizes_requested_input_forms(self) -> None:
        self.assertEqual(normalize_true_false_answer("True"), "True")
        self.assertEqual(normalize_true_false_answer("t"), "True")
        self.assertEqual(normalize_true_false_answer("1"), "True")
        self.assertEqual(normalize_true_false_answer("False"), "False")
        self.assertEqual(normalize_true_false_answer("f"), "False")
        self.assertEqual(normalize_true_false_answer("2"), "False")

    def test_descriptive_evaluation_uses_local_fallback(self) -> None:
        question = {
            "concept_name": "Stack",
            "answer": "A stack follows last in first out order and supports push and pop.",
            "rubric": ["Mention LIFO", "Mention push or pop"],
        }

        result = evaluate_descriptive_answer(
            question=question,
            user_answer="A stack is LIFO and you use push and pop operations.",
            llm_client=None,
        )

        self.assertTrue(result["is_correct"])
        self.assertGreater(result["score"], 0)


if __name__ == "__main__":
    unittest.main()
