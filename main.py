from engine.confidence_engine import (
    initialize_topic,
    update_topic_confidence
)

from engine.adaptive_engine import (
    get_difficulty
)

from models.learning_state import (
    learning_state
)

from ai.tutor import (
    generate_lesson
)

from ai.evaluator import (
    evaluate_answer
)

from ai.memory_context import (
    add_to_history
)


print("\n=== AdaptiveTutor AI ===\n")

topic = input("Enter topic: ")

learning_state["current_topic"] = topic

initialize_topic(topic)


while True:

    topic_data = learning_state["topics"][topic]

    difficulty = get_difficulty(topic)

    lesson = generate_lesson(
        topic,
        difficulty
    )

    print("\n" + "=" * 60)

    print(f"Difficulty: {difficulty}")

    print("=" * 60)

    print("\nAdaptiveTutor AI:\n")

    print(lesson["message"])


    concept = lesson["concept"]

    question = lesson["question"]

    print("\nQuestion Type:", question["type"])

    print("\n" + question["question"])


    if question["type"] == "mcq":

        for i, option in enumerate(question["options"]):

            print(f"{i+1}. {option}")

        choice = int(input("\nEnter option number: "))

        user_answer = question["options"][choice - 1]

    else:

        user_answer = input("\nYour Answer: ")


    evaluation = evaluate_answer(

        question["question"],

        question["answer"],

        user_answer
    )

    is_correct = evaluation["is_correct"]


    print("\nFeedback:")
    print(evaluation["feedback"])


    if is_correct:

        print("\n✅ Correct!")

        if concept not in topic_data["completed_concepts"]:

            topic_data["completed_concepts"].append(
                concept
            )

    else:

        print("\n❌ Incorrect!")

        print("\nHint:")
        print(lesson["hint"])

        print("\nCorrect Answer:")
        print(question["answer"])

        print("\nExplanation:")
        print(lesson["answer_explanation"])

        if concept not in topic_data["weak_areas"]:

            topic_data["weak_areas"].append(
                concept
            )


    update_topic_confidence(
        topic,
        is_correct
    )


    add_to_history(
        "assistant",
        lesson["message"]
    )

    add_to_history(
        "user",
        user_answer
    )


    print(
        f"\nConfidence: "
        f"{topic_data['confidence']}"
    )

    print(
        f"Difficulty: "
        f"{get_difficulty(topic)}"
    )

    print(
        f"Learning Streak: "
        f"{topic_data['learning_streak']}"
    )

    print(
        f"Weak Areas: "
        f"{topic_data['weak_areas']}"
    )

    print(
        f"Completed Concepts: "
        f"{topic_data['completed_concepts']}"
    )


    if lesson["recommended_topics"]:

        print("\nRecommended Topics:")

        for rec in lesson["recommended_topics"]:

            print("-", rec)


    cont = input("\nContinue learning? (y/n): ")

    if cont.lower() != "y":

        print("\n👋 Happy Learning!")

        break

