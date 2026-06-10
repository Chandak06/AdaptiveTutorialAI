from models.learning_state import learning_state

from utils.question_types import (
    get_random_question_type
)


def load_prompt(path):

    with open(path, "r", encoding="utf-8") as file:

        return file.read()


def build_prompt(topic, difficulty):

    topic_data = learning_state["topics"][topic]

    weak_areas = topic_data["weak_areas"]

    completed = topic_data["completed_concepts"]

    history = learning_state["conversation_history"][-5:]

    last_question_type = topic_data.get(
        "last_question_type"
    )


    question_type = get_random_question_type(
        last_question_type
    )


    topic_data["last_question_type"] = (
        question_type
    )


    teaching_prompt = load_prompt(
        "prompts/teaching_prompt.txt"
    )


    return teaching_prompt.format(

        topic=topic,

        difficulty=difficulty,

        completed_concepts=completed,

        weak_areas=weak_areas,

        conversation_history=history,

        question_type=question_type
    )
