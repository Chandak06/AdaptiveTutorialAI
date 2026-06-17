import unittest

from adaptive_tutor.curriculum.mastery import update_concept_mastery
from adaptive_tutor.curriculum.progression import ProgressionEngine
from adaptive_tutor.revision.scheduler import RevisionScheduler
from adaptive_tutor.state import create_topic_state


def build_test_roadmap() -> dict:
    return {
        "topic": "Stack",
        "levels": [
            {
                "index": 0,
                "name": "Introduction",
                "concepts": [
                    {"id": "l0-stack-definition", "name": "Definition of Stack"},
                ],
            },
            {
                "index": 1,
                "name": "Fundamentals",
                "concepts": [
                    {"id": "l1-push", "name": "Push"},
                ],
            },
        ],
    }


class CurriculumTests(unittest.TestCase):
    def test_mastery_requires_attempts_accuracy_and_understanding_signal(self) -> None:
        topic_state = create_topic_state("Stack", build_test_roadmap())

        result_one = update_concept_mastery(topic_state, "l0-stack-definition", True, "mcq")
        result_two = update_concept_mastery(topic_state, "l0-stack-definition", True, "true_false")
        result_three = update_concept_mastery(topic_state, "l0-stack-definition", True, "fill_blank")

        self.assertFalse(result_one["mastered_now"])
        self.assertFalse(result_two["mastered_now"])
        self.assertTrue(result_three["mastered_now"])
        self.assertIn("Definition of Stack", topic_state["completed_concepts"])

    def test_progression_moves_to_next_level_after_mastery(self) -> None:
        topic_state = create_topic_state("Stack", build_test_roadmap())
        scheduler = RevisionScheduler()
        engine = ProgressionEngine(scheduler)

        update_concept_mastery(topic_state, "l0-stack-definition", True, "mcq")
        update_concept_mastery(topic_state, "l0-stack-definition", True, "true_false")
        update_concept_mastery(topic_state, "l0-stack-definition", True, "fill_blank")

        engine.sync_position(topic_state)
        next_target = engine.next_target(topic_state, current_turn=0)

        self.assertEqual(topic_state["current_level_index"], 1)
        self.assertEqual(next_target["concept_id"], "l1-push")
        self.assertEqual(next_target["question_type"], "mcq")

    def test_revision_queue_adds_and_clears_when_concept_is_mastered(self) -> None:
        topic_state = create_topic_state("Stack", build_test_roadmap())
        scheduler = RevisionScheduler()

        update_concept_mastery(topic_state, "l0-stack-definition", False, "mcq")
        scheduler.schedule(topic_state, "l0-stack-definition", current_turn=1, is_correct=False)

        self.assertEqual(scheduler.next_due_concept(topic_state, current_turn=3), "l0-stack-definition")
        self.assertEqual(len(topic_state["revision_queue"]), 1)

        update_concept_mastery(topic_state, "l0-stack-definition", True, "fill_blank")
        update_concept_mastery(topic_state, "l0-stack-definition", True, "fill_blank")
        update_concept_mastery(topic_state, "l0-stack-definition", True, "fill_blank")
        scheduler.clear(topic_state, "l0-stack-definition")

        self.assertIsNone(scheduler.next_due_concept(topic_state, current_turn=10))
        self.assertEqual(topic_state["revision_queue"], [])


if __name__ == "__main__":
    unittest.main()
