from models.learning_state import learning_state


def initialize_topic(topic):

    if topic not in learning_state["topics"]:

        learning_state["topics"][topic] = {

            "confidence": 10,

            "difficulty": "Beginner",

            "correct_answers": 0,

            "wrong_answers": 0,

            "weak_areas": [],

            "completed_concepts": [],

            "learning_streak": 0,

            "last_question_type": None
        }


def update_topic_confidence(
    topic,
    is_correct
):

    topic_data = learning_state["topics"][topic]

    if is_correct:

        topic_data["confidence"] += 10

        topic_data["correct_answers"] += 1

        topic_data["learning_streak"] += 1

    else:

        topic_data["confidence"] -= 5

        topic_data["wrong_answers"] += 1

        topic_data["learning_streak"] = 0

    topic_data["confidence"] = max(
        0,
        min(100, topic_data["confidence"])
    )