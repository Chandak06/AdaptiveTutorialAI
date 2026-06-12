from __future__ import annotations

import time
from typing import Any

from adaptive_tutor.analytics import AnalyticsTracker, build_session_report, build_topic_report
from adaptive_tutor.config import MAX_HISTORY, QUESTION_LABELS
from adaptive_tutor.curriculum import ProgressionEngine, RoadmapGenerator, update_concept_mastery
from adaptive_tutor.evaluation import (
    evaluate_descriptive_answer,
    evaluate_mcq_answer,
    evaluate_true_false_answer,
    normalize_mcq_answer,
    normalize_true_false_answer,
)
from adaptive_tutor.llm import OllamaClient
from adaptive_tutor.revision import RevisionScheduler
from adaptive_tutor.state import create_topic_state, utc_now_iso
from adaptive_tutor.storage import SaveManager


class AdaptiveTutorApp:
    def __init__(self) -> None:
        self.save_manager = SaveManager()
        self.session = self.save_manager.load_session()
        self.llm_client = OllamaClient()
        self.revision_scheduler = RevisionScheduler()
        self.progression_engine = ProgressionEngine(self.revision_scheduler)
        self.roadmap_generator = RoadmapGenerator(self.llm_client)
        self.analytics_tracker = AnalyticsTracker()
        self.analytics_tracker.sync(self.session)

    def run(self) -> None:
        print("\n=== AdaptiveTutorAI ===\n")
        print("Structured, adaptive, and persistent learning with roadmap-based progression.\n")

        while True:
            topic_name = input("Enter a topic to study (or 'exit'): ").strip()
            if not topic_name:
                print("Please enter a topic name.\n")
                continue

            if topic_name.lower() == "exit":
                break

            topic_state = self._get_or_create_topic(topic_name)
            self._run_topic(topic_state)

            another = input("\nStudy another topic? (y/n): ").strip().lower()
            if another != "y":
                break

        self.save_manager.save_session(self.session)
        session_report = build_session_report(self.session)
        print("\nSession summary:")
        print(
            f"- Topics tracked: {session_report['topics_tracked']}\n"
            f"- Accuracy: {session_report['accuracy']}%\n"
            f"- Concepts mastered: {session_report['concepts_mastered']}\n"
            f"- Topics completed: {session_report['topics_completed']}"
        )

    def _get_or_create_topic(self, topic_name: str) -> dict[str, Any]:
        normalized_name = " ".join(topic_name.split())

        for saved_name, saved_topic in self.session["topics"].items():
            if saved_name.casefold() == normalized_name.casefold():
                self.session["current_topic"] = saved_name
                return saved_topic

        roadmap = self.roadmap_generator.build(normalized_name)
        topic_state = create_topic_state(normalized_name, roadmap)
        self.session["topics"][normalized_name] = topic_state
        self.session["topic_order"].append(normalized_name)
        self.session["current_topic"] = normalized_name
        self.save_manager.save_session(self.session)
        return topic_state

    def _run_topic(self, topic_state: dict[str, Any]) -> None:
        print(f"\nNow studying: {topic_state['topic']}")
        print("The curriculum engine controls progression, so concepts will unlock level by level.\n")

        while True:
            target = self.progression_engine.next_target(
                topic_state=topic_state,
                current_turn=self.session["global_turn"],
            )

            if target is None:
                topic_state["completed"] = True
                self.analytics_tracker.sync(self.session)
                self.save_manager.save_session(self.session)
                print(f"You completed the full roadmap for {topic_state['topic']}.")
                return

            lesson = self._build_lesson(topic_state, target)
            self._display_lesson(topic_state, target, lesson)

            started_at = time.time()
            user_answer = self._collect_answer(lesson["question"])
            evaluation = self._evaluate_answer(lesson["question"], user_answer)
            elapsed_seconds = time.time() - started_at

            self._display_feedback(lesson, evaluation)
            self._apply_result(
                topic_state=topic_state,
                target=target,
                lesson=lesson,
                user_answer=user_answer,
                evaluation=evaluation,
                elapsed_seconds=elapsed_seconds,
            )
            self._display_status(topic_state)

            if topic_state["completed"]:
                print(f"You completed the full roadmap for {topic_state['topic']}.")
                return

            cont = input("\nContinue this topic? (y/n): ").strip().lower()
            if cont != "y":
                return

    def _build_lesson(
        self,
        topic_state: dict[str, Any],
        target: dict[str, Any],
    ) -> dict[str, Any]:
        level = topic_state["roadmap"]["levels"][target["level_index"]]
        peer_concepts = [concept["name"] for concept in level["concepts"]]
        request = {
            "topic": topic_state["topic"],
            "mode": target["mode"],
            "concept_name": target["concept_name"],
            "level_index": target["level_index"],
            "level_name": target["level_name"],
            "question_type": target["question_type"],
            "highest_level_reached": topic_state["highest_level_reached"],
            "confidence": topic_state["confidence"],
            "weak_areas": topic_state["weak_areas"][:5],
            "summary": topic_state["conversation"]["summary"],
            "recent_history": topic_state["conversation"]["history"][-6:],
            "peer_concepts": peer_concepts,
        }
        return self.llm_client.generate_lesson(request)

    def _display_lesson(
        self,
        topic_state: dict[str, Any],
        target: dict[str, Any],
        lesson: dict[str, Any],
    ) -> None:
        print("\n" + "=" * 70)
        print(f"Topic: {topic_state['topic']}")
        print(f"Level {target['level_index']}: {target['level_name']}")
        print(f"Concept: {target['concept_name']}")
        print(f"Mode: {target['mode'].capitalize()}")
        print(f"Question type: {QUESTION_LABELS.get(target['question_type'], target['question_type'])}")
        print("=" * 70)
        print("\nTutor:\n")
        print(lesson["message"])
        print("\nQuestion:")
        print(lesson["question"]["prompt"])

        if lesson["question"]["type"] == "mcq":
            for index, option in enumerate(lesson["question"]["options"], start=1):
                letter = chr(64 + index)
                print(f"{index}. {option} ({letter})")
        elif lesson["question"]["type"] == "true_false":
            print("1. True")
            print("2. False")

    def _collect_answer(self, question: dict[str, Any]) -> str:
        question_type = question["type"]

        while True:
            prompt = "\nYour answer: "
            user_answer = input(prompt).strip()

            if question_type == "mcq":
                if normalize_mcq_answer(user_answer, question["options"]) is not None:
                    return user_answer
                print("Use 1-4, A-D, or the option text.\n")
                continue

            if question_type == "true_false":
                if normalize_true_false_answer(user_answer) is not None:
                    return user_answer
                print("Use True/False, T/F, 1 for True, or 2 for False.\n")
                continue

            if user_answer:
                return user_answer

            print("Please enter a response.\n")

    def _evaluate_answer(
        self,
        question: dict[str, Any],
        user_answer: str,
    ) -> dict[str, Any]:
        if question["type"] == "mcq":
            return evaluate_mcq_answer(
                user_answer=user_answer,
                correct_answer=question["answer"],
                options=question["options"],
            )

        if question["type"] == "true_false":
            return evaluate_true_false_answer(
                user_answer=user_answer,
                correct_answer=question["answer"],
            )

        return evaluate_descriptive_answer(
            question=question,
            user_answer=user_answer,
            llm_client=self.llm_client,
        )

    def _display_feedback(
        self,
        lesson: dict[str, Any],
        evaluation: dict[str, Any],
    ) -> None:
        print("\nFeedback:")
        print(evaluation["feedback"] or "No feedback returned.")

        if evaluation["is_correct"]:
            return

        print("\nHint:")
        print(lesson["hint"] or "Think about the definition, purpose, and one example.")
        print("\nReference answer:")
        print(lesson["question"]["answer"])
        print("\nExplanation:")
        print(lesson["answer_explanation"] or "Review the core idea and compare it to your answer.")

    def _apply_result(
        self,
        topic_state: dict[str, Any],
        target: dict[str, Any],
        lesson: dict[str, Any],
        user_answer: str,
        evaluation: dict[str, Any],
        elapsed_seconds: float,
    ) -> None:
        self.session["global_turn"] += 1
        topic_state["turns_on_topic"] += 1
        topic_state["updated_at"] = utc_now_iso()

        concept_result = update_concept_mastery(
            topic_state=topic_state,
            concept_id=target["concept_id"],
            is_correct=evaluation["is_correct"],
            question_type=target["question_type"],
        )

        concept = topic_state["concepts"][target["concept_id"]]
        concept["last_seen_turn"] = self.session["global_turn"]

        self.revision_scheduler.schedule(
            topic_state=topic_state,
            concept_id=target["concept_id"],
            current_turn=self.session["global_turn"],
            is_correct=evaluation["is_correct"],
        )
        self.progression_engine.sync_position(topic_state)

        self._add_history(topic_state, "assistant", lesson["message"])
        self._add_history(topic_state, "assistant", lesson["question"]["prompt"])
        self._add_history(topic_state, "user", user_answer)
        self._add_history(topic_state, "assistant", evaluation["feedback"])

        self.analytics_tracker.record_interaction(
            session=self.session,
            topic_state=topic_state,
            elapsed_seconds=elapsed_seconds,
            is_correct=evaluation["is_correct"],
            was_revision=(target["mode"] == "revision"),
        )

        if topic_state["completed"]:
            topic_state["analytics"]["topics_completed"] = 1

        if concept_result["mastered_now"]:
            self.revision_scheduler.clear(topic_state, target["concept_id"])

        self.save_manager.save_session(self.session)

    def _add_history(
        self,
        topic_state: dict[str, Any],
        role: str,
        content: str,
    ) -> None:
        history = topic_state["conversation"]["history"]
        history.append(
            {
                "role": role,
                "content": content.strip(),
            }
        )

        if len(history) <= MAX_HISTORY:
            return

        overflow = len(history) - MAX_HISTORY
        archived = history[:overflow]
        topic_state["conversation"]["history"] = history[overflow:]

        summary_parts = []
        existing_summary = topic_state["conversation"]["summary"]
        if existing_summary:
            summary_parts.append(existing_summary)

        for item in archived[-6:]:
            snippet = item["content"].replace("\n", " ").strip()[:140]
            summary_parts.append(f"{item['role']}: {snippet}")

        topic_state["conversation"]["summary"] = " | ".join(summary_parts)[-1200:]

    def _display_status(self, topic_state: dict[str, Any]) -> None:
        report = build_topic_report(topic_state)
        print("\nProgress snapshot:")
        print(
            f"- Current level: {report['current_level']}\n"
            f"- Confidence: {report['confidence']}\n"
            f"- Accuracy: {report['accuracy']}%\n"
            f"- Learning streak: {report['learning_streak']}\n"
            f"- Concepts mastered: {report['completed_concepts']}\n"
            f"- Revision queue: {report['revision_queue_size']}\n"
            f"- Weak areas: {', '.join(report['weak_areas']) if report['weak_areas'] else 'None'}"
        )
